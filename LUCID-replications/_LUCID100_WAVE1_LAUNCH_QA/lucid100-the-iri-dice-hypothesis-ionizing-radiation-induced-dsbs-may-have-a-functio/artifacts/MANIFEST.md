# Artifact Manifest — IRI-DICE (Langen et al. 2020)

Slot: LUCID100 Wave 1, slot 8 (rank 39).
DOI: 10.1007/s00411-020-00854-x.
Paper type: Controversial Issue / hypothesis paper (no primary data, no code).
Harvest date: 2026-06-09.

## Files harvested

| File | Bytes | SHA-256 (head) | Source |
|---|---|---|---|
| `paper.pdf` | 645590 | `ba50883d55f1262f9090a7348e170260b13166c8f901dfdea1ba1524e5fadc36` | Springer (CC-BY 4.0 OA) |
| `paper.txt` | ~33 KB | (derived; `pdftotext -layout`) | derived from `paper.pdf` |

URL fetched: `https://link.springer.com/content/pdf/10.1007/s00411-020-00854-x.pdf`
License: Creative Commons Attribution 4.0 International (Open Access).

## Supplementary / code / data status

- **Supplementary materials:** none listed on Springer landing page or in the PDF.
- **Code repository:** none. No GitHub, Zenodo, OSF, or other repository is cited.
- **Data accession:** none. The paper presents no new experimental data.
- **Figures/tables in paper:** 1 figure (Fig. 1, conceptual illustration of IRI-DICE mechanism). 0 tables.
- **Quantitative equations:** none. The paper is qualitative throughout.

## Cited primary data / mechanism papers (potentially reproducible elsewhere)

These are *cited* — not part of this paper's deliverables — and would only matter
for a deeper "is the underlying biology real?" replication, not for replicating
*this* paper:

- Shanbhag et al. 2010, Cell 141:970–981 — DISC mechanism (DSB-induced silencing in cis), original reporter-construct evidence.
- Pankotai et al. 2012, Nat Struct Mol Biol 19:276–282 — DNAPK-dependent RNAPII arrest.
- Iannelli et al. 2017, Nat Commun 8:15656 — multilayered expression around in-situ-mapped DSBs (genome-wide; *this* one does have a public dataset on GEO and would be the closest reproducible follow-up).
- Rothkamm & Löbrich 2003, PNAS 100:5057–5062 — persisting DSBs at very low X-ray dose.
- Langen, Rudqvist, Schüler et al. — author group's own transcriptomic series in mouse tissues after 211At/131I/177Lu (multiple PLoS ONE / EJNMMI Res / Nucl Med Biol papers).

## Derived artifacts (this work)

| File | Purpose |
|---|---|
| `code/iri_dice_toy_mc.py` | Minimal toy Monte Carlo of the IRI-DICE conceptual model. |
| `artifacts/figs/fig_doseresponse_diversity.png` | Per-cell perturbation distribution across 7 doses (0.001–2 Gy). |
| `artifacts/figs/fig_suppression_dominance.png` | Mean suppressed vs overexpressed genes per cell vs dose. |
| `artifacts/figs/fig_repair_threshold.png` | Mean persistent perturbation vs dose, showing repair-threshold non-monotonicity. |
| `artifacts/figs/summary.json` | Numeric summary of the dose scan. |
| `FIRST_PASS_REPORT.md` | Verdict and replication scoping report. |
