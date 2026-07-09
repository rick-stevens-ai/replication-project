# Failure Analysis (honest, no whitewash)

## Bottom line
The tracker label for this slot is **REPLICATED**. The substantive audit verdict is
**PARTIAL (coverage 6/10, agreement 8/10 on tested claims)**. Both facts are
preserved here. The analytical layer of the paper is faithfully reproduced; the Monte
Carlo layer — which carries every headline number that gives the paper its persuasive
force — is *not* reproduced and could not be reproduced from the artifacts the paper
supplies. This document lists what didn't work, why, and what residual uncertainty
remains.

---

## 1. What didn't work

### 1.1 Monte Carlo layer — total blocker (Figs 2, 3–11; §4 headlines 82 %, 7 %, 0.126 %)
- **What was attempted:** re-implement the per-cell Monte Carlo tree the paper uses to
  generate Fig 2 (single-dose overlay of "ideal", "full repair", "all repair"
  variants), Figs 3–6 (two-dose Raper–Yonezawa scenarios), Figs 7–11 (constant
  dose-rate scenarios), and the §4 headline numbers (82 % full repair, up to 7 %
  two-dose effect, 80 h persistence, 0.126 % global colony contribution).
- **What blocked it:** the MC tree is a dependency on **Fornalski et al. 2022
  (*Dose-Response*, DOI 10.1177/15593258221103459)**, cited as ref [1]. That paper is
  CC BY but has **no public code release**. The present paper does not fully specify
  the per-time-step transition graph between {healthy, damaged, mutated, cancerous}
  states, nor the death/multiplication/classical-repair probabilities. It quotes
  P_hit, P_RDEM, and P_M coefficients but not the transition matrix that would let
  someone re-derive Figs 2, 3–11 from §2 alone.
- **Cost of un-blocking:** 3–5 solid days if the parent paper is well-specified, 1–2
  weeks otherwise. Out of scope for this audit slot.
- **Consequence:** ~50 % of the paper's figure surface area and 3 of 4 §4 headline
  numbers are neither confirmed nor refuted by this replication. Any downstream
  claim that Piotrowski et al. is "reproduced" needs to be qualified with "the
  analytical layer is, the Monte Carlo layer is not".

### 1.2 §3.4 P_C label swap (MISMATCH C4c) — unresolved
- **What I found:** §3.4 attributes P_C = 0.45 to scenario 3 (in-vitro parameters at
  ḋ = 0.17 mGy/h). Direct evaluation of Eq (5) at those parameters gives **0.155**,
  not 0.45. The value 0.45 only arises for scenario 2's parameters (HBRA at
  ḋ = 0.002 mGy/h).
- **Three candidate explanations:** (a) the discussion paragraph swaps scenarios 2
  and 3 when quoting P_C; (b) the bullet-list parameter values for scenario 3 are
  wrong; (c) Eq (5) coefficients (11.5, 38) are typos.
- **Why I couldn't disambiguate:** each candidate has different implications for
  whether Figs 7–10 show the right curves, and this requires either author contact
  (not permitted during audit) or a pixel-diff of the paper figures against
  re-synthesized Eq (5) curves under each hypothesis. The pixel-diff was deferred
  because vision endpoints were unavailable in the audit session.
- **Residual uncertainty:** the "Fig 9 shows substantially different behaviour"
  claim cannot be unambiguously linked to a parameter set just by reading the paper.

### 1.3 Visual pixel-diff of paper figures — deferred
- **What was attempted:** run a vision model (Anthropic/OpenAI/Gemini-Flash) over the
  12 paper JPGs vs my Fig 1, Fig 12, and PAR-heatmap outputs to catch qualitative
  disagreements that pure numerical claim-audit would miss.
- **What blocked it:** during the 2026-06-22 audit session, Anthropic credits were
  depleted and Gemini-Flash's model id was rejected by the gateway.
- **What I substituted:** the numeric-band check on claim C5 (mean 99.61 %, min
  97.50 %, max 99.93 % over 10–45 mGy) is a proxy for "Fig 1 shape agrees with
  paper".
- **Residual uncertainty:** low. The analytical layer is deterministic and
  paper-exact; there is no realistic way for the numeric band check to pass while a
  pixel-diff would fail.

### 1.4 Raw calibration data — not re-fitted
- **What was skipped:** the underlying human-lymphocyte / X-ray dose-response data
  behind α_0=22.9, α_1=79.4 mGy⁻¹, α_2=0.0832 h⁻¹ (Eq 2) and μ_0/μ_1 for HBRA and
  in-vitro (Eq 5). Cited to Polish-language B.Sc./M.Sc. theses on ResearchGate
  (refs [21,22,25]) plus Fornalski 2019 *Phys Rev E*.
- **Why:** not machine-readable; Polish theses; out of scope for a light replication.
- **What I did instead:** took constants as given, confirmed self-consistency at the
  single point where the paper's own text constrains them (the (D*, k*) =
  (25 mGy, 24 h) calibration anchor — verified to <1 %).
- **Residual uncertainty:** medium. The α_i and μ_i could be idiosyncratic to the
  calibration cell line and radiation quality; see open question #4.

### 1.5 Standard deviation reproduction on Fig 2 — blocked
- **What the paper says:** §4 mentions "the standard deviation exceeds 100 %" for the
  all-repair MC variant.
- **Blocked by:** the MC tree gap in §1.1.

---

## 2. What worked (for balance, but this is not a whitewash — read §1 first)

- **Every equation in §2–3 (Eqs 1–5) is faithfully re-implemented** with
  paper-exact constants.
- **Claim C5** ("f(D) ≈ 100 % in 10–45 mGy") **verified numerically** at 99.61 % mean.
- **Claims C1a, C1b, C2a, C2b, C3, C4a, C4b, C4d verified** to ≤2 % relative error.
- **The analytical PAR peak** falls exactly at the (D_1=25 mGy, Δt=24 h) priming
  scenario the paper uses for MC scenario 1 — self-consistent to <1 %.
- **Unit consistency (yr ↔ h)** for μ_0, μ_1 holds to <1 % (both 8760 and 8766 h/yr
  conventions checked).

---

## 3. Residual uncertainty (in order of severity)

1. **[CRITICAL]** Whether the paper's MC headline numbers (82 %, 7 %, 0.126 %,
   80 h persistence) are reproducible at all. Requires re-implementing the
   Fornalski 2022 tree. Cost: 3–5 days minimum.
2. **[MEDIUM]** Which resolution of the §3.4 P_C label swap is correct, and whether
   it changes the qualitative story in Figs 7–10.
3. **[MEDIUM]** Whether the empirical constants generalize beyond the HBRA/human
   lymphocyte X-ray calibration to other cell lines and LETs. See open question #4.
4. **[MEDIUM]** Whether "mechanistic" in the paper's title is doing real work or is
   phenomenological reparametrization. See open question #3.
5. **[LOW]** Whether the analytical Fig 1 and Fig 12 replicas would survive a
   pixel-diff against the paper figures. Should survive; not tested.
6. **[LOW]** Whether the specific choice of 1 yr = 8760 vs 8766 h in the μ_i
   calibration matters at the reported precision. Verified: 0.14 % swing, below all
   quoted tolerances.

---

## 4. What this replication does *not* license

- **A claim that the low-dose radioadaptive response is confirmed at the magnitudes
  the paper reports.** Only the *shape* (peak at ~25 mGy priming, ~24 h spacing) is
  confirmed. The 82 %, 7 %, and 0.126 % magnitudes are not.
- **A claim that a specific molecular pathway (ATM, p53, NRF2) is validated.** The
  paper's model is phenomenological. See open question #3.
- **A claim that adaptive response translates to clinical fractionated
  radiotherapy.** The paper's dose regime (10–100 mGy priming, 1.5–4 Gy challenge,
  24–100 h spacing) does not overlap standard clinical fractionation (1.8–3 Gy per
  fraction, 24 h spacing, 20–40 fractions), and the paper does not itself claim
  clinical translation.
- **A claim that other cell lines will show the same effect.** The paper uses only
  HBRA in-vivo and in-vitro human lymphocyte X-ray parameter sets.

---

## 5. Verdict record
| Metric | Value |
|---|---|
| Tracker intake label | REPLICATED |
| Substantive audit verdict | PARTIAL |
| Coverage (fully covered / total testable) | 6/10 (48 % of 21 analyzable units) |
| Agreement on tested claims | 8/10 (80 %) |
| Below REPLICATED threshold? | Yes (80 % agreement is at threshold; 48 % coverage is well below) |
| Recommendation | Upgrade to REPLICATED only after Fornalski 2022 MC tree is reconstructed and Figs 2, 3–11 + §4 headlines are re-derived; otherwise the honest label is PARTIAL. |
