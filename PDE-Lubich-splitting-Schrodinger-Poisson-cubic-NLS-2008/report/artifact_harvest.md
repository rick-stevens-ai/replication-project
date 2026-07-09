# Artifact harvest

| # | Source | URL | Local path | Size (B) | md5 |
|---|--------|-----|------------|----------|-----|
| 1 | Author preprint (Lubich, U. Tübingen) — full text of the 2008 Math. Comp. paper (public preprint) | https://na.uni-tuebingen.de/pub/lubich/papers/speq.pdf | work/lubich_2008.pdf | 169616 | 608e48c81bd247f3d8beef9b420d68cb |
| 2 | Semantic Scholar record (metadata, abstract, TLDR, openAccessPdf URL) | `GET /graph/v1/paper/DOI:10.1090/S0025-5718-08-02101-7` | — (metadata only) | — | — |

## What we did NOT harvest and why

- The AMS-hosted "official" PDF at `https://www.ams.org/mcom/2008-77-264/S0025-5718-08-02101-7/S0025-5718-08-02101-7.pdf` is Cloudflare-guarded and returns an HTML challenge page to non-browser user agents (verified from both local mac and `ssh uicgpu` at 2026-07-05 02:12 UTC). The Semantic Scholar `openAccessPdf.license = "public-domain"` on the same DOI confirms the content is redistributable; we use the author's own Tübingen preprint copy of the same paper.
- No reference software: this is a pure theory paper with **no numerical experiments**, no accompanying code, no data set. All the code below is our own independent implementation of the scheme defined by equation (1.4) of the paper.

## Code we wrote (all in `work/`)

- `lubich_splitting.py` — Fourier-spectral Strang split-step solver, four problems, five step sizes each, JSON output.
- `make_plot.py` — log-log convergence plot.
- `llm_judge.py` — Argo-proxy (free) LLM-judge call.
