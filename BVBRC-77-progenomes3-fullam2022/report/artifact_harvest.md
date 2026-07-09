# BVBRC-77 artifact harvest

All files pulled 2026-07-03 during this replication run. All sources free/public.

## Paper (EuropePMC + NCBI eUtils)

| Artifact | Source | Size |
|---|---|---|
| Paper metadata JSON | `https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=proGenomes3+Fullam+2022+approaching&format=json&resultType=core` | 20 KB (7-hit list, 1 relevant) |
| Paper eSummary JSON | `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=36408900&retmode=json` | ~2 KB |
| Full-text XML | `https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9825469/fullTextXML` | 90,996 B (90 KB) |
| Extracted plain text | derived (stdlib xml.etree) | 33,686 chars |

## proGenomes / EMBL live data (progenomes.embl.de)

| File | URL | Bytes | SHA-256 |
|---|---|---|---|
| download page HTML | `https://progenomes.embl.de/download.cgi` | 16,317 | — |
| `pg4_representatives_for_each_ANI_cluster.tsv.gz` | `https://progenomes.embl.de/data/pg4_representatives_for_each_ANI_cluster.tsv.gz` | 227,325 | `64494a926b171c9b23e944a0ba304819acf65cb6b122ce13061618b140bc8925` |
| `pg4_ANI_clustering.tsv.gz` | `https://progenomes.embl.de/data/pg4_ANI_clustering.tsv.gz` | 5,013,890 | `582f57b5980649e632eaec6f5b1155a9aea8edefa350218323f5f0412cff6b03` |
| `pg4_ncbi_taxonomy.tsv.gz` | `https://progenomes.embl.de/data/pg4_ncbi_taxonomy.tsv.gz` | 6,094,365 | `67164a9817468044eea39df5fd861240986d0bc6814f3394ce5c8846ea18983d` |
| `pg4_consensus_gtdb_taxonomy_per_ani_cluster.tsv.gz` | `https://progenomes.embl.de/data/pg4_consensus_gtdb_taxonomy_per_ani_cluster.tsv.gz` | 442,309 | `549317686135158acd9456b2ee2ba46ca16cdd4a50e659ada5f112f51ca159ba` |
| **[promotion]** `pg4_excluded_genomes.txt.gz` | `https://progenomes.embl.de/data/pg4_excluded_genomes.txt.gz` | 3,816,992 | `203cf5cab40c3fc8397da96cd2986e3cb37b484ca7483b8ec07042daf5cd4a8a` |
| **[promotion]** `pg4_highly_important_strains.tsv.gz` | `https://progenomes.embl.de/data/pg4_highly_important_strains.tsv.gz` | 2,595 | `e648d4d95868bdf0d5e82e1d7dd7562106886373cc6db5db6626ff514db4afd6` |

Total pg4 metadata: ~15.3 MB gzipped, ~91 MB uncompressed. All 4 files verified as legitimate gzipped TSV (magic bytes ok, gunzip -c produces well-formed records).

## NCBI Datasets REST (per-genome, for 100-genome slice)

- Endpoint: `https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/accession/{gca}/dataset_report`
- 100 accessions queried, 99 successful (1 error).
- Per-record fields captured: `accession, contig_n50, total_sequence_length, gc_percent, number_of_contigs, assembly_status, assembly_level, release_date, checkm_completeness, checkm_contamination, checkm_marker_set, organism_name, tax_id`.
- Aggregate saved to `evidence/pg4_slice100_ncbi_stats.json` (~50 KB).

## LLM judges (Argo proxy — free)

### v1 (initial spot-check, 2026-07-03)
- `argo:gpt-4.1` → SPOT-CHECK (coverage=40, agreement=90)
- `argo:claude-sonnet-4.5` → SPOT-CHECK (coverage=45, agreement=75)
- `argo:gpt-4o` → SPOT-CHECK (coverage=60, agreement=80)
- `argo:claude-opus-4.7` → 502 Bad Gateway (dropped)
- `argo:claude-opus-4.8` → 502 Bad Gateway (dropped)
- `argo:gpt-5` → HTTP 400 (wrong request shape for reasoning models; dropped)

### v2 (promotion, 2026-07-04) — fed full-scale structural + DB-scale results
- `argo:gpt-4.1` → **PARTIAL** (coverage=80, agreement=95)
- `argo:claude-sonnet-4.5` → **PARTIAL** (coverage=75, agreement=85)
- `argo:gpt-4o` → **PARTIAL** (coverage=83, agreement=90)
- `argo:claude-opus-4.7` → 502 Bad Gateway (dropped)

**Unanimous PARTIAL** among available judges; mean coverage 79.3%, mean agreement 90.0%.

## Files produced this run (under `~/Dropbox/REPLICATE-PROJECT/BVBRC-77-progenomes3-fullam2022/`)

```
report/
  brief.md                         (0.8 KB)
  REPORT.md                        (9.3 KB)
  attempt_log.md                   (3.9 KB)
  artifact_harvest.md              (this file)
  evidence/
    pg4_slice100_ncbi_stats.json   (per-genome NCBI Datasets query results)
    slice100_summary.json          (aggregate statistics)
    llm_judge_verdicts.json        (v1 3-judge ensemble output)
    pg4_full_scale_stats.json      (v2 DB-scale structural + count analysis)
    llm_judge_verdicts_v2.json     (v2 3-judge ensemble output — unanimous PARTIAL)
work/
  paper_meta.json                  (EuropePMC search hit)
  paper_fulltext.xml               (90 KB, EuropePMC)
  paper_text.txt                   (33 KB, extracted)
  download_page.html               (16 KB)
  slice_analysis.py                (5.1 KB, source)
  compute_claims.py                (6.3 KB, source)
  judge.py                         (7.3 KB, source)
  full_scale_analysis.py           (6.7 KB, source; v2 promotion)
  judge_v2.py                      (8.2 KB, source; v2 promotion)
  slice_analysis.log
  compute_claims.log
  judge.log
  full_scale_analysis.log          (v2)
  judge_v2.log                     (v2)
  downloads/
    pg4_*.tsv.gz                   (6 files, 15.3 MB total)
```
