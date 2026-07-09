# Artifact Harvest

| # | Artifact | Source | URL | Local path | Size (bytes) | MD5 | Notes |
|---|---|---|---|---|---|---|---|
| 1 | Paper PDF (Avci 2017) | DOISerbia via Wayback Machine snapshot 2017-12-02 | https://web.archive.org/web/20171202110906if_/http://www.doiserbia.nb.rs/img/doi/0354-9836/2017/0354-98361600302A.pdf | `work/paper.pdf` | 647,801 | `04148a1f70cec0f99c5e4156aaf80b10` | Original doiserbia.nb.rs and thermalscience.vinca.rs were HTTP 503 (whole servers down at replication time). Fetched via Wayback CDX index (2017 snapshot digest `O3CJRUJCZX6CYSESEG76L5ZCUODXXNIT`). |
| 2 | Paper text (extracted) | pdftotext on artifact #1 | (local) | `work/paper.txt` | ~40 KB | — | Used to lift equations 10–34 verbatim. |
| 3 | Semantic Scholar metadata | Semantic Scholar Graph API | `https://api.semanticscholar.org/graph/v1/paper/DOI:10.2298/TSCI160427302A` | (inline; abstract confirmed) | — | — | S2 paperId `76c498d122cdfc2c489221bfe5f722a3877bb513`, openAccessPdf status GOLD (broken at fetch time). |

**No supplementary data or MATLAB source code was released by the authors.** The paper says "The numerical results are held by introduction MATLAB codes" but does not publish them. Replication had to reimplement everything from the equations in the paper.
