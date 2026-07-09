# Artifact Harvest — BVBRC-66

All artifacts are public, free-to-download, no auth (except keychain-stored S2 key, unused here).

## Paper / metadata

| Artifact | URL / Accession | Size | Notes |
|---|---|---|---|
| Paper PMID 32842587 | https://pubmed.ncbi.nlm.nih.gov/32842587/ | text | Sadek et al. 2020, *Pathogens* 9:687, CC BY 4.0 |
| Paper DOI | https://doi.org/10.3390/pathogens9090687 | HTML/PDF | Open access, MDPI |
| Paper PMC | PMC7558541 | text/HTML | full text mirror |

## Sequencing metadata

| Artifact | Accession | Notes |
|---|---|---|
| BioProject | PRJNA622990, PRJNA630061 | Study + WGS project |
| BioSample | SAMN14534668 | strain EGYMCRVIM (a.k.a. EGYMCRVIM37, "MS37"), beef burger, Egypt: Qena, 25.41°N 32.39°E, 2017-07-15, coll. Mustafa Sadek |
| RefSeq Assembly | GCF_013265685.1 (ASM1326568v1) | Genome-wide assembly (labeled "Contig" but replicons are actually complete circular molecules; NCBI mis-classification) |
| SRA Experiment | SRX8054778 (Study SRP255191) | Illumina MiniSeq WGS |
| SRA Run | SRR11478637 | ⚠️ only 5 spots / 5,188,211 bases — placeholder/dummy record, raw reads effectively not usable |

## Deposited genome (all 5 replicons, downloaded)

| Accession | Size (bp) | Description | Local file |
|---|---:|---|---|
| CP053190.1 | 4,673,152 | chromosome, circular complete | work/genome/CP053190.1.fasta (4,739,994 B) |
| CP053191.1 | 270,915 | plasmid pMS-37a (IncHI2, harbours blaVIM-1 + mcr-9 + 6 more AMR genes) | work/genome/CP053191.1.fasta (274,875 B) + CP053191.1.gb (4,558 lines) |
| CP053192.1 | 129,016 | plasmid pMS-37b (IncC) | work/genome/CP053192.1.fasta (130,949 B) |
| CP053193.1 | 108,277 | plasmid pMS-37c (IncFIB(pHCM2)) | work/genome/CP053193.1.fasta (109,913 B) |
| CP053194.1 | 6,851 | plasmid pMS-37d (Col(pHAD28) partial) | work/genome/CP053194.1.fasta (7,038 B) |
| **TOTAL** | **5,188,211** | full deposited genome | work/genome/EGYMCRVIM_full.fasta (5,262,769 B) |

## Reference databases (cloned to work/dbs/)

| DB | URL | Version fetched | Contents used |
|---|---|---|---|
| ResFinder DB | https://bitbucket.org/genomicepidemiology/resfinder_db | HEAD (git-cloned depth-1, 2026-07-02) | `all.fsa` (all AMR gene alleles) |
| PlasmidFinder DB | https://bitbucket.org/genomicepidemiology/plasmidfinder_db | HEAD (git-cloned depth-1, 2026-07-02) | `enterobacteriales.fsa` (Inc-typing replicon reference alleles) |
| PubMLST *E. cloacae* complex MLST scheme | https://rest.pubmlst.org/db/pubmlst_ecloacae_seqdef/schemes/1 | 2026-07-02 snapshot (rolling data lock to 2024-12-31 for anon) | 3,292 profiles; 4,751 allele sequences across 7 loci (dnaA, fusA, gyrB, leuS, pyrG, rplB, rpoB) |

## Reference sequences (fetched via NCBI efetch)

| Purpose | Accession | Length | Local file |
|---|---|---:|---|
| IS1 canonical | V00609.1 | 768 bp | work/is_elements/V00609.1.fasta |
| IS903 canonical (containing tnpA) | MK479294.1 | 1,209 bp | work/is_elements/MK479294.1.fasta |
| qseB protein (E. coli K-12) | NP_417497.1 | ~219 aa | work/qs/qseB.faa |
| qseC protein (E. coli K-12) | NP_417498.1 | ~449 aa | work/qs/qseC.faa |

## LLM judge

| Model | Endpoint | Cost |
|---|---|---|
| argo:claude-sonnet-4.6 (fallback after Opus 4.8 and 4.7 both 502'd) | http://127.0.0.1:44497/v1/chat/completions (Argo proxy, key=stevens) | FREE (per standing rule) |
