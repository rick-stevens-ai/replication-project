#!/usr/bin/env python
"""
Replication of arXiv:2206.12780 using the AUTHOR'S OWN CIRCUITS (Zenodo 6626417).

This is much stronger than our proxy sim: we run our own MWPM decoder (pymatching, uncorrelated)
on Gidney's actual pentagonal_sharp + chao Stim circuits, compare per-shot logical error rates
to the paper's reported per-shot rates (stats.csv, which used an internal correlated MWPM), and
test the paper's central quantitative claim:
    Gidney's pentagonal_sharp variant has ~2x higher threshold than Chao's construction
    (i.e. at moderate p, pentagonal_sharp has LOWER logical error rate than chao at same distance).

We use pymatching, which is uncorrelated MWPM. Gidney used a correlated internal MWPM, which is
expected to give somewhat lower LER (correlations help). So we should reproduce the QUALITATIVE
ordering (pentagon better than chao at moderate p) but our absolute LER should be >= his.
"""
from __future__ import annotations
import csv
import json
import re
import time
from pathlib import Path

import numpy as np
import stim
import pymatching


ROOT = Path(__file__).resolve().parent.parent
CIRC_DIR = ROOT / "work" / "circuits"
STATS_CSV = ROOT / "work" / "stats.csv"
OUT_DIR = ROOT / "report" / "evidence"


def load_paper_stats():
    """Load the paper's own stats.csv into a dict keyed by (b,c,d,p,r)."""
    out = {}
    with open(STATS_CSV, newline="") as f:
        reader = csv.DictReader(f, skipinitialspace=True)
        for row in reader:
            shots = int(row["shots"].strip())
            errors = int(row["errors"].strip())
            meta = json.loads(row["json_metadata"])
            key = (meta["b"], meta["c"], meta["d"], meta["p"], meta["r"])
            # Accumulate multiple rows if present (some runs are re-samples)
            prev = out.get(key)
            if prev is None:
                out[key] = {"shots": shots, "errors": errors, "q": meta.get("q")}
            else:
                out[key] = {"shots": prev["shots"] + shots, "errors": prev["errors"] + errors, "q": meta.get("q")}
    return out


def run_one(circ_path: Path, shots: int, seed: int):
    circuit = stim.Circuit.from_file(str(circ_path))
    dem = circuit.detector_error_model(decompose_errors=True, approximate_disjoint_errors=True)
    matcher = pymatching.Matching.from_detector_error_model(dem)
    sampler = circuit.compile_detector_sampler(seed=seed)
    dets, obs = sampler.sample(shots, separate_observables=True)
    preds = matcher.decode_batch(dets)
    n_err = int(np.sum(np.any(preds != obs, axis=1)))
    return {"shots": shots, "errors": n_err, "ler": n_err / shots}


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    paper = load_paper_stats()
    print(f"Loaded {len(paper)} paper data-points from stats.csv")

    # Pick a comparison set: b=X, small distances, physical error rates covering below/above pair-meas threshold.
    # For each family we do the same (d, p, r).
    families = ["chao", "pentagonal_sharp", "honeycomb"]
    distances = [5, 7]
    error_rates = [0.001, 0.002, 0.003, 0.004, 0.005, 0.007]
    shots = 20_000

    results = []
    t0 = time.time()
    for c in families:
        for d in distances:
            for p in error_rates:
                # Find matching stim circuit (r may vary per family)
                pattern = re.compile(rf"^b=X,c={re.escape(c)},d={d},p={p},q=\d+,r=(\d+)\.stim$")
                match_files = [f for f in CIRC_DIR.iterdir() if pattern.match(f.name)]
                if not match_files:
                    # Try slightly different p formatting
                    p_str = f"{p:g}"
                    pattern2 = re.compile(rf"^b=X,c={re.escape(c)},d={d},p={re.escape(p_str)},q=\d+,r=(\d+)\.stim$")
                    match_files = [f for f in CIRC_DIR.iterdir() if pattern2.match(f.name)]
                if not match_files:
                    print(f"  MISS c={c} d={d} p={p}: no circuit found")
                    continue
                cfile = match_files[0]
                m = pattern.match(cfile.name) or pattern2.match(cfile.name)
                r = int(m.group(1))
                key = ("X", c, d, p, r)
                t_s = time.time()
                res = run_one(cfile, shots, seed=(20260703 + hash(cfile.name)) % (2**31 - 1))
                res["wall_s"] = round(time.time() - t_s, 2)
                res.update({"family": c, "d": d, "p": p, "r": r, "circuit": cfile.name})
                paper_row = paper.get(key)
                if paper_row is not None:
                    res["paper_shots"] = paper_row["shots"]
                    res["paper_errors"] = paper_row["errors"]
                    res["paper_ler"] = paper_row["errors"] / paper_row["shots"] if paper_row["shots"] else None
                else:
                    res["paper_shots"] = None
                    res["paper_errors"] = None
                    res["paper_ler"] = None
                paper_str = f" paper_LER={res['paper_ler']:.3e}" if res["paper_ler"] is not None else " paper_LER=n/a"
                print(
                    f"  c={c:20s} d={d} p={p:.4f} r={r:2d} "
                    f"mine_LER={res['ler']:.3e}{paper_str} "
                    f"errs={res['errors']:4d}/{shots} ({res['wall_s']}s)"
                )
                results.append(res)

    total_s = round(time.time() - t0, 1)
    print(f"\nDone in {total_s}s")

    # Comparative summary: at each (d, p), rank families by our measured LER
    print("\n=== Pentagon vs Chao vs Honeycomb (our MWPM on paper's circuits) ===")
    print(f"{'d':>3} {'p':>8}  {'chao_LER':>12} {'pentagon_LER':>13} {'honey_LER':>12}  {'ordering (best->worst)'}")
    by_key = {}
    for r in results:
        by_key.setdefault((r["d"], r["p"]), {})[r["family"]] = r["ler"]
    matches_paper_ordering = 0
    total_ordering_tests = 0
    for (d, p), fams in sorted(by_key.items()):
        chao_l = fams.get("chao")
        pen_l = fams.get("pentagonal_sharp")
        hc_l = fams.get("honeycomb")
        pairs = [(name, val) for name, val in [("chao", chao_l), ("pentagon", pen_l), ("honey", hc_l)] if val is not None]
        pairs.sort(key=lambda x: x[1])
        ordering = " < ".join(n for n, _ in pairs)
        print(
            f"{d:>3} {p:>8.4f}  "
            f"{(chao_l if chao_l is not None else float('nan')):>12.3e} "
            f"{(pen_l if pen_l is not None else float('nan')):>13.3e} "
            f"{(hc_l if hc_l is not None else float('nan')):>12.3e}  "
            f"{ordering}"
        )
        # Key claim: pentagon should beat chao at same (d,p) in mid-range p
        if chao_l is not None and pen_l is not None:
            total_ordering_tests += 1
            if pen_l < chao_l:
                matches_paper_ordering += 1

    print(
        f"\nClaim C_ordering (pentagon < chao at same (d,p)): {matches_paper_ordering}/{total_ordering_tests} "
        f"({100 * matches_paper_ordering / max(total_ordering_tests, 1):.0f}%)"
    )

    payload = {
        "paper": "arXiv:2206.12780",
        "decoder": "pymatching MWPM (uncorrelated) on paper's own Stim circuits (Zenodo 6626417)",
        "note": "Paper used an internal correlated MWPM decoder, expected to give slightly lower LER than ours.",
        "shots_per_point": shots,
        "families": families,
        "distances": distances,
        "error_rates": error_rates,
        "results": results,
        "n_pentagon_beats_chao": matches_paper_ordering,
        "n_ordering_tests": total_ordering_tests,
        "stim_version": stim.__version__,
        "pymatching_version": pymatching.__version__,
        "total_wall_s": total_s,
    }
    out = OUT_DIR / "pentagon_vs_chao.json"
    out.write_text(json.dumps(payload, indent=2))
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
