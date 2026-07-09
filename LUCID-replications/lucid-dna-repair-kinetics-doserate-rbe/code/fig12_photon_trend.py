"""
Qualitative reproduction of the *photon* component of Figures 1 & 2
of Liew et al. 2022, using DU145 parameters (Table 1).

Figures 1 & 2 themselves plot the proton RBE vs dose-rate at fixed dose
(2, 6, 12, 24 Gy) and three LET values (2, 8, 25 keV/um), comparing:
  * "fixed-reference" RBE   = D^gamma(2 Gy/min) / D^p(D-dot)
  * "dose-rate adapted" RBE = D^gamma(D-dot)    / D^p(D-dot)
  * "no-repair" RBE         = D^gamma(inf)      / D^p(inf)

We cannot reproduce the proton part (track structure / Kiefer-Chatterjee
not implemented here).  But the PHOTON-only ratio
  R_gamma(D, D-dot) := D^gamma(D-dot) / D^gamma(inf)
is the key piece of Eq.(2) -- and Fig 4 left panel of the paper plots
exactly its inverse evaluated at the TD50 effect level (=R_TD50).

Here we evaluate R_gamma over the same dose / dose-rate grid as Figs 1-2
for DU145, to qualitatively check that:
  (a) at low dose-rate the curve flattens (no kinetic effect at infinite rate)
  (b) the dose-rate effect grows substantially with dose D (paper Table 2)
  (c) the "saturation at high dose-rate" trend is recovered.

We compare to Table 2 (max relative difference between fixed-reference RBE
and no-repair RBE) at 2, 6, 12, 24 Gy.  Since LET only modulates the proton
side, Table 2 numbers vary with LET; the PHOTON-side maximum saturation
gain (gamma-only contribution) is the *upper bound* of those LET-resolved
percentages for each dose row.

We extract R_gamma_max = D^gamma_sat / D^gamma(2 Gy/min) for each dose,
where D^gamma_sat is the dose at the same survival but at very high
photon dose rate (1000 Gy/min ~ effectively infinite vs TiDSB^{1/2}=4 min).
"""
import os, sys, time, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from universe_photon import survival_photon, DU145, dose_for_effect_photon

OUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "results"))
os.makedirs(OUT_DIR, exist_ok=True)

DOSES = [2.0, 6.0, 12.0, 24.0]
D_FIXED = 2.0   # Gy/min  (fixed-reference rate used in Figs 1-2)
D_SAT   = 200.0 # Gy/min  -- effectively "infinite" relative to 4-min repair half-life

rows = []
print(f"{'Dose':>6}  {'S@2Gy/min':>10}  {'S@200Gy/min':>12}  "
      f"{'D@S*@2Gy/min':>13}  {'D@S*@inf':>10}  {'R_gamma_max':>11}", flush=True)

for D in DOSES:
    t = time.time()
    # Linearize the INFINITE-rate curve locally around dose D itself, using
    # a small step delta = 0.5 Gy in BOTH directions so the slope estimate
    # captures local curvature without underflowing.  When S(D, inf) ~ 0
    # at very high D, also bound D_inf_for_sstar from below.
    delta = 0.5
    rng_inf_a = np.random.default_rng(170 + int(D*10))
    rng_inf_b = np.random.default_rng(270 + int(D*10))
    rng_ref   = np.random.default_rng( 70 + int(D*10))
    s_inf_a = survival_photon(D - delta, D_SAT,   DU145, n_iter=2000, rng=rng_inf_a)
    s_inf_b = survival_photon(D + delta, D_SAT,   DU145, n_iter=2000, rng=rng_inf_b)
    s_ref   = survival_photon(D,         D_FIXED, DU145, n_iter=2000, rng=rng_ref)
    s_inf   = (s_inf_a * s_inf_b) ** 0.5  # central-ish estimate of S(D, inf)
    # protect against zero survival
    EPS = 1e-12
    s_inf_a_c = max(s_inf_a, EPS)
    s_inf_b_c = max(s_inf_b, EPS)
    s_ref_c   = max(s_ref,   EPS)
    s_inf_c   = max(s_inf,   EPS)
    k_inf   = -(np.log(s_inf_b_c) - np.log(s_inf_a_c)) / (2.0 * delta)
    # Solve S_ref = s_inf_c * exp(-k_inf * (D_inf_for_sstar - D))
    D_inf_for_sstar = D + (np.log(s_inf_c) - np.log(s_ref_c)) / k_inf
    R_gamma_max = D / D_inf_for_sstar
    pct = (R_gamma_max - 1.0)*100
    rows.append({"D_Gy": D, "S_at_2Gymin": float(s_ref),
                 "S_at_200Gymin": float(s_inf),
                 "k_inf_per_Gy": float(k_inf),
                 "D_inf_for_S_star_Gy": float(D_inf_for_sstar),
                 "R_gamma_max": float(R_gamma_max),
                 "saturation_gain_percent": float(pct)})
    print(f"{D:>6.1f}  {s_ref:>10.4f}  {s_inf:>12.4f}  "
          f"{D:>13.2f}  {D_inf_for_sstar:>10.3f}  {R_gamma_max:>11.4f}    "
          f"({time.time()-t:.1f}s)", flush=True)

# Paper Table 2 -- max relative difference between fixed-reference RBE and
# no-repair RBE for the DU145 cell line (Figs 1+2 settings).  Values are
# percentages, one per (Dose, LET) pair.
table2 = {
    2:  {2: 1.3,  8: 1.8,  25: 3.5},
    6:  {2: 6.2,  8: 5.1,  25: 9.9},
    12: {2: 12.9, 8: 16.6, 25: 22.2},
    24: {2: 34.1, 8: 36.8, 25: 45.4},
}

print("\nComparison: R_gamma_max-1 (this work, photon-only) vs Table 2 values:")
print("(Table 2 numbers depend on LET because the *proton* response also changes;")
print(" the photon-only gain is expected to lie within or below the LET range)")
print(f"{'D[Gy]':>5}  {'gamma-only gain [%]':>20}  "
      f"{'2 keV/um':>9}  {'8 keV/um':>9}  {'25 keV/um':>9}")
comp = {}
for row in rows:
    D = row["D_Gy"]
    gain = row["saturation_gain_percent"]
    vals = table2[int(D)]
    comp[int(D)] = {"gamma_only_gain_pct": gain, "table2_LET": vals}
    print(f"{D:>5.1f}  {gain:>20.2f}  {vals[2]:>9.1f}  {vals[8]:>9.1f}  {vals[25]:>9.1f}")

with open(os.path.join(OUT_DIR, "fig12_photon_trend.json"), "w") as f:
    json.dump({"rows": rows, "paper_table2": table2,
               "comparison": comp}, f, indent=2)
print(f"\nWrote {OUT_DIR}/fig12_photon_trend.json")
