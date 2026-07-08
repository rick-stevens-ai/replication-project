# Replication workflow — QC-2101.05513-local-classical-vs-p2-qaoa

Chronological log of the replication actions taken 2026-07-03 on CherryRd.

## Step 0 — Paper acquisition
- Downloaded arXiv:2101.05513 PDF; text extracted with `pdftotext` to `work/paper.txt`.
- Read §1 (headline claims), §2 (QAOA_2 formula), §3 (Threshold algorithm), Appendix A (Table 1: D=2..19 tabulated values), Appendix B (impossibility argument).

## Step 1 — Claim decomposition
- Extracted 7 testable claims (C1–C7 in REPORT.md §2). Marked C1–C5 and C7 as CPU-testable at n≤26; C6 (Modified Threshold_2 via Hastings framework) as out-of-scope.

## Step 2 — Environment
- `python3 -m venv venv && source venv/bin/activate`
- `pip install qiskit==2.5.0 qiskit-aer==0.17.2 networkx==3.6.1 scipy==1.18.0 numpy==2.4.3`
- No external endpoints; all CPU local.

## Step 3 — Threshold algorithm implementation
- `code/threshold_maxcut.py`: n-step threshold flip rule + Monte Carlo estimator (30k trials, SEM ≈ 6·10⁻⁴).
- Verified on Heawood (D=3, n=14, girth=6, built-in networkx). Sweep τ_1, τ_2 ∈ [1..5]².
- Match to paper Table 1 at D=3: within 1σ Monte Carlo error.

## Step 4 — QAOA_2 implementation
- `code/qaoa2_aer.py`: parameterized-circuit statevector on |V| qubits, standard MAX-CUT ansatz. Diagonal-Z objective computed from |ψ|² with precomputed per-edge sign arrays (avoids 2^n × 2^n Pauli matrices).
- COBYLA optimizer, 5–30 uniform-random restarts.
- Ran on Heawood: result 0.75591, matches paper's 0.7559 to 5 digits.

## Step 5 — Independent (4,6)-cage construction
- `code/pg23_incidence.py`: built the projective plane PG(2,3) from scratch (13 points, 13 lines, each line has 4 points via the standard GF(3)² construction). Emitted the Levi bipartite incidence graph (n=26, D=4, girth=6).
- Verified D=4 regularity, girth=6, bipartite via networkx.

## Step 6 — Head-to-head at D=4
- `code/threshold_pg23.py`: Threshold_1, Threshold_2 full sweep on PG(2,3), 30k trials each. Best (τ_1,τ_2)=(3,3) → 0.7083±0.0017.
- `code/qaoa2_pg23_run.py`: 26-qubit QAOA_2 statevector optimization on PG(2,3), 4 seeded COBYLA restarts × 40 iter. Result 0.66773 (within 0.0016 of paper's 0.6693; short-budget shortfall, not deviation).
- Gap = 0.041 in favor of classical, ~25 SEM. Confirms paper's central claim on the (4,6)-cage empirically.

## Step 7 — Evidence bundle
- All JSON in `report/evidence/`: `qaoa2_aer_heawood_v2.json`, `thr_heawood.json`, `thr_pg23.json`, `qaoa2_pg23.json`, plus intermediate smoke files.

## Step 8 — LLM-judge panel
- Ran 3-model Argo panel (Claude Sonnet 4.6, GPT-5.2, Gemini 2.5 Pro) against the report + evidence. Claude Opus 4.7/4.8 returned 502 at time of run.
- Majority: REPLICATED (2/3). Full JSON in `report/evidence/judges.json`.

## Step 9 — Report authoring
- Wrote `report/REPORT.md`; verdict REPLICATED with graph-choice qualifier (§7 addressing bipartite cages).

## Step 10 — Backfill (this pass, 2026-07-05)
- Added: `report/REPORT.tex`, `report/open_questions.json` (5 open Qs), `report/open_questions_section.tex`, `report/workflow.md` (this file), `report/artifacts_summary.md`, `report/failure_analysis.md`, `extraction/nougat.mmd` stub. Verdict preserved: REPLICATED.

## Endpoint accounting
- Argo (`argo:*`) for the 3-judge panel — FREE.
- No paid API used.
