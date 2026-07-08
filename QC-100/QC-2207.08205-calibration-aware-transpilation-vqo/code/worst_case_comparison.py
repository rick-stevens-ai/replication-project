"""
Focused CA-vs-worst-random comparison.
Force the "random" strategy to sometimes pick placements that include the
bad qubits (mirrors the paper's Fig. 11 where the worst methods drop far
below the best method — the AR spread across methods is the point).
"""
import json, time
import numpy as np
from pathlib import Path
from calibration_aware_qaoa import (
    build_problem, build_mock_device, brute_force_maxcut,
    calibration_aware_placement, run_qaoa_experiment, effective_fidelity,
    coupling_subgraph, is_connected_subgraph, SEED,
)

def bad_forced_placement(device, k, seed):
    """Pick k connected qubits, biased toward BAD qubits {8,9,15,16,17}."""
    r = np.random.default_rng(seed)
    bad = [8, 9, 15, 16, 17]
    for _ in range(500):
        # Force at least 2 bad qubits
        n_bad = min(len(bad), r.integers(2, 4))
        forced = list(r.choice(bad, size=n_bad, replace=False))
        remaining = [q for q in range(device["n_phys"]) if q not in forced]
        rest = list(r.choice(remaining, size=k - n_bad, replace=False))
        picks = tuple(sorted(forced + rest))
        if is_connected_subgraph(device, picks):
            return picks
    return tuple(range(k))

def main(out_dir):
    out_dir = Path(out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    g = build_problem(n=6)
    device = build_mock_device()
    opt = brute_force_maxcut(g)
    n_cx = 2 * g.number_of_edges()
    k = g.number_of_nodes()

    print("Worst-case (bad-biased) random placements vs cal-aware:")
    ca_place, f_ca = calibration_aware_placement(device, k, n_cx)
    print(f"  CA placement: {ca_place}, F={f_ca:.4f}")
    r_ca = run_qaoa_experiment(g, device, ca_place, "cal-aware")
    print(f"    CA best AR = {r_ca['best_AR']:.4f}")

    worst = []
    for i in range(5):
        wp = bad_forced_placement(device, k, seed=SEED + 700 + i)
        f_w = effective_fidelity(wp, device, n_cx)
        print(f"  worst trial {i+1}: {wp}, F={f_w:.4f}")
        r = run_qaoa_experiment(g, device, wp, f"worst_{i+1}", seed=SEED + 700 + i)
        r["effective_F"] = f_w
        worst.append(r)
        print(f"    AR = {r['best_AR']:.4f}")

    mean_w = float(np.mean([r["best_AR"] for r in worst]))
    std_w = float(np.std([r["best_AR"] for r in worst]))
    imp = (r_ca["best_AR"] - mean_w) / mean_w * 100
    print(f"\nCA: {r_ca['best_AR']:.4f}")
    print(f"Bad-biased random: {mean_w:.4f} ± {std_w:.4f}")
    print(f"Relative improvement of CA over bad-biased random: +{imp:.1f}%")

    def _clean(o):
        if isinstance(o, dict): return {k: _clean(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)): return [_clean(v) for v in o]
        if isinstance(o, np.integer): return int(o)
        if isinstance(o, np.floating): return float(o)
        return o
    (out_dir / "worst_case.json").write_text(json.dumps(_clean({
        "cal_aware": {"placement": list(ca_place), "effective_F": f_ca, "AR": r_ca["best_AR"]},
        "bad_biased_random": {
            "n_trials": 5, "mean_AR": mean_w, "std_AR": std_w,
            "per_trial": [{"placement": r["placement"], "AR": r["best_AR"],
                           "effective_F": r["effective_F"]} for r in worst],
        },
        "improvement_percent": imp,
    }), indent=2))
    print(f"Saved: {out_dir / 'worst_case.json'}")

if __name__ == "__main__":
    import sys
    main(sys.argv[1] if len(sys.argv) > 1 else "./evidence")
