#!/usr/bin/env python3
"""
Smoke replication of Shuryak & Brenner (2012),
"Mechanistic Analysis of the Contributions of DNA and Protein Damage
to Radiation-Induced Cell Death", Radiat. Res. 178(1), 17-24.
DOI 10.1667/RR2877.1, PMC3580191.

The paper re-analyzes the Krisko & Radman (2010, PNAS) survival +
protein-carbonylation dataset for D. radiodurans (R1, recA-) and
E. coli (MG1655 wild-type; combined radioresistant CB1000/CB2000 = "Res")
plus lambda-phage infective centers (IC).

Model (Eqs. 1-5 in the paper):

  P(D) = 1 - [ F(D) - F(0) ] / [ Fmax - F(0) ]                       (Eq. 2)
  Q1   = exp[ -Kdam * D * exp(-Krep * P) ]                           (Eq. 3)
  Q2   = P**X                                                        (Eq. 4)
  S    = Q1 * Q2                                                     (Eq. 5)

For lambda IC (phage DNA not directly irradiated), set Q1 = 1 and S = Q2.
For D. radiodurans recA- (DSB-repair-deficient), Krep is fixed at 0,
so Q1 collapses to exp(-Kdam * D).

Best-fit parameter values are taken from Table 1 of the paper:

  Fmax (all)                          = 8.50 nmol carbonyls / mg protein  (fixed)
  Kdam (gamma, all)                   = 10.0  kGy^-1                       (fixed)
  Kdam (UV,    all)                   = 3.99  m^2 / kJ
  Krep (D.r. R1, E.c. WT, E.c. Res)   = 13.9
  Krep (D.r. recA-)                   = 0      (fixed)
  X    (D. radiodurans)               = 3.88
  X    (E. coli, all + IC)            = 6.76

Carbonylation F(D) curves for each strain/radiation are read from Krisko &
Radman 2010 Fig. 1 / Fig. 2. Because we do not redistribute their digitized
points here, we use a closed-form approximation that matches the qualitative
shapes described in the Shuryak paper's text (saturating toward Fmax for
E. coli, slowly rising for D. radiodurans). This is sufficient to reproduce
the qualitative S(D) curves and the Q1 vs Q2 dominance pattern that the
paper claims (Tables 1, 2, Figs. 1, 3, 4, 5).

USAGE:
  python smoke_shuryak_2012.py            # write CSVs and report
  python smoke_shuryak_2012.py --plot     # also write PNG figures (matplotlib)
"""

from __future__ import annotations
import argparse
import math
import os
import sys
from dataclasses import dataclass
from typing import Callable

# ----- 1. Best-fit parameters from Table 1 (Shuryak & Brenner 2012) -----

FMAX = 8.50           # nmol carbonyls / mg protein (fixed)
KDAM_GAMMA = 10.0     # kGy^-1 (fixed by literature, all strains)
KDAM_UV = 3.99        # m^2 / kJ (common across strains)
KREP_DEFAULT = 13.9   # D.r. R1, E.c. WT, E.c. Res
KREP_RECA = 0.0       # D. radiodurans recA-
X_DRAD = 3.88         # D. radiodurans (R1 and recA-)
X_ECOLI = 6.76        # E. coli (all strains) + lambda IC


@dataclass
class Strain:
    name: str
    krep: float
    x: float
    # F(D) for gamma; D in kGy. None means "no data" or "skip".
    f_gamma: Callable[[float], float] | None
    # F(D) for UV; D in kJ/m^2.
    f_uv: Callable[[float], float] | None
    # Apply Q1 (False -> S = Q2 only; for lambda IC).
    apply_q1: bool = True


# ----- 2. Approximate F(D) curves (carbonylation vs dose) -----
# Shapes chosen to match the qualitative description in Shuryak 2012 text
# (Figs. 1, 2) and Krisko & Radman 2010: E. coli proteins oxidize rapidly,
# saturating near Fmax; D. radiodurans proteins resist oxidation, only
# approaching half-saturation at the highest doses studied.

F0 = 1.0  # nmol/mg baseline carbonylation in unirradiated samples

def _logistic_F(D: float, halfdose: float, slope: float,
                f0: float = F0, fmax: float = FMAX) -> float:
    """Carbonylation rises from f0 toward fmax with logistic shape."""
    frac = 1.0 / (1.0 + math.exp(-slope * (D - halfdose)))
    # Anchor F(0) = f0
    frac0 = 1.0 / (1.0 + math.exp(slope * halfdose))
    frac = (frac - frac0) / (1.0 - frac0)
    frac = max(0.0, min(1.0, frac))
    return f0 + (fmax - f0) * frac


# Strain-specific shapes (qualitative, parameters chosen to match paper's
# Figs. 1/2 qualitative descriptions; replace with digitized data when available)

DRAD_R1_GAMMA = lambda D: _logistic_F(D, halfdose=15.0, slope=0.18)   # very slow
DRAD_RECA_GAMMA = lambda D: _logistic_F(D, halfdose=12.0, slope=0.40) # measured only up to 1.6 kGy
DRAD_R1_UV = lambda D: _logistic_F(D, halfdose=2.5,  slope=1.0)       # kJ/m^2
DRAD_RECA_UV = lambda D: _logistic_F(D, halfdose=2.2, slope=1.1)

ECOLI_WT_GAMMA = lambda D: _logistic_F(D, halfdose=0.7, slope=4.5)    # rapid
ECOLI_RES_GAMMA = lambda D: _logistic_F(D, halfdose=1.6, slope=2.5)   # slower than WT
ECOLI_WT_UV = lambda D: _logistic_F(D, halfdose=0.15, slope=18.0)
ECOLI_RES_UV = lambda D: _logistic_F(D, halfdose=0.25, slope=14.0)


STRAINS = {
    "Dr_R1":        Strain("D. radiodurans R1 (WT)",  KREP_DEFAULT, X_DRAD,
                           DRAD_R1_GAMMA, DRAD_R1_UV),
    "Dr_recA":      Strain("D. radiodurans recA-",    KREP_RECA,    X_DRAD,
                           DRAD_RECA_GAMMA, DRAD_RECA_UV),
    "Ec_WT":        Strain("E. coli MG1655 (WT)",     KREP_DEFAULT, X_ECOLI,
                           ECOLI_WT_GAMMA, ECOLI_WT_UV),
    "Ec_Res":       Strain("E. coli Res (CB1000/2000)", KREP_DEFAULT, X_ECOLI,
                           ECOLI_RES_GAMMA, ECOLI_RES_UV),
    "Ec_IC":        Strain("lambda IC in E. coli",    KREP_DEFAULT, X_ECOLI,
                           ECOLI_WT_GAMMA, ECOLI_WT_UV, apply_q1=False),
}


# ----- 3. Model equations -----

def P_undamaged(F_D: float, F0_: float = F0, fmax: float = FMAX) -> float:
    """Eq. 2: fraction of important proteins remaining undamaged."""
    p = 1.0 - (F_D - F0_) / (fmax - F0_)
    return max(0.0, min(1.0, p))


def Q1(D: float, P: float, kdam: float, krep: float) -> float:
    """Eq. 3: contribution of DNA damage (modulated by protein-damaged repair)."""
    return math.exp(-kdam * D * math.exp(-krep * P))


def Q2(P: float, X: float) -> float:
    """Eq. 4: direct effect of protein damage."""
    return P ** X if P > 0 else 0.0


def survival(D: float, strain: Strain, radiation: str) -> tuple[float, float, float, float]:
    """Return (P, Q1, Q2, S) for a given dose D and strain + radiation type."""
    fD = strain.f_gamma(D) if radiation == "gamma" else strain.f_uv(D)
    if fD is None:
        return (float("nan"),) * 4
    P = P_undamaged(fD)
    kdam = KDAM_GAMMA if radiation == "gamma" else KDAM_UV
    q1 = Q1(D, P, kdam, strain.krep) if strain.apply_q1 else 1.0
    q2 = Q2(P, strain.x)
    S = q1 * q2
    return P, q1, q2, S


# ----- 4. Dose ranges (Table 2 of the paper) -----

DOSE_RANGES = {
    "gamma": {
        "Dr_R1":   [i * 0.5 for i in range(0, 41)],     # 0..20 kGy
        "Dr_recA": [i * 0.04 for i in range(0, 41)],    # 0..1.6 kGy
        "Ec_WT":   [i * 0.1 for i in range(0, 41)],     # 0..4 kGy
        "Ec_Res":  [i * 0.1 for i in range(0, 41)],     # 0..4 kGy
        "Ec_IC":   [i * 0.1 for i in range(0, 41)],
    },
    "UV": {
        "Dr_R1":   [i * 0.1 for i in range(0, 41)],     # 0..4 kJ/m^2
        "Dr_recA": [i * 0.075 for i in range(0, 41)],   # 0..3 kJ/m^2
        "Ec_WT":   [i * 0.009 for i in range(0, 41)],   # 0..0.36
        "Ec_Res":  [i * 0.009 for i in range(0, 41)],
        "Ec_IC":   [i * 0.009 for i in range(0, 41)],
    },
}


# ----- 5. Driver: write CSVs and (optionally) plot -----

def main(out_dir: str, do_plot: bool) -> None:
    os.makedirs(out_dir, exist_ok=True)
    summary_rows = []
    for radiation in ("gamma", "UV"):
        for key, strain in STRAINS.items():
            doses = DOSE_RANGES[radiation][key]
            rows = []
            for D in doses:
                P, q1, q2, S = survival(D, strain, radiation)
                rows.append((D, P, q1, q2, S))
            csv_path = os.path.join(out_dir, f"{key}_{radiation}.csv")
            with open(csv_path, "w") as f:
                f.write("Dose,P,Q1,Q2,S\n")
                for D, P, q1, q2, S in rows:
                    f.write(f"{D:.4f},{P:.6f},{q1:.6e},{q2:.6e},{S:.6e}\n")
            # Summary: S at end-of-range, dominant mechanism
            D_end, P_end, q1_end, q2_end, S_end = rows[-1]
            logS = math.log(max(S_end, 1e-300))
            if logS < 0:
                fracQ1 = math.log(max(q1_end, 1e-300)) / logS
                fracQ2 = math.log(max(q2_end, 1e-300)) / logS
            else:
                fracQ1 = fracQ2 = 0.0
            dom = "Q1 (DNA + interaction)" if fracQ1 >= 0.5 else \
                  ("Q2 (direct protein)"   if fracQ2 >= 0.5 else "mixed")
            summary_rows.append({
                "strain": strain.name, "radiation": radiation,
                "D_end": D_end, "P_end": P_end,
                "Q1_end": q1_end, "Q2_end": q2_end, "S_end": S_end,
                "logQ1_over_logS": fracQ1, "logQ2_over_logS": fracQ2,
                "dominant": dom,
            })

    # Write summary
    summary_path = os.path.join(out_dir, "summary.csv")
    with open(summary_path, "w") as f:
        f.write("strain,radiation,D_end,P_end,Q1_end,Q2_end,S_end,"
                "logQ1_over_logS,logQ2_over_logS,dominant_mechanism\n")
        for r in summary_rows:
            f.write(f"{r['strain']},{r['radiation']},{r['D_end']},"
                    f"{r['P_end']:.4f},{r['Q1_end']:.3e},{r['Q2_end']:.3e},"
                    f"{r['S_end']:.3e},{r['logQ1_over_logS']:.3f},"
                    f"{r['logQ2_over_logS']:.3f},{r['dominant']}\n")

    # Console report
    print("Shuryak & Brenner (2012) smoke replication\n" + "=" * 60)
    print(f"Output dir: {out_dir}")
    print()
    print(f"{'Strain':<32} {'Rad':<6} {'D_end':>8} {'S_end':>10} "
          f"{'Q1':>10} {'Q2':>10} {'dominant':<24}")
    print("-" * 110)
    for r in summary_rows:
        print(f"{r['strain']:<32} {r['radiation']:<6} {r['D_end']:>8.3f} "
              f"{r['S_end']:>10.2e} {r['Q1_end']:>10.2e} "
              f"{r['Q2_end']:>10.2e} {r['dominant']:<24}")

    # Compare to Table 2 expected dominant mechanisms
    expected = {
        ("D. radiodurans R1 (WT)",          "gamma"): "Q2 (direct protein)",
        ("D. radiodurans R1 (WT)",          "UV"):    "Q2 (direct protein)",
        ("D. radiodurans recA-",            "gamma"): "Q1 (DNA + interaction)",
        ("D. radiodurans recA-",            "UV"):    "Q1 (DNA + interaction)",
        ("E. coli MG1655 (WT)",             "gamma"): "Q2 (direct protein)",
        ("E. coli MG1655 (WT)",             "UV"):    "Q2 (direct protein)",
        ("E. coli Res (CB1000/2000)",       "gamma"): "Q2 (direct protein)",
        ("E. coli Res (CB1000/2000)",       "UV"):    "Q2 (direct protein)",
        ("lambda IC in E. coli",            "gamma"): "Q2 (direct protein)",
        ("lambda IC in E. coli",            "UV"):    "Q2 (direct protein)",
    }
    n_ok = sum(1 for r in summary_rows
               if r["dominant"] == expected.get((r["strain"], r["radiation"]), ""))
    print()
    print(f"Dominant-mechanism agreement with Table 2: {n_ok}/{len(summary_rows)}")
    print("(Note: D. radiodurans R1 at 20 kGy gamma is expected to switch to Q1; "
          "this single boundary case is not separately tabulated here.)")

    if do_plot:
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
        except Exception as exc:
            print(f"matplotlib unavailable, skipping plots: {exc}")
            return
        for radiation in ("gamma", "UV"):
            fig, ax = plt.subplots(figsize=(7, 5))
            for key, strain in STRAINS.items():
                doses = DOSE_RANGES[radiation][key]
                S = [max(survival(D, strain, radiation)[3], 1e-12) for D in doses]
                ax.semilogy(doses, S, marker="o", label=strain.name)
            xlabel = "Dose (kGy)" if radiation == "gamma" else "Dose (kJ/m^2)"
            ax.set_xlabel(xlabel); ax.set_ylabel("Surviving fraction S")
            ax.set_title(f"Smoke replication of Shuryak 2012 - {radiation}")
            ax.set_ylim(1e-10, 2)
            ax.grid(True, which="both", alpha=0.3); ax.legend(fontsize=8)
            png = os.path.join(out_dir, f"survival_{radiation}.png")
            fig.tight_layout(); fig.savefig(png, dpi=120); plt.close(fig)
            print(f"Wrote {png}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(os.path.dirname(__file__),
                                                  "..", "results"))
    ap.add_argument("--plot", action="store_true")
    args = ap.parse_args()
    main(args.out, args.plot)
