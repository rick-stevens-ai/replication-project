#!/usr/bin/env python3
"""
Extended replication for Botbayev 2026 (Genes 17(2):191).

Beyond the first-pass chi^2/allele OR replication, this script:
  1. Reconstructs integer genotype counts (largest-remainder rounding).
  2. Computes ALL of:
       - Pearson 2x3 genotype chi^2
       - Pearson 2x2 allelic chi^2 + Woolf OR + 95% CI
       - Dominant model OR (homozygous-major vs carriers of minor: AA vs AB+BB)
       - Recessive model OR (homozygous-minor vs others: BB vs AA+AB)
       - Allelic OR with BOTH "minor-vs-major" and the inverted convention
       - HWE exact (mid-p) test in BOTH miners and controls
  3. Decides which OR convention the paper appears to use, per row.
  4. Audits the 4 abstract claims directly:
       - TP53 intron 3 INS allele enriched in exposed (?)
       - TP53 intron 6 A allele enriched in exposed (?)
       - TP53 Pro72 (C) allele enriched in exposed (?)
       - p21 codon 31 A allele enriched in exposed (?)
  5. Writes results/extended_replication.json and a human-readable
     results/extended_summary.tsv.
"""
from __future__ import annotations
import json, math, os, sys
from pathlib import Path
import numpy as np
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent
TABLES_JSON = ROOT / "tables" / "tables_extracted.json"
OUT_JSON = ROOT / "results" / "extended_replication.json"
OUT_TSV = ROOT / "results" / "extended_summary.tsv"

# --- cohort sizes from Table 1 (per location x ethnic group) ------------------
COHORT_N = {
    ("Control",        "Kazakh"):  129,
    ("Control",        "Russian"): 160,
    ("Balkashinskoye", "Kazakh"):   54,
    ("Balkashinskoye", "Russian"): 184,
    ("Stepnogorsk",    "Kazakh"):   52,
    ("Stepnogorsk",    "Russian"): 172,
}

def normalize_pop(p):  # paper mixes "Kazakh"/"Kazakhs"/"Russian"/"Russians"
    if p.lower().startswith("kazakh"): return "Kazakh"
    if p.lower().startswith("russ"):   return "Russian"
    return p

def largest_remainder(freqs, n):
    """Convert proportions to integer counts summing to n, minimizing rounding error."""
    raw = [f * n for f in freqs]
    floor = [int(math.floor(x)) for x in raw]
    rem = n - sum(floor)
    # distribute rem extras to the largest fractional parts
    fracs = sorted(enumerate(x - math.floor(x) for x in raw),
                   key=lambda kv: -kv[1])
    out = list(floor)
    for i in range(rem):
        out[fracs[i][0]] += 1
    return out

def hwe_exact_midp(obs_hom1, obs_het, obs_hom2):
    """Exact HWE test, mid-p, Wigginton et al. 2005. Returns p-value."""
    n = obs_hom1 + obs_het + obs_hom2
    if n == 0:
        return float("nan")
    rare_alleles = 2 * min(obs_hom1, obs_hom2) + obs_het
    common_alleles = 2 * n - rare_alleles
    if rare_alleles == 0 or common_alleles == 0:
        return 1.0
    # full enumeration of possible het counts with the same allele totals
    # het count has same parity as rare_alleles
    het_probs = {}
    # use Wigginton/Abecasis recurrence
    # let n_r = rare alleles, n_c = common alleles, n = total individuals
    # heterozygote count k must satisfy: k <= n_r, (n_r - k) even, (n_c - k) >= 0
    n_r = rare_alleles
    n_c = common_alleles
    # start at the most likely het count and recurse out
    # mean het = n_r * n_c / (2n - 1) approx
    mean_het = (n_r * n_c) // (2 * n - 1) if (2*n - 1) > 0 else 0
    if (mean_het % 2) != (n_r % 2):
        mean_het += 1
    # build pmf by recursion
    # P(k+2) / P(k) = (n_r - k)(n_c - k) / [(k+2)(k+1)]  (after factoring multinomial)
    # We use log-space to avoid overflow.
    log_p = {}
    log_p[mean_het] = 0.0
    # upward
    k = mean_het
    while k + 2 <= n_r and (n_c - k) >= 2:
        log_ratio = (math.log(n_r - k) + math.log(n_c - k)
                     - math.log(k + 2) - math.log(k + 1)
                     - math.log(2) - math.log(2))  # extra 1/4 per pair (hom counts go down by 1 each)
        # Wigginton: P(k+2)/P(k) = [(n_r - k)(n_c - k)] / [4 * (k/2 + 1)^2]
        # equivalent to log_ratio = log((n_r-k)*(n_c-k)) - log(4*((k/2+1)**2))
        log_ratio = (math.log(n_r - k) + math.log(n_c - k)
                     - math.log(4.0) - 2.0 * math.log((k/2.0) + 1.0))
        log_p[k+2] = log_p[k] + log_ratio
        k += 2
    # downward
    k = mean_het
    while k - 2 >= 0:
        # invert: P(k-2)/P(k) = 4 * (k/2)^2 / [(n_r - (k-2)) * (n_c - (k-2))]
        log_ratio = (math.log(4.0) + 2.0 * math.log(k/2.0)
                     - math.log(n_r - (k-2)) - math.log(n_c - (k-2)))
        log_p[k-2] = log_p[k] + log_ratio
        k -= 2
    # normalize
    mx = max(log_p.values())
    probs = {k: math.exp(v - mx) for k, v in log_p.items()}
    total = sum(probs.values())
    probs = {k: v/total for k, v in probs.items()}
    p_obs = probs.get(obs_het, 0.0)
    # mid-p two-sided
    p_val = sum(p for k, p in probs.items() if p < p_obs) + 0.5 * p_obs
    return float(min(1.0, max(0.0, p_val)))

def woolf_or(a, b, c, d):
    """Woolf log-OR with Haldane–Anscombe correction if any zero. Returns (OR, lo, hi)."""
    if min(a, b, c, d) == 0:
        a, b, c, d = a+0.5, b+0.5, c+0.5, d+0.5
    or_ = (a * d) / (b * c)
    se = math.sqrt(1/a + 1/b + 1/c + 1/d)
    lo = math.exp(math.log(or_) - 1.96 * se)
    hi = math.exp(math.log(or_) + 1.96 * se)
    return or_, lo, hi

# minor allele per SNP (which allele the paper calls the "risk"/enriched allele)
MINOR_ALLELE = {
    "rs17878362": "I+",   # 16-bp insertion
    "rs1625895":  "A",
    "rs1042522":  "P",    # Pro72 = C
    "rs1801270":  "A",
}
# paper claim: which allele is ENRICHED in exposed (=miners)?
PAPER_ENRICHED_ALLELE = {
    "rs17878362": "I+",
    "rs1625895":  "A",
    "rs1042522":  "P",
    "rs1801270":  "A",
}

# table parsing: build a tidy long table of (snp, location, pop, genotype_label, miners_freq, controls_freq, OR, CI, chi2_gt, p_gt, chi2_al, p_al)
def load_tables():
    with open(TABLES_JSON) as fh:
        t = json.load(fh)
    paper_tables = t["tables"]
    snp_tables = {
        "rs17878362": paper_tables["table_4_tp53_intron3_rs17878362"],
        "rs1625895":  paper_tables["table_5_tp53_intron6_rs1625895"],
        "rs1042522":  paper_tables["table_6_tp53_exon4_rs1042522"],
        "rs1801270":  paper_tables["table_7_p21_codon31_rs1801270"],
    }
    return snp_tables

def parse_block(snp, rows):
    """
    Rows for one SNP come in groups of 3 (3 genotypes) per location x pop.
    OR/CI/chi2/p are printed on the first row of each block.
    """
    blocks = []
    i = 0
    while i < len(rows):
        loc, pop, gt, mf, cf, OR, CI, c_gt, p_gt, c_al, p_al = rows[i]
        head = (loc, normalize_pop(pop))
        block = {
            "snp": snp,
            "location": loc,
            "population": normalize_pop(pop),
            "genotypes": [(gt, mf, cf)],
            "paper_OR": OR, "paper_CI": CI,
            "paper_chi2_gt": c_gt, "paper_p_gt": p_gt,
            "paper_chi2_al": c_al, "paper_p_al": p_al,
        }
        # consume next 2 rows (genotype continuation)
        for j in (1, 2):
            if i + j >= len(rows): break
            r = rows[i + j]
            if (r[0], normalize_pop(r[1])) != head:
                break
            block["genotypes"].append((r[2], r[3], r[4]))
        i += len(block["genotypes"])
        blocks.append(block)
    return blocks

def order_genotypes(snp, blocks):
    """
    Force a consistent (homozygous-major, het, homozygous-minor) ordering.
    The paper's row order varies, especially Balkashinskoye p21 (CA/CC/AA).
    We choose the canonical mapping based on the genotype labels we see.
    """
    canon_map = {
        "rs17878362": ["I-/I-", "I-/I+", "I+/I+"],
        "rs1625895":  ["GG", "GA", "AA"],
        "rs1042522":  ["AA", "AP", "PP"],   # AA=Arg/Arg, AP=Arg/Pro, PP=Pro/Pro
        "rs1801270":  ["CC", "CA", "AA"],
    }
    canon = canon_map[snp]
    fixed = []
    for b in blocks:
        gts = dict((g[0], g) for g in b["genotypes"])
        try:
            ordered = [gts[g] for g in canon]
        except KeyError:
            ordered = b["genotypes"]
        b["genotypes_ordered"] = ordered
        fixed.append(b)
    return fixed

def analyze_block(b):
    snp = b["snp"]
    loc = b["location"]; pop = b["population"]
    n_miners = COHORT_N[(loc, pop)]
    n_ctrls  = COHORT_N[("Control", pop)]
    # genotype counts (largest-remainder)
    miners_f = [g[1] for g in b["genotypes_ordered"]]
    ctrls_f  = [g[2] for g in b["genotypes_ordered"]]
    miners_c = largest_remainder(miners_f, n_miners)
    ctrls_c  = largest_remainder(ctrls_f,  n_ctrls)
    # genotype chi^2 (2x3)
    table_gt = np.array([miners_c, ctrls_c])
    chi2_gt, p_gt = stats.chi2_contingency(table_gt, correction=False)[:2]
    # allele counts
    AA_m, AB_m, BB_m = miners_c
    AA_c, AB_c, BB_c = ctrls_c
    major_m = 2*AA_m + AB_m
    minor_m = 2*BB_m + AB_m
    major_c = 2*AA_c + AB_c
    minor_c = 2*BB_c + AB_c
    chi2_al, p_al = stats.chi2_contingency(
        np.array([[minor_m, major_m], [minor_c, major_c]]),
        correction=False)[:2]
    # OR conventions
    OR_allelic_minor_vs_major, lo_a, hi_a = woolf_or(minor_m, major_m, minor_c, major_c)
    OR_dominant_carriers_vs_AA, lo_d, hi_d = woolf_or(AB_m + BB_m, AA_m, AB_c + BB_c, AA_c)
    OR_recessive_BB_vs_others,  lo_r, hi_r = woolf_or(BB_m, AA_m + AB_m, BB_c, AA_c + AB_c)
    OR_allelic_major_vs_minor   = 1.0 / OR_allelic_minor_vs_major if OR_allelic_minor_vs_major else float("nan")
    OR_dominant_inverted        = 1.0 / OR_dominant_carriers_vs_AA if OR_dominant_carriers_vs_AA else float("nan")
    # HWE in controls + miners
    p_hwe_miners = hwe_exact_midp(*miners_c)
    p_hwe_ctrls  = hwe_exact_midp(*ctrls_c)
    # Allele frequencies (minor allele = the "enriched" one per paper)
    f_minor_miners = minor_m / (2 * sum(miners_c)) if sum(miners_c) else float("nan")
    f_minor_ctrls  = minor_c / (2 * sum(ctrls_c))  if sum(ctrls_c)  else float("nan")
    # Decide which OR convention best matches the paper's reported OR
    paper_OR = b.get("paper_OR")
    paper_OR = float(paper_OR) if paper_OR is not None else None
    candidates = {
        "allelic_minor_vs_major": OR_allelic_minor_vs_major,
        "allelic_major_vs_minor": OR_allelic_major_vs_minor,
        "dominant_carriers_vs_AA": OR_dominant_carriers_vs_AA,
        "dominant_inverted":       OR_dominant_inverted,
        "recessive_BB_vs_others":  OR_recessive_BB_vs_others,
    }
    best_match = None
    if paper_OR is not None and paper_OR > 0:
        best = min(candidates.items(), key=lambda kv: abs(math.log(kv[1]) - math.log(paper_OR)))
        best_match = {"convention": best[0], "OR": best[1], "abs_log_diff": abs(math.log(best[1]) - math.log(paper_OR))}
    return {
        "snp": snp,
        "location": loc,
        "population": pop,
        "n_miners": n_miners,
        "n_controls": n_ctrls,
        "genotype_order": [g[0] for g in b["genotypes_ordered"]],
        "miners_counts":   miners_c,
        "controls_counts": ctrls_c,
        "miners_freqs":   miners_f,
        "controls_freqs": ctrls_f,
        "minor_allele":   MINOR_ALLELE[snp],
        "minor_freq_miners":   f_minor_miners,
        "minor_freq_controls": f_minor_ctrls,
        "recomp_chi2_gt": chi2_gt, "recomp_p_gt": p_gt,
        "recomp_chi2_al": chi2_al, "recomp_p_al": p_al,
        "OR_allelic_minor_vs_major": (OR_allelic_minor_vs_major, lo_a, hi_a),
        "OR_dominant_carriers_vs_AA": (OR_dominant_carriers_vs_AA, lo_d, hi_d),
        "OR_recessive_BB_vs_others":  (OR_recessive_BB_vs_others,  lo_r, hi_r),
        "paper_OR": paper_OR,
        "paper_CI": b.get("paper_CI"),
        "paper_chi2_gt": b.get("paper_chi2_gt"),
        "paper_p_gt": b.get("paper_p_gt"),
        "paper_chi2_al": b.get("paper_chi2_al"),
        "paper_p_al": b.get("paper_p_al"),
        "best_matching_OR_convention": best_match,
        "hwe_p_miners": p_hwe_miners,
        "hwe_p_controls": p_hwe_ctrls,
    }

def main():
    tabs = load_tables()
    all_results = []
    for snp, tab in tabs.items():
        blocks = parse_block(snp, tab["rows"])
        blocks = order_genotypes(snp, blocks)
        for b in blocks:
            all_results.append(analyze_block(b))
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_JSON, "w") as fh:
        json.dump(all_results, fh, indent=2, default=lambda o: list(o) if isinstance(o, tuple) else o)
    # tsv summary
    cols = ["snp","location","population","minor_allele",
            "minor_freq_miners","minor_freq_controls",
            "recomp_p_gt","paper_p_gt","recomp_p_al","paper_p_al",
            "OR_allelic_minor_vs_major","OR_dominant_carriers_vs_AA","paper_OR",
            "best_OR_convention","best_OR_value","best_OR_logdiff",
            "hwe_p_miners","hwe_p_controls"]
    with open(OUT_TSV, "w") as fh:
        fh.write("\t".join(cols) + "\n")
        for r in all_results:
            best = r["best_matching_OR_convention"] or {}
            fh.write("\t".join([
                r["snp"], r["location"], r["population"], r["minor_allele"],
                f"{r['minor_freq_miners']:.4f}", f"{r['minor_freq_controls']:.4f}",
                f"{r['recomp_p_gt']:.4g}", f"{r['paper_p_gt']}",
                f"{r['recomp_p_al']:.4g}", f"{r['paper_p_al']}",
                f"{r['OR_allelic_minor_vs_major'][0]:.3f}",
                f"{r['OR_dominant_carriers_vs_AA'][0]:.3f}",
                f"{r['paper_OR']}",
                best.get("convention","-"),
                f"{best.get('OR','nan'):.3f}" if best else "-",
                f"{best.get('abs_log_diff','nan'):.3f}" if best else "-",
                f"{r['hwe_p_miners']:.4g}", f"{r['hwe_p_controls']:.4g}",
            ]) + "\n")
    # Abstract-claim audit
    print("\n=== Abstract-claim audit: ENRICHED allele in exposed workers ===\n")
    print(f"{'SNP':12s} {'allele':6s} {'Loc':16s} {'Pop':8s} {'miners':>8s} {'controls':>8s} {'enriched?':>10s}  delta")
    for r in all_results:
        a = MINOR_ALLELE[r["snp"]]
        d = r["minor_freq_miners"] - r["minor_freq_controls"]
        enriched = "YES" if d > 0 else "NO"
        print(f"{r['snp']:12s} {a:6s} {r['location']:16s} {r['population']:8s} "
              f"{r['minor_freq_miners']:>8.3f} {r['minor_freq_controls']:>8.3f} "
              f"{enriched:>10s}  {d:+.3f}")

    print(f"\nWrote {OUT_JSON}")
    print(f"Wrote {OUT_TSV}")

if __name__ == "__main__":
    main()
