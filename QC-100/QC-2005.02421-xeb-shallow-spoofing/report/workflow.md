# Reproducible Workflow — QC-2005.02421 (shallow-XEB spoofing)

Target paper: arXiv:2005.02421v1, Barak / Chou / Gao, *Spoofing Linear Cross-Entropy Benchmarking in Shallow Quantum Circuits*, May 2020.

All steps below run on a single CPU (no HPC, no paid API, no external network).
Seed `20260703`, bit-for-bit reproducible.

## 0. Directory layout

```
QC-2005.02421-xeb-shallow-spoofing/
├── .venv/                                 # cirq-core 1.7.0, numpy 2.5.0
├── scripts/
│   ├── xeb_experiment.py                  # baseline + spoofer driver
│   └── collision_probability_check.py     # CP-vs-depth sanity check
├── work/
│   ├── paper.pdf                          # arXiv 2005.02421 PDF
│   ├── paper.txt                          # pdftotext dump
│   └── abs.html                           # arXiv abstract page
├── extraction/
│   └── nougat.mmd                         # extraction placeholder
└── report/
    ├── REPORT.md                          # narrative report
    ├── REPORT.tex                         # LaTeX version
    ├── failure_analysis.md                # honest critique
    ├── open_questions.json                # 5 open questions (bare list)
    ├── open_questions_section.tex         # LaTeX version
    ├── workflow.md                        # THIS FILE
    ├── artifacts_summary.md               # file inventory
    └── evidence/
        ├── xeb_results.json               # structured raw results
        ├── run.log                        # xeb_experiment.py console log
        └── collision_check.log            # CP trajectory console log
```

## 1. One-shot setup

```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2005.02421-xeb-shallow-spoofing
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install cirq-core numpy
.venv/bin/python -c "import cirq, numpy; print(cirq.__version__, numpy.__version__)"
# Expected: 1.7.0 2.5.0   (any 1.7.x cirq / 2.x numpy will match to the noise floor)
```

## 2. Run experiments

```bash
# ~4.5 min: exact/uniform baselines + depth-1 and light-cone-4 spoofers
.venv/bin/python scripts/xeb_experiment.py 2>&1 | tee report/evidence/run.log

# ~1 min: collision-probability trajectory towards Porter-Thomas
.venv/bin/python scripts/collision_probability_check.py 2>&1 | tee report/evidence/collision_check.log
```

Both scripts write structured JSON to `report/evidence/xeb_results.json` and
console logs to the corresponding `.log` files under `report/evidence/`.

## 3. What is being computed

| Stage | Object | Estimator |
|-------|--------|-----------|
| Baseline exact  | `F_XEB(exact)  = (1/N) Σ (2ⁿ q_C(xᵢ) − 1)`, xᵢ ∼ q_C   | N=5000, 20 circuits/(n,d) |
| Baseline uniform| `F_XEB(uniform)= (1/N) Σ (2ⁿ q_C(xᵢ) − 1)`, xᵢ ∼ U    | N=5000, 20 circuits/(n,d) |
| Spoofer d=1     | Emit `x* = argmax_v ∏ q_k(v)` deterministically         | 1 sample (deterministic) |
| Spoofer d=2..6  | Sample per size-4 block from block-marginal of q_C      | N=1000, 20 circuits/(n,d) |
| CP trajectory   | `CP(q_C) = Σ_x q_C(x)²`; compare to `2/(2ⁿ+1)`          | Exact from |amplitudes|² |

Circuits: 1D brick-wall on n∈{4,6,8}; Haar 2-qubit gates on pairs
`(0,1),(2,3),…` at even depths and `(1,2),(3,4),…` at odd depths.
Haar via QR-of-Gaussian (Mezzadri 2007).

## 4. Reading the outputs

- `report/evidence/xeb_results.json` — machine-readable results
  (per-circuit `F_XEB` estimates plus mean±std across the 20 circuits).
- `report/evidence/run.log` — human-readable console dump matching
  the tables in §4.1 and §4.3 of `REPORT.md`.
- `report/evidence/collision_check.log` — matches §4.2 of `REPORT.md`.

## 5. Regenerating the LaTeX report

```bash
cd report
pdflatex REPORT.tex && pdflatex REPORT.tex  # 2× for cross-refs; no bibliography
```

`REPORT.tex` is self-contained (no `.bib` file needed).

## 6. Honesty notes on the workflow

- **No HPC.** Everything runs on a laptop CPU in under 10 min total.
- **No paid endpoint.** No LLM in the loop for the numerical portion.
  If you re-do the narrative synthesis / open-questions section via an
  LLM, use only free endpoints (Argo Opus, Sophia, CELS, etc.), per the
  standing rule.
- **No refit to the paper.** The paper reports no numerical
  `F_XEB` values; nothing in `scripts/` reads any paper-derived
  constant. All numbers in the report come from fresh, seeded runs.
- **Deviations vs paper** are documented in `report/failure_analysis.md`
  and §6 of `REPORT.md`.
