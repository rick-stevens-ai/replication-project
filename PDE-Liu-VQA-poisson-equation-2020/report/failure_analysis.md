# Failure Analysis — Liu 2020 VQA-Poisson Replication

## Overall
This replication returned a **PARTIAL** verdict. The two analytic claims (C1,
C2) reproduced exactly. The numerical claim (C3) reproduced for m=2..5 and
was truncated at m=6. There were no scientific failures — the paper's
algorithm is honest and reproducible on everything tested. The gaps are
operational (compute budget, scope decisions) or explicitly-noted untested
claims. This document lists them.

## F1 — m=6 sweep truncation (the headline gap)

**What happened.** The paper's Fig. 4 covers m=2..6. This replication fully
covered m=2..5 (p_min = 1, 2, 3, 3 with best fidelities 0.9955, 0.9958,
0.9955, 0.9917 respectively). For m=6, only p=1 (fidelity 0.9428) and p=2
(fidelity 0.9692) were completed. The p=3..8 sweep for m=6 was still
running on uicgpu when the report was finalized.

**Root cause.** Each m=6, p ≥ 3 job takes >800 s serial. Even with
GNU parallel `-j 16` on uicgpu, the batch was ~35 minutes in when
cut off. Total replication wave budget was ~60 minutes end-to-end.

**Impact on verdict.** Downgrades the numerical claim (C3) from REPLICATED
to PARTIAL for the largest qubit count in the paper's stated range. The
paper's own Fig. 4 inset predicts p_min ≈ 4–5 for m=6, and the m=5, p=3
result (0.9917) plus m=6 trend (p=1: 0.9428, p=2: 0.9692) is
consistent with a threshold near p ≈ 4. But an extrapolation is not a
measurement.

**Mitigation available.** Run m=6, p=3..8 to completion on uicgpu
(~35 additional minutes at -j 16). This would either confirm p_min ≈ 4–5
(upgrading the overall verdict to REPLICATED) or reveal an unexpected
failure mode worth investigating on its own.

**Why not done here.** The replication wave brief specifies a single-task,
budget-bounded independent replication. Doubling wall time to close a gap
that the paper's own trend already predicts was judged out-of-scope for
this pass. Flagging it explicitly here is the honest report.

## F2 — Ansatz mismatch is uncontrolled

**What happened.** The paper uses a specific hardware-efficient ansatz
(Fig. 3). This replication uses a "Fig. 3 style, simplified" ansatz: per
layer, RX(θ) on every qubit, RZ(θ) on every qubit, linear CNOT chain
`0→1→…→m−1`, total `2·m·p` params.

**Root cause.** Paper Fig. 3 was interpreted qualitatively rather than
gate-for-gate replicated. There is no released reference implementation
from Liu et al. that we consulted.

**Impact.** Fidelities and p_min values can shift by ±1 layer under
ansatz variation. Our p_min matched or came within one layer of the
paper's inset for m=2..5 — encouraging but not definitive. If a bit-exact
ansatz reproduction gave p_min values one layer smaller, C3 would look
even stronger.

**Mitigation available.** Reimplement the paper's Fig. 3 ansatz exactly
and re-run C3 for m=2..5. Compare p_min side-by-side.

## F3 — 20 random restarts is modest for barren-plateau-suspect landscape

**What happened.** `run_vqa(m, p)` uses 20 random-init restarts (mixing
uniform, near-zero, near-π perturbations). Each restart runs both L-BFGS-B
and BFGS from scipy (`gtol=1e-9`, `maxiter=500`).

**Root cause.** 20 was a wall-time compromise. Larger m benefit from more
restarts because the loss landscape becomes exponentially flatter
(McClean et al., 2018, "Barren plateaus in quantum neural network
training landscapes").

**Impact.** "Best of 20" may under-report the true achievable fidelity at
larger m. For m=6, adding restarts might push best fidelity above 0.99
without increasing p — but might not. Not knowing which is a real gap.

**Mitigation available.** For each `(m,p)` at m ≥ 5, run 100+ restarts
and report the fidelity distribution, not just the max. Track gradient
variance across restarts as a barren-plateau proxy.

## F4 — C4 (extension to d-D and general Toeplitz) is untested

**What happened.** The paper's Appendix A extends the decomposition to
d-D Poisson and general tri/pentadiagonal Toeplitz matrices. This
replication did not test any of that.

**Root cause.** C1 and C2 already validate the recursive scheme, and the
paper's Appendix A generalization follows by inspection. We chose not to
implement it.

**Impact.** "By inspection" is not "tested." A subtle mismatch between
our reading of Appendix A and the authors' intent would be invisible.

**Mitigation available.** Implement `decompose_A_2D` via Kronecker sum
and verify item counts for m_x=m_y=1..4; extend to 3-D on uicgpu.

## F5 — C5 (Bell-measurement scaling) is untested

**What happened.** The paper's Eq. 20 introduces a Bell-measurement trick
to evaluate ⟨X⊗A⟩ efficiently. This replication used exact statevector
simulation, which is strictly stronger for validating the *math* but says
nothing about the *shot-scaling* claim.

**Root cause.** Statevector was faster to implement and sufficient for
the fidelity claim (C3).

**Impact.** The paper's efficiency argument for NISQ hardware is
untested. Whether the Bell-measurement trick actually delivers the
claimed sample complexity in a shot-based setting is unknown from this
replication.

**Mitigation available.** Implement the Bell-measurement subroutine in
Qiskit Aer with shot noise; measure shots needed to reach a
convergent estimate of ⟨A²⟩ at fixed epsilon.

## F6 — Environment drift between local and uicgpu

**What happened.** Local runs used python 3.14, numpy 2.5.0, scipy 1.18.0.
uicgpu runs used python 3.10, numpy 1.23.5, scipy 1.10.1. No single
`(m, p)` point was cross-checked across both environments to bound
optimizer-induced drift.

**Root cause.** uicgpu had a pre-existing env; time budget did not
justify a fresh matched env.

**Impact.** Optimizer behaviour (BFGS line-search tolerances,
random-state seeding) can differ subtly between scipy majors. C3 results
for m=5, 6 come exclusively from uicgpu; comparability with the m=2..4
local results is assumed, not verified.

**Mitigation available.** Rerun m=4, p=3 on uicgpu with matched
random seed and confirm fidelity matches the local run within 1e-4.

## F7 — LLM-judge is not a code auditor

**What happened.** `argo:gpt-5.2` was fed `results.json` and the console
log. It rated per-claim verdicts with confidences 98/97/85 and an overall
PARTIAL at confidence 90.

**Root cause.** By design: LLM-judge is an evidence synthesizer, not a
code reviewer.

**Impact.** The confidence-90 overall verdict is calibrated to the
evidence presented, not to absolute ground truth about the paper. If
`liu_vqa.py` had a silent bug that produced a self-consistent but
paper-inconsistent output, the LLM-judge would not catch it — but neither
did any external human reviewer during this replication.

**Mitigation available.** Cross-validate `decompose_A(m)` for m=2 by
hand against Eq. 11; do the same for `decompose_Asq_pure(m)` at m=2 vs.
paper Eq. 18. The reconstruction check against ground truth in
`verify_A(m)` and `verify_Asq(m)` (both max-abs error 0.0) is the
strongest independent bug filter — an implementation error would show up
as nonzero reconstruction error.

## Summary Matrix

| ID | Description | Severity | Blocking? | Mitigation cost |
|---|---|---|---|---|
| F1 | m=6 sweep truncation | Medium | Verdict-shifting | ~35 min uicgpu |
| F2 | Ansatz mismatch | Low | No | ~30 min impl + 20 min rerun |
| F3 | 20 restarts modest | Low | No | ~2 h uicgpu for 100-restart sweep |
| F4 | C4 untested | Low | No (out of scope) | ~1 day |
| F5 | C5 untested | Low | No (out of scope) | ~1 day |
| F6 | Env drift | Low | No | ~10 min cross-check |
| F7 | LLM-judge not a code audit | Informational | No | Manual hand-check |

None of F1–F7 upgrade or downgrade the PARTIAL verdict. F1 alone could
promote it to REPLICATED with additional compute; the rest are known
limitations honestly reported.
