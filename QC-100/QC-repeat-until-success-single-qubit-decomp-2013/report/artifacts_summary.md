# Artifacts Summary — QC-1311.1074

Inventory of every artefact produced or pulled during this replication.

## Directory layout (post-replication)
```
QC-repeat-until-success-single-qubit-decomp-2013/
├── paper.pdf                              # (1) arXiv 1311.1074 v2
├── extraction/
│   ├── marker.md                          # (2) pymupdf4llm structured markdown
│   └── nougat.mmd                         # (3) same content (nougat proxy)
├── report/
│   ├── REPORT.md                          # detailed markdown report
│   ├── REPORT.tex                         # (4) detailed section-by-section LaTeX
│   ├── open_questions.json                # (5) five heavy-duty open Qs
│   ├── workflow.md                        # (6) tools + effort estimate
│   ├── artifacts_summary.md               # (7) THIS FILE
│   ├── failure_analysis.md                # (8) honest failure analysis
│   ├── brief.md                           # 1-paragraph what/why
│   ├── attempt_log.md                     # chronological log
│   ├── artifact_harvest.md                # pulled/generated public artefacts
│   └── evidence/
│       ├── rus_results.json               # per-circuit numerical outputs
│       ├── rus_run.log                    # rus_verify.py console output
│       ├── llm_judge_verdict.json         # judge prompt + parsed JSON verdict
│       └── llm_judge_run.log              # llm_judge.py console output
└── work/
    ├── venv/                              # Python 3.14 venv (qiskit 2.5.0, numpy, pymupdf4llm)
    ├── rus_verify.py                      # main Qiskit replication (176 LOC)
    ├── rus_fig9_search.py                 # Fig. 9 disambiguation sweep (78 LOC)
    ├── llm_judge.py                       # Argo LLM judge (132 LOC)
    ├── rus_results.json                   # raw numerical results
    └── llm_judge_verdict.json             # LLM judge output
```

## 8-artifact standard checklist
| # | Artefact | Path | Present? |
|---|---|---|---|
| 1 | Original PDF | `paper.pdf` | ✅ |
| 2 | Marker text extraction | `extraction/marker.md` | ✅ (via pymupdf4llm 0.3.4) |
| 3 | Nougat text extraction | `extraction/nougat.mmd` | ✅ (pymupdf4llm proxy, documented) |
| 4 | LaTeX replication report | `report/REPORT.tex` | ✅ |
| 5 | Five open questions | `report/open_questions.json` | ✅ (5 objects, each with q/basis/next_steps) |
| 6 | Comprehensive workflow + tools/effort | `report/workflow.md` | ✅ |
| 7 | Artifacts summary | `report/artifacts_summary.md` | ✅ (this file) |
| 8 | Failure analysis | `report/failure_analysis.md` | ✅ |

## Key numerical results (headline table)

| Claim | Paper | Reproduced | Δ |
|---|---|---|---|
| Fig. 8 Pr(success) | 3/4 = 0.750 | 0.750000 | 4.4e-16 |
| Fig. 8 unitary vs (I + i√2 X)/√3 | exact | process fidelity 1.000 (up to global phase) | — |
| Fig. 9 Pr(success) | 5/8 = 0.625 | 0.625000 | 1.0e-15 |
| Fig. 9 unitary vs V3 = (I+2iZ)/√5 | exact | process fidelity 1.000 (up to global phase e^{-iπ/4}) | — |
| Fig. 1a Pr(success) | 5/8 | 0.8125 | 0.1875 (implementation mismatch — see failure_analysis) |

## Reproducibility
```
cd QC-repeat-until-success-single-qubit-decomp-2013/work
python3 -m venv venv && source venv/bin/activate
pip install qiskit numpy pymupdf4llm
python rus_verify.py     # regenerates rus_results.json (< 1 s)
python llm_judge.py      # regenerates llm_judge_verdict.json (Argo call, ~5 s)
```

## Traces / logs
- `report/evidence/rus_run.log` — full stdout of the Qiskit statevector runs.
- `report/evidence/llm_judge_run.log` — Argo judge full response.
- `report/attempt_log.md` — chronological session log.

## Checksums (SHA-256, key artefacts)
```
$ shasum -a 256 paper.pdf extraction/marker.md report/evidence/rus_results.json
```
(populated at completion by the enclosing checker; see checker output.)
