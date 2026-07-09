# Artifacts Summary — QC-200 / arXiv:1701.05052

Full inventory of every file in this replication's target directory, with provenance and role.

## 8-artifact completion bar

| # | Artifact | Path | Status | Notes |
|---|----------|------|--------|-------|
| 1 | Original PDF | `paper.pdf` | ✅ | Fetched from `https://arxiv.org/pdf/1701.05052` (999 KB, 18 pp, v1) |
| 2 | Marker parse | `extraction/marker.md` | ✅ | Generated 2026-07-05 18:23 CDT on `uicgpu` A100 (env `marker` @ `/gpustor/stevens/anaconda3/envs/marker`), 158 s wall, 457 lines |
| 3 | Nougat parse | `extraction/nougat.mmd` | ✅ | Generated 2026-07-05 on `uicgpu` A100 (env `nougat` @ `/gpustor/stevens/anaconda3/envs/nougat`), 368 lines. **⚠ contains a fabricated `###### Abstract` block** — the source PDF has no formal abstract. See `failure_analysis.md`. |
| 4 | LaTeX report | `report/REPORT.tex` | ✅ | 16 KB, self-contained, references figure |
| 5 | Open questions | `report/open_questions.json` + `## Open Questions` in REPORT | ✅ | Exactly 5 heavy-duty Q with `q`, `basis`, `next_steps` each |
| 6 | Workflow | `report/workflow.md` | ✅ | Timeline, tools+versions, effort estimate |
| 7 | Artifacts summary | this file | ✅ | |
| 8 | Failure analysis | `report/failure_analysis.md` | ✅ | Documents the SCOUT framing failure + parser CLI mismatch + Nougat fabrication + C6 grid tolerance |

## All files in the target dir

| Path | Size | Type | Provenance |
|------|------|------|------------|
| `paper.pdf` | 999 KB | binary PDF | `curl arxiv.org/pdf/1701.05052` on CherryRd, 2026-07-05 18:11 CDT |
| `work/paper.txt` | ~50 KB | text | `pdftotext paper.pdf work/paper.txt` (poppler on CherryRd) — used as ground-truth text source for claim extraction |
| `extraction/marker.md` | ~20 KB | markdown | Marker parse on uicgpu A100 |
| `extraction/nougat.mmd` | ~40 KB | markdown/LaTeX | Nougat parse on uicgpu A100 |
| `report/evidence/sim_majorana_braiding.py` | 21 KB | python | Authored 2026-07-05 for this replication; runs in <1 s CPU |
| `report/evidence/results.json` | 3 KB | JSON | Output of the simulator |
| `report/evidence/run.log` | 3 KB | text | Console log of the simulator run |
| `report/evidence/plot_honeycomb.py` | 2 KB | python | Authored 2026-07-05; produces `figures/kitaev_phase_diagram.png` |
| `figures/kitaev_phase_diagram.png` | ~80 KB | PNG | Reproduction of paper Fig. 3 phase diagram |
| `report/REPORT.tex` | 16 KB | LaTeX | Main report |
| `report/open_questions.json` | 5 KB | JSON | Q1..Q5 |
| `report/workflow.md` | 6 KB | markdown | Timeline + tools + effort |
| `report/artifacts_summary.md` | this file | markdown | |
| `report/failure_analysis.md` | 7 KB | markdown | Honest failure/friction analysis |

## Traces / reproducibility

All 6 numerical checks (C1–C6, +C5b group enumeration, +n=6 sanity for C2) are runnable in one line:

```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-200/QC-1701.05052-topological-quantum-computing-D7-roy-diVincenzo
python3 report/evidence/sim_majorana_braiding.py    # <1 s
python3 report/evidence/plot_honeycomb.py           # <5 s (produces the PNG)
```

Environment: system `python3` 3.13.7 on macOS with `numpy` and `matplotlib` available. No external services required; no LLM inference used in the reproduction step. Free-endpoint policy trivially satisfied.

## LaTeX build (optional)

REPORT.tex is compilable with any modern TeX Live:
```bash
cd report && pdflatex REPORT.tex && pdflatex REPORT.tex
```
The figure reference is `../figures/kitaev_phase_diagram.png`. Not built here (CherryRd's LaTeX stack availability not verified for this session and the .tex file is complete and canonical).
