# Artifacts summary — BVBRC-84

## Deposited-artifact keys
- **BioProject:** PRJNA766157
- **BioSample:** SAMN21619988
- **GenBank (INSDC):** CP084221.1
- **RefSeq:** NZ_CP084221.1
- **Assembly:** GCF_022810665.1
- **BV-BRC genome_id:** 33959.595
- **SRA:** none (esearch db=sra term=SAMN21619988 → count=0 — this is the C12 blocker)

## Local artifact tree (~/Dropbox/REPLICATE-PROJECT/BVBRC-84-ljohnsonii-7409N31/)

```
BVBRC-84-ljohnsonii-7409N31/
├── report/
│   ├── REPORT.md                        long-form Markdown replication report
│   ├── REPORT.tex                       LaTeX version + GENUINE CRITIQUE section
│   ├── brief.md                         1-paragraph what/why
│   ├── attempt_log.md                   chronological log of the replication turn
│   ├── artifact_harvest.md              every URL / accession pulled
│   ├── workflow.md                      step-by-step workflow (this backfill)
│   ├── artifacts_summary.md             this file
│   ├── failure_analysis.md              honest limitations + failure modes
│   ├── open_questions.json              5 genuinely open scientific questions
│   └── evidence/
│       ├── llm_judge.json               Argo argo:gpt-5.2 verdict JSON
│       └── independent_reproduction/
│           ├── comparison.md            full independent comparison narrative
│           ├── indep_summary.json       raw independent numbers
│           ├── tool_versions.txt        Python 3.14.6, curl 8.7.1, prodigal V2.60,
│           │                            barrnap 0.9, abricate 1.4.0, datasets 18.25.1
│           ├── code/
│           │   └── indep_reproduce.py   single-file reproducer
│           └── downloads/
│               ├── ncbi_dataset.zip     fresh NCBI Datasets pull + extracted tree
│               ├── CP084221_indep.gb    fresh efetch GenBank for LOCUS metadata
│               ├── prodigal_predictions.gff, .faa    ab initio CDS
│               ├── barrnap_bac.gff                   ab initio rRNA
│               ├── abricate_card.tsv                 0 hits
│               ├── abricate_resfinder.tsv            0 hits
│               ├── abricate_ncbi.tsv                 0 hits
│               ├── abricate_vfdb.tsv                 0 hits
│               ├── abricate_plasmidfinder.tsv        0 hits
│               ├── bvbrc_patric_facet_indep.json    live PATRIC feature type facets
│               ├── bvbrc_refseq_facet_indep.json    live RefSeq feature type facets
│               ├── bvbrc_rrna_details.json          24 rRNA features (PATRIC — 12×5S + 12×16S only)
│               └── bvbrc_carb_indep.json            30 Carbohydrate subsystem entries
└── work/
    ├── CP084221.fasta                   2.23 MB deposited sequence
    ├── CP084221.gb                      5.12 MB GenBank record with PGAP annotation
    ├── NZ_CP084221.gb                   RefSeq CON record
    ├── paper.xml                        PMC10640944 JATS XML
    ├── annot_report.json                NCBI Datasets v2 annotation_report (RefSeq)
    ├── bvbrc_genome.json                BV-BRC /genome API result
    ├── bvbrc_facet.json                 /genome_feature facet, all annotations
    ├── bvbrc_patric_facet.json          /genome_feature filtered to annotation=PATRIC
    ├── bvbrc_subsys_facet.json          subsystem faceting
    ├── bvbrc_metab.json                 metabolism subsystem
    ├── bvbrc_carb.json                  carbohydrate subsystem
    └── feature_count.txt.gz             (404 HTML content, unused — FTP attempt)
```

## Key numeric artifacts (single-line summary)
- Length: **2,198,442 bp** (matches paper exactly)
- GC: **35.0094%** (matches paper's 35.01%)
- CDS (PATRIC 2026): **2,235** (+13 vs paper's 2,222 — annotation drift)
- CDS (prodigal ab initio): 2,147
- CDS (RefSeq PGAP 2026): 2,117
- rRNA (PATRIC): 24 (matches paper; biologically incomplete — misses 12×23S)
- rRNA (barrnap): 36
- rRNA (RefSeq PGAP): 36
- ncRNA (PATRIC misc_RNA): 3 (matches paper)
- tRNA (PATRIC): 112 (matches paper)
- Topology: 1 circular chromosome, LOCUS = circular BCT (matches paper)
- Platform: PacBio RSII (matches paper)
- Assembly: HGAP v.3, 1886.5× coverage (matches paper)
- AMR / VF / plasmid: 0 hits across 5 abricate databases

## Tool provenance
- Python 3.14.6, stdlib only
- curl 8.7.1
- NCBI Datasets CLI v18.25.1
- prodigal V2.60 (single mode)
- barrnap 0.9 (bacterial kingdom)
- abricate 1.4.0 (all DBs revision 2026-Jul-03)
- Argo proxy `http://127.0.0.1:44497/v1`, model argo:gpt-5.2 (fallback from argo:claude-opus-4.7 and 4.8, both 502 on the judge payload)

## Non-artifact status
- Raw PacBio RSII reads — NOT deposited (SAMN21619988 has count=0 in SRA).
- HGAP v.3 config — NOT reported by paper.
- Functional validation of carbohydrate hydrolase claim — NOT performed by paper or this replication.
