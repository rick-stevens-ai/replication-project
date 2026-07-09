# Failure Analysis — QC-200 / arXiv:1701.05052 Replication

## The one big framing failure (fixed by re-scoping)

**Failure.** The wave-brief target description claimed the paper was about "D_7 topological quantum computing using anyons whose fusion algebra is described by the dihedral D_7 modular tensor category (14 simple objects, F/R symbols, pentagon+hexagon, Kitaev–Solovay compilation of a Hadamard braid word with ε ~ ℓ^{-1/log 5})". None of this is in the paper.

**Root cause.** The SCOUT step (which the wave brief warns is bleed-prone: "SCOUT title starts 'Ananda Roy and David' — bleed; likely Roy & DiVincenzo") apparently generalized from the string "D7" in the title and produced a plausible-sounding but entirely fictional D_7 dihedral tensor category reproduction plan.

**Reality.** The "D7" is the chapter number in the *48th IFF Spring School* lecture-note proceedings (Forschungszentrum Jülich, 2017, "Topological Matter — Topological Insulators, Skyrmions and Majoranas"). The paper is a pedagogical review of **Majorana-fermion** topological quantum computing:
- §2: abelian anyons + Kitaev honeycomb model exact solution via Jordan–Wigner
- §3: non-abelian statistics of Majorana fermions, physical realization in the honeycomb model with a magnetic field
- §4: Clifford operations via braiding + magic states |a_4⟩, |a_8⟩ for T and controlled-phase gates

**Fix applied.** Retargeted the replication to what the paper actually claims. All targeted claims are then successfully reproduced at machine precision.

**Residual risk to downstream.** Any pipeline that trusted the SCOUT description without opening the PDF would happily "reproduce" a paper that does not exist. This is a systemic risk for the QC-200 wave and worth surfacing to the wave coordinator.

## Smaller frictions during this replication

### Marker CLI-signature change
- **Failure.** Initial marker invocation `marker_single INPUT OUTDIR` (Marker v0.x style) returned `Error: Got unexpected extra argument (/tmp/qc1701_marker/)`.
- **Root cause.** Marker's current CLI (in uicgpu's `/gpustor/stevens/anaconda3/envs/marker`) uses `marker_single INPUT --output_dir OUTDIR --output_format markdown`.
- **Fix.** Corrected the invocation; parse completed in 158 s on A100 including OCR error detection, layout, text, and figure extraction. 457-line markdown out.
- **Prevention.** Add a preflight `marker_single --help | grep -q output_dir` check to any future skill wrapper.

### Nougat fabricated abstract
- **Failure.** `extraction/nougat.mmd` contains a `###### Abstract` block with three identical sentences ("In this paper we present a new class of topological quantum computing algorithms…") that do not appear anywhere in the PDF.
- **Root cause.** The paper has no formal abstract — it jumps from title to a Contents ToC. Nougat's model presumably learned "if the PDF starts with title then abstract" as a strong prior and confabulated one.
- **Impact.** Any LLM downstream that reads Nougat's abstract as "the paper's abstract" gets fabricated content. Real, but does not affect this replication because we relied on the direct PDF text for claim extraction.
- **Elevation.** Filed as **Q5** in `open_questions.json` — a corpus-wide sanity check for fabricated Nougat abstracts is a small, high-value cleanup.

### Numerical subtlety: B^4 = -I, not +I
- **Not a failure per se, but a documentation subtlety.** The paper (below Eq. 32) says "B^4 gives rise to the identity operation". Naively one might expect B^4 = I as operators. In fact, using {γ_i, γ_j} = 2δ_ij one gets B^2 = -γ_i γ_{i+1}, and therefore B^4 = (γ_i γ_{i+1})^2 = -I. The identity is a *conjugation-action* identity, not an operator identity — B^4 acts on all Majorana operators by conjugation trivially, but carries an unphysical global phase of -1. The simulator checks both statements: B^4 ≠ +I (err 2), B^4 = -I (err 3e-16), B^4 γ_k B^{-4} = γ_k (err 7e-16).
- **Documented in `sim_majorana_braiding.py` and `REPORT.tex`.**

### C6 grid-vs-analytic tolerance
- **Failure.** First pass used a 401×401 grid to compute min|ε(q)|, which reported gap ≈ 9×10⁻³ for the isotropic point (J_x=J_y=J_z=1) because the Dirac points at (±2π/3, ∓2π/3) fall between grid points.
- **Fix.** Replaced with the exact analytic formula: gap = max(0, J_max − J_mid − J_min). The 401×401 grid is retained as a cross-check.
- **Lesson.** For phase-boundary tests, prefer analytic formulas when they exist; grid searches are inherently biased against gap-closing points.

## What was NOT independently reproduced (honest gaps)

1. **C7: `J_eff = J_x² J_y² / (16 J_z³)` (Eq. 13).** The paper's 4th-order Schrieffer–Wolff perturbation calculation. This is *derivable* but requires either an SW derivation on paper (Appendix B of the referenced Bravyi–DiVincenzo–Loss paper) or a numerical SW calculation. Neither was done; the coefficient is a quoted analytic result of a lengthy calculation. Scope-out justified for a same-day replication; would be a proper 1-day follow-up.
2. **C8: The full ancilla-based controlled-phase and π/8 protocols (§4.2–4.3).** These are described *as protocols in the operators* γ_1 γ_2 γ_3 γ_4 etc. Their correctness reduces to (a) the Clifford action on Paulis (C5, done); (b) magic-state distillation of |a_4⟩ and |a_8⟩ (procedures inherited from Bravyi–Kitaev '05 — reference [24] in the paper). We did not simulate the full teleportation circuit end-to-end. The building blocks (Cliffords via braiding, four-Majorana projective measurement structure) *are* verified.
3. **Physical realization details (§3.3): p+ip superconductor, magnetic-field-induced gap, Chern number of ±1 for Majorana bound states.** These are review of Kitaev '06 and are not this paper's independent numerical claims.
4. **Kitaev–Solovay compilation of a Hadamard braid word with ε ~ ℓ^{−1/log 5}.** This was the *fictional* target from the wave-brief description. It is not in this paper. Any attempt to "reproduce" it against Roy & DiVincenzo would necessarily fabricate the comparison.

## Verdict

**REPLICATED** — every concrete numerical/algebraic claim in the paper that admits a machine-precision check (C1, C2, C3, C4, C5, C5b, C6, spanning Eqs. 11, 20, 21, 30, 32, 33, 39–41) is reproduced to machine precision. The two unverified items (C7 analytic prefactor, C8 protocol-level end-to-end circuits) are either derivations the paper *itself* only states, or protocols whose Clifford building blocks are already covered by C5.

The single meaningful failure was the initial framing mismatch, which was caught by reading the actual PDF and fixed by re-scoping. That failure is generalizable and is flagged upstream via this document.
