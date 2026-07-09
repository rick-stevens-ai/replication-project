# Artifact Harvest

| Artifact | Source | Access | Size / notes |
|---|---|---|---|
| Paper metadata | Crossref `10.1115/1.3167098` | HTTP 200 | J. Appl. Mech. 50(3):609–614, 1983; abstract confirms E(x)=E₀exp(βx), Cauchy kernel, SIF vs β |
| OA full text | Unpaywall → NASA NTRS | is_oa=true | `https://ntrs.nasa.gov/api/citations/19820023830/downloads/19820023830.pdf` |
| PDF (local) | downloaded | 569,410 bytes, 23 pp, PDF 1.3 | `work/delale_erdogan_1983.pdf`  MD5 `ba1ab18356799a46cf8c8d6288c2a211` |
| Extracted text | `pdftotext -layout` | 844 lines | `work/delale_erdogan_1983.txt` |
| Equation page images | `pdftoppm -png -r 220/400` | — | `work/eq-*.png`, `work/mid-*.png` (for OCR of Eqs 9,25-38) |

**Reference/analytic test data (for β=0 validation), from classical Griffith-crack theory & the paper's own Table 1 β=0 row:**
- uniform crack pressure p=−p₀ → k₁(±a)/(p₀√a) = 1.000 / 1.000
- linear p=−p₁(x/a) → 0.500 / −0.500
- quadratic p=−p₂(x/a)² → 0.500 / 0.500
- cubic p=−p₃(x/a)³ → 0.375 / −0.375

**Headline numbers reproduced (paper Table 1, plane stress, ν=0.3, uniform pressure), k₁(a)/(p₀√a), k₁(−a)/(p₀√a):**
βa: 0.01→(1.003,0.997), 0.10→(1.025,0.973), 0.25→(1.060,0.930), 0.50→(1.113,0.861), 0.75→(1.162,0.797), 1.00→(1.209,0.740).

**Tooling:** Python 3 (numpy 2.4.3, scipy 1.18.0, sympy 1.14.0, matplotlib), poppler `pdftotext`/`pdftoppm`, Argo proxy (localhost:44497) for multi-judge (argo:gpt-5.2, argo:gemini-2.5-pro, argo:gpt-4.1). All compute local (light); free endpoints only.

No paper source code exists (1983); replication is fully from-scratch.
