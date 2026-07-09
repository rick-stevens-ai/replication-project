#!/usr/bin/env python3
"""Scaling study: does Duerr-Hoyer quantum-min queries scale like sqrt(L)?

Runs QVA-style min-finding on the trellis path metric arrays for N=4..10
(L = 2^4..2^10) and reports:
  * classical brute-force queries    = L
  * DH expected upper bound (22.5*sqrt(L))
  * DH measured mean queries (over 20 trials)
  * success rate (matches argmin value)
  * empirical exponent alpha where queries ~ L^alpha (fit)
"""
import json
import math
from pathlib import Path
import numpy as np

from qva_replication import (
    encode, bsc, enumerate_path_metrics, duerr_hoyer_min, K, FANOUT
)

OUT = Path(__file__).parent
rng_master = np.random.default_rng(123)

msg = rng_master.integers(0, 2, size=20, dtype=np.int8)
codeword = encode(msg)
received = bsc(codeword, 0.05, rng_master)

sweep = []
for N in [4, 5, 6, 7, 8, 9, 10]:
    if received.size < 2 * N:
        # extend receipt if needed (shouldn't happen for msg_len 20)
        continue
    metrics = enumerate_path_metrics(received[:2*N], N)
    L = metrics.size
    argmin_val = int(metrics.min())
    trials_q, trials_ok = [], 0
    NTRIALS = 20
    for t in range(NTRIALS):
        rr = np.random.default_rng(1000 + N*100 + t)
        _, qval, qq, _ = duerr_hoyer_min(metrics, rr, max_outer=80)
        trials_q.append(qq)
        if qval == argmin_val:
            trials_ok += 1
    sweep.append({
        "N": N,
        "L_eq_F_pow_N": L,
        "classical_queries": L,
        "dh_upper_bound_22p5_sqrtL": 22.5 * math.sqrt(L),
        "dh_measured_mean_queries": float(np.mean(trials_q)),
        "dh_measured_median_queries": float(np.median(trials_q)),
        "success_rate": trials_ok / NTRIALS,
        "trials": NTRIALS,
    })

# Fit alpha where queries ~ c * L^alpha (log-log linear regression)
xs = np.array([math.log(r["L_eq_F_pow_N"]) for r in sweep])
ys = np.array([math.log(r["dh_measured_mean_queries"]) for r in sweep])
alpha, log_c = np.polyfit(xs, ys, 1)
c = math.exp(log_c)

out = {
    "sweep": sweep,
    "log_log_fit": {
        "queries_model": "queries = c * L^alpha",
        "alpha": float(alpha),
        "c": float(c),
        "expected_alpha_if_sqrt_speedup": 0.5,
        "expected_alpha_if_no_speedup": 1.0,
    },
}
(OUT / "scaling.json").write_text(json.dumps(out, indent=2))

print(f"{'N':>3} {'L':>7} {'classical':>10} {'DH-upper':>10} {'DH-meas':>10} {'success':>8}")
for r in sweep:
    print(f"{r['N']:>3} {r['L_eq_F_pow_N']:>7} {r['classical_queries']:>10} "
          f"{r['dh_upper_bound_22p5_sqrtL']:>10.1f} {r['dh_measured_mean_queries']:>10.1f} "
          f"{r['success_rate']:>8.2f}")
print(f"\nLog-log fit: queries ~ {c:.2f} * L^{alpha:.3f}")
print(f"  (0.5 = perfect sqrt speedup ; 1.0 = no speedup)")
