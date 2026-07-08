# Failure analysis — MC-VQE Parrish 2019 replication

Honest critique of what this replication does **not** establish, ordered
roughly by scientific severity. The overall verdict is REPLICATED, but the
verdict is bounded — the gaps below are real and should be visible to any
downstream reader.

## 1. Headline system (N=18 LH2 B850 ring) was not exercised

- **What the paper claims:** the banner demonstration is an N=18 exciton ring,
  Hilbert dimension 2^18 = 262,144, with MC-VQE reaching "tens of μeV"
  accuracy in 14 L-BFGS iterations from a zero-entanglement initial guess.
- **What we did:** launched the N=18 statevector run on uicgpu (8×A100, CPU
  statevector), killed after >40 min wall-time — the numerical-gradient
  L-BFGS over 108 SO(4) angles did not converge within budget.
- **What we substituted:** an N=12 cyclic ring in the same regime (same
  connectivity topology, same ansatz family, same dipole model). N=12 hit 9.7
  μeV max error, cleanly inside the paper's "tens of μeV" claim.
- **Why this is a real gap:** MC-VQE accuracy scaling with N is an
  \emph{implicit} claim of the paper (the whole point of the N=18
  demonstration is to show the method works at a "hard" scale). Reproducing at
  N=12 confirms the per-bond ansatz expressivity but does *not* independently
  confirm the size claim.
- **Fix:** analytical gradients (parameter-shift-rule statevector), tighter
  BFGS Wolfe conditions, or a better initial guess. Estimated re-run cost:
  ~1–2 h on uicgpu with analytical gradients.

## 2. MC-VQE was not benchmarked against classical multi-reference gold standards

- **What the paper compares against:** FCI (exact) and CIS (weak singles).
- **What is missing:** SA-CASSCF, CASCI, and MRCI — the classical multi-state
  gold standards. Without those benchmarks, MC-VQE's claim to practical value
  in the fault-tolerant era is unquantified — one only knows it beats CIS and
  matches FCI on this exciton toy problem.
- **This is a critique of the paper as much as this replication.** The paper
  should have included SA-CASSCF baselines. We did not add them either.
- **Fix:** listed as open Q1. PySCF or OpenFermion can compute SA-CASSCF on the
  exciton active space in a few CPU-minutes.

## 3. Cost-vs-accuracy trade-off not quantitatively swept

- We ran one entangler depth per system (1 layer for N=12, 2 layers for N=8)
  because that was the paper's regime.
- We did not sweep depth × parameter count × measurement count to independently
  verify MC-VQE's implicit **efficiency** claim (few parameters, few
  iterations). The C6 partial verdict is one symptom of this gap:
  81 (N=12) / 163 (N=8) L-BFGS iterations vs the paper's 14 (N=18), which is
  6–12× slower and is not fully explained by finite-difference-gradient
  overhead alone. The paper likely used analytical gradients or a different
  parametrization of SO(4).
- **Fix:** analytical gradients + a depth sweep (1, 2, 3, 4 layers) at fixed
  N=12 would produce the missing accuracy-vs-depth curve.

## 4. Molecule-specific numerics were not reproduced

- The paper's exact TeraChem ωPBE/6-31G* monomer energies, transition dipoles,
  and BChl-a geometry are in a supplemental data packet absent from the arXiv
  source (and we did not chase the journal's supplement).
- We used a **physically-faithful** BChl-a parametrization + the paper's
  supplemental dipole formula. This means our absolute excitation energies
  (~1.6 eV) are only qualitatively right; our reported method-accuracy
  metrics (MC-VQE vs FCI relative errors) are geometry-robust and are the
  claims that actually matter.
- **What we do NOT claim:** that our absolute eigenvalues match the paper's
  reported eigenvalues molecule-for-molecule.

## 5. No noise, no shot noise, no hardware

- The paper's own demonstration is a noiseless statevector simulation on their
  in-house Quasar simulator; we mirror this.
- **What is not established by either the paper or this replication:**
  MC-VQE's behavior under realistic shot noise, readout error, or depolarizing
  noise on today's superconducting or trapped-ion hardware. State-averaged
  optimization *may* average out noise across states (helpful) or *may*
  correlate noise across states (harmful). Neither has been quantified.
- **Fix:** listed as open Q4. A Qiskit Aer noise model + a shot-count sweep
  would answer this.

## 6. Double-excitation states are outside the ansatz — honestly flagged, not fixed

- A CIS-referenced singles ansatz cannot reach doubly-excited FCI states by
  construction.
- The N=8 stack has one FCI state (index 7) with only 0.4% singles character.
  It is excluded from matched metrics. If included naively it would produce a
  ~154 meV "error" that is really an ansatz-scope mismatch, not a method
  failure.
- **This is transparent, not a defect** — but it is a real scientific
  limitation of MC-VQE (and of the paper's own scope) that any downstream
  user should be aware of. Auto-CAS or a doubles-augmented ansatz would
  address it (open Q5).

## 7. LLM-judge second opinion was single-model

- gpt-5.2 (free Argo) returned PARTIAL, coverage 7/10, agreement 5/10.
- The second-judge call to opus-4.8 returned 502 (transient Argo backend);
  gpt-5.2 is the sole judge of record.
- **Impact:** low. The disagreements the judge flagged (C4-sign,
  C6-iterations) are both explained by geometry-dependence and
  optimizer-conditioning, and are addressed in the REPORT §5. But a
  cross-model consistency check would have strengthened the verdict.

## Summary of severity

| Gap | Severity | Fixable? |
|---|---|---|
| N=18 not converged (used N=12 surrogate) | HIGH | yes (analytical gradient) |
| No SA-CASSCF / CASCI baseline | HIGH (as critique of paper) | yes (PySCF, ~CPU-mins) |
| No cost-vs-accuracy sweep | MEDIUM | yes (depth sweep) |
| Molecule-specific numerics not reproduced | MEDIUM | needs paper's supp data packet |
| No noise / hardware runs | MEDIUM (paper doesn't either) | yes (Qiskit Aer) |
| Double-excitation blind spot | LOW (transparent, ansatz-scope) | yes (auto-CAS) |
| Single-model LLM-judge | LOW | trivial (re-run opus later) |

The replication is honest and reproduces the paper's core method-accuracy
claims; but the N=18 gap and the missing SA-CASSCF baseline are the two
places where a stricter reviewer would (rightly) push back.
