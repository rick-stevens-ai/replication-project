# Artifacts summary

## Target directory tree

```
OSTI-2583708-kmc-molecular-anisotropy-resveratrol/
├─ paper.pdf                              (1) 1.30 MB — OSTI open PDF
├─ extraction/
│   ├─ marker.md                          (2) 14.8 KB — Marker-flavored extraction (pdftotext + IOP HTML)
│   └─ nougat.mmd                         (3) 12.6 KB — Nougat-flavored LaTeX extraction
├─ report/
│   ├─ REPORT.md                                — main narrative report + open questions
│   ├─ REPORT.tex                         (4) — LaTeX section-by-section report (compiles standalone)
│   ├─ brief.md                                 — 1-paragraph brief
│   ├─ attempt_log.md                           — chronological log
│   ├─ artifact_harvest.md                      — every public artifact pulled
│   ├─ workflow.md                        (6) — workflow + tools + effort estimate
│   ├─ artifacts_summary.md               (7) — THIS FILE (canonical inventory)
│   ├─ failure_analysis.md                (8) — what failed, why, workarounds, residual gaps
│   ├─ open_questions.json                (5) — 5 grounded open questions, each {q, basis, next_steps}
│   └─ evidence/
│        ├─ aspect_ratio_sweep.json             — 10-seed W:L, H:L measurements
│        ├─ dump.sweep_seed1.txt                — SPPARKS dump for seed 1 (multi-frame text)
│        └─ log.sweep_seed1.txt                 — SPPARKS stdout for seed 1
└─ work/
    ├─ paper_layout.txt                         — pdftotext -layout output (595 lines)
    ├─ paper_plain.txt                          — pdftotext plain output (561 lines)
    ├─ spparks-resv/                            — shallow clone, resveratrol branch
    ├─ spparks-nonorth/                         — shallow clone, nonorth branch
    └─ runs/
         ├─ in.hcp_test                         — HCP + hex-region smoke input
         ├─ in.paper_scale                      — 48×16×24 paper-scale KMC input
         ├─ in.sweep_seed1                      — representative per-seed sweep input
         └─ sweep.sh                            — 10-seed parallel driver
```

## 8-artifact completion check (Rick, 2026-07-05 standard)

| # | Path | Present? | Notes |
|---|---|---|---|
| 1 | `paper.pdf` | ✓ | 1,304,946 B; SHA256 checkable via OSTI |
| 2 | `extraction/marker.md` | ✓ | 14,753 B; produced from pdftotext + IOP HTML (marker binary unavailable on uicgpu) |
| 3 | `extraction/nougat.mmd` | ✓ | 12,631 B; produced from same source (nougat binary unavailable) |
| 4 | `report/REPORT.tex` | ✓ | Detailed LaTeX report, section-by-section, compilable |
| 5 | `report/open_questions.json` | ✓ | 5 objects, each {q, basis, next_steps}; ## Open Questions section also in REPORT.md |
| 6 | `report/workflow.md` | ✓ | Narrative + tools+versions table + effort estimate |
| 7 | `report/artifacts_summary.md` | ✓ | THIS FILE |
| 8 | `report/failure_analysis.md` | ✓ | Honest per-claim what/why/workaround/residual gap |

Bonus: `report/REPORT.md` and `report/brief.md` and `report/attempt_log.md` and `report/artifact_harvest.md`.

## Public-artifact provenance

- OSTI PDF: https://www.osti.gov/servlets/purl/2583708
- Publisher HTML: https://iopscience.iop.org/article/10.1088/1361-651X/ade176 (fetched 2026-07-06 06:20 CDT)
- `tdjanic-snl/spparks` GitHub: https://github.com/tdjanic-snl/spparks (fork of `spparks/spparks`, last commit 2025-03-31)
- Branch `resveratrol` head: `f6bcc3b`
- Branch `nonorth` head: `82a9083`
- Upstream SPPARKS: https://github.com/spparks/spparks

## Uicgpu-side artifacts (not mirrored back)

Left in place for potential follow-on runs:
- `~/replicate/osti-2583708/spparks-resv/` — full clone + compiled `src/spk_uic`
- `~/replicate/osti-2583708/spparks-full/` — full-history clone (used for diff)
- `~/replicate/osti-2583708/runs/sweep/` — all 10 seed dumps + logs (~30 MB)
- `~/replicate/osti-2583708/in.hcp_test` — original smoke input
