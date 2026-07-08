#!/usr/bin/env python3
"""
Independent replication of Craig Gidney, arXiv:2302.07395
"Inplace Access to the Surface Code Y Basis".

Approach:
  1. Pull the paper's actual Stim circuits from the Zenodo release
     (doi.org/10.5281/zenodo.7487893).
  2. Independently sample them with an open-source stack (stim + pymatching),
     then compare our logical-error rates against the paper's own stats.csv
     (which used Google's proprietary correlated matching decoder). The
     paper's own README predicts pymatching will be "slightly worse", so we
     look for consistent-across-basis inflation (not a systematic offset for
     one basis vs another).
  3. Test three specific paper claims:
       (C1) An inplace Y-basis measurement can be built at all (d=3,5,7,9,...
            circuit files exist and decode with matched X+Z detectors).
       (C2) Y-basis LER is not wildly worse than X/Z LER at the same code
            distance (paper: Y is "twice as high, plus an additional factor
            explained by detecting-region sizes").
       (C3) The benefit of adding padding rounds "saturates at around d/2".
            We reproduce this by sweeping rb ∈ {0,1,...,10} at d=5.
       (C4) The inplace scheme (b=Y) beats the twist-braid baseline
            (b=Y_braid) at d=9 (the smallest distance where both exist).
"""
import csv
import json
import os
import re
import sys
import time
from pathlib import Path

import numpy as np
import stim
import pymatching

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
WORK = ROOT / "work"
CIRC = WORK / "circuits"
EV = ROOT / "report" / "evidence"
EV.mkdir(parents=True, exist_ok=True)

# ---- Parse paper's stats.csv ----------------------------------------------
paper_rows = []
with open(WORK / "stats.csv") as fh:
    rdr = csv.DictReader(fh)
    for row in rdr:
        row = {k.strip(): (v.strip() if isinstance(v, str) else v) for k, v in row.items()}
        meta = json.loads(row["json_metadata"])
        paper_rows.append({
            "shots": int(row["shots"]),
            "errors": int(row["errors"]),
            "decoder": row["decoder"],
            "b": meta["b"], "d": meta["d"], "p": meta["p"],
            "r": meta["r"], "rb": meta["rb"], "q": meta["q"],
            "noise": meta["noise"],
        })

def find_circuit(b, d, p, r, rb):
    pat = re.compile(rf"r={r},d={d},p={p},noise=SI1000,b={b},rb={rb},q=\d+\.stim$")
    for f in os.listdir(CIRC):
        if pat.match(f):
            return CIRC / f
    return None

def match_paper(b, d, p, r, rb):
    for row in paper_rows:
        if (row["b"] == b and row["d"] == d and abs(row["p"] - p) < 1e-9
            and row["r"] == r and row["rb"] == rb):
            return row
    return None

def rerun(path, max_shots=500_000, batch=25_000, target_errors=300,
          time_budget_s=180):
    circuit = stim.Circuit.from_file(str(path))
    dem = circuit.detector_error_model(decompose_errors=True)
    matcher = pymatching.Matching.from_detector_error_model(dem)
    sampler = circuit.compile_detector_sampler()
    tot_shots, tot_err = 0, 0
    t0 = time.time()
    while tot_shots < max_shots and tot_err < target_errors:
        if time.time() - t0 > time_budget_s:
            break
        det, obs = sampler.sample(shots=batch, separate_observables=True)
        pred = matcher.decode_batch(det)
        tot_err += int(np.any(pred != obs, axis=1).sum())
        tot_shots += batch
    ler = tot_err / tot_shots if tot_shots else float("nan")
    # Wilson-ish 1-sigma binomial
    if tot_shots:
        se = float(np.sqrt(ler * (1 - ler) / tot_shots))
    else:
        se = float("nan")
    return {
        "path": path.name,
        "num_qubits": circuit.num_qubits,
        "num_detectors": circuit.num_detectors,
        "num_observables": circuit.num_observables,
        "shots": tot_shots,
        "errors": tot_err,
        "logical_error_rate": ler,
        "ler_stderr": se,
        "elapsed_s": round(time.time() - t0, 3),
    }

# ---- Experiment A: cross-check vs paper table -----------------------------
CROSS = [
    ("Y",         3, 0.001, 3, 3),
    ("Y_folded",  3, 0.001, 3, 0),
    ("X",         3, 0.001, 3, 0),
    ("Z",         3, 0.001, 3, 0),
    ("Y",         5, 0.001, 5, 4),
    ("X",         5, 0.001, 5, 0),
    ("Z",         5, 0.001, 5, 0),
    ("Y",         7, 0.001, 7, 5),
    ("X",         7, 0.001, 7, 0),
    ("Z",         7, 0.001, 7, 0),
]
crossA = []
print(">>> Experiment A: cross-check against paper's stats.csv")
for (b, d, p, r, rb) in CROSS:
    path = find_circuit(b, d, p, r, rb)
    if path is None:
        print(f"  [MISS] b={b} d={d} r={r} rb={rb}")
        continue
    print(f"  [RUN ] b={b:<10} d={d} r={r} rb={rb} :: {path.name}")
    sys.stdout.flush()
    res = rerun(path)
    paper = match_paper(b, d, p, r, rb)
    row = {**res, "b": b, "d": d, "p": p, "r": r, "rb": rb}
    if paper:
        pler = paper["errors"] / paper["shots"]
        row.update({"paper_decoder": paper["decoder"],
                    "paper_shots": paper["shots"],
                    "paper_errors": paper["errors"],
                    "paper_ler": pler,
                    "ratio_ours_over_paper": res["logical_error_rate"] / pler})
    print(f"          ours_LER={res['logical_error_rate']:.3e} "
          f"(±{res['ler_stderr']:.1e}, {res['shots']} shots, "
          f"{res['errors']} err) paper_LER="
          f"{row.get('paper_ler', float('nan')):.3e} "
          f"ratio={row.get('ratio_ours_over_paper', float('nan')):.2f}")
    crossA.append(row)

# ---- Experiment B: braid vs inplace at d=9 (paper's headline claim) -------
print("\n>>> Experiment B: inplace (b=Y) vs twist-braid baseline (b=Y_braid) at d=9")
inplace_rb = 4       # padding rounds ~d/2
braid_rb   = 4
crossB = []
for (b, rb_val) in [("Y", inplace_rb), ("Y_braid", braid_rb)]:
    path = find_circuit(b, 9, 0.001, 9, rb_val)
    if path is None:
        print(f"  [MISS] b={b} d=9 rb={rb_val}")
        continue
    print(f"  [RUN ] b={b:<10} d=9 rb={rb_val} :: {path.name}")
    sys.stdout.flush()
    res = rerun(path, time_budget_s=240)
    paper = match_paper(b, 9, 0.001, 9, rb_val)
    row = {**res, "b": b, "d": 9, "p": 0.001, "r": 9, "rb": rb_val}
    if paper:
        pler = paper["errors"] / paper["shots"]
        row["paper_ler"] = pler
        row["paper_shots"] = paper["shots"]
        row["paper_errors"] = paper["errors"]
    print(f"          ours_LER={res['logical_error_rate']:.3e} "
          f"(±{res['ler_stderr']:.1e}, {res['shots']} shots) "
          f"paper_LER={row.get('paper_ler', float('nan')):.3e}")
    crossB.append(row)

# ---- Experiment C: padding-round saturation at d=5 (paper Fig 12 claim) ---
# Paper: benefit saturates at ~d/2 padding rounds. For d=5, that's ~2-3.
print("\n>>> Experiment C: padding-round sweep at d=5 (claim: saturates ~d/2)")
crossC = []
for rb in [0, 1, 2, 3, 4, 6, 8, 10]:
    path = find_circuit("Y", 5, 0.001, 5, rb)
    if path is None:
        continue
    print(f"  [RUN ] b=Y d=5 rb={rb:>2}")
    sys.stdout.flush()
    res = rerun(path, time_budget_s=90)
    paper = match_paper("Y", 5, 0.001, 5, rb)
    row = {**res, "b": "Y", "d": 5, "p": 0.001, "r": 5, "rb": rb}
    if paper:
        pler = paper["errors"] / paper["shots"]
        row["paper_ler"] = pler
    print(f"          ours_LER={res['logical_error_rate']:.3e} "
          f"(±{res['ler_stderr']:.1e}) paper_LER="
          f"{row.get('paper_ler', float('nan')):.3e}")
    crossC.append(row)

# ---- Experiment D: structural round counting -----------------------------
def circuit_structure(path: Path):
    text = path.read_text()
    reps = [int(m.group(1)) for m in re.finditer(r"REPEAT\s+(\d+)\s*\{", text)]
    return {"path": path.name, "num_repeat_blocks": len(reps),
            "repeat_counts": reps, "total_lines": text.count("\n")}

structural = []
for d in (3, 5, 7, 9, 11, 13, 15):
    path = find_circuit("Y", d, 0.001, d, 0)   # rb=0: no padding, minimal-round variant
    if path is not None:
        s = circuit_structure(path)
        structural.append({**s, "b": "Y", "d": d, "rb": 0,
                           "floor_d_over_2_plus_2": (d // 2) + 2,
                           "d_minus_1": d - 1})

# ---- Emit evidence + summary ---------------------------------------------
with open(EV / "expA_cross_check.json", "w") as fh:
    json.dump(crossA, fh, indent=2)
with open(EV / "expB_inplace_vs_braid.json", "w") as fh:
    json.dump(crossB, fh, indent=2)
with open(EV / "expC_padding_sweep.json", "w") as fh:
    json.dump(crossC, fh, indent=2)
with open(EV / "expD_structure.json", "w") as fh:
    json.dump(structural, fh, indent=2)

print("\n=================== SUMMARY ===================")
print("\n[A] Cross-check vs paper (pymatching vs internal_correlated)")
print(f"{'b':<10}{'d':>3}{'rb':>4}  {'ours_LER':>12}{'paper_LER':>12}{'ratio':>8}")
for r in crossA:
    print(f"{r['b']:<10}{r['d']:>3}{r['rb']:>4}  "
          f"{r['logical_error_rate']:>12.3e}"
          f"{r.get('paper_ler', float('nan')):>12.3e}"
          f"{r.get('ratio_ours_over_paper', float('nan')):>8.2f}")

print("\n[B] Inplace vs braid at d=9")
for r in crossB:
    print(f"  {r['b']:<10} rb={r['rb']:>2}  ours={r['logical_error_rate']:.3e} "
          f"paper={r.get('paper_ler', float('nan')):.3e}")

print("\n[C] Padding sweep at d=5 (expect saturation around rb ~ d/2 = 2-3)")
for r in crossC:
    print(f"  rb={r['rb']:>2}  ours={r['logical_error_rate']:.3e} "
          f"paper={r.get('paper_ler', float('nan')):.3e}")

print("\n[D] Structural — b=Y, rb=0, r=d (minimal-round inplace variant)")
for r in structural:
    print(f"  d={r['d']:>2}  REPEAT blocks={r['num_repeat_blocks']} "
          f"counts={r['repeat_counts']}  ⌊d/2⌋+2={r['floor_d_over_2_plus_2']}")
