# Attempt Log — BVBRC-27 (Egan et al. 2020, optrA/poxtA)

Chronological, 2026-07-01.

1. **Read brief + BVBRC-17 exemplar.** Understood target structure (report/ + work/, claims table, LLM-judge verdict, WAVE_RESULT line).
2. **Paper metadata via Europe PMC** — PMID 32129849 → PMCID PMC7303821, DOI 10.1093/jac/dkaa075, OA=Y, JAC 2020. ✅
3. **Fetched full-text XML** (Europe PMC fullTextXML, 80 KB). Searched for accessions.
   - No SRA/BioProject/ERR accessions found (raw reads NOT deposited).
   - Found GenBank accessions **MN831410–MN831419** in the data-availability sentence (3 hybrid-assembled plasmids + optrA-variant DNA regions). This is the real, downloadable data.
4. **esummary on all 10 accessions** — confirmed sizes/species map exactly to paper claims (36331 bp optrA plasmid; 21849 bp poxtA plasmid; etc.). First loop attempt failed on a shell array quoting bug; fixed and reran. ✅
5. **Downloaded all 10 `.gb` + `.fasta`** from NCBI eutils efetch → `work/genbank/`. ✅
6. **grep of GenBank annotations** confirmed optrA/poxtA/fexA/cfr(D)/erm annotated by the authors — but this is *their* annotation, so I needed an independent screen.
7. **Reference-allele fetch attempts** — several guessed accessions (poxtA/fexA/cfr(D)) returned unrelated records (STLV, Salmonella IncHI2, fungal 28S). Lesson: don't guess AMR accessions.
8. **Pivot to the gold standard:** downloaded the full **NCBI AMRFinderPlus curated reference gene catalog** (AMR_CDS.fa, 9,712 alleles, 11 MB). This is the definitive, curated, independent AMR reference set.
9. **Independent AMR screen** (`amr_screen.py`): blastn each of the 10 deposited sequences vs the catalog, present if pident≥90 & cov≥60%.
   - Result: optrA 8/10 (99.7–100%), poxtA 2/2 poxtA plasmids (100%), cfr(D) 1/1 (100%), fexA 6/10, plus erm(B)/tet(M)/tet(L)/fexB/ant(9)-Ia. Matches paper's MDR phenotype exactly. ✅
10. **pE349/pE394 100%-identity claim:** downloaded pE394 (KP399637), blastn vs MN831410. Full 36,331 bp align at **99.997%** (1 mismatch). **Discovered the paper's "pE349" is really pE394** (size + identity are exact for pE394). ✅
11. **optrA-variant / diverse-background claim:** aligned all 8 extracted optrA CDS to canonical NG_048023 → 0–6 nt differences, **6 distinct optrA alleles**. ✅
12. **poxtA 21849 bp + identical 4001 bp IS1216E region claim:** MN831411 = exactly 21,849 bp; the two poxtA plasmids share a ~4109 bp block at 99.9% identity; annotations show poxtA flanked by IS1216E tnpA copies. ✅
13. **Remote BLAST vs nt** was attempted for extra independent confirmation of poxtA/cfr/fexA but stalled/queued >3 min → killed; the AMRFinderPlus-catalog screen (step 9) already provides curated independent confirmation, so this was unnecessary.
14. **LLM-judge** (`llm_judge.py`, free Argo argo:gpt-4o @ localhost:44497): **PARTIAL, Coverage 4/10, Agreement 4/4.**
15. Wrote report suite + saved evidence TSV/JSON.

## What worked
- GenBank was the right data source; the AMRFinderPlus catalog made the AMR screen genuinely independent and curated.
- The plasmid-alignment claims reproduced with striking precision (99.997% over full 36 kb).

## What didn't / caveats
- Raw reads never deposited → prevalence (22.7%), cgMLST/wgMLST clustering, and 23S G2576T copy-number claims are untestable from public data.
- Guessing reference-gene accessions wasted a few minutes; the FTP catalog was the fix.
