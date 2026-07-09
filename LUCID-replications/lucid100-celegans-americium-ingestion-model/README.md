# LUCID100 / Wave 2 slot 20 — C. elegans americium ingestion internal-radiation model

## Citation
Xiong Q, Tan Y, Li C, Wu X, Chen X, Chen C. **An Ingestion-based Chronic Internal Radiation Model in *Caenorhabditis elegans* Using Americium Trichloride Reveals Tissue-specific Oxidative Stress and Reproductive Toxicity.** *Annual Research & Review in Biology* **41(5)**: 25–36 (2026-04-28). DOI: [10.9734/arrb/2026/v41i52391](https://doi.org/10.9734/arrb/2026/v41i52391)

- LUCID100 rank: **51** (Wave 2, slot 20)
- Master TSV: `~/.openclaw/workspace/lucid-replications/LUCID100_SOLID_MASTER_QA.tsv`, row 52
- Worktype tag (master): `simulation/model replication`
- Master QA tag (incoming): `KEEP: relevant and replication-plausible`
- Recommended retag (this report): **DEMOTE — predatory-adjacent venue, 0 citations, brand new**

## DOI landing & availability

- DOI resolves: ✅ `https://doi.org/10.9734/arrb/2026/v41i52391` → `https://journalarrb.com/index.php/ARRB/article/view/2391`
- Landing page reachable: ❌ via plain HTTP (`HTTP 403`, Cloudflare bot challenge / `cf-mitigated: challenge`)
- Direct PDF URL (from Crossref `link`): `https://journalarrb.com/index.php/ARRB/article/download/2391/5070` — also Cloudflare-blocked to curl
- Full-text retrieval status: **NOT obtained** in this recovery pass. A `source/paper.pdf` exists from the previous (timed-out) attempt, but PDF metadata (`Creator: Chrome/149.0.0.0`, `Producer: Skia/PDF m149`, 3 pages, 584 KB) shows it is a **browser-printed render of the article landing page**, not the article PDF itself.
- Open Access flag (OpenAlex / Unpaywall via S2): paper marked OA, license unspecified in Crossref.

## Relevance to LUCID

Topically a clear fit:

- Chronic, low-dose, **high-LET internal alpha** exposure (Am-241 / AmCl₃) via ingestion pathway in *C. elegans*.
- Endpoints: oxidative-stress reporter strains (CF1553 `sod-3::GFP`, CL2166 `gst-4::GFP`, PD4251, RW1596), chemotaxis, reproductive output, embryo hatching, vulva morphology.
- Touches LUCID themes: dose-rate / low-dose response, radiation quality / RBE for alpha vs photon, tissue-specific differential radiosensitivity.

What's missing for full LUCID alignment:

- No computational/dosimetry model is described in the abstract — the paper is **wet-lab** despite master TSV tagging it `simulation/model replication`. The replication category in the master row appears mis-applied.
- No mention of TOPAS/Geant4/PHITS, no Monte Carlo, no MEDRAS-class modeling. The 0.748 µSv "tightly controlled dose" claim is asserted without methodology visible from metadata.

## Venue / credibility signals

| Signal | Value | Source |
|---|---|---|
| Journal | *Annual Research & Review in Biology* | Crossref |
| Publisher | Sciencedomain International | Crossref |
| In DOAJ | **No** | OpenAlex |
| Indexed in Scopus | **No** | OpenAlex |
| 2-year mean citedness | **0.41** | OpenAlex |
| OpenAlex h-index (journal) | 36 | OpenAlex |
| This paper citations | **0** | OpenAlex / S2 / Crossref |
| Author affiliations resolved | none in metadata | OpenAlex/S2 |
| Publisher Beall-list status | Historically flagged predatory (Sciencedomain / SCIENCEDOMAIN) | Beall's list legacy mirrors |

## Layout
- `source/paper.pdf` — **landing-page screenshot PDF** from prior session (not article body). Kept for forensic transparency; do not cite.
- `source/landing.html`, `source/hal.html` — captured Cloudflare/landing HTML from prior session.
- `docs/abstract_metadata.json` — full metadata harvested from Crossref + OpenAlex + Semantic Scholar (canonical content for this no-go).
- `docs/landing_page_extract.txt` — pdftotext of the landing-page render (confirms it's only the journal-style landing chrome).
- `PROGRESS.md` — log of what was attempted.
- `ARTIFACT_MANIFEST.tsv` — accessible / failed artifacts.
- `NO_GO_REPORT.md` — verdict + recommended QA retag.

## Quick verdict
**NO-GO for replication slot. Recommend DEMOTE from LUCID100.** See `NO_GO_REPORT.md`.
