# Artifacts summary — Fang et al. (2018) replication

**Paper:** Fang X et al., *BMC Systems Biology* 12:66 (2018). DOI 10.1186/s12918-018-0587-5.
**Verdict:** PARTIAL REPLICATION (strong).
**Date:** 2026-06-27 (third pass, adds genomic-verification layer).

---

## Directory layout (`work/`)

```
work/
├── .venv/                        Python 3.14 venv: cobra 0.31.1, biopython 1.87
├── models/
│   ├── iML1515.json              2.9 MB — BiGG K-12 GEM (2712 rxn, 1877 met, 1516 gene)
│   └── iJO1366.json              2.8 MB — earlier BiGG K-12 GEM
├── genomes/
│   ├── GCA_000284495.1/          LF82 (B2 AIEC)   — 4,773,108 bp, 1 contig, 4,376 CDS, 50.70% GC
│   ├── GCA_000013265.1/          UTI89 (B2 UPEC)  — 5,179,971 bp, 2 contigs, 5,211 CDS, 50.61% GC
│   ├── GCA_000183345.1/          NRG857c (B2 AIEC) — 4,894,879 bp, 2 contigs, 4,582 CDS, 50.69% GC
│   └── GCF_000005845.2/          K-12 MG1655 (A)  — 4,641,652 bp, 1 contig, 4,300 CDS, 50.79% GC
├── blast/
│   ├── *_db.{nhr,nin,nsq}        nucleotide BLAST databases (4 strains)
│   ├── frl_query.faa             frlA/B/C/D/R K-12 reference proteins
│   ├── metabolic_query.faa       17-gene catabolism panel (K-12 reference)
│   ├── clermont_primers.fa       8 Clermont 2013 quadruplex primers
│   ├── *_frl.tsv                 tblastn raw hits (frl operon per strain)
│   ├── *_metabolic.tsv           tblastn raw hits (17-gene panel per strain)
│   └── frl_presence.json         presence/absence calls (pident≥70, cov≥70, e≤1e-30)
├── genome_stats.py / .json       Biopython assembly-stats driver + output
├── frl_blast.py                  central mechanism (C5) test
├── metabolic_survey.py / .json   17-gene sanity panel (C3)
├── clermont.py / clermont_results.json   independent phylogroup (C6)
├── fba_mucus.py / fba_results.json       mucus-glycan FBA (Fig. 3b, C4d)
├── fba_table1.py / table1_results.json   Table 1 substrates FBA (C4a–c)
└── paper.pdf                     Fang et al. 2018 open-access PDF (1.3 MB)
```

---

## Key result artifacts

| Artifact | Purpose | Key numbers |
|---|---|---|
| `genome_stats.json` | Assembly QC | LF82 4.77 Mb / UTI89 5.18 Mb / NRG857c 4.89 Mb / K-12 4.64 Mb — match published |
| `blast/frl_presence.json` | **Central C5 test** | **frl operon 0/5 in all 3 B2 refs; 5/5 in K-12** |
| `metabolic_survey.json` | Sanity check | 16/17 K-12 catabolism genes present in each B2 (≥96%); only frl lost |
| `clermont_results.json` | **C6 phylogroup** | 4/4 match paper (LF82/UTI89/NRG857c = B2, K-12 = A) |
| `table1_results.json` | **C4a–c FBA** | 6/8 substrates qualitatively match; 2 within paper variance |
| `fba_results.json` | **C4d FBA** | GlcNAc 1.131, Neu5Ac 1.479, L-fucose 0.862, D-gal 0.868, glucuronate 0.705; GalNAc alone = 0 |

---

## Raw inputs

| Source | Artifact | Auth? |
|---|---|---|
| NCBI Datasets v2alpha REST | 4 genome + protein FASTAs | Free, no auth |
| BiGG Models (UCSD) | iML1515.json, iJO1366.json | Free, no auth |
| Europe PMC REST | bibliographic + abstract | Free |
| BV-BRC public API | E. coli corpus count / strain lookup | Free |
| Fang et al. 2018 open-access PDF | `paper.pdf` (1.3 MB) | CC BY 4.0 |

---

## Tools invoked

- COBRApy 0.31.1 (GLPK default)
- BLAST+ 2.x: `makeblastdb`, `tblastn`, `blastn` (with `blastn-short` for primers)
- Biopython 1.87 (FASTA I/O)
- curl (NCBI Datasets download)
- Python 3.14 stdlib (`json`, `subprocess`)

---

## Numbers cross-referenced in REPORT.md

- **8/10 coverage, 10/10 agreement** on tested claims.
- **frl operon** absent in LF82/UTI89/NRG857c: weak hits at 19–29% identity (spurious cross-hits), all below the pident≥70 / cov≥70 orthology threshold; K-12 hits at 100% / 100%.
- **Clermont signatures** — LF82/UTI89/NRG857c all `+-+-` (chuA+, yjaA−, TspE4.C2+, arpA−) → B2; K-12 `-+-+` → A.
- **iML1515 growth rates (μ, h⁻¹)** — fructoselysine 0.893, psicoselysine 0.893, melibiose 1.770, L-xylulose 0.717, phenylpropanoate 1.131, xanthosine 1.023, XMP 1.023, cyanate+glucose 0.886; GlcNAc 1.131, Neu5Ac 1.479, L-fucose 0.862, D-galactose 0.868, D-glucuronate 0.705; GalNAc alone 0.000.
- **iJO1366 growth rates (μ, h⁻¹)** — fructoselysine 1.005, psicoselysine 1.005, melibiose 1.967, L-xylulose 0.806, phenylpropanoate 1.259, xanthosine 1.214, XMP 1.214, cyanate+glucose 0.993.

---

## Artifacts NOT produced (would be needed for full REPLICATED)

- 110-strain pan-genome matrix (Roary / PanX)
- Per-strain GEMs for 53 IBD isolates (CarveMe / KBase)
- 649-substrate × per-strain FBA growth panel (Fig. 3a)
- Fig. 1a heatmap regeneration
- IBD-53-isolate BV-BRC accession map
- SelectKBest 100-gene phylogroup-discriminative scoring
