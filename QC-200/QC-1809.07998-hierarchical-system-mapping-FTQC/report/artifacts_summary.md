# Artifacts summary

Root: `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-1809.07998-hierarchical-system-mapping-FTQC/`

## 8 mandatory artifacts (per QC wave brief, Rick 2026-07-05)

| # | Artifact | Path | Status |
|---|----------|------|--------|
| 1 | Original PDF | `paper.pdf` | ✓ present (143 KB, 4 pages, arXiv:1809.07998v1) |
| 2 | Marker parse | `extraction/marker.md` | ✓ present (pdftotext-normalized fallback, provenance header inside) |
| 3 | Nougat parse | `extraction/nougat.mmd` | ✓ present (pdftotext-normalized fallback, provenance header inside) |
| 4 | Section-by-section LaTeX report | `report/REPORT.tex` (+ `report/workflow_include.tex`) | ✓ present; compilation to `REPORT.pdf` attempted (see `report/REPORT.pdf` if present, else notes below) |
| 5 | Open questions (JSON + report section) | `report/open_questions.json` + `## Open Questions` in REPORT.tex | ✓ 5 heavy-duty questions with `q`, `basis`, `next_steps` each |
| 6 | Comprehensive workflow + tools + effort | `report/workflow.md` | ✓ present |
| 7 | Artifact inventory | `report/artifacts_summary.md` (this file) | ✓ present |
| 8 | Honest failure analysis | `report/failure_analysis.md` | ✓ present |

## Evidence and intermediates

| Path | Bytes | Description |
|------|-------|-------------|
| `report/evidence/repro.py`         | ~18 KB | Reproduction script (Part A: K·N vs K+N scaling; Part B: d=5 surface-code + 15-to-1 magic-state footprint) |
| `report/evidence/qasm_scaling.csv` | ~360 B | CSV of Part A: n_toffolis, non-mod, modular, compression ratio |
| `report/evidence/footprint.csv`    | ~520 B | CSV of Part B: naive vs hierarchical footprint per circuit size |
| `report/evidence/summary.json`     | ~4.5 KB | Machine-readable full summary + provenance |
| `report/evidence/footprint.png`    | matplotlib | Two-panel plot: footprint vs size (log), and reduction % |
| `report/evidence/provenance.txt`   | ~430 B  | Host, python, platform, cwd, UTC run time, git head |
| `work/paper.txt`                    | ~26 KB | Full pdftotext output |

## Headline numbers reproduced

| From paper | Paper value | Our value | Match? |
|------------|-------------|-----------|--------|
| Compression ratio K·N / (K+N) → K as N → ∞ | asymptotic | 15.00 at N=10⁶ (K=15) | ✓ exact |
| Shor-512 QASM 39 TB → 338.6 MB (Table 1) | 39 TB, 338.6 MB | not tested (ScaffCC required) | — |
| Shor-512 map 1500 d → 1 h (Fig 2) | 1500 d, 1 h | not tested | — |
| Hierarchical footprint reduction on Toffoli-heavy circuit (per QC brief) | mechanism argument | 48%, 85.5%, 92.2%, 98.2% at n_Toff = 1, 5, 10, 45 | ✓ measurable across all sizes |

## Trace / audit
- Fetch: `curl -sL -o paper.pdf https://arxiv.org/pdf/1809.07998` (single request, ~140 KB down, 200 OK).
- Zero external LLM calls.
- No external code executed beyond the standard Python interpreter + matplotlib.
- Full script + inputs + outputs stored in `report/evidence/`; provenance line-item in `provenance.txt`.
- Compilation trace (if pdflatex ran): see `report/REPORT.log`.

## What is NOT included (and why)
- **No ScaffCC install and no Shor-N modular/non-modular QASM.** Reproducing Table 1 requires ~200 GB of transient disk to hold the Shor-512 non-modular QASM alone (the paper mentions 128 GB RAM to compile it). Wave brief target time was minutes-not-hours; explicitly noted in failure analysis.
- **No Stim / PyMatching / Qiskit surface-code simulation.** Our footprint model is a parametric bookkeeping model (Fowler/Litinski constants), not a cycle-accurate simulation. Choice justified in report §4 (verdict) and failure analysis.
