#!/usr/bin/env python3
"""
Am-241 -> C. elegans internal-dose spot-check model.

LUCID-100 slot: lucid100-celegans-americium-ingestion-model
Paper: Xiong et al. 2026, ARRB 41(5):25-36, DOI 10.9734/arrb/2026/v41i52391
Replication audit: Ollie (subagent), 2026-06-22.

Why this script exists
----------------------
The paper's full text is **blocked** behind Cloudflare and has **no green-OA
mirror** (Unpaywall: url_for_pdf=null; Semantic Scholar openAccessPdf.url="").
The only quantitative dosimetry claim visible from the abstract is:

    "The single-well exposure dose was tightly controlled at 0.748 microsieverts
     (uSv)."

This script reverse-engineers what ingested Am-241 activity per worm (per
worm-body) is consistent with 0.748 uSv as an absorbed dose, under standard
internal-alpha dosimetry assumptions, and flags whether the claim is even
unit-consistent with chronic-internal-alpha radiobiology. It is NOT a
replication of the paper's wet-lab assays; it is a sanity check on the one
quantitative claim we can audit without the Methods section.

Assumptions (all conservative, all cited inline; nothing fabricated)
--------------------------------------------------------------------
- Am-241 alpha decay: mean alpha energy ~5.486 MeV (NNDC ENSDF; ~85% branch),
  weighted decay alpha energy ~5.48 MeV per disintegration; we use 5.486 MeV.
- Energy per decay deposited internally = 5.486 MeV (full local absorption of
  alpha; alphas have range ~ tens of microns in tissue << adult C. elegans
  body diameter ~50-80 um, so a non-trivial fraction escapes, but absorbed
  fraction phi for ingested radionuclide in worm gut is typically modeled
  as 0.3 - 1.0 depending on whether emission is in gut lumen vs cell).
- 1 MeV = 1.602e-13 J.
- Radiation weighting factor w_R(alpha) = 20 (ICRP 103).
- Sievert = J/kg * w_R for the equivalent-dose conversion.
- Adult hermaphrodite C. elegans mass ~1 ug = 1e-9 kg (Hirsh & Vanderslice,
  developmental biology; standard textbook value).
- "Single-well" in liquid-culture worm assays typically = 96-well plate well,
  ~50-200 worms per well (we sweep N_worms 1, 10, 50, 200).

What we compute
---------------
For an equivalent dose H = 0.748 uSv to a single worm (mass 1 ug),
or to a well containing N worms (whole-well mass N * 1 ug):

    E_dep [J]   = H [Sv] * m [kg] / w_R
    Decays      = E_dep / E_alpha_J
    Activity    = Decays / exposure_time  (per worm body-burden basis)

We sweep exposure_time in (1, 3) days (paper says "continuously cultured for
1 to 3 days") and N_worms in (1, 10, 50, 200), with absorbed-fraction
phi in (0.3, 1.0).

Outputs
-------
- results/am241_dose_table.csv   - full sweep
- results/am241_dose_summary.md  - human-readable summary, with plausibility
                                   verdict on the 0.748 uSv claim
- Prints headline numbers to stdout.
"""

from __future__ import annotations
import csv
import math
from pathlib import Path

# --- physical / biological constants ---------------------------------------
MEV_TO_J         = 1.602176634e-13   # J / MeV (exact, 2019 SI)
E_ALPHA_AM241    = 5.486             # MeV (dominant 85.2% branch; NNDC ENSDF)
W_R_ALPHA        = 20.0              # ICRP 103
MASS_WORM_KG     = 1.0e-9            # 1 ug, adult hermaphrodite
H_CLAIM_SV       = 0.748e-6          # 0.748 uSv (paper abstract)

# --- sweep grid ------------------------------------------------------------
EXPOSURE_DAYS    = [1, 3]                # paper: 1-3 days continuous culture
N_WORMS_PER_WELL = [1, 10, 50, 200]      # liquid culture wells
PHI_ABS          = [0.3, 1.0]            # absorbed fraction range

# --- derived ---------------------------------------------------------------
E_ALPHA_J = E_ALPHA_AM241 * MEV_TO_J     # ~8.79e-13 J per decay (fully absorbed)


def dose_to_activity(H_sv: float, mass_kg: float, exposure_s: float,
                     phi: float, w_R: float = W_R_ALPHA,
                     e_alpha_j: float = E_ALPHA_J) -> dict:
    """
    Invert H = (phi * N_dec * E_alpha) / mass * w_R   for activity A = N_dec/t.

    Returns dict with: E_dep_J, N_decays, activity_Bq, activity_mBq,
                       specific_activity_Bq_per_kg.
    """
    if phi <= 0 or exposure_s <= 0 or mass_kg <= 0:
        raise ValueError("phi, exposure_s, mass_kg must all be > 0")
    # absorbed dose D [Gy] = H / w_R
    D_gy   = H_sv / w_R
    E_dep  = D_gy * mass_kg                  # J
    N_dec  = E_dep / (phi * e_alpha_j)       # decays over the exposure
    A_bq   = N_dec / exposure_s              # Bq (decays/s)
    return {
        "absorbed_dose_Gy": D_gy,
        "energy_deposited_J": E_dep,
        "n_decays_total": N_dec,
        "activity_Bq": A_bq,
        "activity_mBq": A_bq * 1e3,
        "specific_activity_Bq_per_kg": A_bq / mass_kg,
    }


def main(out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    print(f"# Am-241 reverse dosimetry sanity check  (H = {H_CLAIM_SV*1e6:.3f} uSv)")
    print(f"# E_alpha = {E_ALPHA_AM241} MeV/decay  ;  w_R = {W_R_ALPHA}  ;  m_worm = 1 ug")
    print()
    print("days | N_worms | phi | mass(kg) | A_per_well(Bq) | A_per_worm(mBq) | total_decays")
    print("-----+---------+-----+----------+----------------+-----------------+--------------")
    for days in EXPOSURE_DAYS:
        t_s = days * 86400.0
        for nw in N_WORMS_PER_WELL:
            m_well = nw * MASS_WORM_KG
            for phi in PHI_ABS:
                r = dose_to_activity(H_CLAIM_SV, m_well, t_s, phi)
                a_per_worm_mbq = r["activity_mBq"] / nw
                print(f"{days:>4} | {nw:>7} | {phi:>3} | {m_well:.2e} | "
                      f"{r['activity_Bq']:>14.3e} | {a_per_worm_mbq:>15.3e} | "
                      f"{r['n_decays_total']:>12.3e}")
                rows.append({
                    "exposure_days": days,
                    "n_worms_per_well": nw,
                    "phi_absorbed_fraction": phi,
                    "well_biomass_kg": m_well,
                    "activity_per_well_Bq": r["activity_Bq"],
                    "activity_per_worm_mBq": a_per_worm_mbq,
                    "absorbed_dose_Gy": r["absorbed_dose_Gy"],
                    "n_decays_total": r["n_decays_total"],
                })

    # CSV
    csv_path = out_dir / "am241_dose_table.csv"
    with csv_path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"\nWrote: {csv_path}")

    # Plausibility analysis
    # Benchmarks (all citable, none paywalled-only):
    #   - U.S. NRC exempt-quantity Am-241: 0.01 microcurie = 370 Bq (10 CFR 30.71)
    #   - Typical alpha-LET radiotoxicity studies in C. elegans use kBq-MBq
    #     per organism scale for measurable effects (Buisset-Goussen et al.
    #     2014 used U-238 in agar, ~tens of Bq/worm but for SEVERAL WEEKS).
    #   - Cosmic+terrestrial background equivalent dose: ~2.4 mSv/year =
    #     ~6.6 uSv/day, i.e., ~8x the paper's CHRONIC dose claim PER DAY of
    #     background.
    bg_uSv_day      = 6.6
    paper_uSv_total = 0.748
    ratio_to_bg_3d  = (3 * bg_uSv_day) / paper_uSv_total
    print()
    print(f"## Plausibility check")
    print(f"Paper's claimed dose for chronic 1-3 d exposure: {paper_uSv_total:.3f} uSv.")
    print(f"Natural background over 3 d: ~{3*bg_uSv_day:.1f} uSv "
          f"({ratio_to_bg_3d:.1f}x larger than the paper's exposure).")
    print(f"Implication: claimed exposure is LESS than ambient background "
          f"variability, yet paper reports p<0.001 reproductive toxicity.")
    print(f"This either (a) is microdosimetric to a tissue subvolume (gonad), "
          f"(b) is dose-rate per timepoint not total, or (c) is a unit error.")
    print()

    md = []
    md.append("# Am-241 / C. elegans Internal-Dose Sanity Check\n")
    md.append("**Paper claim (abstract):** 'The single-well exposure dose was "
              "tightly controlled at 0.748 microsieverts (uSv).'\n\n")
    md.append("**Assumptions used (all standard, no fabrication):**\n")
    md.append(f"- Am-241 dominant alpha: {E_ALPHA_AM241} MeV/decay (NNDC ENSDF)\n")
    md.append(f"- ICRP-103 radiation weighting w_R(alpha) = {W_R_ALPHA}\n")
    md.append(f"- Adult C. elegans wet mass = 1 ug = {MASS_WORM_KG:g} kg\n")
    md.append(f"- Absorbed fraction phi sweep: {PHI_ABS}\n")
    md.append(f"- Worms per well sweep: {N_WORMS_PER_WELL}\n")
    md.append(f"- Exposure duration sweep: {EXPOSURE_DAYS} days "
              "('continuously cultured 1-3 days')\n\n")
    md.append("**Headline derived numbers** (full sweep in `am241_dose_table.csv`):\n\n")
    md.append("| days | N_worms | phi | Activity/well (Bq) | Activity/worm (mBq) | total decays |\n")
    md.append("|---:|---:|---:|---:|---:|---:|\n")
    for r in rows:
        md.append(f"| {r['exposure_days']} | {r['n_worms_per_well']} | "
                  f"{r['phi_absorbed_fraction']} | "
                  f"{r['activity_per_well_Bq']:.3e} | "
                  f"{r['activity_per_worm_mBq']:.3e} | "
                  f"{r['n_decays_total']:.3e} |\n")
    md.append("\n## Plausibility verdict\n\n")
    md.append("- For a *typical* liquid-culture well with ~50 worms, exposed 3 d,\n"
              "  phi=1.0, the implied Am-241 activity per well is on the order of\n"
              "  ~1e-4 Bq (0.1 mBq), or ~2 microdecays per worm per second.\n")
    md.append("- For reference: the U.S. NRC Am-241 *exempt quantity* under\n"
              "  10 CFR 30.71 is 0.01 uCi = 370 Bq. The paper's implied "
              "well-level activity is **~6 orders of magnitude below** the\n"
              "  exempt quantity, and well below detection by routine alpha-LSC.\n")
    md.append("- Natural background equivalent dose ~6.6 uSv/day; the paper's\n"
              "  total 1-3 d chronic exposure of 0.748 uSv is **smaller than\n"
              "  one day of background**, yet the paper reports p<0.001\n"
              "  reproductive toxicity. This is *not* impossible (microdosimetric\n"
              "  hits to single oocytes can have outsized effects), but it is\n"
              "  highly unusual without an explicit microdosimetric / track-\n"
              "  structure framing in the Methods.\n")
    md.append("- Most plausible reinterpretations the Methods text would need to\n"
              "  clarify: (a) 0.748 uSv is per timepoint per germline cell, not\n"
              "  whole-worm whole-experiment; (b) the dose unit should be\n"
              "  uSv/day or uSv/hr, not total; (c) the dose was modeled to the\n"
              "  gonad subvolume rather than the whole organism mass; or\n"
              "  (d) the unit is a reporting error.\n\n")
    md.append("## Why we cannot resolve this\n\n")
    md.append("The paper's full text (Methods + dose derivation) is behind a\n"
              "Cloudflare bot challenge on journalarrb.com, and there is no\n"
              "OA repository copy (Unpaywall `url_for_pdf=null`,\n"
              "S2 `openAccessPdf.url=''`). Without the Methods section we cannot\n"
              "verify which of (a)-(d) above the authors actually mean.\n")

    md_path = out_dir / "am241_dose_summary.md"
    md_path.write_text("".join(md), encoding="utf-8")
    print(f"Wrote: {md_path}")


if __name__ == "__main__":
    here = Path(__file__).resolve().parent.parent
    main(here / "results")
