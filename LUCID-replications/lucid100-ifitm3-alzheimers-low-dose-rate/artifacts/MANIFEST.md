# Artifact Manifest — LUCID100 slot 31

| File | Source | Purpose | Verified |
|------|--------|---------|----------|
| `semantic_scholar.json` | Semantic Scholar Graph API v1 (DOI lookup) | Title, authors, abstract, tldr, openAccessPdf, externalIds (PMID 37162420, CorpusId 258589148) | 2026-06-09 |
| `unpaywall.json` | api.unpaywall.org v2 | OA status (closed), no repository copy, no embargoed locations | 2026-06-09 |
| `europepmc.json` | EuropePMC RESTful API (search, EXT_ID:37162420) | inPMC=N, hasPDF=N, hasSuppl=N, fullTextUrlList only publisher (Subscription required) | 2026-06-09 |
| `references.txt` | Semantic Scholar references field (38 entries) | Confirms wet-lab framing of the paper | 2026-06-09 |

## NOT obtained (and why)

| Would-want | Status | Reason |
|-----------|--------|--------|
| Full-text PDF | Missing | Closed access; tandfonline 403 (Cloudflare); Unpaywall `is_oa=false`; not in PMC |
| Supplementary tables/figures | Missing | EuropePMC `hasSuppl: N`; publisher landing page not reachable to verify |
| Raw qPCR / behavior CSVs | Missing | No GEO/SRA/Zenodo deposit indicated by any metadata source; paper does not appear to have a data-availability statement we can read |
| Code / scripts | N/A | Paper is wet-lab; no computational artifact expected |

## Replication-blocking determination

All four would-want categories are unattainable without either
(a) institutional access to the journal **and** (b) original
authors releasing raw data. Neither is achievable inside the
subagent constraints (no author contact, no paid endpoints).
