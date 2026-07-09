#!/usr/bin/env python3
"""
LUCID-100 replication analysis for Chen & Zhang 2025
J. Phys.: Conf. Ser. 3109 (2025) 012098 — DOI 10.1088/1742-6596/3109/1/012098
"Proteomic Profiling of Deinococcus radiodurans Reveals Irradiation-Induced
Proteins and Their Associated Functional Pathways."

Data substrate: PRIDE PXD027969 (Xiong et al. 2022, same lab same dose same
strain), MaxQuant proteinGroups.txt. The 2025 paper used pFind3 (Open Search)
instead of MaxQuant, but on the same experimental design (or a sibling cohort).
This script re-derives presence/absence Venn (2025-style) and DAP counts (2022-
style) from the deposited PXD027969 LFQ table.

Outputs:
  results/analysis_report.json
  results/venn_0_1_3h.tsv
  results/named_proteins_check.tsv
  results/dap_3h_top.tsv

Local + free only. No paid endpoints.
"""

import csv, json, math, os, statistics, sys, re
from collections import defaultdict

PROJECT = "/Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-deinococcus-proteomics-irradiation"
PG_PATH = os.path.join(PROJECT, "data/cross_check/pxd027969_proteinGroups.txt")
OUT_DIR = os.path.join(PROJECT, "results")
os.makedirs(OUT_DIR, exist_ok=True)

# Sample layout from the MaxQuant summary.txt
SAMPLES = {
    "C": {
        "0h":  ["C_0h_1", "C_0h_3", "C_0h_4"],
        "1h":  ["C_1h_2", "C_1h_4", "C_1h_5"],
        "3h":  ["C_3h_2", "C_3h_3", "C_3h_4"],
        "6h":  ["C_6h_1", "C_6h_3", "C_6h_5"],
        "12h": ["C_12h_3", "C_12h_4", "C_12h_5"],
    },
    "R": {
        "0h":  ["R_0h_1", "R_0h_2", "R_0h_3"],
        "1h":  ["R_1h_1", "R_1h_2", "R_1h_5"],
        "3h":  ["R_3h_2", "R_3h_3", "R_3h_5"],
        "6h":  ["R_6h_2", "R_6h_4", "R_6h_5"],
        "12h": ["R_12h_2", "R_12h_3", "R_12h_4"],
    },
}

NAMED_TARGETS = {
    # Targets explicitly named in Chen & Zhang 2025
    "RuvC": "Q9RX75",
    "DdrA": "Q9RX92",
    "DdrB": "Q9RY80",
    # Targets named in Xiong 2022 (overlapping DAP-at-every-stage set)
    "PprA": "Q9RY56",
    "CinA-like": None,         # search by name
    "RecA": "Q9RXR9",
    "DdrD": "Q9RVS5",
    "Ssb":  "Q9RY51",          # canonical UniProt for D. radiodurans ssb DR_0099
    "GyrA": "Q9RYM9",
}


def parse_pg(path):
    """Read MaxQuant proteinGroups.txt; return list of dicts plus column names."""
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        rows = list(reader)
    return rows, reader.fieldnames


def filter_main(rows):
    """Drop reverse decoys, contaminants, and only-by-site rows."""
    kept = []
    for r in rows:
        if r.get("Reverse") == "+":
            continue
        if r.get("Potential contaminant") == "+":
            continue
        if r.get("Only identified by site") == "+":
            continue
        kept.append(r)
    return kept


def detected_mask(r, sample):
    """True if protein is "detected" in that sample.
    Definition: LFQ intensity > 0 OR Razor+unique peptides >= 1 in that sample."""
    lfq = r.get(f"LFQ intensity {sample}", "0") or "0"
    try:
        lfq_v = float(lfq)
    except ValueError:
        lfq_v = 0.0
    rup = r.get(f"Razor + unique peptides {sample}", "0") or "0"
    try:
        rup_v = int(rup)
    except ValueError:
        rup_v = 0
    return (lfq_v > 0) or (rup_v >= 1)


def union_present(r, samples):
    return any(detected_mask(r, s) for s in samples)


def majority_present(r, samples, k=2):
    """Detected in at least k of the n samples (default k=2/3)."""
    return sum(detected_mask(r, s) for s in samples) >= k


def first_uniprot(protein_ids):
    """Pull the first UniProt accession from a ';'-joined MaxQuant protein-ID field."""
    accs = all_uniprot(protein_ids)
    return accs[0] if accs else None


def all_uniprot(protein_ids):
    """Extract bare UniProt accessions from a MaxQuant 'Protein IDs' field.
    Handles both bare ('Q9RX92') and prefixed ('sp|Q9RX92|DDRA_DEIRA') formats."""
    if not protein_ids:
        return []
    out = []
    for tok in protein_ids.split(";"):
        tok = tok.strip()
        if not tok:
            continue
        # sp|ACC|NAME or tr|ACC|NAME
        m = re.match(r"^(?:sp|tr)\|([A-Za-z0-9]+)\|", tok)
        if m:
            out.append(m.group(1))
        else:
            out.append(tok)
    return out


def safe_log2(x):
    return math.log2(x) if x > 0 else float("nan")


def welch_t(a, b):
    """Welch's t-statistic; returns (t, df). p must be computed externally if scipy
    not available. Returns NaN if both groups have <2 finite observations or zero
    variance."""
    a = [x for x in a if math.isfinite(x)]
    b = [x for x in b if math.isfinite(x)]
    if len(a) < 2 or len(b) < 2:
        return float("nan"), float("nan")
    ma, mb = statistics.mean(a), statistics.mean(b)
    va, vb = statistics.variance(a), statistics.variance(b)
    if va == 0 and vb == 0:
        return float("nan"), float("nan")
    se = math.sqrt(va/len(a) + vb/len(b))
    if se == 0:
        return float("nan"), float("nan")
    t = (mb - ma) / se
    # Welch–Satterthwaite df
    num = (va/len(a) + vb/len(b))**2
    den = (va/len(a))**2/(len(a)-1) + (vb/len(b))**2/(len(b)-1)
    df = num / den if den > 0 else float("nan")
    return t, df


def t_to_p_two_sided(t, df):
    """Approximate two-sided p from t and df without scipy.
    Uses survival function from a Student-t CDF approximation (good enough for
    sanity-check sign / order of magnitude, not for publication)."""
    if not (math.isfinite(t) and math.isfinite(df) and df > 0):
        return float("nan")
    # Abramowitz & Stegun 26.7.8 — Student-t CDF approximation good for df>2
    x = df / (df + t*t)
    # incomplete beta I_x(df/2, 1/2)
    # use scipy if available; else fall back to a rough normal approximation
    try:
        import math as _m
        # crude: use normal approx for large df
        if df > 30:
            from math import erf, sqrt
            p = 1 - 0.5 * (1 + erf(abs(t) / sqrt(2)))
            return 2 * p
        # for small df, use SciPy if installed
        from scipy.stats import t as t_dist  # type: ignore
        return 2 * (1 - t_dist.cdf(abs(t), df))
    except Exception:
        from math import erf, sqrt
        p = 1 - 0.5 * (1 + erf(abs(t) / sqrt(2)))
        return 2 * p


def bh_fdr(pvals):
    """Benjamini-Hochberg adjusted q-values (returns list aligned to input)."""
    n = sum(1 for p in pvals if math.isfinite(p))
    if n == 0:
        return [float("nan")] * len(pvals)
    indexed = sorted(((p, i) for i, p in enumerate(pvals) if math.isfinite(p)), key=lambda x: x[0])
    q = [float("nan")] * len(pvals)
    prev = 1.0
    for rank_from_top, (p, idx) in enumerate(reversed(indexed)):
        k = n - rank_from_top  # rank from bottom (largest p gets rank n)
        adj = min(prev, p * n / k)
        prev = adj
        q[idx] = adj
    return q


def main():
    rows, fields = parse_pg(PG_PATH)
    print(f"Raw rows: {len(rows)}")
    rows = filter_main(rows)
    print(f"After dropping reverse/contam/only-site: {len(rows)}")

    # ---- Step 1: total proteins detected per group (per timepoint and union of 0/1/3h) ----
    detected_counts = {}
    for group in ("C", "R"):
        for tp in ("0h", "1h", "3h", "6h", "12h"):
            samples = SAMPLES[group][tp]
            # union detection across replicates at this timepoint
            n_union = sum(1 for r in rows if union_present(r, samples))
            # majority detection
            n_maj = sum(1 for r in rows if majority_present(r, samples, k=2))
            detected_counts[f"{group}_{tp}_union"] = n_union
            detected_counts[f"{group}_{tp}_majority"] = n_maj

    # ---- Step 2: 2025-paper-style Venn at 0/1/3h ----
    # Paper claims: 2034 shared, 142 control-only, 62 radiation-only
    c013 = [s for tp in ("0h", "1h", "3h") for s in SAMPLES["C"][tp]]
    r013 = [s for tp in ("0h", "1h", "3h") for s in SAMPLES["R"][tp]]

    venn = {}
    for crit, kpct in (("union", 0), ("majority2of9", 2), ("majority3of9", 3)):
        def present(r, samples, k):
            if k == 0:
                return any(detected_mask(r, s) for s in samples)
            return sum(detected_mask(r, s) for s in samples) >= k
        in_c = []
        in_r = []
        for r in rows:
            ic = present(r, c013, kpct)
            ir = present(r, r013, kpct)
            in_c.append(ic)
            in_r.append(ir)
        shared = sum(1 for i in range(len(rows)) if in_c[i] and in_r[i])
        c_only = sum(1 for i in range(len(rows)) if in_c[i] and not in_r[i])
        r_only = sum(1 for i in range(len(rows)) if in_r[i] and not in_c[i])
        venn[crit] = {
            "shared": shared,
            "control_only": c_only,
            "radiation_only": r_only,
            "control_total": shared + c_only,
            "radiation_total": shared + r_only,
            "union_total": shared + c_only + r_only,
            "criterion_desc": {
                "union": "detected (LFQ>0 or razor>=1) in ANY of the 9 control or radiation 0/1/3h replicates",
                "majority2of9": "detected in >=2 of 9 replicates per group",
                "majority3of9": "detected in >=3 of 9 replicates per group",
            }[crit],
        }

    # Save Venn TSV
    with open(os.path.join(OUT_DIR, "venn_0_1_3h.tsv"), "w") as f:
        f.write("criterion\tshared\tcontrol_only\tradiation_only\tcontrol_total\tradiation_total\tunion_total\tdescription\n")
        for crit, d in venn.items():
            f.write(f"{crit}\t{d['shared']}\t{d['control_only']}\t{d['radiation_only']}\t{d['control_total']}\t{d['radiation_total']}\t{d['union_total']}\t{d['criterion_desc']}\n")

    # ---- Step 3: Named DDR proteins — detection + LFQ trajectories ----
    # Build accession index
    by_acc = defaultdict(list)
    for r in rows:
        for acc in all_uniprot(r.get("Protein IDs", "")):
            by_acc[acc].append(r)

    named_results = []
    for name, acc in NAMED_TARGETS.items():
        if acc is None:
            # name search in Fasta headers
            matched_rows = [r for r in rows if name.lower().split("-")[0] in (r.get("Fasta headers", "") or "").lower()]
            acc_used = None
            r_use = matched_rows[0] if matched_rows else None
            if r_use:
                acc_used = first_uniprot(r_use.get("Protein IDs", ""))
        else:
            matched_rows = by_acc.get(acc, [])
            r_use = matched_rows[0] if matched_rows else None
            acc_used = acc if r_use else None

        if not r_use:
            named_results.append({"name": name, "expected_accession": acc, "found": False})
            continue

        # Per-timepoint per-group mean LFQ
        per_tp = {}
        for group in ("C", "R"):
            for tp in ("0h", "1h", "3h", "6h", "12h"):
                lfqs = []
                for s in SAMPLES[group][tp]:
                    v = r_use.get(f"LFQ intensity {s}", "0") or "0"
                    try:
                        lfqs.append(float(v))
                    except ValueError:
                        lfqs.append(0.0)
                non_zero = [x for x in lfqs if x > 0]
                per_tp[f"{group}_{tp}_mean_LFQ"] = round(statistics.mean(lfqs), 2)
                per_tp[f"{group}_{tp}_nonzero_count"] = len(non_zero)

        # 2025-paper claim: present in radiated, absent (or near-absent) in control
        r_present_013 = any(per_tp[f"R_{tp}_nonzero_count"] >= 1 for tp in ("0h","1h","3h"))
        c_present_013 = any(per_tp[f"C_{tp}_nonzero_count"] >= 1 for tp in ("0h","1h","3h"))

        named_results.append({
            "name": name,
            "expected_accession": acc,
            "accession_used": acc_used,
            "found": True,
            "protein_name": (r_use.get("Fasta headers", "") or "")[:160],
            "razor_unique_total": r_use.get("Razor + unique peptides", ""),
            "r_present_in_0_1_3h": r_present_013,
            "c_present_in_0_1_3h": c_present_013,
            "exclusive_to_radiation_in_0_1_3h": r_present_013 and not c_present_013,
            **per_tp,
        })

    with open(os.path.join(OUT_DIR, "named_proteins_check.tsv"), "w") as f:
        keys = ["name","expected_accession","accession_used","found","r_present_in_0_1_3h","c_present_in_0_1_3h","exclusive_to_radiation_in_0_1_3h","razor_unique_total"]
        keys += [f"{g}_{tp}_mean_LFQ" for g in ("C","R") for tp in ("0h","1h","3h","6h","12h")]
        keys += [f"{g}_{tp}_nonzero_count" for g in ("C","R") for tp in ("0h","1h","3h","6h","12h")]
        f.write("\t".join(keys) + "\n")
        for d in named_results:
            f.write("\t".join(str(d.get(k, "")) for k in keys) + "\n")

    # ---- Step 4: DAP analysis at 3 h (Xiong 2022 Table 1: 122 DAPs at 3h, 57 up + 65 down) ----
    # MaxQuant LFQ -> log2, missing -> nan, Welch t-test on present-in-≥2-replicates-per-group.
    dap_results = []
    for r in rows:
        c_samples = SAMPLES["C"]["3h"]
        r_samples = SAMPLES["R"]["3h"]
        c_lfq = []
        for s in c_samples:
            v = r.get(f"LFQ intensity {s}", "0") or "0"
            try:
                v = float(v)
            except ValueError:
                v = 0.0
            c_lfq.append(safe_log2(v))
        r_lfq = []
        for s in r_samples:
            v = r.get(f"LFQ intensity {s}", "0") or "0"
            try:
                v = float(v)
            except ValueError:
                v = 0.0
            r_lfq.append(safe_log2(v))
        c_present = sum(1 for x in c_lfq if math.isfinite(x))
        r_present = sum(1 for x in r_lfq if math.isfinite(x))
        if c_present < 2 or r_present < 2:
            continue
        c_mean = statistics.mean([x for x in c_lfq if math.isfinite(x)])
        r_mean = statistics.mean([x for x in r_lfq if math.isfinite(x)])
        log2fc = r_mean - c_mean
        t, df = welch_t(c_lfq, r_lfq)
        p = t_to_p_two_sided(t, df)
        dap_results.append({
            "ids": r.get("Protein IDs", ""),
            "acc": first_uniprot(r.get("Protein IDs", "")),
            "fasta_header": (r.get("Fasta headers", "") or "")[:120],
            "log2FC_R_vs_C": log2fc,
            "t": t,
            "df": df,
            "p": p,
            "c_present_n": c_present,
            "r_present_n": r_present,
        })

    pvals = [d["p"] for d in dap_results]
    qvals = bh_fdr(pvals)
    for d, q in zip(dap_results, qvals):
        d["q"] = q

    sig_05 = [d for d in dap_results if math.isfinite(d["q"]) and d["q"] < 0.05]
    sig_05_up = [d for d in sig_05 if d["log2FC_R_vs_C"] > 0]
    sig_05_down = [d for d in sig_05 if d["log2FC_R_vs_C"] < 0]

    # Top by |log2FC| among significant
    sig_05_sorted = sorted(sig_05, key=lambda d: -abs(d["log2FC_R_vs_C"]))
    with open(os.path.join(OUT_DIR, "dap_3h_top.tsv"), "w") as f:
        f.write("acc\tlog2FC_R_vs_C\tp\tq\tc_n\tr_n\tfasta_header\n")
        for d in sig_05_sorted[:200]:
            f.write(f"{d['acc']}\t{d['log2FC_R_vs_C']:.3f}\t{d['p']:.3g}\t{d['q']:.3g}\t{d['c_present_n']}\t{d['r_present_n']}\t{d['fasta_header']}\n")

    # ---- Final report JSON ----
    report = {
        "paper": {
            "doi": "10.1088/1742-6596/3109/1/012098",
            "title": "Proteomic Profiling of Deinococcus radiodurans Reveals Irradiation-Induced Proteins and Their Associated Functional Pathways",
            "authors": ["Chaoyi Chen", "Yongqian Zhang"],
            "year": 2025,
            "venue": "J. Phys. Conf. Ser. 3109 (2025) 012098",
        },
        "data_source": {
            "pride_accession": "PXD027969",
            "primary_publication": "Xiong et al. 2022, Oxid Med Cell Longev (PMC9674996), DOI 10.1155/2022/1622829",
            "relationship": ("Same lab (Yongqian Zhang, Beijing Institute of Technology), same strain "
                             "(D. radiodurans CGMCC 1.633 = R1), same dose (6 kGy 60Co gamma, 30 Gy/min at Peking "
                             "University), same time points (0/1/3/6/12 h PIR), 3 biological reps per condition. "
                             "Xiong 2022 used MaxQuant 1.6.4.0 LFQ + Perseus; Chen 2025 used pFind3 Open Search. "
                             "Whether the 2025 paper uses the IDENTICAL raw spectra or a re-irradiated cohort is "
                             "not stated; published 2025 paper has no data-availability statement."),
        },
        "maxquant_metadata": {
            "version": "1.6.17.0",  # from parameters.txt
            "fasta": "DR_UP000002524_243230.fasta (3,085 proteins)",
            "psm_fdr": 0.01,
            "protein_fdr": 0.01,
            "match_between_runs": True,
            "modifications": "Carbamidomethyl(C) fixed; Oxidation(M), Acetyl(Protein N-term) variable",
            "samples_total": 30,  # 10 conditions × 3 reps
            "experimental_design": "2 groups (C, R) × 5 timepoints (0,1,3,6,12 h) × 3 biological reps",
        },
        "step1_detection_counts": detected_counts,
        "step2_venn_at_0_1_3h": venn,
        "step3_named_proteins": named_results,
        "step4_dap_at_3h": {
            "n_tested": len(dap_results),
            "n_significant_q05": len(sig_05),
            "n_up_q05_R_vs_C": len(sig_05_up),
            "n_down_q05_R_vs_C": len(sig_05_down),
            "paper_xiong2022_table1_3h": {"DAPs_total": 122, "up": 57, "down": 65},
            "note": ("BH-corrected Welch t-test on log2(LFQ); proteins with <2 valid LFQ per group "
                     "excluded. Approx — Xiong 2022 used Perseus s0=2.0 + FDR<0.05 with NAguideR "
                     "imputation (we do not impute). Strict equivalence not expected."),
        },
        "claim_audit": {
            "claim_2025_total_detected_union_0_1_3h": {
                "paper": 2238,
                "ours_union": venn["union"]["union_total"],
                "ours_majority2of9": venn["majority2of9"]["union_total"],
                "ours_majority3of9": venn["majority3of9"]["union_total"],
            },
            "claim_2025_shared": {"paper": 2034, "ours_union": venn["union"]["shared"]},
            "claim_2025_control_only": {"paper": 142, "ours_union": venn["union"]["control_only"]},
            "claim_2025_radiation_only": {"paper": 62, "ours_union": venn["union"]["radiation_only"]},
            "claim_2025_RuvC_DdrA_DdrB_exclusive_to_radiation": [
                {"name": n["name"], "exclusive": n.get("exclusive_to_radiation_in_0_1_3h")}
                for n in named_results if n.get("name") in ("RuvC", "DdrA", "DdrB")
            ],
            "claim_2022_122_DAPs_at_3h": {
                "paper": 122,
                "ours_q05_total": len(sig_05),
                "ours_up_q05": len(sig_05_up),
                "ours_down_q05": len(sig_05_down),
            },
        },
    }
    with open(os.path.join(OUT_DIR, "analysis_report.json"), "w") as f:
        json.dump(report, f, indent=2, default=str)

    print("\n=== KEY RESULTS ===")
    print(json.dumps(report["claim_audit"], indent=2, default=str))


if __name__ == "__main__":
    main()
