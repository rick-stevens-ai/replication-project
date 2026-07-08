# Replication workflow — QC-1907.11679

Paper: Low, Kliuchnikov, Wiebe (2019), "Well-conditioned multiproduct Hamiltonian simulation," arXiv:1907.11679v2.

## 0. Pre-flight
- Verify Argo free proxy reachable at `http://127.0.0.1:44497/v1` (or via aggregator `http://<tailnet-aggregator>:4000/v1`). Bearer token: `stevens` / any string.
- Python 3.14+, numpy, scipy, matplotlib. `venv` under `work/`.

## 1. Paper harvest
1. `curl -L https://arxiv.org/pdf/1907.11679 -o work/paper.pdf`
2. `sha256sum work/paper.pdf > report/artifact_harvest.md`
3. `pdftotext -layout work/paper.pdf work/paper.txt` — used for reading Appendix A tables into `work/mpf.py` as `fractions.Fraction` entries.

## 2. Claim extraction
- Read pages 1–4 (main text) + 7–9 (Appendix A) manually.
- Enumerate claims C1..C9 (see REPORT §2). Mark testable-locally subset (C1..C6).
- Reject C7 (LCU circuit), C8 (analytic BCH), C9 (large N via sparse/MPS) as out-of-scope for classical dense simulation.

## 3. Independent implementation
- `work/mpf.py`: implement five coefficient constructions from first principles:
  (a) Chin closed-form  (b) Chebyshev real (Eqs. 8–9)
  (c) Chebyshev first-half  (d) rounded-integer (Eq. 10)
  (e) Paper Appendix A Table I (verbatim `Fraction` entries).
- `work/heisenberg.py`: dense 1D Heisenberg chain N=4, PBC, odd/even bond split.
- `work/suzuki.py`: `U2(δ)` and `U4(δ)` (recursion, p=1/(4−4^{1/3})).
- `work/mpf_step.py`: linear combination of powers of `U2` per (k, a).

## 4. Cancellation sanity
`python work/mpf.py` → prints per-family `‖V(k^{-2})a − e1‖_∞` for m=2..6.
Output → `evidence/01_cancellation_sanity.txt`.

## 5. Dynamical benchmark
`python work/benchmark.py` with t=1.0, r ∈ {1,2,3,5,8,12,20,30,50,80,120,200}.
Metric: operator-2-norm error `scipy.linalg.norm(U_approx − expm(−iHt), 2)`.
Output → `evidence/02_benchmark_N4_t1.json`.

## 6. Slope fit
`python work/analyze.py` fits `err ∝ r^{−s}` in clean regime `1e-11 < err < 1e-1`.
Compare fitted slope to expected `2m` per method. Output → `evidence/03_slopes.json`.
Figures → `evidence/fig_convergence.png`, `evidence/fig_condition.png`.

## 7. LLM judge
`python work/judge.py` posts REPORT.md + Claims table + slopes to `argo:gpt-5` via Argo free proxy.
Strict JSON schema: `{verdict: <REPLICATED|PARTIAL|SPOT-CHECK|NO-GO>, confidence: 0–1, justification: str}`.
Raw → `evidence/04_judge_raw.json`; parsed → `evidence/05_judge_verdict.json`.

## 8. Report assembly
- `report/REPORT.md`, `report/REPORT.tex`, `report/open_questions.json`, `report/workflow.md`, `report/artifacts_summary.md`, `report/failure_analysis.md`.
- `extraction/nougat.mmd` (canonical arXiv extraction stub; nougat not invoked locally — source is arXiv HTML/latex).

## 9. Verdict rule (Rick 2026-07-05 headline-exercised)
- If the paper's headline claim was independently implemented + numerically exercised on a real Hamiltonian (not just re-derived symbolically), and matches to within stated tolerance: `REPLICATED`.
- If some headline element was skipped or only qualitatively matched: `PARTIAL`.
- If only spot checks on ancillary tables were done: `SPOT-CHECK`.
- If any headline claim actively contradicted: `NO-GO`.
Here: headline = well-conditioned coefficient construction with $\|a\|_1 = O(\log m)$ vs Chin $e^{\Omega(m)}$. **Independently implemented (Eqs. 8–10 coded from paper), $\|a\|_1$ measured across $2m=4..12$, dichotomy directly observed.** Verdict: `REPLICATED`.

## 10. Provenance
- No external inference APIs beyond Argo free proxy.
- No PDF-parsing LLM calls; Appendix A entered by hand from `pdftotext -layout` output.
- All coefficient checks use `fractions.Fraction` (exact) then converted to `float` only for the dynamical benchmark.
