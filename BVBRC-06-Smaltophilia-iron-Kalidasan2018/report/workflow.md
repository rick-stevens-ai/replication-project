# Workflow, Tools, and Effort Estimate
_Backfilled to the 8-artifact standard on 2026-07-05._

## 1. Narrative

The original replication (2026-05-10) was an agent-driven, database-only
re-derivation of the in-silico slice of Kalidasan et al. 2018. No wet-lab
component was attempted (out of scope for a database agent).

Overall flow:

1. **Paper acquisition + parse.** PDF fetched from MDPI (`doi:10.3390/molecules23082048`),
   dropped at `paper/Kalidasan2018.pdf`. A small hand-curated
   `paper/paper_extracted.md` captured the four genomes, the 17 target list,
   and the seven computationally testable claims.
2. **Genome resolution.** All four GenBank accessions (AE016879, CP001111,
   HE798556, CP002986) resolved to BV-BRC genome IDs (522373.48, 391008.21,
   1163399.19, 868597.17). Cached in `data/genome_ids.json`.
3. **Subsystem retrieval.** BV-BRC public REST API queried for the
   "Iron acquisition and metabolism" subsystem class for each genome ID;
   returned role/feature tables cached in `data/iron_subsystems_all.json` and
   the K279a-specific subset in `data/k279a_iron_subsystems.json`.
4. **Locus-tag mapping (K279a).** The 17 paper locus tags
   (`SMLT_RS12950`, `SMLT_RS18575`, ...) mapped to BV-BRC feature IDs
   (`Smlt2716`, `Smlt3898`, ...) via BV-BRC's `feature` endpoint and the
   NCBI GFF cross-index. Result: `data/k279a_target_mapping.json`.
5. **Comparative presence.** For each of the 17 targets, two independent
   lookups were run across the other 3 genomes:
   (a) PLfam ortholog membership at the species level,
   (b) keyword search on the functional-role text.
   Combined result: `data/comparative_targets.json` (v1) and
   `data/comparative_targets_v2.json` (dedup + fallback merge).
6. **Narrative comparison.** Human-readable comparison against paper Table 2:
   `analysis/subsystem_comparison.md`, `analysis/gene_presence_comparison.md`.
7. **Report.** `report/REPORT.md` produced with the claims table, per-claim
   verdicts, scope audit, and method-substitution justification.
   Progress log: `report/PROGRESS.md`.

Backfill (2026-07-05) added:

- `paper.pdf` symlink at repo root (item 1).
- `extraction/marker.md` = layout-preserving pdftotext fallback (item 2; real
  Marker parse pending).
- `extraction/nougat.mmd` = placeholder with sha256 + DOI (item 3; GPU parse
  pending on uicgpu / Polaris corpus sweep).
- `report/REPORT.tex` = detailed LaTeX report with genuine critique (item 4).
- `report/open_questions.tex` = 5-question LaTeX insert.
- `report/open_questions.json` = machine-readable 5-question rollup (item 5).
- `report/workflow.md` = this file (item 6).
- `report/artifacts_summary.md` = inventory + checksums (item 7).
- `report/failure_analysis.md` = honest failure/critique (item 8).

## 2. Tools and Codes (with versions where captured)

| Layer | Tool | Version / Endpoint | Where used |
|-------|------|--------------------|------------|
| Genome DB | BV-BRC public REST API | live 2026-05-10 (unchanged 2026-07-05) | Steps 2, 3, 4, 5 |
| Annotation | RASTtk (BV-BRC-served) | current, delivered by BV-BRC | Steps 3, 5 |
| Ortholog | PLfam (BV-BRC) | species-level protein families, live | Step 5 |
| PDF text | Poppler `pdftotext` (layout mode) | 25.05.0 (Homebrew) | Backfill marker.md fallback |
| PDF math (planned) | Nougat (facebookresearch/nougat) | pending, requires GPU | Backfill item 3 (stub only) |
| Report render | pdflatex (TeX Live) | Homebrew | Backfill item 4 compile |
| Checksum | shasum -a 256 | macOS 25.3.0 | Backfill artifact IDs |
| Agent | OpenClaw / argo:claude-opus-4.7 (backfill) | argo :44497 | Backfill drive |
| Agent (original) | agent driver (see 2026-05-10 log) | recorded in PROGRESS.md | Original replication |

Data cached / annotated by BV-BRC:
- Genome sequences: AE016879 (K279a, 4,851,126 bp), CP001111 (R551-3,
  4,573,969 bp), HE798556 (D457, 4,769,156 bp), CP002986 (JV3, 4,544,477 bp).
- All 4 single-contig chromosomes; no plasmids retrieved.

## 3. Effort Estimate

**Original replication (2026-05-10):**
- Wall-clock: ~15 minutes end-to-end (per `report/PROGRESS.md`, 08:37 - 08:51 CDT).
- Compute: negligible; only BV-BRC API calls. No GPU. No local re-annotation.
- Agent steps: ~10-20 tool calls (paper fetch, API queries, JSON parses, MD writes).
- LOC written: none as a standalone script; work driven directly by agent tool calls.
- Data volume: ~40 KB of cached JSON + ~20 KB of analysis MD + 16 KB REPORT.md.

**Backfill (2026-07-05):**
- Wall-clock: ~20 minutes (agent-driven, one session).
- Compute: pdftotext + pdflatex on CherryRd (host-local, <5s each).
- Agent steps: ~15 tool calls (read/write/exec).
- New LOC / prose: ~600 lines of LaTeX + ~200 lines of Markdown + 5-question JSON.
- New artifacts: 6 files (paper.pdf symlink, marker.md, nougat.mmd, REPORT.tex,
  open_questions.tex, open_questions.json, workflow.md, artifacts_summary.md,
  failure_analysis.md).

**Total end-to-end effort to reach the 8-artifact bar for this paper:**
approximately 35-40 agent-minutes of driver time, plus ~30 seconds of host CPU.
No GPU used. No wet-lab. No new sequencing.

## 4. What Was Intentionally NOT Run

Documented so future backfill or extension is clear about the ceiling:
- No local RASTtk re-run (trusts BV-BRC-served annotations).
- No Prokka / Bakta cross-annotation.
- No reciprocal-best-hit BLAST for HmuT ortholog confirmation.
- No antiSMASH / PRISM BGC prediction.
- No population-genomic extension to the >200 public S. maltophilia genomes.
- No in-silico primer coverage check against BV-BRC panel.
- No HMMER search for Tbp/Lbp receptors (called out in Q4).
- No Nougat parse (called out in extraction/nougat.mmd stub).

Each of the above is called out in the failure analysis or open questions.
