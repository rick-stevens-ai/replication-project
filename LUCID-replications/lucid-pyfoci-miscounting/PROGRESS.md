# PROGRESS — PyFoci foci-miscounting replication

## Timeline

- **2026-05-29 16:29** Original PyFoci subagent launched.
- **2026-05-29 16:44** First attempt timed out after finding Python 3.14 is too new for numba; respawned with Python 3.11 instruction.
- **2026-05-29 16:56** Second attempt falsely completed: cached public code/data but wrote no REPORT/README/PROGRESS/results/figures.
- **2026-05-29 17:02** Finish-only attempt also falsely completed; no deliverables.
- **2026-05-29 17:15** Main agent took over. Verified cached artifacts: PyFoci repo, Colab notebook, public ZIP datasets, and 24 extracted parquet count datasets with 19,200 rows each.
- **2026-05-29 17:18** Wrote `code/analyze_cached_pyfoci.py`; generated per-dataset error summaries and three diagnostic figures.
- **2026-05-29 17:20** Wrote README and REPORT. Initial verdict: PARTIAL — public artifacts/data validate central miscounting claim, but full image-processing pipeline was not rerun.
- **2026-06-23 12:10** RE-PASS subagent (`agent:main:subagent:c19325df`). Marker .md was not in canonical uicgpu corpus for this DOI (paper was already an "Existing LUCID replication" entry), so reparsed PDF with `pdftotext -layout` (PDF has native text layer). Enumerated 13 testable claims; previous pass tested 6. Built `code/repass_extended.py` exercising 7 additional claims: Mann-Whitney p-values vs `P_Values_Fig1` (120/120 reproduced), Fig 4 magnification effect, Fig 5 voxel-size trend, Fig 6 deconvolution effect, Fig 7 3D analysis, Fig 8 clustering vs miscount, Fig 3 repair-kinetics bi-exp constant.
- **2026-06-23 12:14** All 7 new claims reproduce quantitatively against author-released parquet artifacts. Coverage 6→13, Agreement 7→12 (1 explicit BLOCKED on F6 Python-3.14/numba for raw image regen). Verdict lifted from PARTIAL → REPLICATED. REPORT.md updated with 8-section template, prior verdict preserved as sibling note. PARSER_PROVENANCE file written.

## Blockers / friction

- Python 3.14 default environment is incompatible with numba, which PyFoci requires.
- Subagents repeatedly completed after artifact fetch without writing audit deliverables; main agent completed final gate locally.
- The current replication uses cached parquet/count outputs, not a full rerun from raw microscope image stacks / SDDs through PyFoci.
