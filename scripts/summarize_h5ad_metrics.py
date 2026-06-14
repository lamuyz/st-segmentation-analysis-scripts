import anndata as ad
import pandas as pd
import numpy as np

# Summarize basic QC metrics from an h5ad file.
# Update the input path before running.

# ================= 1. Read data =================
h5ad_file = "/path/to/input.h5ad"
adata = ad.read_h5ad(h5ad_file)

# ================= 2. Calculate QC metrics =================
total_cells = adata.n_obs
total_umis = adata.obs["total_counts"].sum()
mean_umi = adata.obs["total_counts"].mean()
median_umi = adata.obs["total_counts"].median()
mean_genes = adata.obs["n_genes_by_counts"].mean()
median_genes = adata.obs["n_genes_by_counts"].median()

mean_mt = adata.obs["pct_counts_mt"].mean()
median_mt = adata.obs["pct_counts_mt"].median()

# ================= 3. Build summary table =================
qc_summary = pd.DataFrame({
    "Metric": [
        "Total cells",
        "Total UMIs",
        "Mean UMIs per cell",
        "Median UMIs per cell",
        "Mean genes per cell",
        "Median genes per cell",
        "Mean mitochondrial percentage",
        "Median mitochondrial percentage",
    ],
    "Value": [
        f"{total_cells:,}",
        f"{total_umis:,.0f}",
        f"{mean_umi:,.0f}",
        f"{median_umi:,.0f}",
        f"{mean_genes:,.0f}",
        f"{median_genes:,.0f}",
        f"{mean_mt:.2f}%",
        f"{median_mt:.2f}%",
    ],
})

# ================= 4. Print summary table =================
print("\n========== Basic QC Summary ==========")
print(qc_summary.to_string(index=False))
