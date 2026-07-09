# Artifacts summary

## Public artifacts fetched

| Artifact | Source | Size | SHA-256 (first 16 chars) |
|---|---|---|---|
| paper.pdf | https://arxiv.org/pdf/quant-ph/0410184 | 111,420 B | `a13d655d7dd8f605` |

That's the only external artifact — this paper has no supplementary
material or dataset. All other content in this directory was generated
by the replication run.

## Files in target dir

```
QC-quant-ph0410184-ripple-carry-adder-cuccaro/
├── paper.pdf                       (original PDF, 111 KB)
├── extraction/
│   ├── marker.md                   (pdftotext -layout fallback, 372 lines)
│   └── nougat.mmd                  (pdftotext fallback, 911 lines)
├── work/
│   ├── .venv/                      (Python 3.14 venv, qiskit 2.5.0)
│   ├── paper.txt                   (raw pdftotext)
│   ├── cdkm.py                     (adder implementation)
│   ├── verify_fast.py              (classical-basis exhaustive harness)
│   ├── verify_statevector.py       (superposition sanity check)
│   ├── draper_control.py           (Draper QFT-adder control)
│   ├── verify_results.json         (288896 / 288896 pass)
│   ├── statevector_check.json      (all amplitudes match)
│   └── draper_results.json         (15/15 spot-checks pass)
└── report/
    ├── REPORT.md                   (main narrative report)
    ├── REPORT.tex                  (LaTeX detailed section-by-section)
    ├── open_questions.json         (5 heavy questions with next_steps)
    ├── workflow.md                 (this run's workflow + tools)
    ├── artifacts_summary.md        (this file)
    ├── failure_analysis.md         (what failed and how it was fixed)
    └── evidence/
        ├── cdkm.py                 (mirror)
        ├── verify_fast.py          (mirror)
        ├── verify_statevector.py   (mirror)
        ├── draper_control.py       (mirror)
        ├── verify_results.json     (mirror)
        ├── statevector_check.json  (mirror)
        ├── draper_results.json     (mirror)
        └── llm_judge_response.json (Argo gpt-5.2 verdict blob)
```

## Reproducibility recipe

```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph0410184-ripple-carry-adder-cuccaro
python3 -m venv work/.venv && source work/.venv/bin/activate
pip install qiskit qiskit-aer
cd work
python cdkm.py                # resource counts
python verify_fast.py         # ~80s -> 288896/288896 PASS
python verify_statevector.py  # <1s -> all superposition amplitudes correct
python draper_control.py      # ~5s -> 15/15 Draper spot-checks PASS
```
