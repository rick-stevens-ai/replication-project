# NO-GO REPORT — LUCID100 slot 31

**Paper:** Son et al. 2023, IJRB, DOI 10.1080/09553002.2023.2211142
**Decision:** NO-GO for in-silico replication.
**Subagent:** `a647a34d-3bf3-45ee-a7f5-eda0ed2f785f`  |  **Date:** 2026-06-09

## Verdict

This paper is **not a viable LUCID100 replication target.** It is an
in vivo mouse study (5xFAD + WT, 112-day chronic LDR exposure) with
**closed-access full text, no supplement, no public dataset, and no
code.** There is no computational artifact to re-run and no
machine-readable data to re-analyse.

## Evidence checklist

| Required for a GO | Present? |
|---|---|
| Full-text access in sandbox | ❌ Tandfonline 403 (Cloudflare); Unpaywall `is_oa=false`; not in PMC |
| Supplementary materials | ❌ EuropePMC `hasSuppl=N`; nothing referenced in indexed metadata |
| Code / scripts | ❌ Paper is wet-lab; no repository referenced |
| Public raw data (GEO/SRA/Zenodo/Figshare) | ❌ No deposit indicated by Crossref, PubMed, EuropePMC, or S2 |
| In-silico model or simulation | ❌ Despite master TSV tag, paper has none |
| Replicable computational pipeline | ❌ |

## Master TSV retag recommendation

Row 75 of `LUCID100_SOLID_MASTER_QA.tsv` currently encodes:

- `topics`: `dose-rate / low-dose response; immune / inflammation / senescence; computational model / simulation`
- `replication_type`: `simulation/model replication`
- `qa_label`: `KEEP: relevant and replication-plausible`

Recommend:

- `topics`: drop the `computational model / simulation` entry; keep the rest.
- `replication_type`: `wet-lab in vivo / no public data`
- `qa_label`: `NO-GO: wet-lab, paywalled, no public data, no code`
- `score`: demote from 15 (A-tier) below the Wave-4 active threshold.

## Constraints honored

- ✅ No author contact attempted.
- ✅ No paid endpoints used (Semantic Scholar API key is free-tier auth).
- ✅ No heavy compute attempted on CherryRd; nothing to run.
- ✅ Source of truth read but not modified.

## Recommended next action

Backfill slot 31 with the next Wave-4 candidate that has either:

- A code release (GitHub/Zenodo) and a reproducible pipeline, or
- An open dataset (GEO/SRA) plus an analysis paper, or
- A real simulation (mechanistic model with parameters/equations).

Also recommend doing a one-pass sweep of the other Wave-4 rows that
were auto-tagged `computational model / simulation` to catch other
wet-lab misclassifications. (See FIRST_PASS_REPORT for rationale.)
