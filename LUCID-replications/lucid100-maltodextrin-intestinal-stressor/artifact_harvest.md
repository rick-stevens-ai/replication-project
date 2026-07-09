# Artifact Harvest — Arnold & Chassaing 2019

## Files in `evidence/`
| File | Size | Description |
|---|---|---|
| `europepmc.json` | 4.0 KB | EuropePMC core record. Title, authors, journal (Cellular and Molecular Gastroenterology and Hepatology), year 2019, DOI 10.1016/j.jcmgh.2018.09.014, MeSH and keywords. **No abstract returned** (truncated record). |
| `fullText.xml` | 16.4 KB | EuropePMC full-text XML stub (small — review article body is short). |
| `europepmc.html` | 28 KB | EuropePMC page snapshot. |
| `sciencedirect.html` | 815 KB | ScienceDirect landing page snapshot (article behind subscription on Elsevier; this is the publisher HTML wrapper, not the article body). |
| `tmp.html` | (top level, not in evidence/) | Scratch HTML, not used. |

## What is NOT here
- No model code, no parameters, no datasets, no Monte Carlo input, no fitted curves, no rate constants, no LQ alpha/beta, no DSB/repair time courses, no track-structure SDD.
- No supplementary tables.
- No radiation dose, dose-rate, LET, fractionation schedule, or repair half-time anywhere in the record.

## What the paper IS
- A short **commentary/mini-review** in a gastroenterology journal summarising published evidence that dietary maltodextrin (a glucose-polymer food additive) alters gut microbiota, mucus barrier, and epithelial cell biology, with implications for IBD.
- No new wet-lab data, no new model, no original numerical results to replicate.

## Conclusion of harvest
Nothing in `evidence/` constitutes a LUCID replication target. Report is **NO-GO**.
