# Artifact Harvest — Herbert 2021 replication

## Paper PDF (open access)

- **URL:** https://arxiv.org/pdf/2203.06846
- **File:** `work/herbert2021.pdf`
- **Size:** 3 335 568 bytes
- **HTTP:** 200
- **Origin:** arXiv preprint of Herbert (2021), WIREs CMS 11:e1519 (open access via S2 `openAccessPdf.status=GREEN`).
- **Publisher URL:** https://onlinelibrary.wiley.com/doi/10.1002/wcms.1519 — returned HTTP 403 (Wiley bot check), preprint used instead.

## Semantic Scholar record

- **URL:** `https://api.semanticscholar.org/graph/v1/paper/DOI:10.1002/wcms.1519?fields=title,year,openAccessPdf,abstract,authors,externalIds`
- **File:** `work/s2.json`
- **Auth:** S2 API key from macOS keychain `semantic-scholar-api-key` / `rick-stevens-ai` (per standing rule).

## Text extraction

- **File:** `work/herbert2021.txt` — `pdftotext -layout` full-text extraction of the PDF, 4748 lines. Used for locating Table 1 verbatim, Section 2.4 quantitative statements, and matrix operator table (Table 2).

## Software

- **PySCF 2.13.1** (installed into project-local venv at `work/.venv`), pip install `pyscf==2.13.1`. Provides four ASC-PCM methods (`C-PCM`, `IEF-PCM`, `COSMO`, `SS(V)PE`) in `pyscf.solvent.pcm.PCM`.
- **Python 3.14** (host) / 3.14 in venv.
- **pdftotext (Poppler)** for text extraction.

## LLM judges (Argo proxy — free)

- **Endpoint:** `http://localhost:44497/v1/chat/completions` (tunneled from studio-ts to CherryRd), `OPENAI_API_KEY=stevens`.
- **Judge A:** `argo:gpt-5.2` → `report/evidence/llm_judge_argo_gpt-52.json` — verdict `PARTIAL`, coverage 0.6, agreement 0.75.
- **Judge B:** `argo:claude-opus-4.7` → `report/evidence/llm_judge_argo_claude-opus-47.json` — verdict `REPLICATED`, coverage 0.75, agreement 0.85.

## No paid endpoints, no author code, no proprietary data

- Herbert 2021 is a **review** — the authors provide no source code and Table 1 numbers
  are cited from Chipman [Ref 95] and use an isodensity cavity implementation not
  distributed. Replication was done from equations and standard implementations only.
