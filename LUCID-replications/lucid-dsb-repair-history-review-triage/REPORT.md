# Triage Report — Berthel et al. 2019 (DSB Repair History Review)

## 1. Bibliography

- **Citation:** Berthel E., Ferlazzo M.L., Devic C., Bourguignon M., Foray N. *What Does the History of Research on the Repair of DNA Double-Strand Breaks Tell Us? — A Comprehensive Review of Human Radiosensitivity.* **Int. J. Mol. Sci.** 2019, **20**(21), 5339. DOI: [10.3390/ijms20215339](https://doi.org/10.3390/ijms20215339).
- **Article type:** Narrative / historical comprehensive **Review** (explicitly labeled "Review" in the MDPI header; Section 7 is "Conclusions"; no Methods, no Results).
- **PDF SHA1 prefix:** `58db87da741bb417f019bddf0ff1f58ff53f7e78` (2,092,179 bytes).
- **Funding:** Commissariat Général à l'Investissement (INDIRA), CNES (BERNADOTTE), INCa (PROUST).
- **Conflicts:** None declared.
- **Supplementary materials:** None mentioned anywhere in the paper.
- **References:** **77 references** (counted from the bibliography, all numbered).

## 2. Verdict

**NO-GO** — not a replication target.

| metric | value |
|---|---|
| coverage | N/A |
| agreement (/10) | N/A |
| effort to replicate the *paper's own claims* | unbounded (would require redoing 40 years of cited primary radiobiology) |
| effort to replicate the *only fitted equations* | medium, but data not supplied (see §4) |

## 3. Why NO-GO

Per the LUCID triage rubric (replicate compact quantitative models / tables / meta-analyses or else write a defensible NO-GO), this paper fails every gate for a clean replication:

1. **No tables.** A full-text scan of the PDF (`pdftotext -layout`) returns **zero matches** for a "Table N" caption. The paper has none.
2. **No original experimental data.** The article is a historical/semantic review. Every numerical claim ("xrs-5/6 have ~50% unrepaired DSB and SF2 ≈ 1%", "controls SF2 ≈ 80%", "AT incidence ≈ 1/100,000", "Group I = 75–85%, Group II = 5–20%, Group III < 1% of patients") is **cited verbatim from prior publications**; the present paper does **not** restate those underlying datasets in tabulated form.
3. **No meta-analysis.** There is no inclusion/exclusion procedure, no PRISMA flowchart, no pooled effect sizes, no forest plot, no heterogeneity statistic, no QUADAS/Newcastle-Ottawa scoring. The word "systematic" is used once in passing, not in the methodological sense.
4. **No mathematical model with parameters that can be re-fit from data the paper supplies.** The only mechanistic/mathematical content discussed (biphasic exponential DSB-repair kinetics, the "Bodgi formula", the linear-quadratic survival model, the RIANS / nucleo-shuttling hypothesis) is referenced to prior papers (refs [34–36], [50–51], [59], [71], [72]) and is **described**, not **fitted** here. Reproducing those models would mean replicating refs [36, 50, 71, 72], not this review.
5. **No survival/dose-response curves with extractable numerical axes that originate in this paper.** All curves shown in Figs. 2 and 5 are explicitly labelled as redrawn from prior references [12, 15, 16, 30].
6. **The figures that *do* carry a fitted equation are not self-contained.** See §4.

## 4. The only quantitative content — and why it is still NO-GO

Two figures carry fitted equations:

### Figure 3 — SF2 vs. % unrepaired DSB

> *"The data obey either a power function (y = 55.36 x^(−0.76); r = 0.68) or an inverse function (y = 75/(x + 0.57); r = 0.63) (dotted line)."*

with data sourced from references [12], [15], and [30] (Joubert et al. 2008; Jeggo & Kemp 1983; Ferlazzo et al. 2017). The paper **does not provide the underlying (x, y) pairs** — they exist only as scatter points in Fig. 3, with unmarked individual identities except for ATM, NBS1, and LIG4-mutated cells.

Sanity-check of the two published fits at anchor points cited elsewhere in the text:

| x = % unrepaired DSB | observed SF2 (text) | power fit | inverse fit |
|---:|---:|---:|---:|
| ~0 (radioresistant controls) | ~80 % | ∞ (singular) | **131.6 %** (impossible — SF2 is a fraction ≤ 1) |
| ~50 (xrs-5/6 mutants) | ~1 % | 2.83 % | 1.48 % |

Both fits are weak (r ≈ 0.6–0.7) and the inverse fit is non-physical at x = 0. They are visual heuristic overlays, not mechanistic models. Even a competent re-fit would require **digitising Fig. 3 by pixel** (rough OCR/WebPlotDigitizer pass), which is below the LUCID threshold for a meaningful replication and would only confirm "two arbitrary 2-parameter curves through a noisy ~25-point cloud, r ≈ 0.6". Not worth the audit cost.

### Figure 5D — linear consistency between PFGE and γH2AX

> *"the dotted line represents a linear fitting formula (y = x + 1; r = 0.99)."*

A trivial 1:1 (+1) identity check between two DSB-repair assays redrawn from refs [12] and [16]. No new data; no new model; r = 0.99 is essentially asserting the two assays agree on the anchor points, with the paper itself flagging *"the early data plots of cells with moderate radiosensitivity that are not in agreement with the linear formula"* (red arrows). This is a **discussion-level visual claim**, not something to "replicate".

### Figure-by-figure inventory

| Fig. | Type | Replicable data? |
|---|---|---|
| 1 | Schematic of HR/NHEJ pathway + clinical consequences | No (cartoon) |
| 2 | Brief history of correlations; cell-survival curves & PFGE DSB-repair kinetics & SF2 vs. unrepaired-DSB scatter, all redrawn from refs [12,15,16] | No — re-rendering of prior data, no values |
| 3 | SF2 vs. % unrepaired DSB scatter with two fits (power & inverse) | **Partially** — equations are published but underlying data are not tabulated; weak fits (§4) |
| 4 | Schematic / timeline of repair-curve interpretation models | No (schematic) |
| 5 | A/B/C/D — PFGE vs. γH2AX comparison kinetics + 1:1 linear overlay | No — redrawn from refs [12,16] |
| 6 | RIANS mechanistic cartoon | No (schematic) |

## 5. What a LUCID-compliant replication would actually require

For Fig. 3 alone:

1. Retrieve the underlying SF2 and DSB-repair values from refs [12] (Joubert et al. 2008), [15] (Jeggo & Kemp 1983), and [30] (Ferlazzo et al. 2017).
2. Reconstruct the cell-line-by-cell-line scatter (~25 points by visual count of Fig. 3).
3. Re-fit power-law and inverse models, compare to (55.36, −0.76) and (75, 0.57).

Risk: even with the underlying tables in hand, the fit quality (r ≈ 0.63–0.68) means the parameter estimates are extremely loose; a reproduction within ±20–30 % of the published coefficients would be considered "agreement" but would teach nothing scientifically meaningful. The exercise becomes a digitisation audit, not a replication.

## 6. Final scoring

- **Verdict:** **NO-GO**
- **Coverage:** N/A (review article, no compact quantitative target)
- **Agreement:** N/A
- **Confidence:** high — every replicability gate (own data / own tables / own model parameters / supplementary data / meta-analytic pooled estimates) fails on a direct read of the PDF.

## 7. Honest exhaustion of the folder

- The single target PDF in the LUCID work item (`58db87da...pdf`) was fully extracted to text (1,318 lines, 100 % of pages 1–15 plus references).
- Every "Table N" reference (regex `[Tt]able\s+\d`) returned zero hits.
- Every "Figure N" caption was inspected; only Figs. 3 and 5D carry fitted equations, both addressed above.
- Both equations were sanity-checked numerically against the paper's own qualitative anchor points (§4).
- No supplementary file is referenced.
- No replicable quantitative model, table, or meta-analysis exists in this paper.

— End of triage —

## Open Questions & Reproducibility Blockers

- **NO-GO is correct**, but the precise missing artifact is the per-cell-line **(% unrepaired DSB, SF2) scatter table** that underlies Berthel et al. 2019 Fig. 3. The paper only prints the fitted curves `y = 55.36 x^(−0.76)` (r = 0.68) and `y = 75/(x + 0.57)` (r = 0.63); the ~25 individual cell-line data points are shown only as unlabeled symbols and are referenced back to Joubert et al. 2008 [ref 12], Jeggo & Kemp 1983 [ref 15], and Ferlazzo et al. 2017 [ref 30]. No supplementary table is provided.
- Secondary missing artifact: the **PFGE-vs-γH2AX paired-assay table** behind Fig. 5D (`y = x + 1`, r = 0.99). Same situation — values exist only as plotted points redrawn from refs [12] and [16], with no machine-readable source.
- Open question: would re-pulling Joubert 2008 + Jeggo & Kemp 1983 + Ferlazzo 2017 supplementary tables (where they exist) recover enough of the underlying scatter to independently audit the two heuristic fits, especially the non-physical `inverse` fit that predicts SF2 > 100% at x = 0?
- Forward extension: this paper would be re-tractable only if treated as a meta-analysis target — pull the primary tables from refs [12], [15], [30], rebuild the (DSB%, SF2) cloud, and either confirm or replace the two-parameter fits with a mechanistic LQ-derived form.

