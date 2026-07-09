# Artifact Harvest — BVBRC-35

## Paper
| Item | Source | Notes |
|---|---|---|
| Full text (PDF) | https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0215038&type=printable | 3.73 MB, `work/paper.pdf` |
| Full text (XML) | https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6464166/fullTextXML | 168 KB, `work/fulltext.xml` — used for claim extraction |

## Genomes (NCBI Datasets v2 REST + nuccore efetch — free, no auth)
| Strain | Accession used | Downloaded size | Role |
|---|---|---:|---|
| PA34 (chromosome) | GCF_003332705.2 (= CP032552) | 6,810,079 bp | subject |
| PA34 plasmid pMKPA34-1 | MH547560.1 | 95,404 bp | subject |
| PA34 plasmid pMKPA34-2 | MH547561.1 | 26,862 bp | subject |
| PAO1 | GCF_000006765.1 | 6,264,404 bp | reference |
| PA14 (UCBPP-PA14) | GCF_000014625.1 | 6,537,648 bp | reference |
| VRFPA04 | GCF_000473745.2 | 6,818,030 bp | reference (Indian eye isolate) |

Datasets endpoint: `https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/accession/<ACC>/download?include_annotation_type=GENOME_FASTA,PROT_FASTA,GENOME_GFF`
Plasmids: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=<ACC>&rettype=fasta`

## Tools / databases (uicgpu)
| Tool | Version | Env |
|---|---|---|
| Prokka | 1.12 | /data/stevens/envs/bvbrc28 |
| Roary | 3.12.0 | /data/stevens/envs/bvbrc28 |
| abricate | (bvbrc14) — DBs: ResFinder 3206, CARD 6052, VFDB 4592 (2026-Apr) | /data/stevens/envs/bvbrc14 |
| mlst | (bvbrc14), paeruginosa scheme | /data/stevens/envs/bvbrc14 |

## Generated evidence (report/evidence/)
- roary_summary_statistics.txt, roary_venn.json, genome_stats.json
- PA34_resfinder.tsv, PA34_card.tsv, PA34_vfdb.tsv, amr_summary.txt, PA34_mlst.tsv
- llm_judge_verdict.txt

## Compute footprint
uicgpu:/data/stevens/pa34_repl/ — full Prokka + Roary intermediates (gene_presence_absence.csv, core alignment, per-strain GFFs). Compressed matrix mirrored to work/roary_out/gene_presence_absence.csv.gz.
All LLM inference: free Argo proxy (argo:gpt-5.2) only. No paid endpoints used.
