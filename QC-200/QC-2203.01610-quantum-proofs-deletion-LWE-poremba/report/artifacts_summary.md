# Artifacts inventory — Poremba 2022 replication

Generated 2026-07-05. Root: `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-2203.01610-quantum-proofs-deletion-LWE-poremba/`.

## The 8 required artifacts

| # | Path | Purpose | Size |
|---|---|---|---|
| 1 | `paper.pdf` | original arXiv PDF, v4 (7 Jan 2023) | 641308 B |
| 2 | `extraction/marker.md` | Marker parse (surrogate; see extraction/README.md) | ~200 KB |
| 3 | `extraction/nougat.mmd` | Nougat parse (surrogate; see extraction/README.md) | ~200 KB |
| 4 | `report/REPORT.tex` + `report/REPORT.pdf` (compiled) | detailed section-by-section report with verdict | tex 11 KB / pdf 290 KB |
| 5 | `report/open_questions.tex` + `report/open_questions.json` | 5 non-trivial open questions grounded in this replication | 3.2 KB + 4.2 KB |
| 6 | `report/workflow.md` | reproducible workflow + tools/versions + effort | ~5 KB |
| 7 | `report/artifacts_summary.md` | this file | small |
| 8 | `report/failure_analysis.md` | honest failure analysis / friction / residual gaps | ~5 KB |

## Traces / evidence

| Path | Content |
|---|---|
| `report/evidence/lwe_base.py` | Classical Dual-Regev PKE at $n{=}8,q{=}257,m{=}128,\sigma{=}3.2$; smoke = 400/400 |
| `report/evidence/bb84_deletion.py` | Pure BB84 layer (16-qubit statevector); honest+cheater experiments |
| `report/evidence/bb84_run.log` | Live output of `bb84_deletion.py` main() |
| `report/evidence/lwe_bb84_full.py` | Combined LWE + BB84 pipeline (17-qubit statevector) |
| `report/evidence/lwe_bb84_full.log` | Live output of `lwe_bb84_full.py` main() |
| `report/evidence/results.json` | Consolidated results (all four functional tests + params + tool versions) |
| `work/paper.pdf` | Copy of the arXiv PDF (dedup of top-level `paper.pdf`) |
| `work/paper.txt` | `pdftotext -layout` output (used both for surrogate extraction and for author/title verification) |
| `extraction/README.md` | Why marker/nougat are surrogated |
| `venv/` | Local Python venv (excluded from git; recreatable via `pip install numpy scipy qiskit qiskit-aer`) |

## How to re-run

```
cd ~/Dropbox/REPLICATE-PROJECT/QC-200/QC-2203.01610-quantum-proofs-deletion-LWE-poremba
python3 -m venv venv && source venv/bin/activate
pip install -q numpy scipy qiskit qiskit-aer
python report/evidence/lwe_base.py       # (a) 400/400
python report/evidence/bb84_deletion.py  # (b),(c),(d),(e) pure BB84
python report/evidence/lwe_bb84_full.py  # combined pipeline
```

Each script prints a JSON summary to stdout that matches
`report/evidence/results.json`.

## Verdict trace

`REPLICATED` — see `report/REPORT.pdf` §Results and §Verdict for the full
table. Consolidated numbers in `report/evidence/results.json` under key
`verdict`.
