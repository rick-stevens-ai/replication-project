# Artifacts summary — BVBRC-68 pPA1011 blaKPC-2 replication

Root: `~/Dropbox/REPLICATE-PROJECT/BVBRC-68-pseudomonas-blakpc2-plasmid/`

## Report artifacts (`report/`)

| Artifact | Purpose | Verdict-supporting claims |
|----------|---------|---------------------------|
| `REPORT.md` | Human-readable narrative replication report (canonical) | C1–C6 (verdict: REPLICATED) |
| `REPORT.tex` | LaTeX version of REPORT.md with dedicated GENUINE CRITIQUE section | C1–C6 |
| `open_questions.json` | Five open scientific questions grounded in pPA1011 / KPC-2 plasmid biology, with basis and next steps | Post-replication follow-up |
| `workflow.md` | Stepwise procedural description of the replication | Method reproducibility |
| `artifacts_summary.md` | This file — index of every artifact used or produced | Traceability |
| `failure_analysis.md` | What did not work, what could not be tested, and why | Honest limits |
| `evidence/summary.json` | Machine-readable summary of all measurements and per-claim outcomes | C1–C6 |
| `evidence/blast_pPA1011_vs_p14057.tsv` | BLAST HSP table underlying the C5 novelty analysis | C5 |

## Input sequence artifacts (`work/seqs/`)

| Artifact | Source | Used for |
|----------|--------|----------|
| `pPA1011_MH734334.fna` | NCBI GenBank accession MH734334.1 | C1 length, C2 GC, C3 CDS extraction, C4 environment parsing, C5 BLAST query |
| `pPA1011_MH734334.gb`  | NCBI GenBank accession MH734334.1 | C4 feature parsing, C6 /note qualifier |
| `p14057_KY296095.fna`  | NCBI GenBank accession KY296095.1 | C5 BLAST subject (comparator plasmid) |
| `p14057_KY296095.gb`   | NCBI GenBank accession KY296095.1 | C5 comparator annotation |
| `pPA1011_blaKPC.fna`   | Excised 17,676–18,557 (+) of MH734334.1 (882 bp) | C3 translation input |
| `pKP048_KPC2.faa`      | Canonical KPC-2 reference (293 aa; == AZZ88873.1) | C3 alignment reference |

## BLAST artifacts (`work/blast/`)

| Artifact | Purpose |
|----------|---------|
| `p14057_db.*` | BLAST+ nucleotide database built from `p14057_KY296095.fna` (via `makeblastdb`) |
| `pPA1011_vs_p14057.tsv` | 19-HSP tabular BLAST output; source of the 82.15% coverage / 98.70% weighted-identity numbers in C5 |

## Prodigal artifacts (`work/prodigal/`)

| Artifact | Purpose |
|----------|---------|
| Prodigal CDS predictions on pPA1011 | Cross-check CDS coordinates against the submitter's GenBank annotation (sanity check only; GenBank features are canonical for C4) |

## Key numerical results (all from `evidence/summary.json`)

| Claim | Measurement | Source artifact |
|-------|-------------|-----------------|
| C1 | Length = 62,793 bp | `pPA1011_MH734334.fna` |
| C2 | GC = 58.78% | `pPA1011_MH734334.fna` |
| C3 | KPC-2 protein identity = 100.00% (293/293 aa) | `pPA1011_blaKPC.fna` translated → aligned to `pKP048_KPC2.faa` |
| C4 | blaKPC-2 CDS at 17,676–18,557 (+); flanking features consistent with paper schema | `pPA1011_MH734334.gb` feature table |
| C5 | Coverage vs p14057 = 82.15%; weighted identity = 98.70%; 19 HSPs | `work/blast/pPA1011_vs_p14057.tsv` |
| C6 | ST463 (provenance from /note qualifier) | `pPA1011_MH734334.gb` LOCUS metadata |

## What is NOT in this artifact set

- No raw Illumina NextSeq 500 or PacBio RSII reads (not deposited under an accessible SRA/ENA accession for this study).
- No independent isolate WGS assembly of PA1011 (not deposited; only the plasmid).
- No ISfinder / ISEScan output (would definitively type the "hypothetical protein" flanking ORFs as ISKpn8 / ISKpn6 / IS26; see `failure_analysis.md`).
- No corpus-wide BLAST vs all P. aeruginosa KPC plasmids (would properly bound C5; see `open_questions.json` Q1).
- No oriTfinder / MOB-suite conjugation-typing output (see `open_questions.json` Q3).

## Provenance chain

1. NCBI GenBank accessions MH734334.1 and KY296095.1 → deterministic by versioned accession.
2. FASTA / GenBank files → local `work/seqs/`.
3. Python-stdlib parsers + NCBI BLAST+ → measurements in `evidence/summary.json`.
4. `evidence/summary.json` → tables in `REPORT.md` / `REPORT.tex`.

All numbers reported in the two report files trace back to `evidence/summary.json`, which traces back to the deposited GenBank accessions.
