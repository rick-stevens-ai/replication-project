# Workflow — QC-1606.07413 replication

Reconstructed from on-disk artifacts (`code/`, `report/evidence/`, `logs/`).

## 0. Preflight
- Confirmed paper is open access (arXiv + QST 1(1) 015003).
- Downloaded `work/paper.pdf`, `pdftotext`-extracted to `work/paper.txt`.
- Identified the four checkable claim classes on laptop:
  1. T-count = 7 for the 5 named 3-qubit circuits (unitary-verifiable)
  2. 4-qubit adder unitary well-formed + naive T-count baseline
  3. Parallel speedup shape (algorithmic, laptop-scale)
  4. (Out of scope) BG/Q architecture-ratio tuning and absolute 4096-core timings

## 1. Environment setup
```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-1606.07413-parallel-circuit-synthesis
python -m venv .venv
source .venv/bin/activate
pip install qiskit==2.5.0 numpy==2.5.0
python -c "import qiskit, numpy, platform, os; \
  print('python', platform.python_version()); \
  print('qiskit', qiskit.__version__); \
  print('numpy', numpy.__version__); \
  print('platform', platform.platform()); \
  print('cpu_count', os.cpu_count())" > report/evidence/environment.txt
```

## 2. Claims C1 + C2 — 3-qubit T-count-7 circuits
- `code/verify_toffoli_tcount.py`:
  - Explicit Nielsen–Chuang / Barenco 1995 6-CNOT + 7-T Toffoli.
  - Fredkin = CNOT(t,c) · Toffoli · CNOT(t,c).
  - Peres = Toffoli · CNOT(c1, c2).
  - Quantum OR = X⊗X⊗I · Toffoli · X⊗X⊗I (De Morgan).
  - Negated Toffoli = X⊗X⊗I · Toffoli · X⊗X⊗I on the control lines then X on target.
  - For each: count `t`/`tdg` gates; compute `Operator(qc)` and compare to
    truth-table target unitary up to global phase (uniform ratio, tol 1e-6).
- Output: `report/evidence/tcount_verification.json` (5 pass/fail rows).

## 3. Claim C3 — 4-qubit 1-bit full adder
- `code/verify_adder_tcount.py`:
  - Build target unitary from truth table (inputs cin, a, b, s; outputs cin, a, a⊕b⊕cin, s⊕maj).
  - Assert `U U†  I` (residual 0.00e+00).
  - Build reversible circuit: 3 Toffolis (majority into scratch) + 2 CNOTs (sum), verify against target.
  - `qc.decompose(['ccx'])` then count T-gates → naive baseline 21.
  - Record paper optimum 7 (Sec 5.3, via Amy [22] affine-Toffoli equivalence).
- Output: `report/evidence/adder_tcount.json`.

## 4. Claim C4 — Parallel synthesis speedup (CORE)
- `code/parallel_synthesis_speedup.py`:
  - 10-gate 2-qubit library; target = random length-6 product; encoding ∈ [0, 10^6).
  - Sequential: linear scan of the 10^6 candidates.
  - Parallel N: `multiprocessing.Pool(N).imap_unordered`; N contiguous chunks; first finder wins; pool terminated on success.
  - 6 random seeds (base seed 42); reject any target encoding in first 5% of space.
  - Time via `time.perf_counter()` around real search that finds a valid decomposition each trial.
  - Sweep N ∈ {1, 2, 4, 8}.
- Outputs:
  - `report/evidence/parallel_speedup.json` (per-trial + aggregate)
  - `logs/parallel_speedup_run2.log` (full stdout)

## 5. Report assembly
- Aggregated results into `report/REPORT.md`.
- Verdict = REPLICATED (4/6 tested claims pass; the 2 untested are HPC-only and out of scope).

## 6. Backfill (2026-07-06)
- Converted REPORT.md → REPORT.tex.
- Added `open_questions.json` (5) + `open_questions_section.tex`.
- Added `workflow.md`, `artifacts_summary.md`, `failure_analysis.md`.
- Added `extraction/nougat.mmd` stub (paper is text-native PDF; pdftotext used).

## Rerun-from-scratch recipe
```bash
source .venv/bin/activate
python code/verify_toffoli_tcount.py      # 5-circuit T-count check → JSON
python code/verify_adder_tcount.py        # 4-qubit adder unitary + naive T=21
python code/parallel_synthesis_speedup.py # sequential vs parallel N∈{1,2,4,8}
```
All three write to `report/evidence/*.json` deterministically; the parallel script uses a fixed base seed (42) for target selection but wall times will vary run-to-run.
