"""Empirical runtime-scaling verification: fit log-time vs t and confirm the exponent.

The paper's central claim (Eq. 6):
    chi_delta(T^t) ~ 2^{alpha t}  with alpha = -2 log2 cos(pi/8) = 0.2284

We time the sum-over-Cliffords simulator (exact, 2^t branches) and the sampled
low-rank simulator (k = ceil(2^{alpha t}) branches) as t grows.  Then we log-linear-fit
the runtimes to extract the empirical exponent and compare to (1.0 for SOC, 0.2284
for low-rank).
"""
from __future__ import annotations
import json, math, os, sys, time
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stabilizer_rank_sim import (
    Gate, statevector_sim, expectation_Z, sum_over_cliffords_state,
    low_rank_expectation_Z_sampled, build_test_circuit, ALPHA
)


def time_it(fn, *args, **kw):
    t0 = time.perf_counter()
    out = fn(*args, **kw)
    return out, time.perf_counter() - t0


def main():
    outdir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "report", "evidence"))
    os.makedirs(outdir, exist_ok=True)

    n = 6
    t_values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    rows = []
    for t in t_values:
        circuit = build_test_circuit(n, t, seed=42)
        # ground truth
        psi, sv_time = time_it(statevector_sim, n, circuit)
        z_ref = expectation_Z(psi, 0, n)
        # SOC (exact)
        (accum, branches), soc_time = time_it(sum_over_cliffords_state, n, circuit)
        z_soc = expectation_Z(accum, 0, n)
        # low-rank sampling: pick R runs of k = ceil(2^{alpha t}), take mean
        k = max(1, int(math.ceil(2 ** (ALPHA * t))))
        R = 32
        vals = []
        t0 = time.perf_counter()
        for r in range(R):
            v, _ = low_rank_expectation_Z_sampled(n, circuit, 0, k, seed=1000 + r)
            vals.append(np.real(v))
        lr_time_per_run = (time.perf_counter() - t0) / R
        z_lr = float(np.mean(vals))
        z_lr_sem = float(np.std(vals) / math.sqrt(R))
        rows.append(dict(
            n=n, t=t, k=k, R=R,
            z_sv=float(z_ref), z_soc=float(z_soc), z_lr=z_lr, z_lr_sem=z_lr_sem,
            sv_time_s=sv_time, soc_time_s=soc_time, lr_time_s_per_run=lr_time_per_run,
            branches=branches, target_2_to_alpha_t=2 ** (ALPHA * t),
            soc_ok=abs(z_soc - z_ref) < 1e-9,
        ))
        print(f"n={n} t={t:2d} k={k:4d}: z_sv={z_ref:+.6f} z_soc={z_soc:+.6f} z_lr={z_lr:+.6f}+/-{z_lr_sem:.3f} "
              f"soc_time={soc_time*1000:.2f}ms lr_time={lr_time_per_run*1000:.2f}ms")

    # Fit log2(time) = a + b*t for SOC and low-rank
    ts = np.array([r["t"] for r in rows])
    soc_log = np.log2([r["soc_time_s"] for r in rows])
    lr_log = np.log2([r["lr_time_s_per_run"] for r in rows])
    # slope via least squares
    A = np.vstack([ts, np.ones_like(ts)]).T
    b_soc, _ = np.linalg.lstsq(A, soc_log, rcond=None)[0], None
    b_lr, _ = np.linalg.lstsq(A, lr_log, rcond=None)[0], None
    # Actually numpy returns array; use item(0)
    soc_slope = float(np.linalg.lstsq(A, soc_log, rcond=None)[0][0])
    lr_slope = float(np.linalg.lstsq(A, lr_log, rcond=None)[0][0])
    print(f"\nEmpirical log2-time slope vs t:")
    print(f"  SOC (expected 1.000):       {soc_slope:.3f}")
    print(f"  Low-rank (expected {ALPHA:.3f}): {lr_slope:.3f}")

    summary = dict(
        alpha_predicted=ALPHA,
        soc_slope_empirical=soc_slope,
        lr_slope_empirical=lr_slope,
        soc_slope_expected=1.0,
        lr_slope_expected=ALPHA,
        rows=rows,
        note=(
            "SOC = sum-over-Cliffords exact (2^t Clifford branches per T gate); slope "
            "should be ~1.0 in log2-t.  Low-rank = importance-sampled with k=ceil(2^{alpha*t}) "
            "branches; slope should match alpha ~= 0.228 in log2-t (small deviations from "
            "constant overhead per Clifford branch)."
        ),
    )
    with open(os.path.join(outdir, "verify_scaling.json"), "w") as f:
        json.dump(summary, f, indent=2)
    print("\nWrote:", os.path.join(outdir, "verify_scaling.json"))


if __name__ == "__main__":
    main()
