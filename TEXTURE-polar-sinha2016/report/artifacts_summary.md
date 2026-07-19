# Artifacts Summary — Sinha 2016 replication package

**Paper:** Debabrata Sinha, *Spin texture of an irradiated warped topological
insulator surface*, arXiv:1604.04081v2 (EPL, 2016).
**Verdict:** REPLICATED · Coverage ~8/10 · Agreement ~9/10.
**Base dir:** `/home/stevens/textures-100/corpus/textures-polar-sinha2016/`

## The 8 artifacts

| # | Artifact | Path | Description |
|---|----------|------|-------------|
| 1 | Report (LaTeX) | `report/REPORT.tex` | Full replication writeup: model, methods, results tables, verdict, honest gaps. Ships as `.tex` source (no `pdflatex`/`tectonic` in env). |
| 2 | Open questions | `report/open_questions.json` | 5 heavy open questions (Q1–Q5) + `next_steps`. |
| 3 | Workflow | `report/workflow.md` | Step-by-step method: transcription → units → params → dual-route cross-check → claim checks. |
| 4 | Artifacts summary | `report/artifacts_summary.md` | This file. |
| 5 | Failure analysis | `report/failure_analysis.md` | Traps caught (60° symmetry-angle trap, k=0 singularities, band selection, sign conventions, tool absence). |
| 6 | Extraction — marker | `extraction/marker.md` | Markdown transcription (interim: pdftotext-normalized, marker binary absent). |
| 7 | Extraction — nougat | `extraction/nougat.mmd` | Mathpix-markdown equation dump (interim: pdftotext-normalized, nougat binary absent). |
| 8 | Evidence (result JSON) | `report/evidence/sinha2016_result.json` | Machine-readable numeric results + verdict. Code copy: `report/evidence/sinha2016_floquet.py`. |

Supporting: `extraction/pdftotext_layout.txt` (raw interim OCR),
`work/sinha2016_floquet.py` (source of truth for the run).

## Key numbers reproduced

| Quantity | Paper | This work |
|----------|-------|-----------|
| `Δω` @ evA0=0.5 | 0.03 eV | 0.0312 eV |
| `Δω` @ evA0=0.9 | 0.10 eV | 0.1013 eV |
| `a` @ evA0=0.5 | 0.17 nm | 0.17 nm (calib) |
| `a` @ evA0=0.9 | 0.55 nm | 0.5508 nm (calib) |
| Induced gap `2Δω` @ evA0=0.9 | 0.20 eV | 0.2025 eV |
| `Sz(k=0)` gapped | +ħ/2 | +1 (ħ/2 units) |
| `Sz(k=0)` gapless | 0 | 0 |
| Analytic vs numeric energy err | — | 0.0 eV (machine precision) |
| Analytic vs numeric spin err | — | 0.0 (machine precision) |

## Two claims (both confirmed)
- **A. Light-induced TR-breaking gap** `2Δω = (evA0)²/ħω × 2` at the Dirac point;
  `Sz` jumps to +ħ/2 at k=0.
- **B. Broken spin-momentum locking**: `δω(θ) ∝ sin(3θ)`, nonzero for `a≠0`
  except along Γ–K and θ=π/3; identically zero for the gapless (`a=0`) TI.

## Reproduce
```
/home/stevens/comfyui-env/bin/python \
  /home/stevens/textures-100/corpus/textures-polar-sinha2016/work/sinha2016_floquet.py
```

## Known limitations (see REPORT §7 / failure_analysis)
- `a` empirically calibrated (`a≈0.68(evA0)² nm`); paper never fixes bare `v`.
- No full 2D colormaps (Figs 1–5); point/line checks only.
- Leading van Vleck term only; higher-order Magnus & `Hhw` warping not included.
