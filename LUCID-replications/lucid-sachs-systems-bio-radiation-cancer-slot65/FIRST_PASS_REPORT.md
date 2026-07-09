# FIRST_PASS_REPORT — slot 65

**Paper:** Little MP, Heidenreich WF, Moolgavkar SH, Schöllnberger H, Thomas DC.
"Systems biological and mechanistic modelling of radiation-induced cancer."
*Radiat Environ Biophys* (2008) 47:39–47.  DOI 10.1007/s00411-007-0150-z.

**LUCID slot:** Wave 7 / rank 96 / backfill.

**Verdict: PARTIAL (scoping-quality replication; recommend QA retag `done-partial; scope=review-paper`)**.

---

## 1. What this paper actually is

A 9-page narrative summary of five talks at the *First International Workshop on Systems
Radiation Biology* (GSF, Neuherberg, 14–16 Feb 2007).  It is a **review/workshop overview**,
not a primary modelling paper.  Every model discussed (TSCE applied to radon-rats and
atomic-bomb survivors; generalized MVK; State-Vector Model; WECARE hierarchical logistic
regression) is published in its own dedicated primary paper.  The master TSV had
worktype = `simulation/model replication`, which is technically reasonable but ambiguous —
the paper offers no equations or parameters that, on their own, allow a numerical
replication of any specific dataset.

The closest things in the paper itself to "replication targets" are:
- **Schematic Fig. 3** — generalized MVK with *k* + *m* states (drawing only).
- **Fig. 4** — refitted SEER colon-cancer hazards under 5 model variants (figure reproduced from
  Little & Li 2007 *Carcinogenesis* 28:479; the data + fitting machinery lives in that paper).
- **Fig. 5** — CGL1 in-vitro transformation freq vs γ dose under SVM (reproduced from
  Schöllnberger et al. 2007 *Radiat Res* 168:614; full machinery lives there).
- **One numeric value:** SVM protective-bystander rate `kap = 0.054 /day` delayed plating,
  `kap = 0.022 /day` immediate plating (with 95% CIs).
- **One equation skeleton:** Thomas first-level WECARE logistic regression.

## 2. What we replicated

`code/smoke_replication.py` (numpy + matplotlib, <2 s on a laptop, no GPU, no licensed code):

1. **Two-stage MVK / TSCE closed-form hazard** (Heidenreich-Jacob-Paretzke 1997 form
   used in the Heidenreich/Moolgavkar/Little talks).  Sweep over three illustrative
   parameter triplets `(mu0, alpha-beta, mu1)` produces age-incidence curves on a
   `0–90 yr × 1e-3–2000 per 100k/yr` log axis.  Spot-checks:
   - Monotonic increase across adult ages (asserted in the script and passing).
   - Asymptotic plateau ~40 per 100k/yr at age 90 — same order of magnitude as
     observed adult SEER colon-cancer incidence (~250 per 100k at age 80 for males;
     paper Fig. 4 vertical scale 10⁻³ – 10³ per 100k/yr).
   - The 2-stage model plateaus too early relative to true SEER data; the paper itself
     reports that the 4-stage Luebeck-Moolgavkar variant gives a sharper rise.  Our
     smoke does not include that variant; it is a deliberate scoping limitation.

2. **State-Vector Model protective-bystander sketch** using the paper's numeric `kap` values.
   Two-panel figure (immediate vs delayed plating) shows direct LQ + bystander removal +
   total.  Spot-checks:
   - `T(0 Gy) = 5.0 × 10⁻⁵` (baseline matches Fig. 5 control point).
   - `T(0.010 Gy) = 3.96 × 10⁻⁵` (delayed plating) — below spontaneous, ✓ U-shape dip.
   - `T(0.500 Gy) = 9.7 × 10⁻⁵` (delayed plating) — above spontaneous, ✓ high-dose rise.
   - Minimum near ~20–50 mGy, matching the Redpath et al. 2001 / Schöllnberger 2007
     reported region of strongest protective bystander effect.

No primary data were refit; this is a **shape comparison only**.

## 3. What we did NOT do, and why

| Item | Reason |
|------|--------|
| Per-talk full replication (5 models × 5 datasets) | Each is a LUCID-slot-sized effort by itself; some are already separate slots (or covered by existing slots — e.g. friedland/friedrich/medras adjacent slots cover DSB-repair-pathway machinery related to Thomas's talk). |
| WECARE Thomas hierarchical model | Requires restricted-access individual-level data (excluded by task — no author contact, no paid access). |
| Full SEER colon-cancer refit | Out of scope for a smoke; the original Little & Li 2007 paper is the right artifact for that. |
| Author contact for code | Explicitly excluded by the task. |
| Heavy compute on CherryRd | Not needed; smoke runs in <2 s on the local machine. |

## 4. Heavy-compute job plan

**None required.**  All five primary models are CPU-bound at modest scale.
If/when LUCID later spawns per-talk full-replication slots, the heaviest of the five
(Little & Wright generalized MVK with k+m states fit to SEER colon by sex and age) is
still a Python/R job tractable on a laptop or single compute node — see notes in the
adjacent slot folders `lucid-mcmahon-2016-medras-original`, `lucid-friedrich-gldm-dsb-clustering-loops-slot63`,
`lucid-friedland-stochastic-nhej-track-slot64` for compute-target conventions.

## 5. QA retag / no-go recommendation

**Recommended retag: `done-partial`**, with sub-tags:
- `scope=review-paper` (paper is a workshop summary, not a primary model)
- `replication=qualitative-shape` (smoke confirms hazard shape + SVM U-shape)
- `defers_to=[Little-Wright-2003, Schoellnberger-2007-RR-168-614, Bernstein-WECARE-2004, Heidenreich-Luebeck-Hazelton-2002-RR-158-607]`

**Not NO-GO**: the paper IS replication-plausible — just at the per-talk granularity.
The original TSV reviewer's note "KEEP: relevant and replication-plausible" remains correct.
The replication target is real; it is simply *five* targets and not *one*.

## 6. Next actions (if Rick wants to upgrade this slot)

1. Spawn a dedicated slot for Schöllnberger et al. 2007 *Radiat Res* 168:614 (full SVM with
   actual CGL1 dose-response refit and 95% CI calculation; should overlap with the existing
   `lucid-globle-photon-cell-killing` style of work).
2. Spawn a dedicated slot for Little & Wright 2003 *Math Biosci* 183:111 (full generalized
   MVK with multi-stage destabilization, fit to SEER colon by sex via NumPy + maximum-likelihood
   on a Poisson-process likelihood).
3. Mark Bernstein/WECARE hierarchical-Bayesian model **NO-GO for replication** in LUCID —
   the data are not publicly available.

## 7. Files

- README.md, PROGRESS.md, ARTIFACT_MANIFEST.md, FIRST_PASS_REPORT.md (this file)
- artifacts/paper.pdf, artifacts/paper.txt
- code/smoke_replication.py
- reports/smoke_run.txt, reports/mvk_hazard.png, reports/svm_bystander.png
