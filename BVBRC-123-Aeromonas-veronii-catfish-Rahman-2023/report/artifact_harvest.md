# Artifact Harvest — BVBRC-123

| Artifact | Source URL | Local path (under work/ unless noted) | Size | Notes |
|---|---|---|---|---|
| Paper PDF | https://europepmc.org/articles/PMC10636080?pdf=render | `../paper.pdf` | 2,264,853 B | Europe PMC OA render; PMC direct returned HTML |
| Paper full text | pdftotext -layout on paper.pdf | `work/paper.txt` (570 lines) | ~29 KB | Clean layout extraction |
| Assembly (GenBank) | NCBI Datasets v2, `/genome/accession/GCA_026738955.1/download?include_annotation_type=GENOME_FASTA` | `work/assembly_dir/ncbi_dataset/data/GCA_026738955.1/GCA_026738955.1_ASM2673895v1_genomic.fna` | 4.56 MB | GenBank version (unannotated) |
| Assembly + annotation (RefSeq) | NCBI Datasets v2, `/genome/accession/GCF_026738955.1/download?include_annotation_type=GENOME_FASTA,GENOME_GFF,PROT_FASTA,CDS_FASTA` | `work/refseq_dir/ncbi_dataset/data/GCF_026738955.1/` | 3.81 MB zip | Includes PGAP-annotated genomic.fna, protein.faa, cds_from_genomic.fna, genomic.gff |
| Assembly report metadata | NCBI Datasets v2 | `work/assembly_report.json` | ~5 KB | Contains CheckM completeness, NCBI ANI check, WGS project accession |
| Reference: A. veronii TH0426 | NCBI Datasets v2, GCF_001593245.1 | `work/ref_GCF_001593245.1/.../GCF_001593245.1_ASM159324v1_genomic.fna` | 1.5 MB zip | Paper's "closest strain" |
| Reference: A. veronii B565 | NCBI Datasets v2, GCF_000204115.1 | `work/ref_GCF_000204115.1/.../GCF_000204115.1_ASM20411v1_genomic.fna` | 1.35 MB zip | Paper's "B56" - likely truncated name for B565 |
| Reference: A. veronii FDAARGOS_632 | NCBI Datasets v2, GCF_008693705.1 | `work/ref_argos/.../GCF_008693705.1_ASM869370v1_genomic.fna` | 1.34 MB zip | Same organism as NZ_CP044060.1 (paper's proteome-comparison ref) |
| PubMLST scan result | POST base64 FASTA to https://rest.pubmlst.org/db/pubmlst_aeromonas_seqdef/schemes/1/sequence | `work/pubmlst_result.json` | ~500 B | 5 exact allele matches, ppsA no exact |
| PubMLST ST 492 profile | https://rest.pubmlst.org/db/pubmlst_aeromonas_seqdef/schemes/1/profiles/492 | inline in notes | ~1 KB | Ground-truth for comparison |
| PubMLST all-profiles CSV | https://rest.pubmlst.org/db/pubmlst_aeromonas_seqdef/schemes/1/profiles_csv | in-memory | ~200 KB | 2,756 profiles scanned for ≥3-allele overlap |
| abricate CARD result | local: `abricate --db card` | `work/abricate_card.tsv` | ~1 KB | 3 hits |
| abricate ResFinder result | local: `abricate --db resfinder` | `work/abricate_resfinder.tsv` | ~1 KB | 2 hits |
| abricate NCBI AMRFinder result | local: `abricate --db ncbi` | `work/abricate_ncbi.tsv` | ~1 KB | 2 hits |
| abricate VFDB result | local: `abricate --db vfdb` | `work/abricate_vfdb.tsv` | ~40 KB | 130 unique gene hits (T3SS, adhesins, hemolysins) |
| abricate PlasmidFinder result | local: `abricate --db plasmidfinder` | `work/abricate_plasmidfinder.tsv` | header only | 0 replicons |
| skani triangle output | local: `skani triangle` | inline in `work/skani.log` | small | ANI matrix Alim_AV_1000 vs 3 refs |
| fastANI output | local: `fastANI -q ... --rl refs.txt` | `work/fastani.tsv` | small | Per-ref ANI + orthologous fragment counts |

## Accession errata found
- Paper states BioProject `PRJNA810265` — this actually points to *Pasteurella multocida* DC2020 by the same institution. Correct A. veronii Alim_AV_1000 BioProject is **PRJNA827572**.
- Paper states BioSample `SUB11126221` — this is a submission handle, not a BioSample accession. Correct BioSample is **SAMN27611687**.

## Databases used (versions/dates)
- NCBI Datasets v2 REST — accessed 2026-07-05 evening (CDT)
- PubMLST Aeromonas seqdef DB — last_updated 2026-06-24, records 4,061; scheme 1 has 2,756 STs
- abricate 1.4.0; all local DBs dated 2026-07-03 (CARD 6,052 seqs, ResFinder 3,206, VFDB 4,592, NCBI 8,232, PlasmidFinder 488)
- skani 0.3.2, fastANI 1.34
- Europe PMC OA render 2026-07-05
