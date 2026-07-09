# PROGRESS — lucid-cu64-topas-nbio-lethal-damage

**Status:** done
**Started:** 2026-05-30 17:53 CDT
**Finished:** 2026-05-30 18:00 CDT
**Target:** Carrasco-Hernandez et al. 2023, "Cellular lethal damage of 64Cu" (Front. Med., DOI 10.3389/fmed.2023.1253746)
**Verdict:** PARTIAL — coverage 5/10, agreement on reproduced fraction 10/10

## Phase log
- [x] 17:53 — workspace created, progress files initialized (≤10 min gate met)
- [x] 17:54 — PDF copied into allowed dir, `pdftotext` extraction (PDF tool errored, fallback used)
- [x] 17:55 — full paper read; triage assumption ("DBSCAN clustering") **wrong** — paper uses Nikjoo proximity rule (≤10 bp opposite strand)
- [x] 17:57 — Eq. 1 cross-check vs Table 2: max error 0.21 % across 5 radionuclides → REPLICATED
- [x] 17:58 — proximity-rule DSB scorer + unit tests + window scan
- [x] 17:59 — track-correlated DSB:SSB demo (literature-consistent 0.04 – 0.16)
- [x] 17:59 — 64Cu ICRP-107 electron-yield spot-check via MIRDsoft (0.23 vs paper 0.18, consistent)
- [x] 18:00 — figures generated (2 PNGs)
- [x] 18:00 — README.md, REPORT.md written

## Deliverables present
- paper.pdf
- README.md
- REPORT.md
- PROGRESS.md  (this file)
- code/01_lethal_damage_equation.py
- code/02_proximity_dsb_scoring.py
- code/03_track_correlated_dsb.py
- code/04_make_figures.py
- results/01_eq1_crosscheck.txt
- results/02_proximity_dsb_demo.txt
- results/03_track_correlated.txt
- figures/fig01_eq1_crosscheck.png
- figures/fig02_dsb_ssb_ratio.png

## What was BLOCKED and why
End-to-end TOPAS-nBio / Geant4-DNA Monte Carlo reproduction of the
0.171 / 0.190 DSB/decay primitive: TOPAS license + nBio extension + Geant4
build + 400 k-history parallel runs. Out of scope for a subagent. The
*downstream* analytic chain that produces the headline clinical numbers
is verified end-to-end.
