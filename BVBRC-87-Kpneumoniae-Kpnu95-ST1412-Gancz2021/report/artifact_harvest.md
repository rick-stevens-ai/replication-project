# Artifact Harvest — BVBRC-87

All artifacts pulled from **free public sources**; no auth required except NCBI's polite-use rate limits.

## Paper

| Artifact | URL / accession | Size | Notes |
|---|---|---:|---|
| Full-text JATS XML | `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=PMC8151138&rettype=xml` | 169,234 B | Complete paper w/ tables, figure captions, refs, and data availability. Written to `work/paper.xml`. |
| PubMed summary | `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=34068663&retmode=json` | small | Confirms title, journal, DOI, PMID. |
| PMC linkout | `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&db=pmc&id=34068663` | small | Confirmed PMC8151138. |
| MDPI PDF | `https://www.mdpi.com/2076-2607/9/5/1022/pdf` | — | **Blocked** (Akamai edge Access Denied). PDF not necessary; XML sufficient. |
| PMC PDF | `https://pmc.ncbi.nlm.nih.gov/articles/PMC8151138/pdf/microorganisms-09-01022.pdf` | — | **Blocked** (returns interstitial HTML). |

## Sequence data

| Artifact | Source | Size | Notes / checksum |
|---|---|---:|---|
| BioProject `PRJNA494961` (KpnU95 WGS) | NCBI | — | Enumerated via `esearch db=assembly`. |
| Assembly `GCA_015714665.1 / ASM1571466v1` | NCBI Datasets REST | 2.9 MB zip → 5.3 MB fna | `datasets/v2alpha/genome/accession/GCA_015714665.1/download?include_annotation_type=GENOME_FASTA,PROT_FASTA,GENOME_GFF`. Scaffold-level, 61 contigs, 5,223,689 bp, 57.51% GC, 4952 protein records, 5063 CDS in GFF. |
| Plasmid MK552109.1 (pKpnU95) FASTA | NCBI eutils efetch | 182,943 B | 180,286 bp; single record; complete. Written to `work/pKpnU95.fasta`. |
| Plasmid MK552109.1 (pKpnU95) GenBank | NCBI eutils efetch | 400,111 B | 243 CDS, full feature table. Written to `work/pKpnU95.gb`. |
| PlasmidFinder DB `enterobacteriales.fsa` | `https://bitbucket.org/genomicepidemiology/plasmidfinder_db/raw/HEAD/enterobacteriales.fsa` | 80,757 B | 159 replicon sequences; used for IncFIB(K) typing. Written to `work/plasmidfinder_db/enterobacteriales.fsa`. |

## Software used (all free/OSS)

| Tool | Version | Where | Purpose |
|---|---|---|---|
| mlst | 2.35.0 (Torsten Seemann) | uicgpu `amr` env | 7-locus MLST for scheme `klebsiella` (PubMLST). |
| Kleborate | **3.2.4** (Holt lab) | uicgpu `/data/stevens/envs/kleborate` | Species/ST/K-O locus typing, AMR calling, virulence scoring, Ciprofloxacin MIC prediction. |
| BLAST+ blastn / makeblastdb | 2.16.x | uicgpu `amr` env | PlasmidFinder replicon BLAST. |
| Biopython | 1.87 | local | FASTA + GenBank parsing, assembly statistics, feature audit. |
| NCBI Datasets REST | v2alpha | public API | Assembly download. |
| NCBI eutils | current | public API | esearch/esummary/efetch/elink for BioProject → assembly → sequence. |

## Data-availability rating

**5 / 5.** Every artifact needed to test the paper's computational claims is publicly available with no auth or paywall (paper is CC-BY OA; assembly and plasmid are in NCBI Datasets / GenBank; DBs used for typing are all free/OSS). Wet-lab claims (nematode killing kinetics, growth curves in artificial urine, copper-tolerance doubling times) cannot be replicated from public artifacts but are secondary to the paper's central genomic/plasmid characterization.
