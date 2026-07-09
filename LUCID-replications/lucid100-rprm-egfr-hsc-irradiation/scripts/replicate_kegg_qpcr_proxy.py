#!/usr/bin/env python3
"""
LUCID-100 cross-paper proxy replication for Li et al. 2022 (cbin.11900).

Paper's only computational asset (Figure 4a KEGG bubble + Figure 4b qPCR) was
generated from BGI-commissioned RNA-seq of FACS-sorted LSK cells, n=3/group,
1 h post 4 Gy. **That dataset was NOT deposited.** The data-availability
statement is "available from the corresponding author upon reasonable request"
and our task forbids author contact.

PROXY DATASET: GSE244971 (Chen X et al., Army Medical University, China; PubMed
38802843; public 2024-06-05). Sorted mouse HSC (Lineage-Sca-1+c-Kit+Flt3-CD34-)
from 8-week WT mice, 3 conditions × 3 reps:
  - Ctrl  : unirradiated
  - IR    : total-body irradiation
  - L_IR  : locally irradiated leg
  - Ab_IR : opposite (un-irradiated) leg of locally-irradiated mouse (abscopal)
Timepoint: 3 days post-IR (paper used 1 h post-IR — direction-only proxy).
Normalization: looks like FPKM-ish (per-sample sums 344K-405K).

This is NOT a replication of Li 2022 — it is a public proxy that tests whether
the *direction* of the paper's qPCR-validated inflammation and EGFR/Lin28a
claims is consistent in an independent WT-only HSC + IR dataset, in the
absence of the RPRM KO arm.

What we test:
  Claim block (Fig 4b qPCR + Fig 4a KEGG): IR upregulates IL-1α, IL-1β, TNF-α,
  IL-13, MCP-1 in WT LSKs (this is the WT side of the WT-vs-KO comparison —
  paper shows these are HIGHER in WT post-IR than KO post-IR, which implies
  IR-induced upregulation that KO blunts).

  Claim block (Fig 4c-f): EGFR and Lin28a are higher in KO LSKs than WT LSKs
  1 h post-IR (we cannot test the KO comparison; instead we ask whether IR
  shifts EGFR/Lin28a/Xrcc6 at all in WT HSCs).

  Claim (paper Sec 3.1): RPRM mRNA is expressed in WT HSCs (paper Fig 2a
  shows induction in WT after IR; in KO it is ablated).

OUTPUT: results/cross_check_GSE244971.json with per-gene IR/Ctrl ratios,
t-test p-values, and a direction-consistency verdict per claim.

Local + free. No paid endpoints. ~31k genes × 12 samples; runs in seconds.
"""
import os
import json
import math
import statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DATA = ROOT / "data"
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)

SAMPLES = {
    "Ctrl": ["GSM7832911_Ctrl_HSC_rep1.txt", "GSM7832912_Ctrl_HSC_rep2.txt", "GSM7832913_Ctrl_HSC_rep3.txt"],
    "IR":   ["GSM7832914_IR_HSC_rep1.txt",   "GSM7832915_IR_HSC_rep2.txt",   "GSM7832916_IR_HSC_rep3.txt"],
    "Ab_IR":["GSM7832917_Ab_IR_HSC_rep1.txt","GSM7832918_Ab_IR_HSC_rep2.txt","GSM7832919_Ab_IR_HSC_rep3.txt"],
    "L_IR": ["GSM7832920_L_IR_HSC_rep1.txt", "GSM7832921_L_IR_HSC_rep2.txt", "GSM7832922_L_IR_HSC_rep3.txt"],
}

# Genes of interest (paper Fig 4 qPCR set + key mechanistic genes)
# Note: paper writes Ccl11 / MCP-1 / IL-13; mouse symbols are Ccl11, Ccl2 (=MCP-1), Il13.
GENES_PAPER = {
    "Ccl11":  "Fig4b qPCR inflammation",
    "Il13":   "Fig4b qPCR inflammation",
    "Tnf":    "Fig4b qPCR inflammation (TNF-α)",
    "Rprm":   "Fig2a — RPRM mRNA",
    "Il1a":   "Fig4b qPCR inflammation",
    "Il1b":   "Fig4b qPCR inflammation",
    "Ccl2":   "Fig4b qPCR inflammation (MCP-1 = Ccl2)",
    "Lin28a": "Fig4c-d, g — Lin28a",
    "Egfr":   "Fig4c-d, e-f — EGFR / p-EGFR",
    "Xrcc6":  "Fig3h — Xrcc6 (Ku70) NHEJ factor",
    # Additional mechanistic anchors mentioned in Discussion
    "Prkdc":  "DNA-PKcs catalytic subunit (paper studies p-DNA-PKcs phosphorylation)",
    "Stat3":  "EGFR-STAT3-Lin28a axis (Sec 3.4-3.5)",
    "Atm":    "ATM — paper's prior work (Zhang 2021) says RPRM neg-regulates ATM",
    "H2ax":   "γ-H2AX is H2AX (Hist1h2ax in mouse)",  # likely H2ax not in this annotation
    "H2afx":  "γ-H2AX gene symbol (mouse)",
    "Trp53":  "p53 — RPRM is p53 target",
    "Cdkn1a": "p21 — p53 target",
}


def load_sample(path):
    """Load gene -> expression dict from a GEO HSC txt file."""
    d = {}
    with open(path) as f:
        next(f)  # header
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 2:
                continue
            g, v = parts[0], parts[1]
            try:
                d[g] = float(v)
            except ValueError:
                pass
    return d


def welch_t(a, b):
    """Welch's t-test (returns t, df, two-sided p approx). Pure-Python stats only."""
    n1, n2 = len(a), len(b)
    if n1 < 2 or n2 < 2:
        return float("nan"), float("nan"), float("nan")
    m1, m2 = statistics.mean(a), statistics.mean(b)
    v1, v2 = statistics.variance(a), statistics.variance(b)
    if v1 == 0 and v2 == 0:
        return 0.0, float("nan"), 1.0
    se = math.sqrt(v1 / n1 + v2 / n2)
    if se == 0:
        return float("inf"), float("nan"), 0.0
    t = (m1 - m2) / se
    # Welch-Satterthwaite df
    df_num = (v1 / n1 + v2 / n2) ** 2
    df_den = ((v1 / n1) ** 2 / max(n1 - 1, 1)) + ((v2 / n2) ** 2 / max(n2 - 1, 1))
    df = df_num / df_den if df_den else float("nan")
    # Approximate two-sided p via Student's t survival.
    # Use a Hill (1970)-style approximation good for small df.
    # For honesty about small-n: report t and df; compute p via scipy-free
    # Abramowitz-Stegun continued fraction is overkill for n=3, so use:
    # p ~ 2 * (1 - Φ(|t|)) for df>=30; otherwise note df explicitly.
    if df != df:  # NaN
        return t, df, float("nan")
    # Crude bounding p-value using normal approx (will be conservative for small df).
    z = abs(t)
    # Normal CDF approx via erf
    p_norm = math.erfc(z / math.sqrt(2.0))
    return t, df, p_norm  # NOTE: p_norm is a normal-approx; small-df p is larger.


def collect():
    samples = {}
    for cond, files in SAMPLES.items():
        samples[cond] = [load_sample(DATA / f) for f in files]
    return samples


def main():
    samples = collect()
    gene_set = set()
    for reps in samples.values():
        for d in reps:
            gene_set.update(d.keys())

    per_gene = {}
    for gene, note in GENES_PAPER.items():
        # mouse-style capitalization first; fall back to case-insensitive
        matches = [g for g in gene_set if g == gene]
        if not matches:
            ci = [g for g in gene_set if g.lower() == gene.lower()]
            matches = ci[:1]
        if not matches:
            per_gene[gene] = {"note": note, "found": False}
            continue
        mg = matches[0]
        per_gene[gene] = {"note": note, "found": True, "mouse_symbol": mg}
        for cond, reps in samples.items():
            vals = [d.get(mg, 0.0) for d in reps]
            per_gene[gene][cond] = {
                "values": vals,
                "mean": statistics.mean(vals),
                "stdev": statistics.stdev(vals) if len(vals) > 1 else 0.0,
            }
        # IR vs Ctrl fold change + t-test
        ctrl_vals = [d.get(mg, 0.0) for d in samples["Ctrl"]]
        ir_vals = [d.get(mg, 0.0) for d in samples["IR"]]
        m_ctrl = statistics.mean(ctrl_vals)
        m_ir = statistics.mean(ir_vals)
        # log2FC with small-value pseudocount
        eps = 0.01
        log2fc = math.log2((m_ir + eps) / (m_ctrl + eps))
        t, df, p = welch_t(ir_vals, ctrl_vals)
        per_gene[gene]["IR_vs_Ctrl"] = {
            "mean_ctrl": m_ctrl,
            "mean_ir": m_ir,
            "log2FC_IR_over_Ctrl": log2fc,
            "fold_change_IR_over_Ctrl": (m_ir + eps) / (m_ctrl + eps),
            "welch_t": t,
            "welch_df": df,
            "p_normal_approx": p,
            "n_per_group": 3,
        }

    # Claim-direction audit
    audit = []
    # Claim 1: RPRM is expressed in HSCs (background expression) — paper says low at baseline, IR-induced.
    rprm = per_gene.get("Rprm", {})
    if rprm.get("found"):
        audit.append({
            "claim_id": "L22-RPRM-detectable",
            "paper_claim": "RPRM is induced in WT LSKs after IR (Fig 2a).",
            "test": "Mean RPRM expression in Ctrl vs IR HSCs (GSE244971, 3d post-IR, WT)",
            "ctrl_mean": rprm["Ctrl"]["mean"],
            "ir_mean": rprm["IR"]["mean"],
            "log2FC": rprm["IR_vs_Ctrl"]["log2FC_IR_over_Ctrl"],
            "direction_paper": "IR > Ctrl",
            "direction_observed": "IR > Ctrl" if rprm["IR"]["mean"] > rprm["Ctrl"]["mean"] else "IR <= Ctrl",
            "consistent": rprm["IR"]["mean"] > rprm["Ctrl"]["mean"],
            "caveat": "Paper measured 1h post-IR; we have 3d post-IR. RPRM is transient (Zhang 2021), so 3d may have returned to baseline.",
        })
    # Claim 2: Inflammatory cytokines are upregulated by IR in WT HSCs (Fig 4a/b — KO blunts this)
    for cyt in ["Il1a", "Il1b", "Tnf", "Il13", "Ccl11", "Ccl2"]:
        g = per_gene.get(cyt, {})
        if not g.get("found"):
            audit.append({
                "claim_id": f"L22-Inflam-{cyt}",
                "paper_claim": f"{cyt} is higher in WT post-IR than KO post-IR (Fig 4b).",
                "test": "Cannot test in GSE244971: gene not found or null.",
                "consistent": None,
            })
            continue
        audit.append({
            "claim_id": f"L22-Inflam-{cyt}",
            "paper_claim": f"{cyt} is higher in WT than KO post-IR (Fig 4b); implies IR upregulates {cyt} in WT.",
            "test": f"IR/Ctrl ratio of {cyt} in WT HSCs (GSE244971, 3d post-IR)",
            "ctrl_mean": g["Ctrl"]["mean"],
            "ir_mean": g["IR"]["mean"],
            "log2FC": g["IR_vs_Ctrl"]["log2FC_IR_over_Ctrl"],
            "fold_change": g["IR_vs_Ctrl"]["fold_change_IR_over_Ctrl"],
            "p_normal_approx": g["IR_vs_Ctrl"]["p_normal_approx"],
            "direction_paper": "IR > Ctrl (upregulation by IR in WT)",
            "direction_observed": "IR > Ctrl" if g["IR"]["mean"] > g["Ctrl"]["mean"] else "IR <= Ctrl",
            "consistent": g["IR"]["mean"] > g["Ctrl"]["mean"],
            "caveat": "Timepoint mismatch: paper 1h post-IR, proxy 3d post-IR. Cytokine kinetics may differ.",
        })
    # Claim 3: EGFR and Lin28a are upregulated post-IR in KO mice (paper says KO > WT post-IR)
    # In WT-only data, we can test whether EGFR/Lin28a are IR-responsive at all.
    for g_name in ["Egfr", "Lin28a", "Xrcc6"]:
        g = per_gene.get(g_name, {})
        if not g.get("found"):
            continue
        audit.append({
            "claim_id": f"L22-Mech-{g_name}",
            "paper_claim": f"{g_name} is upregulated in KO LSKs vs WT LSKs 1h post-IR (Fig 4c-f / Fig 3h for Xrcc6).",
            "test": f"{g_name} IR/Ctrl in WT HSCs (proxy: shows whether IR alone perturbs {g_name})",
            "ctrl_mean": g["Ctrl"]["mean"],
            "ir_mean": g["IR"]["mean"],
            "log2FC": g["IR_vs_Ctrl"]["log2FC_IR_over_Ctrl"],
            "fold_change": g["IR_vs_Ctrl"]["fold_change_IR_over_Ctrl"],
            "p_normal_approx": g["IR_vs_Ctrl"]["p_normal_approx"],
            "direction_paper": "KO > WT (cannot test in WT-only data); proxy tests IR vs no-IR in WT.",
            "consistent": None,
            "caveat": "WT-only dataset; without RPRM-KO arm, this is a directional sanity check, not a replication of the KO-vs-WT delta.",
        })

    summary = {
        "dataset": "GSE244971",
        "source": "Chen X et al., Army Medical University; PubMed 38802843; public 2024-06-05",
        "samples": 12,
        "groups": list(SAMPLES.keys()),
        "n_per_group": 3,
        "timepoint": "3 days post-IR (paper used 1 h post-IR — direction-only proxy)",
        "normalization": "FPKM-like (per-sample sums 344K-405K; not raw counts)",
        "tool": "pure Python stdlib (no pandas/scipy); Welch's t with normal-approx p",
        "warnings": [
            "n=3/group is small; report direction-only.",
            "Paper Fig 4 used 1 h post-IR; proxy is 3 d post-IR — inflammation peak may have decayed.",
            "Proxy is WT-only; cannot test RPRM KO comparison.",
            "p_normal_approx is a normal-distribution approximation; true Welch t-test p-values for df<5 are LARGER. Treat as a lower bound.",
            "FPKM-like normalization is what the GEO submitter provided; we did not re-quantify from raw FASTQs.",
        ],
    }

    out = {
        "summary": summary,
        "per_gene": per_gene,
        "claim_audit": audit,
    }
    out_path = RESULTS / "cross_check_GSE244971.json"
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2, default=lambda x: None if isinstance(x, float) and (math.isnan(x) or math.isinf(x)) else x)
    print(f"Wrote {out_path}")
    # Print a one-screen verdict
    print("\n=== Direction audit ===")
    for a in audit:
        if a.get("consistent") is True:
            mark = "✓ consistent"
        elif a.get("consistent") is False:
            mark = "✗ INCONSISTENT"
        else:
            mark = "— untestable"
        log = a.get("log2FC")
        log_s = f"log2FC={log:+.2f}" if isinstance(log, (int, float)) and log == log else "log2FC=NA"
        print(f"  {mark}  {a['claim_id']:<25} {log_s}")


if __name__ == "__main__":
    main()
