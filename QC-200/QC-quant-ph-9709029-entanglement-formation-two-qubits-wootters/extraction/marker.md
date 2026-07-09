# Entanglement of Formation of an Arbitrary State of Two Qubits

*William K. Wootters*
Department of Physics, Williams College, Williamstown MA 01267

**arXiv:** quant-ph/9709029v2 (13 Sep 1997)
**Journal:** Phys. Rev. Lett. **80**, 2245 (1998)

> **Extraction note (2026-07-05):** produced via `pdftotext -layout`
> post-processed into GFM. Marker-pdf 0.2.6 fails with an internal
> `TypeError: Invalid input type 'PdfDocument'` at
> `pdftext.extraction._load_pdf` on Darwin 25 + Python 3.12 + the
> `pypdfium2 == 4.30.0` combination we could install. See
> `extraction/README.md` for details.

## Abstract

The entanglement of a pure state of a pair of quantum systems is defined
as the entropy of either member of the pair. The entanglement of
formation of a mixed state \(\rho\) is defined as the minimum average
entanglement of an ensemble of pure states that represents \(\rho\). An
earlier paper [Phys. Rev. Lett. **78**, 5022 (1997)] conjectured an
explicit formula for the entanglement of formation of a pair of binary
quantum objects (qubits) as a function of their density matrix, and
proved the formula to be true for a special class of mixed states. The
present paper extends the proof to arbitrary states of this system and
shows how to construct entanglement-minimizing pure-state decompositions.

**PACS numbers:** 03.65.Bz, 89.70.+c

## 1. Introduction

Entanglement is the feature of quantum mechanics that allows, in
principle, feats such as teleportation and dense coding and is what
Schrödinger called "the characteristic trait of quantum mechanics." A
pure state of a pair of quantum systems is called entangled if it does
not factorize. A mixed state is entangled if it cannot be represented
as a mixture of factorizable pure states. Perhaps the most basic of the
proposed measures is the *entanglement of formation*, intended to
quantify the resources needed to create a given entangled state.

## 2. Definitions

Given a density matrix \(\rho\) of a pair of quantum systems \(A\) and
\(B\), consider all pure-state decompositions
\[
\rho = \sum_i p_i |\psi_i\rangle\langle\psi_i|. \tag{1}
\]
For each pure state, the entanglement is the entropy of either subsystem:
\[
E(\psi) = -\mathrm{Tr}(\rho_A \log_2 \rho_A) = -\mathrm{Tr}(\rho_B \log_2 \rho_B). \tag{2}
\]
The entanglement of formation of the mixed state \(\rho\) is
\[
E(\rho) = \min \sum_i p_i E(\psi_i). \tag{3}
\]

## 3. Spin flip and concurrence

For a qubit state \(|\psi\rangle\) with expansion coefficients
\((\alpha,\beta)\) in the computational basis, the *spin flip* is
\[
|\tilde\psi\rangle = \sigma_y |\psi^*\rangle.
\]
For a general density matrix \(\rho\) of two qubits,
\[
\tilde\rho = (\sigma_y \otimes \sigma_y)\,\rho^*\,(\sigma_y \otimes \sigma_y),
\]
where the complex conjugate is taken in the standard basis.

The **concurrence** of a mixed two-qubit state is
\[
C(\rho) = \max\{0,\, \lambda_1 - \lambda_2 - \lambda_3 - \lambda_4\},
\]
where \(\lambda_1 \ge \lambda_2 \ge \lambda_3 \ge \lambda_4 \ge 0\) are
the square roots of the eigenvalues of the (non-Hermitian) matrix
\(\rho\tilde\rho\); equivalently, the singular values of the operator
\(\sqrt{\rho}\sqrt{\tilde\rho}\).

## 4. Main theorem — closed-form entanglement of formation

**Theorem.** For an arbitrary state \(\rho\) of two qubits, the
entanglement of formation is
\[
E(\rho) = \varepsilon\!\big(C(\rho)\big), \qquad
\varepsilon(C) = h\!\left(\frac{1+\sqrt{1-C^2}}{2}\right),
\]
with the binary entropy
\[
h(x) = -x \log_2 x - (1-x)\log_2(1-x).
\]

The function \(\varepsilon(C)\) is monotonically increasing from
\(\varepsilon(0)=0\) to \(\varepsilon(1)=1\).

Wootters proves the theorem constructively by exhibiting an
entanglement-minimizing decomposition of any 2-qubit \(\rho\), using
the "magic basis" that diagonalizes the spin-flip operator.

## 5. Optimal decomposition (sketch)

Given \(\rho\), let \(\rho\tilde\rho\) have eigenvalues (with
multiplicity) whose square roots are \(\lambda_1 \ge \lambda_2 \ge
\lambda_3 \ge \lambda_4\). The paper constructs, via a magic-basis
alignment and a unitary rotation on the ensemble, a specific
four-element ensemble \(\{p_i,|\psi_i\rangle\}\) such that
\[
\sum_i p_i E(\psi_i) = \varepsilon(C(\rho)).
\]

## 6. Discussion

The formula reduces older special cases (Bennett-DiVincenzo-Smolin-Wootters
"positively-conditioned" states; Hill-Wootters real-density-matrix case)
to a common expression valid for any two-qubit density matrix. The
existence of a closed-form measure of mixed-state entanglement is used
extensively in later work on quantum information, decoherence in
quantum computers, and quantum cryptography.

## Acknowledgments

Discussions with C. H. Bennett, D. P. DiVincenzo, J. A. Smolin, S.
Hill, and A. Uhlmann; support from NSF-PHY.

## References

- [1] C. H. Bennett *et al.*, Phys. Rev. Lett. **70**, 1895 (1993).
- [2] C. H. Bennett and S. J. Wiesner, Phys. Rev. Lett. **69**, 2881 (1992).
- [3] E. Schrödinger, Naturwissenschaften **23**, 807 (1935).
- [4] C. H. Bennett, H. J. Bernstein, S. Popescu, and B. Schumacher,
      Phys. Rev. A **53**, 2046 (1996).
- [5] V. Vedral *et al.*, Phys. Rev. Lett. **78**, 2275 (1997).
- [6] C. H. Bennett, D. P. DiVincenzo, J. A. Smolin, and W. K. Wootters,
      Phys. Rev. A **54**, 3824 (1996).
- [9] S. Hill and W. K. Wootters, Phys. Rev. Lett. **78**, 5022 (1997).

*(Complete reference list in `paper.pdf` and `work/paper_layout.txt`.)*
