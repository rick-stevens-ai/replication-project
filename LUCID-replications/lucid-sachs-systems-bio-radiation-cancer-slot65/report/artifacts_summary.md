# Artifacts Summary

**Slot:** `lucid-sachs-systems-bio-radiation-cancer-slot65`
**Paper:** Little et al. (2008) *Radiat Environ Biophys* 47:39–47
**Verdict:** PARTIAL

## Top-Level Files (Pre-Existing, Preserved)

| File | Purpose |
|------|---------|
| `REPORT.md` | Authoritative on-disk audit report (8-section template) |
| `README.md` | Paper framing + reproduce instructions |
| `PROGRESS.md` | Chronological journal |
| `FIRST_PASS_REPORT.md` | First-pass narrative verdict (pre-audit) |
| `ARTIFACT_MANIFEST.md` | Enumerated obtained vs missing artifacts |

## Directory Layout

```
lucid-sachs-systems-bio-radiation-cancer-slot65/
├── REPORT.md                    (top-level; authoritative; preserved)
├── README.md
├── PROGRESS.md
├── FIRST_PASS_REPORT.md
├── ARTIFACT_MANIFEST.md
├── artifacts/
│   ├── paper.pdf                (Springer OA, 378 KB, 9 pp)
│   ├── paper.txt                (pdftotext extract, 1159 lines)
│   └── page_headers.txt         (Springer 303 redirect chain)
├── code/
│   ├── smoke_replication.py     (MVK hazard + SVM bystander figures)
│   └── claim_audit.py           (8-claim ledger, analytic spot-checks)
├── reports/
│   ├── mvk_hazard.png           (Fig-4-shape comparison)
│   ├── svm_bystander.png        (Fig-5-shape comparison)
│   ├── smoke_run.txt            (original smoke stdout)
│   ├── smoke_run_rerun.txt      (2026-06-22 audit re-run)
│   ├── claim_audit_run.txt      (human-readable ledger)
│   └── claim_audit.json         (machine-readable ledger)
├── report/                      (backfill 2026-07-06)
│   ├── REPORT.tex               (LaTeX report with Critique + Open Questions)
│   ├── open_questions.json      (5 open Qs, bare-list format)
│   ├── open_questions_section.tex
│   ├── workflow.md              (pipeline documentation)
│   ├── artifacts_summary.md     (this file)
│   └── failure_analysis.md
└── extraction/
    └── nougat.mmd               (stub; paper had embedded text layer)
```

## Obtained (Primary Analytic Inputs)

| Item | Path | Size | Notes |
|------|------|------|-------|
| Paper PDF | `artifacts/paper.pdf` | 378 KB | Springer OA, CC BY-NC |
| Paper text | `artifacts/paper.txt` | 1159 lines | `pdftotext` extract |
| Redirect trace | `artifacts/page_headers.txt` | small | Springer 303 chain |

## Generated Figures

| Figure | Path | What It Shows |
|--------|------|---------------|
| MVK hazard sweep | `reports/mvk_hazard.png` | Three-parameter TSCE hazard vs age, matches Fig 4 shape |
| SVM bystander U-shape | `reports/svm_bystander.png` | Two-panel dose-response (immediate + delayed), matches Fig 5 shape |

## Generated Machine-Readable Ledger

- `reports/claim_audit.json` — Structured C1–C8 records with numeric values, tolerance, pass/fail
- `reports/claim_audit_run.txt` — Human-readable print log

## NOT Obtained (Named Missing Artifacts — Data-Blockers)

| # | Artifact | Blocks Claim | Access Path (out of LUCID scope) |
|---|----------|--------------|----------------------------------|
| 1 | SEER colon-cancer per-age incidence by sex, 1973–2002 | C6 | SEER*Stat user registration |
| 2 | Little & Wright 2003 generalized-MVK fitter (k+m stage, Poisson-likelihood) | C6 | Never released; would require re-implementation (~1 LUCID slot) |
| 3 | Little & Li 2007 model-comparison harness (5-variant SEER refit + P-values) | C6 | Never released; ~1 LUCID slot |
| 4 | JANUS lung-cancer per-mouse follow-up (Heidenreich ref [18]) | C7 | Internal ANL/GSF archival request |
| 5 | Heidenreich-Luebeck-Hazelton 2002 Thorotrast posterior (μ₀, N, α, β, μ₁) | C8 | Not machine-readable; digitize tables + MC refit |
| 6 | Redpath 2001 CGL1 transformation per-dose per-replicate raw data | k_ap CI recomputation | Not publicly archived; UI/UMass contact |
| 7 | WECARE de-identified genotype + dose + case-status microdata (Bernstein ref [64]) | Full C5 (WECARE result itself) | Consortium DAC / IRB-cleared |
| 8 | Schöllnberger Salzburg-group SVM solver source | k_ap CI recomputation | Not archived; direct group request |

## Claim Ledger Summary

| Verdict | Count | Claim IDs |
|---------|-------|-----------|
| VERIFIED (equation-level) | 4 | C2, C3, C4, C5 |
| SPOT-CHECK | 1 | C1 |
| DATA-BLOCKED | 3 | C6, C7, C8 |
| DISCREPANT | 0 | — |
| **Total** | **8** | — |

## Backfill Artifacts Added (2026-07-06)

7 files under `report/` and `extraction/` — all documentation/format-normalization; zero simulation re-runs; zero external endpoint calls; original `REPORT.md` preserved at top level.
