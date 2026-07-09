# Failure analysis — OSTI 3023480

Honest catalogue of what did NOT work, and why. Two categories: (i) my own reproduction bugs that I fixed; (ii) hard external blockers that cap the verdict at SPOT-CHECK.

## Category (i): fixed reproduction bugs

1. **v1 used the wrong dispersion variant** (ω² = (7/4 + T_e/T_i) v_ti²/R_0² *without* q dependence). This is the *near-axis* form which is degenerate at q=1 and gives 334 kHz instead of the paper's 90 kHz. Root cause: I read "on-axis" in the paper too literally and forgot that the BAAE lives at the *bottom of the BAE gap*, which is displaced from the magnetic axis.
   - Fix: switched to Turnbull BAE-gap ω = c_s √(7/4+T_e/T_i)/(qR_0) in v3. Immediately reproduced 90 kHz at q≈2.5.
   - Lesson: **do not conflate the paper's "on-axis" verbal description with the mode's actual radial peak.** The ALCON continuum plot in the paper's Fig. 3 (left) already shows the BAAE gap at intermediate ψ. I should have checked the figure caption before running the on-axis formula.

2. **v2 forgot the q-factor entirely** — cold-ion limit gave 201 kHz, still off by 2.2×. Same root cause as (1); the q-scaling is essential in the BAE/BAAE gap.

3. **First ω_*i estimate used L_n = a** (i.e. weak gradient) and got 19 kHz. Paper's ~100 kHz needs L_n ≈ a/5. I should have anticipated this: paper §5 explicitly says "the ion density gradient profile (κ_ni) is adjusted to match the original experimental measurement", i.e. steepened. L_n = a/5 is a plausible core value under the artificial density-gradient boost.

## Category (ii): hard blockers (cap verdict at SPOT-CHECK)

4. **`pdf` tool failed at every model.** Anthropic Claude — credit balance too low. google/gemini-3-flash-preview — unknown model. openai/gpt-5.5 — PDF extraction plugin disabled. Fallback: `pdftotext -layout` on macOS. It captured the paper cleanly and preserved column structure but produced plain text (no images/figures/equations rendered). Sufficient for numeric-claim extraction; insufficient for anything requiring figure inspection.

5. **`argo:claude-opus-4.8` via the LiteLLM aggregator returned 502** with "Failed to parse upstream response: choices[0].message does not match any variant". Known intermittent bug per Rick's 2026-07-05 note. Fallback was Argo GPT-5.4 and GPT-5.2 which both work fine. No effect on verdict.

6. **GTC source not accessible.** The version used by Huang et al. is Zhihong Lin group's development branch, not the public github.com/PrincetonUniversity/gtc. Even the public branch requires an access request. Without GTC we cannot rerun a single one of the paper's simulations. Impact: claims C2, C5 (growth rate), C7 (mode structure), C8, C9 (EP suppression) are all untested by direct means. We can only support them via analytic/consistency arguments.

7. **NOVA source not accessible.** PPPL-internal MHD eigenmode code. Same impact — C3 tested only qualitatively by BAE-gap formula with q≈3.

8. **ALCON source not accessible.** Deng et al. 2012 continuum solver, part of the GTC workflow. Impact: we could not independently generate the Alfvén–acoustic continuum plot (paper Fig. 3 left) — but the analytic BAE-gap formula is a valid substitute at the bottom of the gap.

9. **TRANSP profile files not public.** ST40 discharge #09894 kinetic profiles from TRANSP run 09894A03 were not deposited anywhere we could find. We used only the on-axis values quoted verbatim in the paper §3. Impact: we cannot check radial profile sensitivity of the results (part of open question Q4).

10. **No experimental raw data.** ST40 Mirnov spectrogram (Fig. 1) is not archived publicly. Impact: we cannot independently verify the 100–150 kHz lab-frame observation of the mode. We accept it as reported.

## What would move the verdict from SPOT-CHECK → PARTIAL

Obtaining and running GTC (or an equivalent gyrokinetic PIC code, e.g. XGC or GEM in the electromagnetic limit) with the ST40 equilibrium would let us independently derive the growth rate. Even a single benchmark case matching Huang et al.'s Fig. 4 (antenna scan) to within 20 % would upgrade at least C2, C5 to reproduced. That is a ~1-week compute + code-onboarding effort per person, well outside the wave brief.

## What would move it to REPLICATED

Full pipeline (TRANSP profiles → XMAP or CHEASE equilibrium → GTC gyrokinetic run with anisotropic EP distribution → NOVA cross-check) reproducing Huang et al.'s Figs. 3–7. This is essentially redoing the paper. Requires the profile files and INCITE-scale compute. Not achievable in this project.
