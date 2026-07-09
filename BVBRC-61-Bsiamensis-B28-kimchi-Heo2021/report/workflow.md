# Workflow — Heo et al. 2021, *B. siamensis* B28 (BVBRC-61)

Replication workflow, in the order actually executed, on CherryRd, local free tools only.

## 0. Setup
- **Set:** BVBRC-61
- **Analyst:** Ollie (OpenClaw AI subagent)
- **Date:** 2026-07-02
- **Host:** CherryRd (local, offline-capable except NCBI `datasets` pulls)
- **Working dir:** `~/Dropbox/REPLICATE-PROJECT/BVBRC-61-Bsiamensis-B28-kimchi-Heo2021/`
- **Cost:** $0 (Europe PMC OA + NCBI datasets + free tools + free Argo LLM-judge)

## 1. Paper acquisition
1. Pulled full-text via Europe PMC **OA XML** (not the paid `pdf` tool):
   - Article ID `PMC8394110` (Heo et al., *Foods* 2021, 10(8):1906; DOI 10.3390/foods10081906)
   - Saved to `work/paper_fulltext.xml`
2. Extracted claims C1–C5 and all accessions (CP066219–CP066221, GCF_016313165.1, plus 6 comparator strain names).

## 2. Genome acquisition
1. Resolved B28 assembly from nuccore `CP066219` → **GCF_016313165.1** via eutils elink.
2. NCBI `datasets` CLI **v18.25.1** downloaded:
   - **B28** — GCF_016313165.1 (chromosome + 2 plasmids + `protein.faa` 3,808 + `genomic.gff`)
   - **B. siamensis KCTC 13613ᵀ** — GCA_000262045.1 (incomplete, 51 contigs — sanity ✓)
   - **B. siamensis SCSIO 05746** — GCA_002850535.1 (complete, 2 contigs — sanity ✓)
   - **B. amyloliquefaciens FS1092 & RD7-7** (paper's comparators)
   - **B. velezensis JJ-D34 & KMU01** (paper's comparators)
3. All downloads audited into `work/genomes/` with checksums.

## 3. Genome architecture (C2)
1. `genome_stats.py` — per-contig length, GC, N50.
2. tRNA/rRNA counted directly from RefSeq `genomic.gff` (feature-type filter).
3. Compared to paper's Table 1.
4. **Result:** chromosome 3,946,178 bp, GC 45.85%, 86 tRNA, 27 rRNA — all EXACT matches; plasmids 6,117 / 5,433 bp match paper's 6.1 / 5.4 kb rounding.

## 4. ANI reclassification (C1)
1. `fastANI` (default k=16, fragLen=3000) — B28 query vs each of 6 comparators.
2. `skani` (independent algorithm) — same 6 pairwise comparisons.
3. Both tools cross-checked against paper's Table.
4. **Result:** all within ~0.2% of paper; both siamensis comparisons >95%, both velezensis/amyloliquefaciens <95% → reclassification independently reproduced.

## 5. Safety — enterotoxins & hemolysin (C3a, C3b)
1. Proteome scan of `protein.faa` (3,808 seqs) for **Nhe / Hbl / CytK** enterotoxin family patterns → **0 hits (ABSENT)**.
2. Proteome scan for hemolysin-III-like → **4 hits ("hemolysin family protein")**, matching paper's *hlyIII* PRESENT.
3. Phenotype (β-hemolysis assay) is wet-lab → out of reach.

## 6. Safety — AMR (C3c, two independent tools)
1. **AMRFinderPlus 4.2.7** (DB `2026-03-24.1`):
   - Protein + nucleotide + GFF input (`-a pgap`)
   - `--plus` flag (surface stress/virulence too)
   - **Result:** 5 hits, ALL `scope=core` (intrinsic) — satA, fosM, two *bla* (β-lactamases), Tet(L/K/45) efflux MFS.
2. **RGI / CARD 3.2.7** (DIAMOND, protein mode):
   - **Result:** 9 Strict, 0 Perfect — vanT/vanY (fragmented van-cluster homologs, not functional operon), qacG/qacJ (disinfectant efflux), FosBx1 (corroborates fosM), tet(45) (corroborates Tet), BcI (*Bacillus* cephalosporinase — corroborates β-lactamases).
3. Cross-tool concordance → **no acquired/mobile AMR determinants**; all hits are intrinsic *Bacillus* chromosomal homologs. Fully consistent with paper's phenotypic susceptibility and paper's own Table 2 caveats.

## 7. Functional inventory (C4a, C4b, C4c)
1. `func_survey.py` — regex survey of all 3,808 RefSeq products.
2. Targeted greps for GABA, subtilisin/AprX, hlyIII, bacteriocin, cholylglycine hydrolase (BSH), γ-glutamyltransferase, sporulation, biofilm/EPS, adhesion, LTA, ROS-scavenging, α-galactosidase, TAG lipase.
3. Output in `evidence/func_survey.json`.
4. **Result:** every functional category the paper claims is confirmed; unique markers (MelA α-galactosidase, TAG lipase) both PRESENT. Only soft spot: paper's specific "bacitracin + mesentericin operon" naming not directly matched (RefSeq uses different vocabulary — surfactin, Blp class II, lantibiotic, circular bacteriocin — but biosynthetic capacity is unambiguous).

## 8. MLST
1. `mlst` **2.33.1**, scheme `bsubtilis` (pubMLST).
2. Cross-checked against paper's MLST claims.

## 9. LLM-judge (free Argo gpt-5.2)
1. Endpoint: `http://localhost:44497/v1` (Argo proxy, tunneled from studio-ts).
2. Model: `argo:gpt-5.2`, temp 0.
3. Prompt: paper claims + my results → verdict per claim + overall.
4. Output in `evidence/llm_judge.txt`.
5. **Judge verdict:** PARTIAL. Aligned with mine; I upgraded to PARTIAL (strong) on strength of exact genome architecture + dual-tool AMR concordance.

## 10. Reporting
1. `report/REPORT.md` — full markdown report.
2. `report/REPORT.tex` — LaTeX version with dedicated Genuine Critique section (this backfill).
3. `report/workflow.md` — this file.
4. `report/artifacts_summary.md` — audit trail of every file generated.
5. `report/failure_analysis.md` — what didn't work / limitations.
6. `report/open_questions.json` — 5 truly open follow-on questions.
7. Emit `WAVE_RESULT` line for set-level aggregation.

## Reproducibility
Every command is scripted in `work/scripts/`; every artifact is checksum-audited in `artifact_harvest.md`. Re-running end-to-end on any host with the same tool versions should reproduce identical numbers (ANI ±0.05% expected drift with algorithm version updates).
