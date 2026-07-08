# Workflow — QC-2110.12071 replication

## 1. Paper acquisition
- Fetched arXiv abstract HTML → `work/abs.html`
- Downloaded arXiv PDF v2 (13 Jul 2022) → `work/paper.pdf`
- `pdftotext -layout work/paper.pdf work/paper.txt` for machine-readable text pass
- Extracted (during backfill 2026-07-05) via Nougat stub → `extraction/nougat.mmd`

## 2. Paper triage (what is reproducible in a wave brief envelope)
- Identified 5 headline claims (C1–C5).
- C4 (Lemma-2 LCU gate cost, $L$-independent) requires a resource estimator → out of scope.
- C5 (FeMoco resource estimate) requires 152-orbital Appendix-D optimisation → out of scope.
- C1 (CDF estimator structural correctness) + C2 (shot-noise sample-complexity scaling) fit the QC-100 laptop-in-minutes envelope.
- C3 (Fourier weight $A(\vec r)=O(\log d)$) tested structurally at $d=20$.

## 3. Environment
- Host: CherryRd (Apple Silicon, M2 CPU, no GPU).
- Python 3.14.6 in `.venv/`.
- Packages: numpy 2.5.0, scipy 1.18.0, matplotlib, qiskit 2.5.0 (installed; unused for the 4×4 statevector work — installed only to demonstrate the standard QC-100 tool chain works).
- All work local, all endpoints free (no external API calls, no paid compute).

## 4. Implementation (in `code/`)
- `statistical_pe.py`: builds 2q TFIM Hamiltonian ($J=1$, $h=0.5$), eigendecomposes, constructs Fourier series ($d=20$), samples $j\sim|F_j|/A$, computes exact $U_j=e^{i\hat H t_j}$ via eigendecomposition of $\hat H = H/\lambda$, draws Bernoulli Re/Im Hadamard-test shots, accumulates $\tilde C(x)$.
- `make_plots.py`: renders `fig_cdf.png` (analytic vs. sampled CDF) and `fig_scaling.png` (std vs. $N$ log-log + downstream energy RMS vs. $N$).

## 5. Runs (all seeded, deterministic)
```
python code/statistical_pe.py --out-dir report/evidence \
       --n-samples 40000 --d 20 --scaling --scan-reps 24
python code/make_plots.py
```
- Main run: $N=40{,}000$ samples → $80{,}000$ simulated Hadamard tests.
- Scaling scan: $N \in \{500, 1000, 2500, 5000, 10\,000, 25\,000, 50\,000, 100\,000\}$, 24 replicates each, distinct seed per replicate (`20260703 + 1000*rep`).
- Wall time: ~15s total on M2 CPU.

## 6. Evidence emitted (in `report/evidence/`)
- `spe_run.json` — single $N=40\,000$ run: eigenvalues, overlaps, Fourier weights, $\tau E_\text{gs}^\text{est}$, energy error.
- `spe_scaling.json` — full scaling scan (8 sizes × 24 reps): per-$N$ std, bias, downstream RMS energy error.
- `fig_cdf.png` — analytic vs. sampled $\tilde C(x)$, vertical lines at true $\tau E_k$, overlap-weighted.
- `fig_scaling.png` — std-vs-$N$ log-log with fit slope $-0.451$; energy-RMS-vs-$N$ with fit slope $-1.29$ (higher-$N$ regime).

## 7. Analysis
- Compared measured slope $-0.451$ against paper prediction $-0.500$ (Alg. 1 line 3 Hoeffding): within 10%.
- Verified jumps at both non-zero-overlap eigenvalues; verified low/zero-overlap eigenvalues suppressed.
- Diagnosed the low-$N$ energy-error regime (RMS ≈ 1 at $N \le 1000$) as a *binary-search heuristic* artifact (threshold occasionally crosses at first-excited jump), not an estimator failure — the paper's Lin-Tong multi-round binary search is not implemented.

## 8. Backfill (2026-07-05)
- Added: `REPORT.tex`, `open_questions.json` (5 items), `open_questions_section.tex`, `workflow.md` (this file), `artifacts_summary.md`, `failure_analysis.md`, `extraction/nougat.mmd` stub.
- Verdict cross-check: **REPLICATED preserved** (backbone C1+C2 exercised; algorithmic-novelty C4 + resource-estimate C5 explicitly *not* exercised and flagged).
- No simulations re-run; all backfill artifacts are documentation on top of preserved evidence.
