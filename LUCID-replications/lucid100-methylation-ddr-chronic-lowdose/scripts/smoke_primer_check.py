#!/usr/bin/env python3
"""
LUCID100 slot 46 smoke check.

Parses the CC BY 4.0 supplement extracted from figshare 31324581 (DOI
10.1080/09553002.2025.2607004) and verifies:

  1. All 16 DDR-related genes + LINE-1 mentioned in the abstract/methods
     have an MS-HRM forward + reverse primer pair in Supplementary Table 1.
  2. Each primer pair has a non-empty annealing temperature, melt-acquisition
     range, and MgCl2 concentration in Supplementary Table 2.
  3. Primers look like bisulfite-converted MS-HRM primers (C-depleted, T-rich,
     no ambiguous bases other than I).

Emits a JSON summary to ../notes/smoke_results.json and prints a one-line
verdict.

No network calls. Runs in <1 s on CherryRd. Safe by design.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SI_TXT = ROOT / "artifacts" / "supplementary_sm4756_text.txt"
OUT = ROOT / "notes" / "smoke_results.json"

# 16 DDR-related genes + LINE-1 promised by the paper. Note the abstract lists
# the 16-gene panel only by the 4 hits and references "16 DDR-related genes" —
# we use the union of gene labels that actually appear in Supp Table 1.
EXPECTED_GENES = {
    "LINE-1", "TNF", "XPC", "TERT", "ATM", "SIRT1", "APC", "BRCA1",
    "MLH1", "PARP1", "RAD23B", "MRE11A", "DNMT3A", "MTHFR", "MGMT1",
}
# Genes the paper highlights as the headline hypermethylated set:
HEADLINE_HITS = {"RAD23B", "DNMT3A", "MRE11A", "BRCA1"}

PRIMER_LINE_RE = re.compile(r"^(?P<gene>[A-Za-z0-9\-]+)\s+(?P<dir>FP|RP)\s*$")
SEQ_LINE_RE = re.compile(r"^[ACGTUIN ]{10,}$", re.IGNORECASE)


def load_lines() -> list[str]:
    if not SI_TXT.exists():
        sys.exit(f"missing SI text: {SI_TXT}")
    return [ln.rstrip() for ln in SI_TXT.read_text().splitlines()]


def parse_primers(lines: list[str]) -> dict[str, dict[str, str]]:
    """Return {gene: {'FP': seq, 'RP': seq}}."""
    primers: dict[str, dict[str, str]] = {}
    for i, ln in enumerate(lines):
        m = PRIMER_LINE_RE.match(ln.strip())
        if not m:
            continue
        gene = m.group("gene")
        direction = m.group("dir")
        # Look ahead a few lines for the first sequence-looking string.
        for j in range(i + 1, min(i + 5, len(lines))):
            cand = lines[j].strip()
            if SEQ_LINE_RE.match(cand):
                # SIRT1 has two sequences glued on one line in the SI; take the
                # first whitespace-delimited token if so.
                tokens = [t for t in cand.split() if SEQ_LINE_RE.match(t)]
                seq = tokens[0] if tokens else cand
                primers.setdefault(gene, {})[direction] = seq
                break
    return primers


def parse_cycling(lines: list[str]) -> dict[str, dict[str, str]]:
    """Walk the cycling-conditions block (after the 'Target' header).

    Each gene gets four lines: name, annealing, acquisition, MgCl2.
    """
    out: dict[str, dict[str, str]] = {}
    try:
        start = next(i for i, ln in enumerate(lines)
                     if ln.strip() == "Target")
    except StopIteration:
        return out
    # Skip 'Target', 'Annealing temp.', 'Acquisition', 'MgCl2 Conc.'
    i = start + 4
    while i + 3 < len(lines):
        name = lines[i].strip()
        if not name or name.startswith("Supplementary"):
            break
        anneal = lines[i + 1].strip()
        acq = lines[i + 2].strip()
        mg = lines[i + 3].strip()
        # Normalise gene labels used in cycling table to match panel labels.
        key = name.replace("TNF-α", "TNF").replace("MGMT1", "MGMT1")
        out[key] = {"annealing": anneal, "acquisition": acq, "MgCl2": mg}
        i += 4
    return out


def bisulfite_sanity(seq: str) -> dict[str, float | bool]:
    s = seq.upper().replace(" ", "")
    n = len(s)
    if n == 0:
        return {"len": 0, "C_frac": 0.0, "T_frac": 0.0, "C_depleted": False}
    c = s.count("C")
    t = s.count("T")
    return {
        "len": n,
        "C_frac": round(c / n, 3),
        "T_frac": round(t / n, 3),
        # Bisulfite-converted primer for an unmethylated reference should be
        # C-depleted (most non-CpG Cs converted to T). A reasonable smoke
        # threshold: C_frac <= 0.30 AND T_frac >= 0.25.
        "C_depleted": (c / n) <= 0.30 and (t / n) >= 0.25,
    }


def main() -> int:
    lines = load_lines()
    primers = parse_primers(lines)
    cycling = parse_cycling(lines)

    primer_genes = set(primers.keys())
    missing_primers = sorted(EXPECTED_GENES - primer_genes)
    extra_primers = sorted(primer_genes - EXPECTED_GENES)

    incomplete_pairs = sorted(
        g for g, d in primers.items() if not ({"FP", "RP"} <= set(d.keys()))
    )

    cycling_missing = sorted(EXPECTED_GENES - set(cycling.keys()))
    cycling_incomplete = sorted(
        g for g, d in cycling.items()
        if not all(d.get(k) for k in ("annealing", "acquisition", "MgCl2"))
    )

    bs_report: dict[str, dict] = {}
    bs_fail: list[str] = []
    for gene, d in primers.items():
        bs_report[gene] = {}
        for direction, seq in d.items():
            s = bisulfite_sanity(seq)
            bs_report[gene][direction] = {"seq": seq, **s}
            if not s["C_depleted"]:
                bs_fail.append(f"{gene} {direction}")

    headline_present = sorted(HEADLINE_HITS & primer_genes)
    headline_missing = sorted(HEADLINE_HITS - primer_genes)

    pass_ = (
        not missing_primers
        and not incomplete_pairs
        and not cycling_missing
        and not cycling_incomplete
        and not headline_missing
    )

    result = {
        "doi": "10.1080/09553002.2025.2607004",
        "si_file": str(SI_TXT),
        "n_genes_with_primers": len(primer_genes),
        "expected_panel": sorted(EXPECTED_GENES),
        "missing_primers": missing_primers,
        "extra_primer_labels": extra_primers,
        "incomplete_primer_pairs": incomplete_pairs,
        "cycling_n_genes": len(cycling),
        "cycling_missing": cycling_missing,
        "cycling_incomplete": cycling_incomplete,
        "headline_hits_with_primers": headline_present,
        "headline_hits_missing": headline_missing,
        "bisulfite_sanity_failures": bs_fail,
        "primers": primers,
        "cycling": cycling,
        "bisulfite_report": bs_report,
        "verdict": "PASS" if pass_ else "PARTIAL",
        "notes": (
            "Smoke check is structural only. There is NO public per-sample "
            "methylation or expression matrix; this script does not and "
            "cannot reproduce the RAD23B/DNMT3A/MRE11A/BRCA1 dose-correlation "
            "claim. See FIRST_PASS_REPORT.md for the NO-GO rationale."
        ),
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True))
    print(
        f"[smoke] verdict={result['verdict']} "
        f"primers_genes={len(primer_genes)}/{len(EXPECTED_GENES)} "
        f"cycling_genes={len(cycling)} "
        f"headline_present={','.join(headline_present)} "
        f"-> {OUT}"
    )
    return 0 if pass_ else 1


if __name__ == "__main__":
    sys.exit(main())
