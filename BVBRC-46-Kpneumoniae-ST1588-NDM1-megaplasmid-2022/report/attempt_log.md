# Attempt Log — BVBRC-46

Analyst: Ollie (OpenClaw AI), subagent. Date: 2026-07-01/02 (CDT).

1. **Dedup check.** `ls ~/Dropbox/REPLICATE-PROJECT/ | grep -iE "ST1588|megaplasmid|NDM"` → only `BVBRC-09-blaNDM5-K-pneumoniae-Yuan2019` (blaNDM-**5**, different paper/plasmid). No dir for THIS ST1588 NDM-1 megaplasmid paper. Proceeded.
2. **Read brief + exemplar.** `WAVE_BRIEF_2026-07-01.md` + `BVBRC-17-.../report/REPORT.md` (structure/claims-table template).
3. **Paper ID (free, Europe PMC).** Query resolved to **PMC9494972**, DOI 10.3390/antibiotics11091207, Antibiotics 2022 11(9):1207, CC-BY. Pulled abstract + full-text XML (`fulltextXML`, 88 KB). No `pdf`/`image` tools used (endpoint discipline).
4. **Extracted accessions from full text.** WGS `JAMJQY000000000` / version `JAMJQY010000000`; plasmid pNDM-1_UCO361 = `JAMJQY010000002.1` (314,976 bp); comparison plasmid pNDM-1-EC12 = `NZ_MN598004.1`; Raoultella megaplasmid `CP041388`.
5. **Resolved assembly.** eutils esearch on `db=assembly term=JAMJQY01` → UID 12842011 → **GCF_023554495.1 / GCA_023554495.1** (BioSample SAMN28534325).
6. **Downloaded assembly.** NCBI Datasets v2alpha REST (free, no auth): GENOME_FASTA + PROT_FASTA + CDS + GENOME_GFF. (First attempt failed: `GFF3` is not a valid `include_annotation_type` value → used `GENOME_GFF`.) 5.2 MB zip, md5 988216d6…
7. **Confirmed contig inventory.** 15 contigs. Contig 2 (`NZ_JAMJQY010000002.1`) = pNDM-1_UCO-361 at **exactly 314,976 bp**; contig 3 (`…000003.1`) = **exactly 197,209 bp**; contig 1 = 5,288,551 bp chromosome. Split each to its own FASTA; copied to uicgpu `/data/stevens/bvbrc46-kpneu-st1588/`.
8. **uicgpu env recon.** `bvbrc28` had datasets/prokka/blast but NOT mlst/amrfinder/abricate. Found `bvbrc14` (mlst, amrfinder, abricate) and `kleborate` (kleborate v3.2.4 + amrfinder + abricate). Used both.
9. **Kleborate (kpsc preset).** First run downloaded DBs. Result: **ST1588**, KL108, O1αβ,2β, resistome NDM-1/CTX-M-15/OXA-1/SHV/aac/qnr/oqx/sul2/dfrA14. All match paper.
10. **PlasmidFinder (abricate).** Megaplasmid → repHI5B_pC39 + repFIB_pC39 (hybrid, no clean canonical Inc = "un-typeable" nuance). Contig3 → **IncFIB(K)** (matches). Chromosome → none.
11. **ResFinder + NCBI + AMRFinderPlus per contig.** blaNDM-1 = **megaplasmid only** (100/100, 3 DBs). ble-MBL also on megaplasmid. oqxA/oqxB = **chromosome** (3 DBs) → minor discrepancy vs paper text. Contig3 (IncFIB) → **NO antibiotic-resistance genes** (only Sil/Pco/Ars heavy-metal + ClpK) = matches paper.
12. **Tn3000 architecture.** Parsed PGAP GFF around blaNDM-1 (308,200–309,012). Recovered exact paper Fig-1B order: IS3000 → IS30/ΔISAba125 → blaNDM-1 → bleMBL → trpF(PRAI) → dsbD → GroES → GroEL → IS3000.
13. **tra locus.** Contig3 carries complete F-type tra locus (TraA–Y + Trb + TraI relaxase). Megaplasmid carries an IncHI-type conjugal transfer system (temperature-regulated conjugation is canonical for IncHI/R27 plasmids → consistent with paper's 27 °C-only conjugation).
14. **Comparative BLAST.** megaplasmid vs pNDM-1-EC12 (MN598004): ~64.7% length shared; the blaNDM-1 shared HSP = **exactly 2488 bp at 99.96% id** (paper: 2488 bp).
15. **LLM-judge (free Argo gpt-5.2).** COVERAGE 8, AGREEMENT 9, **VERDICT: REPLICATED**.
16. Wrote report/, evidence/, artifact_harvest.md. Wrote ONLY inside target dir. No overwrite of siblings.

**What worked:** authors deposited a complete, well-annotated assembly → every sequence-testable claim was directly reproducible with the paper's own named tools.
**What could not be done:** the wet-lab conjugation frequency (4.3×10⁻⁶ at 27 °C) and the disk-diffusion/MIC AST panel — neither is computable from sequence.
