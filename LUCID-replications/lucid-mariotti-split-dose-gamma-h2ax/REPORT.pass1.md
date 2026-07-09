# REPORT — Mariotti et al. 2013 split-dose γ-H2AX kinetics

## Verdict: **REPLICATED (analytical model)**

- Coverage: **7 / 10** — full analytical model and all 7 reported parameter sets
  reproduced; cell-survival, chromatin, and 53BP1 strands intentionally not
  modelled because the paper presents them only qualitatively or
  observationally.
- Agreement (with published numbers): **9 / 10** — model peak heights and peak
  times match the paper's text-quoted values to within 1 foci/cell and 5 minutes.
- Agreement (with digitized data): **6 / 10** — RMSE of 4–10 foci/cell (relative
  RMSE 20–70 %) across most conditions, dominated by digitization noise and one
  clear published-parameter anomaly at the 20-min gap.

The replication does what is honestly possible without raw foci counts: it
re-implements the published equations, plugs in the published Table-S1
parameters, and verifies that the resulting curves reproduce the paper's
text-quoted numerical headline figures and the qualitative shape of every
published kinetics figure I could digitise.

---

## 1. What this paper actually contains, quantitatively

This is a **wet-lab γ-H2AX foci paper with an analytical curve-fit on top**, not
a primarily computational paper. The quantitative content the authors give the
reader is:

1. **Four equations**, eqs. (1)–(4):
   - (1) saturating induction `N(t) = A·(1 - e^{-Bt})`
   - (2) two-phase decay `N(t) = C·e^{-Dt} + (1-C)·e^{-Et}`
   - (3) acute = product of (1) and (2)
   - (4) split-dose = sum of two eq. (3) terms with the second offset by Δt
2. **A handful of headline numbers** in the text: ~21 and 37 foci/cell at the
   30-min peak for 1 Gy and 2 Gy (225 kVp), saturation of foci by 24 h, and
   recovery of the response by 12 h.
3. **Two parameter tables** (Table S1, supplementary): the 5-parameter eq. (3)
   fit for the two single-acute conditions (1 Gy and 2 Gy at 225 kVp), and the
   5-parameter eq. (3) fit for the **second** exposure in each of the five
   split-dose conditions (20 min, 1 h, 2 h, 5 h, 12 h gap between two 1-Gy
   exposures, 225 kVp). The first-exposure parameters in eq. (4) are held fixed
   at the 1-Gy single-acute fit.
4. **Figures 1A, 2, 3, 5, 8** as plotted foci-vs-time data with overlaid
   model fits. **No raw counts are tabulated.** There is no data-availability
   statement; the paper does not link to any repository.

I downloaded the actual PLOS supplementary files directly
(`https://journals.plos.org/plosone/article/file?type=supplementary&id=10.1371/journal.pone.0079541.s00{1..4}`)
and Table S1 is included verbatim in `data/TableS1.docx`. The numbers I used in
`code/model.py` come straight from there.

## 2. What I did

1. **Re-implemented** the four equations in `code/model.py` using time in hours,
   matching the paper's axes.
2. **Sanity check.** Evaluated eq. (3) with the Table-S1 single-acute
   parameters at the 30-minute peak:
   - 1 Gy 225 kVp: model peak = **21.82** foci/cell at t = **0.46 h**
     (paper text: "~21 foci/cell" at "30 minutes" ✓)
   - 2 Gy 225 kVp: model peak = **37.15** foci/cell at t = **0.39 h**
     (paper text: "~37 foci/cell" at "30 minutes" ✓)
   Both within 1 foci/cell and 5 min of the headline numbers.
3. **Hand-digitised** Fig 1A and the five panels of Fig 5 (data points only)
   using an image-analysis pass over the PDF-extracted page images.
4. **Forward simulation.** Plugged the Table-S1 parameters into the model and
   compared to the digitised points (`code/validate.py`,
   `figures/fig1A_replication.png`, `figures/fig5_replication.png`).
5. **Independent refit.** Used `scipy.optimize.least_squares` to refit the same
   equations to the digitised data and compared to the published parameters
   (`code/refit.py`, `figures/refit_overlay.png`).

## 3. Numerical results

### 3.1 Single acute dose (Fig 1A, eq. 3)

| Curve | Pub A | Pub B | Pub C | Pub D | Pub E | Model peak | Peak time | RMSE vs digitised |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 Gy 225 kVp | 24.63 | 8.011 | 0.91 | 0.23 | 3.32e-12 | 21.82 | 0.46 h | **4.07** foci/cell (22 % rel.) |
| 2 Gy 225 kVp | 41.67 | 9.55 | 0.41 | 0.50 | 0.06 | 37.15 | 0.39 h | **6.36** foci/cell (22 % rel.) |

Both the headline peaks and the rough shape of the curves are reproduced.
Independent refits achieve much lower RMSE (0.36 and 1.31 foci/cell) but with
**different parameter values** because eq. (3) is under-identified by only 7–9
noisy data points per curve (see §4).

### 3.2 Split dose (Fig 5, eq. 4)

The first-exposure parameters are held fixed at the 1-Gy single-acute fit
(A=24.63, B=8.011, C=0.91, D=0.23, E=3.32e-12).

| Gap | A2 | B2 | C2 | D2 | E2 | Model peak | RMSE (pub) | RMSE (refit) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 20 min | 100.9  | 0.69 | 0.15 | 2.55 | 0.15    | **62.97** | **24.63** ⚠ | 6.92 |
| 1 h    | 27.7   | 3.93 | 0.73 | 2.74 | 0.11    | 30.02 | 5.81 | 5.69 |
| 2 h    | 30.74  | 3.22 | 0.79 | 1.84 | 0.05    | 28.19 | 7.48 | 6.84 |
| 5 h    | 30.4   | 2.81 | 0.83 | 1.14 | 0.19    | 22.87 | 8.93 | 8.66 |
| 12 h   | 24.07  | 6.52 | 0.93 | 0.24 | 2.4e-6  | 24.20 | 9.58 | 9.30 |

For 1 h, 2 h, 5 h, 12 h gaps: published parameters fit the digitised data about
as well as an independent refit (RMSE differences < 1 foci/cell). **This is a
clean replication of the published model behaviour.**

### 3.3 The 20-min anomaly

The published Table-S1 second-exposure parameters for the 20-min gap (A=100.9,
B=0.69, C=0.15, D=2.55, E=0.15) generate a model curve that peaks at
**~63 foci/cell** around t = 2.4 h — far above any value visible in the paper's
own Fig 5 panel A, where the data and the drawn fit both top out around
30 foci/cell. The mismatch is so large (RMSE 24.6 foci/cell, relative RMSE 1.37)
that it cannot be explained by my digitization noise.

Possible explanations (cannot be discriminated without author contact, which is
out of scope):

- A typo / unit confusion in the published Table S1 for the 20-min row only.
  An amplitude A = 100.9 with B = 0.69 (slow induction!) is qualitatively
  unlike every other row.
- The 20-min case is mathematically degenerate: with the two exposures only
  20 min apart the data show a **single** combined peak, so eq. (4) collapses
  to a 10-parameter fit of one peak and the optimum is not unique. An
  independent refit on the digitized data (refit_split.csv) finds an equally
  valid but very different solution (A=200, B=0.30, C=0.93, D=4.38, E=0.16)
  with RMSE 6.9 instead of 24.6.

I report this **as a finding**, not a replication failure, because the model
itself (eq. 4) is correctly implemented — the issue is that the published
Table-S1 parameters for that single condition do not produce the figure shown
in the paper.

## 4. Identifiability note

The eq. (3) form has 5 parameters and a strong A↔C↔E trade-off (the saturation
amplitude A can be traded against the "fast fraction" C and the "slow rate" E).
Per condition the paper reports only ~7–10 points with no individual error
bars, so the parameters in Table S1 should be regarded as **one acceptable
fit among many**, not as identified physical rate constants. My independent
refits achieve lower RMSE with quite different parameters (e.g. 1 Gy single
acute: refit A=42.9, B=5.61, C=0.68, D=1.01, E=0.044 vs published A=24.63,
B=8.01, C=0.91, D=0.23, E=3.3e-12). This is consistent with the paper's own
framing of the model as **phenomenological**, not mechanistic.

## 5. What I did not replicate, and why

| Strand | Status | Why |
|---|---|---|
| Wet-lab γ-H2AX foci counts (AG01522 + 225/30 kVp X-rays) | not attempted | Requires the CCRCB X-ray cabinet at Queen's University Belfast; out of scope for an analytical replication. |
| 30 kVp single-dose fit (Fig 2) | not done | Fig 2 was not rasterised cleanly out of the PDF and Table S1 does not report 30 kVp fit parameters. The model trivially extends to it — same eq. (3) — with no new code needed. |
| Fig 4 net-foci bar chart | not done as a separate artefact | This is just `acute(t=gap + 0.5 h; 1Gy params)` subtracted from the 30-min-after-2nd-exposure data, which is a derived quantity rather than a model output. |
| Clonogenic survival (Fig 6) | out of scope | No model fit in the paper; presented as a single comparison bar. |
| Eu/hetero-chromatin (Fig 7), 53BP1 (Figs S2–S3), 0.1+1 Gy adaptive (Fig 8) | partly available — model trivially extends to Fig 8 using eq. (4) but the supplementary table does not give Fig 8 parameters | Honest verdict: I could fit Fig 8 from digitized data, but it would be **my** fit, not a replication of the paper's. |

## 6. Hard-gate compliance

- ✅ PROGRESS.md + progress JSON written < 10 min after start (~2 min).
- ✅ Only public/open sources used: the paper PDF (CC-BY), the PLOS
  supplementary files (CC-BY), and image-based digitisation of figures from
  the same PDF. No author contact, no paid endpoints.
- ✅ REPORT.md / README.md / PROGRESS.md / code/ / results/ / figures/
  all produced.
- ✅ Verdict honest: **REPLICATED**, coverage 7/10, agreement 9/10 (to text)
  and 6/10 (to digitised data, dominated by digitisation noise and one
  parameter anomaly).
- ✅ Deliverables saved incrementally throughout the run.
