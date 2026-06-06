import anndata as ad
import pandas as pd
import numpy as np

# ================= 1. 读取数据 =================
h5ad_file = "HE_grey.h5ad"
adata = ad.read_h5ad(h5ad_file)

# ================= 2. 计算各项指标 =================
total_cells = adata.n_obs
total_umis = adata.obs['total_counts'].sum()
mean_umi = adata.obs['total_counts'].mean()
median_umi = adata.obs['total_counts'].median()
mean_genes = adata.obs['n_genes_by_counts'].mean()
median_genes = adata.obs['n_genes_by_counts'].median()

# 线粒体比例统计
mean_mt = adata.obs['pct_counts_mt'].mean()
median_mt = adata.obs['pct_counts_mt'].median()

# ================= 3. 构建统计表格 =================
qc_summary = pd.DataFrame({
    "指标": [
        "细胞总数", 
        "总UMI数", 
        "平均UMI/细胞", 
        "中位数UMI/细胞", 
        "平均基因/细胞",
        "中位数基因/细胞",
        "平均线粒体比例",
        "中位数线粒体比例"
    ],
    "Control_数值": [
        f"{total_cells:,}",
        f"{total_umis:,.0f}",
        f"{mean_umi:,.0f}",
        f"{median_umi:,.0f}",
        f"{mean_genes:,.0f}",
        f"{median_genes:,.0f}",
        f"{mean_mt:.2f}%",
        f"{median_mt:.2f}%"
    ]
})

# ================= 4. 打印表格 =================
print("\n========== 数据集基础质控统计表 ==========")
print(qc_summary.to_string(index=False))
