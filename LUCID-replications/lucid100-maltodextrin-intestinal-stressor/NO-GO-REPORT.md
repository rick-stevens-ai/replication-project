# NO-GO Report — Arnold & Chassaing 2019, *Cell Mol Gastroenterol Hepatol*

## Paper / Authors / Venue
- **Title:** Maltodextrin, Modern Stressor of the Intestinal Environment.
- **Authors:** Arnold AR, Chassaing B.
- **Venue:** *Cellular and Molecular Gastroenterology and Hepatology* (2019).
- **DOI:** 10.1016/j.jcmgh.2018.09.014

## Claim(s) tested
**None — paper is off-topic for LUCID.**
The paper is a short gastroenterology mini-review summarising published evidence that dietary **maltodextrin** (a glucose-polymer food additive) disturbs the intestinal mucus layer, host–microbiota balance, epithelial cell metabolism, and innate immunity, and may contribute to chronic intestinal inflammation. It contains **no radiation physics, no radiobiology model, no DSB/repair kinetics, no LQ parameters, no dose, no dose-rate, no LET, no track-structure data**.

## Method (this report)
1. Read EuropePMC core record (`evidence/europepmc.json`) — title, author list, journal, year, DOI, MeSH/keywords confirmed.
2. Inspected EuropePMC full-text XML stub (`evidence/fullText.xml`, 16 KB) and EuropePMC HTML snapshot — confirms gut-biology review content.
3. Cross-checked against LUCID inclusion criteria (must have radiobiology model / radiation dose-response / DSB or chromosome aberration kinetics / track-structure / microdosimetric content).
4. No code run. No external fetch. No author contact.

## Results vs Paper
| Item | Paper content | LUCID-relevant content |
|---|---|---|
| Topic | Dietary maltodextrin → gut mucus, microbiota, IBD | None — not radiation |
| Quantitative model | None reported | None to replicate |
| Datasets | None new | None to re-analyse |
| Radiation exposure / dose / LET | Absent | N/A |
| DSB / repair / survival / LQ | Absent | N/A |

## Verdict
**NO-GO — off-topic** for LUCID. Paper was included in the LUCID100 backlog by mistake (likely tagging error on keywords such as "stress" or a citation-graph spillover from a downstream gut-radiation paper). It does not belong in a radiation-biology replication batch.

## Coverage / 10
**0 / 10** — nothing to cover; no claims to replicate.

## Agreement / 10
**N/A** — no model to compare.

## Resources used
- Single-host CPU, 1 Python interpreter call to print metadata.
- No GPU, no cloud, no paid endpoint, no journal-side access.
- Total wall time on writeup: ~1 minute.

## Tools / Datasets / Hardware
- EuropePMC public REST + cached HTML/XML in `evidence/`.
- Local CPU on CherryRd subagent runtime.

## Limitations
- Full publisher PDF was not retrieved (subscription-walled on ScienceDirect). Not a problem here: title + abstract content + journal scope are sufficient to confirm off-topic.
- If future LUCID batches mine the citation graph for downstream "radiation + microbiome + maltodextrin" work, that would belong in a *different* slug, not this one.

## Gates
- ≤10-min writeup: ✅
- Final verdict (REPLICATED/PARTIAL/SPOT-CHECK/NO-GO/BLOCKED): **NO-GO** ✅
- Coverage/Agreement: N/A (consistent with NO-GO) ✅
- No author contact: ✅
- No paid endpoints: ✅
