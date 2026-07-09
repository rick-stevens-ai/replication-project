# Artifact Harvest — Cantabella et al. 2022

## Files in `evidence/`
| File | Size | Description |
|---|---|---|
| `europepmc.json` | 8.9 KB | EuropePMC core record. Title, authors (IRSN / Univ. Montpellier / Inserm), journal *Cancers* 14:3793, year 2022, DOI 10.3390/cancers14153793, open access. Full abstract included. |
| `fullText.xml` | 213 KB | EuropePMC open-access full-text XML — body, methods, results, figure captions, references. |

## String-search evidence in `fullText.xml` (2026-06-16 21:19 CDT)
| Term | Count | Implication |
|---|---:|---|
| `27 DEG` | 6 | Confirms abstract's "27 DEGs at 0.05 mGy/h" is stated in body, multiple times. |
| `200 DEG` | 6 | Confirms abstract's "200 DEGs at 0.5 mGy/h" is stated in body. |
| `530 DEG` | 6 | Confirms abstract's "530 DEGs at 5 mGy/h" is stated in body. |
| `GSE206573` | 4 | Raw RNA-seq data deposited at NCBI GEO, accession **GSE206573**. Re-running the pipeline is feasible (out of scope here). |
| `mGy/h` | 40 | Dose-rate units used throughout — chronic exposure framing consistent. |
| `dose rate` | 37 | Consistent dose-rate-dependent framing. |
| `oxytocin` | 29 | Headline target gene confirmed in body (`crx` is the other RNA-ISH target per abstract). |
| `telencephalon` | 7 | Tissue dissected for RNA-seq, consistent with abstract. |
| `in situ hybridization` | 12 | RNA-ISH validation method consistent. |

## What is NOT here
- No raw FASTQ files (those live at GEO **GSE206573**; not retrieved for this writeup pass).
- No DESeq2 / edgeR result table (figures only in the EuropePMC XML, no machine-readable supplementary table cached locally).
- No re-analysis pipeline (alignment + counting + DE testing) was run — RNA-seq re-analysis of 36 samples is out of scope for a free-local-CPU single-shot pass.
- No behavioural-assay raw data (locomotion / freezing / social-stress traces).

## Conclusion of harvest
- The paper's headline DEG counts (27 / 200 / 530) are internally consistent: each appears 6 times in the body, not just the abstract.
- GEO deposition is real (GSE206573, cited 4 times) — independent re-analysis is possible in a future, larger replication batch.
- A genuine end-to-end replication (download GSE206573, re-align, re-call DEGs) is **out of scope** for a 30-minute writeup pass but is a clean follow-up target. Verdict for this pass: **SPOT-CHECK — internal consistency confirmed, end-to-end re-run deferred.**
