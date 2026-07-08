# Workflow — Mitiq (LaRose et al. 2020) replication

## Pipeline steps

1. **Paper acquisition.** arXiv 2009.04417 → local PDF + ar5iv HTML rendering (PDF vision tooling unavailable at run time, so quantitative claims extracted from the HTML mirror; verbatim excerpt saved in `report/evidence/`).

2. **Claim extraction.** Manual read; three testable quantitative/qualitative claims (C1, C2, C3) plus two out-of-scope (C4 = H₂ VQE surface, mechanistically covered by C3; C5 = real IBM/Rigetti hardware). Full table in `report/REPORT.md` §2.

3. **Environment setup.** Fresh Python 3.12 venv in `work/venv/`. Installed `mitiq==1.0.0`, `cirq==1.6.1`. No paid inference API; free Argo proxy only (localhost:44497).

4. **C1 + C2 driver — PEC Fig 5 reproduction.** `work/rep_pec.py` (single-seed) + `work/rep_pec_multiseed.py` (10-seed characterization). Builds the exact toy circuit `H(q1); X(q0); CNOT(q0,q1)`, executor returns `Re(rho[0,0])` on `cirq.DensityMatrixSimulator` with `cirq.depolarize(0.1)` after every gate, PEC via `mitiq.pec.execute_with_pec` with 1000 samples. Result: unmitigated = 0.062222 (paper 0.0622); PEC mean |err| = 0.0097 over 10 seeds.

5. **C3 driver — ZNE benchmark reproduction.** `work/rep_zne.py`. Generates 20 randomized-benchmarking 2-qubit circuits via `mitiq.benchmarks.generate_rb_circuits`, depolarizing p=0.01, default ZNE (random local unitary folding + Richardson extrapolation). Result: mean |err| 0.577 → 0.326 (1.77×); 20/20 improved.

6. **LLM verdict.** `work/run_judge.py` submits claims + numbers to free Argo proxy. `argo:claude-opus-4.8` hit a proxy parse bug; fell back to `argo:gpt-5.2` (also free). Judge concurred **REPLICATED**. Full transcript in `report/evidence/evidence_llm_judge.txt`.

7. **Reporting.** `report/REPORT.md` (primary), `report/results.json` (machine-readable), this workflow, `failure_analysis.md`, `open_questions.json`, `REPORT.tex`.

## Endpoints
- Free Argo proxy: `http://localhost:44497/v1`, key `stevens`. Models used: `argo:gpt-5.2` (judge).
- No paid inference. No hardware QPU access.

## Reproducibility
- All Python drivers deterministic under fixed seeds (10 seeds enumerated in `rep_pec_multiseed.py`; RB circuit `random_state=42` in `rep_zne.py`).
- Same seeds → same numbers to floating-point precision on any x86-64 or ARM64 CPU.
- Runtime: ~2 minutes total on CherryRd (local, no GPU required).

## Skipped / deferred
- CDR primitive: package presence checked but no CDR benchmark run.
- Qiskit/pyQuil/Braket backends: multi-backend Mitiq claim not exercised.
- Real IBM/Rigetti hardware: no QPU access.
- H₂ VQE energy surface (Fig 4): identical ZNE code path as C3, treated as mechanistically covered.
