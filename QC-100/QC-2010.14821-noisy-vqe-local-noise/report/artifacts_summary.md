# Artifacts Summary — QC-2010.14821 (noisy VQE local noise)

## Directory tree
```
QC-2010.14821-noisy-vqe-local-noise/
├── code/
│   ├── vqe_noisy.py                          # VQE + noise sweep driver (Qiskit Aer density-matrix)
│   └── analyze_and_plot.py                   # small-p linearity + depth-accumulation + plots
├── work/
│   ├── paper.pdf                             # arXiv:2010.14821v2
│   └── paper.txt                             # pdftotext dump
├── extraction/
│   └── nougat.mmd                            # OCR stub (paper ingested via pdftotext)
└── report/
    ├── REPORT.md                             # original narrative Markdown report
    ├── REPORT.tex                            # LaTeX packaging (this backfill)
    ├── open_questions.json                   # 5 open questions, bare JSON list
    ├── open_questions_section.tex            # LaTeX section, \input from REPORT.tex
    ├── workflow.md                           # step-by-step reproducibility narrative
    ├── artifacts_summary.md                  # this file
    ├── failure_analysis.md                   # honest critique
    └── evidence/
        ├── smoke_n2_d1/results.json          # 2-qubit smoke sanity check
        ├── main_n4_d2/results.json           # headline sweep, n=4 d=2 (30 gates)
        ├── main_n4_d3/results.json           # headline sweep, n=4 d=3 (45 gates)
        ├── analysis_summary.json             # slopes, ratios, R²
        ├── energy_vs_p.png                   # E_VQE(p), (E−E₀)/|E₀| vs p, both depths
        └── delta_E_vs_p_linearity.png        # ΔE(p) + small-p linear-fit overlays
```

## Artifact roles

| Path | Role |
|---|---|
| `code/vqe_noisy.py` | Primary simulation driver — implements paper Fig. 2 ansatz + paper Eq. 6 noise model. |
| `code/analyze_and_plot.py` | Downstream analysis — small-p linear fits, depth-accumulation ratios, plot rendering. |
| `work/paper.pdf` / `paper.txt` | Ground-truth paper content. |
| `extraction/nougat.mmd` | OCR stub; the paper was ingested via arXiv PDF + pdftotext (Nougat not needed for text-only claims). |
| `report/REPORT.md` | Original detailed prose replication report (source of truth). |
| `report/REPORT.tex` | LaTeX packaging with honest Critique section (backfill 2026-07-06). |
| `report/open_questions.json` | 5 truly-open follow-ups, each with basis + concrete next_steps. |
| `report/open_questions_section.tex` | Same 5 questions in LaTeX, appended to REPORT.tex via `\input`. |
| `report/workflow.md` | End-to-end reproducibility narrative. |
| `report/failure_analysis.md` | Honest limitations / what would strengthen the claim. |
| `report/evidence/*.json` | Machine-readable raw results per sweep. |
| `report/evidence/*.png` | Figures for the noise-scaling curve and its linear fits. |

## Verdict crosscheck
- `report/REPORT.md` says: **"Verdict: REPLICATED (strong)"**.
- Basis: paper's own ansatz + Hamiltonian + noise model rebuilt in Qiskit Aer; six of nine paper claims (C1–C6) reproduced quantitatively from primary simulation data; observed slopes and depth-accumulation ratios match paper §III text within a small (~10%) residual attributable to 2-qubit-gate fraction.
- **verdict_preserved = REPLICATED**.

## Reproducibility one-liner
```bash
python -m venv .venv && source .venv/bin/activate && \
  pip install "qiskit==2.5.0" "qiskit-aer==0.17.2" numpy scipy matplotlib && \
  python code/vqe_noisy.py --n-qubits 4 --d 2 --n-seeds 5 --maxiter 800 \
    --outdir report/evidence/main_n4_d2 --p-values 0,1e-4,3e-4,1e-3,3e-3,1e-2 && \
  python code/vqe_noisy.py --n-qubits 4 --d 3 --n-seeds 5 --maxiter 1500 \
    --outdir report/evidence/main_n4_d3 --p-values 0,1e-4,3e-4,1e-3,3e-3,1e-2 && \
  python code/analyze_and_plot.py
```
