import numpy as np
import pandas as pd
import tifffile
import anndata as ad
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from PIL import Image

# ==============================================================================
# Script: Global Spatial Mapping Visualization (4-Panel View)
# Objective: Generate a comprehensive 2x2 panel using final output files
#            (.h5ad, .tif, .png, .parquet) to illustrate spatial mapping QC.
# ==============================================================================

# 1. 加载数据文件 (请根据实际情况修改路径)
tif_path = 'C04042E3_HE_regist.tif'
mask_path = 'C04042E3_HE_grey_masks.tif' 
parquet_path = 'HE_bin1_counts.parquet'
h5ad_path = 'HE_grey.h5ad'

# 读取底图
Image.MAX_IMAGE_PIXELS = None
img_tif = np.array(Image.open(tif_path))
if img_tif.ndim == 3:
    img_tif = img_tif[:, :, 0] # 转换为单通道灰度图

# 读取分割掩码和点数据
masks = tifffile.imread(mask_path)
df_raw = pd.read_parquet(parquet_path)

# 读取 h5ad 对象
adata = ad.read_h5ad(h5ad_path)

print(f"Data loaded. H5AD object contains {adata.n_obs:,} cells and {adata.n_vars:,} genes.")

fig, axes = plt.subplots(2, 2, figsize=(20, 20))

# --- Panel 1 (Top-Left): Nissl (RAW Image, Inverted) ---
ax1 = axes[0, 0]
ax1.imshow(np.max(img_tif) - img_tif, cmap='gray')
ax1.set_title("1. RAW Image, Inverted", fontsize=18)
ax1.axis('off')

# --- Panel 2 (Top-Right): Segmentation Masks (Binary View) ---
ax2 = axes[0, 1]
# 使用二值化处理展示物理边界
ax2.imshow(masks > 0, cmap='gray')
total_rois = len(np.unique(masks)) - 1 # 减去背景 0
ax2.set_title(f"2. Segmentation Masks ({total_rois:,} Total ROIs)", fontsize=18)
ax2.axis('off')

# --- Panel 3 (Bottom-Left): Raw Spots Cloud ---
ax3 = axes[1, 0]
# 从原始 parquet 中随机抽样 10 万点优化渲染
sampled_df = df_raw.sample(min(100000, len(df_raw)), random_state=42) 
ax3.scatter(sampled_df['x'], sampled_df['y'], s=1, c='lightpink', alpha=0.1)
ax3.imshow(np.max(img_tif) - img_tif, cmap='gray', alpha=0.3) 
ax3.set_title(f"3. Raw Spots Cloud (100k Sampled from {len(df_raw):,})", fontsize=18)
ax3.axis('off')

# --- Panel 4 (Bottom-Right): Spatial Mapping (Monochromatic) ---
ax4 = axes[1, 1]
print("Reconstructing mapped spatial mask from h5ad index...")

# 1. 绘制底层灰色 Mask (作为参照)
ax4.imshow(masks > 0, cmap='gray', alpha=0.2) 

# 2. 从 h5ad.obs.index 提取成功映射并包含基因表达的 细胞ID
valid_cell_ids = adata.obs.index.astype(int).values

# 3. 构建一个快速查找表 (Lookup Table) 
# 如果 mask 中的像素值在 valid_cell_ids 中，则为 True
lookup = np.zeros(masks.max() + 1, dtype=bool)
lookup[valid_cell_ids] = True

# 4. 生成仅包含有效细胞的 Mask
mapped_mask = lookup[masks]

# 5. 按照你的要求，严格使用单色 (Cyan) 避免渐变误导
# 使用 numpy 的掩码数组 (Masked Array)，把没有数据的地方变透明
mapped_overlay = np.ma.masked_where(~mapped_mask, mapped_mask)
cyan_cmap = ListedColormap(['cyan'])

ax4.imshow(mapped_overlay, cmap=cyan_cmap, alpha=0.6, interpolation='none')
ax4.set_title(f"4. Mapped ROIs: {adata.n_obs:,} Cells containing RNA", fontsize=18)
ax4.axis('off')

# --- 全局标题 (Global Title) ---
mapped_cells = adata.n_obs
mapped_genes = adata.n_vars
total_mapped_counts = int(adata.obs['total_counts'].sum())

plt.suptitle(f"Stereoseq_HE Spatial Mapping Overview \n"
             f"Mapped Results: {mapped_cells:,} Cells | {mapped_genes:,} Genes | {total_mapped_counts:,} Total UMIs", 
             fontsize=24)

# 动态调整边距
plt.tight_layout(rect=[0, 0, 1, 0.95]) 
plt.show()

print(f"\nVisualization completed in {time.time()-start_time:.1f} seconds.")
