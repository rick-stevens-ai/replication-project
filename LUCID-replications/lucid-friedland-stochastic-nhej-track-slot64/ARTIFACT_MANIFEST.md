# Artifact manifest — `lucid-friedland-stochastic-nhej-track-slot64`

All paths are relative to `~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid-friedland-stochastic-nhej-track-slot64/`.

## Top-level reports

| Path | Size | Provenance | Status |
| --- | --- | --- | --- |
| `README.md` | ~3 KB | This task | Authored 2026-06-09 |
| `FIRST_PASS_REPORT.md` | ~6 KB | This task | Authored 2026-06-09 |
| `PROGRESS.md` | ~6 KB | This task | Authored 2026-06-09 |
| `ARTIFACT_MANIFEST.md` | this file | This task | Authored 2026-06-09 |

## Source material (`source/`)

| Path | Size | Provenance | License / status |
| --- | --- | --- | --- |
| `pubmed_20426668.xml` | 5 KB | NCBI E-Utilities `efetch?db=pubmed&id=20426668` 2026-06-09 | Public (PubMed) |
| `rr1965_metadata.md` | 1 KB | Distilled from above XML | Notes |
| `model_notes.md` | 6 KB | Synthesized from PubMed abstract + the three companion PDFs | Notes |
| `henthorn2018_nhej.pdf` | 2.9 MB | `https://www.nature.com/articles/s41598-018-21111-8.pdf` 2026-06-09 | CC-BY 4.0 (Sci Rep) |
| `henthorn2018_nhej.txt` | 80 KB | `pdftotext -layout` of above | Derived |
| `kundrat2021_coupling.pdf` | 2.4 MB | `https://www.frontiersin.org/journals/physics/articles/10.3389/fphy.2021.719682/pdf` 2026-06-09 | CC-BY 4.0 (Front Phys) |
| `kundrat2021_coupling.txt` | 70 KB | `pdftotext -layout` of above | Derived |
| `li2014_nhej_complexity.pdf` | 875 KB | `https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0085816&type=printable` 2026-06-09 | CC0 (PLoS ONE) |
| `li2014_nhej_complexity.txt` | 95 KB | `pdftotext -layout` of above | Derived |

**Note:** the original target paper (Friedland-Jacob-Kundrát 2010, RR1965.1) is **closed-access** and is not stored in this folder. Unpaywall verified no OA, no repository copy as of 2026-02-09.

## Code (`code/`)

| Path | Size | Purpose |
| --- | --- | --- |
| `nhej_smoke.py` | 12 KB | Self-contained stochastic NHEJ smoke model |
| `run_smoke.py` | 6 KB | Driver: low-LET + high-LET cases, CSV / JSON / figure outputs, bi-exponential fit, half-time |

## Results (`results/`)

| Path | Size | Notes |
| --- | --- | --- |
| `smoke_summary.json` | 1 KB | Headline numbers; bi-exponential fit per case |
| `rejoining_curves.csv` | ~50 KB | Time × {surviving, misrejoined, correct} for both cases (721 rows × 7 cols) |

## Figures (`figures/`)

| Path | Size | Notes |
| --- | --- | --- |
| `dsb_rejoining.png` | ~35 KB | symlog-time plot of surviving + misrejoined DSB fractions, low-LET vs high-LET |

## Logs (`logs/`)

| Path | Size | Notes |
| --- | --- | --- |
| `smoke.log` | <1 KB | Stdout of the most recent `run_smoke.py` invocation |

## External references (not stored here)

- Friedland W, Jacob P, Kundrát P. Radiat Res 173:677 (2010). DOI 10.1667/RR1965.1 — closed-access target paper.
- Friedland W et al. Mutat Res 711:28 (2011) — PARTRAC reference paper, closed-access at our endpoints.
- Kundrát P et al. Sci Rep 10:15775 (2020) — DOI 10.1038/s41598-020-72857-z — already replicated in sibling project `~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid-partrac-analytical-formulas/`.
- Belov O et al. J Theor Biol 366:115 (2015) — DOI 10.1016/j.jtbi.2014.09.024 — closed at our endpoints; would be a good cross-check if we obtain the PDF.
