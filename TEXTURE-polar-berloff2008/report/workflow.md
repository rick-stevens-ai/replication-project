# Workflow — Berloff 2008 (arXiv:0801.2964) replication

**Paper:** N. G. Berloff, *Vortex Splitting in Subcritical Nonlinear Schrödinger
Equations*, arXiv:0801.2964 (2008).
**Method class:** nonlinear PDE time-integration / Gross–Pitaevskii (cubic–quintic
"subcritical" NLS).
**Reimplementation:** independent, from Eqs (16), (21), (41); **not** author code.

## Pipeline (acquire → parse → extract → build → run → compare → report)

1. **Acquire.** PDF already present: `textures-polar-berloff2008.pdf` (arXiv v1,
   17 Jan 2008), 460 KB. Reading-order text `textures-polar-berloff2008.txt`
   (1316 lines) already extracted.
2. **Parse / extract.** `marker` and `nougat` binaries are **not installed** on
   this host — only `pdftotext` (poppler) is available. Interim extractions:
   - `extraction/marker.md` — `pdftotext -layout` (structure-preserving), headed
     with a NOTE flagging the interim status.
   - `extraction/nougat.mmd` — `pdftotext` reading-order, headed likewise.
   Regenerate with `marker_single` / `nougat` when a GPU host with the models is
   available.
3. **Extract method/params.** Governing equation reconciled by hand from the
   paper text so bulk ψ=1 is an exact fixed point of Eq (16) AND Eq (21) is its
   radial profile — the sign-reconciliation step that pins units.
4. **Build.** Two from-scratch Python (numpy/scipy) codes:
   - `work/vortex_profile.py` — Part A: 1D radial profile ODE (Eq 21) via Newton
     relaxation with an analytic tridiagonal Jacobian (Thomas solve).
   - `work/vortex_split_2d.py` — Part B: 2D Strang split-step Fourier integrator
     of Eq (16) with an absorbing sponge and plaquette-winding vortex tracker.
   - `work/save_result.py` — driver: runs both, assembles per-claim verdict,
     writes `berloff2008_result.json`.
5. **Run.**
   - Part A: <1 s (1D relaxation, N=3000).
   - Part B: ~28 s (N=128, L=48, dt=0.004, T=200) on CPU.
6. **Compare.** Statics vs paper Table 1 / text (a1, ξ_crit) → ~1% match.
   Dynamics vs Figs 6/7 (core breathing) and the "only s=±1 stable" claim
   (charge-2 topological resolution with conserved circulation).
7. **Report.** This 8-artifact package.

## Tools / versions
- Python: `/home/stevens/comfyui-env/bin/python` (numpy + scipy).
- `scipy.ndimage` for plaquette clustering (`ndimage.label`).
- `pdftotext` (poppler-utils) for interim text extraction.
- `marker` / `nougat`: **absent** (flagged).

## Key techniques (see also the `computational-replication-execution` skill,
NLS/GPE section)
- Reconcile the equation's signs against a stationary solution BEFORE coding.
- Validate the stationary 1D profile FIRST (cheap, pins units) before 2D/3D.
- Strang split-step Fourier: half-kinetic (k-space) / full-nonlinear (real) /
  half-kinetic; absorbing sponge for radiated sound.
- Track TOPOLOGY (2π phase winding on plaquettes) + conserved total charge, not
  a density threshold, for vortex counting.

## Effort estimate
- Statics build + validate: ~1 h.
- 2D dynamics build + sponge + winding tracker + tuning: ~2–3 h.
- Packaging (this report set): ~0.5 h.
- **Total ≈ 4 h** of focused work for a PARTIAL replication of a nontrivial
  time-dependent nonlinear-PDE paper.

## What was NOT built (see failure_analysis.md / open_questions.json)
- 3D axisymmetric vortex-RING solver (the paper's headline Figs 8/9).
- Exact s=2 stationary profile / BdG growth-rate analysis.
- Renormalized energy/impulse/velocity and core-energy l(t) diagnostics.
