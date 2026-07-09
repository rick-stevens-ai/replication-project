# Failure analysis — Lubich (2008) replication

Nothing in the replication produced a wrong-verdict outcome, but several
issues surfaced and were handled. This file records them so a future
replicator (or an audit) can see what could have gone wrong, what did, and
what to watch for.

## 1. Journal PDF was Cloudflare-gated

**Symptom.** Direct fetch of the AMS journal PDF failed under Cloudflare
challenge from the assistant's default egress.

**Root cause.** AMS journals sit behind a bot-mitigation layer that
rejects headless User-Agents.

**Resolution.** Fetched the author preprint (`speq.pdf`) from the Tübingen
page instead — same paper, openAccess per S2 flag. Verified byte-length
and computed md5 (`608e48c81bd247f3d8beef9b420d68cb`, 169616 B) for the
audit trail. A one-off `ssh uicgpu` was also tried as a Cloudflare-bypass
egress but was not needed once the preprint mirror worked.

**Lesson.** For AMS / paywalled math journals: check the author's
university page first; the preprint is almost always the same PDF.

## 2. LLM-judge intended model was unavailable (502)

**Symptom.** `argo:claude-opus-4.8` and `argo:claude-opus-4.7` both
returned 502 from the Argo proxy at run time.

**Root cause.** Upstream Argo flake — not a local config issue (the
same endpoint served `argo:claude-sonnet-4.6` fine).

**Resolution.** Fell back to `argo:claude-sonnet-4.6` and logged the
substitution in REPORT.md §3.4.

**Lesson & risk.** Sonnet is weaker than Opus at spotting subtle
theorem-vs-experiment mismatches. In this case the mismatches were
zero, so the substitution did not change the verdict — but on a
borderline paper the substitution could matter. Log the actual
model used, and note when Opus was the intended judge but was down.

## 3. Reference-solution ceiling risk

**Not a failure but a bounded assumption.** The "true" solution against
which errors were measured is Strang at τ_ref = 1/32000, i.e. our own
scheme at a much finer τ. This is standard practice for smooth-data
PDE convergence studies, but it means:
- Any systematic bug in our Strang implementation that has the same
  order-of-error would go undetected (the convergence study would
  still show clean rate 2).
- The observed error is capped above by the reference's own error;
  at τ = 1/800 the safety margin is 40²=1600× (reference is 1600×
  smaller step) which is comfortable but finite.

**Mitigation applied.** Free-Schrödinger plane-wave sanity test
(‖e‖_L² = 4.4·10⁻¹⁴, machine precision) rules out a broken kinetic
half-step. No independent-solver cross-check was done; that would
strengthen the verdict further.

## 4. Regularity gap between test data and theorem hypothesis

**Not a failure but a scope limitation.** The theorems assume H⁴
regularity. We tested C^∞ data (Gaussian bump, low-mode trig), which
is strictly stronger. Our clean order-2 result therefore says nothing
about the sharpness of the rate at the H⁴ boundary. This is a
"replication passes trivially because we made the input easier than
the theorem needs" caveat and is documented in the REPORT.md
"Caveats / limitations" section and in `open_questions.json` OQ5.

## 5. Dimension gap (1D vs R³)

**Not a failure but a scope limitation, and it deserves visibility.**
The paper proves theorems on R³; we ran on 1D periodic. The paper's
own one-sentence extension claim sanctions the reduction, but:
- The 3D Poisson solve is qualitatively different from
  `V̂ = ρ̂/k²` scalar division on a 1D Fourier line.
- Whole-space R³ far-field decay is not modelled by any periodic
  reduction.

Our replication does not exercise 3D behaviour at all. Documented in
REPORT.md §5 "Caveats / limitations" and `open_questions.json` OQ4.

## 6. Sign symmetry near-tie is weaker evidence than it looks

**Not a failure but an interpretability caveat.** Focusing (+) and
defocusing (−) cubic NLS produced near-identical errors:
- defocusing at τ=1/50: ‖e‖_L² = 8.08·10⁻⁶
- focusing at τ=1/50:  ‖e‖_L² = 1.15·10⁻⁵

At short time and low amplitude the two problems are essentially
identical dynamics; focusing NLS's characteristic soliton dynamics
and (in higher-D) blow-up are not reached in a T=1, low-amplitude,
smooth-mode run. So "both signs converge at order 2" is a weaker
statement about the focusing case than the numbers make it look.
Called out explicitly in REPORT.tex §"Genuine critique" item 5.

## 7. Machine-precision mass drift is a specification of round-off,
not of splitting error

**Handled correctly, worth naming.** Mass drift is O(10⁻¹³) and grows
~sqrt(N_steps). This is a round-off ceiling for a unitary scheme, not
an artifact of the splitting. Reporting it as "drift ≤ 1.2·10⁻¹³"
correctly conveys "machine precision" — but a naive reader could
misread the number as a splitting-error residual. It is not.

## 8. No independent-solver cross-check

**Deliberate omission.** No Sanz-Serna exponential integrator or
Crank–Nicolson reference was implemented. Enumerated in REPORT.tex
§"Genuine critique" item 7 as a real weakness of the verdict.

## Failures that did NOT occur

- No aliasing issues at N=512 for the smooth periodic data used.
- No time-step / grid-size instability at any τ tested (Strang is
  unconditionally stable in L² for the free-Schrödinger + real-valued
  potential composition; consistent with paper).
- No sign errors in the Poisson symbol (verified both signs give
  identical-to-round-off convergence tables — a check that would
  have exposed a sign bug in the FFT-based V solve).
- No convergence-order collapse at the smallest τ (would indicate
  that the reference solution's own error was becoming a floor;
  did not happen — order stays 2.000–2.001 at τ=1/800).
