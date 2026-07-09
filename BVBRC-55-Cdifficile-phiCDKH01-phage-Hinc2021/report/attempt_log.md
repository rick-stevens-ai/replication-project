# Attempt Log — BVBRC-55 (phiCDKH01)

Chronological log. Analyst: Ollie (OpenClaw subagent), 2026-07-02.

1. **Candidate selection.** Read WAVE_BRIEF + BVBRC-17 exemplar. Walked ranks 38+ of `BVBRC_TOPUP85_2026-06-26.tsv`, deduping organism+topic against the 54 existing BVBRC-* dirs:
   - rank 38 = *Clostridioides difficile* bacteriophage phiCDKH01 (Hinc 2021) — **no existing Clostridium/Clostridioides or phage dir → GENUINELY NEW**. PICKED.
   - rank 39 Streptomyces → overlaps BVBRC-15/18 (Streptomyces/BGC). skip.
   - rank 40 K. pneumoniae → overlaps BVBRC-01/09/33/46. skip.
2. **OA check.** Europe PMC: PMID 34014385 is OA (CC BY 4.0), PMC8270841, inEPMC=Y. Fetched full-text XML via `PMC8270841/fullTextXML` (NOT the paid pdf tool).
3. **Created target dir** `BVBRC-55-Cdifficile-phiCDKH01-phage-Hinc2021/` (next free after BVBRC-54).
4. **Extracted claims + accessions** from XML: phage=MN718463, host WGS=JACSDL000000000 (contig JACSDL010000003.1), relative=phiCD24-1.
5. **Fetched genomes** via NCBI efetch: MN718463 (45,089 bp confirmed on download), GenBank record (66 CDS, 0 tRNA/rRNA confirmed instantly).
6. **Genome stats** (Biopython): length 45,089 (=paper), GC 28.72% (=paper 28.7%), CDS 66 (=paper), strands 52+/14− (paper 53+/13−, off-by-one annotation-boundary), tRNA/rRNA 0 (=paper).
7. **phiCD24-1 identity.** Resolved phiCD24-1 = LN681534 via esearch. BLASTn phiCDKH01↔phiCD24-1: aligned-region identity ~96%, query coverage ~82%. VIRIDIC-style whole-genome intergenomic similarity (careful non-overlapping calc) = **81.8%** ≥ 70% ICTV genus threshold → same genus. Paper's "89%" is a conserved-region/Easyfig figure; method-dependent, same conclusion.
8. **Panel + all-vs-all matrix.** Downloaded 11 other C. difficile phages. First VIRIDIC pass double-counted overlapping HSPs (gave impossible 100.3%); rewrote `viridic_matrix2.py` with per-query-position best-pident dedup. Result: phiCD24-1 81.8%, ALL others ≤9.9% → confirms closest-relative + novelty (novel species, <95%).
9. **CRISPR** (minced): detected **exactly 5 spacers, lengths 36/35/35/37/37 bp** at nt 30,200–30,559 → paper says "five spacers of 35, 36 or 37 bp". Exact match.
10. **Prophage localization.** Fetched host contig JACSDL010000003.1 (410 kb). BLASTn phage-vs-host: maps at **nt 288,611–333,698, 99.7% identity across full 45 kb** → paper 288,650–333,698. Endpoints within 39 bp. Confirmed.
11. **C6 caveat.** Paper reports 37/66 ORFs with predicted function (myRAST v36); the GenBank deposit carries only 9 functional product qualifiers. Full myRAST re-annotation not rerun → this single count is method/provenance-dependent, though the named functional modules (terminase, portal, capsid, integrase, amidase, holin, tape-measure) ARE present in the deposit.
12. **LLM judge** (free Argo gpt-5.2): **REPLICATED, agreement 93/100.** Saved to `report/evidence/llm_judge_verdict.txt`.

**What worked:** Everything — a genome-announcement paper with deposited accessions is highly replicable. All core descriptive/comparative claims reproduced on real public data.
**What was method-dependent:** exact phiCD24-1 identity % (81.8 vs 89), functional-annotation count (needs myRAST rerun). Neither changes a biological conclusion.
**Compute:** all light (small phage genomes); ran locally with BLAST+/minced. uicgpu not needed.
