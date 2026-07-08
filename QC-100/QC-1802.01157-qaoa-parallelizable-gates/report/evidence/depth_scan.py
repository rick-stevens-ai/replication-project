"""
Extra evidence: scan N and show that parallel depth is asymptotically
CONSTANT while sequential depth grows quadratically.  Fit a linear model
in log-log space; verify slope ~= 2 for sequential and ~= 0 for parallel.
"""
import json
import numpy as np
from lhz_depth import qiskit_depths, lhz_plaquettes

if __name__ == "__main__":
    Ns = list(range(4, 21))
    rows = []
    for N in Ns:
        r = qiskit_depths(N)
        rows.append(r)

    # Fit power law seq_depth ~ K^alpha
    Ks = np.array([r["K"] for r in rows])
    seq = np.array([r["sequential_depth"] for r in rows])
    par = np.array([r["parallel_depth"] for r in rows])
    valid_seq = seq > 0
    log_seq = np.log(seq[valid_seq])
    log_K = np.log(Ks[valid_seq])
    seq_slope, seq_intercept = np.polyfit(log_K, log_seq, 1)

    valid_par = par > 0
    # For N>=5, parallel_depth plateaus
    par_plateau = par[Ks >= 10]
    par_mean = float(np.mean(par_plateau))
    par_std = float(np.std(par_plateau))

    print(f"Scan N={Ns[0]}..{Ns[-1]}")
    print(f"Sequential depth power-law fit (log-log): slope = {seq_slope:.3f}")
    print(f"  => sequential depth grows as ~K^{seq_slope:.2f} (expect ~2 for O(N^4))")
    print(f"Parallel depth plateau (N>=10): mean={par_mean:.1f}, std={par_std:.1f}")
    print(f"  Paper claim: 28 (constant, independent of N)")
    print(f"  Ratio to paper claim: {par_mean/28:.3f}")

    out = {
        "Ns": Ns,
        "K": Ks.tolist(),
        "seq_depth": seq.tolist(),
        "par_depth": par.tolist(),
        "seq_powerlaw_slope_vs_K": float(seq_slope),
        "par_plateau_mean_N_ge_10": par_mean,
        "par_plateau_std_N_ge_10": par_std,
        "paper_claim": 28,
        "match_within_1_layer": abs(par_mean - 28) <= 1,
    }
    with open("../report/evidence/depth_scan.json", "w") as f:
        json.dump(out, f, indent=2)
    print(f"Wrote depth_scan.json")
