# Workflow — QC-2206.12780 (Gidney pair-measurement pentagon surface code)

## 0. Framing
- Paper: arXiv:2206.12780 → Quantum 7, 1156 (2023), DOI 10.22331/q-2023-10-25-1156.
- Headline exercised: `pentagonal_sharp` LER < `chao` LER at matched (d, p).
- Set: QC-100. Wave: 2026-07-03 Ollie subagent.
- Free-endpoint constraint: honored. All compute local CPU on CherryRd; no paid LLM inference for numerical results.

## 1. Materials acquired
- Paper PDF + text → `work/paper.pdf`, `work/paper.txt`.
- Zenodo 6626417:
  - `work/circuits/` — 720 Stim circuit files (family × distance × error-rate).
  - `work/stats.csv` — paper's per-shot Monte-Carlo LERs (from Fowler correlated MWPM), 720 rows.
- Downloaded 2026-07-03 from official DOI/arXiv/Zenodo links.

## 2. Environment
- Host: CherryRd (macOS).
- Python 3 venv `.venv/` created in dir root.
- Packages installed via `pip`: `stim==1.16.0`, `pymatching==2.4.0`, `numpy==2.5.0`.
- Decoder choice: uncorrelated MWPM (`pymatching`) — strictly weaker than paper's correlated MWPM; deliberately independent implementation.

## 3. Scripts
- `code/replicate.py` — Experiment A. Stim built-in `surface_code:rotated_memory_x`, d∈{3,5,7}, 10 rounds, 20k shots/point, uniform depolarizing p in log grid across 0.001–0.022. Fits threshold-crossing by d-scaling.
- `code/replicate_pentagon.py` — Experiment B. Iterates over `c ∈ {chao, pentagonal_sharp, honeycomb}`, `d ∈ {5,7}`, `p ∈ {0.001..0.007}`. For each cell: load Stim circuit → build DEM → hand to pymatching → sample 20k shots → decode → cross-reference `stats.csv` row.

## 4. Execution
1. `python3 -m venv .venv && source .venv/bin/activate`
2. `pip install stim pymatching numpy`
3. `python code/replicate.py` → `report/evidence/threshold_sweep.json`, `report/evidence/summary.json`, `report/evidence/run.log`.
4. `python code/replicate_pentagon.py` → `report/evidence/pentagon_vs_chao.json` (36 rows), `report/evidence/pentagon_run.log`.
5. Total wall time: ~50 s.

## 5. Analysis
- Experiment A: threshold crossing at p ≈ 0.010 (canonical ~1% MWPM threshold for rotated surface code).
- Experiment B: at all 12 head-to-head (d, p) points, pentagon LER < chao LER. Ratio pentagon/chao ∈ [0.25, 0.90], smaller at low p, growing as p → threshold.
- Absolute LER agreement with paper: within ~1.1–2× across the grid, gap widening at low p — exactly the correlated-vs-uncorrelated MWPM signature.

## 6. Verdict decision
- Headline ordering: 12/12 = pass.
- Absolute LERs: within decoder-gap tolerance.
- Baseline sanity check: canonical ~1% threshold recovered.
- Not tested: numeric thresholds (C1 numeric), teraquop footprint (C2), low-p crossover (C3).
- Verdict: **REPLICATED** on ordering headline. Numeric threshold + teraquop numbers are explicitly outside the exercised claim.

## 7. Deliverables
- `report/REPORT.md` (canonical narrative — pre-existing).
- `report/REPORT.tex` (LaTeX rebuild with honest Critique section).
- `report/open_questions.json`, `report/open_questions_section.tex` (5 questions with concrete probes).
- `report/workflow.md`, `report/artifacts_summary.md`, `report/failure_analysis.md` (this backfill).
- `extraction/nougat.mmd` (stub — paper is heavily formula-driven; native LaTeX/PDF was the primary source, so MMD extraction was skipped in the original run).

## 8. Reproduction contract
Anyone with `stim + pymatching + numpy` and network access to Zenodo 6626417 can, in <10 minutes on a laptop:
1. clone this dir,
2. run the two scripts,
3. observe (a) pentagon-<-chao at all 12 points, (b) baseline ~1% threshold.

That is the reproduction contract. Everything else is out of scope for this window and belongs to the Open Questions list.
