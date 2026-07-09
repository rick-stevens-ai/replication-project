#!/usr/bin/env python3
"""
Replication of Mentana et al. 2025 (Sci. Rep. 15:2209)
DOI: 10.1038/s41598-025-85879-2
"Mapping neutron biological effectiveness for DNA damage induction as
 a function of incident energy and depth in a human sized phantom"

CENTRAL REPRODUCIBLE CLAIM
==========================
The paper provides an explicit analytical fit (Eq. 5) of the maximal neutron
RBE for DSB cluster induction (= RBE in the outermost shell #1, 0-1 cm depth
of the ICRU sphere), as a function of incident neutron energy E_n (MeV):

  RBE(E_n) = q1
           + q2 * exp(-q3 * (ln(E_n * q4))**2)
           + q5 * exp(-q6 * (ln(E_n * q7))**2)
           + q8 * exp(-q9 * (ln(E_n * q10))**2)
           + (q11 * q12**2) / ((ln(E_n * q13))**2 + q12**2)        # Breit-Wigner in log-E
           + q14 * exp(-q15 * (ln(E_n * exp(q16)))**2)

with q1..q16 published in the Methods (one decimal of model RBE in Table 1).

The 26 model RBE(E_n) values in column 1 (shell #1, mean depth 0.5 cm) of
the upper half of Table 1 are the *direct* end-product of the full PHITS+
PARTRAC pipeline at the outermost shell. The same numbers are claimed to be
the data on which Eq. 5 was fit by nlinfit (MATLAB R2022a) with the published
q-parameters. So we can rigorously check:

  (i)  Implementation of Eq. 5 produces RBE values for the tabulated En grid
       that match Table 1 column 1 (DSB clusters, outermost shell) to within
       the rounding (Table is to 1 decimal) and fit residuals.

  (ii) Qualitative features expected: main peak ~0.5 MeV at RBE~16, second
       sharp peak ~20 MeV at RBE~11, low-energy thermal bump ~4 at 1e-8 MeV,
       high-energy fall-off to ~2 at 1e5 MeV.

This is the cleanest single end-to-end audit possible without running PHITS.
The PHITS-PARTRAC pipeline itself (Eqs. 1-4) is logic+citation audited in
the report; it cannot be run here (PHITS license, PARTRAC closed-source).
"""

from __future__ import annotations
import numpy as np
import json
import sys
from pathlib import Path

# ----- Published Eq. 5 parameters (Methods, Mentana et al. 2025) -----
Q = dict(
    q1=2.0384, q2=2.041, q3=0.0712, q4=0.0087,
    q5=14.1637, q6=0.3131, q7=2.5404,
    q8=3.1439, q9=0.611, q10=0.0383,
    q11=4.2598, q12=0.2139, q13=0.0538,
    q14=3.1486, q15=0.0099, q16=25.0623,
)


def rbe_eq5(E_n_MeV: np.ndarray, q: dict = Q) -> np.ndarray:
    """Eq. 5 of Mentana et al. 2025.  E_n in MeV.  Returns max-RBE (DSB clusters)."""
    E = np.asarray(E_n_MeV, dtype=float)
    L = np.log  # natural log
    t1 = q['q1']
    t2 = q['q2'] * np.exp(-q['q3'] * (L(E * q['q4'])) ** 2)
    t3 = q['q5'] * np.exp(-q['q6'] * (L(E * q['q7'])) ** 2)
    t4 = q['q8'] * np.exp(-q['q9'] * (L(E * q['q10'])) ** 2)
    t5 = (q['q11'] * q['q12'] ** 2) / ((L(E * q['q13'])) ** 2 + q['q12'] ** 2)
    t6 = q['q14'] * np.exp(-q['q15'] * (L(E * np.exp(q['q16']))) ** 2)
    return t1 + t2 + t3 + t4 + t5 + t6


# ----- Paper Table 1, upper half (DSB clusters), column 1 = shell #1 (mean depth 0.5 cm) -----
# Transcribed from the OCR/PDF Table 1 (E_n in MeV, RBE_max in shell #1).
TABLE1_DSB_CLUSTERS_SHELL1 = [
    (1e-8,    4.1),
    (1e-7,    3.4),
    (1e-6,    3.0),
    (1e-4,    2.4),
    (1e-3,    2.0),
    (1e-2,    2.3),
    (1e-1,   10.0),
    (2e-1,   14.5),
    (5e-1,   16.1),
    (8e-1,   14.2),
    (1.0,    13.8),
    (2.5,     7.6),
    (5.0,     6.0),
    (7.5,     5.6),
    (10.0,    7.1),
    (15.0,    8.7),
    (17.5,   10.3),
    (20.0,   11.0),
    (22.5,    8.9),
    (25.0,    8.4),
    (50.0,    6.6),
    (100.0,   5.2),
    (500.0,   3.9),
    (1000.0,  3.4),
    (10000.0, 2.6),
    (100000.0, 2.1),
]


def main(out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    E_tab = np.array([row[0] for row in TABLE1_DSB_CLUSTERS_SHELL1])
    RBE_tab = np.array([row[1] for row in TABLE1_DSB_CLUSTERS_SHELL1])
    RBE_eq5 = rbe_eq5(E_tab)

    abs_err = RBE_eq5 - RBE_tab
    rel_err = abs_err / RBE_tab

    print(f"{'E_n (MeV)':>12}  {'Table 1 #1':>10}  {'Eq.5':>8}  {'diff':>7}  {'rel%':>7}")
    print("-" * 60)
    for E, t, m, d, r in zip(E_tab, RBE_tab, RBE_eq5, abs_err, rel_err):
        print(f"{E:12.4g}  {t:10.2f}  {m:8.3f}  {d:7.3f}  {100*r:7.2f}")

    # Summary metrics
    rmse = float(np.sqrt(np.mean(abs_err ** 2)))
    mae = float(np.mean(np.abs(abs_err)))
    max_abs = float(np.max(np.abs(abs_err)))
    max_rel = float(np.max(np.abs(rel_err)))
    n_within_05 = int(np.sum(np.abs(abs_err) <= 0.5))
    n_within_10 = int(np.sum(np.abs(abs_err) <= 1.0))
    n_within_01 = int(np.sum(np.abs(abs_err) <= 0.1))

    # Locate peaks predicted by Eq. 5 on a fine grid
    E_fine = np.logspace(-8, 5, 4001)
    R_fine = rbe_eq5(E_fine)
    i_peak = int(np.argmax(R_fine))
    E_peak = float(E_fine[i_peak]); R_peak = float(R_fine[i_peak])

    # Locate 20 MeV secondary peak (search 10-30 MeV)
    mask2 = (E_fine >= 10) & (E_fine <= 30)
    i2 = int(np.argmax(R_fine[mask2]))
    E_peak2 = float(E_fine[mask2][i2]); R_peak2 = float(R_fine[mask2][i2])

    summary = dict(
        n_points=len(E_tab),
        rmse=rmse, mae=mae,
        max_abs_err=max_abs, max_rel_err=max_rel,
        n_within_0p1=n_within_01,
        n_within_0p5=n_within_05,
        n_within_1p0=n_within_10,
        main_peak_E_MeV=E_peak, main_peak_RBE=R_peak,
        secondary_peak_E_MeV=E_peak2, secondary_peak_RBE=R_peak2,
        paper_main_peak_claim="~0.5 MeV, RBE ~16",
        paper_secondary_peak_claim="~20 MeV, RBE ~11",
        paper_thermal_RBE_claim="RBE(En=1e-8 MeV) = 4.1 (DSB clusters, shell #1)",
    )

    print()
    print("SUMMARY:")
    for k, v in summary.items():
        print(f"  {k}: {v}")

    (out_dir / "replication_summary.json").write_text(json.dumps(summary, indent=2))
    np.savetxt(
        out_dir / "eq5_vs_table1.csv",
        np.column_stack([E_tab, RBE_tab, RBE_eq5, abs_err, rel_err]),
        delimiter=",",
        header="E_n_MeV,RBE_Table1_shell1,RBE_Eq5,abs_err,rel_err",
        comments="",
    )

    # Also dump a fine curve for plotting
    np.savetxt(
        out_dir / "eq5_fine_curve.csv",
        np.column_stack([E_fine, R_fine]),
        delimiter=",",
        header="E_n_MeV,RBE_Eq5",
        comments="",
    )
    print(f"\nWrote: {out_dir/'replication_summary.json'}")
    print(f"Wrote: {out_dir/'eq5_vs_table1.csv'}")
    print(f"Wrote: {out_dir/'eq5_fine_curve.csv'}")


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent.parent / "evidence"
    main(out)
