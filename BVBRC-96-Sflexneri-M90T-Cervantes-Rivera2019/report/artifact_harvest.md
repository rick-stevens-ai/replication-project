# Artifact harvest — BVBRC-96

## Paper
- **Cervantes-Rivera R, Tronnet S, Puhar A.** "Complete genome sequence and annotation of the
  laboratory reference strain *Shigella flexneri* serotype 5a M90T and genome-wide transcriptional
  start site determination." *BMC Genomics* 21:285 (2020).
- DOI: [10.1186/s12864-020-6565-5](https://doi.org/10.1186/s12864-020-6565-5)
- PMID: 32252626 · PMC: PMC7132871
- OA: ✅ CC BY 4.0

## Public artifacts pulled

| URL / accession | What | Size / metric | Provenance |
|---|---|---|---|
| `https://api.ncbi.nlm.nih.gov/datasets/v2/genome/accession/GCF_004799585.1/dataset_report` | Assembly report JSON | 4.4 KB (`work/assembly_report.json`) | NCBI Datasets REST v2, free/no-auth |
| `https://api.ncbi.nlm.nih.gov/datasets/v2/genome/accession/GCF_004799585.1/download?include_annotation_type=GENOME_FASTA,GENOME_GFF,PROT_FASTA,SEQUENCE_REPORT` | Full genome package | 2,695,927 bytes (`work/genome.zip`); FASTA MD5 `b42e8cb5771af766febc5a841847ed3e` | NCBI Datasets REST v2 |
| RefSeq **NZ_CP037923.1** | Chromosome | 4,596,714 bp | included in package |
| RefSeq **NZ_CP037924.1** | Plasmid pWR100 | 232,195 bp | included in package |
| Assembly **GCF_004799585.1 / ASM479958v1** | Complete Genome, Umeå submitter, released 2019-04-18, BioProject PRJNA510559 | 2 replicons, GC 50.5% | NCBI Assembly |
| GCF_000006925.2 | *S. flexneri* 2a 301 (comparator) | 4.83 Mbp | NCBI Datasets |
| GCF_000013585.1 | *S. flexneri* 5b 8401 (comparator; paper's previous ref) | 4.57 Mbp | NCBI Datasets |
| GCF_000092525.1 | *S. sonnei* Ss046 (comparator) | 5.06 Mbp | NCBI Datasets |
| GCF_000012005.1 | *S. dysenteriae* Sd197 (comparator) | 4.56 Mbp | NCBI Datasets |
| GCF_000012025.1 | *S. boydii* Sb227 (comparator) | 4.65 Mbp | NCBI Datasets |
| GCF_000005845.2 | *E. coli* K-12 MG1655 (outgroup) | 4.64 Mbp | NCBI Datasets |

## Tools used
- NCBI Datasets REST v2 (free)
- abricate 0.5 + PlasmidFinder (263-seq DB, 2017-03-19) + VFDB + CARD + ResFinder DBs
- Prokka (available, not re-run — used deposited PGAP annotation)
- BLAST+ 2.x
- mash 2.3
- fastANI (available)
- Python 3 / Biopython (feature parsing)
- Argo proxy (localhost:44497, key `stevens`) for LLM judge — free CELS endpoint

## Sibling replication (referenced, NOT overwritten)
- `~/Dropbox/REPLICATE-PROJECT/BVBRC-54-Sflexneri-M90T-genome-Cervantes2020/` — prior independent
  replication of the same paper, verdict PARTIAL (strong). This replication (BVBRC-96) was executed
  independently with a fresh data pull and a distinct emphasis on the BVBRC-96 workflow class
  (PlasmidFinder + Similar Genome Finder + Specialty Genes + CGA), and converges on the same
  conclusion via independent artefacts.
