# FIRST PASS REPORT — LUCID100 slot 31

**Paper:** Son et al., *Low-dose-rate ionizing radiation affects innate
immunity protein IFITM3 in a mouse model of Alzheimer's disease*,
Int J Radiat Biol 99(11):1649-1659, 2023.
**DOI:** 10.1080/09553002.2023.2211142  |  **PMID:** 37162420

## TL;DR

**Verdict: NO-GO** for an in-silico LUCID replication, with a strong
recommendation to **retag this row** in
`LUCID100_SOLID_MASTER_QA.tsv` from
`simulation/model replication` to a **wet-lab / no-public-data**
category. See `NO_GO_REPORT.md` for the formal verdict.

## What the paper actually does

This is an **in vivo mouse experiment**, not a simulation or model:

- Wild-type and 5xFAD transgenic mice are chronically exposed for
  112 days to low-dose-rate gamma radiation (cumulative 0, 0.1, 0.3 Gy).
- Behavior is assessed with Y-maze (working memory) and open field
  (locomotor / anxiety).
- Brain tissue is analysed for APP processing markers, gliosis
  (Iba1, GFAP), inflammatory cytokines (IL-1β, IL-6, TNF-α), IFN-γ,
  and IFITM3 (qPCR / IHC / western, standard wet-lab readouts).
- The headline result: IFN-γ and IFITM3 are significantly downregulated
  in 5xFAD brains after 0.1 or 0.3 Gy LDR; APP processing and gliosis
  are unaffected.

There is **no computational model, no simulation framework, no GitHub
release, no GEO/SRA series, no Zenodo deposit, no supplementary data
file** indicated in any of: Crossref, PubMed, EuropePMC, Unpaywall,
or Semantic Scholar metadata.

## Accessibility audit

| Channel | Result |
|---------|--------|
| Publisher (T&F / tandfonline) | 403 (Cloudflare) from sandbox; landing page only |
| DOI redirect | 406 |
| Unpaywall | `is_oa: false`, no OA locations, no embargo info |
| EuropePMC | `inPMC: N`, `hasPDF: N`, `hasSuppl: N` |
| PMC | Not indexed |
| Semantic Scholar `openAccessPdf` | `status: CLOSED` |
| PubMed "Free article" flag | Routes only to publisher landing |
| Author preprint (bioRxiv/Research Square) | Not found in S2/EPMC metadata |

The paper is functionally closed-access for the OpenClaw subagent
environment. Author contact and paid endpoints are forbidden per
task constraints, so paywall bypass is not in scope.

## What a replication would require

Two viable paths exist, both out of scope here:

1. **Wet-lab repro** — Repeat the 112-day chronic LDR exposure in
   5xFAD vs WT mice (n ≈ 6–10 per arm × 6 arms ≈ 36–60 mice), behaviour
   battery, and qPCR/IHC/western readouts. Estimated ≥ 6 months of
   wet-lab effort and IACUC-approved low-dose-rate irradiator access
   (such as the KIRAMS facility used by the authors). Not appropriate
   for a computational replication track.
2. **Figure digitization** — Even with full-text access, the paper
   presents only summary bar charts (means ± SEM) for ~10 readouts.
   Digitized values would let us recompute the reported t-tests/ANOVAs,
   but would not constitute a meaningful replication of the underlying
   biology. This path is *also* gated by lack of full-text access.

## Why neither is feasible as a LUCID100 in-silico target

- No raw data → nothing to load, nothing to recompute.
- No model / code → nothing to re-run.
- No supplement → no machine-readable tables to ingest.
- Behavioural + qPCR endpoints (bar charts of group means) → little
  signal to extract beyond "did the published p-value hold."

A LUCID replication value-add (rerun a published pipeline, regenerate
a figure, audit a model on new data) has no surface to attach to
here.

## Recommended QA actions

1. **Retag** in `LUCID100_SOLID_MASTER_QA.tsv` row 75:
   - `simulation/model replication` → `wet-lab / no public data`
   - `KEEP: relevant and replication-plausible` → `NO-GO: wet-lab, paywalled, no data`
2. **Score**: drop from 15 (A-tier) → < tier threshold; retire from
   Wave 4 active slots.
3. **Topic tag**: keep `dose-rate / low-dose response` and
   `immune / inflammation / senescence`; drop `computational model / simulation`.
4. Consider backfilling slot 31 with the next candidate that has
   accessible code/data (the LUCID curation pool likely has several
   wet-lab papers that should be similarly retagged — worth a sweep).

## Heavy-compute job plan

Not applicable. There is no replication target that warrants any
compute, on CherryRd or elsewhere.

## Smoke check

`scripts/smoke_scope.py` re-pulls Semantic Scholar, Unpaywall, and
EuropePMC and asserts the paper is still closed and supplement-free.
If any of those flip in the future, the script exits non-zero — at
which point this row should be re-evaluated.

```bash
cd /Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-ifitm3-alzheimers-low-dose-rate
python3 scripts/smoke_scope.py
```
