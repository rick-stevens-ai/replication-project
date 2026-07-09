# Failure Analysis — OSTI 3374709 (semi-implicit ES-PIC verification)

Verdict: **REPLICATED** (scoped to C1 in the cold 1D limit).

This is not a post-mortem of a failed replication — the core claim was
reproduced. It is an honest catalogue of the ways this replication is
narrower, thinner, or more fragile than the headline verdict alone
would suggest. Each item below is either something that did not work,
was not attempted, or is a plausible risk to the verdict.

## 1. Scope: only 1 of 6 claims was actually re-executed

- The paper's argument spans six claims (C1–C6).
- This replication tested **C1** quantitatively (SIPIC effective
  dielectric + plasma-mode down-shift, Eqs. 12/16) and inherited
  **C3** (stability at large `ωpe·Δt`) as a byproduct of the same
  runs.
- **C2** (modified Bohm–Gross) was reduced to its cold limit (`vth = 0`),
  which zeros the thermal term and collapses C2 back into C1 — so C2
  was not really tested on its own.
- **C4** (hybrid modes, Eqs. 19–20) was not attempted — needs a
  magnetized 2D setup, out of scope for the 1D core.
- **C5** (total energy conservation < 2.5 %, Fig. 2) was not attempted
  — needs full WarpX/Aleph runs and long-time energy diagnostics that
  the from-scratch code does not emit.
- **C6** (Landau damping rates preserved, §III.C) was not attempted
  — the cold-plasma setup used to isolate C1 cannot produce Landau
  damping.
- A paper-level "REPLICATED" verdict must therefore be read as
  "the paper's central verification claim (C1) is reproduced in the
  friendliest possible setting"; it is **not** a re-verification of
  the paper's full §III VERIFICATION suite.

## 2. Under-characterized 10 % error at ωpe·Δt = 16

- At the most extreme step size in the sweep, the measured ω/ωpe =
  0.069 vs Eq. 16 prediction 0.062 gives a **10.2 %** error.
- The other four sweep points (`ωpe·Δt ∈ {1, 2, 4, 8}`) agree to
  0.9–3.9 %. The 10 % jump at 16 is a real outlier in the trend.
- At `ωpe·Δt = 16` there are only **~6 samples per down-shifted
  oscillation** (down-shifted period ≈ 91 / ωpe, sampling period 16 /
  ωpe). The Hann-windowed FFT + parabolic sub-bin interpolation
  diagnostic is near its resolution floor there.
- The replication did **not** repeat the extreme case with a longer
  time series, alternative estimators (Prony, matrix-pencil, LSQ
  sinusoidal fit), or multiple seeds/particle counts to separate
  scheme error from diagnostic error.
- **Risk:** If the 10 % error is real scheme departure, it slightly
  narrows the range of `ωpe·Δt` over which "SIPIC matches Eq. 16" can
  be claimed. If it is diagnostic, the sweep agreement is even better
  than reported. Either way, the current evidence does not
  distinguish.

## 3. κ-notation reading is a judgement call, not a confirmation

- The paper's Eq. 12/13 written literally (`κ = 1/F`, `ω² = ωp²/κ`)
  gives an **up**-shift `ω² = ωp² · F` — the opposite direction from
  Eq. 16 text ("reduced frequency") and Fig. 1 (downward contours).
- The replication treats this as a typographic / bookkeeping inversion
  and implements the physical operator from Eqs. 9–10 directly, which
  produces the down-shift `1/√F` matching Eq. 16.
- This is almost certainly the intended reading, and the numerical
  agreement supports it. But the replication did **not** (a) contact
  the authors to confirm, (b) implement both readings and check which
  is consistent with the paper's own Fig. 1 contours, or (c) inspect
  WarpX/Aleph source to see which formulation is at runtime.
- **Risk:** low but nonzero — the whole replication rests on picking
  the physically-consistent reading.

## 4. Friendly-setting bias in the test problem

- Cold plasma (`vth = 0`) — thermal effects zeroed.
- 1D — no hybrid or magnetic-field physics.
- Single-mode-1 perturbation with `amp = 0.02` and `N = 80,000` CIC
  particles — unusually clean signal-to-noise; no multi-mode coupling.
- Periodic box, uniform density — no boundaries, no sheaths, no
  gradients.
- This is the correct setup for isolating C1, but it is also the
  setup where the SIPIC operator is under the least stress. The paper
  targets high-density plasma **at scale**; this replication does not
  approach that regime.

## 5. No cross-code comparison

- The paper's verification is partly a WarpX ↔ Aleph code-to-code
  exercise.
- This replication is a from-scratch NumPy PIC that touches neither
  WarpX nor Aleph. That is deliberate (from-scratch replication
  avoids inheriting bugs from either code), but it means:
  - If WarpX and Aleph disagreed with each other on some detail, this
    replication would not have seen it.
  - Nothing in this work adjudicates the paper's cross-code agreement
    claims — only the underlying analytic prediction (Eq. 16).

## 6. Single-judge, single-prompt LLM verdict

- Judge: free Argo `argo:gpt-5.2` at `localhost:44497`, temperature 0,
  one prompt, one run.
- Judge was given the measured-vs-analytic table **already framed as
  measured vs prediction** — not blind.
- No adversarial second judge, no human plasma physicist in the loop.
- **Risk:** low for a task this arithmetic — the judge's role is
  closer to a sanity check on the table than an independent verdict.
  But the verdict should be read as "the numbers in the table support
  a REPLICATED call," not as "an independent oracle blindly agrees."

## 7. Diagnostic caveats not fully quantified

- FFT of a finite time series with Hann window has known bias in
  frequency estimation, especially near the Nyquist frequency of the
  sampling rate 1 / Δt.
- Parabolic sub-bin interpolation is a well-known but approximate
  correction; it can bias low or high depending on where the true
  peak sits relative to the FFT bin.
- The "physical search band" restricts the peak search but is not
  documented in REPORT.md as a specific numeric window.
- No repeated runs with different RNG seeds are reported; the tables
  give point estimates without uncertainty bars.

## 8. Paper-internal ambiguities not resolved

- **Δt convention:** Table I gives `Δt = 2a/ωpe` (`ωpe·Δt = 2a`)
  while §III.A prose gives `Δt·ωpe = a/2`. The replication sweeps
  the union of both (`ωpe·Δt ∈ {1, 2, 4, 8, 16}`) because Eq. 16
  depends only on the product. Result is robust, but the paper's
  own ambiguity is not resolved.
- **Sign / direction of κ:** see item 3.

## 9. What could still overturn the verdict

- Author confirmation that the κ-notation reading implemented here
  is wrong (item 3) → would require re-running the sweep with the
  other reading and re-checking against Fig. 1.
- A more careful diagnostic at `ωpe·Δt = 16` showing that the 10 %
  error is real scheme departure across estimators/seeds (item 2) →
  would tighten the claim to "REPLICATED for `ωpe·Δt ≤ 8`."
- An independent 2D magnetized run showing C4 does **not** hold
  (item 1) → would leave C1 replicated but downgrade paper-level
  claims.

## 10. Bottom line

The verdict `REPLICATED` is honest **for what was tested** (C1, cold
1D, ωpe·Δt sweep to 16, C_SI = 4). It should not be read as
"the paper is verified" or "the paper's scheme works in production"
— neither of which this replication is instrumented to say.
