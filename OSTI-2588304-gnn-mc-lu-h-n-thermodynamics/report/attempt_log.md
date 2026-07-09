# Attempt Log — OSTI-2588304

## v1 (2026-07-03)
- Cloned CGCNN, wrote synthetic Lu(H,N,Va)_3 dataset (1000 configs).
- Trained with paper's Table I hyperparameters, MAE=2.94 meV/atom, R²=0.993 on 100 held-out configs.
- Ran short lattice-swap MC demo.
- **Verdict: SPOT-CHECK.** Blocked on real DFT training data (paper's SI is a PDF).

## v2 (2026-07-04) — promotion to PARTIAL
- **Tried SI data acquisition:** `api.osti.gov` fails DNS on this host; ChemRxiv Cloudflare-gates the download; `osti.gov/servlets/purl/2588304` connection timeout. Abandoned SI-data path.
- **Switched to REAL public DFT data via Materials Project OPTIMADE.** No API key required.
  - Harvested 86 metal-hydride structures across 18 metals (Lu, Y, Sc, La, Ce, Pr, Nd, Sm, Gd, Er, Yb, Ti, Zr, Hf, V, Nb, Ta) with GGA/GGA+U formation_energy_per_atom labels.
  - Key finding: **only 3 Lu-H compounds exist in MP** — this IS the data-scarcity that motivated the paper.
- Trained CGCNN with **paper's exact Table I hyperparams** on the 86-config real MP dataset:
  - Test MAE = 82.6 meV/atom, R² = 0.64 on 12 held-out configs.
  - Predict-mean baseline MAE = 120.8 meV/atom → model beats baseline by 32%.
  - Interpretation: ~2× paper target (40 meV/atom), on a much harder cross-metal problem with 10× less data.
- Also trained on rare-earth+group-3 subset (51 configs): MAE=98 meV/atom, R²=0.18 on 7 test configs (too small to conclude, kept as auxiliary evidence).
- **Extended MC:** wrote `mc_free_energy.py` — real 24-interstitial 2×2×2 FCC Lu lattice, Metropolis H↔N swaps, 3 compositions × 7 temperatures (300–2500 K), thermodynamic integration for F(T). Results all physically consistent (C_v > 0, F(T) monotonic, meV/atom composition separation).
- **Independent LLM-judge (Argo `gpt-4.1`, free):** returned PARTIAL with per-claim scoring. Transcript archived.
- Wrote v2 REPORT.md with full claims table, method §, and results tables.

## Timings
- v2 additional work: ~35 minutes wall (data harvest 90s, 200-epoch train ~4 min, 300-epoch train ~5 min, MC 3 compositions × 7 T × 20k steps ~ 6 min).

## What's still blocked
- Paper's SI CIF files (would give exact C2, C4 numbers).
- ASAP MC (paper's exact code).
- Full para-equilibrium optimization + gas-phase reservoirs (needed to test C6 — the main scientific claim).
