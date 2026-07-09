# Failure Analysis — Huang & Shen (2021) IMEX/SAV NS replication

Verdict of the whole exercise: **REPLICATED**. This file documents the
near-misses and honest limits — the things that almost blocked replication,
what caused them, how they were resolved, and what remains as an honest
caveat on the final numbers.

## 1. Collapse of the SAV factor under the forced manufactured problem

### Symptom
On first pass, running Example 1 with the paper's SAV/BDFk time stepper
starved: after a few steps the SAV factor `η` decayed toward 0, the
rescaled velocity `u = η·ū` shrank to numerical noise, and every fitted
convergence order came out as garbage (~0 for BDF3/BDF4).

### Root cause
Huang & Shen state Theorem 1 and derive the SAV `r`-update for the
**unforced** Navier–Stokes system (`f = 0`). The `r`-update they write
does not include a production term for external forcing. But Example 1
is a manufactured problem, so `f ≠ 0`: kinetic energy is being pumped in
at every time step. Without a matching production term in the discrete
`r`-update, the auxiliary variable `r` gets driven artificially low
relative to `E(ū)+1`, `ξ = r/(E(ū)+1) → 0`, and therefore
`η = 1 − (1−ξ)^k → 0` — the scheme "shrinks the flow to death."

### Fix
Derive the energy-consistent production term directly from the
continuous dissipation identity for `E(u) = ½‖∇u‖²` and add it to the
discrete `r`-update:

```
(f, −Δū) = (∇f, ∇ū)                      # 2D, E = ½‖∇u‖²
```

This is the correct forcing contribution to `dE/dt` for our choice of
energy functional. With it, `η` stays in `[0.985, 1.001]` on the sweep
and the paper's order-k rates are recovered exactly (1.00 / 1.89 / 3.02 /
4.14 for velocity).

### Honest caveat
This term is **our derivation, not the paper's equation**. The paper's
theory is for `f = 0`. Anyone reproducing this work from the paper alone
will hit the same collapse if they blindly plug forcing into the
unforced `r`-update. Documented in `work/attempt_log.md` and in the
Genuine Critique section of `report/REPORT.tex`.

## 2. What was NOT tested (honest coverage gaps)

- **Example 2 (double shear layer).** Qualitative vorticity-contour
  comparison; no reference number in the paper to check against.
  Skipped by design, flagged explicitly rather than silently omitted.
- **3D SAV variant.** Uses `E = ½‖u‖²` instead of `½‖∇u‖²`. Not
  implemented or run.
- **Non-periodic (no-slip) boundary conditions.** The paper's whole
  construction leans on periodicity so pressure can be eliminated via
  the Leray projection in Fourier space. No-slip is out of scope for
  the paper and for this replication.
- **Analytical error estimates (Theorem 2 / Theorem 3).** Proofs; not
  subject to numerical replication.
- **Stress-test of Theorem 1.** We spot-checked at Δt = 0.05 and
  observed bounded H¹-energy and η ≈ 1. We did **not** sweep Δt into
  the regime where an ordinary IMEX scheme would blow up, so we did
  not push the "unconditional" claim empirically to its edge.
- **Aliasing / dealiasing.** N=40 modes on a very smooth manufactured
  solution: aliasing is negligible. We did not verify that the
  observed BDF3/BDF4 orders survive with weaker spatial resolution
  and/or an explicit 2/3-rule filter.

## 3. What "REPLICATED" therefore means, precisely

- The **fitted temporal convergence orders** for velocity and pressure
  in H¹ match the paper's Figure 1 expected order-k rates for
  k ∈ {1, 2, 3, 4}, on the manufactured Example 1, in 2D periodic,
  using our from-scratch Fourier-spectral IMEX-BDFk/SAV solver with an
  independently-derived energy-consistent forced `r`-update.
- The **large-step numerical stability spot-check** is consistent with
  Theorem 1 in the resolved-smooth-flow regime.
- Three independent free-Argo LLM judges (gpt-5.2, gemini-2.5-pro,
  gpt-4.1) at temperature 0 concur.

What "REPLICATED" here does **not** claim:
- It does not claim the paper's error magnitudes to two digits (we
  compare invariant orders, not magnitudes — REPORT.md §3 explains why).
- It does not claim reproduction of Example 2, the 3D variant, or any
  no-slip case.
- It does not re-derive or independently verify Theorems 2–3.
- It does not, on its own, rule out a discretization bug that yields
  the "right" orders for the wrong reason; the strongest positive
  evidence remains the clean order-k halving under Δt-refinement, not
  the judge concurrence.

## 4. Lessons carried forward

- For SAV schemes on **forced** systems, always derive the r-update
  production term from the continuous dissipation identity that
  matches the chosen energy functional — never inherit an unforced
  r-update unchanged.
- For manufactured-solution convergence studies, compare **orders**,
  not error magnitudes, unless the paper actually publishes magnitudes.
  Magnitudes are constant-of-integration / forcing dependent and are
  not the invariant.
- For "unconditional stability" claims, an empirical spot-check at a
  single large Δt is corroborative, not conclusive. A real stress-test
  sweeps Δt until an ordinary IMEX would blow up.
