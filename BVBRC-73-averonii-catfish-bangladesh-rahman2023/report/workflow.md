# Workflow: BVBRC-73 replication of Rahman et al. 2023

**Paper:** Complete genome of MDR *Aeromonas veronii* Alim_AV_1000 from Bangladeshi stinging catfish (Shing fish).
**DOI:** 10.5455/javar.2023.j711 · **PMCID:** PMC10636080
**Deposited genome:** BioProject PRJNA810265, WGS JALLKR000000000, RefSeq **GCF_026738955.1**.
**Host:** CherryRd (macOS), local only. No HPC/GPU needed for a 4.5 Mb genome.
**Date:** 2026-07-03.

## 0. Setup
- Free/local toolchain only — no paid endpoints.
- Argo LLM proxy at `127.0.0.1:44497` (key=stevens) used only for the 4 free judge models.

## 1. Data acquisition
1. Pull PMC full text of the paper → `work/paper.xml`.
2. Extract 13 falsifiable claims → `report/evidence/claims_table.md`.
3. Download 6 genomes via NCBI Datasets FTP:
   - target `GCF_026738955.1` (Alim_AV_1000)
   - refs `GCF_001593245.1` (TH0426), `GCF_000204115.1` (B565), `GCF_008693705.1` (FDAARGOS_632)
   - outgroups `GCF_000014805.1` (*A. hydrophila* ATCC 7966), `GCF_000196395.1` (*A. salmonicida* A449)
   Land in `work/genomes/*.fna`.

## 2. Genome architecture (C1–C3)
- Biopython 1.87 → total length, GC%, contig count, longest contig, N50 on `GCF_026738955.1`.
- Compare against paper Table/Text: 4,494,515 bp / 58.87% / 93 contigs.

## 3. Annotation (C4–C6)
- Prodigal V2.60 (closed + open-ended) → CDS counts.
- Aragorn → tRNA count.
- Barrnap 0.9 → rRNA count + GFF (`report/evidence/rRNA.gff`).

## 4. Species phylogeny (C11)
- skani (learned-ANI mode) triangle across all 6 genomes → `report/evidence/ani_skani.tsv`.
- Check that target ↔ *A. veronii* refs > 95% and outgroups < 95%.

## 5. Virulence factors (C8, C9)
- abricate 1.4.0 vs. VFDB (4,592 seqs, DB 2026-Jul-03) on target genome → `report/evidence/vfdb.tsv`.
- Group hits by system (T2SS/T3SS/T6SS/flagella/pili) → cross-check paper's explicit T2SS+T3SS+T6SS + adhesion+flagella+pili claim.

## 6. AMR (C10) — 5-way concordance
- abricate 1.4.0 vs. **CARD, NCBI-AMR, ResFinder, ARGannot, MEGARes** (all DBs dated 2026-Jul-03).
- Intersect hits across DBs → high-confidence loci (OXA-12, cphA4, rsmA).
- Outputs → `report/evidence/{card,ncbi,resfinder,argannot,megares}.tsv`.

## 7. MLST (C7) — direct PubMLST scan
- PubMLST REST API scheme 1 (Aeromonas 6-locus MLST): submit target assembly, one locus at a time (gyrB, groL, gltA, metG, ppsA, recA).
- For each locus record exact/partial allele match + best-hit allele ID + %id/mismatches.
- Fetch the ST profile table (2,755 STs current) and check for any ST matching the observed alleles.
- Compare against ST 492's canonical profile (gyrB=112, groL=347, gltA=44, metG=217, ppsA=384, recA=381).
- Full evidence → `report/evidence/mlst_analysis.txt`.

## 8. Phage (C12)
- Attempt phaster.ca POST with `GCF_026738955.1` assembly (4.5 MB) — broken pipe error, service refused. Marked SPOT-CHECK, not replicated.

## 9. Wet-lab AST (C13)
- Not testable from a genome rerun; noted as such.

## 10. LLM judging
- Full 13-row claims table + observed evidence sent to 4 free Argo judges (`argo:gpt-5.2`, `argo:claude-sonnet-4.5`, `argo:gemini-2.5-pro`, `argo:gpt-4.1`).
- Each judge returns strict JSON `{coverage, agreement, fidelity, reproducibility, verdict, rationale}` on 0-10 scale.
- Judge A (opus-4.7) and Judge C (opus-4.8) returned Argo-side 502; substituted the three above to keep four independent judges.
- Aggregate: `report/evidence/llm_judges_raw.json` + `report/evidence/llm_judge_summary.json`.

## 11. Reporting
- REPORT.md (canonical narrative).
- REPORT.tex (LaTeX + genuine critique section).
- brief.md (short summary).
- attempt_log.md (running log).
- artifact_harvest.md (which files landed where).
- open_questions.json (5 truly open follow-ups).
- workflow.md (this file).
- artifacts_summary.md (index of every output).
- failure_analysis.md (what didn't replicate + why).

## Reproducibility note
End-to-end run time ≈ 15 min on a laptop. No paid API calls in the pipeline; only the 4 LLM judges call out to the free Argo proxy. All AMR/VF/rRNA/tRNA/CDS/ANI/MLST tools are `brew install`-able. PubMLST REST is a public unauthenticated endpoint.
