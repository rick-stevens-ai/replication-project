"""Refined scaling: dense s-grid, adaptive minimum-finding, plus track the
instantaneous ground state's overlap with |z=00..0> = |m=+n/2> in the
symmetric subspace (which is index dim-1 with our convention m=-j..+j)."""

import json, time
from pathlib import Path
import numpy as np

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from symmetric_subspace import build_HP_sym, build_HB_sym, build_HE_sym_full, build_HE_sym_farhi
from adiabatic_paths import A_FARHI

HERE = Path(__file__).resolve().parent


def dense_gap_sweep(HB, HP, HE, n_s=2001, use_HE=True):
    """Very fine s-grid to nail the true g_min."""
    s_grid = np.linspace(0, 1, n_s)
    gaps = np.zeros(n_s)
    ov_gs_with_z0 = np.zeros(n_s)
    dim = HB.shape[0]
    # |z=00..0> in symmetric basis = m=+n/2 = last index (m from -j to +j)
    z0_idx = dim - 1
    for idx, s in enumerate(s_grid):
        H = (1 - s) * HB + s * HP
        if use_HE and HE is not None:
            H = H + s * (1 - s) * HE
        w, v = np.linalg.eigh(H)
        gaps[idx] = w[1] - w[0]
        ov_gs_with_z0[idx] = abs(v[z0_idx, 0]) ** 2
    return s_grid, gaps, ov_gs_with_z0


def refine_gap_min(HB, HP, HE, s_center, use_HE=True, span=0.02, n_refine=2001):
    """Around a candidate s_center, do a finer sweep to nail g_min."""
    s0 = max(0.0, s_center - span)
    s1 = min(1.0, s_center + span)
    s_grid = np.linspace(s0, s1, n_refine)
    gaps = np.zeros(n_refine)
    for idx, s in enumerate(s_grid):
        H = (1 - s) * HB + s * HP
        if use_HE and HE is not None:
            H = H + s * (1 - s) * HE
        w = np.linalg.eigvalsh(H)
        gaps[idx] = w[1] - w[0]
    imin = int(np.argmin(gaps))
    return float(gaps[imin]), float(s_grid[imin])


def run(ns=(4, 6, 8, 10, 12, 16, 20, 30, 50, 80, 120, 200)):
    from adiabatic_paths import A_FARHI
    results = {}
    for n in ns:
        t0 = time.time()
        HP = build_HP_sym(n)
        HB = build_HB_sym(n)
        # Full HE for n<=12; leading order beyond.
        if n <= 12:
            HE = build_HE_sym_full(n, A_FARHI)
            HE_kind = "full-from-A_FARHI"
        else:
            HE = build_HE_sym_farhi(n)
            HE_kind = "leading-order-asymptotic"

        # First pass: dense grid n_s=2001
        s_g_lin, g_lin, ov_lin = dense_gap_sweep(HB, HP, None, n_s=2001, use_HE=False)
        s_g_far, g_far, ov_far = dense_gap_sweep(HB, HP, HE, n_s=2001, use_HE=True)
        i_lin = int(np.argmin(g_lin))
        i_far = int(np.argmin(g_far))
        # Refine near the coarse minimum
        gm_lin, sm_lin = refine_gap_min(HB, HP, None, s_g_lin[i_lin], use_HE=False,
                                        span=1.5/2000, n_refine=4001)
        gm_far, sm_far = refine_gap_min(HB, HP, HE, s_g_far[i_far], use_HE=True,
                                        span=1.5/2000, n_refine=4001)
        # Ground state overlap of GS(s=1) with |z=00..0> (should be 1 by construction of HP)
        # For linear path: track GS at s=1 -- always the |0..0> since HP is diagonal in Z basis.
        # More interesting: overlap at s=s_min_lin -- to see if GS "picked up" the right state
        # or fell off a cliff.
        results[str(n)] = {
            "n": n,
            "dim_sym": n + 1,
            "HE_kind": HE_kind,
            "linear": {"g_min": gm_lin, "s_at_min": sm_lin,
                       "gs_overlap_z0_at_smin": float(ov_lin[i_lin]),
                       "gs_overlap_z0_at_s1": float(ov_lin[-1])},
            "farhi_A": {"g_min": gm_far, "s_at_min": sm_far,
                        "gs_overlap_z0_at_smin": float(ov_far[i_far]),
                        "gs_overlap_z0_at_s1": float(ov_far[-1])},
            "gap_ratio": gm_far / gm_lin,
            "T_ratio_lin_over_far": (gm_far / gm_lin) ** 2,
            "wall_seconds": time.time() - t0,
        }
        print(f"[n={n:3d}] lin: g={gm_lin:9.5f} @s={sm_lin:.4f}   FarhiA: g={gm_far:9.4f} @s={sm_far:.4f}   ratio={gm_far/gm_lin:8.2f}   T-ratio={(gm_far/gm_lin)**2:11.2f}  ({HE_kind})")
    with open(HERE / "refined_scaling.json", "w") as f:
        json.dump(results, f, indent=2)
    return results


if __name__ == "__main__":
    run()
