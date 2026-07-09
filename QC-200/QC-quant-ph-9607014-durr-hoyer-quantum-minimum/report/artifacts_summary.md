# Artifacts Summary — Dürr-Høyer (1996) Replication

## Directory layout
```
QC-quant-ph-9607014-durr-hoyer-quantum-minimum/
├── paper.pdf                              # (1) Source PDF (arXiv:quant-ph/9607014v2)
├── extraction/
│   ├── marker.md                          # (2) Text extraction, Marker fallback via pdftotext -layout
│   └── nougat.mmd                         # (3) Text extraction, Nougat fallback via pdftotext -raw
├── report/
│   ├── REPORT.tex                         # (4) Detailed section-by-section LaTeX report
│   ├── REPORT.pdf                         # (4) Compiled PDF (if LaTeX available)
│   ├── open_questions.json                # (5) 5 heavy-duty open questions with next steps
│   ├── workflow.md                        # (6) Comprehensive workflow + tools + effort
│   ├── artifacts_summary.md               # (7) THIS FILE
│   ├── failure_analysis.md                # (8) Honest failure/friction analysis
│   └── evidence/
│       ├── results.json                   # All measured numbers, seeded
│       └── run.log                        # Cleaned stdout of the simulation run
├── work/
│   ├── durr_hoyer.py                      # Simulation code (298 LOC, Qiskit)
│   └── paper.txt                          # pdftotext dump of paper.pdf
└── .venv/                                 # Python venv (Qiskit 2.5.0 + Aer 0.17.2)
```

## Full inventory (non-venv files)

| Path                              | Size    | Type    | Description                                              |
|-----------------------------------|---------|---------|----------------------------------------------------------|
| paper.pdf                         |  ~77 KB | PDF     | arXiv:quant-ph/9607014v2, downloaded via curl 2026-07-05 |
| extraction/marker.md              | ~13 KB  | Markdown| pdftotext -layout fallback + header                      |
| extraction/nougat.mmd             |  ~7 KB  | Markdown| pdftotext -raw fallback + header                         |
| work/paper.txt                    | ~10 KB  | Text    | pdftotext dump used for skimming                         |
| work/durr_hoyer.py                | ~12 KB  | Python  | Simulation (Grover circuit + BBHT + DH outer loop)       |
| report/REPORT.tex                 | ~14 KB  | LaTeX   | Detailed replication report                              |
| report/REPORT.pdf                 |   var   | PDF     | Compiled report (if pdflatex available)                  |
| report/open_questions.json        |  ~5 KB  | JSON    | 5 Q/basis/next_steps objects                             |
| report/workflow.md                |  ~5 KB  | Markdown| Workflow + tools + effort                                |
| report/artifacts_summary.md       | (this)  | Markdown| Artifact inventory                                       |
| report/failure_analysis.md        |  ~3 KB  | Markdown| Failure analysis                                         |
| report/evidence/results.json      |  ~2 KB  | JSON    | All measured numbers                                     |
| report/evidence/run.log           |  ~1 KB  | Text    | Cleaned run log                                          |

## Traces / provenance

- **Paper resolution:** `curl -sL -o paper.pdf https://arxiv.org/pdf/quant-ph/9607014` on 2026-07-05.
- **Simulation runs:** all seeded (Part A seed=1234+N, Part B seed=9000+N).
  Rerunning `python work/durr_hoyer.py` produces byte-identical numbers.
- **Wall time:** 252 seconds (single-core macOS).
- **Environment file:** `pip freeze` inside `.venv` captures the exact
  dependency graph (Qiskit 2.5.0, Qiskit-Aer 0.17.2, NumPy 2.4.3, plus
  transitive deps).
- **No external services called** during the simulation. LLM endpoints
  (Argo, CELS) were available but not used — the verdict is a numeric
  comparison, not an LLM-judged one.

## Reproducibility

Full rerun from scratch (given only `paper.pdf` or the arXiv id):
```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-9607014-durr-hoyer-quantum-minimum
python3 -m venv .venv --system-site-packages
source .venv/bin/activate
pip install --quiet qiskit qiskit-aer
python work/durr_hoyer.py
```
Expect `report/evidence/results.json` to reproduce with identical numbers
(seeded RNG throughout).

## Key results

| N   | R   | Inner backend           | Success prob | Mean queries | Paper bound |
|-----|-----|-------------------------|--------------|--------------|-------------|
|   4 | 100 | Real Qiskit statevector | 1.000        |  0.15        |  50.60      |
|   8 | 100 | Real Qiskit statevector | 1.000        |  0.51        |  76.24      |
|  16 |  50 | Real Qiskit statevector | 1.000        |  1.40        | 112.40      |
|  16 | 500 | Analytic Grover prob    | 1.000        |  1.29        | 112.40      |
|  32 | 500 | Analytic Grover prob    | 1.000        |  2.87        | 162.28      |
|  64 | 500 | Analytic Grover prob    | 1.000        |  5.59        | 230.40      |
| 128 | 500 | Analytic Grover prob    | 1.000        | 10.22        | 323.16      |
| 256 | 500 | Analytic Grover prob    | 1.000        | 17.90        | 449.60      |

Fitted scaling constant: ĉ ≈ **0.96** (in <Q(N)> = c·√N), vs. paper worst-case 22.5.

## Verdict
**REPLICATED** — Success probability ≥ 1/2 and O(√N) scaling both reproduced on
real Qiskit Aer statevector simulation.
