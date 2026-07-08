# Workflow — QC-2203.04340 Parity QAOA Replication

## 1. Paper acquisition
- arXiv 2203.04340 PDF fetched to `work/2203.04340.pdf`.
- `pdftotext` dump to `work/2203.04340.txt` for grep-friendly reference.

## 2. Claim extraction (headline-exercised rule)
- Identified 5 claims (C1-C5) in Sec. V / Fig. 7 of the paper.
- Marked C1-C3 as **testable-in-15-min-noiseless-sim** (the actual
  headline of the plot's y-intercept).
- Marked C4 as **structural** (verifiable by counting driver-line
  lengths, not by numerical simulation).
- Marked C5 as **out of scope** (requires a per-gate noise model
  in Aer; skipped to keep the simulator dependency-free).

## 3. Environment
- Python 3.14.6 on CherryRd (Darwin 25.3.0).
- venv with numpy 2.5.0, scipy 1.18.0, networkx 3.6.1. No Qiskit.

## 4. Simulator design (`code/parity_qaoa.py`, ~600 LoC)
- Instance generation: `J_ij ~ U[-1,1]` on K_6 complete graph, 15 couplings.
- Parity code space: enumerate the 2^{N-1}=32 CF states via GF(2) map
  `b_i -> (b_i XOR b_j)_{i<j}`.
- Diagonal-basis evolution for H_Z and H_C (both diagonal in Z basis).
- Multi-qubit-X propagator via `cos(β) I - i sin(β) P` on qubit-mask
  permutation.
- Three QAOA protocols: `qaoa_explicit`, `qaoa_implicit`, `qaoa_hybrid`.
- Optimiser: paper's stochastic accept-if-improves (8 starts × 150 moves
  per start per instance).

## 5. Sanity checks (all PASS before production run)
- `|H_CF| = 32 = 2^{N-1}`.
- `max(H_C on CF) = 0.0`.
- `H_Z(cf_state)` matches logical Ising energy on all 32 CF states.
- All 5 implicit driver lines preserve the CF subspace.

## 6. Production run
```bash
cd code && source ../venv/bin/activate
python parity_qaoa.py --N 6 --p 3 --instances 24 \
       --n_starts 8 --n_moves 150 --seed 2026 \
       > ../logs/full_run.log 2>&1
```
- 24 random instances (paper uses 96; medians already tight at 24).
- Wall time ~21 min on one CherryRd CPU core.
- Output: `report/evidence/results.json`.

## 7. Cross-check against Fig. 7
- Read off Fig. 7 y-axis markers by eye (paper's Fig. 7 uses log-y).
- All four `nr` values fall inside the plotted intervals.
- Monotone ordering `Eres[0.0] < Eres[0.4] < Eres[0.6] < Eres[1.0]`
  holds on every single one of 24 instances (not just the median).

## 8. Standard-QAOA baseline
- Same problem, unencoded, standard X-driver at p=3.
- Median Eres = 0.260 vs 0.031 for implicit parity QAOA — confirms C3.

## 9. Verdict
- REPLICATED for C1, C2, C3, C4 (structural).
- C5 (noise scan) not attempted — listed as open question #2.

## 10. Backfill (this pass, 2026-07-06)
- Original REPORT.md preserved unchanged.
- Added: REPORT.tex, open_questions.json (bare list of 5),
  open_questions_section.tex, workflow.md, artifacts_summary.md,
  failure_analysis.md, extraction/nougat.mmd stub.
- Simulator, logs, evidence JSON, venv unchanged.
