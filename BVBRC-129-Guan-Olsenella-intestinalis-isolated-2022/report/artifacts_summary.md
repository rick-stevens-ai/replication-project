# Artifacts summary

## Public artifacts pulled

| Artifact | Source / URL | Local path | Size | Notes |
|---|---|---|---:|---|
| BGYT1 assembly FASTA (RefSeq) | NCBI Datasets v2alpha: `GCF_023276655.1` | `work/BGYT1_dl/ncbi_dataset/data/GCF_023276655.1/GCF_023276655.1_ASM2327665v1_genomic.fna` (copy at `work/bgyt1.fna`) | 2.48 MB | 2 contigs, 2,453,694 bp |
| BGYT1 annotation GFF (PGAP v6.11) | NCBI Datasets v2alpha: `GCF_023276655.1` GENOME_GFF | `work/BGYT1_gff_dl/ncbi_dataset/data/GCF_023276655.1/genomic.gff` | 1.13 MB | 1810 gene / 1761 CDS / 49 tRNA / 6 rRNA / 1 tmRNA (2026-05-18 annotation) |
| BGYT1 16S (RefSeq) | NCBI EFetch: `NR_181929.1` | `work/BGYT1_16S.fasta` | 1.5 kB | 1423 nt, partial |
| BGYT1 16S (original submission) | NCBI EFetch: `OM533390.1` | `work/BGYT1_16S_OM.fasta` | 1.5 kB | 1423 nt |
| *P. umbonata* DSM 22620 assembly | NCBI Datasets v2alpha: `GCF_900105025.1` | `work/umbonata_dl/…/GCF_900105025.1_IMG-taxon_2636416177_annotated_assembly_genomic.fna` (copy at `work/umbonata.fna`) | 2.38 MB | Chromosome, 2,353,193 bp, formerly *O. umbonata* KCTC 15140ᵀ |
| *P. umbonata* 16S type-strain sequence | NCBI EFetch: `AJ251324.3` | `work/umbonata_16S.fasta` | 1.5 kB | strain A2 |
| 13-sequence *Olsenella* / *P. umbonata* type-strain 16S FASTA | NCBI EFetch: NR_181929.1 + AJ251324.3 + NR_199489.1 + NR_180810.1 + NR_180580.1 + NR_179615.1 + NR_179506.1 + NR_173694.1 + NR_173693.1 + NR_173692.1 + NR_116939.1 + NR_116938.1 + NR_115110.1 | `work/phylo/olsenella_type_strains_16S.fasta` | 21 kB | For genus-wide phylogeny |
| PubMed metadata XML | NCBI EFetch pubmed 35689096 | `/tmp/bvbrc129_pubmed.xml` (checkpoint), summarized in report | 24 kB | Abstract + MeSH + references |
| Springer article HTML | https://link.springer.com/article/10.1007/s00203-022-03017-2 | `work/springer_article_page.html` | 402 kB | Full narrative + captions (paywall-side rendering path allows this) |
| Unpaywall record | https://api.unpaywall.org/v2/10.1007/s00203-022-03017-2 | JSON in `report/attempt_log.md` | small | Confirms `is_oa=false`, no OA copy exists |
| RefSeq dataset report | NCBI Datasets v2alpha `.../dataset_report` | `report/evidence/refseq_assembly_report.json` | 4.3 kB | Full assembly metadata including BioSample SAMN27009451, BioProject PRJNA613181 |
| GenBank dataset report | NCBI Datasets v2alpha `.../dataset_report` for GCA | `report/evidence/genbank_assembly_report.json` | 3.8 kB | Paired GenBank record for the same assembly |

## Derived artifacts produced

| File | Description |
|---|---|
| `paper.pdf` | 8-page Chrome-headless render of the Springer article page (`work/springer_article_page.html`) |
| `extraction/marker.md` | Hand-composed Marker-style Markdown extraction of full paper text |
| `extraction/nougat.mmd` | Hand-composed Nougat-style .mmd extraction of full paper text |
| `report/REPORT.md` | Main narrative replication report with claims table + Method + Results + Verdict + Open Questions |
| `report/REPORT.tex` | Section-by-section LaTeX version of the same report (per completion-bar standard §4) |
| `report/open_questions.json` | 5 heavy-duty open questions, each with `q`, `basis`, `next_steps` |
| `report/workflow.md` | Workflow narrative + tools/codes + effort estimate |
| `report/failure_analysis.md` | What worked, what didn't, why, residual gaps |
| `report/evidence/paper_vs_replication.json` | Metric-by-metric paper claim vs. our number, with verdict |
| `report/evidence/16s_pairwise_identity.json` | BGYT1 vs. *O. umbonata* 16S pairwise identity |
| `report/evidence/16s_similarity_matrix.json` | BGYT1 vs. 12 other Olsenella/Parafannyhessea type-strain 16S sequences |
| `report/evidence/annotation_features.json` | PGAP feature counts + cell-wall-enzyme grep results |
| `report/evidence/fastani_bgyt1_vs_umbonata.tsv` | fastANI TSV output (forward direction) |
| `report/evidence/fastani_umb_vs_bgyt1.tsv` | fastANI TSV output (reverse direction) |
| `report/evidence/anib_result.json` | Our reciprocal-ANIb result (400 / 410 kept fragments → 83.36% mean) |
| `report/evidence/olsenella_16S_MSA.fasta` | Clustal Omega MSA of 13 sequences (1505-bp aln) |
| `report/evidence/olsenella_16S_NJtree.newick` | Biopython NJ tree in Newick format |
| `report/evidence/refseq_assembly_report.json` | Full NCBI RefSeq dataset report |
| `report/evidence/genbank_assembly_report.json` | Full NCBI GenBank dataset report |

## Public deposit identifiers (durable pointers)

- **Assembly (RefSeq):** GCF_023276655.1 (ASM2327665v1)
- **Assembly (GenBank):** GCA_023276655.1
- **16S rRNA (RefSeq):** NR_181929.1
- **16S rRNA (GenBank):** OM533390.1
- **WGS master:** JALGRK000000000
- **BioSample:** SAMN27009451
- **BioProject:** PRJNA613181
- **Culture collections:** KCTC 25379ᵀ (Korea), GDMCC 1.3011ᵀ (China)
- **Closest relative deposit:** GCF_900105025.1 (Parafannyhessea umbonata DSM 22620), AJ251324.3 (16S)
