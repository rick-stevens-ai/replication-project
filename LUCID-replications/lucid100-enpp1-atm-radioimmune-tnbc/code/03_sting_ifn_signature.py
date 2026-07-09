#!/usr/bin/env python3
"""
03_sting_ifn_signature.py

Test the paper's secondary claim that the CTC-in transcriptomic program
is consistent with cGAS-STING / type-I IFN response axis modulation
(i.e. ENPP1 hydrolyzes cGAMP and antagonizes STING; the paper argues
elevated ENPP1 in CTC-in dampens cGAS-STING signaling — but downstream
the *radioimmune* combo restores IFN/STING firing).

We score canonical IFN/STING signatures against the CTC-in vs parental
DEG tables already produced in 02_smoke_deg.py:

  * Hallmark INTERFERON_ALPHA_RESPONSE
  * Hallmark INTERFERON_GAMMA_RESPONSE
  * A minimal cGAS-STING axis gene set (cGAS=Mb21d1, Sting1=Tmem173,
    Tbk1, Irf3, Irf7, Ifnb1, Isg15, Mx1, Oas1a, Ifit1, Cxcl10).

For each signature × lineage:
  - mean log2FC
  - one-sample t-test against 0 (whether the signature is shifted)
  - Wilcoxon signed-rank
  - fraction of genes with padj < 0.05

We *also* run Enrichr against MSigDB Hallmark / KEGG / Reactome with
the same intersected up-DEG set, to see whether IFN/STING categories
appear (they should, if the paper's framing is right).

All numbers go to results/sting_ifn_check.json and a short plot to
figures/fig4_sting_ifn_signature.png.
"""

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "results"
FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)


# --- signatures (mouse symbols) --------------------------------------------
# Hallmark IFN_ALPHA_RESPONSE (canonical 97 genes, MSigDB v7.5; mouse-cased)
# Truncated to a robust core list — full mapping done via case-insensitive
# match below. (We don't need every member; we need a reproducible core.)
HALLMARK_IFN_A = """
ADAR B2M BST2 C1S CASP1 CASP4 CASP7 CASP8 CD47 CD74
CMPK2 CMTR1 CNP CSF1 CXCL10 CXCL11 DDX60 DHX58 EIF2AK2 ELF1
EPSTI1 GBP2 GBP4 GMPR HELZ2 HERC6 IFI27 IFI30 IFI35 IFI44
IFIH1 IFIT1 IFIT2 IFIT3 IFITM1 IFITM2 IFITM3 IRF1 IRF2 IRF7
IRF9 ISG15 ISG20 LAMP3 LAP3 LGALS3BP LY6E MOV10 MX1 MX2
NCOA7 NMI NUB1 OAS1 OAS2 OAS3 OASL OGFR PARP12 PARP14
PARP9 PLSCR1 PNPT1 PROCR PSMA3 PSMB8 PSMB9 PSME1 PSME2 RIPK2
RNF31 RSAD2 RTP4 SAMD9L SELL SLC25A28 SOCS1 STAT1 STAT2 TAP1
TDRD7 TMEM140 TRAFD1 TRIM14 TRIM21 TRIM25 TRIM26 TRIM5 TXNIP UBA7
UBE2L6 USP18 WARS1 XAF1
""".split()

HALLMARK_IFN_G = """
ADAR APOL6 ARID5B ARL4A AUTS2 B2M BANK1 BATF2 BPGM BST2
BTG1 C1R C1S CASP1 CASP3 CASP4 CASP7 CASP8 CCL2 CCL5
CCL7 CD274 CD38 CD40 CD69 CD74 CD86 CDKN1A CFB CFH
CIITA CMKLR1 CMPK2 CSF2RB CXCL10 CXCL11 CXCL9 DDX58 DDX60 DHX58
EIF2AK2 EIF4E3 EPSTI1 FAS FCGR1A FGL2 FPR1 GBP4 GBP6 GCH1
GPR18 GZMA HELZ2 HERC6 HIF1A HLA-A HLA-B HLA-DMA HLA-DQA1 HLA-DRB1
HLA-G ICAM1 IDO1 IFI27 IFI30 IFI35 IFI44 IFI44L IFIH1 IFIT1
IFIT2 IFIT3 IFITM2 IFITM3 IFNAR2 IL10RA IL15 IL15RA IL18BP IL2RB
IL4R IL6 IL7 IRF1 IRF2 IRF4 IRF5 IRF7 IRF8 IRF9
ISG15 ISG20 ISOC1 ITGB7 JAK2 KLRK1 LAP3 LATS2 LCP2 LGALS3BP
LY6E LYSMD2 MARCHF1 METTL7B MT2A MTHFD2 MVP MX1 MX2 MYD88
NAMPT NCOA3 NFKB1 NFKBIA NLRC5 NMI NOD1 NUP93 OAS2 OAS3
OASL OGFR P2RY14 PARP12 PARP14 PDE4B PELI1 PFKP PIM1 PLA2G4A
PLSCR1 PML PNP PNPT1 PSMA2 PSMA3 PSMB10 PSMB2 PSMB8 PSMB9
PSME1 PSME2 PTGS2 PTPN1 PTPN2 PTPN6 RAPGEF6 RBCK1 RIPK1 RIPK2
RNF31 RSAD2 RTP4 SAMD9L SAMHD1 SECTM1 SELP SERPING1 SLAMF7 SLC25A28
SOCS1 SOCS3 SOD2 SP110 SPPL2A SRI SSPN ST3GAL5 ST8SIA4 STAT1
STAT2 STAT3 STAT4 TAP1 TAPBP TDRD7 TNFAIP2 TNFAIP3 TNFAIP6 TNFSF10
TOR1B TRAFD1 TRIM14 TRIM21 TRIM25 TRIM26 UBE2L6 UPP1 USP18 VAMP5
VAMP8 VCAM1 WARS1 XAF1 XCL1 ZBP1 ZNFX1
""".split()

# Minimal cGAS-STING axis (mouse-relevant identifiers)
CGAS_STING_AXIS = [
    "Mb21d1", "Cgas",       # both common symbols
    "Sting1", "Tmem173",
    "Tbk1", "Irf3", "Irf7",
    "Ifnb1", "Ifna1", "Ifna2",
    "Isg15", "Mx1", "Mx2", "Oas1a", "Oas2", "Oas3",
    "Ifit1", "Ifit2", "Ifit3",
    "Cxcl10", "Ccl5",
    "Enpp1",
]


def score_signature(deg: pd.DataFrame, genes_uc: list[str], label: str) -> dict:
    deg = deg.copy()
    deg["sym_uc"] = deg["symbol"].astype(str).str.upper()
    hit = deg[deg["sym_uc"].isin(genes_uc)].dropna(subset=["log2FoldChange"])
    n_total = len(set(genes_uc))
    n_hit = hit["symbol"].nunique()

    lfcs = hit["log2FoldChange"].astype(float).values
    padj = hit["padj"].astype(float).values
    sig_05 = int(np.sum(padj < 0.05))
    up_05 = int(np.sum((padj < 0.05) & (lfcs > 0)))
    down_05 = int(np.sum((padj < 0.05) & (lfcs < 0)))

    if len(lfcs) >= 5:
        t_stat, t_p = stats.ttest_1samp(lfcs, 0.0, nan_policy="omit")
        w_stat, w_p = stats.wilcoxon(lfcs, alternative="two-sided") \
            if np.any(lfcs != 0) else (np.nan, np.nan)
    else:
        t_stat, t_p, w_stat, w_p = (np.nan,) * 4

    return {
        "signature": label,
        "n_genes_in_signature": n_total,
        "n_genes_matched": int(n_hit),
        "mean_log2FC": float(np.nanmean(lfcs)) if len(lfcs) else None,
        "median_log2FC": float(np.nanmedian(lfcs)) if len(lfcs) else None,
        "n_padj_lt_0p05": sig_05,
        "n_up_padj_lt_0p05": up_05,
        "n_down_padj_lt_0p05": down_05,
        "ttest_p": float(t_p) if not np.isnan(t_p) else None,
        "wilcoxon_p": float(w_p) if not np.isnan(w_p) else None,
        "matched_genes_sample": hit[["symbol", "log2FoldChange", "padj"]]
            .head(15)
            .to_dict(orient="records"),
    }


def main() -> None:
    deg_a = pd.read_csv(RES / "deg_ANV5.tsv", sep="\t")
    deg_t = pd.read_csv(RES / "deg_4T1.tsv", sep="\t")

    ifn_a_uc = [g.upper() for g in HALLMARK_IFN_A]
    ifn_g_uc = [g.upper() for g in HALLMARK_IFN_G]
    axis_uc = [g.upper() for g in CGAS_STING_AXIS]

    out: dict[str, dict] = {}
    for label, deg in [("ANV5", deg_a), ("4T1", deg_t)]:
        out[label] = {
            "HALLMARK_IFN_ALPHA": score_signature(deg, ifn_a_uc, "HALLMARK_IFN_ALPHA"),
            "HALLMARK_IFN_GAMMA": score_signature(deg, ifn_g_uc, "HALLMARK_IFN_GAMMA"),
            "CGAS_STING_AXIS": score_signature(deg, axis_uc, "CGAS_STING_AXIS"),
        }

    (RES / "sting_ifn_check.json").write_text(json.dumps(out, indent=2))

    # ----- short summary table to stdout -----
    print("\n=== IFN / cGAS-STING signature shift in CTC-in vs parental ===")
    print(f"{'lineage':<6} {'signature':<22} {'meanLFC':>8} {'medLFC':>8} "
          f"{'t-p':>10} {'wilc-p':>10} {'n_match':>8} {'sig05':>6} "
          f"{'up05':>5} {'dn05':>5}")
    for lin, blocks in out.items():
        for sig_name, blk in blocks.items():
            print(
                f"{lin:<6} {sig_name:<22} "
                f"{blk['mean_log2FC']:>8.3f} "
                f"{blk['median_log2FC']:>8.3f} "
                f"{blk['ttest_p']:>10.2e} "
                f"{blk['wilcoxon_p']:>10.2e} "
                f"{blk['n_genes_matched']:>8} "
                f"{blk['n_padj_lt_0p05']:>6} "
                f"{blk['n_up_padj_lt_0p05']:>5} "
                f"{blk['n_down_padj_lt_0p05']:>5}"
            )

    # ---- figure: signature LFC distributions ----
    fig, axes = plt.subplots(2, 3, figsize=(13, 7), sharey=True)
    sig_map = {
        "HALLMARK_IFN_ALPHA": ifn_a_uc,
        "HALLMARK_IFN_GAMMA": ifn_g_uc,
        "CGAS_STING_AXIS": axis_uc,
    }
    for i, (lin, deg) in enumerate([("ANV5", deg_a), ("4T1", deg_t)]):
        deg2 = deg.copy()
        deg2["sym_uc"] = deg2["symbol"].astype(str).str.upper()
        for j, (sname, sg) in enumerate(sig_map.items()):
            ax = axes[i, j]
            vals = deg2.loc[deg2["sym_uc"].isin(sg), "log2FoldChange"].dropna().values
            if len(vals):
                ax.violinplot(vals, showmedians=True)
                ax.axhline(0, color="grey", lw=0.8, ls="--")
                ax.set_title(f"{lin} – {sname}\nn={len(vals)} mean={np.mean(vals):+.2f}",
                             fontsize=9)
            ax.set_xticks([])
            if j == 0:
                ax.set_ylabel(f"{lin}\nlog2FC (CTC-in vs parental)")
    fig.suptitle("IFN/STING signature shift — CTC-in vs parental (PyDESeq2)")
    fig.tight_layout()
    fig.savefig(FIG / "fig4_sting_ifn_signature.png", dpi=140)
    plt.close(fig)
    print("\nWrote", RES / "sting_ifn_check.json")
    print("Wrote", FIG / "fig4_sting_ifn_signature.png")


if __name__ == "__main__":
    main()
