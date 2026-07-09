# paper.pdf — MISSING

The target paper PDF was not successfully fetched during backfill on 2026-07-05.

## Target
- **Citation:** Chan AP, Choi Y, Brinkac LM, *et al.* (2020) "AbGRI4, a novel antibiotic resistance island in multiply antibiotic-resistant *Acinetobacter baumannii* clinical isolates." *J Antimicrob Chemother* 75(10):2760–2768.
- **DOI:** 10.1093/jac/dkaa266
- **PMID:** 32681170
- **PMC:** PMC7556812 (open access)

## Fetch attempts (all failed 2026-07-05)
| URL | Result |
|---|---|
| `https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7556812/pdf/dkaa266.pdf` | 1.8 KB HTML redirect (PMC PDF endpoint requires session cookie / interstitial) |
| `https://pmc.ncbi.nlm.nih.gov/articles/PMC7556812/pdf/dkaa266.pdf` | 1.8 KB stub — same redirect |
| `https://europepmc.org/backend/ptpmcrender.fcgi?accid=PMC7556812&blobtype=pdf` | HTTP/2 stream not closed cleanly (STREAM_CLOSED) |
| `https://academic.oup.com/jac/article-pdf/75/10/2760/34003345/dkaa266.pdf` | 5.6 KB HTML (paywall / Cloudflare interstitial) |

## Impact
None on the verdict. The paper's core testable claims (AbGRI4 gene content, AbGRI4± assignment,
ST2 lineage, OXA-23 breadth) are all independently verified from the public RefSeq assemblies in
`data/`. The paper PDF is required only for archival co-storage next to the replication artefacts.

## Manual retrieval
Download the free full-text PDF from:
- <https://pmc.ncbi.nlm.nih.gov/articles/PMC7556812/> (click "PDF" link — requires interactive session)
- <https://academic.oup.com/jac/article/75/10/2760/5871783> (JAC open access)

and drop the resulting file at:
`~/Dropbox/REPLICATE-PROJECT/BVBRC-24-AbGRI4-Abaumannii-Chan2020/paper.pdf`

Once present, this marker file can be deleted.
