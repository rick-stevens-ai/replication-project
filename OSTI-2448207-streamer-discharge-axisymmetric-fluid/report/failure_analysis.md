# Failure Analysis — OSTI 2448207

Honest accounting of what did **not** work in this replication, what was
attempted-and-abandoned, and what was explicitly ruled out of scope. Kept
separate from the main report so the replication can be re-audited without
scanning for hedges buried in prose.

---

## 1. Coupled 1-D nonlinear streamer surrogate — **FAILED (unstable)**

**Scripts:** `work/streamer1d_convergence.py`, `work/streamer1d_stable.py`.

**Intent:** Provide an independent, if reduced-dimensional, check of the
paper's C6 (peak-E convergence <1% at Δh≈4 μm) and C8 (upwind overestimates
streamer velocity vs Koren) claims without needing the full 2-D r-z HPC
run or the proprietary CWI reference curves.

**Design:** 1-D axial drift-diffusion for `n_e` and `n_i`; tridiagonal
Poisson solve for `φ`; local-field ionization source `Q = ᾱ(|E|) μ_e |E| n_e`
using an illustrative bounded transport table; forward-Euler time integration;
upwind vs Koren flux-limited advection to compare velocities.

**Failure mode:** At fine Δh (below ~10 μm), the explicit forward-Euler
treatment of the ionization source blew up before the streamer traversed the
domain. The source term is exponentially sensitive to `|E|` near the head,
and explicit stability requires Δt ≲ 1/(ᾱ μ_e |E|), which is far tighter
than the drift CFL. `streamer1d_stable.py` (an attempted stabilization via
clamped source and reduced Δt) alleviated the blow-up but at the cost of
distorting the ionization physics, making the resulting numbers
unrepresentative of anything the paper is claiming.

**Consequence:** Zero numbers from these scripts entered the evidence
artifacts. Not counted as evidence for or against C6/C8. Documented as an
attempted-but-failed secondary check (per the "no fabricated numbers" rule).

**What a proper fix would need:**
- Semi-implicit or IMEX time stepping with implicit source treatment (backward-Euler on the ionization term).
- The paper's actual transport/rate tables (Bolsig+ output for the CWI-benchmark gas), not an illustrative bounded surrogate.
- Extended to 2-D r-z axisymmetric to match the paper's actual geometry.
- All of which exceeds the efficient/free-only budget.

---

## 2. Full HPC coupled streamer benchmark (C6, C7) — **OUT OF SCOPE**

- The paper reports one benchmark run at ~48 h on 64 procs.
- The efficient budget for this replication is <25 min wall on a workstation.
- Ratio ≈ 4 orders of magnitude over budget.
- Additionally, C7 requires the proprietary CWI reference curves from the community streamer benchmark, which are not freely redistributed.
- **Not attempted. Not counted as evidence for or against.**

## 3. Strong/weak scaling study (C9) — **OUT OF SCOPE**

- The paper reports scaling from 64 up to 1024 procs on a Cray/CTS-1-class system with Trilinos/Belos GMRES + MueLu.
- No free HPC allocation was consumed for this replication.
- CherryRd (workstation) cannot produce a meaningful proxy — 8–24 cores tells us nothing about the ≥512-proc field-solver bottleneck the paper identifies.
- **Not attempted. Not counted as evidence for or against.**

## 4. Environmental / logistical friction (recovered)

**CherryRd blocked on osti.gov.** The direct `curl` from CherryRd fails.
**Recovery:** SSH to `uicgpu` (which has open outbound), fetch the PDF there,
`scp` back to CherryRd. Fetched artifact MD5 `41204e9adef92fa85c980f66c0d8d39f`
is recorded in evidence for reproducibility.

**Lesson:** Any future OSTI batch replication on CherryRd should route the fetch
through `uicgpu` (or another unblocked host) from the start rather than trying
`curl` locally first.

---

## 5. What was NOT a failure but is worth flagging

**MMS is 1-D linear, not 2-D coupled.** The C5 confirmation
(observed order 0.995) is genuine but reduced. See the GENUINE CRITIQUE
section of `REPORT.tex` and open_questions.json Q1: it certifies the paper's
stencil, not the coupled r-z behavior with the moving ionization front.
This is a scope limitation on the strength of the evidence, not a failure of the check.

**LLM-judge is not independent corroboration.** The judge (free Argo gpt-5.2)
sees only the same evidence artifacts the human sees and can share failure modes
with any single-model evaluator. Its ``moderate / PARTIAL'' agreement is a
consistency indicator, not a second opinion. Do not read it as external validation.

**"REPLICATED" would be unwarranted.** With C6–C9 unreproduced, the honest
verdict is PARTIAL. Any prompt or downstream summary that upgrades this to
REPLICATED is doing so on the strength of C1–C5 alone — which cover the paper's
arithmetic self-consistency and stencil order, but not its central coupled-physics
outputs.

---

## Summary
- 1 failed attempt (1-D nonlinear surrogate) — reported honestly, no numbers used.
- 3 explicit out-of-scope items (C6, C7, C9) — budget/data constraints, not method failures.
- 1 environmental workaround (uicgpu PDF proxy) — captured for future runs.
- 1 evidence-strength caveat (MMS 1-D vs. paper's 2-D coupled) — documented in critique + open questions.
- Overall: **PARTIAL** verdict is well supported; upgrading it would require additional evidence not present in this replication.
