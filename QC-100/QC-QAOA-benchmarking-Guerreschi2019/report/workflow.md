# Workflow — QC-100 replication of arXiv:1907.02359 (Willsch et al., QAOA benchmarking)

Slot slug: `QC-QAOA-benchmarking-Guerreschi2019` (queue metadata drift; actual
paper is Willsch 2020, not Guerreschi 2019 — see REPORT.md §1).

## 1. Metadata reconciliation
- Queue TSV row (rank 17) named "QAOA benchmarking Guerreschi 2019".
- Cross-checked arXiv id in the row → `1907.02359` → Willsch, Willsch, Jin,
  De Raedt, Michielsen, "Benchmarking the Quantum Approximate Optimization
  Algorithm", Quantum Inf. Process. 19, 197 (2020).
- Kept the assignment slug, added a note at the top of REPORT.md, and
  replicated the paper actually pointed to by the arXiv id.

## 2. Paper acquisition
- arXiv PDF fetched into `extraction/` (see `extraction/nougat.mmd` stub).
- No author code exists publicly (JUQCS is J\"ulich in-house).

## 3. Claims extraction
- Read the paper; extracted 7 claims (C1..C7), 5 simulator-testable + 2
  hardware-only (see REPORT.md §2).

## 4. Clean-room re-implementation
- `work/qaoa_core.py`: diagonal cost Hamiltonian, elementwise `U_C`,
  per-qubit `U_B` via `np.moveaxis`, metrics M1/M2/M3, analytic Eq. 19.
- `work/run_replication.py`: T1 (C1 exact instances + Eq. 19 check),
  T2 (2-SAT-8A p=1..5 sweep), T3 (16-var MaxCut sweep).
- `work/finish.py`: fast MaxCut p=5 + T3 tau-scan for linear-annealing init.
- Tools: Python 3.14.6, numpy 2.4.3, scipy 1.18.0.
- Compute: local CherryRd CPU, ≤16 qubits, ≤2^16 = 65536 amplitudes.

## 5. Execution
- `python3 work/run_replication.py` → `run.log` + partial `results.json`.
- `python3 work/finish.py` → `finish.log` + completed `results.json`.
- Deterministic seeds throughout; no re-run needed on replay.

## 6. Comparison to paper
- C1 exact instances: E_C0 = -9, -17.7 match Fig. 10/11 to the reported digit.
- C2 Eq. 19: max abs error 4.4e-15 (2-SAT-8A), 6.2e-15 (MaxCut) — machine precision.
- C3 Table 1: p=1 succ 8.84% & r=0.71 match exactly; p=5 succ 41.03% vs
  42.39% (-1.4pp), r=0.844 vs 0.84.
- C4 Fig. 7: p=1 succ 1.45% < 2% ✓; monotone rise through p=5.
- C5 Figs. 10-11 linear-anneal init: 2-SAT p=50 succ 81.24% (paper ~82.7%);
  MaxCut p=10 succ 76.43% (paper ~85.6%).

## 7. LLM-judge (free Argo endpoints only)
- Called `argo:gpt-5.2` and `argo:gpt-5.1` via the local Argo proxy
  (`http://127.0.0.1:44497/v1`, `Bearer stevens`, free per standing rule).
- Both returned REPLICATED with coverage ~8-9/10, agreement ~8-9/10.

## 8. Backfill (2026-07-06)
- Added `report/REPORT.tex`, `report/open_questions.json`,
  `report/open_questions_section.tex`, `report/workflow.md` (this file),
  `report/artifacts_summary.md`, `report/failure_analysis.md`, and
  `extraction/nougat.mmd` stub.
- Called out the queue-metadata drift explicitly (Guerreschi vs Willsch)
  in both REPORT.tex and failure_analysis.md rather than hiding it.

## 9. Verdict
REPLICATED (simulator core, headline-exercised). Hardware claims (C6, C7)
out of scope. The Guerreschi & Matsuura "several-hundred-qubit crossover"
framing in the subagent brief is NOT the paper actually in this slot and
was NOT exercised — flagged in failure_analysis.md.
