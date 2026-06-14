import time
import numpy as np
import pandas as pd
import tifffile
import anndata as ad
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from PIL import Image

# ==============================================================================
# Script: Global Spatial Mapping Visualization (4-Panel View)
# Objective:
#   Generate a 2x2 overview figure using final output files
#   (.h5ad, .tif, .png, .parquet) to check spatial mapping quality.
# ==============================================================================

start_time = time.time()

# 1. Input files
# Update these paths according to the local dataset.
tif_path = "/path/to/registered_image.tif"
mask_path = "/path/to/segmentation_mask.tif"
parquet_path = "/path/to/transcript_counts.parquet"
h5ad_path = "/path/to/expression_matrix.h5ad"

# 2. Read image
Image.MAX_IMAGE_PIXELS = None
img_tif = np.array(Image.open(tif_path))

if img_tif.ndim == 3:
    img_tif = img_tif[:, :, 0]

# 3. Read mask, transcript table, and h5ad object
masks = tifffile.imread(mask_path)
df_raw = pd.read_parquet(parquet_path)
adata = ad.read_h5ad(h5ad_path)

print(f"Data loaded. H5AD object contains {adata.n_obs:,} cells and {adata.n_vars:,} genes.")

fig, axes = plt.subplots(2, 2, figsize=(20, 20))

# --- Panel 1: Raw image ---
ax1 = axes[0, 0]
ax1.imshow(np.max(img_tif) - img_tif, cmap="gray")
ax1.set_title("1. RAW Image, Inverted", fontsize=18)
ax1.axis("off")

# --- Panel 2: Segmentation masks ---
ax2 = axes[0, 1]
ax2.imshow(masks > 0, cmap="gray")
total_rois = len(np.unique(masks)) - 1
ax2.set_title(f"2. Segmentation Masks ({total_rois:,} Total ROIs)", fontsize=18)
ax2.axis("off")

# --- Panel 3: Raw transcript spots ---
ax3 = axes[1, 0]
sampled_df = df_raw.sample(min(100000, len(df_raw)), random_state=42)
ax3.scatter(sampled_df["x"], sampled_df["y"], s=1, c="lightpink", alpha=0.1)
ax3.imshow(np.max(img_tif) - img_tif, cmap="gray", alpha=0.3)
ax3.set_title(f"3. Raw Spots Cloud (100k Sampled from {len(df_raw):,})", fontsize=18)
ax3.axis("off")

# --- Panel 4: Mapped ROIs ---
ax4 = axes[1, 1]
print("Reconstructing mapped spatial mask from h5ad index...")

ax4.imshow(masks > 0, cmap="gray", alpha=0.2)

valid_cell_ids = adata.obs.index.astype(int).values

lookup = np.zeros(masks.max() + 1, dtype=bool)
lookup[valid_cell_ids] = True

mapped_mask = lookup[masks]
mapped_overlay = np.ma.masked_where(~mapped_mask, mapped_mask)

cyan_cmap = ListedColormap(["cyan"])
ax4.imshow(mapped_overlay, cmap=cyan_cmap, alpha=0.6, interpolation="none")
ax4.set_title(f"4. Mapped ROIs: {adata.n_obs:,} Cells containing RNA", fontsize=18)
ax4.axis("off")

# --- Global title ---
mapped_cells = adata.n_obs
mapped_genes = adata.n_vars
total_mapped_counts = int(adata.obs["total_counts"].sum())

plt.suptitle(
    "Spatial Mapping Overview\n"
    f"Mapped Results: {mapped_cells:,} Cells | {mapped_genes:,} Genes | {total_mapped_counts:,} Total UMIs",
    fontsize=24,
)

plt.tight_layout(rect=[0, 0, 1, 0.95])

fig_path = "report_figures/example_spatial_mapping_overview.png"
plt.savefig(fig_path, dpi=150, bbox_inches="tight", facecolor="white")

plt.show()
plt.close(fig)

print(f"Spatial mapping overview saved to: {fig_path}")
print(f"Visualization completed in {time.time() - start_time:.1f} seconds.")
```
