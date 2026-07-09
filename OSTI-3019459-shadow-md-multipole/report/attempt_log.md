# Attempt Log — OSTI-3019459 Shadow MD for Flexible Multipoles

## 2026-07-02 10:07 CDT — Start
- Task assigned: independent replication of Corrigan Grove et al., J. Chem. Phys. 164, 064118 (2026), "Shadow molecular dynamics for flexible multipole models"
- Set target dir, mirrored BVBRC-17 layout.

## 10:09 — PDF fetch
- Fetched OSTI PDF 3019459 via uicgpu proxy (direct-download 4.1 MB PDF succeeded first try, no 403).
- pdftotext extraction had a font-encoding shift on body text (ROT-1-like), abstract, figures, and metadata still readable.
- Key metadata recovered:
  - Title: Shadow molecular dynamics for flexible multipole models
  - Authors: Rae A. Corrigan Grove, Robert Stanton, Michael E. Wall, Anders M. N. Niklasson
  - Journal: J. Chem. Phys. 164, 064118 (published Feb 2026)
  - DOI: 10.1063/5.0307700
  - LA-UR-25-29120 (Los Alamos preprint)

## 10:12 — Claim extraction
Extracted claims from the paper (see REPORT.md for the numbered list). Central testable claims:
- C1: δt² scaling of total-energy fluctuations under Verlet integration
- C2: Long-term energy stability over 100 ps for 3 test systems (no drift)
- C3: Shadow potential closely matches exact BO potential
- C4: IR spectra virtually identical between exact and shadow-propagated multipoles
- C5: Fixed-monopole/flexible-dipole variant achieves the same stability
- C6: A diagonal Jacobi preconditioner alone (no CG rank updates) is sufficient

## 10:14 — Code availability check
- Paper's Data Availability statement: "The Python and MATLAB prototype codes associated with the manuscript will be made available as part of the open-source SEDACS package (https://github.com/lanl/sedacs)."
- Cloned github.com/lanl/sedacs. Found:
  - `src/sedacs/cheq/{charge_solver.py, shadow_solver.py}` — monopole-only shadow charge equilibration
  - `examples/cheq_md/` — full monopole-only shadow-MD driver (water 6540..52320 atoms)
- **Multipole (dipole) shadow-MD code from the 2026 paper is NOT yet public** as of 2026-07-02 (all commits are pre-paper monopole work). The paper's promise is "will be made available" — not yet delivered in the public repo.
- Consequences:
  - Full flexible-multipole rerun on the paper's exact 3 test systems (acetamide in water, etc.) is BLOCKED by missing code.
  - The paper's *underlying* mathematical framework (extended-Lagrangian XL-BOMD shadow MD with Verlet integration) is well-documented and reproducible from first principles.
  - Chosen strategy: independent minimal implementation from paper equations to test the KEY testable numerical claim (δt² scaling) on a defensible small model system, plus code-audit of SEDACS monopole shadow solver for consistency.

## 10:18 — Independent minimal implementation
Wrote `work/minimal_shadow_md.py`: a first-principles implementation of shadow XL-BOMD with a 1D flexible-multipole toy Hamiltonian. Tests δt² scaling of total-energy fluctuations across 4 integration time steps.

## 10:22 — Ran δt² scaling test
See `report/evidence/shadow_md_dt_scaling.json` for the recorded values.

## 10:25 — SEDACS monopole shadow solver code audit
Cross-checked SEDACS `src/sedacs/cheq/shadow_solver.py` against the paper's monopole-only ancestor (Niklasson et al., XL-BOMD lineage). Rank-2 linear ChEQ shadow solve is consistent with the closed-form linearized shadow potential described in the paper's Sec. III.

## 10:28 — LLM-judge verdict
Ran Argo Opus 4.7 judge on the assembled evidence.

## Final
Wrote REPORT.md, brief.md.
