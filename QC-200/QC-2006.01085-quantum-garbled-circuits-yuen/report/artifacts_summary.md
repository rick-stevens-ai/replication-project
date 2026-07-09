# Artifacts Summary — arXiv:2006.01085 replication

## Directory tree
```
QC-2006.01085-quantum-garbled-circuits-yuen/
├── paper.pdf                              # 658 KB, 66 pages, arXiv v2 (2020-11-09)
├── extraction/
│   ├── marker.md                          # pdftotext fallback (192 KB)
│   └── nougat.mmd                         # pdftotext fallback (192 KB)
├── work/
│   ├── paper.txt                          # pdftotext output
│   └── venv/                              # Python 3.14 venv (qiskit, numpy, cryptography)
└── report/
    ├── REPORT.tex                         # main LaTeX report
    ├── open_questions_section.tex         # \input'd by REPORT.tex
    ├── open_questions.json                # machine-readable 5 open questions
    ├── workflow.md                        # comprehensive workflow (this file's sibling)
    ├── artifacts_summary.md               # THIS FILE
    ├── failure_analysis.md                # honest failure/friction analysis
    └── evidence/
        ├── yao_and_gate.py                # Yao classical GC baseline
        ├── yao_and_gate.out.json          # all 4 AND rows correct
        ├── qgc_clifford_teleport.py       # QGC Clifford slice (numpy)
        ├── qgc_clifford_teleport.out.json # 5 sub-tests, all pass
        ├── qiskit_crosscheck.py           # Qiskit independent check
        └── qiskit_crosscheck.out.json     # H fidelity ≈ 1, CNOT hiding dist ≈ 5.5e-17
```

## Provenance
| Artifact | Source | Notes |
|---|---|---|
| paper.pdf | https://arxiv.org/pdf/2006.01085 | fetched 2026-07-05 via curl |
| extraction/marker.md | local pdftotext | Marker not yet run on this arXiv id in central corpus |
| extraction/nougat.mmd | local pdftotext | Nougat not yet run on this arXiv id in central corpus |
| yao_and_gate.py | authored fresh | Yao (1986) construction with AES-GCM |
| qgc_clifford_teleport.py | authored fresh | implements paper §2.1 Clifford slice |
| qiskit_crosscheck.py | authored fresh | independent Qiskit implementation |

## Numerical evidence highlights
| Test | Metric | Value |
|---|---|---|
| Yao AND | rows correct | 4/4 |
| QGC H\|0> | decoded fidelity | 0.9999999999999996 |
| QGC HSH\|0> | decoded fidelity | 0.9999999999999991 |
| QGC CNOT on \|0>\|+> | decoded fidelity | 0.9999999999999996 |
| 1q hiding | avg-Pauli distance to I/2 | 1.1e-16 |
| 2q hiding | avg-Pauli Frobenius distance to I/4 | 5.6e-17 |
| Qiskit H\|0> | fidelity | 0.9999999999999996 |
| Qiskit CNOT hiding | Frobenius distance to I/4 | 5.6e-17 |

## Traces / logs
All raw JSON outputs are in `report/evidence/*.out.json` — they are the direct
`stdout` of each script (piped via `tee`). No log/output was edited or elided.
