# Workflow Documentation

**Slot:** `lucid-sachs-systems-bio-radiation-cancer-slot65`
**Paper:** Little MP, Heidenreich WF, Moolgavkar SH, Schöllnberger H, Thomas DC (2008), *Radiation and Environmental Biophysics* 47:39–47.
**DOI:** 10.1007/s00411-007-0150-z
**Auditor:** Ollie (LUCID subagent), 2026-06-22
**Backfill:** Kukla (subagent), 2026-07-06

## Slot-Name Note

The queue-assigned slot slug names "Sachs" (probably auto-tagged from a related paper in the same 2007 workshop proceedings), but the paper delivered and audited is by Little et al. Rainer K. Sachs's two-track / TE-CE / dual-radiation-action work is NOT the subject here. Audit substance below is against the Little et al. paper actually on disk.

## Pipeline

### Step 1: Paper Retrieval
- **When:** 2026-06-09
- **Source:** Springer OA DOI landing page for `10.1007/s00411-007-0150-z`
- **How:** Follow 303 redirect chain (captured to `artifacts/page_headers.txt`); no paywall, no captcha; CC BY-NC license.
- **Output:** `artifacts/paper.pdf` (378 KB, 9 pp)

### Step 2: Text Extraction
- **How:** Local `pdftotext` (poppler); no OCR needed (PDF has embedded text layer)
- **Output:** `artifacts/paper.txt` (1,159 lines)

### Step 3: Structural Read
- Identified paper as 9-page workshop summary of 5 separate talks (GSF, 14–16 Feb 2007)
- Enumerated 5 talks × ~2 substantive claims each ≈ 8 testable quantitative claims (C1–C8)
- Classified each claim: equation-level (reproducible from paper alone) vs data-level (needs primary paper's microdata)

### Step 4: Equation-Level Re-Implementation
- **File:** `code/smoke_replication.py`
- Two-stage MVK / TSCE closed-form hazard (Heidenreich-Jacob-Paretzke 1997 form), 3 illustrative parameter sets
- SVM bystander skeleton: `T(D, k_ap)` = direct LQ + bystander removal `R_max · (1 − exp(−k_ap·t_int)) · D/(D+D_half)`
- Uses numpy + matplotlib (Agg backend) only
- Wall time: < 2s on laptop

### Step 5: Claim Audit
- **File:** `code/claim_audit.py`
- Enumerated ledger over C1–C8
- Analytic vs numerical spot-checks for C2 (MVK plateau: rel error 1.4e-9)
- Age-tabulation for C3 (monotone confirmed)
- Dose-tabulation for C4 (U-shape + k_ap ordering confirmed)
- Newton–Raphson MLE on synthetic case-control (n=8000) for C5 (logit skeleton recovery)
- C1, C6, C7, C8 marked SPOT-CHECK or DATA-BLOCKED with exact missing artifact named

### Step 6: Verdict Assignment
- **Verdict:** PARTIAL (4 VERIFIED equation-level; 3 DATA-BLOCKED; 1 SPOT-CHECK)
- Rationale: PARTIAL driven by *scope* (data-blocked dataset claims), not *disagreement* (no contradictions)
- Coverage 5/10; Agreement 9/10

### Step 7: Backfill (2026-07-06, Kukla subagent)
- Read existing `REPORT.md` (top-level, preserved in place)
- Generated `report/REPORT.tex` (LaTeX with genuine Critique section)
- Generated `report/open_questions.json` (5 open questions, bare-list format)
- Generated `report/open_questions_section.tex` (included in REPORT.tex)
- Generated `report/workflow.md` (this file)
- Generated `report/artifacts_summary.md`
- Generated `report/failure_analysis.md`
- Generated `extraction/nougat.mmd` stub
- No simulations re-run; no external endpoints called; no author contact

## Tools Used

- `pdftotext` (Poppler)
- Python 3 stdlib
- numpy
- matplotlib (Agg backend)

## Tools NOT Used

- LLM judgment (no API calls in audit path)
- SEER*Stat (would require user registration)
- Author contact (against LUCID protocol)
- Paid endpoints (none)
- Nougat / Marker (paper had embedded text layer; stub file created for pipeline compat)

## Reproduction Instructions

```bash
cd /Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid-sachs-systems-bio-radiation-cancer-slot65/
python3 code/smoke_replication.py | tee reports/smoke_run_rerun.txt
python3 code/claim_audit.py        | tee reports/claim_audit_run.txt
```

Expected: both scripts exit 0 in <3s combined; assertions all pass; `reports/*.png` + `reports/claim_audit.json` regenerated.

## LaTeX Build (optional)

```bash
cd report/
pdflatex REPORT.tex
pdflatex REPORT.tex   # second pass for cross-references
```
