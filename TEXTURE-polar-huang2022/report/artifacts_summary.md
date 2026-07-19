# Artifacts Summary --- huang2022 (arXiv:2202.11348)

## The 8-artifact bar

| # | Artifact | Path | Status |
|---|----------|------|--------|
| 1 | Source paper | `textures-polar-huang2022.pdf` | present (3.7 MB) |
| 2 | Marker extraction (prose) | `extraction/marker.md` | **interim** (pdftotext -layout; marker absent) |
| 3 | Nougat extraction (math) | `extraction/nougat.mmd` | **interim** (hand-transcribed eqs + pdftotext dump; nougat absent) |
| 4 | Report | `report/REPORT.tex` | complete (.tex source; no LaTeX engine on host) |
| 5 | Open questions | `report/open_questions.json` | complete (5 Qs + next_steps) |
| 6 | Workflow | `report/workflow.md` | complete |
| 7 | Artifacts summary | `report/artifacts_summary.md` | this file |
| 8 | Failure analysis | `report/failure_analysis.md` | complete |
| + | Evidence | `report/evidence/` | result JSON + code + sim output |
| + | Work | `work/` | `skyrmion.py`, result JSONs (gitignored) |

## Evidence inventory (`report/evidence/`)
- `huang2022_result.json` --- per-claim checks + verdict block (coverage 7, agreement 7).
- `skyrmion.py` --- the from-scratch micromagnetic relaxer (square lattice,
  Neel DMI, overdamped LLG, Berg--Luscher charge, analytic D_c).
- `_sim_out.json` --- raw per-case simulation output ($D_c$ + 4 cases).

## Headline numbers (traced to evidence)
| Quantity | Value | Source key |
|----------|-------|-----------|
| Analytic critical DMI $D_c$ | 0.255 mJ/m$^2$ | `_sim_out.json:Dc_mJm2` (0.2546) |
| $D_\uparrow=0.28$: skyrmion | yes, $Q=-0.87$, 39.5 nm | `_sim_out.json:cases.D_up` |
| $D_\downarrow=0.06$: skyrmion | no, $Q=0$, 0 nm | `_sim_out.json:cases.D_down` |
| $D_{\uparrow\uparrow}=0.22$: skyrmion | yes, $Q=-0.90$, 19.9 nm | `_sim_out.json:cases.D_upup` |
| $D_{\downarrow\downarrow}=-0.24$: skyrmion | yes, $Q=-0.99$, 28.2 nm | `_sim_out.json:cases.D_downdown` |
| Verdict | PARTIAL (mechanism replicated) | `huang2022_result.json:verdict` |

**Verification during packaging:** the kernel was re-executed live
(`/home/stevens/comfyui-env/bin/python`); output matched the saved JSON to the
quoted digits ($D_c=0.255$; D_up 39.54 nm/Q=-0.871; D_down 0/0; D_upup
19.87/-0.902; D_downdown 28.19/-0.987).

## Reproduce block
```bash
cd /home/stevens/textures-100/corpus/textures-polar-huang2022
/home/stevens/comfyui-env/bin/python work/skyrmion.py
# prints: A, K, analytic Dc, and per-case {diameter, Q, sky}; writes work/_sim_out.json
```

## Extraction-tooling note (not a physics gap)
`marker` and `nougat` are not installed on this host; only `pdftotext` (poppler)
is available. Artifacts 2 & 3 are the documented pdftotext interims with honest
provenance headers. The paper's key equations (spin Hamiltonian Eq.5, skyrmion
radius Eq.6, critical-DMI criterion) are hand-transcribed into LaTeX in both
`extraction/nougat.mmd` and `report/REPORT.tex`, which are the authoritative math
sources. Regenerate the real extractions with:
`marker_single textures-polar-huang2022.pdf extraction/ --output_format markdown`
and `nougat textures-polar-huang2022.pdf -o extraction/ --markdown`.
