# Artifacts Summary

Target dir: `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-0102136-entanglement-simulations-shor/`

## Required 8 artifacts (per QC_WAVE_BRIEF_2026-07-03.md)

| # | Artifact | Path | Status |
|---|---|---|---|
| 1 | `paper.pdf` | `paper.pdf` (320830 bytes, 18 pp, v2) | ✅ present |
| 2 | Marker parse | `extraction/marker.md` | ⚠️ **surrogate** — Marker CLI not installed on CherryRd; produced from pdftotext + hand-cleanup, clearly labeled at top |
| 3 | Nougat parse | `extraction/nougat.mmd` | ⚠️ **surrogate** — Nougat not installed; MathPix-Markdown-style file produced from pdftotext, clearly labeled |
| 4 | LaTeX report | `report/REPORT.tex` (+ `report/REPORT.pdf` if compile succeeds) | ✅ present |
| 5 | 5 open questions JSON | `report/open_questions.json` (each `{q, basis, next_steps}`, 5 items) | ✅ present |
| 6 | Workflow doc | `report/workflow.md` | ✅ present |
| 7 | Artifacts summary | `report/artifacts_summary.md` (this file) | ✅ present |
| 8 | Failure analysis | `report/failure_analysis.md` | ✅ present |

## Evidence / code

| Path | What it is |
|---|---|
| `report/evidence/shor_entanglement.py` | Full Qiskit implementation: 3+4 qubit Shor for N=15 a=2, coherent + non-selective-measurement traces, all-63-bipartitions log-negativity, no-entanglement control. Reproducible. |
| `report/evidence/shor_entanglement_results.json` | Machine-readable snapshot values: coherent snapshots, measurement snapshots, control snapshots, and summary averages. |
| `work/paper.txt` | `pdftotext -layout` dump of `paper.pdf`; input to extraction surrogates and manual claim extraction. |

## Repro command

```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-0102136-entanglement-simulations-shor
python3 -m venv .venv && source .venv/bin/activate
pip install --quiet qiskit numpy scipy
python report/evidence/shor_entanglement.py
```

Expected: `report/evidence/shor_entanglement_results.json` regenerated, terminal prints the same 9-stage table shown in `REPORT.tex` Results section.

## Provenance / trace summary

- **arXiv fetch**: `https://arxiv.org/pdf/quant-ph/0102136` on 2026-07-05, 320830 bytes.
- **Authors verified from PDF**: S. Parker, M. B. Plenio (Imperial College, Blackett Lab).
- **Version**: v2, dated Sep 12 2001.
- **Central claim source**: Section VI + Figs 7-16 of paper.pdf; principally Figs 11 & 15 (the pure-state N=15 a=2 curves) which are what we compared against.
- **Sim tool**: Qiskit 2.5.0 exact statevector + density matrix.
- **No third-party numbers copied in.**
