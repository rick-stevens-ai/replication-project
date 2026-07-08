# Honest Failure Analysis — QC-1905.04054

This is a candid inventory of what this replication does **not** prove, in
service of Rick's 2026-07-05 hard requirement that every REPLICATED verdict
carry a genuine critique. The verdict itself (REPLICATED) is defensible: the
paper's headline claim was exercised on the paper's own test system, and the
numbers agree with reference. The list below is about the *scope* of that
success, not its validity.

## 1. Only the first derivative was independently reimplemented
The paper derives analytical expressions for **first-, second-, and
third-order** VQE energy derivatives, plus the response-equation solve
(their Eq. 10) for `d theta_star / dR`. We reproduced only the first-order
result at the variational optimum. The higher-order harmonic + cubic PES
approximation in their Fig. 4 was **not** independently reimplemented. Its
consistency with the framework is inherited from the paper, not re-verified.

## 2. Parameter-shift circuits used from PennyLane's built-in
We used `diff_method="parameter-shift"` on the ansatz parameters. This is
functionally the same rule the paper derives in Sec. 2, but we did not
reimplement the R ± pi/2 shifted expectation-value circuits from scratch
and cross-check them against a direct symbolic gradient of `<H>_theta`.
That would be the true "independent re-derivation." What we verified is
that PennyLane's implementation of this rule, when applied to a
correctly-built H2 Hamiltonian, gives correct energies at a variational
optimum such that Hellmann-Feynman gives the right force.

## 3. No end-to-end geometry optimization or vibrational analysis
The paper motivates analytical VQE derivatives in large part by enabling
downstream applications: **BFGS geometry optimization** with analytical
gradients, and **vibrational analysis** (harmonic frequencies) from the
Hessian. We did not close either loop. Our replication proves the
first-derivative arithmetic is right at a fixed geometry; it does not
prove that iterative BFGS driven by these gradients converges to the
correct equilibrium, nor that a second-derivative-driven harmonic
frequency for H2 matches the experimental ~4401 cm^-1. This is a real
gap.

## 4. Measurement-overhead comparison is qualitative, not quantitative
The paper is careful about circuit counts and shot budgets for the
analytical vs numerical routes (how many Pauli-group measurements each
gradient element costs, how the shot budget scales with target gradient
precision). Our replication is on a noiseless state-vector simulator and
**does not quantify measurement overhead per gradient call**. Our C4
comparison shows analytical beats numerical in *accuracy per VQE run*, but
not in *shots per Ha/A of gradient precision on hardware*. On real NISQ
hardware, the analytical advantage could be larger or smaller than what
we report.

## 5. Noiseless comparison overstates the mechanism, not the existence
Our numerical-difference baseline fails on the noiseless simulator because
the true dE = ~10^-6 Ha at r=0.735 A is below VQE convergence noise ~5e-5 Ha.
This is closely related to but not identical to the paper's motivating
regime (finite-step vs *shot* noise). Both are "noise dominates the
gradient signal," but the specific noise source differs. Our replication
demonstrates the failure exists; it does not exercise the *same* failure
the paper motivates.

## 6. One molecule, one geometry, one basis, one ansatz
We tested the paper's own test point exactly. By design (this is a
replication, not a generalization study). But it means the replication
does not certify robustness to:
- Other molecules (LiH, BeH2, H2O, N2)
- Larger basis sets (6-31G, cc-pVDZ)
- Non-equilibrium geometries where VQE is a worse eigenstate approximation
  and the Hellmann-Feynman residual grows
- Other ansatz families (UCCSD, hardware-efficient with different
  topologies, QAOA-style)

## 7. Ansatz variant, not bit-for-bit
We used `RX(theta) RY(theta)` per wire per layer + CNOT chain, instead of
the paper's precise single-parameter rotation choice in Fig. 3. This is a
small practical variant used because it plays cleanly with PennyLane's
parameter-shift rule out of the box, and it still reaches FCI to 5.8e-5 Ha
on this system. It is not bit-for-bit the paper's ansatz.

## 8. No cross-check against classical analytical gradients
For H2/STO-3G, PySCF can compute the analytical HF/FCI energy gradient
directly, giving a *classical analytical* reference (not just a
finite-difference reference). We compared to a full-diag FD "exact"
reference, not to a classical analytical gradient. The two should agree
to numerical precision, but the direct cross-check was not performed.

## 9. Not tested with shot noise or gate noise
`default.qubit` is noiseless. The paper's strongest claim — analytical
strictly beats numerical *under shot / gate noise* — is not directly
tested. This is question 2 in `open_questions.json`.

## 10. Not tested with real quantum hardware
No IBMQ / IonQ / Rigetti hardware call. All results are simulator-only.
The paper is careful to note its own experiment is also simulated
(Qulacs); however, the real-world stress test would be a NISQ hardware
run showing analytical dE/dR gives usable forces where reoptimize-and-diff
does not.

---

## Bottom line
The core claim — analytical VQE derivatives reproduce the exact answer
to |Delta| = 2.9e-5 Ha/A on the paper's own H2/STO-3G/r=0.735A benchmark,
~330x tighter than reoptimized-VQE finite differences — is directly
demonstrated on the correct test system with an open-source stack.
Everything in this file is scope, not error. Readers who want geometry
optimization, vibrational frequencies, NISQ hardware validation, or
ansatz-family generality should treat those as unaddressed by this
replication and see `open_questions.json` for concrete follow-up probes.
