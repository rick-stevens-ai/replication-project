# marker.md — Preconditioned quantum linear system algorithm

**NOTE ON PROVENANCE:** Marker (VikParuchuri/marker) was not installed on this
host at the time of replication. The following extraction is a best-effort
fallback produced from `pdftotext -layout paper.pdf` + light post-editing to
recover section boundaries. Structural fidelity (equations, references) is
lower than a real Marker run would provide; a future pass with Marker
installed should replace this file. The full raw `pdftotext` dump is preserved
at `../work/paper.txt`.

---

## Title & Authors

**Preconditioned quantum linear system algorithm**
B. D. Clader, B. C. Jacobs, and C. R. Sprouse
The Johns Hopkins University Applied Physics Laboratory, Laurel, MD 20723, USA
arXiv:1301.2340v4 [quant-ph] 7 May 2013

## Abstract

We describe a quantum algorithm that generalizes the quantum linear system
algorithm [Harrow et al., Phys. Rev. Lett. 103, 150502 (2009)] to arbitrary
problem specifications. We develop a state preparation routine that can
initialize generic states, show how simple ancilla measurements can be used to
calculate many quantities of interest, and integrate a quantum-compatible
preconditioner that greatly expands the number of problems that can achieve
exponential speedup over classical linear systems solvers. To demonstrate the
algorithm's applicability, we show how it can be used to compute the
electromagnetic scattering cross section of an arbitrary target exponentially
faster than the best classical algorithm.

## 1. Introduction and prior art

Feynman's original observation on quantum simulation; Shor's factoring
algorithm. Harrow, Hassidim & Lloyd (HHL) 2009 gave a quantum linear system
algorithm exponentially faster than classical (for the appropriate output
functional) provided (1) elements of A are queryable via an efficient oracle;
(2) A is sparse or efficiently sparsifiable; (3) the condition number κ scales
as polylog(N). This paper attacks three gaps that made HHL hard to apply in
practice: state preparation of |b⟩, solution readout, and the κ = polylog(N)
requirement.

## 2. Original HHL review

Prepare |Ψ⟩ = Σ_τ |τ⟩|b⟩, phase-estimate the eigenvalues of A via Hamiltonian
simulation (t₀ = O(κ/ε)), rotate an ancilla by C/λ_j, uncompute, and post-select
|1⟩ on the ancilla to obtain the normalised solution |x⟩ = A⁻¹|b⟩. The
post-selection is the reason the original algorithm scales linearly in κ.

## 3. Generic state preparation |b_T⟩ (Eqs. 5-7)

Introduces the "twin" state |b_T⟩ = cos φ_b |b̃⟩|0⟩_a + sin φ_b |b⟩|1⟩_a which
can be prepared with a single oracle call giving amplitude b_j and phase φ_j of
|b⟩ = Σ b_j e^{iφ_j} |j⟩, plus one ancilla rotation. No a-priori |b⟩
is required.

## 4. Unitary HHL (Eq. 8) and read-out (Eq. 9)

Drop the final post-selection to keep the algorithm unitary:
|Ψ⟩ = (1 − sin²φ_b sin²φ_x)^{1/2} |Φ_0⟩ + sin φ_b sin φ_x |x⟩|1⟩_a|1⟩_a.

Readout of |⟨R|x⟩|² via a controlled-swap test between |x⟩ and a
similarly-prepared |R_T⟩ (Eq. 9): |⟨R|x⟩|² = (P_1110 − P_1111) /
(sin²φ_b sin²φ_x sin²φ_r). Moments ⟨x|x^n|x⟩ and individual amplitudes x_j
follow via ancilla measurements and amplitude estimation.

## 5. Preconditioning (§ around Eqs. 10-12)

The core new tool. Replace Ax = b by MAx = Mb with κ(MA) ≪ κ(A). Quantum
constraints: (a) only local access to A; (b) MA must remain sparse. Sparse
Approximate Inverse (SPAI) satisfies both by solving, for each column,
```
    min_{m_k}  || A m_k − e_k ||₂    (Eq. 11)
```
with m_k restricted to a chosen (a priori or adaptive) sparse pattern. This
reduces to N independent (n × d) least-squares problems.

**Eq. (12) bound on the preconditioned condition number:** if
sqrt(d) · ε_pre < 1 (with ε_pre = max_k || A m_k − e_k ||) then
```
    κ(MA)  ≤  (1 + sqrt(d) ε_pre) / (1 − sqrt(d) ε_pre)
```

## 6. Cost analysis

Best classical (conjugate gradient) sparse solver: O(N d κ log(1/ε)).
Quantum, with the paper's unitary HHL + SPAI:
```
    T_quantum  =  Õ( d⁷ · κ · log(N) / ε² )
```
The d⁷ pre-factor comes from the Suzuki-integrator Hamiltonian simulation
(m = 6 d²) and the O(1/ε²) from amplitude-estimation of the readout
probabilities. The preconditioning step contributes only an O(d³) overhead per
oracle call. Therefore preconditioning yields an HHL runtime factor
κ(A)/κ(MA).

## 7. Application: FEM electromagnetic scattering / RCS

Cast Maxwell's equations on edge basis functions N_i (Eq. 13) — the
FEM matrix F is fixed by the discretisation; A and b depend on the scatterer
via boundary conditions. Far-field radiation (Eq. 14) and RCS (Eq. 15-16)
are expressible as ⟨R|x⟩-type functionals of the solution, which the paper's
Eq. (9) readout can estimate exponentially faster than classical FEM assembly
+ CG solve once the condition number is bounded.

## References (abridged, from raw text)

[3]  Harrow, Hassidim & Lloyd, PRL 103, 150502 (2009).
[9]  Brassard et al., Amplitude Estimation.
[13-15, 22-23]  SPAI preconditioning references.
[20-21]  Berry et al. Hamiltonian simulation; Suzuki higher-order integrator.
[24]  Standard FEM electromagnetic scattering references.
