# Workflow — BVBRC-106 (Singh et al. 2018, MDR E. bugandensis ISS)

## Narrative

Single-session, single-agent replication executed 2026-07-05 00:09–00:26 CDT.
LLM-authored backfill (this document + REPORT.tex + items 5-8) added the same day,
starting ~10:19 CDT via a second subagent pass (no re-run of the genomic analyses;
evidence tree from the original session was reused verbatim).

### Phase 1 — Paper ingest & claim extraction (~00:09–00:13, ~4 min wall)
1. Read the BVBRC-106 wave brief for target paper + verdict framework.
2. Pulled PubMed abstract for PMID 30466389 via NCBI E-utils (`efetch.fcgi?db=pubmed`).
3. Pulled full-text PMC XML for PMC6251167 (`efetch.fcgi?db=pmc&rettype=xml`).
4. Parsed out: BioProject `PRJNA319366`, 5 ISS WGS accessions (POUR/POUQ/RBVJ/POUP/POUO),
   3 clinical comparators (FYBI, NZ_JVSD, PRJNA310238), Table 1 paper ANI/dDDH values,
   Table 2 AMR narrative.

### Phase 2 — Environment (~00:13–00:14, ~1 min)
5. SSHed to `uicgpu`, created `~/replicate/bvbrc-106/{genomes,work,logs}`.
6. Confirmed `bvbrc14` conda env (AMRFinderPlus 4.2.7 + DB 2026-03-24.1) and `bvbrc28`
   conda env (NCBI Datasets 18.32.0, FastANI, prokka, mash, prodigal) already existed —
   no fresh env build required.

### Phase 3 — Data pull (~00:15–00:18, ~3 min)
7. Ran `work/resolve_accessions.py` (Entrez `esearch`/`esummary` Python script) to map
   the 8 paper accessions to current NCBI RefSeq assembly accessions. 7 of 8 resolved
   directly; EB-247T's `FYBI00000000` (ENA-only WGS master) required a strain-name
   fallback query to reach `GCF_900324475.1`.
8. `datasets download genome accession <8 GCFs> --include genome --filename bugandensis_assemblies.zip`
   (11.5 MB). Unzipped, symlinked strain-named FASTAs into `genomes/fastas/`.

### Phase 4 — ANI matrix (~00:19, ~2 s FastANI compute + ~30 s wall)
9. `fastANI --ql all_fastas.txt --rl all_fastas.txt -o ani_matrix.tsv -t 8` on 8 threads.
10. Built pretty 8×8 matrix as `report/evidence/ani_matrix_pretty.csv`.

### Phase 5 — AMR screen (~00:20–00:23, ~4 min)
11. `amrfinder -n <strain>.fna --organism Enterobacter_cloacae --plus --threads 8`
    per strain, 8 total, ~40 s each.
12. Output: 8 per-strain TSVs collated in `report/evidence/amr/`.

### Phase 6 — LLM judge (~00:25, ~30 s)
13. Prompt sent to Argo proxy at `127.0.0.1:44497/v1/chat/completions` with `Bearer stevens`.
14. Primary model `argo:claude-opus-4.8` → HTTP 502. Fallback `argo:claude-sonnet-4.6` → OK.
15. Judge returned **REPLICATED** verdict. Raw output saved as `report/evidence/llm_judge_output.md`.

### Phase 7 — Reporting (~00:26)
16. Authored `REPORT.md`, `brief.md`, `artifact_harvest.md`, `attempt_log.md`.

### Phase 8 — Backfill (this pass, 2026-07-05 ~10:19 CDT)
17. Re-read PMC full-text XML for genuine open-question grounding.
18. Wrote `REPORT.tex` (§1 summary, §2 claims table, §3 method, §4 results, §5 per-claim
    what-worked / what-didn't, §6 critique, §7 verdict, §8 open questions).
19. Wrote `open_questions.json` (5 grounded, non-superficial questions with next_steps).
20. Wrote this `workflow.md`, `artifacts_summary.md`, `failure_analysis.md`.

## Enumerated tools and versions

| Tool / code | Version | Where | Purpose |
|---|---|---|---|
| NCBI E-utils (`efetch`) | live 2026-07-05 | remote HTTPS | fetch PubMed abstract + PMC XML |
| NCBI `datasets` CLI | 18.32.0 | uicgpu env `bvbrc28` | download 8 RefSeq assemblies |
| Python 3.11 | stdlib | uicgpu env `bvbrc28` | `resolve_accessions.py` (Entrez esearch/esummary) |
| FastANI | 1.34 | uicgpu env `bvbrc28` | all-vs-all 8×8 ANI |
| AMRFinderPlus | 4.2.7 | uicgpu env `bvbrc14` | AMR gene screen (`--organism Enterobacter_cloacae --plus`) |
| AMRFinderPlus DB | 2026-03-24.1 | uicgpu env `bvbrc14` | reference alleles |
| Argo proxy | live 2026-07-05 | CherryRd `127.0.0.1:44497` | LLM judge (free ANL endpoint) |
| `argo:claude-opus-4.8` | Argo | Argo proxy | primary judge (502'd) |
| `argo:claude-sonnet-4.6` | Argo | Argo proxy | fallback judge (returned verdict) |
| `argo:claude-opus-4.7` | Argo | Argo proxy | backfill report author (this pass) |
| bash / conda / ssh | system | uicgpu, CherryRd | orchestration |
| `pdftotext` (poppler) | as-installed | CherryRd | marker.md fallback (backfill) |

## Codes/scripts written (all under `work/`)

| Script | LOC | Purpose |
|---|---|---|
| `resolve_accessions.py` | ~40 | Entrez esearch/esummary WGS → assembly resolver |
| `fetch_assemblies.sh` | ~15 | `datasets download` wrapper |
| `download_genomes.sh` | ~10 | (superseded early alternative) |
| `llm_judge.py` | ~35 | Argo POST client for verdict |

Total code written: ~100 LOC across 4 files.

## Effort estimate

- **Compute wall-time (analysis)**: ~9 min end-to-end on uicgpu (FastANI 2 s + AMRFinderPlus 8×40 s
  in serial ≈ 5.5 min + data download ~2 min + resolution ~1 min).
- **Compute wall-time (backfill)**: ~5 min authoring time on CherryRd, negligible tool CPU.
- **Human/agent wall-time (original)**: ~17 min, single subagent session.
- **Human/agent wall-time (backfill)**: ~10 min, single subagent session.
- **Total wall**: ~30 min.
- **Total LLM tokens** (rough): original ~15 k in / 5 k out; backfill ~30 k in / 15 k out.
- **Runs executed**: 1 FastANI, 8 AMRFinderPlus, 1 LLM judge (retry). No re-run in backfill.
- **Agent steps**: ~40 tool calls total.
- **LOC written**: ~100 LOC of Python/bash + ~800 lines of Markdown/LaTeX report.

## Non-goals (out of scope for this run)

- PathogenFinder v2 rerun (paper claim C9).
- Prokka/RAST subsystem re-annotation (paper claim C10 gene count 4733).
- Targeted BLAST for MAR operon (paper claim C7).
- Plasmid separation and plasmid-gene-content re-derivation (paper Additional file 2 Table S2).
- 2018-vs-2026 assembly-drift audit (see Q5).
- MLST recomputation from raw contigs.

These are captured as open questions Q1–Q5 in `open_questions.json` for future work.
