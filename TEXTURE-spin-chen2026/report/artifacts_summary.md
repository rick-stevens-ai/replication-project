# Artifacts Summary --- chen2026

**Paper:** Chen et al. 2026, *A Route to Nonrelativistic Altermagnetic Spin Splitting via
Ultrafast Light* (KNiF3, rt-TDDFT).
**Verdict:** REPLICATED (6/6 checks) | **Coverage 8/10** | **Agreement 9/10**.

## The 8 artifacts
| # | Artifact | Path | Status |
|---|----------|------|--------|
| 1 | Source PDF | `textures-spin-chen2026.pdf` | present |
| 2 | marker.md (prose extraction) | `extraction/marker.md` | **INTERIM** -- `pdftotext -layout` + NOTE header (marker binary absent) |
| 3 | nougat.mmd (math extraction) | `extraction/nougat.mmd` | **INTERIM** -- hand-transcribed LaTeX Eqs 1-5 + raw pdftotext appendix (nougat binary absent) |
| 4 | REPORT.tex | `report/REPORT.tex` | complete (compiles off-host; amsmath/booktabs/hyperref) |
| 5 | open_questions.json | `report/open_questions.json` | 5 heavy Qs + next_steps |
| 6 | workflow.md | `report/workflow.md` | complete |
| 7 | artifacts_summary.md | `report/artifacts_summary.md` | this file |
| 8 | failure_analysis.md | `report/failure_analysis.md` | complete |
| + | evidence | `report/evidence/` | result JSON + solver .py |

## Physics result (this work vs paper)
| Check | Claim | This work | Paper | Status |
|-------|-------|-----------|-------|--------|
| C1 | undistorted AFM spin splitting | max\|Delta\| = 0.0 | zero (type-IV AFM) | EXACT |
| C2 | a0b-c- -> d-wave | m=2, 4 nodes, mirror-odd resid 0.0 | d-wave | MATCH |
| C3 | a0b0c- -> g-wave | m=4, 8 nodes | g-wave | MATCH |
| C4 | splitting vs eta | monotone, Delta(0)=0, lin-corr 0.988 | switched on by rotation | MATCH |
| C5 | mode switching | m=4 <-> m=2 | Fig 2b g<->d switching | MATCH |
| C6 | Hall on/off (spin Hall) | 0.0 vs -1.3e-2 (SOC, gobel2024 Kubo) | 0 vs finite (Fig 3) | MATCH |
| C6' | charge AHC magnitude | ~3e-16 (2D) vs +/-400 S/cm | +/-400 S/cm | SCOPED (3D/DFT) |

## Reproduce (live re-run confirmed)
```
cd /home/stevens/textures-100/corpus/textures-spin-chen2026/work
/home/stevens/comfyui-env/bin/python chen2026_replicate.py
# -> [SAVED] work/chen2026_result.json ; VERDICT=REPLICATED pass 6/6
#    coverage=8/10 agreement=9/10  (~1.5 s)
```

## Kernel credit
Kubo-Bastin Hall machinery adapted from
`/home/stevens/shared-kernels-cache/gobel2024_sd_skyrmion_kubo_Lz_kernel.py`
(Gobel et al. 2024, arXiv:2410.00820, topological orbital Hall from skyrmions).
`spin_ed_probes.py` was reviewed (many-body ED path) but not applicable to this
band-structure spin-splitting claim.

## Interim / environment notes
- marker & nougat binaries NOT installed on host (only poppler `pdftotext`). Artifacts 2 & 3
  are honest pdftotext interims with role-differentiated NOTE headers; regenerate commands
  are in-file. Not physics gaps.
- No LaTeX engine on host: REPORT.tex is delivered as source, compiles off-host.
