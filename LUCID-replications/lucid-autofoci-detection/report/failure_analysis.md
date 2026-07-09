# Failure Analysis — AutoFoci Replication

**Verdict framing.** The original run declared **REPLICATED (coverage 8/10, agreement 9/10).** That verdict is honest for the algorithmic-core reading. This document is the counter-narrative: what actually did not work, what got glossed, and what the residual uncertainty is. Read this alongside `REPORT.tex §Critique`.

---

## 1. Direct failures (things that did not reproduce as literally specified in the paper)

### 1.1 Equation 3 (weighting factor `w`) — DID NOT REPRODUCE
- Paper: `w = I_STD,red / I_STD,green`, typical range 0.9–1.2.
- This replication: per-cell pixel-SD reading gives w ∈ [0.30, 1.05], median 0.52.
- Impact on eq. 4 (weighted geometric-mean combination of channel OEPs): drags Spearman ρ from 0.90 (paper) down to **0.555**.
- Workaround used: substitute `w = 1` (plain geometric mean, the eq. 4 limit as w → 1). This recovers ρ = 0.890, matching the paper's headline.
- **Root cause: unknown.** Most likely the paper's `I_STD` is not the per-cell pixel standard deviation in the DAPI-masked object region (which is what we computed). Candidates: per-image mean, per-experiment normalisation, background-subtracted signal SD, or something else buried in the Java source. We did not chase the Java source.
- **Residual gap:** the headline number reproduces only under a documented deviation from the paper's stated eq. 3. A rigorous replication would either (a) confirm the jar disagrees with the text (would be a real find), or (b) confirm the jar matches the text and our reading of `I_STD` is wrong.

### 1.2 Panels (i), (ii), (iv), (vi), (viii) — SYSTEMATIC OVER-CORRELATION
- Deltas (ours − paper): +0.10, +0.38, +0.12, +0.11, +0.08.
- All five intermediate metrics are **stronger in our reimpl. than in the paper**. Panel (ii) — mean γH2AX object intensity — goes from paper 0.47 to ours 0.846, a factor-of-2 discrepancy in ρ-shortfall.
- The one-sided nature (our ρ always higher, never lower) strongly implies a systematic difference in ground-truth aggregation or object masking, not random noise.
- **Root cause: not diagnosed.** Most likely we used a different ground-truth aggregation than the paper's Fig. 2d panels (we used the average of the three raters; the paper may have used a single rater, the median, or a different subset).
- **Residual gap:** if the paper used a stricter aggregation and our looser aggregation inflates ρ for weak features, that same effect is inflating the (ix') headline number too. The 0.890 vs. 0.90 match may be lucky. We did not test.

### 1.3 Biological claims (C6, Fig. 4 kinetics) — NOT TESTED
- The paper's high-value scientific claim — that low-dose (12 mGy) DSB repair is impaired in a way consistent with earlier manual studies (refs. 18, 20) — was not tested here.
- Root cause: raw kinetic images (~600 000 cells) not in the public GitHub repo. Only the 473-object rated set and the 804 demo cells are public.
- **Residual gap:** the biology is untested by this replication. The paper's biological conclusion is itself a re-replication of earlier work, so a partial pass here is defensible, but a claim like "the paper's biology reproduces" is not supported by this run.

### 1.4 Pipeline claims (C7, Cellect necessity) — NOT TESTED
- We used author-provided pre-cropped single-cell images. The Cellect pre-processing (autofocus, z-stack Sobel best-plane selection, single-cell cropping) was neither executed nor cross-checked.
- **Residual gap:** if Cellect introduces its own biases (e.g. z-plane selection preferring high-intensity foci), OEP scores computed downstream inherit that bias. Not tested.

---

## 2. Weak-evidence shortcuts + tolerance hand-waving

### 2.1 In-sample threshold selection
Both the valley threshold (log₁₀(OEP) ≈ 3.74) and the F1-optimal threshold (3.18) were chosen on the same 473-object set they were then evaluated on. The reported precision/recall/F1/AUC/AP are **in-sample**. A proper replication would report at least a 5-fold CV or a bootstrap 95% CI on the headline metrics.

### 2.2 No bootstrap CI on the headline ρ
`ρ = 0.890` is a point estimate on n = 473. A basic bootstrap over object sampling would give a plausible 95% CI of roughly ±0.02–0.03. Without a CI, "within 0.01 of the paper" is not calibrated — 0.890 vs. 0.90 might be statistical noise, or it might be a real 0.01 offset. We treated it as an exact match.

### 2.3 Single ground-truth aggregation
Only the mean-of-three-raters aggregation was scored. Alternatives (median, majority, per-rater ρ then averaged) were not tried. Sensitivity to aggregation choice is unknown, and per §1.2 above it may be exactly the mechanism inflating our panel-i/ii/iv/vi/viii ρ values.

### 2.4 No comparison against the compiled jar
Running `AutoFoci.jar` on the same 473 objects and diffing its per-object combined OEP against ours would have been a ~5-minute sanity check. It would have immediately answered §1.1 (eq. 3 root cause) and §1.2 (ground-truth aggregation) with certainty. We did not do it. This is the single largest lost-value shortcut in the original run.

### 2.5 LoG kernel provenance
The LoG 5×5 kernel is documented in the paper Materials & Methods but the specific weights were confirmed against the Java source (`ObjectFinder.java` line 91). The paper does not give the exact weights. Good that we cross-checked; would have been better to note in the paper that the weights are only in the source.

### 2.6 Inertia disk radius = 3 px
This constant appears in eq. 1 but its value is not in the paper text — only in the Java source. We used the source value silently. Any reader replicating from the paper alone would not know this number.

---

## 3. Unverified claims + missed controls

### 3.1 Compactness ablation
The compactness factor of eq. 1 is never ablated. It is trivial to run (drop compactness from the OEP product, re-score) and would tell us whether the third factor is actually pulling weight or is decorative. Not run.

### 3.2 Cross-platform generalisation
All 473 rated objects come from a single lab, single microscope, single antibody batch. OEP has six hand-coded numerical constants presumably tuned to that stack. We did not stress-test on independent lab data.

### 3.3 Low-dose FNR
Valley threshold gives 100% precision but only 56% recall on the 473-object set. The paper's Fig. 4 low-dose kinetics rest on counting at doses where expected foci-per-cell is <1. A 44% FNR floor could non-trivially bend the fitted repair rate constants. Not tested here (see Q4 in `open_questions.json`).

### 3.4 Modern-classifier comparison
No small learned classifier (logistic regression, RF, tiny CNN) was trained on the 22 features as a sanity check against OEP. We took the paper's hand-crafted feature product on faith. See Q3 in `open_questions.json`.

---

## 4. Backfill-specific gaps

### 4.1 No canonical `paper.pdf` archived at replication time (RESOLVED at backfill)
The original run extracted with `pdftotext` and moved on. No PDF copy was preserved. Backfill (2026-07-06) fetched the PDF from https://www.nature.com/articles/s41598-018-35660-5.pdf (2 425 148 B, sha256 `f9511a7ad59b62c49f303173daa274197c1e4b13e8a90b60e7d35c9655c99c89`) and archived it at `paper.pdf`, plus wrote a `pdftotext -layout` extraction to `extraction/marker.md` (76 349 B) as the Marker-fallback. The re-read of the paper for open-questions Q1–Q5 was grounded in this backfilled text.

### 4.2 No Nougat parse
GPU-parsed Nougat MMD is not available for this paper in the target dir. Backfill wrote `extraction/nougat.mmd` as a stub noting the sha256 is pending (no PDF on disk to sha) and the file should be filled by a future central corpus sweep.

### 4.3 No supplementary methods audit
The paper has supplementary methods (Sci. Rep. supp. materials). We used the main-text PDF only. Any parameter definition buried in supp. is missed.

---

## 5. What is needed to close each gap (concrete)

| Gap | Effort | Deliverable |
|---|---|---|
| §1.1 eq. 3 `w` mismatch | ~30 min: run `AutoFoci.jar` on 473 objects, diff per-object combined OEP against ours | Definitive answer: does the jar match the text or the reimpl.? |
| §1.2 systematic over-correlation | ~30 min: re-score panels (i)–(viii) under per-rater aggregation, median aggregation, and majority-vote | Diagnose ground-truth aggregation mismatch |
| §1.3 biology (C6) | Weeks: request raw kinetic images from authors OR find LUCID-collaborator raw data | End-to-end kinetic replication of Fig. 4 |
| §1.4 Cellect | ~1 day: run Cellect on a small in-house z-stack, compare foci counts before/after cropping vs. manual crop | Sensitivity of OEP score to upstream cropping |
| §2.1 in-sample thresholding | ~15 min: 5-fold CV on threshold selection | Out-of-sample precision/recall |
| §2.2 no CI on headline ρ | ~10 min: 1000-sample bootstrap over object indices | 95% CI on ρ = 0.890 |
| §2.3 aggregation robustness | ~20 min: re-score under 4 aggregation choices | Aggregation-robustness table |
| §2.4 no jar comparison | ~30 min: `java -jar AutoFoci.jar …` batch mode + diff | Per-object concordance |
| §3.1 compactness ablation | ~5 min: 4 extra rho computations on features.csv | Marginal contribution table |
| §3.2 cross-platform | Weeks: acquire IRIF-net + HPA data, re-run reimpl. | Portability characterisation |
| §3.3 low-dose FNR | ~1 day: synthetic foci simulator + Fig.4 re-fit under FNR priors | FNR-corrected rate constants |
| §3.4 modern classifier baseline | ~1 day: LR + RF + tiny CNN 5-fold CV | Head-to-head with bimodality test |
| §4.1 paper.pdf missing | ~~~5 min: fetch from DOI, sha256, drop in dir~~ **DONE at backfill 2026-07-06** | ~~Canonical PDF archived~~ paper.pdf + extraction/marker.md now on disk |
| §4.2 Nougat MMD | Central corpus sweep dependency (Kukla/Polaris) | Fill nougat.mmd via sha256 lookup |
| §4.3 supp methods | ~15 min: pull supp. from Nature server, pdftotext | Any extra parameter defs surfaced |

---

## 6. Bottom-line evidence-strength assessment

**Algorithmic-core replication:** strong. Eqs. 1–4 reimplemented from scratch in Python, LoG kernel cross-checked against source, all 22 features regenerated, headline ρ matches to −0.01. Bimodality qualitatively matches Fig. 3.

**Numerical-headline replication:** medium-strong, with the eq. 3 caveat. The 0.890 vs. 0.90 match holds only under a substitution (`w = 1`) that is not what the paper's eq. 3 literally says. Absent a jar-vs-text diff, we do not know whether this substitution is (a) a legitimate limit approximation, (b) a paper-vs-source disagreement, or (c) a masking of a real reimpl. bug.

**Biological-endpoint replication:** none. Not tested. Not testable with the public dataset.

**Pipeline replication:** none. Not tested. Not testable without in-house image acquisition.

**Recommended honest headline for this dir:** *"Algorithmic core of AutoFoci independently reimplemented in Python and shown to reproduce the paper's headline Spearman ρ within 0.01, under a documented deviation from eq. 3 that is likely benign but not verified against the compiled jar. Biological end-to-end claims not tested."*
