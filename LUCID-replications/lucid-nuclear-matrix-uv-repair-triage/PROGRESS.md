# LUCID triage — nuclear-matrix UV repair (Mullenders 1988)

## Target
- File: `/Users/stevens/Dropbox/XFER/LUCID-replication-targets/836900dabbab0a772f50988ffcc98745c86f10f1.pdf`
- Confirmed citation (from page 1 of PDF):
  Mullenders L.H.F., van Kesteren van Leeuwen A.C., van Zeeland A.A.,
  Natarajan A.T. (1988). "Nuclear matrix associated DNA is preferentially
  repaired in normal human fibroblasts, exposed to a low dose of
  ultraviolet light but not in Cockayne's syndrome fibroblasts."
  *Nucleic Acids Research* **16**(22): 10607–10622.
- DOI: 10.1093/nar/16.22.10607 (constructed from NAR pattern; not printed in 1988 issue). PMID: 3186443 (lookup-confirmable, not verified here).
- Pages: 16. No paid lookup used.

## What the paper is
1988 wet-lab paper. Confluent human fibroblasts UV-irradiated (254 nm) at 5 or 30 J/m²,
pulse-labelled with ³H-thymidine, ¹⁴C-prelabelled to normalize DNA distribution.
Nuclei extracted with 2 M NaCl (high salt) or 25 mM LIS (low salt), digested
with DNase I, fractionated by neutral sucrose gradient → matrix-vs-loop DNA.
Read-out: ³H/¹⁴C ratio at the matrix as a function of % DNA at the matrix.
Plus autoradiographic grain-counting of halo-matrix structures and a Southern
blot for the ADA gene 5′ region. Cell lines: normal, XP-D, XP-C, CS.

## Quantitative content inventory
- **Fig. 1 A–D** — 4 scatter panels: x = "%DNA AT THE MATRIX" (0–100),
  y = "³H/¹⁴C RATIO" (0–4). ~10–25 points/panel, no error bars, dashed line at y=1.
  Digitizability: **MEDIUM**.
- **Fig. 2** — single scatter, same axes, pulse-chase; ~15–20 points, 2 conditions.
  Digitizability: **HIGH** (cleanest panel).
- **Fig. 3** — A: autoradiograph (image, not a plot). B–E: histograms of
  "% GRAINS AT THE MATRIX" vs "NUMBER OF DNA-HALOS"; some panels overlay
  two doses (5 vs 30 J/m²) as dotted/striped fills. Digitizability: **MEDIUM**.
- **Fig. 4** — scatter, same axes as Fig. 1/2, with normal + XP-D + XP-C + CS curves.
  ~20–30 points across 4 cell types. Digitizability: **HIGH**.
- **Fig. 5** — Southern-blot/gel image, 5 lanes. **No numeric axes.** Not a plot.
- **Tables:** none anywhere in the paper.
- **Reported summary numbers in the text:**
  - 30 J/m²: 1.3–1.6× enrichment of ³H label at matrix (1.5× in discussion).
  - 5 J/m², 2 h label: ~1.7× enrichment in normal and XP-D; >3× in XP-C;
    ~2× *depletion* in CS (i.e. matrix repair 2-fold less than loop).
  - Replication enrichment for comparison: 15–20×.
  - Grain percentages at matrix from autoradiography: 18.1% (unirradiated baseline),
    34.1% (5 J/m², 6 min pulse), 32.5% (5 J/m², 10 min pulse),
    23.6% (30 J/m², 10 min pulse), 18.7% (30 J/m², 120 min pulse).
  - ADA Southern: matrix DNA = 17.5% / loop = 82.5% (10 µg/ml DNase I);
    matrix = 10% / loop = 90% (12 µg/ml DNase I).
- **No equations, no rate constants, no fitted parameters, no p-values, no
  explicit SDs/N reported.** The "curves" through scatter points are eyeballed
  trends, not fits.

## Replication assessment
Nothing computational to replicate. There is:
- no model with parameters,
- no statistical test result to re-run,
- no machine-readable dataset (1988, autoradiography + sucrose-gradient
  ³H/¹⁴C scintillation counting),
- no algorithm description.

The only honest in-silico work possible is **figure digitization** + **re-derivation
of the summary fold-enrichments** (e.g. take Fig. 4, digitize each cell-type's
scatter, compute weighted-mean ³H/¹⁴C at low %-matrix vs high %-matrix and
recover the reported 1.7×, >3×, ~0.5× ratios). That would be a *cross-check*
of the authors' verbal summary against their own published scatter, not a
replication of an independent computation, and it cannot reach the original
biological measurement because the underlying DPM data are not tabulated.

## Verdict: **NO-GO**
- **Verdict:** NO-GO (with optional SPOT-CHECK fallback below)
- **Coverage:** N/A
- **Agreement:** N/A
- **Rationale:** Pre-modern (1988) wet-lab paper. Zero tables, zero
  parameters, zero algorithms, zero supplementary data. The quantitative
  content is a handful of scatter plots without error bars or fits, summarized
  by ~5 fold-enrichment numbers stated in text. No meaningful computational
  replication target exists.

### Optional SPOT-CHECK that *could* be done (~1–2 h of work, not done here)
If a re-analysis artifact is ever wanted:
1. Digitize Fig. 4 (4 cell types, ~25 points) with WebPlotDigitizer.
2. For each cell type, compute the ratio of mean (³H/¹⁴C) at the lowest two
   %DNA-at-matrix bins (matrix-enriched) vs the highest bin (mostly loop DNA).
3. Compare to reported text values: normal ≈1.7×, XP-D ≈1.7×, XP-C >3×, CS ≈0.5×.
4. Agreement criterion: within ±20% of stated fold-changes.

Likely outcome: it will reproduce because the authors literally read those
ratios off the same plot. Scientific value: ~zero. Cost: real. This is why
the headline verdict is NO-GO rather than SPOT-CHECK.

## Hard gates
- PROGRESS.md + progress JSON: written within 10-min window. ✅
- Final verdict assigned: NO-GO. ✅
- No author contact. ✅
- No paid endpoints. ✅
- Source PDF copied locally for inspection only; no redistribution. ✅
