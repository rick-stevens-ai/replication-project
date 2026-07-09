# Artifact harvest — BVBRC-124

All artifacts are public, open access.

## Primary source (paper)
| Path | Bytes | SHA-256 (first 16) | Source URL |
|---|---:|---|---|
| `paper.pdf` | 1,738,014 | `5c6c1ed176437d98` | https://europepmc.org/articles/PMC6193043?pdf=render |
| `work/data/paper.pdf` | 1,738,014 | `5c6c1ed176437d98` | duplicate of top-level (convenience) |

## Authors' data + code (github.com/erolkavvas/microbial_AMR_ML)
| Path | Bytes | SHA-256 (first 16) | Origin |
|---|---:|---|---|
| `work/data/pangen_allele_df.csv` | 44,904,872 | `a9753684e73ab922` | authors' GitHub `data/` |
| `work/data/pangen_cluster_df.csv` | 35,373,702 | `bd2694275890f716` | authors' GitHub `data/` |
| `work/data/cluster_info.csv` | 961,583 | `e5e628c204b3fb4a` | authors' GitHub `data/` |
| `work/data/resistance_data.csv` | 177,054 | `0fe5053065499972` | authors' GitHub `data/` |
| `work/data/strain_information.csv` | 1,358,946 | `70f1d0308a7ad92a` | authors' GitHub `data/` |

(Copied from sibling replication BVBRC-25 which originally downloaded them from the authors' GitHub repo. Files are byte-identical to the upstream distribution.)

## Springer supplementary
Springer static-content CDN (open access CC BY 4.0).

| Path | Bytes | SHA-256 (first 16) | Source URL |
|---|---:|---|---|
| `work/data/supplementary.pdf` (symlink → BVBRC-90 mirror) | 5.4 MB | (see BVBRC-90) | `static-content.springer.com/esm/art%3A10.1038%2Fs41467-018-06634-y/MediaObjects/41467_2018_6634_MOESM1_ESM.pdf` |
| `work/data/MOESM4.xlsx` | 83,565 | `6f61f7392e0d747c` | `…MOESM4_ESM.xlsx` |
| `work/data/MOESM5.xlsx` | 81,420 | `23805518a5d69aeb` | `…MOESM5_ESM.xlsx` |
| `work/data/MOESM7.xlsx` | 41,339 | `446af467ba63c625` | `…MOESM7_ESM.xlsx` |
| `work/data/MOESM9.xlsx` | 479,416 | `319df0d299ac8c93` | `…MOESM9_ESM.xlsx` |

(MOESM8 returns AccessDenied from Springer CDN per BVBRC-90's harvest; we did not need it here.)

## External API calls (no downloaded artifact, but logged)
| API | Endpoint | Query count | Purpose |
|---|---|---:|---|
| RCSB Search v2 | `search.rcsb.org/rcsbsearch/v2/query` | 40 (20 genes × 2 query types) | structural availability probe |
| Argo | `localhost:44497/v1/chat/completions` | 2 (1 attempted claude-opus-4.8 502, 1 successful gpt-5.2) | LLM-judge verdict |
| NCBI Eutils | `eutils.ncbi.nlm.nih.gov/…/esummary.fcgi` | 1 | verify PMID:30333483 is Kavvas et al. (assignment title said "Wang-2018" which is a typo) |

## License
All source PDFs, XLSX, and CSVs are open access (CC BY 4.0 for the Nature Communications paper; authors' GitHub repo is open source). No paywalled or embargoed data was accessed.
