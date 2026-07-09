# Artifact Harvest — BVBRC-25 (Kavvas et al. 2018)

All artifacts are free and public. No auth required for any of these.

## Publication
| Artifact | Source / URL | Notes |
|---|---|---|
| Full-text XML | `https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6193043/fullTextXML` | 136,903 bytes; parsed for Methods + claims |
| Bibliographic record | Europe PMC `EXT_ID:30333483` (`work/europepmc.json`) | Nat Commun 9:4306, OA=Y |
| DOI | 10.1038/s41467-018-06634-y | CC BY 4.0 |

## Authors' processed data (GitHub: erolkavvas/microbial_AMR_ML, branch master)
| File | URL (raw.githubusercontent.com/.../master/data/) | Size | md5 |
|---|---|---:|---|
| `pangen_allele_df.csv` | allele presence/absence, 1595 strains × 15,367 alleles | 44,904,872 | e124e8743266015a3b78be89a7be6a6d |
| `pangen_cluster_df.csv` | cluster presence/absence, 1595 × 11,039 | 35,373,702 | b4b9fd0ad5d1009818230ee1618fc26c |
| `cluster_info.csv` | cluster → Rv/gene_name/product/pan-category map (11,039 clusters) | 961,583 | d88760d6b94cd631b0e4943a29d64d1e |
| `resistance_data.csv` | genome_id → R/S for 19 drug columns (13 used in paper) | 177,054 | 44b44275c1ee6a9abac2178061081cc7 |
| `strain_information.csv` | strain metadata | 1,358,946 | c08ff72d749eeceb41edd6e2029a145e |

Repo also contains the authors' own notebooks (`scripts/01_pairwise_tests.ipynb`, `02_ML_ensemble_SVM.ipynb`, `03_epistatic_analysis.ipynb`) and supplementary Excel data. We did **not** run their notebooks — we re-implemented the pipeline independently.

## Underlying primary data (not re-downloaded; provenance noted)
- 1,595 *M. tuberculosis* genomes: PATRIC / BV-BRC (`patricbrc.org`), identifiers in paper Supplementary Data 7.
- TB-ARC unpublished sequencing: Broad Institute (`https://olive.broadinstitute.org/projects/tb_arc`).
- NPEET entropy toolbox referenced by paper: `https://github.com/gregversteeg/NPEET`.

## Generated evidence (this replication)
| File | Description |
|---|---|
| `report/evidence/association_results.json` | Per-drug MI/chi2 gene rankings + known-gene recovery (10 drugs) |
| `report/evidence/pangenome_stats.json` | Core/accessory/unique breakdown + PE/PPE/PGRS enrichment |
| `report/evidence/svm_results.json` | Ensemble L1-SVM feature-selection frequencies + known-gene recovery |
| `work/replicate_fast.py` | Independent vectorized MI + chi2 implementation |
| `work/replicate_svm.py` | Independent ensemble L1-SGD-SVM implementation |
