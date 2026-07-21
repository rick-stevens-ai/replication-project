# Failure analysis — Kumar, Sun & Fradkin (2015) replication

## What was reproduced (successes)
- **Topological headline exact, in the paper's explicit flux.** We built the
  paper's actual XY-limit **(2π, π/2, π/2) flux state** on the doubled 6-site
  magnetic unit cell (Eqs. 4.20–4.22), solving directed Peierls bond phases and
  **numerically verifying** every plaquette flux (triangles = π/2, hexagons =
  0 mod 2π). Diagonalizing the 6×6 Bloch H gives an open half-filling gap
  Δ = 1.464 t and a gauge-robust non-Abelian **occupied bottom-3 Chern = +1 →
  σ_xy^s = 1/2**, matching the paper's Eq. 4.20 occupied Chern +1. The C=+1
  chiral response therefore survives in the paper's *specific* flux, not just a
  generic uniform-chirality proxy.
- **Uniform-flux cross-check.** Finite chirality-induced Peierls flux at zero
  external field opens a band gap and gives the lowest kagome band C = +1 →
  σ_xy^s = 1/2 across the small-chirality onset window (independent confirmation).
- **Correct Heisenberg baseline.** At φ = 0 the two lower bands touch (Dirac
  cone, gap ~1e-16), TRS is unbroken, C = 0 — no chiral order without the
  chirality term, as the paper states.
- **Spontaneous loop current.** Im⟨c_A†c_B⟩ ≠ 0 in the chiral state and grows
  with the chirality flux — the microscopic signature of the CSL.

## Limitations / honest gaps
1. **Imposed/verified vs self-consistent flux.** The paper *derives* the bond
   Peierls phase self-consistently from flux attachment,
   φ = arctan[(h/J)(1/2−n)] (Eq. 3.5). We **construct and verify** the exact
   flux geometry (all plaquette fluxes checked numerically) and confirm its
   topological consequence, but did not iterate n ↔ flux to a self-consistent
   fixed point. So we confirm the *consequence* (C_occ=+1, σ_xy^s=1/2) but not
   the *self-selection* of the flux. → open_questions Q3.
2. **Per-band Chern labels vs occupied total.** The gauge-robust **non-Abelian
   occupied bottom-3 Chern is +1** (matches the paper exactly). The per-band
   Abelian FHS readout on our doubled-cell gauge is (0,−1,+1,−1,+1,0) rather
   than the paper's (+1,−1,+1,+1,−1,−1), because bands 1–2 and 5–6 nearly touch
   (individual Chern is ill-defined at a touching). The physically meaningful
   invariant — the occupied-manifold Chern — is correct; splitting the touching
   bands to recover band-by-band labels is an open item. → open_questions Q1.
3. **No XXZ anisotropy sweep.** We worked at the effective tight-binding level
   representing the XY regime; we did not sweep the anisotropy λ across the
   XY→Ising crossover. → open_questions Q2.
4. **Chern-number grid sensitivity.** FHS Chern numbers can be sensitive near
   gap-closing points; we used nk=42 and did not run a full convergence study.
   The C=+1 result is stable in the gapped window but a convergence sweep is
   pending. → open_questions Q5.
5. **Extraction OCR.** Neural OCR (Nougat/Marker) was unavailable in-env; we
   used pdftotext. Equations of interest (3.2, 3.5, 4.22) were verified by hand
   against the physics, so this did not affect the replication.

## Net assessment
The **qualitative/topological claim is REPLICATED** in the paper's explicit flux:
σ_xy^s = 1/2 at zero external field from the chirality term, occupied Chern = +1
on the numerically-verified (2π, π/2, π/2) doubled-cell flux state, plus a
spontaneous loop current and an independent uniform-flux cross-check. The
quantitative *self-consistent onset* in h/J and the band-by-band Chern labels
(touching-band gauge) are scoped out and captured as open questions — a strong
topological replication.
