# Artifacts Summary — WaveTrain (Riedel et al., 2023)

Every artifact produced or pulled during this replication, with sizes/checksums where easy.

## Directory tree
```
PDE-wavetrain-quantum-chain-2023/
├── paper.pdf                             # (1) 706 KB — arXiv 2302.03725v2
├── extraction/
│   ├── README.md                         # provenance for the substitute extractions
│   ├── paper.txt                         # pdftotext -layout raw
│   ├── marker.md                         # (2) copy of paper.txt (substitute)
│   └── nougat.mmd                        # (3) copy of paper.txt (substitute)
├── report/
│   ├── REPORT.md                         # main markdown report
│   ├── REPORT.tex                        # (4) LaTeX section-by-section detailed report
│   ├── brief.md                          # 1-paragraph what/why
│   ├── attempt_log.md                    # chronological run log
│   ├── artifact_harvest.md               # every public artifact pulled
│   ├── open_questions.json               # (5) 5 heavy-duty follow-ons
│   ├── workflow.md                       # (6) tools/codes/effort
│   ├── artifacts_summary.md              # (7) this file
│   ├── failure_analysis.md               # (8) honest failure analysis
│   └── evidence/
│       ├── bench.json                    # numerical benchmark JSON
│       ├── paper.pdf.sha256              # sha256 checksum
│       ├── replication_bench.py.copy     # copy of driver
│       ├── llm_judge.py.copy             # copy of judge
│       └── llm_judge.json                # judge output (verdict + rubric)
└── work/
    ├── wave_train/                       # PGelss/wave_train git clone (HEAD)
    ├── venv/                             # python 3.12 venv (contains patched scikit_tt)
    ├── replication_bench.py              # bench driver (~130 LOC, custom)
    ├── replication_bench.log             # ~1500 lines of WaveTrain solver output
    ├── llm_judge.py                      # Argo Opus 4.8 rubric judge
    ├── smoke_test.py                     # initial repro
    └── wavetrain_2302.03725.pdf          # downloaded arXiv PDF
```

## Key artifact table

| # | Artifact | Path | Provenance | Size / notes |
|---|---|---|---|---|
| 1 | Paper PDF | `paper.pdf` | Downloaded from arxiv.org/pdf/2302.03725v2 | 706 379 B; sha256 `fe2d4c48…65f295` |
| 2 | Marker text | `extraction/marker.md` | **Substitute** = pdftotext -layout | Not a real Marker parse; see extraction/README.md |
| 3 | Nougat text | `extraction/nougat.mmd` | **Substitute** = pdftotext -layout | Not a real Nougat parse; see extraction/README.md |
| 4 | LaTeX report | `report/REPORT.tex` | Written this run | Detailed section-by-section |
| 5 | Open questions | `report/open_questions.json` | Written this run | 5 heavy-duty questions with next_steps |
| 6 | Workflow | `report/workflow.md` | Written this run | Tools + effort |
| 7 | Artifacts | `report/artifacts_summary.md` | Written this run | THIS FILE |
| 8 | Failure analysis | `report/failure_analysis.md` | Written this run | Independent scikit_tt fix + rank-cap caveat |

## Bench results (`report/evidence/bench.json`)

Live-populated table (updated after every N; see final REPORT.md/TeX for the
committed numbers). Header of each row: N, wall_s, max_err vs analytic,
max_bond_rank.

## LLM judge (`report/evidence/llm_judge.json`)

Model: `argo:claude-opus-4.8` via localhost:44497 Argo proxy (free endpoint per
Rick's standing free-endpoints-only rule). Rubric embedded in `work/llm_judge.py`.

## Third-party code modifications

- `work/venv/lib/python3.12/site-packages/scikit_tt/solvers/evp.py` — 4-line
  dtype patch (backup at `evp.py.bak`).
