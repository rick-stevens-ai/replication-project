# Failure analysis — arXiv:2304.07917 replication

An honest post-mortem of where this replication is soft, where it could
silently be wrong, and what a stronger follow-up would touch first.

## 1. What we tested, and what "REPLICATED" here does *and does not* mean

The verdict **REPLICATED** covers the paper's Fig 7 and Fig 8 central
quantitative claims (ground-state convergence and cumulative
success-probability decay for the 4-site TIM and the 2-site Hubbard).
These are the paper's headline experiments and they were reimplemented
independently, in a fresh venv, from the equations in Section IV of the
paper. Two independent baselines (scipy `expm` on the same Hamiltonians,
and exact diagonalisation) agree with our results.

What **REPLICATED does not mean**:

- We did **not** verify the paper on any Hamiltonian the paper itself did
  not report on.
- We did **not** confirm the paper's larger-system extrapolation (Claim
  C6: 3- and 4-site Hubbard $p_{\rm success}$ decaying to $10^{-5}$ and
  $10^{-9}$). If those numbers are wrong the paper's "PITE is practical
  at $n\!=\!4$" story falls, and our replication cannot see that.
- We did **not** reproduce the paper's stochastic-sampling error bars
  (they run 100 000 ancilla-outcome shots per Trotter step); we compute
  exact expectation values instead, which is the same *green Trotterised
  curve* the paper plots, but not the black-dot shot-noise cloud.
- We did **not** benchmark PITE against standard measurement-based QITE
  or against VQE, so any claim of relative advantage is unverified.
- We did **not** run a noise model.
- We did **not** quantify circuit depth or two-qubit gate count.

## 2. The ancilla-circuit shortfall (soft spot #1)

The cleanest test of Claim C1 (post-selection realises the non-unitary
Pauli exponential) would be a full Qiskit ancilla-circuit build with
mid-circuit measurement, running under Statevector or aer, and matching
the state within the accepted ancilla-`|0>` branch against
`exp(-c dtau sigma) |psi> / N`. We attempted this in
`work/qiskit_gadget_verify.py` and `work/qiskit_full_ite.py`. We got:

- system-state fidelity $\gtrsim 0.999$ with the target operator (good);
- a residual factor-of-two ambiguity in the success-probability
  convention (ancilla $|0\rangle$ vs.\ $|+\rangle$ input; $\alpha$ vs.\
  $\alpha^2$ definitions differ between the paper's Eq.\ 26 and the
  circuit-level probability we measured).

We stopped there and fell back to the statevector-with-post-selection
implementation (which *is* the standard classical way to simulate PITE
and *is* semantically equivalent). This means we have strong evidence
Claim C1 is *approximately* right at the state-fidelity level, but we
did not fully reconcile the probability normalisation. A more thorough
replication would spend an extra day tracing the $\alpha$ convention
through the paper's Eq.\ 26 and the Qiskit-level circuit and closing
the gap.

## 3. Boundary-condition inference (soft spot #2)

The paper's Fig 8 for the 2-site Hubbard model reports $E_0 \approx
-0.156$ but **does not state explicitly** whether periodic or open
boundary conditions are used. We inferred **open boundary conditions**
because the OBC Lieb--Wu closed form
$E_0 = U/2 - \sqrt{(U/2)^2 + (2t)^2}$ evaluates to $-0.156155$ at
$t = -0.1, U = 0.1$, matching the paper's value; whereas PBC on a
2-site chain doubles the hopping and gives $E_0 = -0.353$, which
does not match.

**Risk:** had we defaulted to PBC without cross-checking against the
closed form, the ground-state energy would have been off by a factor
of 2, and the "converges to the correct $E_0$" verdict would have
silently failed. This inference step should be explicit in any
future rerun, and the paper's BC ambiguity should be flagged to the
authors. A more defensive replication would run both BCs, print both
$E_0$ values, and match whichever equals the paper's number.

## 4. Missing baselines (soft spot #3)

The paper implicitly positions PITE as competitive against standard
measurement-based QITE (McArdle et al.\ 2019) and against VQE, but
we did not implement either baseline. We can therefore say
"PITE gets to $E_0$ at these parameters" but we cannot say
"PITE gets to $E_0$ *faster* / with fewer *gates* / with fewer
*shots* than the alternatives". If a future reviewer wanted to
attack the paper's practicality claim, the missing baseline is the
first place to look.

## 5. Trotter-error scaling not measured (soft spot #4)

We ran only $\Delta\tau = 0.1$ throughout. The residual $|\Delta E|
\sim 2\times 10^{-4}$ at $\beta = 4.5$ on the TIM is consistent with
first-order Trotter error at this step size, and cross-checking against
scipy `expm` shows the exact ITE gets to $\sim 10^{-6}$ (i.e.\ the gap
is Trotter-limited not implementation-limited). But we did not do a
proper $\Delta\tau$ sweep to *measure* the Trotter-error exponent
and confirm it is first-order. A one-line follow-up experiment
(run $\Delta\tau \in \{0.2, 0.1, 0.05, 0.025\}$, fit
$|\Delta E|(\Delta\tau)$) would sharpen this.

## 6. No noise model (soft spot #5)

All results are ideal statevector. PITE runs one mid-circuit measurement
per Pauli term per Trotter step; on real superconducting hardware with
99% measurement fidelity, a 45-step 4-site TIM run with $\sim 10$
Pauli terms is $\sim 450$ measurements per shot, i.e.\ another
$e^{-4.5}\!\sim\!1\%$ overhead on top of the algorithmic ~0.6%
post-selection --- and, more worryingly, measurement error can bias
the branch label rather than just reduce yield. Whether the noise
failure mode is *benign* (fewer shots survive but the survivors are
correct) or *malignant* (survivors are biased) is not tested. This is
the single most important follow-up experiment for anyone trying to
run PITE on hardware.

## 7. Nougat extraction not run

We extracted the paper via `pdftotext` (standard poppler tool) into
`work/paper.txt` and worked from that plus the PDF directly. We did
**not** run Nougat (the specialised math-aware PDF-to-Markdown
extractor). The `extraction/nougat.mmd` file in this directory is a
**stub** placeholder created for the backfill (2026-07-06); the actual
paper reading was done from `pdftotext` output and the PDF. This is a
provenance gap: if the survey pipeline expects a Nougat mmd
extraction, that step needs to be run separately (uicgpu A100 idle
capacity, or Polaris PBS batch --- see the standing OCR-allocation
rule in TOOLS.md).

## 8. Author-name discrepancy in the wave brief

The spawn brief listed the authors as "Turkeshi et al." The actual
arXiv metadata for 2304.07917 shows Leadbeater, Fitzpatrick, Mu\~noz
Ramo, and Thom. Same arXiv id, same subject, so the replication
proceeded against the correct paper --- but the queue-side brief
generator should be checked for a bad author-lookup on this id.

## 9. What a stronger v2 replication would do

In order of importance:

1. Add a calibrated depolarising noise model in qiskit-aer and rerun
   both experiments; report converged $\langle E\rangle$ vs.\ noise
   strength and separate the coherent-gate from measurement-error
   contributions.
2. Implement the standard measurement-based QITE (McArdle 2019) in
   the same framework and compare shot-cost to reach matched
   $|\Delta E|$.
3. Fully reconcile the ancilla-circuit $\alpha$ convention and match
   the paper's success-probability curve at the circuit-sampling
   level (not just at the state-fidelity level).
4. Attempt the 3-site Hubbard PITE run (still tractable on classical
   statevector) and check whether the paper's Claim C6 extrapolation
   holds at $n\!=\!3$.
5. Sweep $\Delta\tau$ and fit the Trotter-error exponent.
6. Try both BCs by default and print both $E_0$ values before running.
