# Attempt Log — BVBRC-53 (chronological)

**2026-07-02 (subagent, CherryRd + uicgpu)**

1. Read WAVE_BRIEF_2026-07-01.md + BVBRC-17 exemplar REPORT.md for structure.
2. Read candidate TSV ranks 34–61. Dedup vs existing BVBRC-01..52:
   - Rank 34 (Campylobacter, Ocejo 2021, PMID 33903652) = **exact duplicate of BVBRC-52** (Campylobacter-ruminants-AMR-Ocejo2021). Skipped.
   - Rank 35 (**S. epidermidis** bacteriocin plasmids, Nakazono, PMID 35041663) = **no existing S. epidermidis study**. New organism, clear public genome data (deposited plasmids), BV-BRC PlasmidFinder workflow. **PICKED.**
3. Confirmed OA via Europe PMC (PMC8765612, PLOS ONE, CC-BY). Created target dir BVBRC-53-Sepidermidis-bacteriocin-plasmids-Nakazono2022 (BVBRC-53 was free).
4. Fetched full-text XML; parsed out accessions: pEpi56=OK031036, pNuk650=OK031035, ref pIVK45=KP702950. Extracted quantitative claims (sizes, ORF counts, insertion, peptide identities).
5. Downloaded all 3 sequences from NCBI efetch (FASTA + GenBank). FASTA length check: 64386 / 26160 / 21840 — **exact match to paper on first pass.**
6. Parsed GenBank: CDS counts 81 / 29 / 17; GC 27.5 / 26.0 / 26.1%. Extracted epiA and nukA translations.
7. **Peptide checks (local Python):**
   - epiA KSE56 prepeptide = 100% aa identical to canonical Tü3298 epidermin (C4 ✓).
   - nukA KSE650 vs IVK45: exactly 1 mismatch, position 4 (L↔F) in the leader; mature C-terminus identical (C5 ✓).
8. Attempted nucmer/dnadiff locally → broken (Perl `TIGR::Foundation` @INC + MUMmer mbedtls mismatch). Pivoted to **blastn** for pNuk650 vs pIVK45: 99.6% backbone identity, 70.3% aligned, **7,781 bp insertion** unique to pNuk650, largest block 5,926 bp (17040–22965) → reproduces the "~8 kbp insertion" C3 ✓.
9. **uicgpu offload** (heavy-tool step, per compute rule): copied 3 FASTAs to `/data/stevens/scratch/bvbrc53/`. Env `bvbrc28` lacked abricate/mlst; **`bvbrc14` (conda-activated)** had abricate 1.4.0 (card/resfinder/vfdb/plasmidfinder/bacmet2/megares), amrfinder 4.2.7, mlst 2.33.1.
10. Ran BV-BRC-style specialty-gene screen: **PlasmidFinder** found shared rep genes (repUS46, repUS23_repA, rep21) in pNuk650 & pIVK45 (same replicon family), rep39/rep5a-like in pEpi56; **no AMR** (card/resfinder/megares/amrfinder empty); **no classical VFDB virulence**; bacmet2 only spurious <33% hits. → plasmids are bacteriocin-immunity plasmids, not AMR/VF plasmids (consistent with paper).
11. Copied evidence TSVs back to `report/evidence/`.
12. LLM-judge (Argo `gpt-5.2`, free) on the full claim set → **PARTIAL**, coverage 0.83, agreement 0.95.
13. Wrote report files.

**No overwrites** of any sibling dir. All writes confined to BVBRC-53 target dir + uicgpu scratch.
