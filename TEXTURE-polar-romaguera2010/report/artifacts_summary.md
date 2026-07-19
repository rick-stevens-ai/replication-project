# Artifacts Summary — arXiv:1001.1715 Reduced Replication

| # | Artifact | Path | Description |
|---|----------|------|-------------|
| 1 | Replication code | `code/romaguera2010_replication.py` | Reduced 2D GL cross-section solver (TDGL relaxation, fixed dipole A, Peierls covariant Laplacian); thin-disk + thick-rod layer stack; plaquette phase-singularity vortex finder; figure generation. CPU-only, numpy/scipy/matplotlib. |
| 2 | Results (machine-readable) | `work/results.json` | Per-geometry winding, net topological charge, vortex-core positions/charges, core RMS radius, mean\|Ψ\|², free energy; per-claim {expectation, observed, reproduced, match, note}; summary + verdict. |
| 3 | Figure: thin disk | `figs/thin_disk_psi2.png` | \|Ψ\|² map of thin disk (D=2ξ) with vortex markers → single central giant vortex (W=2). |
| 4 | Figure: thick rod layers | `figs/thick_rod_layers_psi2.png` | \|Ψ\|² maps at three z-layers of the thick rod (D=6ξ), top/mid/bottom → structure changes with depth. |
| 5 | Figure: depth profile | `figs/thick_depth_profile.png` | Winding, #cores, and mean\|Ψ\|² vs depth for the thick rod → winding 6→0, \|Ψ\|² rising toward the bottom (Meissner retained). |
| 6 | Report (LaTeX + PDF) | `report/REPORT.tex`, `report/REPORT.pdf` | Full narrative: method, reduced-scope rationale, results, per-claim scoring, figures. |
| 7 | Open questions | `report/open_questions.json` | 5 open questions (q, basis, next_steps): 3D line, D-crossover, reentrant Meissner, self-consistent A, Table-1 quantitative match. |
| 8 | Process docs | `report/workflow.md`, `report/artifacts_summary.md`, `report/failure_analysis.md` | Workflow, this summary, and failure/limitation analysis. |

Supporting (pre-existing): `paper.pdf`, `extraction/marker.md`, `report/method_extract.md`, `META.json` (updated with status + verdict).

## Headline results (numbers)
- **Thin disk D=2ξ (μ=25):** winding **W=2**, both phase singularities at core RMS radius **0.05 ξ** (piled at center) → **GIANT VORTEX**. match=yes.
- **Thick rod D=6ξ (μ=25):** winding by depth (top→bottom) = **6 → 1 → 0 → 0 → 0**; mean\|Ψ\|² = **0.00 → 0.22 → 0.33 → 0.37 → 0.38**; top-layer cores spread (RMS 1.86 ξ), bottom fully Meissner. match=partial.
- **Thickness crossover:** thin = uniform giant; thick = depth-varying/curved → qualitatively different. match=partial.

**Verdict: PARTIAL** — reduced model reproduces the thickness-dependent mechanism (giant vs curved/top-to-side + Meissner-at-bottom) but not the full 3D curved vortex line or exact Table-1 μ-sequences.
