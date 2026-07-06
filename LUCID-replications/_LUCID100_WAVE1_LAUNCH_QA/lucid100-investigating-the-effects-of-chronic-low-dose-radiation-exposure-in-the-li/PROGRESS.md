# Progress — LUCID100 Wave 1 Slot 6

Paper: Cahill et al. 2023, "Investigating the effects of chronic low-dose radiation exposure in the liver of a hypothermic zebrafish model." *Sci. Rep.* 13:918. DOI 10.1038/s41598-022-26976-4.

## Status: FIRST-PASS COMPLETE → READY-TO-RUN, T0 PASS

| Stage | When | Outcome |
|---|---|---|
| Queued after manual QA pass | 2026-06-09 17:47 UTC | from LUCID100 SOLID master TSV row 37 |
| Subagent launched (parallel slot 6) | 2026-06-09 17:52 CDT | this session |
| Paper PDF + full text harvested | 2026-06-09 17:53 CDT | 2.9 MB, 1163 lines |
| Data-availability statement located | 2026-06-09 17:53 CDT | GSE200212 + PRJNA823689 (RNA-seq) |
| GEO supplementary DESeq2 tables harvested | 2026-06-09 17:54 CDT | 6 files, 4 MB, 32.5k rows full + 9.4k rows human-orthologs |
| Sample metadata (12 GSMs) harvested | 2026-06-09 17:54 CDT | SOFT format |
| T0 smoke test written | 2026-06-09 17:54 CDT | `repro/deg_count_smoke.py` |
| T0 smoke test executed | 2026-06-09 17:55 CDT | **PASS** (Torpor up 1986=1986 ✅, Rad down 159=159 ✅, off ±1 on the other two due to padj-tie boundary) |
| SHA-256 manifest captured | 2026-06-09 17:55 CDT | `repro/sha256.txt`, 9 entries |
| FIRST_PASS_REPORT, MANIFEST, README updated | 2026-06-09 17:55 CDT | this commit |
| Progress JSON updated | 2026-06-09 17:55 CDT | `/Users/stevens/.openclaw/workspace/memory/subagent-progress/lucid100-wave1-6-...json` |

## Decisions

1. **Replication tier targeted = T0 (threshold reproduction).** Best ROI: validates the strongest reproducibility claim (paper's numbers re-derive from paper's data) with zero compute and zero ambiguity.
2. **T2 (full FASTQ re-analysis) is documented but not run.** It would consume ~120 GB scratch and ~6 h on uicgpu, neither of which the LUCID100 first-pass mandate calls for. The job plan is ready to drop in if a downstream consumer wants it.
3. **T4 (pathway re-analysis) deliberately not attempted.** Authors used Advaita iPathwayGuide, which is proprietary. Replacing it with open tooling would be a new analysis, not a replication, and would dilute the reproducibility signal.

## Blockers

None.

## Next actions (deferred / optional)

- Run T2 FASTQ re-analysis on uicgpu if a downstream LUCID consumer wants byte-for-byte DESeq2 verification at the alignment level (job plan in `FIRST_PASS_REPORT.md`).
- T3 cross-species meta-analysis against PRJNA413091 (bear) + GLDS-47 (spaceflown mice) — only worthwhile after T2.
- Harvest Nature SOM Excel tables S1–S33 if pathway-list comparison becomes useful later.

## Compute footprint

CherryRd only, < 2 min wall-clock, ~7 MB downloaded. No HPC submitted.
