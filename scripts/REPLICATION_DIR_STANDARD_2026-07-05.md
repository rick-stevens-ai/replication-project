# Replication Working-Directory Standard (Rick, 2026-07-05) — MANDATORY for EVERY paper replication

Every paper-replication working directory (QC-100, QC-200, LUCID, PDE, BVBRC, OSTI, and all
future sets) MUST contain the following 8 artifacts. This is the canonical completion bar.
"Done" = all 8 present and real. Do not mark a replication complete without them.

## The 8 required artifacts

1. **Original PDF** — the source paper PDF.
   - Path: `<dir>/paper.pdf` (or `work/<arxiv_id>.pdf`; a copy/symlink at `<dir>/paper.pdf` preferred).

2. **Marker text extraction (.md)** — full-paper Marker parse.
   - Path: `<dir>/extraction/marker.md`.
   - Source of truth for the Marker parse is the central corpus if already parsed (SCOUT/LUCID/OSTI
     manifests on Eagle); copy the resolved .md into the dir. If not yet parsed, run Marker.

3. **Nougat text extraction (.mmd)** — full-paper Nougat parse.
   - Path: `<dir>/extraction/nougat.mmd`.
   - Same rule: copy from the central Nougat manifest if available, else run Nougat.

4. **LaTeX replication report (very detailed), section by section** — what worked, what didn't work, etc.
   - Path: `<dir>/report/REPORT.tex` (compile to `report/REPORT.pdf` when possible).
   - Detailed, section-by-section: paper summary; claims table (C1..Cn, type/testable?/tested?);
     numbered method (exact data sources, tool versions, commands); results-vs-paper tables;
     per-claim what-worked / what-didn't; verdict + justification.
   - The existing markdown REPORT.md may remain, but the LaTeX detailed report is now required.

5. **Five open questions (heavy-duty, solid, important) — each with next steps.**
   - Path: `<dir>/report/open_questions.json` = list of 5 objects
     `{"q": "...", "basis": "...", "next_steps": "..."}`, plus an `## Open Questions` section in
     the report (Q1..Q5). NOT superficial, NOT generic paper "future work". Each grounded in what
     the replication actually surfaced, and each with concrete next steps to pursue it.

6. **Comprehensive workflow + tools/codes + effort estimate.**
   - Path: `<dir>/report/workflow.md`. Full workflow narrative; enumerated list of every tool and
     code/script used (with versions); and an estimate of work done to replicate (compute time,
     wall-clock, human/agent steps, LOC written, runs executed).

7. **Summary of all artifacts and traces of the replication.**
   - Path: `<dir>/report/artifacts_summary.md`. Inventory of every artifact produced/pulled (files,
     URLs, accessions, sizes, checksums where easy) and traces (logs, run records, evidence files).

8. **Failure analysis of the replication.**
   - Path: `<dir>/report/failure_analysis.md`. Honest analysis of what failed, why (root cause),
     what was worked around, residual gaps, and what would be needed to close them. Even for clean
     REPLICATED verdicts, document friction/partial mismatches/assumptions.

## Canonical directory layout
```
<SET>/<paper-dir>/
  paper.pdf                     # (1)
  extraction/marker.md          # (2)
  extraction/nougat.mmd         # (3)
  report/REPORT.tex             # (4) + REPORT.pdf when compiled
  report/open_questions.json    # (5)
  report/workflow.md            # (6)
  report/artifacts_summary.md   # (7)
  report/failure_analysis.md    # (8)
  report/evidence/              # real outputs (json/csv/logs/figures/code)
  work/                         # code + downloaded data + intermediates
```

## Enforcement
- New replications: wave briefs require all 8 before printing WAVE_RESULT.
- Existing replications (~580): backfill pass fills the missing artifacts. Marker/Nougat pulled from
  central manifests where already parsed; LaTeX report + items 5-8 generated from the existing
  REPORT.md + evidence via free-endpoint agent pass (no re-running the sim unless report is absent).
- Completion check script: `scripts/check_repl_dir_standard.py` (audits all 8 per dir).
