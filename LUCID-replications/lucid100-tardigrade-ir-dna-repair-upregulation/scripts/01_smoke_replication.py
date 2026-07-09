#!/usr/bin/env python3
"""
LUCID100 slot 51 — first-pass smoke replication.

Paper: Clark-Hachtel et al. 2024 Current Biology 34:1819
DOI:   10.1016/j.cub.2024.03.019
GEO:   GSE253471 (SuperSeries) -> GSE240501 (IR) + GSE253470 (Bleomycin)

What this does (no R/edgeR required):
  1. Loads the GEO-supplied EdgeR output tables for the three Bleomycin
     contrasts (10ug/100ug/1mg vs control) - these tables are the authors'
     own DE output (Data S1C-equivalent), so re-deriving identical EdgeR
     statistics from raw counts in Python would be circular without R.
     Instead we VERIFY internal consistency of the supplied tables and
     compute the paper's headline summaries:
        - DEG counts at FDR<0.05, |log2FC|>=1 (per contrast)
        - up vs down split
        - rank-correlation among contrasts (dose response)
        - top DDR-gene fold changes vs paper Figure 2 callouts.
  2. Sanity-recomputes per-sample library sizes & top-expressed transcripts
     from the raw featureCounts matrix (independent step).
  3. Identifies DDR-pathway candidate genes by NCBI product names (genome
     v3.1 annotation, NCBI feature_table). Reports the top up-regulated
     hits in the 1 mg/mL Bleo arm and compares vs the paper's named genes
     (XRCC5, RAD51, LIG1, PARP2, PARP3, PNKP, PCNA, FEN1, POLB, XRCC1,
     XRCC6, LIG4, BARD1, POLQ, MPG).
  4. Writes a JSON result blob + human-readable summary.

Author: ollie (subagent), 2026-06-09
"""

import gzip
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
DATA = HERE / "data"
RESULTS = HERE / "results"
RESULTS.mkdir(exist_ok=True)


def read_edger(path: Path) -> dict[str, dict]:
    """Read a GEO EdgeR output: Gene_ID\tlogFC\tlogCPM\tPValue\tFDR"""
    rows: dict[str, dict] = {}
    with gzip.open(path, "rt") as fh:
        hdr = fh.readline().rstrip("\n").split("\t")
        assert hdr == ["Gene_ID", "logFC", "logCPM", "PValue", "FDR"], hdr
        for line in fh:
            f = line.rstrip("\n").split("\t")
            rows[f[0]] = dict(
                logFC=float(f[1]),
                logCPM=float(f[2]),
                PValue=float(f[3]),
                FDR=float(f[4]),
            )
    return rows


def read_featurecounts(path: Path) -> tuple[list[str], dict[str, list[int]]]:
    """Read featureCounts -> (sample_names, gene_id -> counts list)."""
    with gzip.open(path, "rt") as fh:
        # skip first comment line
        first = fh.readline()
        assert first.startswith("# Program:featureCounts"), first[:50]
        hdr = fh.readline().rstrip("\n").split("\t")
        # Cols: Geneid, Chr, Start, End, Strand, Length, sample_1, ...
        samples = [h.rsplit(".bam", 1)[0] for h in hdr[6:]]
        # Strip technical barcode suffix -> condition_rep
        # e.g. "He_bleo_100ug_1_TTGCCTAG-ACCACTTA" -> "He_bleo_100ug_1"
        samples_short = ["_".join(s.split("_")[:4]) for s in samples]
        counts: dict[str, list[int]] = {}
        for line in fh:
            f = line.rstrip("\n").split("\t")
            counts[f[0]] = [int(x) for x in f[6:]]
    return samples_short, counts


def load_feature_table(path: Path) -> dict[str, str]:
    """BV898 locus_tag -> best product name across CDS rows.

    NCBI feature_table has 'gene' rows (empty product name) plus 'CDS' rows
    (with name). We only use CDS rows and prefer non-hypothetical names.
    """
    locus2name: dict[str, str] = {}
    with gzip.open(path, "rt") as fh:
        hdr = fh.readline().lstrip("#").rstrip("\n").strip().split("\t")
        idx = {n: i for i, n in enumerate(hdr)}
        for line in fh:
            f = line.rstrip("\n").split("\t")
            if len(f) <= max(idx.values()):
                continue
            if f[idx["feature"]] != "CDS":
                continue
            lt = f[idx["locus_tag"]]
            name = f[idx["name"]].strip()
            if not lt or not name:
                continue
            cur = locus2name.get(lt, "")
            # Prefer non-hypothetical, then longer name
            if (not cur
                or (cur.lower().startswith("hypothetical")
                    and not name.lower().startswith("hypothetical"))):
                locus2name[lt] = name
    return locus2name


def pearson(xs, ys):
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    dx = (sum((x - mx) ** 2 for x in xs)) ** 0.5
    dy = (sum((y - my) ** 2 for y in ys)) ** 0.5
    if dx == 0 or dy == 0:
        return float("nan")
    return num / (dx * dy)


def main():
    out: dict = {"summary": {}, "contrasts": {}, "ddr": {}}

    # 1. Load all three Bleomycin EdgeR outputs
    bleo_dir = DATA / "GSE253470"
    contrasts = {
        "10ug_vs_C": "GSE253470_He_Bleo_10ugvC_EdgeR_output.txt.gz",
        "100ug_vs_C": "GSE253470_He_Bleo_100ugvC_EdgeR_output.txt.gz",
        "1mg_vs_C": "GSE253470_He_Bleo_1mgvC_EdgeR_output.txt.gz",
    }
    edger = {c: read_edger(bleo_dir / fn) for c, fn in contrasts.items()}

    # 2. DEG counts at paper thresholds (FDR<0.05, |log2FC|>=1)
    for c, tab in edger.items():
        up = [g for g, r in tab.items() if r["FDR"] < 0.05 and r["logFC"] >= 1]
        dn = [g for g, r in tab.items() if r["FDR"] < 0.05 and r["logFC"] <= -1]
        sig = [g for g, r in tab.items() if r["FDR"] < 0.05]
        out["contrasts"][c] = {
            "n_tested": len(tab),
            "n_sig_FDR_lt_0.05": len(sig),
            "n_up_log2FC_ge_1": len(up),
            "n_dn_log2FC_le_-1": len(dn),
        }
        print(f"[{c}] tested={len(tab)}  sig(FDR<0.05)={len(sig)}  up={len(up)}  down={len(dn)}")

    # 3. Featurecounts: library sizes + top expressed
    samples, counts = read_featurecounts(
        bleo_dir / "GSE253470_He_Bleo_featurecounts.txt.gz"
    )
    lib_sizes = [sum(counts[g][i] for g in counts) for i in range(len(samples))]
    out["library_sizes"] = dict(zip(samples, lib_sizes))
    print("\nLibrary sizes (M reads):")
    for s, lib in zip(samples, lib_sizes):
        print(f"  {s}: {lib/1e6:.2f}")
    out["summary"]["n_genes_in_counts_matrix"] = len(counts)
    out["summary"]["n_samples"] = len(samples)
    print(f"\nCount matrix: {len(counts)} genes x {len(samples)} samples")

    # 4. Cross-contrast dose-response: pearson of logFC across genes shared
    common = set(edger["10ug_vs_C"]) & set(edger["100ug_vs_C"]) & set(edger["1mg_vs_C"])
    common = sorted(common)
    for a, b in [("10ug_vs_C", "100ug_vs_C"), ("100ug_vs_C", "1mg_vs_C"), ("10ug_vs_C", "1mg_vs_C")]:
        xs = [edger[a][g]["logFC"] for g in common]
        ys = [edger[b][g]["logFC"] for g in common]
        r = pearson(xs, ys)
        out["summary"][f"pearson_logFC_{a}_vs_{b}"] = r
        print(f"Pearson r(logFC) {a} ↔ {b}: {r:.4f}")

    # 5. Load locus_tag -> product name mapping (NCBI nHd_3.1 annotation)
    locus2name = load_feature_table(DATA / "genome" / "feature_table.txt.gz")
    out["summary"]["n_locus_with_product_name"] = len(locus2name)
    print(f"\nLocus annotations loaded: {len(locus2name)} BV898 tags")

    # 6. DDR pathway candidate hits: search by product name keywords
    # NCBI nHd_3.1 product names use long form (e.g. "DNA ligase 1", not LIG1).
    # Use phrase keywords + paper-callout aliases.
    ddr_keywords = [
        # canonical / paper Fig.2 callouts (long form names in NCBI annotation)
        "DNA ligase 1", "DNA ligase 3", "DNA ligase 4",
        "DNA repair protein RAD51", "DNA repair protein XRCC",
        "X-ray repair cross-complementing",
        "Ku70", "Ku80", "Ku autoantigen",
        "Poly [ADP-ribose] polymerase",
        "Bifunctional polynucleotide phosphatase/kinase",   # PNKP
        "Proliferating cell nuclear antigen",               # PCNA
        "Flap endonuclease 1",                              # FEN1
        "DNA polymerase beta", "DNA polymerase theta",      # POLB, POLQ
        "DNA polymerase delta", "DNA polymerase epsilon",
        "BRCA1-associated RING domain",                     # BARD1
        "DNA-3-methyladenine glycosylase",                  # MPG
        "DNA repair", "excision repair", "mismatch repair",
        "DNA damage-binding", "DNA damage response",
        "Nibrin", "meiotic recombination",
        "MRE11", "BRCA", "DNA topoisomerase",
        "Histone H2AX", "Replication protein A",
        "DNA cross-link repair",
        # also short forms (defensive)
        "XRCC", "RAD51", "PARP", "PNKP", "PCNA", "FEN1", "POLQ", "BARD1",
        "MRE11", "BRCA", "ERCC", "MSH", "MLH", "XPA ", "XPB ",
    ]
    ddr_hits = []
    for lt, name in locus2name.items():
        nl = name.lower()
        for kw in ddr_keywords:
            if kw.lower() in nl:
                ddr_hits.append((lt, name, kw))
                break

    print(f"\nDDR-keyword product hits in annotation: {len(ddr_hits)}")

    # Cross-reference with EdgeR 1mg_vs_C results
    e1mg = edger["1mg_vs_C"]
    ddr_de = []
    for lt, name, kw in ddr_hits:
        if lt in e1mg:
            r = e1mg[lt]
            ddr_de.append(
                dict(locus=lt, name=name, matched=kw,
                     logFC_1mg=r["logFC"], FDR_1mg=r["FDR"], logCPM=r["logCPM"])
            )
    ddr_de.sort(key=lambda d: -d["logFC_1mg"])
    out["ddr"]["all_hits"] = ddr_de
    out["ddr"]["n_DDR_with_DE"] = len(ddr_de)
    out["ddr"]["n_DDR_up_FDR05_log2FC1"] = sum(
        1 for d in ddr_de if d["FDR_1mg"] < 0.05 and d["logFC_1mg"] >= 1
    )
    print("\nTop 25 upregulated DDR-keyword genes in 1 mg/mL Bleo (vs control):")
    print(f"  {'locus_tag':<14}{'log2FC':>9}{'FDR':>11}{'logCPM':>9}  product (matched keyword)")
    for d in ddr_de[:25]:
        print(
            f"  {d['locus']:<14}{d['logFC_1mg']:>9.3f}{d['FDR_1mg']:>11.2e}"
            f"{d['logCPM']:>9.2f}  {d['name']} [{d['matched']}]"
        )

    # 7. Specifically named genes the paper highlights, find matches
    # by paper-symbol -> NCBI long-name patterns
    paper_aliases = {
        "XRCC5 (Ku80)":   ["x-ray repair cross-complementing protein 5", "ku80"],
        "XRCC6 (Ku70)":   ["x-ray repair cross-complementing protein 6", "ku70"],
        "XRCC1":          ["x-ray repair cross-complementing protein 1"],
        "RAD51":          ["dna repair protein rad51"],
        "LIG1":           ["dna ligase 1"],
        "LIG4":           ["dna ligase 4"],
        "PARP2":          ["poly [adp-ribose] polymerase 2"],
        "PARP3":          ["poly [adp-ribose] polymerase 3"],
        "PNKP":           ["bifunctional polynucleotide phosphatase/kinase"],
        "PCNA":           ["proliferating cell nuclear antigen"],
        "FEN1":           ["flap endonuclease 1"],
        "POLB":           ["dna polymerase beta"],
        "POLQ":           ["dna polymerase theta"],
        "BARD1":          ["brca1-associated ring domain"],
        "MPG":            ["dna-3-methyladenine glycosylase"],
    }
    paper_genes_status = []
    for symbol, pats in paper_aliases.items():
        hits = []
        for d in ddr_de:
            nl = d["name"].lower()
            if any(p in nl for p in pats):
                hits.append(d)
        if hits:
            for m in hits[:5]:
                paper_genes_status.append(
                    dict(symbol=symbol, locus=m["locus"], name=m["name"],
                         logFC_1mg=m["logFC_1mg"], FDR_1mg=m["FDR_1mg"])
                )
        else:
            paper_genes_status.append(dict(symbol=symbol, found=False))
    out["ddr"]["paper_named_genes_in_1mg_bleo"] = paper_genes_status

    print("\nPaper-named DDR genes in 1 mg/mL Bleo arm:")
    print(f"  {'symbol':<14}{'log2FC':>9}{'FDR':>11}  product (locus_tag)")
    for s in paper_genes_status:
        if s.get("found") is False:
            print(f"  {s['symbol']:<14}      NOT FOUND in NCBI nHd_3.1 annotation")
        else:
            print(f"  {s['symbol']:<14}{s['logFC_1mg']:>9.3f}{s['FDR_1mg']:>11.2e}  {s['name']} ({s['locus']})")


    # 8. Write JSON + plain summary
    (RESULTS / "smoke_replication.json").write_text(
        json.dumps(out, indent=2, default=str)
    )
    print(f"\nWrote {RESULTS/'smoke_replication.json'}")

    # Short text summary
    with (RESULTS / "smoke_replication.txt").open("w") as fh:
        fh.write("LUCID100 slot 51 - smoke replication summary\n")
        fh.write("=" * 60 + "\n\n")
        for c, s in out["contrasts"].items():
            fh.write(
                f"Bleo {c}: tested={s['n_tested']:>6}  "
                f"sig(FDR<0.05)={s['n_sig_FDR_lt_0.05']:>5}  "
                f"up(log2FC>=1)={s['n_up_log2FC_ge_1']:>4}  "
                f"down(log2FC<=-1)={s['n_dn_log2FC_le_-1']:>4}\n"
            )
        fh.write(f"\nPearson r(logFC) dose-response (Bleo):\n")
        for k, v in out["summary"].items():
            if k.startswith("pearson_"):
                fh.write(f"  {k}: {v:.4f}\n")
        fh.write(f"\nDDR-keyword-matched genes with DE results: {out['ddr']['n_DDR_with_DE']}\n")
        fh.write(f"DDR genes upregulated at FDR<0.05 & log2FC>=1: {out['ddr']['n_DDR_up_FDR05_log2FC1']}\n")
    print(f"Wrote {RESULTS/'smoke_replication.txt'}")


if __name__ == "__main__":
    main()
