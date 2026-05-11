# Progress Log: BVBRC-10 — *L. lactis* LL16 (Milerienė 2023)

## 2026-05-10 08:55 CDT — REPORT COMPLETE

**Status:** REPORT.md written with full per-claim verification and verdict.

### Summary
- **Paper:** Milerienė et al. (2023), DOI 10.3390/microorganisms11041034
- **Verdict:** PARTIAL
- **Claims:** 34 total, 28 tested (82.4%), 21 verified, 7 partial, 0 contradicted, 6 not tested
- **Genome accession:** GCF_029912225.1 (2,473,617 bp, 372 contigs, 35.55% GC)
- **Key discrepancy:** Deposited assembly 4.5% smaller than paper's reported genome size (NCBI contamination filtering)
- **Method:** NCBI PGAP annotation used instead of paper's Prokka; web-only tools (ResFinder, BAGEL4, antiSMASH, etc.) not locally available

### Work Done
1. Downloaded genome assembly (GCF + GCA) and PGAP annotation from NCBI
2. Computed genome statistics (BioPython): size, GC, contigs, N50
3. Extracted all testable claims from paper (abstract + sections 3.1-3.3 of Results)
4. Searched PGAP GFF3/protein annotations for all key genes:
   - Safety: AMR genes, virulence factors, biogenic amine genes
   - Probiotic: gadB/C, bsh, efTu, cspA, fbp, F0F1 ATPase, LPXTG, sortases
   - Functional: L-lactate dehydrogenase, folate/riboflavin biosynthesis, proteases
   - Secondary metabolites: bacteriocin genes, PKS regulator
   - Mobile elements: IS transposases, plasmid replication/mobilization genes, CRISPR-Cas
5. Built BLAST databases and ran reference protein searches (earlier phase)
6. Wrote comprehensive REPORT.md with 34-claim comparison table

### NOT_TESTED Items (with reasons)
- RAST subsystem count (tool-specific, no PGAP equivalent)
- OrthoANI similarity (web-only tool)
- PathogenFinder probability (web-only tool)
- Enterolysin A (requires BAGEL4, web-only)
- KEGG pathway analysis (BlastKOALA, web-only)
- GABA production in milk (wet-lab experiment)
- Antibacterial activity (wet-lab experiment)
