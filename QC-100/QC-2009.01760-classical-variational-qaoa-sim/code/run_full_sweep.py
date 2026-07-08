"""Run the full replication sweep: fidelity vs qubit count, at p=1 and p=2.

Mirrors the structure of Fig. 3 of Medvidović & Carleo 2020/21 but at
smaller scale (paper: 10-18 qubits; we use n=6,8,10 to keep runtime bounded
for a per-turn subagent replication).
"""
from __future__ import annotations

import json
import math
import os
import time

from classical_variational import run_replication

OUT = "../data/full_sweep_results.json"

# Keep total runtime bounded. FD gradient cost scales ~ params * 2^n per step.
# Adam FD with H = 2n:  ~ (n=6: 2s), (n=8: 40s), (n=10: ~5min at 300 steps).
# So we use H=2n and step count that keeps a 3-graph sweep manageable.
CONFIGS = []
# p = 1 sweep: n = 6, 8, 10
CONFIGS.append(dict(n=6,  p=1, H=8,  n_steps=250, lr=0.03))
CONFIGS.append(dict(n=8,  p=1, H=12, n_steps=200, lr=0.03))
CONFIGS.append(dict(n=10, p=1, H=12, n_steps=150, lr=0.03))
# p = 2 sweep: n = 6, 8
CONFIGS.append(dict(n=6,  p=2, H=10, n_steps=250, lr=0.03))
CONFIGS.append(dict(n=8,  p=2, H=14, n_steps=200, lr=0.03))


def gammas_betas_for(p: int):
    if p == 1:
        return [0.6155], [math.pi / 8]
    elif p == 2:
        return [0.42, 0.66], [0.55, 0.29]
    elif p == 4:
        return [0.31, 0.51, 0.66, 0.75], [0.61, 0.48, 0.32, 0.14]
    raise ValueError(p)


def main() -> None:
    all_results = []
    seed_graphs = [42, 43]  # two random 3-reg graphs per (n, p) to average over

    for cfg in CONFIGS:
        p = cfg["p"]
        gammas, betas = gammas_betas_for(p)
        for sg in seed_graphs:
            print(f"\n>>> n={cfg['n']} p={p} H={cfg['H']} steps={cfg['n_steps']} seed_graph={sg}")
            t0 = time.time()
            res = run_replication(
                n=cfg["n"],
                seed_graph=sg,
                seed_nn=0,
                p=p,
                gammas=gammas,
                betas=betas,
                H=cfg["H"],
                n_steps=cfg["n_steps"],
                lr=cfg["lr"],
                verbose=False,
            )
            elapsed = time.time() - t0
            res["config"] = cfg
            all_results.append(res)
            print(
                f"    fid={res['fidelity_NN_vs_exact']:.4f}  "
                f"E_NN={res['E_NN_variational']:.4f}  "
                f"E_ex={res['E_exact_statevector']:.4f}  "
                f"rel_err={abs(res['E_NN_variational']-res['E_exact_statevector'])/max(1e-9,abs(res['E_exact_statevector'])):.3e}  "
                f"({elapsed:.1f}s)"
            )

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(all_results, f)

    # Summary table by (n, p)
    from collections import defaultdict
    grouped = defaultdict(list)
    for r in all_results:
        grouped[(r["n"], r["p"])].append(r)

    print("\n\n============ REPLICATION SUMMARY TABLE ============")
    print(f"{'n':>4} {'p':>3} {'H':>4} {'mean_fid':>10} {'std_fid':>10} {'mean_relE':>12}  {'n_seeds':>7}")
    summary_rows = []
    for (n, p), rs in sorted(grouped.items()):
        fids = [r["fidelity_NN_vs_exact"] for r in rs]
        rel_es = [
            abs(r["E_NN_variational"] - r["E_exact_statevector"])
            / max(1e-9, abs(r["E_exact_statevector"]))
            for r in rs
        ]
        import statistics
        mean_f = statistics.mean(fids)
        std_f = statistics.stdev(fids) if len(fids) > 1 else 0.0
        mean_e = statistics.mean(rel_es)
        H = rs[0]["H_hidden"]
        print(f"{n:>4} {p:>3} {H:>4} {mean_f:>10.4f} {std_f:>10.4f} {mean_e:>12.3e}  {len(rs):>7}")
        summary_rows.append(dict(n=n, p=p, H=H, mean_fid=mean_f, std_fid=std_f, mean_rel_E=mean_e, n_seeds=len(rs)))

    # Also record analytical-vs-statevector agreement across the sweep at p=1
    p1 = [r for r in all_results if r["p"] == 1]
    if p1:
        diffs = [abs(r["E_exact_statevector"] - r["E_p1_analytical"]) for r in p1]
        print(f"\nAppendix A analytical vs statevector (p=1): max |diff| = {max(diffs):.3e}, mean = {sum(diffs)/len(diffs):.3e}")

    with open(OUT.replace(".json", "_summary.json"), "w") as f:
        json.dump(summary_rows, f, indent=2)


if __name__ == "__main__":
    main()
