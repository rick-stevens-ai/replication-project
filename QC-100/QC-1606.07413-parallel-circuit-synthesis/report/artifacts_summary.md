# Artifacts Summary — QC-1606.07413

## Code (`code/`)
- `verify_toffoli_tcount.py` — Constructs the 5 named 3-qubit circuits (Toffoli, Fredkin, Peres, Quantum OR, Negated Toffoli) as explicit Clifford+T decompositions; counts T/T† gates by scanning `qc.data`; verifies each computed `Operator(qc)` matches the truth-table target unitary up to global phase (tol 1e-6). Writes pass/fail table to `report/evidence/tcount_verification.json`.
- `verify_adder_tcount.py` — Builds the 4-qubit 1-bit full-adder unitary from its truth table; asserts unitarity; constructs a 3-Toffoli + 2-CNOT reversible implementation; verifies it matches the target unitary; measures naive T-count after `decompose(['ccx'])` = 21; records the paper's optimum T-count=7 (accepted via affine-Toffoli equivalence, Sec 5.3). Writes `report/evidence/adder_tcount.json`.
- `parallel_synthesis_speedup.py` — Random length-6 target over a 10-gate 2-qubit Clifford+T library (10^6-candidate space). Sequential linear scan vs `multiprocessing.Pool(N).imap_unordered` first-finder-wins over N contiguous chunks. 6 seeded trials, N ∈ {1,2,4,8}, wall time via `time.perf_counter()`. Writes `report/evidence/parallel_speedup.json`.

## Evidence (`report/evidence/`)
- `tcount_verification.json` — 5 rows: {circuit, paper_tcount, measured_tcount, unitary_correct, match}. All 5 rows are pass.
- `adder_tcount.json` — Adder unitary residual (0.00e+00), naive T-count (21), paper optimum (7), consistency verdict.
- `parallel_speedup.json` — Per-trial (target seed, sequential wall, parallel wall for N∈{1,2,4,8}) + aggregate (mean, std, mean speedup vs sequential).
- `environment.txt` — python 3.14.6 / qiskit 2.5.0 / numpy 2.5.0 / macOS-26.3-x86_64 / cpu_count 20.

## Logs (`logs/`)
- `parallel_speedup_run2.log` — full stdout of the benchmark run (per-trial timings + aggregate table).

## Report (`report/`)
- `REPORT.md` — canonical narrative report (2026-07-03).
- `REPORT.tex` — LaTeX conversion with critique section (2026-07-06 backfill).
- `open_questions.json` — 5 open questions with basis + concrete next steps.
- `open_questions_section.tex` — LaTeX version of the 5 open questions.
- `workflow.md` — end-to-end workflow to reproduce this replication.
- `artifacts_summary.md` — this file.
- `failure_analysis.md` — honest critique of what the "REPLICATED" verdict does and does not cover.

## Working files (`work/`)
- `paper.pdf` — Di Matteo & Mosca 2016 arXiv preprint.
- `paper.txt` — pdftotext extraction (native text PDF; no OCR needed).

## Extraction (`extraction/`)
- `nougat.mmd` — stub / placeholder. Paper is a native text PDF; pdftotext gave clean output, so no nougat OCR pass was needed. Stub is present for artifact-slot uniformity across the QC-100 wave.

## What is NOT here
- No pQCS binary or C++/MPI/OpenMP source (the paper's reference implementation is HPC-oriented and out of scope for a laptop replication).
- No BG/Q or MPI-cluster runs; C5 (architecture ratio) and C6 (26s-mean on 4096 cores) not reproduced.
- No independent optimal-T-count search for the 4-qubit adder; C3's optimum is accepted on paper authority.
