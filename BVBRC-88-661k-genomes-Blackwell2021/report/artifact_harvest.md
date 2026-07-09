# Artifact Harvest — BVBRC-88 (Blackwell et al. 2021 / 661k bacterial genomes)

All artifacts fetched via unauthenticated public HTTPS/FTP on 2026-07-03.

## Primary publication
| Item | URL | Size | Local |
|---|---|---|---|
| Paper PDF (OA, CC-BY) | https://journals.plos.org/plosbiology/article/file?id=10.1371/journal.pbio.3001421&type=printable | 1.83 MB | `work/pbio.3001421.pdf` |
| PubMed record | https://pubmed.ncbi.nlm.nih.gov/34752446/ | – | – |
| DOI | https://doi.org/10.1371/journal.pbio.3001421 | – | – |

## EBI FTP dataset root: `ftp.ebi.ac.uk/pub/databases/ENA2018-bacteria-661k/`
Full artifact listing (from FTP directory index, HEAD-verified reachable 2026-07-03):

| File | Size | Purpose | Fetched? |
|---|---:|---|---|
| `checklist.chk` | 55,626,683 B (53 MB) | MD5 checksum for every artifact (661,413 lines) | ✅ downloaded, parsed |
| `sampleid_assembly_paths.txt` | 70,245,400 B (67 MB) | Tab-separated `sample_id \t path` for every genome (661,405 lines) | ✅ downloaded, parsed |
| `661_assemblies.tar` | 750 GB | All 661,405 gzipped contigs in one tar | ⬛ HEAD 200; not downloaded (budget) |
| `661k.cobs_compact` | 872 GB | Compact bit-sliced signature index (COBS) | ⬛ listed only |
| `661_ppsketch_v1.5.h5` | 67 GB | pp-sketch genome distance index | ⬛ listed only |
| `661K_sourmash_index_scaled.sbt.zip` | 45 GB | MinHash/sourmash SBT index | ⬛ listed only |
| `Assemblies/batch_XXX/` | per-batch tree | Per-genome `SAM*.contigs.fa.gz` | ✅ 25 random samples pulled |

## Per-genome spot-check (25 random samples, seed=661405)
25 assemblies pulled to `work/sample_assemblies/`. All 25/25 md5 checksums match `checklist.chk`. Full per-sample table in `report/evidence/spot_check_results.json`. Species labels in `report/evidence/spot_check_species.json`.

## Figshare (metadata + Rnotebooks): `10.6084/m9.figshare.16437939`
Article API: https://api.figshare.com/v2/articles/16437939 → 18 files, list mirrored to `work/figshare_meta.json`.

| Figshare file | Size | Purpose | Fetched? |
|---|---:|---|---|
| `File2_taxid_lineage_661K.txt` | 95,719,950 B (91 MB) | Per-sample major species + NCBITaxa lineage | ✅ downloaded, parsed for species distribution |
| `File3_metadata_661K.txt` | 77,107,542 B (74 MB) | Summarized ENA metadata per sample | listed only |
| `File4_QC_characterisation_661K.txt` | 430,624,499 B (411 MB) | Full QC (QUAST, MLST, checkM, clermonTyping, seqSero2, high_quality flag) | ✅ streamed to count col 39 `high_quality` |
| `File1_full_krakenbracken.txt.zip` | 51 MB | Full Kraken2/Bracken top-50 per sample | listed |
| `File5_AMR_plasmids_661K.txt` | 99 MB | AMRFinder + plasmid replicon output | listed |
| `File6_AMR_presenceabsence_661K.txt.zip` | 10 MB | AMR gene P/A matrix | listed |
| `File8_plasmidreplicons_presenceabsence_661K.txt` | 575 MB | Plasmid replicon P/A matrix | listed |
| `Rnotebook1_QC_filtering.nb.html` | 2.6 MB | Fig 1 reproduction notebook | listed |
| `Rnotebook2_species_breakdown_section.nb.html` | 1.7 MB | Species-distribution notebook | listed |
| `Rnotebook3_AMR_section_figures.nb.html` | 2.6 MB | AMR figures notebook | listed |
| `Rnotebook4_661K_vs_genbank_patric.nb.html` | 1.3 MB | Cross-DB comparison | listed |
| `File4_column_descriptions.txt` | 761 B | Column key for File4 (39 cols, col 39 = high_quality) | ✅ downloaded, informs QC parse |

## Code repositories (pointed to by paper)
| Repo | URL | Purpose |
|---|---|---|
| assemble-all-ena | https://github.com/iqbal-lab-org/assemble-all-ena | The Unicycler/SPAdes wrapper used to produce all 661,405 assemblies |
| COBS index code | (in the ENA2018-bacteria-661k dir) | Serving the searchable index |

Not re-cloned (not needed for a data-plane spot check).

## Third-party ENA project umbrella
- ENA Umbrella project: `PRJEB46036` — the 661,405 assemblies re-deposited as third-party assemblies. Not re-queried this run; the FTP path is canonical.

## Provenance summary
- Every quantitative claim in the paper's abstract (661,405 total, 639,981 high-quality, 2,336 species, ~20 species covering 90%) is backed by a specific file at the URLs above, and every one of them was independently checked against the paper's numbers this run.
