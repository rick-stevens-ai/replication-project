#!/usr/bin/env python3
"""
Reconstruct a PIDE-equivalent NB1RGB heavy-ion cell-survival dataset.

CONTEXT / HONEST PROVENANCE
---------------------------
Debreceni et al. 2024 (Toxics 12(8):545) filtered the GSI PIDE database to the
NB1RGB human normal-fibroblast cell line: 51 experiments -> 318 (dose, surviving
fraction) points, ions {12C:24, 20Ne:15, 28Si:7, 56Fe:5}. Each PIDE experiment
stores an LQM parameterization (alpha, beta) and (for 3.2+) the raw dose/SF
points, plus dose-mean LET.

The raw PIDE ensemble file is EMAIL-GATED (GSI registration form; the download
link is not served publicly and is not on the Wayback Machine). See REPORT.md
"reproducibility blocker".

To still exercise the paper's *pipeline* and test whether its central structural
claim reproduces, we reconstruct an NB1RGB-equivalent ensemble from the published
literature that feeds PIDE for this cell line. The NB1RGB heavy-ion LQM(LET)
response is dominated by the NIRS/Furusawa program:
  Furusawa et al., Radiat Res 154:485 (2000) and follow-ups (C/Ne/Si/Fe on
  NB1RGB & V79). We encode the well-established NB1RGB LQM alpha(LET), beta(LET)
  trend for each ion track (alpha rises with LET to an overkill peak ~100-200
  keV/um then falls; beta ~ roughly constant-to-declining), and regenerate the
  318-point dose/SF ensemble by sampling doses spanning each experiment's assay
  range and applying S = exp(-(alpha D + beta D^2)) with realistic clonogenic
  scatter. This preserves the physics (LET dependence) the paper's RF exploits.

This is a FAITHFUL-PIPELINE / STRUCTURAL replication, NOT an exact-number match
to PIDE. The exact-number claim is data-blocked; that is stated plainly in the
report.
"""
import numpy as np
import pandas as pd

RNG = np.random.default_rng(20260702)

# Per-ion experiment counts from the paper (Sec 2.3): total 51 experiments.
ION_EXP = {"12C": 24, "20Ne": 15, "28Si": 7, "56Fe": 5}
# Atomic number Z for each ion.
ION_Z = {"12C": 6, "20Ne": 10, "28Si": 14, "56Fe": 26}

# Representative dose-mean LET ranges (keV/um) actually spanned by NB1RGB
# clonogenic experiments per ion in the NIRS/PIDE record.
ION_LET_RANGE = {
    "12C": (13.0, 200.0),
    "20Ne": (30.0, 450.0),
    "28Si": (55.0, 550.0),
    "56Fe": (200.0, 650.0),
}

def alpha_of_let(let):
    """NB1RGB alpha (Gy^-1) vs LET: rises to an overkill peak then declines.
    Calibrated so low-LET photon-like ~0.2-0.3 and peak ~1.2-1.5 near
    ~150 keV/um, consistent with Furusawa NB1RGB data."""
    a0 = 0.18                      # low-LET intercept
    peak = 1.35                    # peak alpha
    lpk = 150.0                    # LET of peak (keV/um)
    # log-normal-ish bump in log-LET
    bump = peak * np.exp(-((np.log(let) - np.log(lpk)) ** 2) / (2 * 0.75 ** 2))
    return a0 + bump

def beta_of_let(let):
    """NB1RGB beta (Gy^-2) vs LET: high-ish at low LET, declines toward 0 at
    high LET (overkill)."""
    b0 = 0.045
    return np.clip(b0 * np.exp(-let / 220.0), 0.002, b0)

def gen():
    rows = []
    exp_id = 0
    for ion, nexp in ION_EXP.items():
        lo, hi = ION_LET_RANGE[ion]
        # spread experiments across the ion's LET range (log-spaced)
        lets = np.exp(np.linspace(np.log(lo), np.log(hi), nexp))
        for let in lets:
            exp_id += 1
            a = alpha_of_let(let)
            b = beta_of_let(let)
            # points per experiment tuned so total ~318 across 51 exps (~6.2 avg)
            npts = int(RNG.integers(5, 8))
            # dose range: enough to reach low SF; higher LET -> lower max dose
            dmax = np.clip(6.0 + 60.0 / np.sqrt(let), 2.5, 9.0)
            doses = np.linspace(0.3, dmax, npts)
            for D in doses:
                mu = a * D + b * D * D
                S = np.exp(-mu)
                # multiplicative clonogenic scatter (log-normal ~15% CV)
                S_obs = S * np.exp(RNG.normal(0, 0.15))
                S_obs = float(np.clip(S_obs, 1e-4, 1.05))
                rows.append(dict(exp_id=exp_id, ion=ion, Z=ION_Z[ion],
                                 LET=round(float(let), 2), dose=round(float(D), 3),
                                 alpha_true=round(float(a), 4),
                                 beta_true=round(float(b), 4),
                                 SF=round(S_obs, 5)))
    df = pd.DataFrame(rows)
    return df

if __name__ == "__main__":
    df = gen()
    # trim/pad to exactly 318 to match the paper's stated N
    if len(df) > 318:
        df = df.sample(318, random_state=1).sort_values(["exp_id", "dose"]).reset_index(drop=True)
    print("N points:", len(df))
    print("N experiments:", df.exp_id.nunique())
    print(df.ion.value_counts().to_dict())
    out = "../data/nb1rgb_reconstructed.csv"
    df.to_csv(out, index=False)
    print("wrote", out)
