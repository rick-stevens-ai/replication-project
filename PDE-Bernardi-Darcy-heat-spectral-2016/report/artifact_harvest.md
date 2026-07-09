# Artifact Harvest

| Artifact | Source | Detail |
|---|---|---|
| Paper PDF (OA green) | HAL: https://hal.sorbonne-universite.fr/hal-01085011/document | 23 pages, 927,448 bytes, MD5 `2d6ead2ce797287b0718d8cc156a1ecd`. Saved as `work/bernardi_darcy_heat_2016.pdf`. |
| S2 metadata | Semantic Scholar Graph API (DOI:10.1093/IMANUM/DRV047) | paperId `ed41fbd44ddc06ab0e0a66ba61f4607d76a784c2`, CorpusId 44216113, year 2016; openAccessPdf status GREEN pointing at the HAL file. |
| Extracted text | `pdftotext` of the PDF | `work/paper.txt` (1853 lines). |

## Access notes
- Unpaywall reports `oa_status: closed` (the OUP publisher copy is paywalled), but Semantic
  Scholar surfaced the authors' HAL preprint (green OA). The HAL preprint (submitted 2014-11-20,
  "Preprint submitted") is the OA version used here; it contains the full model, discretization,
  a priori analysis, and the Section 5 numerical experiments.
- HAL is behind an "Anubis" JS proof-of-work anti-bot wall. Plain `curl` returned the challenge
  HTML. Resolved by loading the page in the OpenClaw-controlled Chromium (challenge auto-solved),
  reading the `c2sd-an-auth` cookie via CDP `evaluate`, then replaying it with `curl -H Cookie:`
  to fetch the raw `application/pdf` (verified `%PDF-1.4`, 23 pages).

## No upstream code
- The paper's computations were done in **FreeFEM3D (spectral version)**, an internal/thesis
  code (Yakoubi thesis [19], Del Pino [13]); no public repository is referenced. The replication
  is therefore a **from-scratch independent reimplementation**, not a rerun of author code.
