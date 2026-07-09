# LUCID100 — Slot 25 (Wave 3, rank 56)
## Efficient cell-by-cell simulation of DNA DSBs, chromosome aberrations, and cell survival for low- and high-LET radiation using TOPAS-nBio and MEDRAS (Lim et al. 2026)

- **DOI:** 10.1088/1361-6560/ae6d6d
- **Journal:** Physics in Medicine & Biology, vol. 71, no. 10, art. 105028
- **Published:** 3 June 2026 (open access, CC-BY 4.0)
- **Authors:** Anthony Lim¹², Matthew Andriotty¹, Alexander O'Dell¹, Anna Seppings¹, Greeshma Agasthya¹², Anuj Kapadia², C-K Chris Wang¹ (corresp.)
  - 1. Nuclear & Radiological Engineering and Medical Physics, Georgia Institute of Technology, Atlanta, GA
  - 2. Oak Ridge National Laboratory, Oak Ridge, TN
- **Funding:** DOE-BER LUCID program (UT-Battelle EPKPA71); ORNL LDRD; CADES compute.
- **LUCID slot:** 25 / Wave 3 / rank 56 / candidate_curated → **PARTIAL FIRST PASS COMPLETE**
- **Work folder:** `~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-topas-medras-cellbycell`

## Why this matters for LUCID
This is a methods paper that closes the gap between **TOPAS-nBio track-structure simulation** (initial DNA damage) and **MEDRAS-MC mechanistic repair/misrepair** (DSB rejoining, chromosome aberrations, cell killing) by inserting a **pre-computed Single-Particle-Track Standard DNA Damage (SPT-SDD) library** as a look-up table. The library + Poisson/dose-matching sampler turns a normally HPC-only pipeline into a workstation-tractable one for any dose, dose-rate, particle, or energy spectrum already covered by the library. For LUCID this is directly relevant because:

- Slot 16 (`lucid-medras-mc`) replicated McMahon's MEDRAS-MC mechanism on CherryRd in ~5 min CPU. This paper produces the *input* SDD files MEDRAS-MC consumes.
- Slot 19 (`lucid100-topas-proton-cellular-response`, Zhu 2020) replicated TOPAS-nBio metadata and a parameter-rebuild plan but flagged ~120 k thread-hour cost. This paper's SPT-SDD library exactly *eliminates* that runtime burden for downstream users (one-time library build at the host institution, free sampling thereafter).
- Three in-vitro validation cases cover the LUCID-relevant LET ladder: **280 kVp x-rays (Cornforth 1987)**, **clinical proton SOBP (Marshall 2016)**, and **²³⁸Pu alpha particles (Inkret/Eisen/Raju 1990–1991, Cornforth 2002)**.

## Relation to prior LUCID slots
| Slot | Folder | Status | Relation |
|------|--------|--------|----------|
| 16 | `lucid-medras-mc` | DONE (full replication) | Provides the downstream repair model. This paper consumes its output. |
| 17 (Wave 2 backfill 47) | `lucid100-topas-proton-cellular-response` | PARTIAL | Same TOPAS-nBio + MEDRAS pipeline applied to proton energies; this paper *generalizes* it to e/p/α plus library acceleration. |
| 25 (this work) | `lucid100-topas-medras-cellbycell` | **PARTIAL — framework runnable end-to-end on CherryRd; full library + HPC needed for paper-quality reproduction** | Methods-level acceleration |

## What we have
- **Paper PDF + extracted text** (`artifacts/paper.pdf`, `artifacts/paper.txt`) — 19 pages, open access from IOPscience.
- **Author code** `ahlim3/SPT-SDD-Framework` cloned into `code/SPT-SDD-Framework/` (Python, 1446 files, ~110 MB on disk; includes dummy SDD libraries + phase-space files for all three particles).
- **Smoke-test run** on CherryRd, all three configs, 10 cells each, all green (<1 s per config). See `results/smoke_summary.csv` and `FIRST_PASS_REPORT.md`.
- **Artifact manifest** `ARTIFACT_MANIFEST.md`.

## What we do not have
- **Full pre-computed SPT-SDD libraries** (electron 1 keV–1 MeV, proton 50 keV–100 MeV, alpha 0.1–10 MeV). Authors explicitly excluded these from GitHub ("intentionally excluded due to size and infrastructure constraints", >50 GB).
- **TOPAS-nBio input decks** used to build the library (Geant4-DNA physics list, geometry, exact ∆E binning).
- **HPC submission scripts** (ORNL CADES).
- **Supplementary Data 1** at `https://doi.org/10.1088/1361-6560/ae6d6d/data1` — IOP page is Radware-bot-protected; fetch blocked from CherryRd. **Fetch from a browser session is a 5-second manual step.**

## Reproducibility verdict
- **Framework code:** open source on GitHub, single Python entry point `main_assembler.py`, MIT-style availability (no LICENSE file but explicit "open-source" claim in §Data availability). Runs out-of-the-box with shipped dummy data.
- **Method:** fully described; SDDv2.0 output verified to conform.
- **Numerical re-derivation of paper figures (Figs 8–17):** requires the full SPT-SDD library, the three reference TOPAS phase-space simulations, and end-to-end MEDRAS-MC runs to compute chromosome aberrations / surviving fraction. **Estimated HPC budget:** see `HPC_JOB_PLAN.md` (forthcoming if/when promoted from first-pass).

## Files
- `README.md` (this file)
- `PROGRESS.md` — chronological log
- `ARTIFACT_MANIFEST.md` — every file and where it came from
- `FIRST_PASS_REPORT.md` — verdict
- `artifacts/paper.pdf`, `artifacts/paper.txt`, `artifacts/paper_landing.html`
- `code/SPT-SDD-Framework/` — author code, runnable
- `code/summarize_smoke.py` — our SDD parser / summary
- `results/smoke_summary.csv` — per-cell dose/track/damage from smoke run
- `logs/` — captured stdout from smoke runs

## How to reproduce the smoke test
```bash
cd code/SPT-SDD-Framework
python3 /tmp/smoke_runner.py    # or edit main_assembler.py's __main__ to loop the three configs
python3 ../summarize_smoke.py   # parses Alpha_Simulation/, Proton_Simulation/, Electron_Sim/
```
Total wall time on CherryRd: <2 s. No GPU. No HPC.

## License & ethics
- Paper: CC-BY 4.0.
- Author code: declared open source (no explicit LICENSE file in repo — flagged below as a small open-science nit; safe to use under the author's published "open-source" statement).
- No author contact made. No paid endpoints used.
