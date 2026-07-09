# Artifact Harvest

All fetches via uicgpu proxy internet (`source ~/env.sh`); local arXiv API/PDF access was
blocked by the CherryRd network, so retrieval was done on uicgpu.

| Artifact | URL | Size | Notes |
|---|---|---|---|
| Paper PDF | https://arxiv.org/pdf/2104.11813 | 3,636,289 B | arXiv:2104.11813v1, 23 Apr 2021 |
| Paper abstract HTML | https://arxiv.org/abs/2104.11813 | 39,550 B | metadata/author confirm |
| Paper LaTeX e-print | https://arxiv.org/e-print/2104.11813 | 7,916,857 B | CMS_Submission.tex (90 KB) + figures; exact equations extracted |
| Extracted text | pdftotext -layout paper.pdf | 122,764 B | 2049 lines; source of eqs 2.7/2.8, Tables 6.1/6.2, Thm 3.9/4.1 |

Local copies:
- `work/paper_2104.11813.pdf`
- `work/paper_2104.11813.txt`

**Paper identity confirmed:** title "Discrete Maximum principle of a high order finite difference
scheme for a generalized Allen-Cahn equation"; authors Jie Shen, Xiangxiong Zhang (Purdue Univ.);
arXiv 2104.11813v1 [math.NA]; DOI 10.4310/cms.2022.v20.n5.a9 (rank-10 candidate in
PDE_NEXT50_2026-06-26.tsv, OA-PDF/repro-ok).

No paper source code was used — the scheme was implemented purely from the published equations.
Software: Python 3, numpy, scipy (splu / dense inv), sympy (manufactured sources). Versions:
local numpy 2.4.3 / scipy 1.18.0 / sympy 1.14.0; uicgpu numpy 1.23.5 / scipy 1.10.1 / sympy 1.13.3
(Table 6.2 heavy 320x320 run executed on uicgpu).
