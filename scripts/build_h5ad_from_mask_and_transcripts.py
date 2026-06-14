import time

import numpy as np
import pandas as pd
import tifffile
import anndata as ad
from scipy.sparse import csr_matrix

start_time = time.time()
print("Step 1: Initializing data loading...")

# Input files
# Update these paths according to the local dataset.
mask_path = "/path/to/segmentation_mask.tif"
parquet_path = "/path/to/transcript_counts.parquet"
output_h5ad = "/path/to/output_expression_matrix.h5ad"

# Load segmentation mask
masks = tifffile.imread(mask_path)
max_y, max_x = masks.shape
print(f"Segmentation mask loaded. Dimensions: Y={max_y}, X={max_x}")

# Load spatial transcriptomic spots data
df = pd.read_parquet(parquet_path)
print(f"Transcriptomic spots data loaded. Total records: {len(df):,}")

print("\nStep 2: Spatial coordinate mapping...")

# Round spatial coordinates for mask indexing
df["x_int"] = df["x"].round().astype(int)
df["y_int"] = df["y"].round().astype(int)

# Filter out-of-bounds coordinates
valid_mask = (
    (df["x_int"] >= 0) &
    (df["x_int"] < max_x) &
    (df["y_int"] >= 0) &
    (df["y_int"] < max_y)
)

df_valid = df[valid_mask].copy()

# Map transcript coordinates to ROI IDs in the segmentation mask.
# Note: NumPy indexing order is [y, x].
df_valid["cell_id"] = masks[df_valid["y_int"].values, df_valid["x_int"].values]

# Remove transcripts mapped to background regions.
df_cells = df_valid[df_valid["cell_id"] > 0]

print(
    f"Successfully mapped {len(df_cells):,} transcriptomic spots "
    f"to {df_cells['cell_id'].nunique():,} segmented ROIs."
)

print("\nStep 3: Aggregating counts and constructing AnnData object...")

# Aggregate UMI counts for each cell-gene pair
matrix_df = df_cells.groupby(["cell_id", "gene"])["counts"].sum().reset_index()

# Use categorical encoding to construct the sparse matrix
cells = matrix_df["cell_id"].astype("category")
genes = matrix_df["gene"].astype("category")

# Construct sparse expression matrix
X_sparse = csr_matrix(
    (
        matrix_df["counts"].values,
        (cells.cat.codes.values, genes.cat.codes.values),
    )
)

# Initialize AnnData object
obs = pd.DataFrame(index=cells.cat.categories.astype(str))
var = pd.DataFrame(index=genes.cat.categories.astype(str))
adata = ad.AnnData(X=X_sparse, obs=obs, var=var)

print("\nStep 4: Calculating QC metrics and spatial information...")

# Gene-level information
adata.var["gene_name"] = adata.var_names
adata.var["n_cells"] = np.array((adata.X > 0).sum(axis=0)).flatten()
adata.var["n_counts"] = np.array(adata.X.sum(axis=0)).flatten()

# Cell centroid coordinates
spatial_coords = df_cells.groupby("cell_id")[["x", "y"]].mean()
spatial_aligned = spatial_coords.loc[cells.cat.categories]

adata.obs["x"] = spatial_aligned["x"].values
adata.obs["y"] = spatial_aligned["y"].values
adata.obsm["spatial"] = spatial_aligned[["x", "y"]].values

# Cell-level QC metrics
adata.obs["total_counts"] = np.array(adata.X.sum(axis=1)).flatten()
adata.obs["n_genes_by_counts"] = np.array((adata.X > 0).sum(axis=1)).flatten()

# Mitochondrial percentage
is_mt = adata.var_names.str.lower().str.startswith("mt-")
mt_counts = np.array(adata.X[:, is_mt].sum(axis=1)).flatten()

adata.obs["pct_counts_mt"] = np.divide(
    mt_counts * 100,
    adata.obs["total_counts"].values,
    out=np.zeros_like(mt_counts, dtype=float),
    where=adata.obs["total_counts"].values != 0,
)

print(f"\nPipeline completed in {time.time() - start_time:.1f} seconds.")
print("AnnData object summary:")
print(adata)

print("\nPreview of adata.obs:")
print(adata.obs.head())

adata.write(output_h5ad)
print(f"\nData successfully saved to: {output_h5ad}")

