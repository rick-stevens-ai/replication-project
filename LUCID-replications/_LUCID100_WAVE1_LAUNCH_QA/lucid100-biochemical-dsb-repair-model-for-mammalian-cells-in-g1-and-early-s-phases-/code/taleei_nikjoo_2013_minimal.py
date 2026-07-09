"""
Minimal compartmental ODE reimplementation of Taleei & Nikjoo (2013):
"Biochemical DSB-repair model for mammalian cells in G1 and early S phases
of the cell cycle", Mutation Research/Genetic Toxicology and Environmental
Mutagenesis 756(1-2): 206-212.   doi:10.1016/j.mrgentox.2013.06.004

PMID 23792210. Paper is CLOSED ACCESS (verified via Unpaywall + S2).

------------------------------------------------------------------------------
SCOPE / DISCLAIMER
------------------------------------------------------------------------------

This is a FIRST-PASS, MINIMAL REIMPLEMENTATION built from:

    (a) the published abstract (PubMed 23792210),
    (b) the model description echoed in the companion Taleei & Nikjoo papers
        (Radiat Res 179, 540-548, 2013; Radiat Res 179, 530-539, 2013;
         Int J Radiat Biol 88, 948-953, 2012; RPD 143, 154-160, 2011 - SSA),
        all of which restate the law-of-mass-action ODE formalism and the
        NHEJ pathway used here,
    (c) the parameter set reused (with the same physical interpretation) in
        the openly-available Qi et al. (2021) Cancers 13:2202 Table 1
        (`lucid-slow-fast-nhej/code/nhej_model.py` in this repo), which is a
        documented spatial extension of the same Taleei/Nikjoo NHEJ skeleton,
    (d) the public DaMaRiS pathway listings (`lucid-slow-fast-nhej/artifacts
        /damaris/pathwayNHEJ.txt`) which preserve the same per-step
        transition times.

It is NOT a digit-perfect reproduction of the paper's Figures 2-5 -- we have
not seen the paper PDF, so absolute values cannot be claim-by-claim
checked.  The intent is:

    *  reproduce the QUALITATIVE biphasic repair kinetics (fast c-NHEJ +
       slow MMEJ/processed branch) for simple vs complex DSBs in G1/early-S
       described in the abstract,
    *  expose the model rate constants and pathway topology in a single
       small Python file for downstream LUCID work and parameter scans,
    *  serve as a smoke test that the artifact harvest pipeline produces
       runnable code with sensible numerical output.

We DO NOT model: chromatin (heterochromatin processing penalty), LET-
dependent damage spectra, HR (paper restricts to G1/early-S where HR is
suppressed), or the explicit microhomology-search step inside MMEJ (folded
into an effective slow ligation time).

------------------------------------------------------------------------------
PATHWAY TOPOLOGY (Taleei-Nikjoo 2013, abstract)
------------------------------------------------------------------------------

           +-- simple DSB (~50%) --> Ku --> DNA-PKcs --> ligation       (c-NHEJ)
DSB pool --|
           +-- complex DSB (~50%) --> Ku --> processing --+
                                                          |
                                                          +-> NHEJ (slow)
                                                          +-> MMEJ (resection
                                                              -dependent, slow)

The model resolves each DSB to one of:

    REP_FAST   repaired via direct c-NHEJ (simple DSB, k_fast)
    REP_SLOW   repaired via processed NHEJ (complex DSB, k_slow_NHEJ)
    REP_MMEJ   repaired via MMEJ (complex DSB, k_MMEJ)
    UNREP     still unrepaired at time t

Probability a complex DSB resolves through MMEJ vs slow NHEJ is `p_mmej`
(default 0.10, consistent with published in-vivo NHEJ:MMEJ partition in
G1 cells).  Per-step mean transition times (s) below.

------------------------------------------------------------------------------
"""

from __future__ import annotations

import json
import math
import os
import sys
from dataclasses import dataclass, asdict

import numpy as np
from scipy.integrate import solve_ivp


# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------

@dataclass
class TaleeiNikjoo2013Params:
    # ---- DSB partition ----
    f_complex: float = 0.50         # fraction of induced DSBs that are "complex"
    # ---- Per-pathway mean times (seconds) ----
    tau_ku:           float = 1.1   # Ku70/80 recruitment
    tau_dnapk_fast:   float = 1.2   # DNA-PKcs recruitment (simple)
    tau_lig_fast:     float = 1200. # final ligation, c-NHEJ           ~ 20 min
    tau_process:      float = 500.  # end-processing for complex DSBs  ~  8 min
    tau_lig_slow:     float = 5400. # slow NHEJ ligation (Artemis-Lig4)~ 90 min
    tau_mmej:         float = 7200. # MMEJ resection + microhomology + Lig3 ~ 2 h
    p_mmej:           float = 0.10  # complex-DSB branching to MMEJ
    # ---- Damage input ----
    dsb_per_Gy:       float = 35.   # mammalian G1 DSB yield, photons (Nikjoo)
    # ---- Deficiency switches (qualitative-only) ----
    artemis_def: bool = False       # blocks slow NHEJ branch
    ligase4_def: bool = False       # blocks both NHEJ ligations
    ligase3_def: bool = False       # blocks MMEJ ligation


STATES = [
    "S_dsb",      # simple DSB awaiting Ku
    "C_dsb",      # complex DSB awaiting Ku
    "S_ku",       # simple, Ku-bound, awaiting DNA-PKcs / ligation
    "C_ku",       # complex, Ku-bound, processing
    "C_proc",     # complex, processed, committed to NHEJ branch
    "C_mmej",     # complex, resected, committed to MMEJ branch
    "REP_FAST",   # repaired by c-NHEJ
    "REP_SLOW",   # repaired by slow NHEJ
    "REP_MMEJ",   # repaired by MMEJ
]
IDX = {n: i for i, n in enumerate(STATES)}
N = len(STATES)


def rates(p: TaleeiNikjoo2013Params) -> dict:
    """Convert mean times -> first-order rate constants (1/s)."""
    k = {
        "k_ku":          1.0 / p.tau_ku,
        "k_fast_lig":    0.0 if p.ligase4_def else 1.0 / p.tau_lig_fast,
        "k_process":     1.0 / p.tau_process,
        "k_slow_lig":    0.0 if (p.artemis_def or p.ligase4_def) else 1.0 / p.tau_lig_slow,
        "k_mmej_lig":    0.0 if p.ligase3_def else 1.0 / p.tau_mmej,
    }
    return k


def derivs(t, y, p):
    k = rates(p)
    (S_dsb, C_dsb, S_ku, C_ku, C_proc, C_mmej,
     REP_FAST, REP_SLOW, REP_MMEJ) = y

    # ---- transitions ----
    # 1. DSB -> Ku  (both simple and complex)
    j_S_ku = k["k_ku"] * S_dsb
    j_C_ku = k["k_ku"] * C_dsb

    # 2. simple Ku -> repaired (c-NHEJ direct ligation)
    j_S_lig = k["k_fast_lig"] * S_ku

    # 3. complex Ku -> processed (split between slow-NHEJ and MMEJ branches)
    j_C_split = k["k_process"] * C_ku
    j_C_to_proc = (1.0 - p.p_mmej) * j_C_split
    j_C_to_mmej = p.p_mmej * j_C_split

    # 4. complex processed -> slow-NHEJ ligated
    j_C_slow_lig = k["k_slow_lig"] * C_proc

    # 5. complex resected -> MMEJ ligated
    j_C_mmej_lig = k["k_mmej_lig"] * C_mmej

    d = np.zeros(N)
    d[IDX["S_dsb"]]   = -j_S_ku
    d[IDX["C_dsb"]]   = -j_C_ku
    d[IDX["S_ku"]]    = +j_S_ku - j_S_lig
    d[IDX["C_ku"]]    = +j_C_ku - j_C_split
    d[IDX["C_proc"]]  = +j_C_to_proc - j_C_slow_lig
    d[IDX["C_mmej"]]  = +j_C_to_mmej - j_C_mmej_lig
    d[IDX["REP_FAST"]] = +j_S_lig
    d[IDX["REP_SLOW"]] = +j_C_slow_lig
    d[IDX["REP_MMEJ"]] = +j_C_mmej_lig
    return d


# ---------------------------------------------------------------------------
# Simulation API
# ---------------------------------------------------------------------------

def simulate(t_hours, dose_Gy=2.0, params=None):
    """Solve the Taleei-Nikjoo (2013) ODE on a t_hours grid (numpy array).

    Returns dict with normalised state fractions plus absolute counts.
    """
    p = params or TaleeiNikjoo2013Params()
    t_s = np.asarray(t_hours, dtype=float) * 3600.0
    N0 = p.dsb_per_Gy * dose_Gy

    y0 = np.zeros(N)
    y0[IDX["S_dsb"]] = (1.0 - p.f_complex)
    y0[IDX["C_dsb"]] = p.f_complex

    sol = solve_ivp(
        derivs, (t_s[0], t_s[-1]), y0, t_eval=t_s,
        args=(p,), method="LSODA", rtol=1e-9, atol=1e-12, max_step=30.0,
    )
    if not sol.success:
        raise RuntimeError(f"LSODA failed: {sol.message}")

    out = {n: sol.y[i] for i, n in enumerate(STATES)}
    out["t_hours"] = np.asarray(t_hours, dtype=float)
    out["unrep_frac"] = 1.0 - (out["REP_FAST"] + out["REP_SLOW"] + out["REP_MMEJ"])
    out["unrep_count"] = out["unrep_frac"] * N0
    out["N0"] = N0
    out["params"] = asdict(p)
    return out


# ---------------------------------------------------------------------------
# Smoke-test driver
# ---------------------------------------------------------------------------

def smoke():
    """Print a small results table and a JSON summary for QA."""
    t = np.geomspace(0.001, 24.0, 200)  # 3.6 s ... 24 h, log spaced
    # Insert t=0 manually for tidy initial-state plot
    t = np.r_[0.0, t]

    summary = {
        "paper": "Taleei & Nikjoo 2013, Mutat Res Genet Tox Environ Mutagen 756:206-212",
        "doi": "10.1016/j.mrgentox.2013.06.004",
        "pmid": 23792210,
        "model": "minimal compartmental ODE (8 states, NHEJ+MMEJ G1/early-S)",
        "runs": [],
    }

    for label, kw in [
        ("WT 2 Gy",        dict()),
        ("WT 0.5 Gy",      dict()),
        ("WT 4 Gy",        dict()),
        ("Artemis-def",    dict(artemis_def=True)),
        ("Ligase4-def",    dict(ligase4_def=True)),
        ("Ligase3-def",    dict(ligase3_def=True)),
        ("high complex",   dict(f_complex=0.80)),
    ]:
        p = TaleeiNikjoo2013Params(**kw)
        dose = kw.get("dose", 2.0) if "dose" in kw else (
            0.5 if "0.5" in label else 4.0 if "4 Gy" in label else 2.0)
        r = simulate(t, dose_Gy=dose, params=p)
        snapshot = {}
        for h in [0.25, 1.0, 6.0, 24.0]:
            idx = int(np.argmin(np.abs(t - h)))
            snapshot[f"t={h}h"] = {
                "unrep_frac": float(r["unrep_frac"][idx]),
                "unrep_count": float(r["unrep_count"][idx]),
                "REP_FAST_frac": float(r["REP_FAST"][idx]),
                "REP_SLOW_frac": float(r["REP_SLOW"][idx]),
                "REP_MMEJ_frac": float(r["REP_MMEJ"][idx]),
            }
        summary["runs"].append({
            "label": label, "dose_Gy": dose,
            "params": asdict(p), "snapshots": snapshot,
        })

    # ---- print tabular summary ----
    print(f"\n{'='*78}")
    print(f"Taleei & Nikjoo (2013) minimal ODE -- smoke test")
    print(f"{'='*78}\n")
    print(f"{'run':<18} {'dose':>5} {'t (h)':>6} {'unrep%':>8} {'unrep#':>8} "
          f"{'fast%':>6} {'slow%':>6} {'mmej%':>6}")
    print("-" * 78)
    for run in summary["runs"]:
        for tlabel, snap in run["snapshots"].items():
            print(f"{run['label']:<18} {run['dose_Gy']:>5.1f} {tlabel:>6} "
                  f"{100*snap['unrep_frac']:>7.2f}% "
                  f"{snap['unrep_count']:>7.2f}  "
                  f"{100*snap['REP_FAST_frac']:>5.1f}% "
                  f"{100*snap['REP_SLOW_frac']:>5.1f}% "
                  f"{100*snap['REP_MMEJ_frac']:>5.1f}%")
        print()
    return summary


if __name__ == "__main__":
    out_dir = os.environ.get(
        "TN2013_OUT",
        os.path.join(os.path.dirname(__file__), "..", "results"),
    )
    os.makedirs(out_dir, exist_ok=True)

    summary = smoke()

    out_path = os.path.join(out_dir, "smoke_summary.json")
    with open(out_path, "w") as fh:
        json.dump(summary, fh, indent=2)
    print(f"Wrote {out_path}")

    # Plot if matplotlib available
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        t = np.geomspace(0.001, 24.0, 400)
        t = np.r_[0.0, t]
        fig, axes = plt.subplots(1, 2, figsize=(11, 4.4))

        # Panel 1: WT repair kinetics (decomposition)
        r = simulate(t, dose_Gy=2.0, params=TaleeiNikjoo2013Params())
        axes[0].plot(t, 100 * r["unrep_frac"], "k-", lw=2, label="unrepaired")
        axes[0].plot(t, 100 * r["REP_FAST"], "C0--", label="c-NHEJ (fast)")
        axes[0].plot(t, 100 * r["REP_SLOW"], "C1--", label="slow NHEJ")
        axes[0].plot(t, 100 * r["REP_MMEJ"], "C3--", label="MMEJ")
        axes[0].set_xscale("symlog", linthresh=0.05)
        axes[0].set_xlabel("Time after irradiation (h)")
        axes[0].set_ylabel("Fraction of induced DSBs (%)")
        axes[0].set_title("WT G1/early-S, 2 Gy photons (Taleei-Nikjoo 2013)")
        axes[0].grid(alpha=0.3); axes[0].legend(loc="best", fontsize=8)

        # Panel 2: WT vs deficiencies (unrepaired only)
        for label, p in [
            ("WT",            TaleeiNikjoo2013Params()),
            ("Artemis-def",   TaleeiNikjoo2013Params(artemis_def=True)),
            ("Ligase4-def",   TaleeiNikjoo2013Params(ligase4_def=True)),
            ("Ligase3-def",   TaleeiNikjoo2013Params(ligase3_def=True)),
        ]:
            r = simulate(t, dose_Gy=2.0, params=p)
            axes[1].plot(t, 100 * r["unrep_frac"], label=label, lw=1.6)
        axes[1].set_xscale("symlog", linthresh=0.05)
        axes[1].set_xlabel("Time after irradiation (h)")
        axes[1].set_ylabel("Unrepaired DSBs (%)")
        axes[1].set_title("Genetic deficiencies vs WT")
        axes[1].grid(alpha=0.3); axes[1].legend(loc="best", fontsize=8)

        fig.tight_layout()
        fig_path = os.path.join(out_dir, "..", "figures", "fig_smoke_kinetics.png")
        os.makedirs(os.path.dirname(fig_path), exist_ok=True)
        fig.savefig(fig_path, dpi=130)
        print(f"Wrote {fig_path}")
    except Exception as e:
        print(f"matplotlib plot skipped: {e}", file=sys.stderr)
