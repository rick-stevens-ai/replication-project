# Workflow, tools, and effort estimate — BVBRC-120

## Workflow (chronological)

1. **Locate paper.** PMID 37337195 → esummary → DOI 10.1186/s12866-023-02907-9 → PMC PMC10278307. Confirmed correct paper (a first attempt fetched the wrong Zhang 2023 paper — see failure_analysis.md).
2. **Fetch full PDF.** Via `curl -sL -A "Mozilla/5.0" -o paper.pdf "https://bmcmicrobiol.biomedcentral.com/counter/pdf/10.1186/s12866-023-02907-9.pdf"` from uicgpu (through the <lan-host>:3128 proxy).
3. **Fetch all 9 supplementary XLSX files** from `static-content.springer.com/esm/art%3A10.1186%2Fs12866-023-02907-9/MediaObjects/12866_2023_2907_MOESM{1..9}_ESM.xlsx`.
4. **Extract accessions.** `openpyxl` used to parse S1 (178 host strains), S4 (20 focal lytic phages), S9 (236 lytic-phage accessions) into CSV.
5. **Download 236 lytic phage genomes.** `efetch -db nuccore -id ... -format fasta` in batches of 50 into a single FASTA. Result: 231/236 (5 dropped by NCBI dedup).
6. **Download 20 focal lytic phages.** 7 already in the 231-set; 13 missing (mostly RefSeq NC_* vs GenBank pairs) — fetched separately → 20/20 recovered.
7. **Genome-level stats.** `seqkit stats` + `seqkit fx2tab --name --length --gc` on both sets.
8. **All-vs-all genome distance.** MASH sketch per-genome + `mash dist` all-pairs. 231×231 → 53,361 rows; 20×20 → 400 rows.
9. **ORF prediction.** Prodigal `-p meta` on concatenated 231-set and 20-set FASTA → 35,069 and 2,497 proteins respectively.
10. **Protein clustering.** MMseqs2 `mmseqs cluster --min-seq-id 0.3 -c 0.5` on both proteomes.
11. **Phylogeny (20 focal).** Whole-genome MAFFT alignment attempted, abandoned after 4 min on divergent panel; replaced with rapidnj BIONJ tree from 20-genome MASH distance matrix.
12. **Analytics.** Python (pandas, numpy) to compute distribution statistics, protein-cluster size histograms, and JSON summaries.
13. **Report + LaTeX + supporting docs** written in `report/`.
14. **Marker + Nougat parses** run in parallel on uicgpu for extraction/ dir.

## Tools & code

| Tool | Version | Used for | Env / how installed |
|---|---|---|---|
| entrez-direct (`efetch`) | 22.4 | Download 236+13 genomes from NCBI nuccore | bvbrc76 conda (miniforge3, bioconda) |
| seqkit | 2.13.0 | Genome length/GC/stats, per-genome split | bvbrc76 |
| MASH | 2.3 | All-vs-all genome sketch + distance | mamba install -c bioconda mash |
| prodigal | 2.6.3 | ORF/protein prediction (`-p meta`) | bvbrc76 |
| MMseqs2 | 13.45111 | Protein clustering at 30% id / 50% cov | mamba install -c bioconda mmseqs2 |
| MAFFT | 7 (bundled) | Whole-genome nt alignment (abandoned) | bvbrc76 |
| IQ-TREE | 3.1.2 | Installed for phylogeny; final tree used rapidnj instead | mamba install -c bioconda iqtree |
| rapidnj | 2.3.2 | BIONJ tree from 20-genome MASH matrix | mamba install -c bioconda rapidnj |
| openpyxl | 3.0 | Parse 9 supplementary XLSX to CSV | pip / bvbrc76 |
| pandas, numpy | 1.3 / 1.21 | Summary stats + histograms | pip in bvbrc76 |
| pdftotext | poppler 22 | PDF → text (for local verification) | macOS Homebrew poppler |
| Marker | 0.2 (data/stevens/envs/marker) | Full-paper Markdown extraction | Pre-existing conda env on uicgpu |
| Nougat | 0.1 (gpustor nougat) | Full-paper LaTeX-flavour extraction | Pre-existing conda env on uicgpu |
| shell scripts | — | download.sh, phase2.sh, phase3.sh, fetch_missing.sh | Written for this replication |

Scripts written for this replication (in `work/` mirror on uicgpu `/data/stevens/bvbrc120/`):
- `download.sh` — batch efetch of 236 accessions
- `fetch_missing.sh` — recover the 13 missing focal phages with correct proxy env
- `phase2.sh` — planned MMseqs2 + prodigal + MAFFT + IQ-TREE run (MAFFT stalled, killed)
- `phase3.sh` — final analytics + rapidnj tree + MMseqs2 on 20-phage subset
- `analyze.sh` — combined orchestrator (initial version, superseded by phase2/phase3)

## Effort estimate

| Category | Effort |
|---|---|
| Wall-clock end-to-end | ~28 min (agent runtime, incl. Marker/Nougat parses running in parallel) |
| Compute (uicgpu) | efetch ~90 s · prodigal ~15 s · MMseqs2 ~10 s · mash all-pairs ~5 s · rapidnj <1 s · Marker ~7 min · Nougat ~9 min |
| Human/agent decision steps | ~14 (paper fix, tool install, proxy fix, killed-MAFFT decision, tree-method swap, etc.) |
| Lines of code written | ~360 (7 shell scripts + inline Python) |
| Independent runs executed | ~11 (download batches × 5, prodigal ×2, mmseqs ×2, mash ×2, rapidnj ×1) |
| Data downloaded | ~22 MB genomes + 10 MB paper PDF + 145 KB supplementary XLSX |
| Report/documents authored | REPORT.md (~15 KB), REPORT.tex (~14 KB), brief.md, attempt_log.md, artifact_harvest.md, workflow.md, artifacts_summary.md, failure_analysis.md, open_questions.json (5 questions) |
