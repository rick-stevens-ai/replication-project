# Artifacts Summary — BVBRC-64 Lactobacillus reuteri PNW1

**Target:** BVBRC-64-lactobacillus-reuteri-pnw1
**Paper:** Alayande et al. 2020, PLoS ONE 15(7):e0235873 (DOI 10.1371/journal.pone.0235873, PMID 32687505)
**Assembly:** GCA_003790365.1 (GenBank live; GCF_003790365.1 RefSeq suppressed as "contaminated")
**Date:** 2026-07-03
**Verdict:** REPLICATED (strong)

## Directory layout

```
BVBRC-64-lactobacillus-reuteri-pnw1/
├── report/
│   ├── REPORT.md                # canonical markdown replication report (this run)
│   ├── REPORT.tex               # detailed LaTeX version incl. GENUINE CRITIQUE section
│   ├── open_questions.json      # 5 open-question objects (q / basis / next_steps)
│   ├── workflow.md              # end-to-end pipeline + concrete commands
│   ├── artifacts_summary.md     # this file
│   ├── failure_analysis.md      # what failed / what was partial / what was not testable
│   └── evidence/
│       ├── ncbi_datasets_report.json
│       ├── assembly_stats.json
│       ├── gene_search.json
│       ├── abricate_resfinder.tsv
│       ├── abricate_card.tsv
│       ├── abricate_ncbi.tsv
│       ├── abricate_argannot.tsv
│       ├── abricate_vfdb.tsv
│       ├── abricate_victors.tsv
│       ├── abricate_ecoli_vf.tsv
│       ├── abricate_plasmidfinder.tsv
│       └── minced_crispr.gff
├── extraction/                  # (empty for this target — no PDF OCR needed; genomic replication)
└── work/                        # transient: pnw1.zip + unpacked NCBI Datasets bundle
```

## Evidence artifacts (report/evidence/)

| File | Source tool | Role | Notes |
|---|---|---|---|
| `ncbi_datasets_report.json` | NCBI Datasets v2alpha REST | strain metadata provenance (C2) | 2 records for PNW1: GCA (live), GCF (suppressed) |
| `assembly_stats.json` | Python custom | assembly QC (C1) | contigs=420, total_bp=2,430,215, GC=38.98% (ATGC-only), Ns=189 |
| `gene_search.json` | Python regex on protein.faa | named-CDS presence (C3, C6) | arg-deiminase, D-2-hydroxyacid-DH, L-LDH, bacteriocin, transposases by family |
| `abricate_resfinder.tsv` | abricate + ResFinder | AMR (C4) | 2 hits: tet(W)_4, lnu(C)_1 |
| `abricate_card.tsv` | abricate + CARD | AMR (C4) | 2 hits: tet(W), lnuC |
| `abricate_ncbi.tsv` | abricate + NCBI-AMR | AMR (C4) | 2 hits: tet(W), lnu(C) |
| `abricate_argannot.tsv` | abricate + ARG-ANNOT | AMR (C4) | 2 hits: (Tet)tetW, (MLS)lnu(C) |
| `abricate_vfdb.tsv` | abricate + VFDB | virulence (C5) | 0 hits |
| `abricate_victors.tsv` | abricate + VICTORS | virulence (C5) | 0 hits |
| `abricate_ecoli_vf.tsv` | abricate + ecoli_vf | virulence (C5) | 0 hits |
| `abricate_plasmidfinder.tsv` | abricate + PlasmidFinder | plasmid rep (bonus, not in paper) | 1 hit: rep30_1_CDS22269(pLR581), 100%/100% |
| `minced_crispr.gff` | MinCED v0.4 | CRISPR (C6) | empty (0 arrays; assembly-fragmentation artifact) |

## Key headline numbers (from evidence, cross-referenced to paper)

| Claim | Paper | This replication | Source artifact |
|---|---|---|---|
| Genome length | 2,430,215 bp | 2,430,215 bp | assembly_stats.json |
| Contigs | 420 | 420 | assembly_stats.json |
| GC content | 39% | 38.98% (rounds to 39%) | assembly_stats.json |
| Sequencer | Illumina MiSeq | Illumina MiSeq | ncbi_datasets_report.json |
| Assembler | SPAdes | SPAdes v3.12.0 | ncbi_datasets_report.json |
| AMR genes | lnu(C), tet(W) | lnu(C), tet(W) (4/4 DBs) | abricate_{resfinder,card,ncbi,argannot}.tsv |
| Virulence factors | 0 hits | 0 hits (3/3 DBs) | abricate_{vfdb,victors,ecoli_vf}.tsv |
| Arginine deiminase | present (only "toxic-biochemical" enzyme) | present (ROV61345.1) | gene_search.json |
| L-lactate DH | present | 5 CDSs (ROV62718/63569/63627/63895/64206) | gene_search.json |
| D-lactate DH | present | 4 CDSs as "D-2-hydroxyacid DH" (PGAP family name) | gene_search.json |
| Helveticin J | present | 1 "bacteriocin, partial" CDS (ROV54067.1) | gene_search.json |
| IS families | 7 | ≥7 by name (IS3, IS5/1182, IS30, IS66, IS200/605, ISL3, IS21, ISLre2, IS1595) | gene_search.json |
| CRISPR arrays | 5 CRISPR CDSs each with Cas | 0 arrays (MinCED on fragmented assembly) | minced_crispr.gff |

## Independence check

- **AMR (C4):** quadruple-independent (ResFinder + CARD + NCBI-AMR + ARG-ANNOT), all databases refreshed 2026-07-03 — exact same 2 genes and nothing else.
- **Virulence (C5):** triple-independent (VFDB + VICTORS + ecoli_vf) — all 0 hits.
- **Assembly stats (C1):** exact reproduction from GenBank FASTA.
- **Provenance (C2):** exact reproduction from NCBI Datasets metadata.

## Non-reproducible items (flagged, not counted against the paper)

- **PHASTER** (paywalled service; used PGAP phage/integrase CDSs instead — 31 CDSs including a structural module).
- **PathogenFinder** (paywalled CGE service; used 3-DB VF-null result as proxy — consistent).
- **CRISPRFinder** (paper's tool; used MinCED as FOSS replacement — 0 arrays because assembly is fragmented, N50 ≈ 28 kb).
- **C7 wet-lab agar-well-diffusion vs STEC O177** (not reproducible in silico by construction).

## Total cost / wall time

- **Wall time on CherryRd:** ~3 minutes.
- **Compute:** local macOS only. No GPU. No HPC.
- **Paid endpoints:** 0.
- **Data:** open NCBI GenBank; all tools FOSS.
