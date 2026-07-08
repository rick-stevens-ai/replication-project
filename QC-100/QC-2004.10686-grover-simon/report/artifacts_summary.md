# Artifacts Summary — QC-2004.10686-grover-simon

## Directory layout
```
QC-2004.10686-grover-simon/
├── report/
│   ├── REPORT.md                       # canonical replication report (Markdown)
│   ├── REPORT.tex                      # LaTeX version w/ open questions
│   ├── open_questions.json             # 5 open questions (bare JSON list)
│   ├── open_questions_section.tex      # LaTeX \input for REPORT.tex
│   ├── workflow.md                     # stage-by-stage pipeline
│   ├── artifacts_summary.md            # this file
│   ├── failure_analysis.md             # honest critique + limits
│   └── evidence/
│       ├── grover_pair1.json           # 1-pair Grover raw counts + summary
│       ├── grover_pair2.json           # 2-pair Grover raw counts + summary
│       ├── grover_scaling.json         # iteration scan raw numbers
│       ├── simon_classical.py          # classical SIMON reference impl
│       ├── classical_brute.py          # brute-force oracle enumeration
│       ├── grover_simon.py             # Qiskit Grover circuit
│       ├── grover_scaling.py           # k-vs-P scan driver
│       └── versions.txt                # exact Python/Qiskit/Aer versions
├── code/                               # working copies of the above scripts
├── extraction/
│   └── nougat.mmd                      # Nougat OCR of paper (stub)
└── (paper PDF, if cached)
```

## Artifact roles

| Artifact | Role | Verifies |
|---|---|---|
| `REPORT.md` | Human-readable primary report | Verdict + all 7 checkable claims |
| `REPORT.tex` | LaTeX version for PDF build | Same, plus critique + open-Qs |
| `open_questions.json` | Machine-readable open questions | 5-item follow-up list |
| `open_questions_section.tex` | LaTeX inclusion | Renders open-Qs into REPORT.pdf |
| `workflow.md` | Reproducibility guide | Exact stage ordering + commands |
| `artifacts_summary.md` | Directory map | Navigation |
| `failure_analysis.md` | Honest critique | What we skipped, what could break |
| `evidence/*.json` | Raw simulator output | C5, C6, C7 numerics |
| `evidence/*.py` | Simulation source code | Reproducibility of the Qiskit runs |
| `extraction/nougat.mmd` | OCR extraction of paper | Text-searchable source |

## Verdict
**REPLICATED.** Paper's reduced-SIMON Grover-key-search demonstration
(Figures 11 + 14a/b) reproduces on independent 20-qubit Qiskit statevector
implementation. Two-peak / one-peak histogram structure matches to $>99\%$
combined probability; success-vs-iteration curve matches $\sin^2((2k{+}1)\theta)$
to $<0.01$ across $k=0..7$.

## Not verified
- Full-scale gate-count / T-depth tables for SIMON32/64…SIMON128/256 (C8).
- Noisy-hardware execution.
- Surface-code overhead / FT resource cost.
