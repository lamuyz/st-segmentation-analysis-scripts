import os

# Temporary cache directories.
# Update these paths according to the local computing environment.
os.environ["MPLCONFIGDIR"] = "/path/to/tmp/matplotlib"
os.environ["NUMBA_CACHE_DIR"] = "/path/to/tmp/numba_cache"

os.makedirs(os.environ["MPLCONFIGDIR"], exist_ok=True)
os.makedirs(os.environ["NUMBA_CACHE_DIR"], exist_ok=True)

import anndata as ad
import matplotlib.pyplot as plt
import seaborn as sns

# Input file
h5ad_path = "/path/to/input.h5ad"
adata = ad.read_h5ad(h5ad_path)

# QC thresholds
tc_lo = adata.obs["total_counts"].quantile(0.025)
tc_hi = adata.obs["total_counts"].quantile(0.975)
ng_lo = adata.obs["n_genes_by_counts"].quantile(0.025)
ng_hi = adata.obs["n_genes_by_counts"].quantile(0.975)
mt_max = 15.0

# Plot violin plots of QC metrics
fig2, axes2 = plt.subplots(1, 3, figsize=(15, 5))
fig2.suptitle("QC Metrics Distribution (Violin Plot)", fontsize=14, fontweight="bold", y=1.05)

sns.violinplot(y=adata.obs["total_counts"], ax=axes2[0], color="#3498db", inner="quartile", alpha=0.7)
sns.stripplot(y=adata.obs["total_counts"], ax=axes2[0], color="black", size=1.5, alpha=0.1, jitter=0.3)
axes2[0].axhline(y=tc_lo, color="red", linestyle="--", linewidth=1.5, label=f"Min (2.5%): {tc_lo:.0f}")
axes2[0].axhline(y=tc_hi, color="darkred", linestyle="--", linewidth=1.5, label=f"Max (97.5%): {tc_hi:.0f}")
axes2[0].set_title("Total UMI counts")
axes2[0].set_ylabel("Total UMI")
axes2[0].set_xticks([])
axes2[0].legend(loc="upper right", fontsize=9)

sns.violinplot(y=adata.obs["n_genes_by_counts"], ax=axes2[1], color="#2ecc71", inner="quartile", alpha=0.7)
sns.stripplot(y=adata.obs["n_genes_by_counts"], ax=axes2[1], color="black", size=1.5, alpha=0.1, jitter=0.3)
axes2[1].axhline(y=ng_lo, color="red", linestyle="--", linewidth=1.5, label=f"Min (2.5%): {ng_lo:.0f}")
axes2[1].axhline(y=ng_hi, color="darkred", linestyle="--", linewidth=1.5, label=f"Max (97.5%): {ng_hi:.0f}")
axes2[1].set_title("Genes detected")
axes2[1].set_ylabel("Genes")
axes2[1].set_xticks([])
axes2[1].legend(loc="upper right", fontsize=9)

sns.violinplot(y=adata.obs["pct_counts_mt"], ax=axes2[2], color="#e74c3c", inner="quartile", alpha=0.7)
sns.stripplot(y=adata.obs["pct_counts_mt"], ax=axes2[2], color="black", size=1.5, alpha=0.1, jitter=0.3)
axes2[2].axhline(y=mt_max, color="darkred", linestyle="-", linewidth=2, label=f"Threshold: < {mt_max}%")
axes2[2].set_title("MT gene %")
axes2[2].set_ylabel("MT %")
axes2[2].set_xticks([])
axes2[2].legend(loc="upper right", fontsize=9)

for ax in axes2:
    ax.spines[["top", "right", "bottom"]].set_visible(False)
    ax.set_xlabel("")

plt.tight_layout()

os.makedirs("report_figures", exist_ok=True)
violin_path = "report_figures/example_qc_violin.png"
fig2.savefig(violin_path, dpi=150, bbox_inches="tight", facecolor="white")

plt.show()
plt.close(fig2)
print(f"QC violin plot saved to: {violin_path}")

# Apply QC filtering
qc_mask = (
    (adata.obs["total_counts"] >= tc_lo) &
    (adata.obs["total_counts"] <= tc_hi) &
    (adata.obs["n_genes_by_counts"] >= ng_lo) &
    (adata.obs["n_genes_by_counts"] <= ng_hi) &
    (adata.obs["pct_counts_mt"] < mt_max)
)

adata_qc = adata[qc_mask].copy()

qc_h5ad = "example_qc_filtered.h5ad"
adata_qc.write(qc_h5ad)

print(f"QC retained {adata_qc.n_obs:,}/{adata.n_obs:,} cells, saved to: {qc_h5ad}")
