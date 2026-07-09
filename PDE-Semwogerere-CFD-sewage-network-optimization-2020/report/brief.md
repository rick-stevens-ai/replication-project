# Brief — Semwogerere et al. 2020, CFD sewer optimization (Tororo Municipality)

Semwogerere, Noah, Masanja et al. (J. Adv. Math. 18, 2020,
doi:10.24297/jam.v18i.8345) propose using OpenFOAM's `interFoam` two-phase VOF
solver with a k-ε turbulence model to optimize municipal sewage networks, using
Tororo Municipality (Uganda) as a case study.  Their concrete deliverable is
**Table 1**, a set of recommended minimum slopes S for eight standard sewer pipe
diameters D ∈ {150, 200, 250, 300, 375, 450, 525, 600} mm, plus qualitative
CFD velocity/pressure field visualisations (Figs 2–10) in a 2D, 20 m × 0.5 m
pipe.  Independently, we (a) show Table 1 IS the Manning self-cleansing curve
at v_min = 0.60 m/s, n = 0.013, half-full (mean |err| = 2.7 %, max 10.8 %), and
(b) rerun the paper's `interFoam` two-phase pipe simulation on a fresh 8 000-cell
mesh and reproduce the qualitative behaviour (mean flow speed 0.62 m/s,
hydrostatic pressure ~4.4 kPa at the pipe bottom, water fraction 0.52 → 0.59
over 5 s of simulated time).  Verdict: **REPLICATED** for the paper's core
quantitative claim (Table 1); the OpenFOAM/interFoam methodology is
independently confirmed as executable and self-consistent.
