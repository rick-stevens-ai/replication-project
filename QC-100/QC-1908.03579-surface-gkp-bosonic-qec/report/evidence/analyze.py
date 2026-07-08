#!/usr/bin/env python3
"""Post-hoc analysis: estimate crossing point (threshold proxy) from
the (bias, distance, p, p_L) grid produced by sim_surface_biased.py.

We use the standard cheap crossing-based threshold estimator: find the p
at which p_L(d) curves for adjacent d cross (i.e. increasing d stops
helping).  Not a critical-exponent fit, just an interval estimate.
"""
import json
from pathlib import Path
from collections import defaultdict

DATA = Path(__file__).resolve().parents[1] / "data" / "results.json"

payload = json.loads(DATA.read_text())
rows = payload["results"]

# group by bias, distance -> list of (p, pL)
by = defaultdict(lambda: defaultdict(list))
for r in rows:
    by[r["bias"]][r["distance"]].append((r["p"], r["p_L"]))

for bias, dmap in by.items():
    print(f"\n=== bias={bias} ===")
    dists = sorted(dmap.keys())
    ps = sorted({p for d in dists for (p, _) in dmap[d]})
    # print a compact table
    hdr = "p       " + "  ".join(f"d={d:<8d}" for d in dists)
    print(hdr)
    for p in ps:
        row_str = f"{p:.4f}  "
        for d in dists:
            pL = dict(dmap[d]).get(p, None)
            row_str += f"{pL:.3e}    " if pL is not None else "  --       "
        print(row_str)

    # crossing estimator: at each p, is p_L(d=3) > p_L(d=5) > p_L(d=7)?
    print("\ncrossing markers (below/above threshold):")
    for p in ps:
        pl = {d: dict(dmap[d]).get(p) for d in dists}
        if all(v is not None for v in pl.values()):
            monotone_dec = all(pl[dists[i]] > pl[dists[i+1]] for i in range(len(dists)-1))
            monotone_inc = all(pl[dists[i]] < pl[dists[i+1]] for i in range(len(dists)-1))
            tag = "BELOW" if monotone_dec else ("ABOVE" if monotone_inc else "MIXED")
            print(f"  p={p:.4f}  {tag}  " +
                  " ".join(f"d{d}={pl[d]:.3e}" for d in dists))

    # find approximate threshold interval: last p that is BELOW ... first p that is ABOVE
    below_ps = []
    above_ps = []
    for p in ps:
        pl = {d: dict(dmap[d]).get(p) for d in dists}
        if all(v is not None for v in pl.values()):
            if all(pl[dists[i]] > pl[dists[i+1]] for i in range(len(dists)-1)):
                below_ps.append(p)
            elif all(pl[dists[i]] < pl[dists[i+1]] for i in range(len(dists)-1)):
                above_ps.append(p)
    if below_ps and above_ps:
        print(f"\n  approx threshold interval: ({max(below_ps):.4f}, {min(above_ps):.4f})")
    elif below_ps:
        print(f"\n  approx threshold: > {max(below_ps):.4f} (no ABOVE point in range)")
    elif above_ps:
        print(f"\n  approx threshold: < {min(above_ps):.4f} (no BELOW point in range)")
