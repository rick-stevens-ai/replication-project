# PROGRESS — LUCID Medras-MC Replication

**Target paper:** McMahon & Prise (2021), *A Mechanistic DNA Repair and Survival Model (Medras): Applications to Intrinsic Radiosensitivity, RBE and Dose-Rate.* Front. Oncol. 11:689112. DOI: 10.3389/fonc.2021.689112.

**Local PDF:** `mcmahon_prise_2021.pdf` (copied from `~/Dropbox/XFER/LUCID-replication-targets/ee7df40d975b967007190d62a4ad035c4db64ee2.pdf`)

**Public repo:** https://github.com/sjmcmahon/Medras-MC (cloned at `Medras-MC/`, commit `0e51be7`)

**License:** BSD-2-Clause (per-file headers — no top-level LICENSE file). ✅ Open.

**Data:** Radial-energy `.xlsx` tables for H/He/C/N ions ship in `damagegenerator/`. SDD v1.0 (Schuemann 2019) used for exchange. ✅ Open.

## Phases

- [x] Workspace dir created at `~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid-medras-mc/`
- [x] Repo cloned; readme + license + structure verified
- [x] PROGRESS.md scaffolded (within 10-min window)
- [x] Skim paper for claims to target (Frontiers HTML methods + local pdftotext for Table 2)
- [x] Python env verified (numpy 2.4.3, scipy 1.17.1, openpyxl 3.1.5, matplotlib 3.10.8)
- [x] Run `damagegenerator.basicXandIon(runs=20)` — 23 SDD files in 114 s
- [x] Run `repairanalysis.medrasrepair.repairSimulation(..., 'Fidelity')` — 144 s
- [x] Parse log, extract misrepair-vs-LET / vs-dose / kinetics, dump CSV
- [x] Three figures generated
- [x] REPORT.md with claim-by-claim table, agreement score, friction tags
- [x] README.md
- [x] Progress JSON updated

## Status: COMPLETE

**Headline result:** All 7 targeted mechanistic claims reproduce qualitatively;
the two quantitative-test claims (DSB yield 33 vs 35 per Gy; complex fraction
0.43±0.02 → 0.42 grand mean) reproduce within paper-stated uncertainty.

**Compute:** 4–5 min wall on CPU. No GPU, no network beyond initial `git clone`.

**Friction tags:** `license-without-LICENSE-file`, `no-pinned-deps`,
`deterministic-seed-not-exposed`, `scope-mismatch` (paper figs 4–7 need
external Paganetti/PIDE survival data), `kinetics-column-not-self-described`,
`registration-required-dataset` (PIDE 3.4 is registration-gated at GSI —
probed 2026-05-28; no anonymous mirror; access requires institutional-email
request).

See `REPORT.md` for the full claim-by-claim replication report.
