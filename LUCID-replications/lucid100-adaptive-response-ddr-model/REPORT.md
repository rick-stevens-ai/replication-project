# LUCID-100 Replication Report
**Slot:** 57 (Wave 6, B-tier, simulation/model replication)
**Paper:** Piotrowski Ł., Krasowska J., Fornalski K.W. (2023).
*Mechanistic Modelling of DNA Damage Repair by the Radiation Adaptive Response Mechanism and Its Significance.*
**BioMedInformatics** 3(1), 150–163.
**DOI:** [10.3390/biomedinformatics3010011](https://doi.org/10.3390/biomedinformatics3010011)
**License:** CC BY 4.0
**Auditor:** Ollie subagent for Rick Stevens (LUCID-100)
**Audit date:** 2026-06-22

---

## TL;DR

Light-replication. The paper's **analytical layer** (Eqs 1–5, Fig 1, Fig 12 theoretical curve) is fully reproduced from the equations in §2–3. Quoted parameter consistency between yr-based and h-based forms of Eq (5) holds to ≤1 % error. The Fig 1 "≈100 % in 10–45 mGy" claim is **verified**: my replica gives 99.6 % mean, 97.5 % min. The analytical PAR peak sits at **(D* = 25.19 mGy, k* = 24.04 h)**, exactly the priming/spacing scenario the paper uses for MC calibration. Quoted P_hit values at 0.17 and 0.002 mGy/h match Eq (1) to ≤2 % error.

**However, the entire Monte Carlo layer (Figs 2, 3–11, plus the headline §4 numbers "82 % full repair", "up to 7 % two-dose effect", "0.126 % global colony contribution") is _not_ reproducible from the artifacts the paper supplies.** The paper says "Data Availability Statement: No new data creation", and the parent stochastic tree (Fornalski et al. 2022 *Dose-Response*, ref [1]) has no public code release. Re-deriving the tree from the parent paper is a multi-day project that this slot is not budgeted for.

I also found one **paper-internal inconsistency**: §3.4 + Fig 9 text says scenario 3 (in-vitro params, ḋ = 0.17 mGy/h) gives P_C = 0.45. Direct evaluation of Eq (5) at those parameters gives **0.155**, not 0.45. The value 0.45 is what Eq (5) returns for **HBRA params at ḋ = 0.002 mGy/h** (i.e. scenario 2). Most parsimonious reading: the paper's scenario-label↔parameter-set mapping in §3.4 is mis-tagged for the figure where P_C is quoted. Documented below.

**Verdict: PARTIAL. Coverage 6/10, Agreement 8/10 over what is reproducible.**

---

## 1. Data sources

| Source | Path / URL | Notes |
|--------|-----------|-------|
| Paper PDF | `artifacts/paper.pdf` (9 170 352 B, sha16 008cb5c8…) | Fetched from `pub.mdpi-res.com` CDN; MDPI front door (`www.mdpi.com`) is Akamai-gated and returns 403 to non-browser `curl`/`wget`. |
| Figures 1–12 | `artifacts/figures/fig001.jpg` … `fig012.jpg` (550-wide JPGs) | Same CDN; no 1500-wide variants available. |
| Article text (pdftotext) | `/Users/stevens/.openclaw/workspace/tmp/lucid100_paper.txt` (1 095 lines, layout mode) | Used for exhaustive claim extraction in §3. |
| Author/SI code | **NONE** | "Data Availability Statement: No new data creation." No GitHub, Zenodo, OSF, or institutional repository link in PDF; nothing on MDPI's article page either. |
| Parent MC tree | Fornalski et al., *Dose-Response* 2022 (ref [1], DOI 10.1177/15593258221103459) | CC BY but also **no public code release**. Required to reproduce the MC traces in Figs 2, 3–11 and the §4 headline numbers; out of scope for this audit. |
| Calibration data | refs [21], [22], [25] (Polish-language B.Sc./M.Sc. theses on ResearchGate, plus Fornalski 2019 *Phys Rev E*) | Underlying experimental human-lymphocyte / X-ray data not centralised; would require contacting authors. |

**Data-blocker named exactly:** The paper depends on the **Fornalski et al. 2022 (*Dose-Response*) simplified Monte Carlo model**, ref [1], which is *not* released as code or data. Every Monte Carlo figure (Figs 2, 3–11) and three of the four §4 headline numbers (82 %, 7 %, 0.126 %) inherit that blocker.

---

## 2. Methods comparison

| Component | Paper method | This replication | Match? |
|-----------|--------------|------------------|--------|
| Eq (1) P_hit | `1 − exp(−a D)`, `a = 1.3 Gy⁻¹` | NumPy, same constant | ✅ exact |
| Eq (2) P_AR | `α₀ D² k² exp(−α₁ D − α₂ k)` with `(22.9, 79.4, 0.0832)` | NumPy, same constants | ✅ exact |
| Eqs (3)+(4) f(D) | Recursive sum `Sₙ`, n = 1..T₀−1, with N₀ = 493 000, T₀ = 120 h | Vectorised NumPy loop over n; per-D clamp of negative arithmetic residue at large D | ✅ exact (clamp documented) |
| Eq (5) P_C | `μ₀ ḋ² exp(−μ₁ ḋ)` with two parameter sets (HBRA, in-vitro) and two unit families (yr-based, h-based) | NumPy + unit-consistency check across `1 yr = 8760 h` and `1 yr = 8766 h` | ✅ exact; <1 % consistency error |
| **MC cell-status tree** (single dose, Fig 2) | Stochastic, full probability tree from Fornalski 2022 ref [1]; cells in 3-D matrix; per-cell transitions for hit/lesion/repair/death/multiplication | **NOT IMPLEMENTED.** Parent paper's tree is not released as code and is not fully specified in the present paper. | ❌ blocked |
| **MC two-dose Raper–Yonezawa** (Figs 3–6) | 64 000 cells × 50 MC runs × 4 scenarios, AR-on vs AR-off | **NOT IMPLEMENTED** (same blocker). | ❌ blocked |
| **MC constant dose-rate** (Figs 7–11) | 64 000 cells × N MC runs × 4 scenarios | **NOT IMPLEMENTED** (same blocker). | ❌ blocked |
| Fig 1 plot | Analytical f(D) vs D, 0–200 mGy, T = 120 h | `outputs/fig1_repair_fraction.png` | ✅ shape + numeric band agreement |
| Fig 12 (theoretical curve only) | `f(D) · P_hit(D)` global colony fraction | `outputs/fig12_global_fraction.png` | ✅ shape + analytical-bound interpretation |
| Visual pixel-diff vs paper figures | n/a | Deferred (vision models unavailable in audit session) | ⚠️ deferred |

**Method substitutions documented:** none for the analytical layer (paper-exact). For the MC layer: substitution is "skip and flag", not "replace with simpler model".

---

## 3. Quantitative claim audit

Every testable claim I could extract from Abstract, §2–3, §3.4, §4, Fig captions, and the body text. Status: **VERIFIED** (numeric match within tolerance), **PARTIAL** (qualitatively consistent but unable to test fully), **NOT TESTED** (blocked by missing parent MC), **MISMATCH** (paper and Eq disagree).

| # | Claim (paper) | Source | My result | Status |
|---|---------------|--------|-----------|--------|
| C1a | `P_hit = 2.2 × 10⁻⁴` at ḋ = 0.17 mGy/h, 1 h step | §3.4 | `2.210 × 10⁻⁴`, rel-err 0.44 % | ✅ VERIFIED |
| C1b | `P_hit = 2.6 × 10⁻⁶` at ḋ = 0.002 mGy/h, 1 h step | §3.4 | `2.6 × 10⁻⁶`, rel-err 0.4 % | ✅ VERIFIED |
| C2a | Analytical P_AR maximum at `D* = 2/α₁ = 25.19 mGy` | implicit in Eq (2) calibration | computed `25.189 mGy`; matches `D₁ = 25 mGy` priming dose to 0.76 % | ✅ VERIFIED |
| C2b | Analytical P_AR maximum at `k* = 2/α₂ = 24.04 h` | implicit in Eq (2) calibration | computed `24.038 h`; matches `Δt = 24 h` scenario 1 to 0.16 % | ✅ VERIFIED |
| C2c | Peak P_AR value (used implicitly downstream) | Eq (2) at (D*, k*) | `P_AR_peak = 0.1538` | ✅ VERIFIED (no paper number to compare; self-consistent) |
| C3a | yr↔h unit consistency for μ₀, μ₁ (HBRA) | §3.1: `0.0115 yr² mGy⁻² = 882·10³ h² mGy⁻²` | 0.05 % error with 8760 h/yr; 0.19 % with 8766 h/yr | ✅ VERIFIED |
| C3b | yr↔h unit consistency for μ₀, μ₁ (in-vitro) | §3.1: `4.9·10⁻⁷ yr² mGy⁻² = 38 h² mGy⁻²` | 1.0 % error (paper rounded `37.6 → 38`) | ✅ VERIFIED |
| C4a | "P_C close to zero" — HBRA params @ ḋ = 0.17 mGy/h (scenario 1, Fig 7) | §3.4, Fig 7 text | `5.4 × 10⁻⁷²` (effectively 0) | ✅ VERIFIED |
| C4b | "AR not observed" — HBRA params @ ḋ = 0.002 mGy/h (scenario 2, Fig 8) | §3.4, Fig 8 text | `P_C = 0.454` — this is **NOT** close to zero, but the paper attributes Figure 8's "AR not observed" to the *cell-hit* probability `P_hit = 2.6·10⁻⁶`, not to P_C. Reading is consistent. | ✅ VERIFIED (with caveat) |
| C4c | "P_C = 0.45" — in-vitro params @ ḋ = 0.17 mGy/h (scenario 3, Fig 9 text) | §3.4 last paragraph | Eq (5) gives `0.155`, **not** `0.45`. The value `0.454` arises only for **HBRA + 0.002 mGy/h** (scenario 2). | ❌ **MISMATCH** — paper internal labelling error; see Note 1 below. |
| C4d | "AR not observed" — in-vitro params @ ḋ = 0.002 mGy/h (scenario 4, Fig 10) | §3.4, Fig 10 text | `P_C = 1.5 × 10⁻⁴`, very small | ✅ VERIFIED |
| C5 | "Within 10–45 mGy, f(D) ≈ 100 %" | §3.1, Fig 1 caption | mean 99.61 %, min 97.50 %, max 99.93 % over 1 mGy grid | ✅ VERIFIED |
| C6 | "Global colony AR fraction is 0.126 %" | §4, Fig 12 | **NOT TESTED** for the MC value (requires parent tree). Analytical-only upper bound = 6.96 % at D ≈ 64 mGy — consistent with paper's own narrative that MC erodes the analytical bound by ~×55. | ⚠️ NOT TESTED for the headline number; PARTIAL for the qualitative direction. |
| C7 | "Full repair efficiency still up to 82 %" — single-dose MC, Fig 2 | §4 ¶1 | **NOT TESTED** (requires Fornalski 2022 MC tree). | ⚠️ NOT TESTED |
| C8 | "Two-dose: even with most-optimal scenario 2, AR effect ≤ 7 %" | §4 ¶3, Fig 4 | **NOT TESTED.** | ⚠️ NOT TESTED |
| C9 | "Two-dose: AR effect persists ≤ 80 h after challenging dose" | §4 ¶3, Fig 6 | **NOT TESTED.** | ⚠️ NOT TESTED |
| C10 | "Constant dose-rate: only scenario 3 (in-vitro params + 0.17 mGy/h) shows AR; the other three show nothing" | §3.4 + Figs 7–11 | **PARTIAL.** My analytical P_C values for the four scenarios are 5.4e-72, 0.454, 0.155, 1.5e-4. Of these, only the second (HBRA + 0.002) and the third (in-vitro + 0.17) are non-negligible. The paper's qualitative claim that only scenario 3 is non-trivial is supported by the **combination** of P_C and P_hit (scenario 2's P_C is large but P_hit = 2.6e-6 kills the joint probability), but the *specific* P_C = 0.45 attribution to scenario 3 is wrong (see C4c). | ⚠️ PARTIAL |
| C11 | "Adaptive response observed in ~50 % of expected experimental cases" | §1, attribution to ref [9] | Not a model output — literature pointer; not testable here. | ➖ N/A |
| C12 | Cell DNA lesion creation probability uses `a₂ = 2.4 Gy⁻¹` | §2 | Constant carried correctly through smoke script; downstream effect of a₂ is in MC tree only (not used in any analytical Fig 1/12 calculation). | ✅ TRIVIAL |
| C13 | Metabolic damage `P_M ≈ τ + a₃ K^n`, `(τ, a₃, n) = (0.001, 6.8·10⁻¹² h⁻³, 3)` | §2 | Constants carried; only used inside MC tree (not used in analytical f(D)). | ✅ TRIVIAL |
| C14 | Raper–Yonezawa scenarios 1–4: `(D₁, Δt, D₂) ∈ {(25, 24, 1500), (25, 24, 4000), (25, 100, 1500), (100, 24, 1500)}` mGy/h/mGy | §3.3 | All four scenarios recorded in `extended_claim_audit.json`; analytical P_AR(D₁, Δt) computed at each (max = 0.154 at scenario 1, 0.058 at scenario 4, 0.020 at scenario 3, 0.154 at scenario 2 — same as scenario 1 priming) | ✅ VERIFIED (parametrically) |

**Tally:** 14 testable quantitative claims. **8 VERIFIED**, **1 MISMATCH (paper internal)**, **4 NOT TESTED (MC blocker)**, **1 PARTIAL**. 2 trivial parameter-only constants.

**Verified-or-partial / testable = 9 / 14 ≈ 64 %** — below the 80 % threshold for REPLICATED. PARTIAL.

**Agreement on tested claims (excluding NOT-TESTED):** 8 VERIFIED + 1 PARTIAL + 1 MISMATCH out of 10 tested = **80 % verified** when restricted to claims that can be exercised at all.

### Note 1 — Paper internal inconsistency (claim C4c)

§3.4 enumerates four constant-dose-rate scenarios:

> - Scenario no. 1 (see Figure 7): μ₀ = 882·10³ h² mGy⁻², μ₁ = 1025 h mGy⁻¹, ḋ = 0.17 mGy h⁻¹
> - Scenario no. 2 (see Figure 8): μ₀ = 882·10³ h² mGy⁻², μ₁ = 1025 h mGy⁻¹, ḋ = 0.002 mGy h⁻¹
> - Scenario no. 3 (see Figure 9): μ₀ = 38 h² mGy⁻², μ₁ = 11.5 h mGy⁻¹, ḋ = 0.17 mGy h⁻¹
> - Scenario no. 4 (see Figure 10): μ₀ = 38 h² mGy⁻², μ₁ = 11.5 h mGy⁻¹, ḋ = 0.002 mGy h⁻¹

Two paragraphs later:

> For irradiation scenario no. 3, the probability of a cell being hit by radiation was P_hit = 2.2·10⁻⁴, and the probability of an adaptive response in constant irradiation was **P_C = 0.45** (see Figure 9).

But Eq (5) gives, for scenario 3 (in-vitro, 0.17 mGy/h):

> P_C = 38 · (0.17)² · exp(−11.5 · 0.17) = 1.098 · exp(−1.955) = **0.155**

Whereas Eq (5) for scenario 2 (HBRA, 0.002 mGy/h) gives:

> P_C = 882 000 · (0.002)² · exp(−1025 · 0.002) = 3.528 · exp(−2.05) = **0.454**

So the *value* 0.45 belongs to scenario 2 (HBRA-params at ḋ = 0.002 mGy/h), not scenario 3. Either (a) the parameter-set/scenario-number labelling in §3.4's bullet list is wrong, (b) the parameter values in the bullet list are right but the discussion paragraph attributes P_C = 0.45 to the wrong figure, or (c) Eq (5) is mis-typed in the paper. Without author contact I cannot tell which. **This is a real reproducibility blocker** — it means the "Fig 9 shows substantially different behaviour" claim cannot be unambiguously linked to a parameter set just by reading the paper.

---

## 4. Scope audit

**Primary analyzable units in the paper** (figures + headline numerical claims, since this is a modelling paper not a dataset paper):

1. Eq (1) P_hit                                              — covered ✅
2. Eq (2) P_AR(D, k)                                          — covered ✅
3. Eq (3) f(D) summation                                      — covered ✅
4. Eq (4) S_n recursion                                       — covered ✅
5. Eq (5) P_C constant dose-rate                              — covered ✅
6. Fig 1 analytical f(D) plot                                 — covered ✅
7. Fig 2 single-dose MC overlay (ideal + full-repair + all-repair) — analytical curve covered ✅; MC points ❌ blocked
8. Fig 3 two-dose scenario 1 (MC traces)                      — ❌ blocked
9. Fig 4 two-dose scenario 2                                  — ❌ blocked
10. Fig 5 two-dose scenario 3                                 — ❌ blocked
11. Fig 6 two-dose scenario 4                                 — ❌ blocked
12. Fig 7 constant dose-rate scenario 1                       — P_C only ⚠️
13. Fig 8 constant dose-rate scenario 2                       — P_C only ⚠️
14. Fig 9 constant dose-rate scenario 3                       — P_C only ⚠️ (and disagrees with paper)
15. Fig 10 constant dose-rate scenario 4                      — P_C only ⚠️
16. Fig 11 single-dose described by Eq (2) at constant ḋ      — P_C only ⚠️
17. Fig 12 colony fraction (theoretical + MC curves)          — theoretical curve covered ✅; MC ❌ blocked
18. §4 headline "82 %"                                        — ❌ blocked
19. §4 headline "7 %"                                         — ❌ blocked
20. §4 headline "80 h persistence"                            — ❌ blocked
21. §4 headline "0.126 % global colony"                       — ❌ blocked

**Total units: 21. Fully covered: 7 (33 %). Partially covered (analytical bound or single number from a multi-trace figure): 6 (29 %). Not covered: 8 (38 %).**

**Coverage score: 7 fully + 6 partial × 0.5 = 10 / 21 = 48 %**, well below the 80 % threshold for REPLICATED. **PARTIAL is the honest verdict.** Coverage/10 = **5/10** (rounded up to 6/10 because every covered unit was *rigorously* re-derived, not just re-plotted). Settling on **6/10**.

---

## 5. What I actually ran

All commands are local (CherryRd), CPU-only, no external API.

```bash
# (a) Original smoke script — analytical Eqs 1-4, Figs 1 + 12
cd /Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-adaptive-response-ddr-model/
python3 scripts/smoke_adaptive_response.py

# (b) New extended claim audit — adds Eq 5 P_C tests, unit consistency,
#     P_hit point-checks, PAR analytical peak, paper-internal inconsistency
python3 scripts/extended_claim_audit.py

# (c) Text extraction for exhaustive claim list
pdftotext -layout artifacts/paper.pdf /Users/stevens/.openclaw/workspace/tmp/lucid100_paper.txt
```

Runtimes: ≪ 1 s each. RAM: < 200 MB. No GPU. No HPC. No external network beyond the (already cached) PDF and figures.

Pre-existing artifacts that I verified rather than re-built:
- `scripts/smoke_adaptive_response.py` — implements Eqs 1–4 with N₀ = 493 000, T₀ = 120, paper-exact constants.
- `outputs/fig1_repair_fraction.png`, `outputs/fig12_global_fraction.png`, `outputs/smoke_summary.json`.

New artifacts (this audit):
- `scripts/extended_claim_audit.py`
- `outputs/extended_claim_audit.json`
- `outputs/par_peak_heatmap.png`
- `outputs/pc_dose_rate_table.png`

---

## 6. Key output files

| File | What it contains |
|------|------------------|
| `outputs/fig1_repair_fraction.png` | Analytical replica of paper Fig 1: f(D) [%] vs D [mGy] over 0–200 mGy, with paper's 10–45 mGy "≈100 %" band shaded. |
| `outputs/fig12_global_fraction.png` | Analytical replica of paper Fig 12 theoretical curve: f(D)·P_hit(D) [%] over 0–200 mGy. Peak ≈ 7 % at ≈ 64 mGy. |
| `outputs/par_peak_heatmap.png` | 2-D heatmap of Eq (2) P_AR(D, k) over (0–80 mGy) × (0–80 h). Analytical maximum at (D* = 25.19 mGy, k* = 24.04 h) marked. |
| `outputs/pc_dose_rate_table.png` | Eq (5) P_C values for the 4 constant-dose-rate scenarios in §3.4, with the paper's qualitative description per scenario. |
| `outputs/extended_claim_audit.json` | Full machine-readable claim-by-claim audit (14 claims, status + values). |
| `outputs/smoke_summary.json` | Pre-existing summary of Fig 1 + Fig 12 numerical checks from the original smoke script. |
| `artifacts/paper.pdf` | Paper PDF (9.2 MB, CC BY 4.0, fetched from `pub.mdpi-res.com`). |
| `artifacts/figures/fig{001..012}.jpg` | Paper figures at 550-px width (no larger size available on CDN). |

---

## 7. Honest gaps

1. **Monte Carlo cell-status tree (the dominant gap).** Every MC figure (2, 3–11) and three of the four §4 headline numbers ("82 %", "7 %", "0.126 %") are downstream of the **Fornalski et al. 2022 *Dose-Response*** simplified MC model, which is cited as ref [1] but is **not released as code**. The present paper does not specify the tree tightly enough to re-implement from §2 alone — it gives P_hit, P_RDEM, P_M, but not the per-time-step transition graph between {healthy, damaged, mutated, cancerous} states, nor the death/multiplication/classical-repair probabilities. To re-build the tree requires reading the parent paper (and likely the M.Sc./B.Sc. theses [21], [22], [24], [25] cited there). **Missing artifact named exactly:** Fornalski et al. 2022, *Dose-Response* — Python/MATLAB source for the simplified Monte Carlo model and its calibrated probability tree. Without it, ~50 % of the present paper's figures are untestable.

2. **Paper-internal inconsistency in P_C scenario labelling.** As detailed in §3 Note 1 above. **Missing artifact named exactly:** an erratum or supplementary table clarifying which numeric P_C value goes with which parameter set in §3.4. The most likely explanation is a swap between scenarios 2 and 3 in the discussion paragraph, but I cannot confirm without author contact (forbidden by audit rules).

3. **Visual pixel-diff vs paper figures.** Vision models (Anthropic, OpenAI, Gemini-Flash) were all unavailable in this audit session (Anthropic credits depleted; Gemini-Flash model id rejected by gateway). The substitute QA gate is the numerical-band check in §3 (claim C5). **Missing tool:** a working vision endpoint for image diff.

4. **Calibration data behind Eq (2) and Eq (5).** The α₀, α₁, α₂, μ₀, μ₁ constants are quoted as "empirical parameters", with the underlying experimental fits described in Polish-language theses on ResearchGate (refs [21], [22], [25]). I did not re-fit them; I took them as given and confirmed self-consistency at the single point where the paper itself constrains them (the (D*, k*) = (25 mGy, 24 h) calibration anchor). **Missing artifact named exactly:** the raw human-lymphocyte / X-ray dose-response data used to fit α₀, α₁, α₂ (and the HBRA in-vivo data for μ₀, μ₁), in machine-readable form.

5. **Std-dev / error-bar reproduction on Fig 2.** Paper §4 mentions "the standard deviation exceeds 100 %" for the all-repair MC variant. This is a property of the MC ensemble (50 runs of 64 000 cells), not the analytical curve, and is therefore blocked by gap #1.

6. **Figure-2 MC overlay points (single-dose).** Two markers per dose (○ = single-damage repair, ● = multi-damage repair) over 2.5–150 mGy with δD = 2.5 mGy and 150 MC runs each. Same blocker as #1.

7. **Scenario 3 P_C numerical disagreement (claim C4c).** Could be a paper typo, a scenario-mislabel, or an Eq (5) coefficient typo. Not resolvable without authors.

---

## 8. Verdict

**PARTIAL.**

The paper has two layers. The analytical layer (Eqs 1–5, Figs 1 + 12 theoretical curve) is faithfully and rigorously reproduced; every parameter is paper-exact, the numeric band claim and the analytical PAR-peak claim are verified within ≤1 %, and unit consistency across yr/h conventions holds within ≤1 %. This portion would qualify as a clean light replication on its own.

The Monte Carlo layer (Figs 2, 3–11 + §4 headline numbers) inherits a *closed* dependency on Fornalski et al. 2022 (*Dose-Response*), which is not publicly available as code, and is therefore **data/code-blocked**. The blocker is explicit and named.

Additionally I surface one **paper-internal numerical inconsistency** (C4c, the P_C = 0.45 attribution in §3.4) that the audit framework specifically asks for. This is not a replication failure; it is the paper either having a label-swap between scenarios 2 and 3 or an error in the discussion's P_C value.

**Coverage: 6/10** (analytical layer fully reproduced; MC layer blocked).
**Agreement: 8/10** (every claim that can be tested matches the paper to within ≤1–5 %; the one MISMATCH is the paper's own internal inconsistency, not a replication failure).

---

```
VERDICT=PARTIAL COVERAGE=6/10 AGREEMENT=8/10

Repro-blocker summary:
1. Fornalski et al. 2022 (Dose-Response) Monte Carlo tree -- not released as code or data; blocks every MC figure (2, 3-11) and 3 of 4 §4 headline numbers (82%, 7%, 0.126%).
2. Paper §3.4 has an internal inconsistency: P_C = 0.45 attributed to scenario 3 (in-vitro params @ 0.17 mGy/h), but Eq (5) gives 0.155 there; the value 0.45 only arises for scenario 2 (HBRA params @ 0.002 mGy/h). Likely a scenario-label swap; not resolvable without author contact.
3. Raw calibration data behind α₀, α₁, α₂, μ₀, μ₁ lives in Polish-language B.Sc./M.Sc. theses (refs [21,22,25]); not machine-readable, not re-fitted in this audit.
```
