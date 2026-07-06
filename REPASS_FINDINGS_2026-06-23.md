# Re-pass Master — 2026-06-23

**46 papers re-passed** (coverage-lift pass on the prior REPLICATE-PROJECT corpus).
Each got PARSER_PROVENANCE.md; original report preserved as REPORT.pass1.md.

## Scores (re-pass final)

| Paper | Cov | Agr | Verdict | Parser |
|---|---|---|---|---|
| 1412756-Chiral-Spin-Order-in-Kondo-Heisenberg-systems | 9 | 9 | PARTIAL | pdftotext |
| 1461824-APPROXIMATING-PHOTO-Z-PDFS-FOR-LARGE-SURVEYS | 8 | 8 | PARTIAL | pdftotext |
| 1523841-Quantitative-relationship-between-polarization-differences-a | 6 | 8 | REPRODUCED-WITH-CAVEATS | pdftotext |
| 1559043-ignition-kernel-turbulent | 9 | 9 | PARTIAL | OCR |
| 1997354-Integer-Sequences-from-Configurations-in-the | 9 | 10 | PARTIAL | pdftotext |
| 2217719-SCALE-depletion-capabilities-for-molten-salt | 8 | 8 | REPRODUCED | pdftotext |
| 2587225-ScaWL-Scaling-k-WL-Weisfeiler-Lehman-Algorithms-in | 7 | 8 | PARTIAL | pdftotext |
| 26392213-Outer-mucus-niche | 2 | 11 | MOSTLY REPLICATED | pdftotext |
| 28589945-ARG-dissemination | 7 | 8 | REPLICATED | none |
| 29769716-Mutant-phenotypes-bacterial-genes | 9 | 9 | REPLICATED | recorded |
| 3003857-DIVIDE-AND-CONQUER-CHAOTIC | 8 | 5 | Tier B | pdftotext |
| 3014512-Spin-dependent-scattering-of-sub-GeV-dark-matter | 7 | 8 | ? | pdftotext |
| apbs-pb | 8 | 9 | PARTIAL | recorded |
| BVBRC-02-Ralstonia-Fluit2021 | 8 | 8 | PARTIAL | pdftotext |
| BVBRC-04-Variovorax-trehalose-Shrestha2022 | 9 | 9 | REPLICATED | pdftotext |
| BVBRC-05-Trueperella-pyogenes-Thakur2022 | 8 | 8 | REPLICATED | pdftotext |
| BVBRC-07-Sherry-AMR-workflow-2023 | 100 | ? | REPLICATED | recorded |
| BVBRC-08-Lplantarum-DJF10-Kandasamy2022 | 28 | 8 | PARTIAL | pdftotext |
| BVBRC-10-Llactis-LL16-Mileriene2023 | 8 | 9 | VERIFIED / PARTIAL / NOT | recorded |
| BVBRC-11-VREfm-LatAm-Rios2020 | ? | ? | SPOT-CHECK REPLICATED | pdftotext |
| dedalus | 8 | 8 | ? | pdftotext |
| fast-poisson-spectral | 9 | 8 | ? | pdftotext |
| FFNO-Tsunami-Makarynskyy2026 | 6 | 8 | REPLICATED | pdftotext |
| jax-cfd | 5 | 9 | REPLICATED | pdftotext |
| lightning-laplace | ? | 8 | REPRODUCED | pdftotext |
| lucid-franken-alpha-gamma-rbe | 6 | 11 | REPLICATED | pdftotext |
| lucid-fukui-saga-lq-sldr-aldh | 9 | 9 | PARTIAL | pdftotext |
| lucid-globle-photon-cell-killing | 7 | 8 | REPLICATED | pdftotext |
| lucid-hsgc-c5-repair-performance | 6 | 7 | PASS | pdftotext |
| lucid-mariotti-split-dose-gamma-h2ax | 7 | 7 | PARTIAL | pdftotext |
| lucid-pariset-53bp1-mouse-strains | 8 | 8 | PARTIAL replication | pdftotext |
| lucid-spatiotemporal-early-dna-damage | 9 | 9 | REPRODUCED | pdftotext |
| lucid-staaf-mixed-beam-gamma-h2ax | 9 | 1 | PARTIAL | pdftotext |
| lucid-stochastic-rejoining | 13 | ? | PARTIAL | Marker |
| lucid100-biochemical-dsb-repair-g1-s | 9 | 8 | REPLICATED | pdftotext |
| modal-space-stochastic-zhang-2019 | 8 | 8 | PARTIAL | pdftotext |
| optimized-schwarz-helmholtz | ? | ? | ? | pdftotext |
| pinn-domain-decomp-2023 | ? | ? | PARTIAL | none |
| pwdg-helmholtz | 9 | 9 | STRONG REPLICATION | pdftotext |
| pyclaw-wave4 | 9 | 9 | REPLICATED | pdftotext |
| Rasp-2018-Climate | 8 | 8 | REPLICATED | pdftotext |
| repass_paper | ? | ? | NO-REPORT | pdftotext |
| SOWFA-WindFarm | 8 | 9 | REPLICATED | none |
| space-nanograv-15yr-gwb | 9 | 0 | REPLICATED for everything the public rel | pdftotext |
| walk-on-stars | 8 | ? | ? | pdftotext |
| zhang-spde-deepxde | 9 | 4 | PARTIAL | pdftotext |

## Provenance
- Papers with parser provenance recorded: **43/46**

## Headline integrity catches (manually curated — verify against reports)
- **zhang-spde**: pass-1 replicated the WRONG Zhang paper (1905.01205 vs cited 1809.08327). Re-pass fixed identity → 9/11 cov, 78% agr.
- **modal-space**: two silent v2 setup bugs (wrong distribution params on Ex1, wrong PDE on Ex3); corrected Ex1 now beats the paper → REPLICATED.
- **BVBRC-07**: 26 'missed' genes were an AMRFinder --organism flag mismatch, not a real gap; 15 acquired AMR genes match exactly.
- **divide-conquer-chaotic**: quantified Lorenz gradient explosion 1.6e13×; fixed KS stability; ERA5 honestly reclassified as data-blocked.
- **SCALE-molten-salt**: caught a Table-1 element-label swap; named RSICC-gated SCALE 6.3 blocker.
- **mutant-phenotypes**: 17 claims confirmed EXACT vs deposited tables; named 84GB R-image blocker.
- **nanograv-15yr**: reproduced headline GWB detection significances exactly (p=7.85e-4 vs 1e-3; OS S/N p=4.75e-5 vs 5e-5).
- **Variovorax**: caught a coordinate typo in the original paper.
