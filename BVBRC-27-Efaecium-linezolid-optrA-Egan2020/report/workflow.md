# Workflow — BVBRC-27 Egan 2020 optrA/poxtA replication

**Target:** Egan SA et al. 2020, *J. Antimicrob. Chemother.* 75(7):1704–1711. PMID 32129849 / PMCID PMC7303821.
**Analyst:** Ollie (OpenClaw AI), Wave 2026-07-01, target #27.
**Independent second pass:** 2026-07-03 (fresh subagent, no shared state).
**Verdict:** PARTIAL REPLICATION.

## Stage 0 — Scoping
1. Identify paper is open-access on Europe PMC.
2. Read text; enumerate 7 discrete claims (C1–C7); classify each as `genomic-testable` (C1–C4) or `epidemiological / phylogenomic / SNP` requiring raw reads (C5–C7).
3. Decision: attempt C1–C4 on deposited artifacts; declare C5–C7 out of reach up front (raw reads never deposited → no SRA/BioProject).

## Stage 1 — Artifact harvest
1. `curl` Europe PMC full-text XML (`PMC7303821/fullTextXML`).
2. Scrape for accessions → 10 GenBank IDs found (`MN831410`–`MN831419`).
3. Confirmed absence of SRA experiment / BioProject in data-availability statement.
4. `esummary` on all 10 → verify length + species map to paper claims.
5. `efetch` all 10 → `work/genbank/*.gb` + `*.fasta`.

## Stage 2 — Reference resources
1. Download NCBI AMRFinderPlus curated catalog (`AMR_CDS.fa`, 9,712 alleles) — independent AMR reference, NOT the authors' RAST annotation.
2. `efetch` canonical *optrA* (NG_048023) for C4 variant comparison.
3. `efetch` pE394 (KP399637, 36,331 bp) as the C2 reference plasmid (inferred from paper's ambiguous "pE349" name + exact size hit).
4. `makeblastdb` for each reference set.

## Stage 3 — Independent AMR screen (C1)
1. `amr_screen.py`: for each of the 10 deposited records, `blastn` vs `AMR_CDS.fa`.
2. Presence rule (AMRFinderPlus-style, conservative): `pident ≥ 90 %` AND `alignment coverage ≥ 60 %` of the reference allele; retain best hit per gene symbol.
3. Emit `amr_screen_results.json` — one record per accession × detected-gene.
4. Cross-check gene set against Egan Table 1 / Table 2 text.

## Stage 4 — Plasmid identity (C2)
1. `blastn` MN831410 (pM17/0149, 36,331 bp) vs pE394 (KP399637, 36,331 bp).
2. Sum HSP identities weighted by aligned length → 99.997 % (1 mismatch total over full 36,331 bp).
3. Confirm extracted *optrA* CDS is 100 % identical to canonical NG_048023.
4. **Ancillary finding:** paper's "pE349" is not a real accession at that size; pE394 is the true reference. Recorded as a nomenclatural correction (Egan Table 2 typo).

## Stage 5 — poxtA cassette structure (C3)
1. `blastn` MN831411 (*E. faecium* poxtA plasmid) vs MN831412 (*E. faecalis* poxtA plasmid).
2. Extract HSPs ≥ 500 bp → shared blocks identified (~4,109 bp + 4,426 bp near-identical).
3. Biopython parse of MN831411 features → locate *poxtA* CDS (17,064–18,693) and flanking IS*1216E* `tnpA` copies (16,330–17,017 upstream; 19,651–20,338 downstream).
4. Confirm 809/811 bp 100 %-identity sub-hits between the two plasmids are repeated IS*1216E* copies (not artefactual).

## Stage 6 — optrA variant diversity (C4)
1. Biopython extract of *optrA* CDS from all 8 optrA-carrying deposited records.
2. Pairwise nt-differences vs canonical NG_048023: {0, 1, 2, 2, 2, 3, 6, 6}.
3. 6 distinct alleles across both species.

## Stage 7 — Verdict
1. `llm_judge.py` → Argo proxy `localhost:44497`, model `argo:gpt-4o`, key=`stevens`, free.
2. Evidence-only prompt (no chain-of-thought hidden; verdict vocabulary enforced: REPLICATED / PARTIAL / FAILED / OUT-OF-REACH).
3. Judge output: PARTIAL, Coverage 4/10, Agreement 4/4.

## Stage 8 — Report emission
1. `REPORT.md` (canonical).
2. `brief.md`, `attempt_log.md`, `artifact_harvest.md`.
3. `report/evidence/` bundle: all TSVs + judge verdict + JSON.

## Stage 9 — Independent reproduction (2026-07-03, fresh subagent)
1. Fresh session with no access to prior workspace state.
2. Re-`efetch` all 12 sequences from NCBI.
3. **Different AMR pipeline:** `abricate v1.4.0` + NCBI AMRFinderPlus DB (8,232 alleles) + ResFinder DB (3,206 alleles) cross-check.
4. Re-run C2/C3/C4 with BLAST+ 2.17.0.
5. Deterministic 36-number comparison table: 36/36 exact match at 2-decimal precision.
6. Incidental: `erm(A)` flagged at 87.16 % id on 4 records — below 90 % threshold, correctly excluded, known catalog cross-reactivity, NOT a contradiction.
7. Verdict CONFIRMED: PARTIAL.

## Data-flow summary
```
Europe PMC full-text  ──►  accession list  ──►  NCBI efetch  ──►  work/genbank/
                                                                    │
             ┌──────────────────────────────────────────────────────┤
             ▼                        ▼                        ▼
      AMR screen (C1)      Plasmid identity (C2)    poxtA cassette (C3)
             │                        │                        │
             └────────────────►  REPORT.md  ◄──────────────────┘
                                    │
                            LLM-judge (C1–C4)
                                    │
                              PARTIAL verdict
                                    │
                     Independent reproduction (2026-07-03)
                                    │
                             36/36 CONFIRMED
```

## Wall clock + cost
- ~2 min laptop CPU (original run) + ~3 min (independent rerun).
- All inputs free / public (~12 MB total data + ~15 MB independent bundle).
- LLM cost: $0 (free Argo proxy).
