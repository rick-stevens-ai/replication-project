# paper.pdf — MISSING

**Paper.** Harmer CJ, Lebreton F, Stam J, McGann PT, Hall RM. "Complete genome of the extensively antibiotic-resistant GC1 *Acinetobacter baumannii* isolate MRSN 56 reveals a novel route to fluoroquinolone resistance." *J Antimicrob Chemother* 77(7):1851-1855, 2022.

- **DOI:** 10.1093/jac/dkac115
- **PMID:** 35403193
- **PMCID:** PMC9244215 (open access, CC-BY)
- **Semantic Scholar paperId:** b43c132b5dd2c5d3b00089bc784354c3c1f7302e

## Why paper.pdf is not on disk

Non-interactive fetch attempts on 2026-07-05 during both the initial replication pass and the 8-artifact backfill pass failed at all 7 open-access endpoints tried:

| Endpoint | Result |
|---|---|
| `https://academic.oup.com/jac/article-pdf/77/7/1851/44373670/dkac115.pdf` | HTML anti-bot challenge page (OUP) |
| `https://oup.silverchair-cdn.com/oup/backfile/Content_public/Journal/jac/77/7/10.1093_jac_dkac115/1/dkac115.pdf` | 146-byte XML error stub (Silverchair CDN) |
| `https://europepmc.org/backend/ptpmcrender.fcgi?accid=PMC9244215&blobtype=pdf` | HTTP/2 STREAM_CLOSED |
| `https://europepmc.org/article/MED/35403193/pdf` | 28 KB HTML (redirect landing page, not PDF bytes) |
| `https://europepmc.org/article/PMC/9244215/pdf` | 28 KB HTML (redirect landing page, not PDF bytes) |
| `https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9244215/pdf/dkac115.pdf` | 1.8 KB "Preparing to download" HTML gate |
| `https://pmc.ncbi.nlm.nih.gov/articles/PMC9244215/pdf/dkac115.pdf` | 1.8 KB "Preparing to download" HTML gate |
| `https://www.researchgate.net/publication/359942929/download` | 17-byte error stub |

All three primary open-access gates (OUP publisher, Europe PMC, NCBI PMC) implement some form of interactive-only fetch gate (bot detection, JS-issued cookie, or referer/session check). The paper is not in the central Eagle Marker or Nougat corpus either (grep across `/eagle/projects/AuroraGPT/stevens/scout_corpus/{md,mmd}/` and `/eagle/projects/AuroraGPT/stevens/osti_marker/{md,mmd}/` returned zero hits for "MRSN 56", "dkac115", or "Harmer").

## How to close this gap

1. Open a real browser session and download `dkac115.pdf` from any of:
   - `https://academic.oup.com/jac/article/77/7/1851/6572708` → PDF link
   - `https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9244215/pdf/dkac115.pdf`
   - `https://europepmc.org/article/MED/35403193` → PDF link
2. Save at `~/Dropbox/REPLICATE-PROJECT/BVBRC-111-Acinetobacter-baumannii-GC1-XDR-2022/paper.pdf`.
3. Delete this MISSING marker.
4. Optional but recommended:
   - `marker_single paper.pdf --output_dir extraction/ --output_format markdown` → rename to `extraction/marker.md`, deleting the pending stub.
   - Queue into Nougat pipeline OR run `nougat paper.pdf -o extraction/` on a GPU host → replaces `extraction/nougat.mmd`.
   - Recompute sha256(paper.pdf) and record in both extraction stubs for future central-corpus alignment.

## What the replication used instead

Grounding for this replication in the absence of the PDF text:

- Paper's own GenBank submission metadata for chromosome CP090606.1 + plasmids CP080453..CP080456 (which encodes the AbaR28 / Tn2006 / Tn7 / Tn7+ / gyrA / marR annotations directly in the feature table).
- NCBI PubMed abstract via `esummary` for PMID 35403193.
- Paper's per-claim assertions transcribed from the abstract into `report/REPORT.md` and `report/REPORT.tex`.

This means any nuance living only in the paper's Methods, discussion, or supplementary tables was not consulted during this replication. See `report/failure_analysis.md` §A1 for the residual gap.
