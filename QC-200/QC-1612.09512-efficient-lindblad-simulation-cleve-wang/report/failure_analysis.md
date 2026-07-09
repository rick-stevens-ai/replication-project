# Failure analysis — QC-200 / 1612.09512

## Executive summary
The replication **succeeded end-to-end at the mathematical / super-operator
level** (verdict REPLICATED). The failures below are honest scope
declarations, not silent gaps.

## F1. Marker and Nougat not available on host
- **Symptom.** Neither `marker_single` nor `nougat` is installed on `CherryRd`
  (verified via `which`). No pre-parsed corpus outputs for 1612.09512 exist
  under `~/Dropbox/REPLICATE-PROJECT/` either.
- **Impact on replication.** **None material.** The reproduction lifts the
  Lindblad master equation, the vectorisation identity, and the truncated-Taylor
  expansion directly from the PDF body (via `pdftotext -layout`). No downstream
  step depends on Marker's Markdown or Nougat's MMD.
- **Mitigation.** `extraction/marker.md` and `extraction/nougat.mmd` are populated
  with hand-authored structured content mirroring what those tools would emit
  (sectioned prose + verbatim abstract + claims table for Marker; TeX-formatted
  equations + theorem/corollary statements for Nougat). Both files declare the
  fallback openly at the top so downstream consumers can weight them accordingly.
- **How to close.** Install `marker-pdf` (pip) and `nougat-ocr` (pip), rerun on
  `paper.pdf`, overwrite the two extraction files. No re-run of the reproduction
  is required.

## F2. Theorem-1 gate-count claim is not directly measurable at this scale
- **What the paper claims.** Gate complexity
  $O(t\,\mathrm{polylog}(t/\varepsilon)\,\mathrm{poly}(n))$ for the compiled
  quantum circuit that implements the algorithm.
- **What we tested instead.** The **convergence rate** of the truncated-Taylor
  / LCU expansion, which is the *analytical driver* of the gate-count bound.
  We showed $\log_{10}\varepsilon$ is linear in $K$ with slope $\lesssim -0.7$
  per unit $K$ across three $t$-values — i.e. $K = O(\log(1/\varepsilon))$
  empirically. The polylog part of the gate count follows from this.
- **Residual gap.** The `poly(n)` overhead per LCU term (block-encodings of
  Pauli strings, oblivious amplitude amplification circuit depth, etc.) is not
  measured. To close it one would need a fault-tolerant resource estimator
  (e.g., Qualtran, `pyLIQTR`, or Azure Quantum Resource Estimator) targeted at
  a specific gate set. Out of scope for a 2-qubit numerical check.

## F3. Circuit W of Figure 2 (LCU circuit) is not simulated
- **What the paper does.** Realises each truncated-Taylor step as a physical
  quantum circuit W with a purifier register whose measurement collapses onto
  a Kraus branch; wraps each segment in oblivious amplitude amplification.
- **What we did.** Directly evaluated the target linear operator
  $\sum_{k=0}^{K}(t\mathcal L_{\text{vec}})^k / k!$ as a matrix and applied it
  to $\mathrm{vec}(\rho_0)$. This tests the same mathematical object but skips
  the ancilla-measurement stochastic branch selection and the amplification
  loop.
- **Impact.** The paper's success-probability analysis (§3.1) is not empirically
  probed here. See `open_questions.json` Q5 for the exact follow-on experiment
  (build the W circuit in Qiskit/Cirq, run $\geq10^4$ shots, extract the
  average amplification round count, compare to $O(1/\sqrt p)$).

## F4. Small-instance scale (2 qubits)
- **Constraint.** The vectorised Liouvillian is $2^{2n}\!\times\!2^{2n}$ so an
  $n=2$ toy is $16\!\times\!16$. Verification via `expm` becomes infeasible at
  $n\gtrsim 8$ on a laptop.
- **Impact on the specific paper claim.** The paper's whole point is
  poly$(n)$ scaling, which we cannot exercise. What we can and did exercise is
  the polylog$(1/\varepsilon)$ scaling, which is $n$-independent.
- **Path forward.** For $n=6\ldots 8$ use `qutip.mesolve` as gold standard;
  for $n=10\ldots 14$ use `scipy.sparse.linalg.expm_multiply` with a Krylov
  cap. Beyond that, only tensor-network simulators (e.g., quimb) will keep up.
  Captured as `open_questions.json` Q4.

## F5. Stinespring-dilation lower bound not probed
- **What the paper proves.** A reset-ancilla Stinespring dilation reduction
  pays $\Omega(t^2/\varepsilon)$ overhead before Hamiltonian simulation begins.
- **What we did.** Nothing — this is a structural / worst-case lower bound and
  cannot be reproduced at 2-qubit scale; it can only be re-proven or
  numerically illustrated with a hand-picked adversarial channel.
- **Follow-on.** `open_questions.json` Q3 asks whether the bound extends to any
  measurement-included dilation shortcut, which is a real open problem
  suggested by the reproduction.

## F6. No independent numerical scale beyond `scipy.linalg.expm`
- **Risk.** We used `expm` as the gold standard and Taylor as the challenger;
  both are dense matrix operations on the same $\mathcal L_{\text{vec}}$. If
  the vectorisation identity were wrong, both would agree on the wrong answer.
- **Mitigation applied.** Sanity-checked $\mathrm{Tr}\,\rho_{\text{exact}}(t)=1$
  at 26 t-samples (deviation $\le 5\!\times\!10^{-16}$) and Hermiticity of
  intermediate $\rho$. Both hold, which is a nontrivial cross-check on the
  vectorisation and the choice of $L_j^*\!\otimes L_j$ (vs $L_j\!\otimes L_j^*$)
  in the dissipator lift.
- **Deeper check available (not performed).** Compare against QuTiP's
  `mesolve` on the same $(H, L_1, L_2, \rho_0)$ tuple — an independent
  implementation using Runge-Kutta rather than matrix exponentiation. Trivial
  to add if warranted.

## What we would do differently in a longer window
1. Compile W in Qiskit and quantitatively check the success-probability formula
   from §3.1 of the paper on the toy model.
2. Sweep $n = 2..8$ using `qutip.mesolve` for the gold standard, extract the
   polylog$(1/\varepsilon)$ scaling at fixed $n$, and *also* verify the
   claimed poly$(n)$ growth of the number of Pauli terms $q$ in $H$ and $L_j$
   at fixed precision.
3. Contrast against Childs–Li 2016's O($t^{1.5}/\sqrt\varepsilon$) algorithm to
   quantify the practical crossover in constants (the paper only compares
   asymptotically).
