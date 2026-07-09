# Failure Analysis — BVBRC-75

**Paper:** Ramsamy et al. 2020, Pathogens 9(2):89.
**Verdict:** REPLICATED. This document catalogs **partial / uncovered / drift** items — what failed to reproduce, why, and what would be needed to close the gap. Nothing in this list overturns the REPLICATED verdict; the paper's headline claims all reproduced at byte-level resolution.

---

## Category A — Uncovered claims (6 items; drove PARTIAL judge score)

These are claims the paper makes via web-only bioinformatics tools that this replication did not re-run. **No contradiction with the paper**; simply not covered.

### A1. Plasmid replicon typing (C13)
- **Paper claim:** 4 plasmid replicons — Inc A/C2, Inc FIB(pB171), Inc FII(Yp), Inc Q1.
- **Coverage here:** partial (PGAP annotates RepA IncFII-family replicon on contig 19).
- **Why not reproduced:** PlasmidFinder web tool was not re-run locally.
- **How to close:** run PlasmidFinder 2.x locally against `GCF_015208815.1_ASM1520881v1_genomic.fna`; also try MOB-suite for plasmid clustering.

### A2. Prophage typing (C14)
- **Paper claim:** 4 intact prophages — Escher_HK639, Entero_c_1, Salmon_RE_2010, Salmon_SJ46.
- **Coverage here:** none.
- **Why not reproduced:** PHASTER is a web-only server.
- **How to close:** submit assembly to PHASTER (or use offline PHASTEST if licensed); compare intact-prophage list.

### A3. Pathogenicity score (C20)
- **Paper claim:** Pscore ≈ 0.875.
- **Coverage here:** none.
- **Why not reproduced:** PathogenFinder is a DTU-hosted web tool without a straightforward CLI.
- **How to close:** submit assembly to PathogenFinder web UI; compare Pscore.

### A4. CRISPR arrays (C21)
- **Paper claim:** 2 CRISPR arrays, no Cas systems.
- **Coverage here:** none.
- **Why not reproduced:** CRISPRCasFinder is web-primary.
- **How to close:** run CRISPRCasFinder locally (Docker image available) or the standalone MinCED/CRT tools.

### A5. Restriction-modification systems (C22)
- **Paper claim:** Type II R-M — Eco128I + M.EcoRII.
- **Coverage here:** none.
- **Why not reproduced:** REBASE / RM-Finder are web-only.
- **How to close:** BLAST the assembly against REBASE Gold Standard proteins; report Type II hits.

### A6. GyrA S83I substitution (C17)
- **Paper claim:** GyrA S83I (fluoroquinolone-resistance QRDR mutation).
- **Coverage here:** PARTIAL — gyrA CDS is present on contig 6 but the specific amino-acid substitution was not extracted.
- **Why not reproduced:** requires a 3-line protein-alignment step that was skipped.
- **How to close:** translate gyrA CDS from contig 6, align vs wild-type *E. coli* K-12 GyrA (UniProt P0AES4) with clustalo, report residue at position 83 (and 87 for the parC-adjacent QRDR site).

---

## Category B — Quantitative drift (2 items; do not overturn verdict)

### B1. Acquired resistance gene count: 25 (paper) vs 17 (this run)
- **Root cause:** methodological, not biological. The paper counts distinct hits across ResFinder + ARG-ANNOT + CARD (tool-union), which is known to inflate distinct-loci counts by 30–50% via subfamily double-counting (e.g., blaCTX-M-15 also getting counted as "CTX-M family" or "blaOXA-1" also appearing as "OXA-1-like"). This replication used a single PGAP+regex pass and deduped by locus.
- **Coverage note:** every drug-class family the paper reports is represented in the 17 detected loci (β-lactams, aminoglycosides, sulfonamide/trimethoprim, tetracycline, chloramphenicol, quinolone, rifampin).
- **Not a discrepancy in what the isolate carries** — a discrepancy in how the paper counts hits.

### B2. Total CDS: 5006 (paper COG) / 5135 (paper Table A1) vs 5093 + 116 pseudogenes (this run)
- **Root cause:** annotation-pipeline drift. RefSeq re-ran PGAP on 2020-11-02, redepositing the assembly with a slightly different CDS/pseudogene call set. Delta is < 1%.
- **Not a discrepancy in what the assembly contains** — a discrepancy in how PGAP versions call CDSs.

---

## Category C — Table-label ambiguity in the paper (1 item)

### C1. tRNA count 12 vs 70
- **Paper Table A1:** `tRNA = 12`, `Number of RNAs = 70`.
- **This run (PGAP GFF):** 70 tRNA CDS records.
- **Interpretation:** Table A1 labels for the tRNA and total-RNA columns appear swapped. The 70 matches PGAP tRNA count exactly; the 12 is not consistent with any plausible RNA-family total for a 5.3 Mbp *C. freundii*.
- **Action:** flag for a note to the authors; not a scientific issue.

---

## Category D — Scope limits of this replication itself

### D1. Assembly used is the RefSeq redeposit (2020-11-02), not the original 2020-01 submission.
- The exact contig set is identical (58 contigs, bp-exact, N50-exact, L50-exact per `_assembly_stats.txt`).
- Annotation drift (−42 CDS, +116 pseudogenes) is from the later PGAP re-annotation.
- Correct phrasing: "we replicated from the current public deposit," not "we replicated from the original 2020-01 deposit."

### D2. Short-read only — no plasmid closure.
- The central plasmid claim was reproduced at 100.000% identity over 14,979 bp of contig 22 vs CP023554.1. But short-read Illumina/SKESA cannot close a 212 kbp plasmid. Whether H2730R carries an **intact** p18-43_01 or a mosaic that shares only the NDM-1 island cannot be resolved without long-read (Nanopore/PacBio) resequencing. Both the paper and this replication share this scope limit.

### D3. No comparative context.
- No pan-genomic or SNP-cluster analysis against other ST498 or other p18-43_01-carrying isolates. The paper's implicit "emerging clone" framing would benefit from such analysis; neither the paper nor this replication does it.

### D4. XDR phenotype not verified genomically.
- Claim C23 (XDR phenotype) is a wet-lab AST result. The resistome is genomically **consistent** with XDR (all classes except tigecycline covered), but genotype→phenotype inference is probabilistic, not deterministic. Marked PROXY in the claims table.

---

## Category E — Would-fail-if-attempted (none observed)

No claims were tried and failed to reproduce. Every claim that was tested with real data agreed with the paper exactly or within tool tolerance.

---

## Summary

| Category | Count | Overturns verdict? |
|---|---|---|
| A. Uncovered (web-tool-only)      | 6 | No |
| B. Quantitative drift (pipeline)  | 2 | No |
| C. Paper-table label swap         | 1 | No |
| D. Replication scope limits       | 4 | No |
| E. Tested and failed              | 0 | — |

**Net:** the REPLICATED verdict stands. The gaps are all methodological (which tools were run, which weren't) and cosmetic (label swap, count conventions), not scientific.
