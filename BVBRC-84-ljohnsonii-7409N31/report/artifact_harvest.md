# BVBRC-84 artifact harvest

All resources fetched 2026-07-03 from live NCBI E-utils / NCBI Datasets API / BV-BRC data API. All are publicly available with no auth.

## Paper
- **PMID:** 37970500 · **DOI:** 10.5187/jast.2022.e98 · **PMCID:** PMC10640944
- **JATS XML full text** — `work/paper.xml` — 32,120 bytes — fetched via `efetch.fcgi?db=pmc&id=PMC10640944&rettype=xml`

## Deposited genome
- **GenBank accession:** CP084221.1 (INSDC, original submitter annotation, 2022-04-04)
- **RefSeq accession:** NZ_CP084221.1 (RefSeq re-annotation, currently 2026-05-18 by PGAP v6.11)
- **Assembly:** GCF_022810665.1 (RefSeq) / GCA_022810665.1 (GenBank), assembly name `ASM2281066v1`
- **BioProject:** PRJNA766157 (GenBank) / PRJNA224116 (RefSeq umbrella)
- **BioSample:** SAMN21619988
- **Organism/strain:** *Lactobacillus johnsonii* strain 7409N31, taxid 33959

## Fetched files (in `work/`)
| File | Bytes | Source |
| --- | --- | --- |
| CP084221.fasta | 2,229,929 | `efetch.fcgi?db=nuccore&id=CP084221.1&rettype=fasta` |
| CP084221.gb | 5,123,283 | `efetch.fcgi?db=nuccore&id=CP084221.1&rettype=gb` |
| NZ_CP084221.gb | 3,178 | `efetch.fcgi?db=nuccore&id=NZ_CP084221.1&rettype=gb` (CON record; features not inline) |
| paper.xml | 32,120 | `efetch.fcgi?db=pmc&id=PMC10640944&rettype=xml` |
| bvbrc_genome.json | see below | `https://www.bv-brc.org/api/genome/?eq(strain,7409N31)&select(...)` |
| bvbrc_facet.json | see below | `https://www.bv-brc.org/api/genome_feature/?eq(genome_id,33959.595)&facet(...)` |
| bvbrc_patric_facet.json | see below | same, filtered to `annotation=PATRIC` |
| bvbrc_subsys_facet.json / bvbrc_metab.json / bvbrc_carb.json | see below | `https://www.bv-brc.org/api/subsystem/?eq(genome_id,33959.595)&facet(...)` |
| annot_report.json | ~4 MB | `https://api.ncbi.nlm.nih.gov/datasets/v2/genome/accession/GCF_022810665.1/annotation_report?annotation_source_type=refseq` |

## Raw sequencing reads
- **NOT DEPOSITED.** SRA search for BioSample SAMN21619988 and for the strain name returned 0 hits (`esearch.fcgi?db=sra&term=SAMN21619988` → count=0). This is the reason full de novo re-assembly is blocked. Common gap for "complete genome announcement" papers pre-2020.

## Key data pulls (verbatim from API)
- BV-BRC `/api/genome`: `{"genome_id":"33959.595","genome_name":"Lactobacillus johnsonii 7409N31","genome_length":2198442,"gc_content":35.00943,"cds":2235,"patric_cds":2235,"trna":112,"rrna":24,"contigs":1,"assembly_method":"HGAP v. 3","sequencing_platform":"PacBio RSII"}`
- BV-BRC `/api/genome_feature?annotation=PATRIC` facet counts: CDS=2235, tRNA=112, repeat_region=49, rRNA=24, misc_binding=6, regulatory=5, misc_RNA=3, misc_feature=3
- CP084221.gb `##Genome-Annotation-Data##` block reports (PGAP-2021): Genes total=2250, CDSs=2100, rRNAs=36 (12+12+12), tRNAs=111, ncRNAs=3, Pseudo=72
- CP084221.gb `##Genome-Assembly-Data##` block: Assembly Method=HGAP v. 3, Coverage=1886.5×, Platform=PacBio RSII
