import scanpy as sc
import matplotlib.pyplot as plt
import os

# Plot spatial distributions of QC metrics from an h5ad file.
# Update the input and output paths before running.

# 1. Set input file path
h5ad_path = "/path/to/input.h5ad"

if not os.path.exists(h5ad_path):
    raise FileNotFoundError(f"Input file not found: {h5ad_path}")

adata = sc.read_h5ad(h5ad_path)

# 2. Check spatial coordinates
if "spatial" not in adata.obsm.keys():
    if "x" in adata.obs.columns and "y" in adata.obs.columns:
        adata.obsm["spatial"] = adata.obs[["x", "y"]].values
    else:
        raise ValueError("No spatial coordinates found in adata.obsm or adata.obs[['x', 'y']].")

# 3. Plot spatial QC metrics
sc.set_figure_params(facecolor="white", figsize=(6, 6))

sc.pl.spatial(
    adata,
    color=["total_counts", "n_genes_by_counts", "pct_counts_mt"],
    cmap="magma",
    spot_size=15,
    title=[
        "Total UMIs per Spot",
        "Total Genes per Spot",
        "MT Gene % per Spot",
    ],
    frameon=False,
    vmax="p99",
    save="spatial_distribution_example.pdf",
    show=True,
)
