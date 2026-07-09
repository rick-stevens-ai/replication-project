# Attempt Log — BVBRC-58 (chronological)

**2026-07-02 (all times CDT)**

1. Read WAVE_BRIEF_2026-07-01.md + BVBRC-17 exemplar REPORT.md for structure.
2. Read priority list rows 45–73 of BVBRC_TOPUP85_2026-06-26.tsv; pulled full titles/authors/venue.
3. **Candidate dedup (down from rank 45):**
   - rank 45 — E. coli co-MCR-1+NDM-1 bloodstream (Zheng 2017, Sci Rep). AMR/plasmid; distinct from BVBRC-09 (NDM5 K. pneu) and BVBRC-49 (mcr1 duck). Complete genomes, clear accessions → **PICKED** (highest-ranked genuinely-new isolate genome study).
   - Verified OA via Europe PMC: PMID 29263349, PMC5738369, isOpenAccess=Y.
4. Created target `BVBRC-58-Ecoli-MCR1-NDM1-bloodstream-Zheng2017/` (next free after BVBRC-57). Confirmed no collision.
5. Fetched full-text XML from Europe PMC (82 KB). Parsed Materials/Methods + Table 1 (9 accessions CP021202–CP021210, sizes, GC, ST types, per-plasmid resistance genes, replicon types).
6. Downloaded all 9 GenBank FASTA via NCBI efetch (free). GenBank strain labels Z1002/Z247 = paper EC1002/EC2474; plasmid names match Table 1.
7. **Genome stats** (local venv, Biopython 1.87): all replicon lengths match paper Table 1 to 0–8 bp; per-replicon GC within 0.5%. → C1, C2 reproduced.
8. Set up uicgpu (`~/bvbrc58/`), copied genomes + per-strain concatenated FASTAs.
9. **MLST** (mlst 2.35.0, scheme ecoli_achtman_4):
   - Hit a Perl-version conflict — mlst shebang wanted 5.32 but base PATH gave 5.30. Fix: prepend `~/micromamba/envs/amr/bin` to PATH so env's own perl 5.32.1 is used.
   - Result: EC1002 → **ST405**, EC2474 → **ST131** — exact match to paper. → C3 reproduced.
10. **AMRFinderPlus 3.12.8**:
    - First run failed: `No valid AMRFinder database` (hard-coded bioconda path, `$CONDA_PREFIX` unset). Fix: export `CONDA_PREFIX` and pass `-d <db 2024-07-22.1>` explicitly.
    - Ran per strain with `--organism Escherichia --plus`. Genes mapped to contig → plasmid. Core AMR (mcr-1.1, blaNDM-1, blaCTX-M-14/15/55, rmtC, floR, fosA3, sul, aph, aac, mph, ble, tet(B)) reproduced per-plasmid. mcr-1 & blaNDM-1 on separate plasmids confirmed. → C4 partial, C6 reproduced.
11. **PlasmidFinder replicon typing**: fetched enterobacteriales.fsa (159 refs) locally (uicgpu needs proxy), scp'd to uicgpu, makeblastdb + blastn (95%id/60%cov). All 7 plasmid replicon types match paper (IncA/C2 reported as its renamed IncC; IncF refined to IncFII; IncFIB confirmed). → C5 reproduced.
12. **LLM judge** (Argo gpt-5.2, free): coverage 5/6 = 83.3%; agreement ~85–90%; canonical verdict **PARTIAL**.
13. Saved all evidence to `report/evidence/`; wrote report set.

## What worked
- efetch pulled all 9 complete replicons cleanly; genome stats + MLST + replicon typing matched the paper near-perfectly on real data.

## What was tricky (and fixed)
- amr-env Perl version conflict for mlst (fixed via env PATH).
- AMRFinder DB path resolution (fixed via `-d` + `CONDA_PREFIX`).
- uicgpu outbound internet for the PlasmidFinder DB (fetched locally, scp'd).

## Honest limitations
- AMR called with 2024 AMRFinderPlus vs the paper's 2017 ResFinder 2.1 → expected allele/nomenclature drift (fosA3 vs fosA14, aac(3)-IIe vs aac(3)-Ib, arr/oqxB not called, extra ble/qacEΔ1/ter loci). Core AMR conclusions unaffected.
- Did not rebuild plasmid comparison figures (BRIG/Easyfig) or re-run the genetic-context alignments beyond confirming co-localization of blaNDM-1 + rmtC + ble on one contig.
