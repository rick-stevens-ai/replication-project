# Data-availability search trail

Goal: identify any public dataset, supplementary file, or code repository tied to DOI `10.1016/j.dnarep.2025.103875` before deciding whether a minimal computational replication is feasible without author contact and without solving captchas.

## API checks (all run 2026-06-09)

| API | Query | Result |
| --- | --- | --- |
| Europe PMC `webservices/rest/search` (resultType=core) | `DOI:"10.1016/j.dnarep.2025.103875"` | 1 hit (`PMID 40737910`). `inPMC=N`, `hasSuppl=N`, `hasData=N`, `hasDbCrossReferences=N`. |
| NCBI eutils elink (pubmed→pmc) | `id=40737910` | No PMC linkset. No PMCID. |
| Crossref `works/` | DOI | Confirms PII `S1568786425000710`, vol 152, p.103875, published 2025-08, license=TDM, funder Strålsäkerhetsmyndigheten (SE). |
| Unpaywall v2 | DOI | `is_oa=true`, `oa_status=hybrid`, `license=cc-by`, but `url_for_pdf=null`, `has_repository_copy=false`, evidence=`deprecated`. |
| Elsevier `api.elsevier.com/content/article/PII:...` (no key) | `httpAccept=text/xml` | Returns coredata only (2 KB). Confirms `openaccess=1`, `openaccessType=Full`, license CC-BY 4.0, RAP 2025 (Poland) sponsor. |
| Elsevier same endpoint with `view=FULL` | — | `AUTHENTICATION_ERROR` (needs `X-ELS-APIKey`). |
| OpenAIRE | DOI | Only publisher landing-page URLs (DOI + PubMed). No repository copy. |
| ORCID (Wojcik 0000-0002-3951-774X) | works list | Entry present; only `external-ids` are DOI + ISSN — no Zenodo / GitHub / figshare attached. |

## Full-text acquisition attempts

| Route | Status | Notes |
| --- | --- | --- |
| `linkinghub.elsevier.com/retrieve/pii/S1568786425000710` (curl) | 200 HTML stub | No PDF link; redirects expected client-side. |
| `sciencedirect.com/.../pdfft?...&download=true` (curl) | 403 (Cloudflare HTML) | Bot-check; needs browser-issued tokens. |
| `reader.elsevier.com/reader/sd/pii/...` (curl) | redirected to cloudflare HTML | Same. |
| `sciencedirect.com/science/article/pii/S1568786425000710` (OpenClaw Chrome) | "Are you a robot?" Cloudflare Turnstile | **Captcha not solved** (out-of-scope autonomous action). |
| `researchgate.net/publication/393957175` (OpenClaw Chrome) | "Security check required" | Same gating. |
| `api.elsevier.com FULL` view | 401 INVALID_API_KEY | Would need Argonne/UJK API entitlement. |
| DDG `filetype:pdf` + paper title | 0 hits | No mirrored PDF surfaced. |
| DDG `site:ujk.edu.pl` + author + endpoint | 0 hits | No UJK institutional repo copy. |

## Inferences

- **No public omics deposition exists** for this paper based on every cross-index I can reach without author contact. The Europe PMC record's `hasData=N` + `hasDbCrossReferences=N` is the strongest indirect evidence; the absence of any `GSE…`, `PRJNA…`, `PRJEB…`, `E-MTAB-…`, `PXD…`, `figshare`, or `zenodo` reference in Crossref reference list, abstract, Unpaywall, OpenAIRE, or ORCID confirms it. The gene-expression endpoint is therefore almost certainly a **qPCR panel** (or NanoString), not an RNA-seq deposition.
- **Supplementary file enumeration requires the article landing page**, which is blocked by Cloudflare this pass. The Elsevier coredata view does not surface `mmc*` attachments.
- **OA license is CC-BY 4.0**, so re-distribution and quantitative reuse of any figure data is permitted once the PDF is in hand.

## Next-pass acquisition path (single best route)

1. Open the article in a *user* Chrome profile (`browser profile=user`) and let the human solve the Cloudflare Turnstile once (one-click checkbox).
2. From the rendered page, save:
   - Article PDF (`mmc0` / main).
   - All `mmc*` supplementary files (typically `mmc1.docx` methods + `mmc2.xlsx` data table for a paper of this kind).
3. Drop the PDF into `data/paper.pdf` and the supplements into `supplementary/`.
4. Re-run a non-data-blocked first pass: digitize Fig 1–3 with `WebPlotDigitizer` (locally installed) into `data/digitized_fig*.csv`, then run `code/foci_kinetics.py --fit data/digitized_fig1.csv` and `code/atm_inhibition_compare.py`.

No paid endpoints, no author contact.
