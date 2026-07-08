# Workflow — arXiv:1803.03621 replication

## Environment
- macOS on m1 (Apple Silicon), Python 3.14.6 in local `.venv`
- numpy 2.5.0, scipy 1.18.0, matplotlib (pip latest)
- CPU only, no GPU. No external quantum libraries (qiskit, cirq, stim).

## Steps

1. **Fetch paper.**
   ```bash
   curl -sL https://arxiv.org/pdf/1803.03621 -o work/1803.03621.pdf
   pdftotext -layout work/1803.03621.pdf work/1803.03621.txt
   ```

2. **Implement monomial-unitary group.**
   - File: `work/monomial_rb.py`
   - `Monomial` dataclass: `(perm: int[d], phases: complex[d])`
   - Methods: `to_matrix()`, `__matmul__` (composition), `inverse()`, `sample_monomial(d, n, rng)`
   - Verify composition-vs-dense agreement on 20 random pairs to <1e-14.

3. **Implement noise channels.**
   - MU case: `T(ρ) = p·ρ + (1-p)·σ`, σ ~ HS-uniform via Ginibre.
   - Clifford case: `T(ρ) = p·ρ + (1-p)·U ρ U†`, U Haar-random.
   - Analytic ground-truth fidelities:
     - MU: `F_true = (p(d-1) + 1) / d`
     - Clifford: `F_true = p + (1-p)(|Tr U|² + d)/(d(d+1))`

4. **RB estimator.**
   - Sequence lengths `m` in grid.
   - For each m: draw M sequences, compute composite inverse, simulate ρ under noisy composite, read P(0).
   - Fit `A + B·f^m` via `scipy.optimize.curve_fit` with bounds.
   - Convert f → F̂ via analytic map.

5. **Table 1 replication.**
   - `python work/monomial_rb.py`
   - Config: d ∈ {4, 8, 16}, M ∈ {50, 200}, n=8, p=0.9, 20 σ/cell
   - m-list: [1, 2, 4, 8, 12, 20, 30, 40, 60, 80]
   - Output: `report/evidence/results_monomial.json`, log to `report/evidence/monomial_run.log`
   - Wall time: ~150s.

6. **Table 3 replication.**
   - `python work/clifford_generator_rb.py`
   - Config: n=2, gate set A = {H_i, S_i, S_i^{-1}, CNOT_{ij}} (|A|=8)
   - (p, b, M) ∈ {(0.99, 8, 40), (0.98, 8, 40), (0.95, 8, 40)}
   - 10 random U per config, m-list [1..40]
   - Output: `report/evidence/results_clifford.json`
   - Wall time: ~7s.

7. **Three-protocol comparison (Fig 1).**
   - `python work/compare_protocols.py`
   - MU(4, 8), p=0.95, M=60, 10 σ
   - P1: full-Haar; P2: 11-gen b=3; P3: 11-gen b=15
   - Output: `report/evidence/results_compare.json`
   - Wall time: ~18s.

8. **Plots.**
   - `python work/plot_results.py`
   - Outputs: `rb_three_protocols.png`, `monomial_error_vs_d.png`

9. **LLM judge.**
   - `python work/judge.py` (adapted to `argo:gpt-5.2` after Opus responses hit an Argo validator bug)
   - Prompt: claims table + results tables + verdict vocab
   - Output: `report/evidence/llm_judge_verdict.md`
   - Endpoint: Argo `:44497` (free)

10. **Reporting.**
    - Hand-write `report/REPORT.md` interpreting each claim.
    - This backfill pass (2026-07-05): compile `report/REPORT.tex`, generate `open_questions.json`, `open_questions_section.tex`, `workflow.md` (this file), `artifacts_summary.md`, `failure_analysis.md`, and add `extraction/nougat.mmd` stub for provenance.

## Reproduction
```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-1803.03621-approximate-randomized-benchmarking-for-finite-groups
python -m venv .venv
source .venv/bin/activate
pip install numpy==2.5.0 scipy==1.18.0 matplotlib
python work/monomial_rb.py         # ~150s
python work/clifford_generator_rb.py  # ~7s
python work/compare_protocols.py    # ~18s
python work/plot_results.py         # ~5s
```
Total wall time end-to-end: ~3 minutes.

## Endpoints Used
- Argo proxy `http://localhost:44497/v1` (via LiteLLM aggregator `<tailnet-aggregator>:4000` when on mesh) — LLM judge only, free.
- No paid endpoints. No non-free calls.

## Reproducibility Notes
- All RNG seeds are drawn fresh per run; results reproduce to statistical noise, not bitwise.
- The `curve_fit` bounds `(0, 0, 0.5)` to `(1, 1, 1)` for `(A, B, f)` prevent degenerate fits at short m.
- The Ginibre construction for σ (`G = randn + 1j·randn`, `σ = GG†/Tr(GG†)`) uses the standard convention; other HS-uniform samplers would give statistically equivalent results.
