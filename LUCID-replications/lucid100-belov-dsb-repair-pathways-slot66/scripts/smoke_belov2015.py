#!/usr/bin/env python3
"""
Smoke replication of Belov et al. 2015, J. Theor. Biol. 366:115-130.
DOI 10.1016/j.jtbi.2014.09.024.  Equations and parameters taken verbatim from
the JINR Communication E19-2014-39 preprint (Appendices A, B, C, Tables A.1/A.2).

Implements the full coupled 22-ODE system:
  - NHEJ:   n0, x2, x4, x5, x6, x8, x10, x12, x13, x14   (Eq A.1, 10 equations
              where x14 is the gamma-H2AX foci read-out and x13 the repaired dsDNA)
  - HR:     y2, y3, y5, y7, y8, y10, y11, y12            (Eq B.1, 8 equations)
  - SSA:    z2, z3, z5, z6, z8                            (Eq C.1, 5 equations)
Constant pool levels x1, x3, x7, x9, x11, x15 = x1 = 1 (normalisation).
Constant pool levels y1, y4, y6, y9 = x1 = 1.
Constant pool levels z1, z4, z7      = x1 = 1.

Tau is dimensionless time scaled by 1/K8: t_real_min = tau / K8.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp


# ----------------------------------------------------------------------------
# Table A.1 -- dimensional rate constants  (units: M^-1 min^-1 or min^-1)
# ----------------------------------------------------------------------------
A_L_a = 27.5            # alpha(L) prefactor (Gy^-1 per cell)
A_L_b = 2.43e-3         # alpha(L) LET exponent (keV/mu m)^-1

K1, K_1 = 1.67e-1, 1.10e-2
K2, K_2 = 9.70e3,  8.76e-3
K3       = 3.10e-2
K4, K_4 = 2.30e4,  6.44e-6
K5, K_5 = 2.54e-1, 1.38e-1
K6, K_6 = 3.01e-1, 2.21e-2
K7, K_7 = 4.55e3,  5.34e-2
K8       = 9.20e-3
K9       = 2.77e-3
# K10 depends on Nir:  K10 = 1.93e-7 / Nir M
K11      = 1.25e-3
K12      = 1.85e-1

P1, P_1 = 2.91e1,  2.21e-6
P2       = 9.20e-4
P3, P_3 = 2.00e3,  1.47e-6
P4, P_4 = 3.11e3,  2.58e-5
P5       = 3.56e-1
P6, P_6 = 2.00e2,  4.14e-6
P7       = 8.86e3
P8       = 1.20e-4
P9       = 1.01e-5
P10      = 4.60e-3

Q1, Q_1 = 1.30e2,  2.85e-6
Q2       = 5.00e2
Q3, Q_3 = 1.00e2,  1.01e-5
Q4       = 2.76e-8
Q5, Q_5 = 1.40e3,  7.91e-6
Q6       = 1.93e-1

# Ku total per cell (Appendix A): X1 = N / (NA * Vnucl) = 9.19e-7 M
X1 = 9.19e-7


def dimensionless_params(Nir: float, binding_speedup: float = 1.0) -> dict:
    """Convert dimensional Tables A.1 / A.2 entries into the scaled k, p, q
    constants that appear directly in Eqs A.1, B.1, C.1 (scaling factor K8).

    `binding_speedup` multiplies the bimolecular K1..K7 / P1..P7 / Q1..Q5
    rate constants.  The Table A.1 values as printed yield Ku binding
    pseudo-first-order rates ~1.5e-7 min^-1, but Reynolds et al. 2012 (the
    Ku-binding dataset the paper fits) reports half-times ~15-30 s.  This is
    ~7 orders of magnitude off, most plausibly a units typo in Table A.1.
    Default `binding_speedup=1.0` integrates the system EXACTLY as printed;
    `binding_speedup=1e6` recovers physically realistic NHEJ half-times of
    order minutes to tens of minutes.
    """
    K10 = 1.93e-7 / Nir      # Michaelis constant for gamma-H2AX (Sec 3.5)
    bs = binding_speedup
    return dict(
        # NHEJ
        k1  = bs * K1 * X1 / K8,
        k_1 = K_1 / K8,
        k2  = bs * K2 * X1 / K8,
        k_2 = K_2 / K8,
        k3  = K3 / K8,
        k4  = bs * K4 * X1 / K8,
        k_4 = K_4 / K8,
        k5  = bs * K5 * X1 / K8,
        k_5 = K_5 / K8,
        k6  = bs * K6 * X1 / K8,
        k_6 = K_6 / K8,
        k7  = bs * K7 * X1 / K8,
        k_7 = K_7 / K8,
        k8  = 1.0,
        k9  = K9 / K8,
        k10 = K10 / X1,
        k11 = K11 / K8,
        k12 = K12 / K8,
        # HR
        p1  = bs * P1 * X1 / K8,
        p_1 = P_1 / K8,
        p2  = P2 / K8,
        p3  = bs * P3 * X1 / K8,
        p_3 = P_3 / K8,
        p4  = bs * P4 * X1 / K8,
        p_4 = P_4 / K8,
        p5  = P5 / K8,
        p6  = bs * P6 * X1 / K8,
        p_6 = P_6 / K8,
        p7  = bs * P7 * X1 / K8,
        p8  = P8 / K8,
        p9  = P9 / K8,
        p10 = P10 / K8,
        # SSA
        q1  = bs * Q1 * X1 / K8,
        q_1 = Q_1 / K8,
        q2  = bs * Q2 * X1 / K8,
        q3  = bs * Q3 * X1 / K8,
        q_3 = Q_3 / K8,
        q4  = Q4 / K8,
        q5  = bs * Q5 * X1 / K8,
        q_5 = Q_5 / K8,
        q6  = Q6 / K8,
    )


def alpha_L(L: float) -> float:
    """DSB yield per Gy per cell, alpha(L) = a * exp(-b * L)."""
    return A_L_a * np.exp(-A_L_b * L)


# ---------- state vector ----------------------------------------------------
# Indexing of the integrated state.  Constant pools x1,x3,x7,x9,x11,x15 = 1.
STATE_NAMES = [
    "n0",                                                  # 0
    "x2", "x4", "x5", "x6", "x8", "x10", "x12", "x13", "x14",  # 1..9   NHEJ
    "y2", "y3", "y5", "y7", "y8", "y10", "y11", "y12",     # 10..17 HR
    "z2", "z3", "z5", "z6", "z8",                           # 18..22 SSA
]
NSTATES = len(STATE_NAMES)
IDX = {n: i for i, n in enumerate(STATE_NAMES)}


def rhs(tau: float, s: np.ndarray, par: dict) -> np.ndarray:
    """Right-hand side of the full Belov 2015 system (Eqs A.1, B.1, C.1).

    Note: equation (1) couples dose to n0.  In our smoke setup we deliver an
    instantaneous dose D at tau=0 via the initial condition n0(0) = alpha(L)*D
    (paper: x2..x14, y..., z... = 0).  Therefore dD/dt = 0 for tau > 0 and the
    induction term drops out of the dynamic equation; only the loss terms
    remain.  This matches the paper's Eq A.1 (first line)."""
    n0  = s[IDX["n0"]]
    x2  = s[IDX["x2"]];  x4  = s[IDX["x4"]];  x5  = s[IDX["x5"]]
    x6  = s[IDX["x6"]];  x8  = s[IDX["x8"]];  x10 = s[IDX["x10"]]
    x12 = s[IDX["x12"]]; x13 = s[IDX["x13"]]; x14 = s[IDX["x14"]]
    y2  = s[IDX["y2"]];  y3  = s[IDX["y3"]];  y5  = s[IDX["y5"]]
    y7  = s[IDX["y7"]];  y8  = s[IDX["y8"]];  y10 = s[IDX["y10"]]
    y11 = s[IDX["y11"]]; y12 = s[IDX["y12"]]
    z1  = 1.0;    # constant pool
    z2  = s[IDX["z2"]];  z3  = s[IDX["z3"]];  z5  = s[IDX["z5"]]
    z6  = s[IDX["z6"]];  z8  = s[IDX["z8"]]

    # constant intracellular pools (paper: x1=x3=x7=x9=x11=x15=1; y1=y4=y6=y9=1; z1=z4=z7=1)
    x1 = x3 = x7 = x9 = x11 = x15 = 1.0
    y1 = y4 = y6 = y9 = 1.0
    z4 = z7 = 1.0

    p = par
    dn0_dt = -n0 * (p["k1"] * x1 + p["p1"] * y1) + p["k_1"] * x2 + p["p_1"] * y2

    # ---- NHEJ (Eqs A.1) -----------------------------------------------------
    dx2  = p["k1"]  * n0  * x1 - x2  * (p["k_1"] + p["k2"] * x3) + p["k_2"] * x4
    dx4  = p["k2"]  * x2  * x3 - x4  * (p["k3"] + p["k_2"])
    dx5  = p["k3"]  * x4 - p["k4"] * x5 * x5 + p["k_4"] * x6
    dx6  = p["k4"]  * x5 * x5 - x6 * (p["k_4"] + p["k5"] * x7) + p["k_5"] * x8
    dx8  = p["k_6"] * x10 + p["k5"] * x6 * x7 - x8 * (p["k_5"] + p["k6"] * x9)
    dx10 = p["k_7"] * x12 + p["k6"] * x8 * x9 - x10 * (p["k_6"] + p["k7"] * x11)
    dx12 = p["k7"]  * x10 * x11 - x12 * (p["k8"] + p["k_7"])
    dx13 = p["k8"]  * x12 + p["p10"] * y11 + p["p9"] * y12 + p["q6"] * z8
    sum_nhej = x5 + x6 + x8 + x10 + x12
    dx14 = (p["k9"] * sum_nhej * x15) / (p["k10"] + sum_nhej) \
           - p["k11"] * x13 - p["k12"] * x14

    # ---- HR  (Eqs B.1) ------------------------------------------------------
    dy2  = p["p1"]  * n0  * y1 - y2 * (p["p2"] + p["p_1"])
    dy3  = p["p2"]  * y2 - p["p3"] * y3 * y4 + p["p_3"] * y5
    dy5  = p["p3"]  * y3 * y4 \
           - y5 * (p["p_3"] + p["p4"] * y6 + p["q1"] * z1) \
           + p["p_4"] * y7 + p["q_1"] * z2
    dy7  = p["p4"]  * y5 * y6 - y7 * (p["p5"] + p["p_4"])
    dy8  = p["p_6"] * y10 + p["p5"] * y7 - p["p6"] * y8 * y9
    dy10 = p["p6"]  * y8 * y9 - y10 * (p["p7"] + p["p_6"])
    dy11 = p["p7"]  * y10 - y11 * (p["p8"] + p["p10"])
    dy12 = p["p8"]  * y11 - p["p9"] * y12

    # ---- SSA (Eqs C.1) ------------------------------------------------------
    dz2  = p["q1"]  * y5 * z1 - z2 * (p["q_1"] + p["q2"] * z2)
    dz3  = p["q2"]  * z2 * z2 - p["q3"] * z3 * z4 + p["q_3"] * z5
    dz5  = p["q3"]  * z3 * z4 - z5 * (p["q4"] + p["q_3"])
    dz6  = p["q4"]  * z5 - p["q5"] * z6 * z7 + p["q_5"] * z8
    dz8  = p["q5"]  * z6 * z7 - z8 * (p["q6"] + p["q_5"])

    out = np.zeros(NSTATES)
    out[IDX["n0"]]  = dn0_dt
    out[IDX["x2"]]  = dx2;  out[IDX["x4"]]  = dx4;  out[IDX["x5"]]  = dx5
    out[IDX["x6"]]  = dx6;  out[IDX["x8"]]  = dx8;  out[IDX["x10"]] = dx10
    out[IDX["x12"]] = dx12; out[IDX["x13"]] = dx13; out[IDX["x14"]] = dx14
    out[IDX["y2"]]  = dy2;  out[IDX["y3"]]  = dy3;  out[IDX["y5"]]  = dy5
    out[IDX["y7"]]  = dy7;  out[IDX["y8"]]  = dy8;  out[IDX["y10"]] = dy10
    out[IDX["y11"]] = dy11; out[IDX["y12"]] = dy12
    out[IDX["z2"]]  = dz2;  out[IDX["z3"]]  = dz3;  out[IDX["z5"]]  = dz5
    out[IDX["z6"]]  = dz6;  out[IDX["z8"]]  = dz8
    return out


def run_scenario(name: str, dose_Gy: float, LET_keVum: float, Nir: float,
                  t_max_min: float = 24 * 60,
                  binding_speedup: float = 1.0) -> dict:
    """Integrate the full system for an instantaneous dose at t=0."""
    par = dimensionless_params(Nir, binding_speedup=binding_speedup)
    # Initial condition.  Paper Appendix A states literally  n0(0) = alpha(L) * D
    # (number of induced DSBs per cell, used as the scaled state).  The xi are
    # intermediate-complex counts in the same scaling; constant pools x1,x3,...
    # are normalised to 1 by the Ku reservoir convention.  We follow the paper.
    n0_init = alpha_L(LET_keVum) * dose_Gy
    y0 = np.zeros(NSTATES)
    y0[IDX["n0"]] = n0_init

    # tau = K8 * t_min  =>  t_real_min = tau / K8
    tau_max = K8 * t_max_min
    t_eval_min = np.unique(np.concatenate([
        np.linspace(0.0, 60.0, 121),         # 0 .. 60 min
        np.linspace(60.0, t_max_min, 200),   # 1 h .. 24 h
    ]))
    tau_eval = K8 * t_eval_min

    sol = solve_ivp(rhs, (0.0, tau_max), y0, t_eval=tau_eval,
                     args=(par,), method="LSODA",
                     rtol=1e-8, atol=1e-12, max_step=K8 * 10.0)

    if not sol.success:
        raise RuntimeError(f"solve_ivp failed: {sol.message}")

    n0_t   = sol.y[IDX["n0"]]
    x13_t  = sol.y[IDX["x13"]]
    x14_t  = sol.y[IDX["x14"]]
    y12_t  = sol.y[IDX["y12"]]
    z8_t   = sol.y[IDX["z8"]]
    sum_nhej_t = (sol.y[IDX["x5"]] + sol.y[IDX["x6"]] + sol.y[IDX["x8"]]
                  + sol.y[IDX["x10"]] + sol.y[IDX["x12"]])

    # repair-kinetic half-time on remaining DSBs ( n0 + bridged intermediates )
    remaining = n0_t + sol.y[IDX["x2"]] + sol.y[IDX["x4"]] + sum_nhej_t
    if remaining[0] > 0:
        target = remaining[0] / 2.0
        idx = np.searchsorted(-remaining, -target)
        thalf = float(t_eval_min[min(idx, len(t_eval_min) - 1)])
    else:
        thalf = float("nan")

    return {
        "scenario": name,
        "dose_Gy": dose_Gy,
        "LET_keVum": LET_keVum,
        "Nir": Nir,
        "alpha_L_DSB_per_Gy_per_cell": float(alpha_L(LET_keVum)),
        "binding_speedup": binding_speedup,
        "n0_initial_normalised": float(n0_init),
        "n0_at_24h_normalised": float(n0_t[-1]),
        "x13_repaired_dsDNA_at_24h": float(x13_t[-1]),
        "x14_gammaH2AX_peak": float(np.max(x14_t)),
        "x14_gammaH2AX_t_peak_min": float(t_eval_min[int(np.argmax(x14_t))]),
        "x14_gammaH2AX_at_24h": float(x14_t[-1]),
        "y12_HR_dHJ_at_24h": float(y12_t[-1]),
        "z8_SSA_at_24h": float(z8_t[-1]),
        "residual_DSB_fraction_24h": float(n0_t[-1] / n0_init) if n0_init > 0 else float("nan"),
        "DSB_half_time_min": thalf,
        # traces (subsampled for JSON compactness)
        "t_min": t_eval_min[::5].tolist(),
        "n0_trace": n0_t[::5].tolist(),
        "x14_trace": x14_t[::5].tolist(),
        "x13_trace": x13_t[::5].tolist(),
    }


def main(out_root: Path) -> None:
    results_dir = out_root / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    scenarios = [
        # (label,                 dose_Gy, LET keV/um, Nir)
        ("low-LET gamma 1Gy wt",   1.0,   0.2,  0.01),   # Asaithamby '08 baseline
        ("X-ray 1Gy DNA-PKcs-",    1.0,   0.2,  0.43),   # NHEJ defective (Rothkamm '03)
        ("X-ray 1Gy LigIV-",       1.0,   0.2,  0.20),   # NHEJ-late defective (Okayasu '12)
        ("X-ray 1Gy BRCA2-",       1.0,   0.2,  0.33),   # HR defective (Shibata '11)
        ("Fe 1GeV/u 1Gy wt",       1.0,   150.0, 0.30),  # high-LET (Asaithamby '08)
        ("Fe 1GeV/u 1Gy 236keV/um",1.0,   236.0, 0.40),  # highest-LET tabulated
    ]

    runs = []
    for s in scenarios:
        for bs in (1.0, 1.0e6):
            label = f"{s[0]} [bs={bs:.0e}]"
            runs.append(run_scenario(label, s[1], s[2], s[3], binding_speedup=bs))

    # Optional plot
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, axs = plt.subplots(2, 2, figsize=(13, 9))
        for r in runs:
            col = 0 if r["binding_speedup"] < 10 else 1
            short = r["scenario"].split(" [bs")[0]
            axs[0, col].plot(r["t_min"], r["n0_trace"], label=short)
            axs[1, col].plot(r["t_min"], r["x14_trace"], label=short)
        for col, title in enumerate(["as published (Table A.1 verbatim)",
                                       "binding_speedup = 1e6"]):
            axs[0, col].set_xscale("log");   axs[0, col].set_xlim(0.5, 24 * 60)
            axs[0, col].set_xlabel("time (min)")
            axs[0, col].set_ylabel("n0 (scaled remaining DSBs)")
            axs[0, col].set_title(f"DSB clearance -- {title}")
            axs[0, col].legend(fontsize=7)
            axs[1, col].set_xscale("log");   axs[1, col].set_xlim(0.5, 24 * 60)
            axs[1, col].set_xlabel("time (min)")
            axs[1, col].set_ylabel("x14 (scaled gamma-H2AX foci)")
            axs[1, col].set_title(f"gamma-H2AX -- {title}")
            axs[1, col].legend(fontsize=7)
        plt.tight_layout()
        fig.savefig(results_dir / "smoke_traces.png", dpi=120)
        plot_ok = True
    except Exception as exc:        # noqa: BLE001
        plot_ok = False
        plot_err = str(exc)

    out = {
        "paper": "Belov et al. 2015, JTB 366:115-130, DOI 10.1016/j.jtbi.2014.09.024",
        "source_used": "JINR preprint E19-2014-39 (open access via INIS/IAEA)",
        "model": "22-coupled-ODE NHEJ + HR + SSA + gamma-H2AX, verbatim Eqs A.1/B.1/C.1",
        "integrator": "scipy.integrate.solve_ivp LSODA rtol=1e-8 atol=1e-12",
        "X1_Ku_total_M": X1,
        "scenarios": runs,
        "plot_written": plot_ok,
    }
    if not plot_ok:
        out["plot_error"] = plot_err

    with open(results_dir / "smoke_results.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print(f"WROTE  {results_dir / 'smoke_results.json'}")
    if plot_ok:
        print(f"WROTE  {results_dir / 'smoke_traces.png'}")

    # Console summary
    print("\nScenario summary:")
    for r in runs:
        print(f"  {r['scenario']:32s}  alpha(L)={r['alpha_L_DSB_per_Gy_per_cell']:5.1f}  "
              f"t1/2={r['DSB_half_time_min']:6.1f} min  "
              f"residual24h={r['residual_DSB_fraction_24h']:.3f}  "
              f"H2AX_peak={r['x14_gammaH2AX_peak']:.3e} @ {r['x14_gammaH2AX_t_peak_min']:.1f} min")


if __name__ == "__main__":
    main(Path(__file__).resolve().parent.parent)
