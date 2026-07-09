# Artifact Harvest — BVBRC-73

All artifacts pulled from public, free sources on 2026-07-03.

## Paper artifacts
| Type | ID | Source | Size |
|------|----|--------|------|
| PubMed record | PMID 37969805 | NCBI E-utilities esummary | metadata |
| Full-text XML | PMC10636080 | NCBI E-utilities efetch (PMC) | 80,656 bytes → `work/paper.xml` |
| Journal DOI | 10.5455/javar.2023.j711 | Journal of Advanced Veterinary and Animal Research | — |

## Sequence data pulled
| Role | Strain / label | Accession | Source | Size (fna) |
|------|----------------|-----------|--------|-----------|
| Target genome | *A. veronii* Alim_AV_1000 (paper's isolate) | GCF_026738955.1 (WGS JALLKR01, BioProject PRJNA810265, BioSample SAMN27611687) | NCBI Assembly FTP | 4,559,891 B |
| Reference | *A. veronii* TH0426 (China catfish; paper's phylogenetic sister strain) | GCF_001593245.1 (chromosome NZ_CP012504.1) | NCBI Assembly FTP | 4,984,622 B |
| Reference | *A. veronii* B565 (Chinese catfish; paper's other cited sister strain) | GCF_000204115.1 (chromosome NC_015424.1) | NCBI Assembly FTP | 4,608,736 B |
| Reference | *A. veronii* FDAARGOS_632 (RefSeq reference strain; paper's proteome-comparison reference NZ_CP044060) | GCF_008693705.1 | NCBI Assembly FTP | 4,619,065 B |
| Species-boundary outgroup | *A. hydrophila* ATCC 7966 | GCF_000014805.1 | NCBI Assembly FTP | 4,803,835 B |
| Species-boundary outgroup | *A. salmonicida* subsp. salmonicida A449 | GCF_000196395.1 | NCBI Assembly FTP | 5,104,076 B |

## Reference databases queried
| DB | Version / date | Content |
|----|---------------|---------|
| CARD (via abricate 1.4.0) | 2026-Jul-03 | 6,052 AMR sequences |
| ResFinder (via abricate) | 2026-Jul-03 | 3,206 AMR sequences |
| NCBI AMR (via abricate) | 2026-Jul-03 | 8,232 sequences |
| ARGannot (via abricate) | 2026-Jul-03 | 2,224 sequences |
| MEGARes (via abricate) | 2026-Jul-03 | 6,635 sequences |
| VFDB (via abricate) | 2026-Jul-03 | 4,592 virulence-factor sequences |
| PlasmidFinder (via abricate) | 2026-Jul-03 | 488 plasmid replicons |
| PubMLST *pubmlst_aeromonas_seqdef* scheme 1 | queried live via REST API 2026-07-03 | 2,755 STs |

## Tool versions used
| Tool | Version | Purpose |
|------|---------|---------|
| skani | (Homebrew, latest) | ANI (species boundary check) |
| Prodigal | V2.60 (Oct 2011) | CDS calling |
| barrnap | 0.9 | rRNA calling |
| aragorn | (installed) | tRNA calling |
| abricate | 1.4.0 (Homebrew) | AMR + VF + plasmid scans |
| BLASTN | 2.17.0+ | (via abricate) |
| Biopython | 1.87 | genome stats |
| PubMLST REST API | live (2026-07-03) | MLST typing |

## LLM judges (free Argo proxy at 127.0.0.1:44497)
| Model alias | Role |
|-------------|------|
| argo:gpt-5.2 | Judge B |
| argo:claude-sonnet-4.5 | Judge D |
| argo:gemini-2.5-pro | Judge E |
| argo:gpt-4.1 | Judge F |
| argo:claude-opus-4.7 | ATTEMPTED — Argo upstream 502 (endpoint bug, not our error) |
| argo:claude-opus-4.8 | ATTEMPTED — Argo upstream 502 |

## Artifacts NOT pulled / attempted-and-blocked
| What | Why not |
|------|---------|
| PHASTER phage-region call | phaster.ca API rejected our POST (broken pipe on 4.5 MB submission — external service issue, not our error). Claim C12 marked SPOT-CHECK. |
| Raw Illumina reads | Not required — deposited assembly matches paper's size/GC/contigs essentially exactly. |
| Wet-lab AST cultures | Not reproducible from a genome rerun. |
