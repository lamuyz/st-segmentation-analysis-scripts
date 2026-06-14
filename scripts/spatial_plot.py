import scanpy as sc
import matplotlib.pyplot as plt
import os

# 1. 设置输入文件路径
h5ad_path = 'HE_grey.h5ad'

if not os.path.exists(h5ad_path):
    raise FileNotFoundError(f"找不到输入文件: {h5ad_path}")

adata = sc.read_h5ad(h5ad_path)

# 2. 校验空间坐标系
if 'spatial' not in adata.obsm.keys():
    if 'x' in adata.obs.columns and 'y' in adata.obs.columns:
        adata.obsm['spatial'] = adata.obs[['x', 'y']].values
    else:
        raise ValueError("在 adata.obs 中未找到 'x' 和 'y' 坐标。")

# 3. 渲染空间特征图

# 设置全局绘图参数
sc.set_figure_params(facecolor="white", figsize=(6, 6))

# 执行绘图函数
sc.pl.spatial(
    adata, 
    color=['total_counts', 'n_genes_by_counts', 'pct_counts_mt'], # 依次调用三个核心指标
    cmap='magma',          
    spot_size=15,          
    title=[
        'Total UMIs per Spot', 
        'Total Genes per Spot', 
        'MT Gene % per Spot'
    ],
    frameon=False,         
    vmax='p99',            
    save='spatial_distribution_HE_grey_fluo_raw.pdf', 
    show=True
)
