# Re-pass Lift Table — FINAL (2026-06-23)

**45 papers re-passed** (all 5<cov<8 PARTIAL targets across LUCID / PDE / BVBRC / OSTI / general).
All on FREE compute (CherryRd CPU + Argo Opus 4.7). Each has PARSER_PROVENANCE.md + preserved REPORT.pass1.md.

- **Coverage lifted:** +80 points total across 45 papers (avg +1.8)
- **Agreement lifted:** +34 points total (avg +0.8)
- **Papers improved:** 44/45
- **Now REPLICATED/REPRODUCED/STRONG:** 28/45
- **Real errors caught in originals:** 9

## Integrity catches (errors in the prior pass-1 corpus)

- **2217719-SCALE-molten-salt** — Table-1 label swap caught; RSICC blocker
- **28589945-ARG-dissemination** — corrupt pass1 parse fixed; 100% id match
- **BVBRC-02-Ralstonia** — coord typo caught
- **BVBRC-04-Variovorax** — coord typo caught
- **BVBRC-07-Sherry-AMR** — --organism flag mismatch caught
- **FFNO-Tsunami** — pass1 peak nums wrong; corrected 5.20/7.30
- **apbs-pb** — caught pass1 error
- **modal-space-zhang-2019** — 2 silent v2 bugs: wrong dist + wrong PDE
- **zhang-spde-deepxde** — WRONG PAPER caught (1905 vs 1809)

## Full before→after table

| Paper | cov | agr | verdict | note |
|---|---|---|---|---|
| 1412756-Chiral-Spin-Order | 7→9 | 8→9 | PARTIAL-strong |  |
| 1461824-Photo-Z-PDFs | 6→6 | 7→7 | PARTIAL | held |
| 1523841-Polarization-diff | 6→8 | 8→8 | REPRODUCED-W-CAVEATS | named Wannier90 blocker |
| 1559043-ignition-kernel-turbulent | 7→9 | 8→9 | PARTIAL-strong |  |
| 1997354-Integer-Sequences | 7→9 | 8→10 | PARTIAL-strong |  |
| 2217719-SCALE-molten-salt | 6→8 | 8→8 | REPRODUCED | Table-1 label swap caught; RSICC blocker |
| 2587225-ScaWL-WL | 7→8 | 8→9 | PARTIAL | 11/12 PASS |
| 26392213-Outer-mucus-niche | 6→8 | 8→9 | REPLICATED |  |
| 28589945-ARG-dissemination | 7→8 | 8→9 | REPLICATED | corrupt pass1 parse fixed; 100% id match |
| 29769716-Mutant-phenotypes | 7→9 | 7→9 | REPLICATED | 17 claims EXACT; 84GB R-image blocker |
| 3003857-Divide-Conquer-Chaotic | 7→8 | 5→5 | Tier B | Lorenz grad 1.6e13x; ERA5 data-blocked |
| 3014512-DarkMatter-scattering | 6→7 | 8→8 | PARTIAL |  |
| BVBRC-02-Ralstonia | 6→8 | 8→8 | PARTIAL | coord typo caught |
| BVBRC-04-Variovorax | 6→9 | 8→9 | REPLICATED | coord typo caught |
| BVBRC-05-Trueperella | 7→8 | 8→9 | REPLICATED |  |
| BVBRC-07-Sherry-AMR | 7→9 | 8→9 | REPLICATED | --organism flag mismatch caught |
| BVBRC-08-Lplantarum | 6→8 | 8→8 | PARTIAL |  |
| BVBRC-10-Llactis-LL16 | 7→8 | 8→8 | PARTIAL |  |
| BVBRC-11-VREfm-LatAm | 6→8 | 8→8 | PARTIAL |  |
| FFNO-Tsunami | 6→9 | 8→9 | REPLICATED(ext) | pass1 peak nums wrong; corrected 5.20/7.30 |
| lucid-franken-alpha-gamma-rbe | 6→9 | 7→8 | REPLICATED |  |
| lucid-fukui-saga-lq-sldr | 7→9 | 7→9 | PARTIAL-strong |  |
| lucid-globle-photon-killing | 6→8 | 7→8 | REPLICATED |  |
| lucid-hsgc-c5-repair | 5→6 | 7→7 | REPLICATED |  |
| lucid-mariotti-split-dose | 6→7 | 7→7 | PARTIAL |  |
| lucid-pariset-53bp1 | 6→8 | 7→8 | PARTIAL |  |
| lucid-spatiotemporal-dna-damage | 7→9 | 8→9 | REPRODUCED |  |
| lucid-staaf-mixed-beam | 6→8 | 7→8 | PARTIAL |  |
| lucid-stochastic-rejoining | 6→8 | 7→8 | PARTIAL |  |
| lucid100-biochem-dsb-repair-g1s | 6→9 | 7→8 | REPLICATED |  |
| apbs-pb | 7→8 | 8→9 | PARTIAL | caught pass1 error |
| dedalus | 6→8 | 8→8 | EXACT-new-claims |  |
| fast-poisson-spectral | 6→9 | 8→8 | REPRODUCED |  |
| jax-cfd | 7→8 | 8→9 | REPLICATED |  |
| lightning-laplace | 6→8 | 8→8 | REPRODUCED |  |
| modal-space-zhang-2019 | 7→8 | 5→8 | REPLICATED(Ex1) | 2 silent v2 bugs: wrong dist + wrong PDE |
| optimized-schwarz-helmholtz | 7→8 | 8→8 | PARTIAL |  |
| pinn-domain-decomp | 6→8 | 8→8 | PARTIAL |  |
| pwdg-helmholtz | 6→9 | 8→9 | STRONG-REPLICATION |  |
| pyclaw-wave4 | 8→9 | 9→9 | REPLICATED |  |
| walk-on-stars | 6→8 | 8→8 | REPLICATED |  |
| Rasp-2018-Climate | 6→8 | 7→8 | REPLICATED | prognostic CAM data-blocked |
| SOWFA-WindFarm | 7→8 | 8→9 | REPLICATED | OpenFOAM/MPI cluster blocker named |
| space-nanograv-15yr-gwb | 7→8 | 8→8 | PARTIAL |  |
| zhang-spde-deepxde | 6→9 | 4→8 | PARTIAL-strong | WRONG PAPER caught (1905 vs 1809) |
