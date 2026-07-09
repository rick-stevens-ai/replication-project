# Artifact Harvest — BVBRC-75

All artifacts fetched fresh over the public internet, no auth required (except polite S2 header, not used here).

| Artifact | URL / Source | Size | Purpose |
|---|---|---|---|
| Full-text XML | https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7168644/fullTextXML | 134 KB | Paper text (Europe PMC OA API) |
| RefSeq assembly metadata | NCBI E-utils esummary for assembly UID 8406111 | ~2 KB | Confirmed GCF_015208815.1 / GCA_015208815.1, WGS project VWTQ01, SKESA 2018-09-01, MiSeq 99x coverage |
| H2730R genome FASTA | ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/015/208/815/GCF_015208815.1_ASM1520881v1/GCF_015208815.1_ASM1520881v1_genomic.fna.gz | 1.5 MB gz | Assembly nucleotide sequence (58 contigs, 5.29 Mbp) |
| H2730R PGAP GFF | .../GCF_015208815.1_ASM1520881v1_genomic.gff.gz | 488 KB gz | RefSeq PGAP annotation for feature counts + gene names |
| H2730R CDS FASTA | .../GCF_015208815.1_ASM1520881v1_cds_from_genomic.fna.gz | 1.7 MB gz | Coding-sequence set |
| H2730R protein FAA | .../GCF_015208815.1_ASM1520881v1_protein.faa.gz | 1.1 MB gz | Protein set (unused here) |
| Assembly stats | .../GCF_015208815.1_ASM1520881v1_assembly_stats.txt | 3.8 KB | contig/N50/L50/GC canonical values |
| Reference plasmid p18-43_01 | NCBI E-utils efetch db=nuccore id=CP023554.1 rettype=fasta | 217 KB | Comparison plasmid for BLAST |
| PubMLST *C. freundii* MLST profiles | https://rest.pubmlst.org/db/pubmlst_cfreundii_seqdef/schemes/1/profiles_csv | ~15 KB (1250 STs) | ST498 profile lookup + in silico typing |
| PubMLST allele FASTAs (7 loci) | https://rest.pubmlst.org/db/pubmlst_cfreundii_seqdef/loci/{arcA,aspC,clpX,dnaG,fadD,lysP,mdh}/alleles_fasta | 100–240 KB each | Local BLAST-based MLST calling of H2730R genome |

## Verified identifiers
- Paper: PMID 32024012 · PMC7168644 · DOI 10.3390/pathogens9020089
- Assembly: GCF_015208815.1 (RefSeq) = GCA_015208815.1 (GenBank) · WGS VWTQ01 · ASM1520881v1 · submitted 2020-11-02 by U KwaZulu-Natal
- BioSample SAMN12706440 · BioProject PRJNA564235
- Comparison plasmid: CP023554.1 = p18-43_01 (212,326 bp, *K. pneumoniae*, Pedersen et al. 2018)
- MLST database: PubMLST *C. freundii* scheme 1 (1,250 STs as of 2026-07-03)
