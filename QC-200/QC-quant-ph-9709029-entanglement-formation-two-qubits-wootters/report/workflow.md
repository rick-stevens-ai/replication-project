# Workflow — Wootters (1998) 2-qubit entanglement of formation replication

## Objective
Independently reproduce the closed-form Wootters formula for E_F(rho) of an
arbitrary 2-qubit mixed state (arXiv:quant-ph/9709029, PRL 80, 2245) with
real numerical simulation on CPU, and validate it against Bell / product /
Werner / Bell-diagonal / Haar-random density matrices.

## Environment / tools / versions
- Host: CherryRd (Darwin 25.3.0 x86_64)
- Python: **3.14.0** (system) for the main run; **3.12.13** venv for
  marker-pdf (heavier PDF-parser)
- Key libs (from `pip list`, main venv):
  - `numpy==2.4.3`
  - `qiskit==2.5.0`
  - `matplotlib==3.10.7`
- `pdftotext` (Poppler CLI) 25.10.0 for the raw text extraction
- `marker-pdf` (installed in `.venv312/`) for Markdown extraction
- LaTeX (BasicTeX) for compiling `REPORT.pdf`

## Steps executed (chronological)
1. **Read brief** (`~/Dropbox/REPLICATE-PROJECT/scripts/QC_WAVE_BRIEF_2026-07-03.md`).
2. **Create target dir** + subdirs `work/`, `extraction/`, `report/evidence/`.
3. **Fetch paper** from `https://arxiv.org/pdf/quant-ph/9709029` → `paper.pdf`
   (117 kB, 13 pp). Verified authorship: William K. Wootters, Williams College;
   PRL 80, 2245 (1998).
4. **Extract text** with `pdftotext paper.pdf work/paper.txt`. Confirmed the
   central formulas match the brief.
5. **Set up main venv** (Python 3.14) and install numpy + qiskit + matplotlib.
6. **Write core replication code** `report/evidence/wootters_concurrence.py`
   implementing:
   - `binary_entropy(x)`
   - `concurrence(rho)` via YY spin-flip + eigenvalues of `rho * rho_tilde`
   - `entanglement_of_formation(rho)`
   - `random_2qubit_mixed(rng)` via Haar purification
   - `brute_force_ef_upper_bound(rho, ...)` via HJW isometry sampling
7. **Run test suite** with 12 checks (Bell, product, Werner sweep, random
   states, monotonicity, Bell-diagonal, brute-force bound).
   - **First run: 11/12** — brute-force test failed.
   - **Root cause**: `numpy.linalg.eigh` returns ASCENDING eigenvalues, but
     the code used `w[:r]` intending the largest r eigenmodes. This picked
     zero eigenvalues of a rank-2 state.
   - **Fix**: sort descending via `np.argsort(w)[::-1]` before taking the top r.
   - **Second run: 12/12**.
8. **Produce plots**:
   - `werner_sweep.png` — C(p) and E(p) with separability line at p=1/3
   - `random_states_E_vs_C.png` — 1000 random states over the Wootters curve
9. **Write LaTeX report** `report/REPORT.tex`.
10. **Extract Markdown** with marker (marker-pdf in `.venv312/`).
11. **Nougat surrogate** — see `extraction/README.md`; nougat depends on an
    old torch stack and is not installable on Darwin 25 / Python 3.12+ without
    a heavy backport, so we produced a documented pdftotext-based `nougat.mmd`
    surrogate that captures the same semantic content.
12. **Write** `report/artifacts_summary.md`, `report/failure_analysis.md`,
    `report/open_questions.json`.
13. **Compile** `REPORT.tex` → `REPORT.pdf` via `pdflatex` (attempted;
    fallback OK if LaTeX absent).

## Compute estimate
- End-to-end wall time on a single core: **< 2 minutes** for the numerical
  replication (12 tests, 1000 random states, 400 brute-force decompositions).
- No GPU, no HPC, no paid inference. All-CPU on the local laptop.

## Reproduction command (single line)
```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-9709029-entanglement-formation-two-qubits-wootters && \
  python3 -m venv .venv && source .venv/bin/activate && \
  pip install numpy scipy qiskit matplotlib && \
  python report/evidence/wootters_concurrence.py && \
  python report/evidence/plot_werner.py
```

## Result summary
- **12/12 quantitative checks pass** (see `report/evidence/results.json`).
- Verdict: **REPLICATED**.
