# Artifacts summary — arXiv:0708.1879 replication

All paths relative to `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-0708.1879-quantum-random-access-memory-vittorio/`.

## 8-artifact completion bar (Rick 2026-07-05)

| # | Required artifact | Present? | Path |
|---|---|---|---|
| 1 | Original PDF | ✅ | `paper.pdf` (also mirrored at `work/paper.pdf`) |
| 2 | Marker parse (or documented surrogate) | ✅ | `extraction/marker.md` (PyMuPDF surrogate — see `extraction/README.md`) |
| 3 | Nougat parse (or documented surrogate) | ✅ | `extraction/nougat.mmd` (`pdftotext -layout` surrogate) |
| 4 | Detailed LaTeX report | ✅ | `report/REPORT.tex` + compiled `report/REPORT.pdf` |
| 5 | 5 open questions (JSON + report section) | ✅ | `report/open_questions.json` + `## Open Questions` in `REPORT.md`/`REPORT.tex` |
| 6 | Workflow + tool inventory + work estimate | ✅ | `report/workflow.md` |
| 7 | Artifact inventory (this file) | ✅ | `report/artifacts_summary.md` |
| 8 | Honest failure analysis | ✅ | `report/failure_analysis.md` |

## Evidence & code

| Path | Type | Purpose |
|---|---|---|
| `report/evidence/bucket_brigade_qram.py` | Python | BB-qRAM simulator (Full-register at n=2; reduced-subspace at n=2,3,4) |
| `report/evidence/scaling.json` | JSON | Machine-readable scaling table + fidelity results |
| `report/evidence/bucket_brigade_run.log` | log | stdout of the simulator run |
| `report/evidence/bb_qram_n2.qasm` | QASM | Oracle-equivalent BB-qRAM circuit at n=2 (address prep + address-conditioned bus XOR + labelled BB routing barriers) |
| `report/evidence/llm_judge.py` | Python | LLM-judge script |
| `report/evidence/llm_judge_result.json` | JSON | Judge response (`argo:gpt-5.4`, temperature 0) |
| `report/evidence/llm_judge_stdout.log` | log | Judge stdout |

## Intermediates

| Path | Purpose |
|---|---|
| `work/paper.pdf` | Fetched arXiv PDF (mirror of root `paper.pdf`) |
| `work/paper.txt` | `pdftotext` skim for claim identification |
| `work/venv` | Symlink to sibling QC-100 venv (Qiskit 2.5.0 + Aer 0.17.2 + PyMuPDF 1.28.0) |

## Trace of key numeric results (source of truth)

From `report/evidence/scaling.json` and `bucket_brigade_run.log`:

```
Full-register n=2 (dim=512, addr+trit+bus = 9 qubits):
  |a=0..3> readout: all four fidelities = 1.000000000000
  uniform-superposition fidelity vs (1/sqrt N) Sum |a>|D[a]>: 1.000000000000

Reduced-subspace n=2,3,4 (dim=8, 16, 32):
  single-address pass: 4/4, 8/8, 16/16
  uniform-superposition fidelity: 1.0, 1.0, 1.0
  active switches BB/call:      2, 3, 4    (= log2 N: True)
  active switches naive/call:   3, 7, 15   (= N-1:   True)
  total tree nodes:              3, 7, 15   (= N-1:   True)
```

## LLM-judge verdict (Argo `argo:gpt-5.4`)
`{h1: YES, h2: YES, h3: YES, verdict: PARTIAL}` — see `report/evidence/llm_judge_result.json` for the full response including caveats.
