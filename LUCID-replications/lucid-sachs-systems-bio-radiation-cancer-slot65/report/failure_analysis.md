# Failure Analysis — Honest Gaps in This Replication

**Slot:** `lucid-sachs-systems-bio-radiation-cancer-slot65`
**Paper:** Little MP, Heidenreich WF, Moolgavkar SH, Schöllnberger H, Thomas DC (2008), *Radiat Environ Biophys* 47:39–47
**Verdict:** PARTIAL

This document lists what this audit **did not** establish and why, in the spirit of Rick's 2026-07-05 hard rule requiring genuine critique.

---

## 1. Slot-Name Mismatch (Meta-Failure)

The queue slug `lucid-sachs-systems-bio-radiation-cancer-slot65` names **Sachs**, but the paper actually delivered and audited is by **Little, Heidenreich, Moolgavkar, Schöllnberger, and Thomas**. Rainer K. Sachs (Berkeley) is famous for two-track / dual-radiation-action / TE-CE cancer-induction models — none of which appear in the audited paper.

**Impact.** If the LUCID queue intended a Sachs paper (e.g. Sachs et al. TE-CE dose-response modelling), that paper was never audited. The paper on disk is a different paper by different authors on adjacent-but-distinct topics.

**Not fixed by this backfill.** Backfill preserves substance. If the queue wants a real Sachs slot, spawn one separately.

---

## 2. What Was Done vs the Paper's Actual Headline

### Done (equation-level surface)

- **Two-stage MVK / TSCE closed-form hazard** (Talks 1–3 implicit form): re-implemented from Heidenreich-Jacob-Paretzke 1997; analytic plateau vs numerical hazard at t=200 yr agrees to relative error **1.4 × 10⁻⁹**. This is a genuine equation-level replication.
- **SVM bystander skeleton** (Talk 4): analytic `T(D, k_ap)` re-implementation reproduces the paper's U-shape and delayed-vs-immediate `k_ap` ordering (0.054/d vs 0.022/d). But the parameter values were **used**, not **re-fit** from Redpath 2001 CGL1 raw data.
- **Thomas/WECARE first-level logit** (Talk 5): Newton–Raphson MLE on synthetic case-control (n=8000) recovers seeded (−3.0, 1.6, 0.9) as (−3.055, 1.677, 0.914). This validates **equation form only** — not the WECARE result itself.

### NOT Done (the paper's scientific weight)

#### Failure Mode A: ODE / analytical models were not independently integrated from primary microdata

- The SVM `k_ap = 0.054/d` (delayed) and `0.022/d` (immediate) were **quoted, not re-derived**. Doing so requires the Redpath 2001 CGL1 per-dose per-replicate raw data + the Schöllnberger Salzburg-group SVM solver. Neither is publicly archived.
- Our SVM smoke demonstrates that the paper's *quoted numbers* produce the paper's *claimed U-shape*. It does **not** demonstrate that those numbers themselves are the maximum-likelihood fit.

#### Failure Mode B: Epidemiological cohort fits were not reproduced

None of the paper's four data figures were re-fit from primary microdata:
- Heidenreich rat-radon ERR (Fig 1) — requires radon-exposed rat cohort microdata
- Heidenreich JANUS mouse lung-cancer (Fig 2) — internal ANL/GSF dataset
- Little & Li 2007 SEER colon model-comparison (Fig 4) — SEER*Stat gated + never-released fitting code
- Schöllnberger CGL1 dose-response (Fig 5) — Redpath 2001 raw data, not archived

**The single largest gap:** the paper's most informative quantitative claim — the SEER-colon model comparison (2-stage best; 4-stage acceptable; 5-stage significantly worse at P<0.01) — was not tested at all. This is claim C6 in REPORT.md and it is DATA-BLOCKED.

#### Failure Mode C: ERR / EAR predictions vs epidemiological data were not benchmarked

- No BEIR-VII 2006 Table 12D-1 comparison
- No UNSCEAR 2020 Annex B comparison
- No A-bomb LSS (Preston 2007; Grant 2017) comparison
- No INWORKS (Richardson 2015, 2023) comparison

The paper's implicit claim that MVK/TSCE-family models qualitatively track observed ERR patterns vs age-at-exposure and time-since-exposure is neither confirmed nor contradicted by this audit. This is captured as Open Question Q3 in `open_questions.json`.

#### Failure Mode D: WECARE result itself is untested

The C5 logit recovery uses **synthetic data seeded by us**. It proves:
- The equation is well-posed
- Newton–Raphson converges
- Coefficients recover within ≤4% relative error

It does **not** prove:
- That Bernstein et al.'s ATM/BRCA × radiation-dose coefficients on real WECARE data reproduce
- That the WECARE hierarchical second-level model works

WECARE microdata is permanent NO-GO under LUCID's IRB-cleared / no-consortium-DAC-contact protocol.

---

## 3. Verdict Sensitivity Analysis

| Definition of "headline" | Implied verdict |
|--------------------------|-----------------|
| The paper's own explicit equations (3 present) | REPLICATED (3/3 machine precision) |
| The paper's numerical claims about the world (best-fit stage counts, `k_ap` CIs, Thorotrast distribution, ERR curves) | SPOT-CHECK (mostly untested; 1 SPOT-CHECK entry) |
| Combined equation + data-level (weighted by claim count) | PARTIAL (4/8 verified equation-level; 4/8 data-blocked or spot-check) |

**PARTIAL is the honest midpoint** and matches the on-disk `REPORT.md`. The queue brief noted that "if the paper is purely analytical/review-of-systems-biology (no MC + no wet-lab), a legitimate PARTIAL→REPLICATED upgrade is allowed IF the report substantiates full headline recovery." This paper's headlines live in the primary papers it summarizes, NOT in its own body. Therefore **PARTIAL is retained**.

---

## 4. Named Missing Artifacts (Consolidated)

These are the exact artifacts whose absence blocks REPLICATED:

1. **SEER colon-cancer per-age incidence by sex, 1973–2002** — SEER*Stat registration gated
2. **Little & Wright 2003 generalized-MVK fitter** (k+m stage, Poisson-likelihood) — never released
3. **Little & Li 2007 model-comparison harness** — never released
4. **JANUS lung-cancer per-mouse follow-up** — internal ANL/GSF
5. **Heidenreich-Luebeck-Hazelton 2002 Thorotrast posterior** (μ₀, N, α, β, μ₁) — not machine-readable
6. **Redpath 2001 CGL1 transformation raw data** — not archived
7. **WECARE de-identified genotype+dose+case microdata** — consortium DAC / IRB
8. **Schöllnberger Salzburg-group SVM solver source** — not archived

---

## 5. Contradictions Found

**None.** Every claim we could test agrees with the paper at machine precision (C2 to 1.4 × 10⁻⁹) or within MLE tolerance (C5 ≤4%). C3 monotonicity and C4 ordering both hold. No discrepancies were logged in `reports/claim_audit.json`.

The PARTIAL verdict is driven by **scope** (data-blocked dataset-level claims), not by **disagreement** at the equations we could reach.

---

## 6. Lessons for Future LUCID Slots

- **Workshop-summary papers are structurally harder to audit than primary papers.** A 5-talk summary defers all real machinery to 5 different primary papers. Auditing the summary faithfully means either (a) auditing only the summary's own equation surface (thin) or (b) auditing all 5 primary papers (5x the work).
- **PARTIAL is often the correct verdict for review papers**, not a failure mode. Coverage 5/10 + Agreement 9/10 is a defensible outcome when the paper's own testable surface is small and its data-figure headlines live in inaccessible primary datasets.
- **Slot-slug mismatches should be flagged aggressively.** The queue tagged this slot "sachs" but the paper is by Little et al. Silent auditing of the wrong paper would corrupt the LUCID meta-database.
