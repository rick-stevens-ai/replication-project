# Workflow — BVBRC-86 Streptomyces (Albuquerque et al. 2021)

Independent replication workflow, in the order executed.

## 0. Scope
Replicate the paper's core biological claims from deposited public data (no re-sequencing). BV-BRC set entry 86, suggested workflows = Codon Tree / Phylogenetic Tree + Genome Assembly (Unicycler/SPAdes). Compute: CherryRd (parsing / ANI) + uicgpu 8×A100 (antiSMASH docker, 32 CPU per container).

## 1. Paper acquisition
- Pull open-access PDF from EuropePMC (`work/paper.pdf`, 1.99 MB, 10 pp).
- Text extract to `work/paper.txt` for grep / claim identification.

## 2. Claim identification
- Parse abstract + Table 1 + Section 2 for quantitative and qualitative claims.
- Assemble the 7-claim table (C1–C7) covering assembly stats, annotation counts, ANI, BGC totals, BGC composition, named MIBiG hits, data deposit.

## 3. Data resolution
- BioProject: `PRJNA754006`.
- NCBI E-utilities `esearch → esummary` on assembly:
  - UID 11377691 → **GCF_020740535.1** (MA3_2.13 / *S. profundus*, biosample SAMN20720482).
  - UID 11376371 → **GCF_020739505.1** (S07_1.15, biosample SAMN21157270).
- Pull assemblies + PGAP annotations from NCBI FTP: `*_genomic.fna.gz` and `*_genomic.gff.gz` per assembly → `work/genomes/`.
- Pull ANI reference genomes (exact references from paper):
  - `GCA_000220705.1` — *S. xinghaiensis* S187.
  - `GCA_002128305.1` — *Streptomyces* sp. SCSIO 3032.

## 4. Assembly-statistics recomputation (C1)
- Python direct FASTA parsing of `work/genomes/*.fna`.
- Per-record: length, GC% = (G+C)/(A+C+G+T) × 100, contig count.
- Output: `report/evidence/assembly_stats_recomputed.tsv`.

## 5. Structural-annotation counts (C2)
- Parse NCBI PGAP GFF, count features by `type` column: CDS, rRNA, tRNA.
- rRNA operon proxy = 16S rRNA count; cross-check subunit type via `Dbxref=RFAM:RF00177`.
- Note: paper used RAST + PGAP hybrid; we used PGAP-only because the public RAST server is unreliable/deprecated. Documented annotator caveat.

## 6. ANI (C3)
- `skani dist <query.fna> <ref.fna>` (v0.3.x learned-ANI mode, `/usr/local/bin/skani` on CherryRd).
- `fastANI -q <query.fna> -r <ref.fna> -o <out>` (v1.x, `/usr/local/bin/fastANI` on CherryRd).
- Species-boundary threshold: 95–96% ANI (Jain et al. 2018).
- Output: `report/evidence/ani_results.tsv`.

## 7. antiSMASH re-run (C4, C5, C6)
Docker image `antismash/standalone:6.1.1` on uicgpu, 32 CPU per container.

### Pass 1 — general BGC counting
```
docker run -d --name as_MA3 -v $PWD:/input -v $PWD/out_MA3:/output antismash/standalone:6.1.1 \
    GCF_020740535.1.fna --output-dir /output --genefinding-tool prodigal --cpus 32 \
    --taxon bacteria --minimal --cb-general --pfam2go --smcog-trees
```
(analogous container for S07_1.15 → `out_S07/`)

### Pass 2 — MIBiG knownclusterblast
```
docker run -d --name as_MA3_kcb -v $PWD:/input -v $PWD/out_MA3_kcb:/output antismash/standalone:6.1.1 \
    GCF_020740535.1.fna --output-dir /output --genefinding-tool prodigal --cpus 32 \
    --taxon bacteria --minimal --cb-knownclusters
```
(analogous container for S07_1.15)

### Post-processing
- Region count = number of `feature.type == "region"` in the antiSMASH JSON output (= per-region GBK file count in the output dir).
- Category composition from region `products` field.
- Top MIBiG hit per region from knownclusterblast JSON (BGC id, blast score, gene-level hit count).
- Outputs: `report/evidence/bgc_summary_table.tsv` (52 rows = header + 51 regions across both isolates), `report/evidence/known_cluster_hits.tsv`.
- Full antiSMASH JSONs archived as `report/evidence/antismash/{MA3_2.13,S07_1.15}_{general,knownclusters}.json.gz`.
- Full output trees (per-region GBKs + HTML reports) preserved on `uicgpu:/data/stevens/replicate/bvbrc86/out_*` (not copied to Dropbox for space).

## 8. Cross-comparison table
- Build `report/evidence/paper_vs_replication_table.md` row-by-row against paper's Table 1 and Section 2 claims.
- Flag: EXACT | consistent | version drift | annotator drift | CONFIRMED (for qualitative claims).

## 9. LLM-judge (free endpoint per wave-brief rule)
- Assemble structured judge prompt at `work/llm_judge_input.md` containing: claim table, results table, tool-drift explanations, and constrained-vocabulary instruction.
- POST to `http://127.0.0.1:44497/v1/chat/completions` (Argo proxy on CherryRd, auth `Bearer stevens`), model `argo:claude-sonnet-4.6`.
- Constrained vocabulary: REPLICATED | PARTIAL | SPOT-CHECK | NO-GO | CONTRADICTED | BLOCKED | FAILED.
- Save full response verbatim to `report/evidence/llm_judge_response.txt`.

## 10. Reporting
- `report/REPORT.md` — full narrative report (source of truth).
- `report/REPORT.tex` — LaTeX version with dedicated Genuine Critique section.
- `report/brief.md` — 1-paragraph summary.
- `report/attempt_log.md` — chronological execution log.
- `report/artifact_harvest.md` — every public artifact pulled.
- `report/artifacts_summary.md` — inventory + provenance for evidence files.
- `report/failure_analysis.md` — what was NOT reproduced and why.
- `report/open_questions.json` — 5 open follow-up questions grounded in the biology.
- `report/workflow.md` — this file.

## 11. Provenance / integrity
- Every downloaded artifact has NCBI accession recorded in `artifact_harvest.md`.
- All rerun outputs are byte-identical to the antiSMASH JSONs archived in `evidence/antismash/`.
- The LLM-judge response is stored verbatim (not paraphrased).

## Order of operations (executable summary)
1. paper.pdf ← EuropePMC.
2. GCF_020740535.1 + GCF_020739505.1 ← NCBI FTP.
3. Recompute assembly stats (Python) → C1 pass.
4. Parse PGAP GFF → C2 pass (with annotator caveat).
5. skani + fastANI vs S187 and SCSIO 3032 → C3 pass.
6. antiSMASH docker pass 1 (both isolates) → C4, C5 pass (with v5→v6 drift on MA3).
7. antiSMASH docker pass 2 (both isolates, knownclusterblast) → C6 pass (three named MIBiG hits confirmed).
8. Cross-comparison table built.
9. LLM-judge run → REPLICATED verdict.
10. Reports written.
