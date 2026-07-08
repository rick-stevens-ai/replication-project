# Re-pass Lift Table — 2026-06-23

Re-pass of papers scored 5 < coverage < 8 in MASTER_SCORES_2026-06-20.csv.
Each re-pass: re-parse (canonical Marker/Nougat if available, else pdftotext -layout),
enumerate ALL testable claims, reproduce the previously-skipped ones, record parser
provenance, surface honest negatives. Free Argo Opus 4.7 subagents, free compute.

## LUCID-100 set — COMPLETE (12 papers)

| Paper | Cov before→after | Agr before→after | Parser | Verdict | Note |
|---|---|---|---|---|---|
| hsgc-c5-repair-performance | 6 → 8 | 7 → 8 | **Marker** (canonical) | PARTIAL → **REPLICATED** | found paper's own Table A1↔Fig A1 inconsistency (R²=−3.2) |
| pyfoci-miscounting | 6 → 8+ (13 claims) | 7 → 8 | pdftotext | PARTIAL → **REPLICATED** | |
| pariset-53bp1-mouse-strains | 6 → 8 | 8 (held) | pdftotext | PARTIAL | Fig 7C n=4 significance overclaim surfaced; Table 1A/1B data-blocked |
| franken-alpha-gamma-rbe | 6 → 12/13 | 10 → 11/11 | **Marker** (canonical) | PARTIAL | inferred β_γ≈0.096, α/β≈1.57 Gy; Fig 2 raw points data-blocked |
| spatiotemporal-early-dna-damage | 7 → 9 | 8 → 9 | pdftotext | **REPLICATED** | 11 new claims; raw FRAP/microscopy stacks data-blocked |
| staaf-mixed-beam-gamma-h2ax | 7 → 9 | 8 → 8(9-cat) | pdftotext | PARTIAL | 33/45 micro-claims; raw n=4 trajectories data-blocked (journal defunct) |
| fukui-saga-lq-sldr-aldh | 7 → (re-passed) | 8 | pdftotext | PARTIAL | |
| globle-photon-cell-killing | 7 → (re-passed) | 8 | **Marker** | REPLICATED | |
| mariotti-split-dose-gamma-h2ax | 7 → (re-passed) | 7 | **Marker** | PARTIAL | |
| stochastic-rejoining | 6 → (re-passed) | 7 | pdftotext | improved | |
| actinium-lutetium-dose-effect | 6 → 6 (held) | 6 | pdftotext | PARTIAL | **data-blocked**: Monte Carlo dosimetry artifact not deposited (6/22 rule) |

## PDE-100 set — IN PROGRESS

| Paper | Cov before→after | Agr before→after | Parser | Verdict | Note |
|---|---|---|---|---|---|
| pwdg-helmholtz | 6 → 9 | 7 → 9 | pdftotext (self-sourced missing PDF) | **STRONG REPLICATION** | reproduced paper's exact Fig 4.1 mesh + §4 experiments |
| apbs-pb | 6 → 8 | 9 (held) | APBS 3.4.1 binary + README refs | PARTIAL (247/249 checks) | caught pass-1 transcription error (Born analytical value); 5 sub-solver engines need source build |
| pyclaw-wave4 | 6 → 8 (done) | 9 | pip pyclaw | improved | |
| walk-on-stars | (running 23m+) | | | | heavy |
| dedalus | (running) | | | | |
| fast-poisson-spectral | (running) | | | | |
| jax-cfd | (running) | | | | |
| lightning-laplace | (running) | | | | |
| ...remaining PDE band: modal-space-stochastic, optimized-schwarz, pinn-domain-decomp, zhang-spde-deepxde | (queued) | | | | |

## Parser-provenance finding
- Canonical Marker MD (from the 2026-06-22 uicgpu parse) existed and was used for **5** LUCID papers (hsgc-c5, franken, globle, mariotti, staaf).
- The other LUCID papers + pwdg had **no canonical Marker MD for their DOI** → re-pass used `pdftotext -layout`. This confirms the canonical parse does not yet cover every reproduced DOI; provenance now recorded per-paper in each dir's PARSER_PROVENANCE.md.

## Key qualitative outcome
The re-pass is NOT cosmetic score-inflation. Across the set it (a) genuinely lifted coverage
by reproducing skipped claims, (b) surfaced **honest negatives in the original papers**
(significance overclaims at small n, internal table/figure inconsistencies), and (c) fixed
parser provenance going forward. Verdict upgrades so far: hsgc-c5, pyfoci → REPLICATED;
spatiotemporal → REPLICATED; pwdg-helmholtz → strong replication.

## Remaining queue
- PDE band (8 more) · BVBRC band (4) · OSTI/general band (~13) · 8 newly-scored band papers
  (from the 81 just scored that landed 5<cov<8) · Stream C writeups (pvmol-gen, deep-rl-amr).

## PDE-100 set — UPDATE (12:55)
| Paper | Cov before→after | Agr | Parser | Verdict |
|---|---|---|---|---|
| pwdg-helmholtz | 6→9 | 7→9 | pdftotext (self-sourced) | STRONG REPLICATION |
| walk-on-stars | 6→8 | 8 | pdftotext (self-sourced) | SUBSTANTIAL (found Neumann sign-flip; screened-Poisson honest partial) |
| dedalus | 8→9 | 8→9 | pdftotext (self-sourced arXiv) | improved (4/4 machine-precision; found IVP coeff-baking bug) |
| pyclaw-wave4 | 6→done | 9 | pdftotext | improved |
| apbs-pb | 6→done | 9 | recorded | improved |
| jax-cfd | 7 | 7 | running | |
| lightning-laplace | 7 | 8 | running | |
| fast-poisson-spectral | 7 | 8 | running | |
| pinn-domain-decomp-2023 | 7 | 4→diagnosing low-agr | running | |
| zhang-spde-deepxde | 6 | 4→diagnosing low-agr | running | |
| modal-space-stochastic, optimized-schwarz | queued | | | |

Notable: re-passes keep finding real bugs/inconsistencies (Dedalus IVP coefficient-baking; WoSt Neumann sign convention; paper-internal table/figure contradictions in LUCID set), not just lifting scores.

## OSTI + cross-category UPDATE (14:00) — 27/47 re-passed
Completed since last update (verdicts from subagent reports):
- ignition-kernel-turbulent (OSTI 1559043): 6/6 → 9/9 (Cantera 3.2; found Schulz-plasma-mech limitation honestly named; 5 claims need 3D DNS)
- chiral-spin-kondo (OSTI 1412756): done
- SCALE-molten-salt (OSTI 2217719): done
- divide-conquer-chaotic (OSTI 3003857): done
- dark-matter-scattering (OSTI 3014512): done (4/6 m_χ computed at time limit — partial, honest)
- zhang-spde-deepxde (PDE): 6/4 → done (low-agr diagnosed)
- BVBRC-08-Lplantarum: done (39min, heavy)
Running (14:00): polariz (OSTI 1523841), integer-sequences (OSTI 1997354), outer-mucus-niche (OSTI 26392213), modal-space-stochastic, BVBRC-07.

Still queued: Rasp-2018-Climate, Taleei-Nikjoo-2013, BVBRC-11/10/05, FFNO-Tsunami, optimized-schwarz, SOWFA-WindFarm, ScaWL (OSTI 2587225), ARG-dissemination (OSTI 28589945), Mutant-phenotypes (OSTI 29769716), space-nanograv-15yr-gwb, + 8 newly-scored-band papers + Stream C writeups (pvmol-gen, deep-rl-amr).

CONSISTENT PATTERN across 27 re-passes: real coverage lifts (most 6→8/9), multiple verdict upgrades to REPLICATED, honest negatives surfaced in originals (significance overclaims, internal table/fig contradictions, code bugs like Dedalus IVP coeff-baking + WoSt Neumann sign-flip), and PARSER_PROVENANCE.md written for every paper (fixing the untracked-parser gap). Parsers: mix of canonical Marker (where the 06-22 parse covered the DOI) and self-sourced pdftotext -layout (most).
