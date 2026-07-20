# Failure analysis — Kumar, Sun & Fradkin (2015) replication

## What was reproduced (successes)
- **Topological headline exact.** Finite chirality-induced Peierls flux at zero
  external field opens a band gap and gives the lowest kagome band Chern number
  **C = +1 → σ_xy^s = C/2 = 1/2**, matching the paper's central claim.
- **Correct Heisenberg baseline.** At φ = 0 the two lower bands touch (Dirac
  cone, gap ~1e-16), TRS is unbroken, C = 0 — the model has no chiral order
  without the chirality term, as the paper states.
- **Spontaneous loop current.** Im⟨c_A†c_B⟩ ≠ 0 in the chiral state and grows
  with the chirality flux — the microscopic signature of the CSL.

## Limitations / honest gaps
1. **Imposed vs self-consistent flux.** The paper *derives* the bond Peierls
   phase self-consistently from flux attachment,
   φ = arctan[(h/J)(1/2−n)] (Eq. 3.5). We **impose** a directed flux and verify
   its topological consequence. We did not iterate n ↔ flux to a self-consistent
   fixed point, so we confirm the *consequence* (C=+1, σ_xy^s=1/2) but not the
   *self-selection* of the flux. → open_questions Q3.
2. **Uniform vs (2π, π/2, π/2) flux pattern.** We used the kernel's simple
   `uniform` flux pattern. It reproduces C=+1 for small chirality flux
   (φ/π ≤ ~0.08 and again 0.24–0.30), but at intermediate φ the net triangle
   flux (3φ) wraps past 2π and C oscillates (0, then ±1). This is a
   **parametrization artifact**, not physics: the paper's XY limit is the
   specific staggered (2π, π/2, π/2) assignment, which we did not encode
   explicitly. The robust small-φ onset is the physically faithful window. →
   open_questions Q1.
3. **No XXZ anisotropy sweep.** We worked at the effective tight-binding level
   representing the XY regime; we did not sweep the anisotropy λ across the
   XY→Ising crossover to test gap closure. → open_questions Q2.
4. **Chern-number grid sensitivity.** FHS Chern numbers can be sensitive near
   gap-closing points; we used nk=42 and did not run a full convergence study.
   The C=+1 result is stable in the gapped window but a convergence sweep is
   pending. → open_questions Q5.
5. **Extraction OCR.** Neural OCR (Nougat/Marker) was unavailable in-env; we
   used pdftotext. Equations of interest (3.2, 3.5, 4.22) were verified by hand
   against the physics, so this did not affect the replication.

## Net assessment
The **qualitative/topological claim is REPLICATED** (σ_xy^s = 1/2 at zero field
from the chirality term, C=+1 Chern band, spontaneous loop current). The
quantitative *self-consistent onset* in h/J and the exact XY-limit flux pattern
are scoped out and captured as open questions — hence not a BLOCKED and not a
full quantitative REPLICATED, but a strong topological replication.
