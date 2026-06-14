import pandas as pd
import numpy as np
import tifffile
import anndata as ad
from scipy.sparse import csr_matrix

start_time = time.time()
print("Step 1: Initializing data loading...")

# 加载分割掩码 (Segmentation Mask)
mask_path = 'C04042E3_HE_grey_masks.tif' 
masks = tifffile.imread(mask_path)
max_y, max_x = masks.shape
print(f"Segmentation mask loaded. Dimensions: Y={max_y}, X={max_x}")

# 加载空间转录组散点数据 (Spatial transcriptomic spots data)
df = pd.read_parquet('HE_bin1_counts.parquet')
print(f"Transcriptomic spots data loaded. Total records: {len(df):,}")

print("\nStep 2: Spatial coordinate mapping...")

# 提取并四舍五入空间坐标，用于矩阵索引映射
df['x_int'] = df['x'].round().astype(int)
df['y_int'] = df['y'].round().astype(int)

# 过滤越界坐标 (Out-of-bounds filtering)
valid_mask = (df['x_int'] >= 0) & (df['x_int'] < max_x) & \
             (df['y_int'] >= 0) & (df['y_int'] < max_y)
df_valid = df[valid_mask].copy()

# 将转录本坐标映射至掩码矩阵获取对应的 ROI ID (注: Numpy 索引顺序为 [y, x])
df_valid['cell_id'] = masks[df_valid['y_int'].values, df_valid['x_int'].values]

# 剔除映射至背景 (cell_id == 0) 的环境游离 RNA
df_cells = df_valid[df_valid['cell_id'] > 0]
print(f"Successfully mapped {len(df_cells):,} transcriptomic spots to {df_cells['cell_id'].nunique():,} segmented ROIs.")

print("\nStep 3: Aggregating counts and constructing AnnData object...")

# 1. 聚合计算每个 ROI 内各基因的 UMI 总数
matrix_df = df_cells.groupby(['cell_id', 'gene'])['counts'].sum().reset_index()

# 2. 分类变量编码优化内存
cells = matrix_df['cell_id'].astype('category')
genes = matrix_df['gene'].astype('category')

# 3. 构建压缩稀疏行矩阵 (CSR)
X_sparse = csr_matrix((matrix_df['counts'].values, (cells.cat.codes.values, genes.cat.codes.values)))

# 4. 初始化 AnnData 
obs = pd.DataFrame(index=cells.cat.categories.astype(str)) 
var = pd.DataFrame(index=genes.cat.categories.astype(str)) 
adata = ad.AnnData(X=X_sparse, obs=obs, var=var)

print("\nStep 4: Calculating customized QC metrics and spatial info...")

# ======================= [新增] var 层面信息计算 =======================
# 基因名
adata.var["gene_name"] = adata.var_names 
# 表达该基因的细胞数 (将 > 0 的布尔矩阵按列求和)
adata.var["n_cells"] = np.array((adata.X > 0).sum(axis=0)).flatten()
# 该基因的总 UMI (将表达量按列求和)
adata.var["n_counts"] = np.array(adata.X.sum(axis=0)).flatten()


# ======================= [新增] obs 层面信息计算 =======================
# 计算物理质心坐标
spatial_coords = df_cells.groupby('cell_id')[['x', 'y']].mean()
spatial_aligned = spatial_coords.loc[cells.cat.categories]

# 1. 将坐标写入 obs
adata.obs["x"] = spatial_aligned['x'].values
adata.obs["y"] = spatial_aligned['y'].values
# (强烈建议同时保留在 obsm['spatial'] 中，这是绝大多数空间转录组下游软件的默认标准)
adata.obsm['spatial'] = spatial_aligned[['x', 'y']].values 

# 2. 每个细胞的总 UMI (按行求和)
adata.obs["total_counts"] = np.array(adata.X.sum(axis=1)).flatten()

# 3. 表达的基因数 (按行统计 > 0 的元素个数)
adata.obs["n_genes_by_counts"] = np.array((adata.X > 0).sum(axis=1)).flatten()

# 4. 线粒体比例 pct_counts_mt 
# 判断是否为线粒体基因 (通常以 MT- 或 mt- 开头，这里使用忽略大小写的方法)
is_mt = adata.var_names.str.lower().str.startswith('mt-')
# 提取线粒体基因在每个细胞的表达量并求和
mt_counts = np.array(adata.X[:, is_mt].sum(axis=1)).flatten()
# 计算百分比 (防范除零错误)
adata.obs["pct_counts_mt"] = np.divide(
    mt_counts * 100, 
    adata.obs["total_counts"].values, 
    out=np.zeros_like(mt_counts, dtype=float), 
    where=adata.obs["total_counts"].values != 0
)
# ======================================================================

print(f"\nPipeline completed in {time.time()-start_time:.1f} seconds.")
print("AnnData object summary:")
print(adata)
print("\nPreview of adata.obs:")
print(adata.obs.head())

# 序列化保存至本地
output_h5ad = 'HE_grey.h5ad'
adata.write(output_h5ad)
print(f"\nData successfully saved to: {output_h5ad}")
