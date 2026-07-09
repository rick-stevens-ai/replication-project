# Artifact Harvest

| Artifact | Source URL | Type | Size | Notes |
|---|---|---|---|---|
| arXiv abstract/metadata | http://export.arxiv.org/api/query (au:Bertozzi, ti:"finite time blowup") | API/XML | — | Resolved to arXiv:1204.1095v1, 2012-04-05 |
| Full-text PDF | https://arxiv.org/pdf/1204.1095 | PDF | 436,511 B | 32 pages, PDF 1.4; `work/bgl.pdf` |
| LaTeX source | https://arxiv.org/e-print/1204.1095 | gzip'd .tex | 45,613 B (compressed) → 155,653 B | single file `BGL-revised-Nov18.tex`; `work/BGL-revised.tex` (2519 lines) |
| Extracted text | (local pdftotext -layout) | txt | 119,559 B | `work/bgl.txt` (1781 lines) |

## Access notes
- Publisher (SIAM / T&F / MDPI) landing pages were Cloudflare/403-blocked to curl and web_fetch. Not needed: arXiv provides the authoritative full text + LaTeX source (free/OA), which is the canonical version of record for the mathematical content.
- No authors' code repository is associated with this paper (it is an analysis paper). Replication therefore = independent re-derivation + from-scratch numerical verification of its exact Section-4 predictions.

## Tool versions
- Python 3, numpy 2.4.3, scipy 1.18.0 (local, CherryRd).
- pdftotext (poppler) /usr/local/bin/pdftotext.
- LLM judges via Argo proxy (localhost:44497, key=stevens, FREE): argo:gpt-5.2, argo:gemini-2.5-pro, argo:gpt-4.1.
