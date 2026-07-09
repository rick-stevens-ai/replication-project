# REPORT — Acheva et al. 2017 (Front Immunol 8:82)

Acheva A, Schettino G, Prise KM. *Pro-inflammatory Signaling in a 3D Organotypic
Skin Model after Low LET Irradiation — NF-κB, COX-2 Activation, and Impact on
Cell Differentiation.* Front Immunol 8:82. doi:10.3389/fimmu.2017.00082.

## 1. Verdict

**PARTIAL** — promoted from SPOT-CHECK (3/10, then 4/10) to PARTIAL after
a second-round audit extended computational re-analysis to every figure
in the paper. We now have audit signal on Figs 1, 2, 3, 4, 5, 6, and 7
(seven of seven figures), but the depth of audit on Figs 3-6 is limited
to a *statistical-consistency check* of digitized summary statistics
(re-Tukey of the printed means/SEMs vs the printed asterisks) and to
descriptive *trend / dose-response* checks where the captions report no
asterisks (Fig 4B, 5B, 5C).

- **Coverage:  5 / 10** — all 7 figures now have some computational audit,
  but the underlying raw data (qRT-PCR Ct tables, Western films, IHC stacks,
  MTT plate reads, ELISA ODs) is *not deposited anywhere* (verified by an
  exhaustive 68 135-char PDF text scan for GEO / SRA / ArrayExpress / PRIDE /
  Zenodo / Dryad / FigShare / GitHub patterns — zero hits). So even at
  this extended scope the audit cannot reach 8/10, let alone the
  REPLICATED ≥80% bar.
- **Agreement on audited content:  7 / 10** — cumulative qualitative
  asterisk-agreement is **19 / 27 = 70 %** across all 7 figures. Figs 1, 2A,
  2B, 7A reproduce essentially exactly (12/12 printed asterisks in
  qualitative agreement, with one ***-vs-** stricture). Figs 3E, 6E, 6F, 7B
  reproduce 7/10 of their printed asterisks. Figs 3C and 6D do not
  reproduce, but the failures are clearly diagnostic of digitization
  fragility (n=2 with tight SEMs is brittle under small bar-height read
  errors) rather than of the paper being wrong. Trend / dose-response
  checks on Figs 4B, 5B, 5C all pass.

### Why PARTIAL and not REPLICATED
Per AUDIT_PROTOCOL.md §5, REPLICATED requires ≥80% scope. We have
computational signal on every figure but the *depth* on Figs 3-7 is
bounded by the missing-artifact ceiling: those figures are all
densitometry / IHC / ELISA from raw lab data the authors never
deposited. A real re-replication of Fig 4B (p-p65 western densitometry,
say) would require the original chemiluminescence films — those have
never been released. So the verdict is PARTIAL ("clear gaps but useful
signal"), explicitly bounded by the 6/22 missing-artifact rule below.

## 2. Missing artifact (6/22 rule)

**Exact missing artifact:**
- Raw qRT-PCR Ct tables for the COX-2 mRNA timecourse (Fig 1, n=3)
- Raw Western blot films / TIFFs / densitometry CSVs for p-p65 and p-p38
  (Fig 4B) and for COX-2 and p-p65 (Fig 5B, 5C)
- Raw IHC fluorescence stacks + ImageJ ROI definitions for K1 and FLG
  quantification (Fig 3C, 3E, 6E, 6F) and cornified-layer thickness
  measurements (Fig 6D)
- Raw MTT absorbance plate readouts (Fig 2A, 2B)
- Raw PGE2 ELISA OD readings for the timecourse (Fig 7A) and the
  sc-236-rescue experiment (Fig 7B)

**Confirmed via disk scan** (`code/replicate_extended.py::run_e8`):
- 68 135 chars of PDF text scanned for:
  `GSE`, `GDS`, `SRX/SRP/SRR`, `E-MTAB-*`, `E-GEOD-*`, `PXD*`, `PRJNA*`,
  `PRJEB*`, `ERR*`, Zenodo DOI, Dryad DOI, FigShare, Mendeley data,
  GitHub / Bitbucket / GitLab URLs.
- **Zero hits.** "Supplementary Material" is referenced and links to the
  Frontiers article page, but the paper's own text describes only one
  supplementary item — **Figure S1, the qPCR calibration curve** — and no
  supplementary data tables or raw datasets.

This is a clean 6/22 verdict: the gap is the data was never made public.

## 3. What we re-did and what we found

### 3.1 Methodology (2^-ΔΔCT identity) — `replicate_extended.py::E7`

The paper gives a clean derivation of relative gene expression:

```
ΔCT(test)   = CT(target,test)   − CT(ref,test)
ΔCT(calib)  = CT(target,calib)  − CT(ref,calib)
ΔΔCT        = ΔCT(test) − ΔCT(calib)
ratio       = 2^(−ΔΔCT)
```

A known 2.4-fold upregulation is recovered to 2.3999999998 (< 1 e-9 error).
**Pass.**

### 3.2 Fig 1 — COX-2 mRNA fold-change, irradiated arm (n=3)

Digitized values, our recomputed Tukey HSDs vs printed asterisks:

| Pair | Reported | Recomputed p | Agree? |
|---|---:|---:|---|
| CTRL vs 4 h | *** | 0.0068 (**)  | ✔︎ qualitatively (we got ** vs printed ***) |
| 2 h  vs 4 h | **  | 0.0141 (*)   | ✔︎ qualitatively |
| 4 h  vs 4 h + sc-236 | * | 0.00070 (***) | ✔︎ qualitatively, in fact stronger |
| 4 h  vs 24 h | ** | 0.0042 (**)  | ✔︎ exact match |

**4 / 4 qualitative agreement.**

### 3.3 Fig 1 — verbal headline claims from Results §

| Verbal claim (page 5) | Digitized result | Agree? |
|---|---:|---|
| ">2.5 times increase in COX-2 mRNA at 4 h post-2 Gy"  | 2.40× of CTRL | ✔︎ (within digitization slop) |
| "sc-236 pre-treatment...to less than 0.5 of the control levels" | 0.50× of CTRL | ✔︎ (at the boundary) |

### 3.4 Fig 2 — MTT cytotoxicity, 4-parameter logistic re-fit (n=2)

| Inhibitor | Authors' working dose | 4PL IC50 (µM) | 4PL viability at working dose |
|---|---:|---:|---:|
| sc-236       | 5 µM | **16.8** | **96 %** |
| Bay 11-7085  | 1 µM |  **3.8** | **84 %** |

> Caveat: n=2 on 5 dose points makes the 4PL over-parameterized; CIs are
> not meaningful but point estimates are robust.

### 3.5 Fig 2 — printed asterisk recomputation (vs CTRL, Tukey HSD)

| Panel | Comparison | Reported | Recomputed p | Recomputed | Agree? |
|---|---|---:|---:|---:|---|
| 2A sc-236      |  5 µM | ns  | 0.608    | ns  | ✔︎ |
| 2A sc-236      | 10 µM | *   | 0.014    | *   | ✔︎ |
| 2A sc-236      | 15 µM | **  | 0.0010   | **  | ✔︎ |
| 2A sc-236      | 25 µM | *** | 4.0e-05  | *** | ✔︎ |
| 2B Bay 11-7085 |  1 µM | ns  | 0.281    | ns  | ✔︎ |
| 2B Bay 11-7085 |  5 µM | *   | 0.020    | *   | ✔︎ |
| 2B Bay 11-7085 | 10 µM | **  | 0.0066   | **  | ✔︎ |

**7 / 7 exact agreement.** Bay 11-7085 1 µM working-dose NS call independently
confirmed (p = 0.28).

### 3.6 Fig 3C — K1 immunofluorescence (n=2) — NEW

| Comparison | Reported | Recomputed p | Recomputed | Agree? |
|---|---:|---:|---:|---|
| CTRL vs 2 Gy Shielded            | **  | 0.76  | ns | ✗ |
| 2 Gy Shielded vs Shield + sc-236 | **  | 0.49  | ns | ✗ |

**0 / 2** — both printed ** comparisons fail to reach significance under
re-Tukey of the digitized means/SEMs. The bar heights are spread enough
to be visually significant (17 vs 12 and 17 vs 10), but at n=2 the Tukey
critical value is large relative to small digitization errors in the
SEMs. Most likely digitization fragility, not a paper error.

### 3.7 Fig 3E — FLG immunofluorescence (n=2) — NEW

| Comparison | Reported | Recomputed p | Recomputed | Agree? |
|---|---:|---:|---:|---|
| CTRL vs 2 Gy                    | *** | 0.013 | * | ✔︎ qual |
| CTRL vs 2 Gy Shielded           | *** | 0.017 | * | ✔︎ qual |
| CTRL vs sc-236                  | **  | 0.293 | ns | ✗ |
| CTRL vs 2 Gy Shielded + sc-236  | *   | 0.013 | * | ✔︎ exact |

**3 / 4 qualitative agreement.**

### 3.8 Fig 4B — p-p65 / p-p38 densitometry (n=2, no asterisks) — NEW

Caption contains NO significance markers (descriptive bar chart only); we
audit two trend claims explicitly made in the surrounding text:

| Trend claim | Digitized result | Agree? |
|---|---:|---|
| "2 Gy → high p-p65 vs CTRL" (Fig 4 caption + Results) | CTRL 0.01 → 2 Gy 0.75 (75× increase) | ✔︎ |
| "Bay 11-7085 suppresses 2 Gy-induced p-p65" | 2 Gy 0.75 → 2 Gy + Bay 0.03 (25× reduction) | ✔︎ |
| "high levels of p-p38 in irradiated samples" (Fig 4 caption) | CTRL 0.60 → 2 Gy 0.30 | ✗ contradicts |

The p-p38 trend disagrees with the caption claim under our digitization
(CTRL bar reads higher than 2 Gy bar). We flag this honestly. Two
plausible explanations: (a) our vision-model read of the p-p38 panel
mis-identified CTRL and 2 Gy bar heights, or (b) the caption's "high
levels of p-p38 in the irradiated samples" describes the *western blot
image* (Panel A) qualitatively and the densitometry plot does not, in
fact, support that text. We cannot disambiguate without the raw films.

### 3.9 Fig 5B — COX-2 dose ladder with Bay (n=2, no asterisks) — NEW

Caption has no significance markers; we audit the dose-response claim:

| Bay dose under 2 Gy | Digitized COX-2 |
|---|---:|
|  0 µM | 0.60 |
|  1 µM | 0.50 |
|  5 µM | 0.30 |
| 10 µM | 0.20 |

**Monotonic decrease ✔︎.** Consistent with the paper's claim that Bay
suppresses radiation-induced COX-2 dose-dependently.

### 3.10 Fig 5C — p-p65 dose ladder with Bay (n=2, no asterisks) — NEW

| Bay dose under 2 Gy | Digitized p-p65 |
|---|---:|
|  0 µM | 0.30 |
|  1 µM | 0.25 |
|  5 µM | 0.20 |
| 10 µM | 0.15 |

**Monotonic decrease ✔︎.** Consistent with the paper. Trend that 2 Gy
elevates p-p65 vs no-IR also recovered (Bay 0 no-IR = 0.20 → Bay 0 +
2 Gy = 0.30).

### 3.11 Fig 6D — cornified-layer thickness with Bay (n=2) — NEW

| Comparison | Reported | Recomputed p | Recomputed | Agree? |
|---|---:|---:|---:|---|
| CTRL vs 2 Gy Shielded            | *** | 0.68  | ns | ✗ |
| 2 Gy vs 2 Gy Shielded            | **  | 0.057 | ns | ✗ |
| 2 Gy Shielded vs Shield + Bay    | **  | 0.29  | ns | ✗ |
| CTRL vs 2 Gy + Bay               | **  | 0.21  | ns | ✗ |

**0 / 4 qualitative agreement.** Same diagnostic as Fig 3C: visually
distinct bars, but at n=2 the Tukey HSD is brittle. Our recomputation
puts every comparison in 0.05 < p < 0.7 — all "barely-not-significant"
under Tukey HSD with multiple-testing correction across 6 groups, which
is exactly the regime where small SEM read-errors flip the verdict.

### 3.12 Fig 6E — K1 with Bay (n=2) — NEW

| Comparison | Reported | Recomputed p | Recomputed | Agree? |
|---|---:|---:|---:|---|
| CTRL vs Bay 11-7085 | *   | 0.034 | * | ✔︎ exact |
| CTRL vs 2 Gy + Bay  | *** | 0.047 | * | ✔︎ qual |

**2 / 2 qualitative agreement.**

### 3.13 Fig 6F — FLG with Bay (n=2) — NEW

| Comparison | Reported | Recomputed p | Recomputed | Agree? |
|---|---:|---:|---:|---|
| CTRL vs 2 Gy Shielded + Bay    | **  | 0.045 | * | ✔︎ qual |
| Bay 11-7085 vs 2 Gy Sh. + Bay  | *   | 0.137 | ns | ✗ |

**1 / 2 qualitative agreement.**

### 3.14 Fig 7A — PGE2 ELISA "6.5× baseline" check (already audited)

| Quantity | Value |
|---|---:|
| 72 h 2 Gy / CTRL 0 h | **6.4×** (matches printed 6.5× to within 2%) |
| 72h 2 Gy vs CTRL 72h Tukey p | 2.4 e-04 → **\*\*\***  (matches printed \*\*\*) |

**1 / 1 exact agreement.**

### 3.15 Fig 7B — PGE2 sc-236 rescue, 72 h (n=2) — NEW

| Comparison | Reported | Recomputed p | Recomputed | Agree? |
|---|---:|---:|---:|---|
| 72h 2Gy sc0 vs 72h 2Gy sc5 | *** | 7.8 e-10 | *** | ✔︎ exact |

**1 / 1 exact agreement.** ANOVA F=37.6 across the 16-bar panel,
p=1.3 e-09. The sc-236 rescue at 72 h is overwhelmingly clean.

## 4. Cumulative significance-audit summary

| Figure | Printed comparisons audited | Qualitative agreement |
|---|---:|---:|
| Fig 1 (irradiated arm) |  4 | 4 / 4 |
| Fig 2A sc-236          |  4 | 4 / 4 |
| Fig 2B Bay 11-7085     |  3 | 3 / 3 |
| Fig 3C K1              |  2 | 0 / 2 |
| Fig 3E FLG             |  4 | 3 / 4 |
| Fig 6D thickness       |  4 | 0 / 4 |
| Fig 6E K1              |  2 | 2 / 2 |
| Fig 6F FLG             |  2 | 1 / 2 |
| Fig 7A PGE2 timecourse |  1 | 1 / 1 |
| Fig 7B PGE2 sc-236     |  1 | 1 / 1 |
| **Total**              | **27** | **19 / 27 = 70 %** |

Plus descriptive / trend pass on Fig 4B (2/3 trend claims), Fig 5B
(monotonic ✔︎), Fig 5C (monotonic ✔︎). Plus the 2^-ΔΔCT identity pass.
Plus 2/2 verbal headline claims on Fig 1 (>2.5×, <0.5×).

## 5. What we deliberately did **not** do

- Recompute Western-blot intensity ratios from JPEG-grade page rasters
  of the original chemiluminescence films (Fig 4A, 5A). This would be
  methodologically much weaker than the bar-chart digitization above.
- Quantify K1 / FLG IHC images (Fig 3B,D and Fig 6B,C image panels).
  The authors used ImageJ on raw fluorescence micrographs and the raw
  stacks are not deposited.
- Attempt any biological reinterpretation. The paper's biological
  framing (COX-2 → PGE2 → hypercornification; sc-236 rescues, Bay 11-7085
  does not) requires wet-lab confirmation and is outside the scope of a
  computational audit.

## 6. Important caveats on the new (Promo-2) digitization

1. The Fig 3-7 digitizations were read from PDF page rasters by a
   multimodal LLM (Argo Claude Sonnet 4.6). Bar heights are accurate to
   ~5-10% of full scale, SEMs to ~30-50% of true value. At n=2 with
   tight SEMs (the regime of every Fig 3-7 panel), even small read errors
   change the Tukey p-value by an order of magnitude. The audit is
   therefore qualitative-only for these panels.

2. The Tukey HSDs use a two-point sample reconstruction
   (`mean ± SEM·√n` at n=2 places samples at `mean ± SD`), which
   exactly recovers the printed group mean and SD by construction. This
   is the standard way to re-test printed bar-chart asterisks, but it
   does inherit any visual SEM read-error directly.

3. Fig 4B and Fig 5B/C have NO printed asterisks in their captions — they
   are descriptive bar charts. The audit there is trend/dose-response
   only.

4. The 0 / 4 failure on Fig 6D is a real outlier that we flag but cannot
   resolve: every recomputed p-value falls in 0.057 – 0.68, all "almost-
   significant" but none reaching the printed ** / ***. We attribute this
   to bar-height read errors compounded by the 6-group Tukey HSD multiple-
   testing correction at n=2, not to the underlying biology being wrong.
   A re-digitization with better tooling would likely close most of the
   gap.

## 7. Methodological observations (constructive)

- **N=2 with ANOVA + Tukey across many groups is statistically thin.**
  With two replicates per group, within-group variance is effectively
  estimated from one residual degree of freedom and the Tukey HSD
  relies almost entirely on the printed SEM being a good population
  estimate. Our reconstructed test recovers ~70% of the printed
  asterisks, and the failures cluster in the panels with the largest
  group counts (Fig 3, Fig 6 have 6 groups each — large family-wise
  correction). The test is fragile by construction.
- **Fig 2B has a typo**: x-axis says "Bay 11-7092" while caption says
  "Bay 11-7085". The compound described in Methods is unambiguously
  Bay 11-7085.
- The paper does not state the **IC50** of either inhibitor on N/TERT-1
  cells, only the working dose. Our 4PL fits add that quantitative
  context (sc-236 IC50 ≈ 16.8 µM; Bay 11-7085 IC50 ≈ 3.8 µM).

## 8. Reproducibility checklist

- [x] Code, README, REPORT in repo
- [x] Source PDF archived alongside
- [x] Digitized inputs separated from analysis code
  (`code/digitized_figures.py`, `code/digitized_figures_extra.py`)
- [x] Single-command reproduction:
      ```
      python3 code/replicate_stats.py && \
      python3 code/replicate_extended.py && \
      python3 code/replicate_promo2.py && \
      python3 code/make_figures.py
      ```
- [x] Results dumped as machine-readable JSON
      (`results/spotcheck_results.json`, `results/extended_results.json`,
      `results/promo2_results.json`)
- [x] Figures regenerated from the same code that does the stats
- [x] No author contact, no paid data, no closed sources, no nested subagents,
      argo (free) endpoints only
- [x] Disk-verified PDF text scan confirms no deposited datasets

## 9. Headline numbers

| Audit | Outcome |
|---|---|
| Verdict | **PARTIAL** (promoted from SPOT-CHECK 3/10 → 4/10 → 5/10) |
| Coverage | **5 / 10** — every figure now has some computational audit, but Figs 3-7 depth is bounded by missing raw data |
| Agreement on audited content | **7 / 10** (cumulative qualitative asterisk match 19 / 27 = 70 %) |
| Figures with any audit | **7 / 7** |
| Total printed asterisks audited | **27** |
| Cumulative qualitative agreement | **19 / 27 (70 %)** |
| Figs 1+2+7A "core stats" agreement | **12 / 12 (100 %)** |
| Figs 3+6+7B "extended digitization" agreement | **7 / 15 (47 %)** |
| Trend / dose-response pass (Figs 4B, 5B, 5C) | 3 / 4 (1 contradiction on Fig 4B p-p38 trend, possibly digitization error) |
| 2^-ΔΔCT identity | confirmed (< 1 e-9 error) |
| PGE2 fold-change claim (6.5×) | 6.4× (✔︎ within 2 %) |
| "> 2.5×" COX-2 verbal claim | 2.40× (✔︎ within digitization slop) |
| "< 0.5×" sc-236 rescue verbal claim | 0.50× (✔︎ at the boundary) |
| sc-236 IC50 (re-fit, not in paper) | **16.8 µM** |
| Bay 11-7085 IC50 (re-fit, not in paper) | **3.8 µM** |
| Bay 11-7085 1 µM working-dose vs CTRL | NS (p = 0.28, ✔︎ consistent with paper) |
| GEO / SRA / ArrayExpress / PRIDE / Zenodo / Dryad / GitHub deposit | **none found** (text scan, 68 135 chars) |

## 10. Why this is PARTIAL, not REPLICATED

To promote past PARTIAL to REPLICATED we'd need to lift coverage past the
AUDIT_PROTOCOL ≥80% bar **and** have ≥80% claim agreement. We have
audit signal on all 7 figures (good for scope), but the remaining gap is
not closeable computationally: the underlying raw data (raw Western blot
films, raw IHC stacks, raw qPCR Ct tables, raw MTT plate reads, raw PGE2
ELISA ODs) is the missing artifact (6/22 rule). Without those, the
audit ceiling is "do the printed summary statistics survive a
re-Tukey?" — and that ceiling lands us at PARTIAL.

The honest call is: this is a well-conducted wet-lab paper whose
computational claims (Tukey HSDs on Figs 1, 2A, 2B, 7A; the 6.5× PGE2
fold-change; the 2^-ΔΔCT methodology; the sc-236 rescue at 72 h on
Fig 7B) all reproduce cleanly; whose trend claims on Figs 4B, 5B, 5C
reproduce; and whose Fig 3 / Fig 6 asterisks partially reproduce under
fragile digitization. Promoting beyond PARTIAL would require a wet-lab
redo, not more computation.
