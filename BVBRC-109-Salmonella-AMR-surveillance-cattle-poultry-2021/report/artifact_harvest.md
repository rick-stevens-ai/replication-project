# Artifact harvest — BVBRC-109

## Source paper + metadata
- Paper PDF (PLOS ONE, public domain): https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0243681&type=printable — 2.9 MB → `work/paper.pdf`
- Semantic Scholar record: `work/s2_paper.json` (S2 paperId ce2e75f86fe1abf9fc9a5a32065f6f4e405d0b1b)
- PubMed ID: 33951039 · PMC: PMC8099073 · DOI: 10.1371/journal.pone.0243681
- Open access under CC0 (public domain).

## Supplementary data (all from PLOS)
- `work/S1_File.xlsx` (77 study isolates + NCBI accessions + assembly QC) — auto-normalized to `work/study_isolates.csv`
- `work/S2_File.xlsx` (2400 public NCBI Pathogen Detection Salmonella from Mexico by source category) — auto-normalized to `work/public_isolates.csv`
- `work/S3_File.xlsx` (40 public Typhimurium from Mexico, with AMR genotypes and MDR classifications) — auto-normalized to `work/S3_File.csv`
- `work/S4_File`, `S5_File`, `S6_File`, `S7_File` — supplementary PDFs (figures/tables), downloaded but not required for replication.

## NCBI assemblies (68 of the study's 77)
- BioProject: PRJNA480281 (SENASICA Mexico Salmonella surveillance)
- Discovered via `datasets summary genome accession PRJNA480281 --assembly-source GenBank` (1147 total assemblies in project; 68 match study BioSamples in S1_File)
- Bulk downloaded via NCBI `datasets` CLI v18.32.0 → `study_genomes.zip` (97.2 MB)
- Flattened to 68 individual `.fna` files under `/data/stevens/bvbrc109/assemblies_flat/` on uicgpu (total 315 MB)
- Mapping table: `work/study_assemblies.tsv` (GCA_… → BioSample SAMN…)
- 9 study isolates have no NCBI assembly (raw reads only): SAMN12345832, SAMN12345840, SAMN15872719–25 → `work/missing_samns.txt`

## Reference sequences
- Salmonella Genomic Island 1 (SGI-1): NCBI nuccore AF261825.2, 48.8 kb, fetched via `efetch -db nuccore -id AF261825.2 -format fasta` → `sgi1_ref.fna` on uicgpu

## Compute environment (uicgpu, /data/stevens/bvbrc109)
- OS: Ubuntu; 8 × NVIDIA A100 80GB (unused for this task — CPU-only bioinformatics)
- Conda env `/data/stevens/envs/bvbrc14` (Python 3.11.15):
  - amrfinder 4.2.7 (database 2026-03-24.1)
  - mlst 2.33.1 (senterica_achtman_2 scheme, PubMLST snapshot)
  - blastn (NCBI BLAST+ 2.14+)
  - entrez-direct efetch (for reference sequence pull)
- NCBI datasets CLI 18.32.0 (self-installed from ftp.ncbi.nlm.nih.gov)
- Proxy: uicgpu uses `HTTP(S)_PROXY=http://<lan-host>:3128` for outbound (loaded from `~/env.sh`)

## Analysis outputs (all under `work/` and `report/evidence/`)
- `work/all_amr_calls.tsv` — 7,639 AMRFinderPlus AMR gene + point mutation records across 68 assemblies
- `work/all_mut_calls.tsv` — 5,142 AMRFinderPlus point-mutation-all records (includes silent variants)
- `work/mlst_results.tsv` — 68 MLST profiles under senterica_achtman_2 scheme
- `work/analyze.py`, `work/analyze_v2.py` — replication statistical analysis scripts
- `report/evidence/replication_summary.json` — v1 numeric summary
- `report/evidence/replication_summary_v2.json` — v2 (with corrected silent-variant filter)
- `report/evidence/judge_verdict.json` — LLM-judge (Argo GPT-5.2) verdict JSON
- `work/judge_prompt.md` — full evidence packet supplied to the judge

## No external artifacts we could not obtain
- Fig 6 BLAST-atlas visualizations (GView Server) were reproduced numerically (SGI-1 coverage per Typhimurium isolate), not visually.
- Heatmap software Heatmapper (Fig 5) — we tabulated the underlying counts in the JSON summary; heatmap not regenerated.
- No paywalled, restricted, or missing datasets encountered.
