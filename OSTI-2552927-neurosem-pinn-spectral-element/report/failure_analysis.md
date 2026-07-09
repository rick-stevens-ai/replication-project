# Failure Analysis — OSTI 2552927 NeuroSEM Replication

This file records what did **not** work, what was **not attempted** and why,
and what specific failure modes a downstream re-runner should watch for.

## 1. Not attempted: end-to-end Nektar++ coupled solve
**Impact:** claims C1–C8 (Tables 1–3, drag/lift 2.39/10.41%, Nusselt agreement,
PIV vorticity contours) are not independently verified.

**Root cause:** The authors' C++ coupling glue —
`PINNBodyForce.cpp` and the modified `UnsteadyAdvection.cpp` — is **not in
the public repo**. The published NeuroSEM release contains only the PINN
training half; the SEM half references a Nektar++ patch that the authors
describe in prose but do not distribute.

**Additional cost:** even if the patch existed, Nektar++ is a large C++/MPI
package requiring an HPC build. A 100-paper wave cannot afford one full
Nektar++ standup per PINN-hybrid paper.

**Mitigation used:** we replicated the strongest test achievable from the
released artifacts alone — verifying that the PINN component reproduces the
paper's monotone-with-Ra error scaling on 300k independent SEM quadrature
points. A poor PINN would guarantee a poor NeuroSEM output; a good PINN is
therefore a necessary (not sufficient) precondition for C1–C8 to hold.

## 2. Not attempted: retraining from scratch
**Impact:** we cannot confirm that the reported hyperparameters
(600,000 Adam iterations per checkpoint, Appendix B lr schedule) actually
reach the shipped-weight L2 accuracy.

**Root cause:** 600k iters × 40+ checkpoints ≈ hundreds of GPU-hours on
uicgpu; not affordable in a wave budget. This is a scope decision, not a
technical failure.

**Mitigation used:** verified reload + inference reproducibility only.
Recorded as open question #3 for future work.

## 3. Not attempted: Case C noise-sweep checkpoint reload
**Impact:** the paper's 5-noise-variant Table 3 (u,v L2 errors ranging
0.63% to 6.44% across σ = 0.01 to 0.10) is not spot-checked.

**Root cause:** wave-budget scope decision. The five .eqx checkpoints
are present in the repo, so this is trivially runnable in principle,
just not run here.

**Mitigation used:** recorded as open question #2.

## 4. Not attempted: cylinder-flow variant sweep
**Impact:** the 16-variant depth/data-density sweep in Appendix B is
untested. Drag error 2.39% and lift error 10.41% are unverified.

**Root cause:** requires Nektar++ end-to-end. Same as #1.

## 5. Not attempted: PIV data provenance audit
**Impact:** we take `PINNdata_dSpace1_dTime1.mat` (725,423 samples, 51
snapshots) at face value. No independent PIV acquisition or metadata
cross-check.

**Root cause:** would require experimental facility access;
out-of-scope for a computational replication.

## 6. Not attempted: JAX .eqx vs PyTorch traced .pt equivalence check
**Impact:** our L2 error numbers use the JAX `.eqx` path; the actual
downstream Nektar++ solver consumes the PyTorch traced `.pt` path.
If the trace step introduces silent numerical drift, our component
numbers may not be what NeuroSEM actually saw.

**Root cause:** scope decision — flagged as open question #5 for
follow-up.

## 7. Numerical gap between component and end-to-end
At Ra = 1e5, our PINN T-surrogate L2 error is 0.433% while paper's
NeuroSEM u,v error is 0.181% / 0.176%. At Ra = 1e6 the gap is
0.635% vs 0.336% / 0.336%.

**Interpretation A (paper's implicit story):** SEM acts as a
physical low-pass filter, reducing PINN error by the momentum-equation
residual. Consistent with the ~2× ratio.

**Interpretation B (adversarial):** cancellation between PINN error
and SEM discretization error at these specific polynomial orders.
Not distinguishable from A without perturbation study (open question #1).

**Failure risk:** if B holds, mildly perturbing the PINN would break
end-to-end error non-linearly, which would matter for any downstream
application that swaps in a different surrogate.

## 8. Equinox version brittleness (observed, worked around)
Equinox `.eqx` serialization stores the leaves of a pytree keyed by
class structure. Loading requires the *same class definition* at load
time. Version drift (Equinox 0.11 → 0.12 changed default init in the
`Linear` layer signature) will silently truncate or mis-key weights.

**Mitigation used:** pinned `equinox==0.11.10` exactly in the
`fem-pinns` micromamba env. Documented in `workflow.md` and
`artifacts_summary.md`.

## 9. What did NOT fail
- Repo clone: clean.
- Checkpoint reload: 6/6 cavity checkpoints load without error.
- SEM reference load: `.mat` files parse cleanly with `h5py`.
- JAX vmap over 300k points on a single A100: sub-minute.
- KD-tree provenance check: returns exact zeros as expected.
- Monotone-with-Ra scaling: reproduced in both Case A and Case B.

## Summary
No hard technical failures were encountered. All limitations of this
replication are **scope-driven** (Nektar++ out of budget, retraining out
of budget) or **provenance-gap-driven** (Nektar++ patch not in repo). The
released PINN half of NeuroSEM is well-behaved, well-pinnable, and
independently verifiable.
