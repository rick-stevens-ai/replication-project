# Artifacts summary — arXiv:0811.3208 replication

## Directory layout
```
QC-0811.3208-quantum-algorithms-highly-nonlinear-boolean-rotteler/
├── paper.pdf                      # canonical arXiv PDF (mirror of work/paper.pdf)
├── extraction/
│   ├── README.md                  # explains surrogate-tool convention
│   ├── marker.md                  # PyMuPDF surrogate for Marker
│   └── nougat.mmd                 # pdftotext -layout surrogate for Nougat
├── work/
│   ├── paper.pdf                  # source
│   └── paper.txt                  # pdftotext (used for skim)
└── report/
    ├── REPORT.tex                 # full LaTeX report, section-by-section
    ├── open_questions.json        # 5 heavy-duty non-superficial Qs
    ├── workflow.md                # workflow, tools+versions, effort estimate
    ├── artifacts_summary.md       # this file
    ├── failure_analysis.md        # honest friction + residual gaps
    └── evidence/
        ├── rotteler_replication.py    # single-file replication code
        ├── results.json               # headline numeric outputs
        ├── scaling.json               # classical vs quantum vs n
        └── run.log                    # tee of last replication run
```

## Provenance of every artifact
| Artifact | Source / provenance |
|---|---|
| `paper.pdf` | Downloaded `curl -sL https://arxiv.org/pdf/0811.3208` on 2026-07-05, 187 KB, SHA-1 unchanged from arXiv v2. |
| `work/paper.txt` | `pdftotext work/paper.pdf work/paper.txt`, 976 lines. |
| `extraction/marker.md` | Fresh PyMuPDF text extraction, page-boundary markers preserved. 51 141 bytes, 1 002 lines. |
| `extraction/nougat.mmd` | Fresh `pdftotext -layout` extraction, 817 lines. |
| `extraction/README.md` | Adopted convention from sibling `QC-0704.3628.../extraction/README.md`. |
| `report/evidence/rotteler_replication.py` | Written from scratch here, ~17 KB, single-file, numpy-only. Deterministic seed `RNG = np.random.default_rng(0xB3170208)`. |
| `report/evidence/results.json` | Output of the above script's `main()`. |
| `report/evidence/scaling.json` | Output of the same run (`main()` continuation). |
| `report/evidence/run.log` | `tee` of that run, verbatim stdout. |
| `report/REPORT.tex` | Written from scratch here; numbers pasted from `results.json`, method matches script. |
| `report/open_questions.json` | Grounded in observations of the actual replication run (see basis fields). |
| `report/workflow.md` | Written here. |
| `report/failure_analysis.md` | Written here; enumerates real friction. |

## Headline numeric results
Extracted from `report/evidence/results.json`:

| n | Walsh max abs error | Dual bent match | A1 (2q, 0-err) | A2 (4n q) | Classical ML min-T |
|---|--:|---|---|---|--:|
| 4 | 0.000e+00 | ✓ | 20/20 (prob = 1.000000) | 20/20 | 4.4 (mean of 5) |
| 6 | 0.000e+00 | ✓ | 20/20 (prob = 1.000000) | 20/20 | 6.8 (mean of 5) |

Scaling scan (single-trial classical ML min-T vs 4n quantum queries):
```
n= 2: classical T=2,  quantum 4n=8
n= 4: classical T=5,  quantum 4n=16
n= 6: classical T=8,  quantum 4n=24
n= 8: classical T=9,  quantum 4n=32
n=10: classical T=12, quantum 4n=40
```
(As discussed in the report and in Open Question Q1, this classical
detector is intentionally strong — it uses full knowledge of `f` — and
its linear scaling with `n` reflects the information-theoretic lower
bound, not the paper's 2^{Ω(n)} query LB which applies to a black-box
randomised adversary.)

## Verdict
**REPLICATED** — Walsh-flatness + dual-bent formula + Algorithm A_1
(2-query, zero-error) + Algorithm A_2 (O(n)-query, HSP-style)
all reproduce the paper to machine precision on n=4 AND n=6.
