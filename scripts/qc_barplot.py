import os
os.environ["MPLCONFIGDIR"] = "/data2/lamuyangzong/tmp/matplotlib"
os.environ["NUMBA_CACHE_DIR"] = "/data2/lamuyangzong/tmp/numba_cache"
os.makedirs(os.environ["MPLCONFIGDIR"], exist_ok=True)
os.makedirs(os.environ["NUMBA_CACHE_DIR"], exist_ok=True)

import anndata as ad
import matplotlib.pyplot as plt
import seaborn as sns

os.makedirs("report_figures", exist_ok=True)

h5ad_path = 'HE_grey.h5ad'
adata = ad.read_h5ad(h5ad_path)

tc_lo, tc_hi = adata.obs["total_counts"].quantile(0.025), adata.obs["total_counts"].quantile(0.975)
ng_lo, ng_hi = adata.obs["n_genes_by_counts"].quantile(0.025), adata.obs["n_genes_by_counts"].quantile(0.975)
mt_max = 15.0

fig1, axes1 = plt.subplots(1, 3, figsize=(15, 4))
fig1.suptitle("QC Metrics Distribution (Histogram)", fontsize=14, fontweight="bold")

axes1[0].hist(adata.obs["total_counts"], bins=60, color="#3498db", alpha=0.7, edgecolor="white", lw=0.5)
axes1[0].axvline(tc_lo, color="black", ls="--", lw=1.5, label=f"2.5%: {tc_lo:.0f}")
axes1[0].axvline(tc_hi, color="gray", ls="--", lw=1.5, label=f"97.5%: {tc_hi:.0f}")
axes1[0].set_title("Total UMI counts")
axes1[0].set_xlabel("Total UMI")
axes1[0].legend(fontsize=8)

axes1[1].hist(adata.obs["n_genes_by_counts"], bins=60, color="#2ecc71", alpha=0.7, edgecolor="white", lw=0.5)
axes1[1].axvline(ng_lo, color="black", ls="--", lw=1.5, label=f"2.5%: {ng_lo:.0f}")
axes1[1].axvline(ng_hi, color="gray", ls="--", lw=1.5, label=f"97.5%: {ng_hi:.0f}")
axes1[1].set_title("Genes detected")
axes1[1].set_xlabel("Genes")
axes1[1].legend(fontsize=8)

axes1[2].hist(adata.obs["pct_counts_mt"], bins=60, color="#e74c3c", alpha=0.7, edgecolor="white", lw=0.5)
axes1[2].axvline(mt_max, color="red", ls="-", lw=1.5, label=f"< {mt_max}%")
axes1[2].set_title("MT gene %")
axes1[2].set_xlabel("MT %")
axes1[2].legend(fontsize=8)

for ax in axes1:
    ax.spines[["top", "right"]].set_visible(False)

plt.tight_layout()

hist_path = "report_figures/HE_grey_01_qc_hist.png"
fig1.savefig(hist_path, dpi=150, bbox_inches='tight', facecolor='white')

plt.show()
plt.close(fig1)
print(f"[*] QC 直方图已保存至: {hist_path}")
