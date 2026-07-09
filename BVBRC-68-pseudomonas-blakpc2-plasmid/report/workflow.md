# Workflow — BVBRC-68 pPA1011 blaKPC-2 replication

This document describes the end-to-end steps used to replicate Hu et al. 2019 (pPA1011 plasmid, GenBank MH734334.1). All work was performed inside `~/Dropbox/REPLICATE-PROJECT/BVBRC-68-pseudomonas-blakpc2-plasmid/` using free/public data only.

## 0. Inputs

Fetched (once, prior to the replication turn) into `work/seqs/`:

| File | Accession | Purpose |
|------|-----------|---------|
| `pPA1011_MH734334.fna` | MH734334.1 | Complete pPA1011 plasmid nucleotide sequence |
| `pPA1011_MH734334.gb`  | MH734334.1 | GenBank annotation (features, LOCUS metadata, /note qualifiers) |
| `p14057_KY296095.fna`  | KY296095.1 | Closest published *P. aeruginosa* KPC-2 comparator plasmid |
| `p14057_KY296095.gb`   | KY296095.1 | Comparator annotation |
| `pPA1011_blaKPC.fna`   | (excised)  | 882-bp blaKPC-2 CDS region excised from MH734334.1 |
| `pKP048_KPC2.faa`      | canonical  | Reference KPC-2 protein (293 aa), identical to AZZ88873.1 |

## 1. Stepwise procedure

### Step 1 — Verify plasmid length (C1)
- Read `work/seqs/pPA1011_MH734334.fna`.
- Sum sequence characters (strip header, whitespace, newlines).
- **Result:** 62,793 bp → exact match to paper.

### Step 2 — Compute GC content (C2)
- Count A/C/G/T (case-insensitive) across the FASTA.
- GC% = (G + C) / (A + C + G + T) × 100.
- **Result:** 58.78% → matches paper's 58.8% (within 0.02%).

### Step 3 — Extract and translate blaKPC-2 CDS (C3)
- Use CDS coordinates from the MH734334.1 feature table (17,676–18,557, forward strand) to excise the 882-bp region into `work/seqs/pPA1011_blaKPC.fna` (done previously; reused here).
- Translate all 6 reading frames using the standard bacterial genetic code (Python stdlib).
- Select the longest M…* ORF.
- Align position-by-position against `work/seqs/pKP048_KPC2.faa` (canonical 293-aa KPC-2).
- **Result:** 293/293 aa = 100.00% identity. Confirms paper's PCR-based blaKPC-2 call at the strictly stronger sequence level.

### Step 4 — Parse blaKPC-2 genetic environment (C4)
- Parse `pPA1011_MH734334.gb` feature table.
- Extract all CDS / mobile_element / repeat_region features within ±6 kb of the blaKPC-2 CDS (i.e., coordinates ~11,676 to ~24,557).
- Compare feature order / spacing to paper's schema: ΔIS6-Tn3-ISKpn8-blaKPC-2-ISKpn6-IS26.
- **Result:**
  - Tn3 resolvase 15,740–16,297 (+)
  - Hypothetical CDS 16,420–17,400 (ISKpn8 position)
  - blaKPC-2 17,676–18,557 (+)
  - Downstream hypothetical CDSs 18,807–20,289 (ISKpn6 / IS26 positions)
  - KlcA 20,417–20,842
  - → structurally consistent with paper (submitter annotates several IS ORFs generically as "hypothetical protein").

### Step 5 — Backbone novelty vs prior KPC plasmid (C5)
- Reuse existing BLAST+ output at `work/blast/pPA1011_vs_p14057.tsv` (19 HSPs).
- BLAST command that produced it (for record):
  ```
  makeblastdb -in work/seqs/p14057_KY296095.fna -dbtype nucl -out work/blast/p14057_db
  blastn -query work/seqs/pPA1011_MH734334.fna \
         -db work/blast/p14057_db -task megablast \
         -outfmt "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore qlen slen" \
         -out work/blast/pPA1011_vs_p14057.tsv
  ```
- Aggregate:
  - Union of covered query positions on pPA1011 = 51,587 bp.
  - Query-side coverage = 51,587 / 62,793 = **82.15%**.
  - Length-weighted mean % identity across the 19 HSPs = **98.70%**.
- **Result:** Backbone novelty claim only weakly supported; pPA1011 is best described as a p14057-family variant with ~11.2 kb (~18%) of pPA1011-unique / rearranged content.

### Step 6 — MLST call (C6)
- Read `/note="genotype: ST463"` qualifier from LOCUS metadata of MH734334.1.
- **Result:** ST463 recorded as provenance-only (no isolate WGS on SRA for independent re-typing).

### Step 7 — Emit machine-readable summary
- Write `report/evidence/summary.json` with per-claim measurements, tests, and match status.
- Copy `work/blast/pPA1011_vs_p14057.tsv` to `report/evidence/blast_pPA1011_vs_p14057.tsv`.

### Step 8 — Write human-readable report
- `report/REPORT.md` — narrative report with claims table, results-vs-paper table, verdict, caveats.
- `report/REPORT.tex` — LaTeX version with dedicated GENUINE CRITIQUE section.

## 2. Determinism note

All numeric claims (C1–C4) derive from a specific NCBI accession (MH734334.1). Sequence content is deterministic by versioned accession, so re-running the workflow on any host at any date will produce byte-identical FASTA and identical downstream numbers.

## 3. Tooling

- Python 3 (system stdlib only) — parsing, translation, GC counting, alignment.
- NCBI BLAST+ (installed on host) — `makeblastdb`, `blastn -task megablast`.
- `grep`/`awk` — GenBank feature parsing.
- No paid endpoints, no proprietary libraries, no network access required during the replication turn (all input files pre-fetched).

## 4. Reproducibility

- Fixed inputs (versioned GenBank accessions).
- Stdlib-only Python analysis (no pip installs).
- All command lines and outputs recorded in the terminal transcript and in `report/evidence/summary.json`.
- To re-run: re-fetch MH734334.1 and KY296095.1 by accession, re-run BLAST with the command above, re-execute the stdlib Python analyses on the resulting FASTA/GenBank files.
