# PROGRESS — LUCID100 slot 65 (MS-GSM² UHDR cell survival)

## Task
LUCID100 max-rate backfill slot 65 (Wave 4): first-pass artifact harvest +
replication scoping + minimal runnable smoke for Battestini et al. 2024,
*A multiscale radiation biophysical stochastic model describing the cell
survival response at ultra-high dose rate* (arXiv:2412.16322).

## Status: GO (smoke complete, mechanism reproduced)

## Timeline (2026-06-09, all CDT)
- 13:47 — task received
- 13:47 — verified TSV row (slot 65 of LUCID100_SOLID_MASTER_QA.tsv)
- 13:48 — bibliographic ID verified via Semantic Scholar; resolved to
          arXiv:2412.16322v1, Battestini/Missiaggia/Bolzoni/Cordoni/Scifoni 2024
- 13:48 — fetched arxiv PDF (4.1 MB), text-extracted with pdftotext
- 13:49 — fetched arxiv source tarball (2.5 MB), extracted LaTeX with
          full Table TAB:chempar, Table TAB:biorates, and Algorithm MS-GSM²
- 13:49 — confirmed NO public code repo (searched fcordoni, Battestini,
          2MaBa, MS-GSM2, GSM2-microdosimetric); paper states "Julia, no repo"
- 13:50 — checked existing related LUCID replications: slot 27 (Cordoni
          Entropy 2023) is already REPLICATED — same X/Y/a/b/r Markov core
- 13:51 — drafted `code/smoke_ms_gsm2.py` (Python/SciPy port of chem ODE +
          GSM² SSA)
- 13:51 — first run: mean-field GSM² gave unphysical SF > 1 → switched to
          true Gillespie SSA on integer X
- 13:52 — second run: chem ODE went negative at low O₂ → switched to BDF
          stiff solver + non-negative clamp in RHS
- 13:53 — third run: physical SF curves, FLASH ratio > 1 at expected
          regime; smoke PASSES
- 13:54 — generated artifact manifest with SHA-256 hashes
- 13:54 — wrote README.md, PROGRESS.md, FIRST_PASS_REPORT.md

## Artifacts produced
- `refs/arxiv-2412.16322.pdf`, `.txt`, `-src.tar.gz` + extracted source
- `code/smoke_ms_gsm2.py` (Python smoke implementation)
- `results/smoke_results.csv`, `smoke_results.png`, `smoke_chem_trace.csv`
- `artifacts/MANIFEST.md` (SHA-256 of all artifacts)
- `reports/FIRST_PASS_REPORT.md`, `reports/REPORT.md` (copy)
- `README.md`, `PROGRESS.md`

## Blockers
- None for smoke replication.
- Bit-exact comparison blocked by: (a) closed Julia source, (b) authors'
  raw clonogenic data not released, (c) TRAX-CHEM microdosimetric spectra
  not bundled.

## Next actions / recommendations
1. Update LUCID100_SOLID_MASTER_QA.tsv slot 65:
   - DOI cell → `arXiv:2412.16322` (paper has no journal DOI yet)
   - Venue cell → `arXiv:2412.16322 [physics.bio-ph] (preprint)`
   - Status → `smoke_only_go`
   - Notes → "smoke-only mechanism replication; SF curves + FLASH ratio
     qualitatively reproduced from open paper parameters; bit-exact blocked
     by closed Julia + unreleased raw data"
2. (Optional) If/when Battestini publishes the Julia code, port + bit-exact
   compare on the Adrian2020 DU145 dataset.
3. (Optional) Cross-link slot 65 ↔ slot 27 (Cordoni 2023 Entropy) in the
   master TSV — they share the GSM² biological core.
