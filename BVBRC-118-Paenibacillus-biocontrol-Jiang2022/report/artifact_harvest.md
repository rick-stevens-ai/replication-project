# Artifact Harvest — BVBRC-118

Every public artifact pulled during this replication, in fetch order.

| Fetch order | Artifact | URL | Bytes (as fetched) | Verified against |
|------------:|----------|-----|------------------:|------------------|
| 1 | `paper.pdf` (BMC Genomics OA) | https://bmcgenomics.biomedcentral.com/counter/pdf/10.1186/s12864-022-08330-0.pdf | 9,991,602 | DOI 10.1186/s12864-022-08330-0 |
| 2 | PubMed esummary for PMID 35209846 | https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=35209846&retmode=json | JSON | matches paper title + authors + PMC PMC8876185 |
| 3 | 16S rRNA sequence esummary (MK911741.1) | https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=nuccore&id=1644588792 | JSON | 1,461 bp, Paenibacillus peoriae strain HJ-2 |
| 4 | BioProject PRJNA580302 elink → SRA/BioSample | https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=bioproject&db=sra&id=580302 | XML | SRR10363117 |
| 5 | SRA esummary (SRX7071172 / SRR10363117) | https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=sra&id=9296566 | XML | 183,095 spots / 1,302,748,453 bp / PacBio Sequel |
| 6 | `SRR10363117.sra` | https://sra-pub-run-odp.s3.amazonaws.com/sra/SRR10363117/SRR10363117 | 329,222,294 | byte count matches SRA record |
| 7 | `GCF_002937395.1` P. peoriae IBSD35 genome (RefSeq) | https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/002/937/395/GCF_002937395.1_ASM293739v1/GCF_002937395.1_ASM293739v1_genomic.fna.gz | 1,758,533 (gz) / 5,941,734 (unpacked) | header contains `NZ_PTJM01000010.1 Paenibacillus peoriae strain IBSD35` |
| 8 | `GCF_001272655.2` P. peoriae HS311 genome (RefSeq) | https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/001/272/655/GCF_001272655.2_ASM127265v2/GCF_001272655.2_ASM127265v2_genomic.fna.gz | 1,858,767 (gz) / 6,297,727 (unpacked) | `NZ_CP011512.1 Paenibacillus peoriae strain HS311 chromosome, complete genome` |
| 9 | `GCF_014692735.1` P. peoriae ZF390 genome (RefSeq) | https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/014/692/735/GCF_014692735.1_ASM1469273v1/GCF_014692735.1_ASM1469273v1_genomic.fna.gz | 1,907,096 (gz) / 6,464,120 (unpacked) | `NZ_CP061172.1 Paenibacillus peoriae strain ZF390 chromosome, complete genome` |
| 10 | MIBiG BGC references (via antiSMASH knownclusterblast; local DB shipped with antismash 8.0.4) | (bundled) | (bundled ~3 GB DB) | BGC0000408.5, BGC0000449.5, BGC0000403.5, BGC0001152.5, BGC0001727.3, BGC0001356.4 all resolved |

Notes:
- `prefetch` via SRA-toolkit initially failed due to uicgpu HTTP proxy DNS resolution — pivoted to S3 direct fetch (also faster).
- All downloads used the standard uicgpu HTTP proxy (`http://<lan-host>:3128`) except the SRA S3 fetch which used the tailnet direct route (`NO_PROXY` list).
- No paywall crossed at any step (BMC Genomics is OA CC BY 4.0; SRA is public; NCBI RefSeq is public).
