# Artifact manifest — slot 65

## Primary paper artifacts

| Path | Source | Size | License | Notes |
|------|--------|------|---------|-------|
| `artifacts/paper.pdf` | `https://link.springer.com/content/pdf/10.1007/s00411-007-0150-z.pdf` | 378 KB, 9 pp | Open Access (CC BY-NC) | Full primary paper; downloaded 2026-06-09 14:53 CDT. |
| `artifacts/paper.txt` | local `pdftotext` of paper.pdf | 1,159 lines | derived | Extraction for grep/citation purposes. |
| `artifacts/page_headers.txt` | HTTP headers from a redirect probe of the article landing page | small | n/a | Captured during fetch; confirms Springer 303 redirect chain. |

## Code / outputs

| Path | Purpose | Run-time | External deps |
|------|---------|----------|---------------|
| `code/smoke_replication.py` | Shape-level replication of (A) 2-stage MVK / TSCE hazard curve and (B) State-Vector Model protective-bystander U-shape | <2 s on laptop | numpy, matplotlib only |
| `reports/smoke_run.txt` | Captured stdout from the smoke run (parameter values, spot-check hazards, asserts passed) | n/a | — |
| `reports/mvk_hazard.png` | Age-incidence MVK curves, three parameter variants, log-y, ages 0–90 | n/a | — |
| `reports/svm_bystander.png` | Two-panel SVM: immediate plating (kap=0.022/d) and delayed plating (kap=0.054/d), dose 0–1 Gy, showing direct/bystander/total | n/a | — |

## Code / data NOT obtained

| What | Why not | Effort needed to obtain |
|------|---------|-------------------------|
| Original SVM source code (Schöllnberger 2007) | No code archive cited; would require author contact (excluded by task). | Email Schöllnberger group; not attempted. |
| Generalized MVK code from Little & Wright 2003 | No code release announced in either paper; published as math only. | Reimplementation from equations (a separate LUCID slot). |
| Heidenreich 2-step radon/JANUS fitting code | Internal GSF Fortran/Mathematica — not public. | Reimplementation from Heidenreich 1997 RR + Heidenreich 1999 RR. |
| SEER colon-cancer data tables used in Fig. 4 | Publicly available from `seer.cancer.gov` but require registration + SEER\*Stat extraction. | Out of scope for a shape-only smoke. |
| WECARE individual-level data | Restricted-access human-subjects data; would need an Institutional Data Access Committee request. | Not attainable in a backfill slot; excluded by task (no author contact, no paid access). |

## Equations / parameters captured from the paper body

- `logit Pr(Yᵢ = 1) = α + Σⱼ βⱼ Xᵢⱼ + γ Zᵢ` (Thomas/WECARE first-level model).
- Schöllnberger SVM bystander rate `kap = 0.054 /day` (delayed plating, 95% CI 0.031–0.078)
  and `kap = 0.022 /day` (immediate plating, 95% CI 0.007–0.036).
- (Schematic only) Generalized MVK with `k` cancer-stage mutations × `m` destabilizing
  mutations, with arrows for asymmetric/symmetric division and mutation (Fig. 3).
- Little & Li 2007 model selection: best-fit = 2-stage 1-destabilization (Little-Wright 2003)
  and 2-stage of Nowak et al. 2002; 4-stage Luebeck-Moolgavkar "not markedly inferior";
  5-stage 2-destabilization fitted "particularly poorly (P < 0.01)".
- Quantitative cellular mutation-rate elevation after genomic destabilization: ≥ 10,000×
  (Little & Li 2007), consistent with Loeb's 10,000–100,000× chromosomal-abnormality estimates.
