# Artifact Harvest

| Artifact | Source | Notes |
|---|---|---|
| Paper PDF | Wayback Machine snapshot `20200819013624` of `content.sciendo.com/downloadpdf/journals/amns/5/2/article-p177.pdf` | 708,147 bytes, PDF v1.5, 6 pages. md5 `2b45aa9e9e100404f6696d47a8c4bb6c`. Saved as `work/paper.pdf`. |
| Paper text | `pdftotext -layout paper.pdf` | `work/paper.txt`, 485 lines. |
| DOI | 10.2478/amns.2020.2.00023 | OA GOLD CC-BY per Semantic Scholar + Unpaywall. |

## Fetch notes (provenance of the retrieval)
- Live publisher pages are **dead**: `sciendo.com/article/...` and `sciendo.com/pdf/...` now return a Next.js 404 shell (site migrated to Paradigm/reference-global); `degruyterbrill.com/document/doi/10.2478/amns.2020.2.00023/html` returns "Page not found"; De Gruyter `/pdf` returns HTTP 202 bot-challenge with empty body.
- ResearchGate fulltext PDF: Cloudflare error 1020 (blocked), from both local and uicgpu egress.
- CORE (`api.core.ac.uk/v3/outputs/330046325`): record exists but no downloadable fulltext.
- **Resolution:** located an archived copy of the original Sciendo PDF via the Wayback Machine CDX API (`web.archive.org/cdx/search/cdx?url=content.sciendo.com/downloadpdf/journals/amns/5/2/article-p177.pdf&filter=statuscode:200`) — one hit, `application/pdf`, 659,450 bytes, snapshot 2020-08-19. Downloaded via `web.archive.org/web/20200819013624id_/...` (raw byte-identical replay). This is the authentic publisher PDF, not a re-render.

## No external data required
This is a self-contained numerical PDE replication using manufactured solutions; no external datasets are needed. The only "data" are the paper's own reported error-norm tables, transcribed verbatim into `work/cn_frac_burgers.py`.
