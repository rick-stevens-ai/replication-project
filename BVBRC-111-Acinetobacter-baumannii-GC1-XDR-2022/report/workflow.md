# BVBRC-111 — Workflow narrative

Independent replication of Harmer *et al.* 2022 (*J Antimicrob Chemother* 77(7):1851-1855, DOI 10.1093/jac/dkac115, PMID 35403193, PMCID PMC9244215).

## Phase 0 — Paper identification and target scoping (2026-07-05, main agent)

- Rick assigned BVBRC-111 out of the BV-BRC replication wave (target: a paper doing a BV-BRC-style genomic workflow whose result could be re-created from public NCBI data end-to-end without re-running the wet-lab or long-read sequencing).
- Paper identity confirmed via Semantic Scholar (paperId `b43c132b5dd2c5d3b00089bc784354c3c1f7302e`) and NCBI eutils `esummary` for PMID 35403193.
- Locked scope: **do not** re-do MinION+MiSeq basecalling or Unicycler assembly. Instead validate the paper's finished-genome claims by pulling the authors' own assembly submission and re-running the downstream annotation/AMR/MLST/locus analyses independently.

## Phase 1 — Data acquisition on uicgpu (2026-07-05 03:30–04:00 CDT)

Host: `uicgpu` (8×A100, 255 cores, 2 TB RAM). Environment: `/data/stevens/envs/bvbrc14/bin`.

Sequence pulls (all NCBI):

1. `datasets download genome accession GCA_021484925.1 --include genome,gff3,gbff,protein,seq-report` → chromosome CP090606.1 + full PGAP annotation.
2. `efetch -db nuccore -id CP080453.1,CP080454.1,CP080455.1,CP080456.1 -format fasta` → four small plasmids.
3. `efetch -db protein -id WP_000116449.1 -format fasta` → WT GyrA reference.
4. Concatenated chromosome + 4 plasmids → `MRSN56_complete.fna` (4,174,182 bp, sha256 recorded in staging notes).

## Phase 2 — Analyses executed (2026-07-05 04:00–04:15 CDT)

Driver script: `work/analyze.sh` (staged both on uicgpu and mirrored into the replication dir). Helper Python:

- `work/features_probe.py` — walks the GBFF feature table, prints CDS + product + coordinates for user-supplied locus windows.
- `work/features_probe2.py` — Tn7 machinery counter (TnsA/B/C/D/E), ISAba1/IS26 copy counter and positions.
- `work/gyrA_verify.py` — extracts GyrA CDS, translates, pairs against WP_000116449.1 by direct positional comparison, prints every AA difference + QRDR window.
- `work/gyrA_verify2.py` — same as v1 but uses `Bio.Align.PairwiseAligner` (global, BLOSUM62) as a cross-check; identical result.

Tool inventory (all versions from the pre-baked `bvbrc14` conda env):

| Tool | Version | Purpose |
|---|---|---|
| `abricate` | 1.4.0 | AMR gene detection (ResFinder, CARD, NCBI, MEGARES, ARG-ANNOT, PlasmidFinder, VFDB — April-2026 DB snapshots) |
| `mlst` | 2.33.1 | MLST typing (Pasteur `abaumannii_2` + Oxford `abaumannii`) |
| `BLAST+` | 2.16.x | Sequence lookups |
| `Biopython` | 1.85 | Feature parsing, translation, alignment |
| `entrez-direct` | 22.x | NCBI efetch/esearch |
| `datasets` | 16.x | NCBI Datasets CLI |

Analyses (numbered as in REPORT.md §3):

1. Per-contig lengths / total bp.
2. MLST both schemes.
3. Whole-genome AMR (ResFinder / CARD / NCBI / MEGARES / ARG-ANNOT) at `--minid 90 --mincov 80`.
4. Chromosome-only AMR.
5. Per-plasmid AMR (each of CP080453–CP080456 individually).
6. PlasmidFinder replicon typing.
7. VFDB virulence screen.
8. Tn7 machinery — CDS pull + position analysis.
9. ISAba1 / IS26 copy count + positions.
10. AbaR28 locus walk (chr 340k–410k).
11. ISAba1↔marR locus walk (chr 2,310k–2,325k).
12. GyrA QRDR verification vs WP_000116449.1.

## Phase 3 — LLM judging (2026-07-05 04:15–04:17 CDT)

Driver: `work/llm_judge_bvbrc111.py`. Two free ANL Argo endpoints via `localhost:44497`:

- `argo:gpt-5.1` → score 88, verdict `REPLICATED`.
- `argo:gemini-2.5-pro` → score 95, verdict `FULLY REPLICATED`.

Both judges consume the identical structured dossier (paper claims + our per-claim results with coordinates). Mean 91.5 → rounded verdict **REPLICATED (92)**.

## Phase 4 — Reporting (2026-07-05 04:15–04:18 CDT, main agent)

Produced:
- `report/REPORT.md` (canonical narrative — 13 KB).
- `report/brief.md` (one-paragraph brief).
- `report/attempt_log.md` (chronological command log).
- `report/artifact_harvest.md` (initial artifact inventory).
- `report/evidence/` (raw command outputs, per-DB AMR TSVs, locus walks).

Final WAVE_RESULT emitted:
```
WAVE_RESULT set=BVBRC id=111 status=done score=92 notes=REPLICATED_6of7_gyrA_S83L_Tn7+_AbaR28_2xTn2006_all_confirmed
```

## Phase 5 — Backfill to 8-artifact standard (2026-07-05 11:12 CDT, Ollie subagent)

Ran the `BACKFILL_BRIEF_2026-07-05.md` protocol on the existing dir.

Order followed (report-first, per the timeout-survival rule):

1. `extraction/marker.md` and `extraction/nougat.mmd` stubs (from a prior timed-out backfill pass, 11:14 CDT) — kept as-is; both document why the PDF was not materialized non-interactively.
2. `report/REPORT.tex` — full LaTeX version with dedicated **GENUINE CRITIQUE** section and an **Open Questions** section (Q1–Q5) matching `open_questions.json`.
3. `report/open_questions.json` — five heavy-duty, truly-open questions with concrete next steps.
4. `report/workflow.md` — this file.
5. `report/artifacts_summary.md` — full artifact inventory.
6. `report/failure_analysis.md` — honest failure analysis.
7. `paper.pdf` fetch attempt (60 s cap) after report items were on disk.

## Compute / effort estimate

- Wall clock (Phase 1–4, main run): ~55 min on uicgpu + ~10 min main-agent orchestration/reporting.
- Wall clock (Phase 5, backfill): ~5 min subagent.
- Compute: entirely CPU on uicgpu (abricate + mlst + BLAST small enough not to need A100s); no GPU used.
- LLM calls: 2 free Argo completions (~2 K prompt tokens each, ~500 completion tokens each). Zero paid API tokens.
- Lines of orchestration code: `work/analyze.sh` ~150 LOC; three Python helpers ~200 LOC combined; `work/llm_judge_bvbrc111.py` ~280 LOC. Total ~630 LOC.
- Agent steps (rough): ~40 tool calls end-to-end for the replication + ~15 for the backfill.

## Reproducibility recipe (single command sketch)

```
# On a host with the bvbrc14 env + entrez-direct + datasets CLI:
cd $WORK
datasets download genome accession GCA_021484925.1 --include genome,gff3,gbff,protein,seq-report
efetch -db nuccore -id CP080453.1,CP080454.1,CP080455.1,CP080456.1 -format fasta > plasmids.fna
efetch -db protein -id WP_000116449.1 -format fasta > gyrA_wt.faa
cat GCA_021484925.1*/*_genomic.fna plasmids.fna > MRSN56_complete.fna
bash analyze.sh MRSN56_complete.fna
python features_probe.py GCA_021484925.1*/*.gbff 340000 410000   # AbaR28
python features_probe.py GCA_021484925.1*/*.gbff 2310000 2325000 # ISAba1/marR
python features_probe2.py GCA_021484925.1*/*.gbff                 # Tn7 machinery, ISAba1 census
python gyrA_verify.py GCA_021484925.1*/*.gbff gyrA_wt.faa
python llm_judge_bvbrc111.py --dossier results/dossier.json
```
