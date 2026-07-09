# Artifact Harvest

All artifacts are open-access from arXiv (no paywall). Fetched via uicgpu proxy
(`ssh uicgpu; source ~/env.sh`) on 2026-07-02.

| Artifact | Source URL | Size | Notes |
|---|---|---|---|
| Paper PDF | https://arxiv.org/pdf/2104.12109v1 | 4,758,356 B | PDF 1.4 |
| Paper LaTeX source | https://arxiv.org/e-print/2104.12109v1 | 9,643,624 B (gz) | contains `revised1106.tex`, `ref.bib`, `revised1106.bbl`, `figures/*.eps` |
| pdftotext -layout dump | (derived) | 98,517 B | `work/paper.txt` |
| Main TeX source | (from tarball) | 80,669 B | `work/revised1106.tex` |

- arXiv id: **2104.12109v1** [math.NA], published 2021-04-25.
- DOI (published): 10.1137/20m135577x (SIAM J. Sci. Comput.).
- No author code repository is referenced in the paper; replication is a from-scratch
  reimplementation based on the equations in the text (schemes 3.9/3.12, 4.1).
- LLM judges (Argo proxy, free): argo:gpt-5.2, argo:gemini-2.5-pro, argo:gpt-4.1.
