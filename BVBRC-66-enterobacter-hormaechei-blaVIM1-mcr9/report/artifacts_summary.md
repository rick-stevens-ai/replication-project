# Artifacts Summary — BVBRC-66 (Sadek 2020, *E. hormaechei* blaVIM-1 + mcr-9)

Inventory of every input dataset, reference DB, deposited assembly, and derived file consumed or produced by this replication.

---

## 1. Paper artifacts

| Artifact | Value | Source |
|---|---|---|
| DOI | 10.3390/pathogens9090687 | MDPI Pathogens |
| PMID | 32842587 | NCBI PubMed |
| PMC | PMC7558541 | NCBI PMC |
| License | CC BY 4.0 | Open access |
| Report date | 2026-07-02 | This session |

## 2. Isolate / deposited assembly (input)

| Item | Accession / value | Notes |
|---|---|---|
| BioSample | SAMN14534668 | Strain EGYMCRVIM ("MS37") |
| Collection date | 2017-07-15 | Qena, Egypt (25.41°N 32.39°E) |
| Isolation source | Beef burger / uncooked beef patty | Food chain sample |
| Depositor | Mustafa Sadek | Corresponding author group |
| RefSeq assembly | GCF_013265685.1 | Complete hybrid assembly |
| Chromosome | CP053190.1 | ~4.67 Mb, circular |
| Plasmid pMS-37a | CP053191.1 | **270,915 bp, IncHI2/IncHI2A** — carries both blaVIM-1 and mcr-9 |
| Plasmid pMS-37b | CP053192.1 | 129,016 bp, IncC (+IncA) |
| Plasmid pMS-37c | CP053193.1 | 108,277 bp, IncFIB(pHCM2) |
| Plasmid pMS-37d | CP053194.1 | 6,851 bp, Col(pHAD28) |
| Genome total size | 5,188,211 bp | Sum of 5 replicons |
| Assembly method | hybrid Unicycler v0.4.7 @ 165× | GenBank header of CP053191.1 |
| SRA record | SRR11478637 | ⚠️ Placeholder — 5 spots/5.2 Mb (assembly length recorded as "bases"); raw reads NOT deposited |
| Nanopore reads | — | Not deposited |

## 3. Reference databases (input)

| DB | Version | URL / access | Use |
|---|---|---|---|
| PubMLST *E. cloacae* complex, scheme 1 (7 loci) | Live pull, 2026-07-02 | `rest.pubmlst.org/db/pubmlst_ecloacae_seqdef/schemes/1` | MLST call |
| PubMLST allele counts | dnaA=772, fusA=560, gyrB=809, leuS=967, pyrG=734, rplB=388, rpoB=521 (total 4,751) | Same | MLST call |
| PubMLST ST profile table | 3,292 profiles | Same | ST lookup (ST279) |
| ResFinder DB (`all.fsa`) | HEAD, 2026-07-02 | Bitbucket cge/resfinder_db | AMR gene detection |
| PlasmidFinder DB (`enterobacteriales.fsa`) | HEAD, 2026-07-02 | Bitbucket cge/plasmidfinder_db | Inc typing |
| IS1 canonical | V00609.1 (768 bp, *E. coli*) | NCBI nuccore | IS1 flanking BLAST |
| IS903 canonical | MK479294.1 (1,209 bp, *K. pneumoniae* IS903 tnpA + mgrB region) | NCBI nuccore | IS903 flanking BLAST |
| QseB protein | NP_417497.1 (*E. coli* K-12, ~219 aa) | NCBI protein | tblastn regulator search |
| QseC protein | NP_417498.1 (*E. coli* K-12, ~449 aa) | NCBI protein | tblastn regulator search |

## 4. Software / tools

| Tool | Version | Use |
|---|---|---|
| NCBI E-utilities (`esearch`, `elink`, `efetch`) | current | Metadata + FASTA retrieval |
| BLAST+ | 2.17 (local) | All homology searches |
| `makeblastdb` | 2.17 (local) | DB build for each replicon and combined genome |
| Python 3 | system | Region-clustering / best-hit-per-locus reduction |
| Argo LLM proxy | 127.0.0.1:44497 (free, standing rule) | Final LLM-judge pass |
| Judge model | Claude Sonnet 4.6 (Opus 4.8/4.7 both 502'd on the prompt) | Score aggregation only |

## 5. Derived / output files (this replication)

Under `~/Dropbox/REPLICATE-PROJECT/BVBRC-66-enterobacter-hormaechei-blaVIM1-mcr9/`:

| Path | Content |
|---|---|
| `report/REPORT.md` | Primary markdown report — full claim table + method + verdict |
| `report/REPORT.tex` | LaTeX version + dedicated GENUINE CRITIQUE section |
| `report/open_questions.json` | 5 truly open biological questions grounded in E. hormaechei blaVIM-1 + mcr-9 biology |
| `report/workflow.md` | 9-stage pipeline recipe |
| `report/artifacts_summary.md` | This file |
| `report/failure_analysis.md` | Where the replication is weak / what would strengthen it |
| `report/evidence/summary.json` | Structured claim-vs-evidence table (LLM judge input) |
| `report/evidence/llm_judge.json` | Claude Sonnet 4.6 verdict JSON |
| `extraction/` | Paper extraction artifacts (marker) |
| `work/` | Intermediate BLAST outputs, filtered tables, per-locus best-hit CSVs (workspace; not authoritative) |

## 6. Key numbers to cross-reference

| Metric | Paper | This replication |
|---|---|---|
| Sequence type | ST279 | **ST279** (7/7 loci at 100%/100%) ✅ |
| pMS-37a size | 270.9 kb | **270,915 bp** ✅ |
| pMS-37a Inc | IncHI2 / pMLST1 | **IncHI2 + IncHI2A at 100% id** ✅ |
| Genes on pMS-37a | 8 (blaVIM-1, aac(6')-Il, dfrA1, ΔaadA22, sul1, tetA, aac(6')-Ib-cr, mcr-9) | **All 8 present**; 6 at 100%/100%; tetA 95%; dfrA1 99.79% ✅ |
| mcr-9 upstream flanker | IS903 | **IS903 at 87.6% id, 133 bp 5' of mcr-9** ✅ |
| mcr-9 downstream flanker | IS1 | **IS1 at 99.87% id, 4 bp 3' of mcr-9** ✅ |
| Plasmid qseB/qseC | Absent | **Absent on pMS-37a** (chromosomal true copies present) ✅ |
| Total assembled genome | ~5.2 Mb | **5,188,211 bp** ✅ |
| Coverage | (paper: hybrid Illumina + Nanopore) | 165.0× per GenBank header ✅ |

## 7. Provenance chain

Paper → PubMed metadata → BioSample SAMN14534668 → BioProject → Assembly GCF_013265685.1 → 5 nuccore replicons CP053190–CP053194.1 → local FASTA → local BLAST DBs → BLAST against PubMLST/ResFinder/PlasmidFinder/IS canonicals/QseBC → per-claim evidence table → LLM judge → verdict.

Every step above is publicly re-runnable without authentication, without paid services, and (modulo DB HEAD drift) byte-deterministic.
