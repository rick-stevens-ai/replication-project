# NO-GO Report — Mullenders et al. 1988, NAR 16(22):10607–10622

## Verdict
**NO-GO** — No computational replication target.
- Coverage: N/A
- Agreement: N/A

## Why
The paper is a 1988 wet-lab study (UV irradiation of human fibroblasts,
³H/¹⁴C dual-label pulse, 2 M NaCl or LIS nuclear-matrix extraction, DNase I
digestion, neutral sucrose gradient, scintillation counting, plus
autoradiographic grain counting and a Southern blot for ADA). It reports:

- 5 small scatter/histogram figures with eyeballed trend lines, no error bars, no fits, no equations, no rate constants.
- ~5 fold-enrichment numbers in the prose (1.5×, 1.7×, >3×, ~0.5×, plus 15–20× replication-comparison reference, plus autoradiographic grain % values 18.1 / 34.1 / 32.5 / 23.6 / 18.7 and Southern lane shares 17.5/82.5 and 10/90).
- Zero tables.
- Zero supplementary data, zero machine-readable artifacts.
- Zero algorithms, zero statistical tests with p-values.

There is **no model, no parameter, no algorithm, and no dataset to re-run**.
The "computational" maximum possible here is digitizing Figs 1/2/4 in
WebPlotDigitizer and re-eyeballing the same fold-enrichments the authors
themselves eyeballed from those plots — which is a circular re-derivation,
not a replication.

## What was inspected
- 16-page PDF rendered to PNG at 150 dpi, pages 6–11 (figure pages) visually inspected.
- Full text extracted via `pdftotext -layout` → `source.txt` (734 lines).
- Citation, abstract, methods, results, discussion, figures and legends all reviewed.
- Confirmed no tables and no fitted parameters anywhere in the body.

## Author-stated key numbers (for the record)
- 30 J/m², 5–10 min pulse: matrix:loop label enrichment 1.3–1.6× (summarized as 1.5× in Discussion).
- 5 J/m², 2 h label: enrichment 1.7× (normal), 1.7× (XP-D), >3× (XP-C); CS shows ~2× depletion at matrix.
- Replication-incorporation reference: 15–20× matrix enrichment.
- Grain % at matrix (autoradiography): baseline 18.1%, 5 J/m² 6-min pulse 34.1%, 5 J/m² 10-min pulse 32.5%, 30 J/m² 10-min pulse 23.6%, 30 J/m² 120-min pulse 18.7%.
- ADA Southern: matrix DNA fraction 17.5% (10 µg/ml DNase I), 10% (12 µg/ml DNase I).

## Optional SPOT-CHECK (not executed)
If a re-analysis artifact is ever required, the only meaningful exercise is:
1. Digitize Fig. 4 (~25 points across normal/XP-D/XP-C/CS).
2. Compute ratio of mean (³H/¹⁴C) in low-%-matrix bins vs high-%-matrix bins per cell type.
3. Compare to 1.7× / 1.7× / >3× / ~0.5×, ±20% tolerance.
Expected outcome: pass by construction. Scientific value: negligible.

## Gates
- ≤10-min PROGRESS write: ✅
- Final verdict (REPLICATED/PARTIAL/SPOT-CHECK/NO-GO/BLOCKED): NO-GO ✅
- Coverage/Agreement: N/A (consistent with NO-GO)
- No author contact: ✅
- No paid endpoints: ✅

## Open Questions & Reproducibility Blockers

- **Exact missing artifact (NO-GO root cause):** The paper provides no machine-readable supplementary data, no source tables, no algorithm/code, and no fitted parameters — only eyeballed scatter/histogram figures (Figs 1–5) with summary fold-enrichments stated in prose. Specifically missing: per-fraction (³H/¹⁴C) ratio tables underlying Fig 2 and Fig 4 (the matrix-vs-loop scatter plots) and the raw scintillation counts for the 30 J/m² and 5 J/m² conditions. Without these, no quantitative re-derivation is possible beyond circular WebPlotDigitizer re-eyeballing of the very plots the authors eyeballed.
- **No supplementary materials / no archived raw counts:** No NAR supplement, no PRIDE/GEO-equivalent deposit (1988 predates such norms), no contact for surviving authors' lab notebooks.
- **Forward open question 1:** Do the qualitative fold-enrichments (1.7× normal, 1.7× XP-D, >3× XP-C, ~0.5× CS at matrix for 5 J/m² 2 h pulse) hold under modern matrix-prep protocols (e.g., low-salt LIS extraction with CSK pre-extraction)? A modern wet-lab re-do would be the only meaningful test of the paper's biology, not a computational replication.
- **Forward open question 2:** Could a digitization-based meta-analysis combine Figs 2/4 here with subsequent matrix-attachment NER studies (1990s–2000s) to test whether the matrix-enrichment-of-NER claim survives modern repair-foci imaging (γH2AX, XPC-GFP) — i.e., is this a real biology effect or a fractionation artifact? Outside scope of this replication target.
