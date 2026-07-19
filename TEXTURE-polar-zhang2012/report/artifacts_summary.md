# Artifacts Summary: arXiv:1211.0762 (Zhang, Liu & Zhang 2012)

**Paper:** *Spin-orbital Texture in Topological Insulators*
**Directory:** `textures-100/corpus/textures-polar-zhang2012/` (repo name: `TEXTURE-polar-zhang2012`)
**Verdict:** REPLICATED — Coverage 8/10, Agreement 9/10
**Method:** analytic effective k·p model-Hamiltonian; from-equations reimplementation (no author code)

## The 8-artifact inventory

| # | Artifact | Path | Status |
|---|----------|------|--------|
| 1 | Source paper | `textures-polar-zhang2012.pdf` | present (576 KB) |
| 2 | Marker (prose) extraction | `extraction/marker.md` | INTERIM (pdftotext -layout; marker not installed) |
| 3 | Nougat (math) extraction | `extraction/nougat.mmd` | INTERIM (hand-transcribed LaTeX eqs + pdftotext dump; nougat not installed) |
| 4 | Detailed report + critique | `report/REPORT.tex` | complete (ships as .tex source; pdflatex absent) |
| 5 | Open questions + next steps | `report/open_questions.json` | complete (5 heavy Qs + 5 next_steps) |
| 6 | Workflow + tools/versions | `report/workflow.md` | complete |
| 7 | Artifacts summary (this file) | `report/artifacts_summary.md` | complete |
| 8 | Failure/gap analysis | `report/failure_analysis.md` | complete |
| — | Evidence | `report/evidence/{zhang2012_result.json,zhang2012_checks.json,zhang2012_replicate.py}` | present |
| — | Work/code | `zhang2012_replicate.py` (root), `work/` (empty scratch) | present |

## Headline results traced to evidence

All numbers trace to `report/evidence/zhang2012_result.json` (`quantitative_results` block) and
`report/evidence/zhang2012_checks.json` (raw errors):

| Claim | Evidence-JSON key | Value | Meaning |
|-------|-------------------|-------|---------|
| p_z helical texture | `pz_texture_maxabs_err` | 2.2e-16 | EXACT angular form; LH upper / RH lower |
| p_x texture (Eq.7) | `px_texture_smallk_maxabs_err` | 3.9e-5 | small-k `[sin,cos]` match |
| p_y texture (Eq.8) | `py_texture_smallk_maxabs_err` | 3.9e-5 | small-k `[sin,cos]` match |
| Orbital-char 2θ | `orbital_char_diff_2theta_maxabs_err` | 2.1e-16 | EXACT `cos(2θ)` (π-period) |
| Total in-plane spin | `total_inplane_spin_maxabs_err` | 0.108 | angular form + handedness EXACT; prefactor ×2 convention gap |
| Net handedness | `total_inplane_right_handed_both_cones` | true | RH in-plane orbital spin BOTH cones |
| P_{px} (Eq.10) | `Ppx_Eq10_maxabs_err` | 2.5e-16 | EXACT closed form |
| P_{px} signs | `Ppx_upper_tangential(neg)` / `Ppx_lower_radial(pos)` | true / true | sign flip across Dirac point |
| Norm sanity | `norm_Phi_upper` | 1.064 | consistent |

## Key caveats (see failure_analysis.md)

- **No hexagonal warping** — the paper contains none (isotropic Dirac only); the task framing's
  warping mention refers to a different paper (Fu PRL 2009). Correct scoping, not a gap.
- **Factor-2 prefactor** on total in-plane spin magnitude — an exact, constant convention gap
  (α atom-sum collapse), angular form/handedness exact. Not a physics disagreement.
- **Extraction tooling degraded** (marker/nougat/pdflatex absent) — environment state, not physics.

## Reproduce

```bash
cd /home/stevens/textures-100/corpus/textures-polar-zhang2012
/home/stevens/comfyui-env/bin/python zhang2012_replicate.py
# prints per-claim errors; writes zhang2012_checks.json
# matches report/evidence/zhang2012_result.json
```
