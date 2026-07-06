# PROGRESS.md - Ríos et al. 2020 VREfm Replication
## Last updated: 2026-05-10 08:50 CDT

### Status: IN PROGRESS

### Steps completed:
1. ✅ Paper fetched (PDF + supplementary)
2. ✅ 55 ERV genome accessions identified from Supplementary Table 1
3. ⬜ Download genomes from NCBI
4. ⬜ MLST typing
5. ⬜ Pangenome analysis (Roary)
6. ⬜ Phylogeny (RAxML)
7. ⬜ AMR gene detection (ResFinder/BLAST)
8. ⬜ Recombination analysis (ClonalFrameML)
9. ⬜ Insertion sequence detection
10. ⬜ Claim testing
11. ⬜ REPORT.md

### Key facts from paper:
- 55 Latin American VREfm genomes (1998-2015, 5 countries)
- Core genome: 1,674 orthogroups (>90% presence)
- Pan-genome: 6,735 orthogroups
- Two main clades within Latin American isolates
- vanA cluster in 54/55 genomes
- All in global clade A
- Recombination: 54% of clade A genome

---

## RE-PASS 2026-06-23 (Pass 2)

### Steps completed in re-pass:
1. ✅ Pass-1 REPORT frozen at `report/REPORT.pass1.md`
2. ✅ `pdftotext` canonical re-parse of both PDFs; provenance in `PARSER_PROVENANCE.md`
3. ✅ Enumerated all testable LATAM-specific resistome/metadata claims from main text + Supp Tables
4. ✅ Single re-pass script `code/repass/repass_analysis.py` runs every test from existing abricate ResFinder/CARD/VFDB outputs + metadata
5. ✅ Secondary virulence tblastn script `code/repass/virulence_blast.py` (esp/hyl/acm/scm/sgrA/fms6/fms22/swpC/ptsD)
6. ✅ 19 new/cross-check claims tested (C16–C34), 17 VERIFIED + 2 PARTIAL
7. ✅ Identified 2 blockers (paper's custom virulence reference set; PBP5 training data) with specific named missing artifacts
8. ✅ REPORT.md updated in place with full 4-tier verdict table and coverage/agreement lifted from 6/22 to ~12/22

### Key new findings (TIER 1 exact matches in re-pass):
- Country distribution Col=40, Per=7, Ecu=3, Ven=3, Mex=2 — EXACT
- ant(6)-Ia in 49/55 = 89.1% — EXACT match to paper 89% (n=49)
- tet(L) in 9/55 = 16.4% — EXACT match to paper 16.3% (n=9)
- tet(S) in 1/55 = 1.8% — EXACT match to paper 1.8% (n=1)
- cat in exactly 3 Peruvian genomes (ERV121, ERV123, ERV125) — EXACT including country attribution
- optrA in ERV138 only — EXACT isolate-level match
- cfrB in ERV275 only — EXACT isolate-level match
- vanB absent in 0/55 — EXACT match to paper PCR result
- erm(B) 53/55 = 96.4%; aph(3')-III 50/55 = 90.9% — both consistent with paper-reported broad presence

### PARTIAL in re-pass (both attributed to abricate ≥80% threshold vs paper custom BLASTX):
- C20 aac(6')-aph(2'') 20/55 (36.4%) vs paper 49% (n≈27) — gap of 6–7 isolates from fragmented/partial hits
- C22 tet(M) 14/55 (25.5%) vs paper 43.6% (n=24) — gap of ~10 isolates from fragmented hits

### Coverage lift: 6/22 → 12/22, PARTIAL → SPOT-CHECK REPLICATED with explicit 4-tier verdict.

