import os
os.environ["MPLCONFIGDIR"] = "/data2/lamuyangzong/tmp/matplotlib"
os.environ["NUMBA_CACHE_DIR"] = "/data2/lamuyangzong/tmp/numba_cache"
os.makedirs(os.environ["MPLCONFIGDIR"], exist_ok=True)
os.makedirs(os.environ["NUMBA_CACHE_DIR"], exist_ok=True)

import anndata as ad
import matplotlib.pyplot as plt
import seaborn as sns

h5ad_path = 'HE_grey.h5ad'
adata = ad.read_h5ad(h5ad_path)

tc_lo = adata.obs["total_counts"].quantile(0.025)
tc_hi = adata.obs["total_counts"].quantile(0.975)
ng_lo = adata.obs["n_genes_by_counts"].quantile(0.025)
ng_hi = adata.obs["n_genes_by_counts"].quantile(0.975)
mt_max = 15.0

fig2, axes2 = plt.subplots(1, 3, figsize=(15, 5))
fig2.suptitle("QC Metrics Distribution (Violin Plot)", fontsize=14, fontweight="bold", y=1.05)

sns.violinplot(y=adata.obs["total_counts"], ax=axes2[0], color="#3498db", inner="quartile", alpha=0.7)
sns.stripplot(y=adata.obs["total_counts"], ax=axes2[0], color="black", size=1.5, alpha=0.1, jitter=0.3)
axes2[0].axhline(y=tc_lo, color='red', linestyle='--', linewidth=1.5, label=f'Min (2.5%): {tc_lo:.0f}')
axes2[0].axhline(y=tc_hi, color='darkred', linestyle='--', linewidth=1.5, label=f'Max (97.5%): {tc_hi:.0f}')
axes2[0].set_title("Total UMI counts")
axes2[0].set_ylabel("Total UMI")
axes2[0].set_xticks([])
axes2[0].legend(loc='upper right', fontsize=9)

sns.violinplot(y=adata.obs["n_genes_by_counts"], ax=axes2[1], color="#2ecc71", inner="quartile", alpha=0.7)
sns.stripplot(y=adata.obs["n_genes_by_counts"], ax=axes2[1], color="black", size=1.5, alpha=0.1, jitter=0.3)
axes2[1].axhline(y=ng_lo, color='red', linestyle='--', linewidth=1.5, label=f'Min (2.5%): {ng_lo:.0f}')
axes2[1].axhline(y=ng_hi, color='darkred', linestyle='--', linewidth=1.5, label=f'Max (97.5%): {ng_hi:.0f}')
axes2[1].set_title("Genes detected")
axes2[1].set_ylabel("Genes")
axes2[1].set_xticks([])
axes2[1].legend(loc='upper right', fontsize=9)

sns.violinplot(y=adata.obs["pct_counts_mt"], ax=axes2[2], color="#e74c3c", inner="quartile", alpha=0.7)
sns.stripplot(y=adata.obs["pct_counts_mt"], ax=axes2[2], color="black", size=1.5, alpha=0.1, jitter=0.3)
axes2[2].axhline(y=mt_max, color='darkred', linestyle='-', linewidth=2, label=f'Threshold: < {mt_max}%')
axes2[2].set_title("MT gene %")
axes2[2].set_ylabel("MT %")
axes2[2].set_xticks([])
axes2[2].legend(loc='upper right', fontsize=9)

for ax in axes2:
    ax.spines[["top", "right", "bottom"]].set_visible(False)
    ax.set_xlabel("")

plt.tight_layout()

violin_path = "report_figures/HE_grey_02_qc_violin.png"
fig2.savefig(violin_path, dpi=150, bbox_inches='tight', facecolor='white')

plt.show()
plt.close(fig2)
print(f"[*] QC 小提琴图已保存至: {violin_path}")

qc_mask = (
    (adata.obs["total_counts"] >= tc_lo) &
    (adata.obs["total_counts"] <= tc_hi) &
    (adata.obs["n_genes_by_counts"] >= ng_lo) &
    (adata.obs["n_genes_by_counts"] <= ng_hi) &
    (adata.obs["pct_counts_mt"] < mt_max)
)
adata_qc = adata[qc_mask].copy()
qc_h5ad = 'HE_grey_QC.h5ad'
adata_qc.write(qc_h5ad)
print(f"[*] QC 后保留 {adata_qc.n_obs:,}/{adata.n_obs:,} 个细胞，已保存至: {qc_h5ad}")
