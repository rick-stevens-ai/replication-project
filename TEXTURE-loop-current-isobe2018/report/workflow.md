# Workflow — Isobe-Yuan-Fu 2018 replication

1. **Fetch/extract.** `paper.pdf` present. `pdftotext -layout paper.pdf` recovered
   the full text + equations (text layer intact; no OCR/vision). See
   `extraction/marker.md`.
2. **Kernel review (required).** Read the TEXTURES-100 shared kernel
   `loop_current_kagome_kernel.py`. Determined it is a kagome tight-binding +
   Peierls-flux loop-current kernel — a DIFFERENT physics class. Flagged the
   kernel as out-of-scope for this paper's core; reused only the conceptual
   "coupling -> ordering channel selection" idea. See `code/PROVENANCE.md`.
3. **Identify machine-checkable claims.** Picked 5 concrete claims tied to
   Eqs. (9)-(24) and Sec III B-C / Fig. 4-5.
4. **Implement core.** `code/isobe2018_rg.py`: RG beta-functions (9)-(15),
   interaction strengths (17)-(23), RPA divergence (16)/(24), SciPy RK45 flow.
5. **Run checks.** `code/run_checks.py` -> `work/results.json` +
   `work/rg_flow_and_phase.png`. Real numerical integration, no transcribed numbers.
6. **Compare quantitatively.** Each claim has a pass/fail with computed metrics
   (see `artifacts_summary.md`). 5/5 pass.
7. **Report.** REPORT.tex (+PDF if latex), open_questions.json (5),
   workflow.md, artifacts_summary.md, failure_analysis.md.

## Reproduce
```
cd code && python3 run_checks.py     # numpy>=2, scipy>=1.18, matplotlib
```
