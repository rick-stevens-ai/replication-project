# Workflow — arXiv:1507.00432 replication

## Timeline (2026-07-05, single session)

| Time (rel) | Step | Output |
|---|---|---|
| 00:00 | Read QC_WAVE_BRIEF + REPLICATION_DIR_STANDARD | requirements confirmed (8 artifacts, verdict, WAVE_RESULT line) |
| 00:01 | Fetch `paper.pdf` from arxiv.org/pdf/1507.00432 | 388 KB, 31 pages, PDF v1.4 |
| 00:02 | `pdftotext -layout` skim; verify title + authors | ✓ "Approximate Span Programs" by Ito & Jeffery |
| 00:04 | Search REPLICATE-PROJECT tree for pre-parsed extractions | none found |
| 00:05 | Run PyMuPDF `fitz` on paper.pdf → `extraction/marker.md` (surrogate) | 94 KB, 31 pages, header labeled |
| 00:05 | Run `pdftotext -layout` → `extraction/nougat.mmd` (surrogate) | 144 KB, header labeled |
| 00:06 | Read Sec 1.1, 2.1, 2.2, 2.3, 2.4 of the paper for formal definitions | Def 2.1, 2.2, 2.4, 2.5, Thm 2.3, 2.10 identified |
| 00:15 | Write `span_programs.py`: SpanProgram class + w_+, w_-, e_+ | 533 LOC |
| 00:20 | Build OR_n, AND_n, 3-EDGE-DETECTION examples + main driver | verified truth-tables |
| 00:22 | Run script; first pass OR clean, AND showed n>=6 anomaly (W_- collapsed) | root-caused: sampled only 0^n, not single-zero pattern |
| 00:24 | Fix AND single-zero sampling; rerun | ratio C/Q = 1.000 for all n |
| 00:26 | Write REPORT.tex (7 sections + claims table + open questions Q1..Q5) | 18 KB |
| 00:28 | Write open_questions.json (5 with next_steps) | 4.9 KB |
| 00:29 | Write workflow.md, artifacts_summary.md, failure_analysis.md | this file + 2 others |
| 00:30 | Attempt LaTeX compile (pdflatex or tectonic) | see failure_analysis.md |
| 00:31 | Final WAVE_RESULT | REPLICATED |

## Tools / codes / versions

| Tool | Version | Purpose |
|---|---|---|
| Python | 3.14.6 (CPython, macOS Darwin 25.3.0) | driver |
| numpy | 2.x | linear algebra |
| PyMuPDF (fitz) | 1.27.2.3 | Marker surrogate extraction |
| Poppler pdftotext | (system) | Nougat surrogate extraction, paper skim |
| curl | (system) | fetching arXiv PDF |
| pdflatex or tectonic | attempted for REPORT.pdf | see failure_analysis.md |
| standard shell tools | grep, sed, wc | text manipulation |

## Code

- `report/evidence/span_programs.py` (533 LOC) — full implementation of Def 2.1, 2.2, 2.4, 2.5; three example span programs; approximate + Thm 2.10 verification; main driver writes `report/evidence/results.json`.

## Outputs / evidence

- `report/evidence/span_programs.py` — the code.
- `report/evidence/results.json` — machine-readable numerical results (Def 2.2 witness sizes, Def 2.4 errors, Thm 2.10 identity products, complexity ratios).
- `report/evidence/run_log.txt` — human-readable stdout capture.

## Effort estimate

- **Wall clock:** ~31 minutes (single agent session, no waiting on external services).
- **Compute:** 0.04 seconds of numpy on a 2020-era MacBook (`main()` runtime). Negligible.
- **Human/agent steps:** ~35 tool calls (read, write, edit, exec).
- **LOC written:** 533 (span_programs.py) + ~330 (REPORT.tex) + ~100 (5 open questions + workflow.md + this file's peers).
- **Runs executed:** 2 (initial + post-AND-fix rerun).
- **No LLM inference used** in the replication itself (the Argo endpoint was available but the QC-200 core is pure linear algebra — no need to spend tokens on it).

## Reproducibility

Full reproduction from scratch:
```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-200/QC-1507.00432-approximate-span-programs-ito-jeffery
python3 report/evidence/span_programs.py | tee report/evidence/run_log.txt
```

Outputs are deterministic (no randomness) modulo numpy floating-point non-associativity in KKT solve; all reported values agree with the analytic formulas to $\sim 10^{-15}$.
