# Workflow — BVBRC-36 (González-Escalona et al. 2019, STEC nanopore plasmid AMR)

## Replication workflow (as executed)

1. **Paper + accessions** — Europe PMC full text (`PMC6667211/fullTextXML`); accessions extracted by regex. bioRxiv/DuckDuckGo were Cloudflare-blocked; Europe PMC + Crossref resolved cleanly.
2. **Genome acquisition** — NCBI efetch of 7 CP replicons (CP037941–CP037947) via nuccore FASTA (free, no auth).
3. **Genome stats** — `work/genome_stats.py` (length + GC per replicon).
4. **AMR + virulence + plasmid screen** — `work/run_blast.py`: `makeblastdb` per replicon; `blastn` each reference gene DB against each replicon; abricate default thresholds (≥80% id, ≥80% qcov).
   - Reference DBs (abricate-format nucleotide FASTA): ResFinder (3,206 seqs), VFDB (4,592), ecoli_vf/EcOH (2,701, STEC-specific), PlasmidFinder (488, Inc replicons).
   - Allele-level hits collapsed to gene symbols by best identity (`work/summarize.py`).
5. **MLST** — `work/mlst.py` against PubMLST *Escherichia* seqdef Achtman scheme #1 (adk fumC gyrB icd mdh purA recA); required exact 100% full-length allele match; ST looked up in 16,242-row profile table.
6. **Stx location** — `work/stx_location.py`: blastn stx A/B subunits vs each chromosome; compare to paper Table 8 windows.
7. **Verdict** — LLM-judge over structured claim-vs-result comparison; free Argo endpoint (opus 502'd → fell back to argo:gpt-5.2 per brief). No regex scoring.

## Tools / codes used

| Tool | Role | Cost |
|---|---|---|
| Europe PMC REST | Full text + accession extraction | Free |
| Crossref | Preprint↔journal linkage | Free |
| NCBI efetch (nuccore) | 7 complete-genome FASTAs | Free, no auth |
| ENA portal API | SRA read metadata | Free |
| BLAST+ 2.x (`makeblastdb`, `blastn`) | Sequence homology | Free |
| abricate reference DBs (ResFinder/VFDB/ecoli_vf/PlasmidFinder) | AMR/VF/plasmid gene refs | Free |
| PubMLST *Escherichia* seqdef Achtman scheme | 7-locus MLST | Free |
| Biopython 1.87 | Sequence handling | Free |
| Argo `argo:gpt-5.2` (free proxy) | LLM-as-judge | Free |
| Local scripts: `run_blast.py`, `summarize.py`, `mlst.py`, `genome_stats.py`, `stx_location.py`, `judge.py` | Analysis + scoring | Free |

## Compute footprint

- Wall-clock: ~5 min laptop CPU end-to-end.
- Extensions from open_questions.json (raw-read re-assembly Q1, PHASTER Q2, plasmid mobility Q3) each add 4-8 h uicgpu compute.
