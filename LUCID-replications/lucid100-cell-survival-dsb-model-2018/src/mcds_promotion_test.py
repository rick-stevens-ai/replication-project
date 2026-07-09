"""
Wang 2018 PARTIAL -> REPLICATED promotion test.

QUESTION (from AUDIT_PROTOCOL promotion gate, mirrors LUCID-Prelim P3):
  The original replication marked PARTIAL because the published D10 values
  (4.08 Gy HSG, 7.07 Gy V79, X-ray) only reproduce when Y_X (X-ray DSB yield)
  is treated as a FREE parameter ~= 55.5 (HSG) / 50.9 (V79). The publicly
  available McMahon 2017 MCDS calibration gives Y_X ~= 34, which UNDER-predicts
  low-LET sensitivity (D10 ~= 6.6 / 11.2 Gy).

  Kukla produced a FIRST-PRINCIPLES MCDS 3.10A Sigma_DSB(LET) table.
  Promotion test: feed the MCDS X-ray-equivalent (low-LET limit) Sigma_DSB as Y
  into the Wang model. Does D10 4.08 / 7.07 reproduce WITHOUT free-fitting Y?
    - If YES -> PARTIAL -> REPLICATED
    - If NO  -> stays PARTIAL (published params only self-consistent w/ inflated Y)

DATA:
  MCDS table: ~/Dropbox/LUCID-Prelim/problem-03-rbe-let-radiation-quality/data/MCDS/sigma_dsb_let_mcds310a.tsv
  columns: ion, KE_MeV, AD, LET_keV_um, DSB_total (=Sigma_DSB DSB/Gy/cell), SSB_total

METHOD:
  X-rays / 250 kVp photons are sparsely ionizing, dose-mean LET ~ 1-2 keV/um
  (secondary electrons). The MCDS X-ray-equivalent DSB yield is the low-LET
  limit of Sigma_DSB(LET). We take the lowest-LET protons as the X-ray proxy
  AND extrapolate Sigma_DSB to LET->0 in log-LET space, bracketing the answer.
"""
import os
import numpy as np
from wang2018_model import (
    cell_survival, HSG_PARAMS, V79_PARAMS,
)

MCDS_TSV = os.path.expanduser(
    "~/Dropbox/LUCID-Prelim/problem-03-rbe-let-radiation-quality/data/MCDS/sigma_dsb_let_mcds310a.tsv"
)


def load_mcds():
    rows = []
    with open(MCDS_TSV) as f:
        header = f.readline().strip().split("\t")
        for line in f:
            p = line.strip().split("\t")
            if len(p) < 5:
                continue
            try:
                rows.append({
                    "ion": p[0],
                    "KE": float(p[1]),
                    "LET": float(p[3]),
                    "DSB": float(p[4]),
                })
            except ValueError:
                continue
    return rows


def d10_from_survival(Y, lam_p, n_p_perGy, cell):
    """Find dose where SF = 0.1 by scanning."""
    D = np.linspace(0.01, 30, 30000)
    S = cell_survival(D, Y, lam_p, n_p_perGy, cell)
    # first crossing of 0.1
    idx = np.argmin(np.abs(S - 0.1))
    return D[idx]


def main():
    rows = load_mcds()
    protons = sorted([r for r in rows if r["ion"] == "1H"], key=lambda r: r["LET"])

    print("=" * 72)
    print("Wang 2018 MCDS-promotion test  (Kukla Sigma_DSB(LET) first-principles Y)")
    print("=" * 72)
    print("\nMCDS proton low-LET tail (X-ray proxy candidates):")
    for r in protons[:6]:
        print(f"   1H KE={r['KE']:>6} MeV  LET={r['LET']:>7.3f} keV/um  Sigma_DSB={r['DSB']:.3f} DSB/Gy/cell")

    # X-ray-equivalent Sigma_DSB:
    # (a) lowest-LET proton entry (LET~0.45) as direct low-LET proxy
    low = protons[0]
    Y_mcds_lowestproton = low["DSB"]

    # (b) log-LET extrapolation of Sigma_DSB to a typical X-ray dose-mean LET ~ 1.5 keV/um
    lets = np.array([r["LET"] for r in protons])
    dsb = np.array([r["DSB"] for r in protons])
    # fit Sigma_DSB vs log10(LET) over the low-LET region (LET < 30)
    mask = lets < 30
    coef = np.polyfit(np.log10(lets[mask]), dsb[mask], 1)
    Y_mcds_xrayLET = np.polyval(coef, np.log10(1.5))  # X-ray dose-mean LET ~1.5

    print(f"\nMCDS X-ray-equivalent Sigma_DSB candidates:")
    print(f"   (a) lowest-LET proton (LET={low['LET']:.2f}):   Y = {Y_mcds_lowestproton:.2f} DSB/Gy/cell")
    print(f"   (b) log-LET extrap to X-ray LET~1.5 keV/um:  Y = {Y_mcds_xrayLET:.2f} DSB/Gy/cell")

    # For X-rays, low-LET limit: lam_p -> 1 (each track makes ~1 DSB),
    # n_p_perGy -> Y (every DSB from a separate sparse track).
    lam_p = 1.0

    print("\n" + "-" * 72)
    print("D10 PREDICTIONS with first-principles MCDS Y (X-ray, lam_p=1):")
    print("-" * 72)
    targets = {"HSG": (HSG_PARAMS, 4.08), "V79": (V79_PARAMS, 7.07)}
    free_fit = {"HSG": 55.48, "V79": 50.94}

    results = {}
    for name, (cell, d10_paper) in targets.items():
        print(f"\n{name}  (paper D10 = {d10_paper} Gy; free-fit Y = {free_fit[name]:.1f}):")
        for label, Yval in [
            ("MCDS lowest-proton", Y_mcds_lowestproton),
            ("MCDS X-ray-LET extrap", Y_mcds_xrayLET),
            ("McMahon2017 ref ~34", 34.43 if name == "HSG" else 32.13),
            ("free-fit (orig)", free_fit[name]),
        ]:
            d10 = d10_from_survival(Yval, lam_p, Yval, cell)
            err = 100 * (d10 - d10_paper) / d10_paper
            flag = "  <-- reproduces" if abs(err) < 10 else ""
            print(f"   Y={Yval:6.2f}  ({label:24s})  D10={d10:6.2f} Gy   err={err:+6.1f}%{flag}")
            if label.startswith("MCDS"):
                results.setdefault(name, []).append((label, Yval, d10, err))

    print("\n" + "=" * 72)
    print("PROMOTION VERDICT")
    print("=" * 72)
    promote = True
    for name, (cell, d10_paper) in targets.items():
        best = min(results[name], key=lambda t: abs(t[3]))
        ok = abs(best[3]) < 10
        promote = promote and ok
        print(f"  {name}: best MCDS D10={best[2]:.2f} Gy vs paper {d10_paper} "
              f"(err {best[3]:+.1f}%, via {best[0]}) -> {'PASS' if ok else 'FAIL'}")
    print(f"\n  => {'PROMOTE to REPLICATED' if promote else 'STAYS PARTIAL'}: "
          f"first-principles MCDS Y "
          f"{'reproduces' if promote else 'does NOT reproduce'} published D10 "
          f"without free-fitting.")


if __name__ == "__main__":
    main()
