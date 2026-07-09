# Artifacts Summary — lucid100-dsb-repair-theoretical-framework

## Layout

```
lucid100-dsb-repair-theoretical-framework/
├── README.md, MANIFEST.json, PROGRESS.md          # meta
├── REPORT.md                                       # canonical audit (2026-06-22)
├── FIRST_PASS_REPORT.md                            # original first-pass (2026-06-09)
├── artifacts/                                      # data + outputs
│   ├── paper.pdf                                   # primary source, 649 KB CC BY 4.0
│   ├── paper.xml                                   # JATS full text, 104 KB
│   ├── paper_unpaywall_s2_acquired.pdf             # provenance duplicate
│   ├── smoke_results.json                          # 6/6 qualitative checks PASS
│   ├── closure_validation.json                     # SSA-vs-ODE RMS both closures, both lines
│   ├── closure_validation_MDA-MB-468.csv           # full SSA vs (2.5) vs (2.8) trajectories
│   ├── closure_validation_MCF7.csv                 # same for MCF7
│   ├── ssa_exact_mda468.json                       # exact-Gillespie cross-check
│   └── claim_audit.json                            # 16-entry machine-readable claim table
├── scripts/                                        # implementation
│   ├── smoke_model.py                              # ODE smoke + qualitative checks
│   ├── scripts_ssa.py                              # vectorised tau-leap SSA (eq 2.1)
│   ├── ssa_exact.py                                # exact-Gillespie cross-check
│   ├── closure_validation.py                      # Fig-3 quantitative replication
│   └── claim_audit.py                              # claim table generator
├── extraction/
│   └── nougat.mmd                                  # stub — see below
├── notes/                                          # (empty)
└── report/                                         # backfilled artifacts (2026-07-06)
    ├── REPORT.tex                                  # LaTeX audit summary
    ├── open_questions.json                         # 5 open questions machine-readable
    ├── open_questions_section.tex                  # LaTeX mirror of open_questions.json
    ├── workflow.md                                 # end-to-end workflow
    ├── artifacts_summary.md                       # this file
    └── failure_analysis.md                         # honest critique
```

## Key artifact provenance

| File | Source | Provenance |
| --- | --- | --- |
| `artifacts/paper.pdf` | EuropePMC PMC4759787 render | CC BY 4.0; sha256 `5dd2700d10bf1c4c95d8ecdd46c22da57a3544c97dda1161cbadb45d4d8433ef` |
| `artifacts/paper.xml` | EuropePMC REST fullTextXML | JATS 1.1; md5 `17b5fb806d45e3d4141298151616d748` |
| `artifacts/paper_unpaywall_s2_acquired.pdf` | S2 / Unpaywall | byte-identical to primary (provenance duplicate) |
| Table 1 constants | in-paper Table 1, both cell lines | used verbatim; hard-coded in `scripts/claim_audit.py` |
| Table 2 constants | in-paper Table 2 | used verbatim |
| Fig 4 raw foci/OTM | none deposited | figure-only in this paper AND cited refs [12,17] — blocker #1 |
| Fig 7e antibody sweep | none deposited | figure-only — blocker #2 |
| Fig 8b clonogenic-vs-R | none deposited | figure-only, ref [17] — blocker #3 |
| Author MATLAB / SSA code | none | not released |

## Output artifact key numbers

- `smoke_results.json`:
  - MDA468 24h endpoint: <X>=0.39, peak <Z>=73 at t=0.49h
  - MCF7 24h endpoint: <X>=0.040, peak <Z>=49 at t=0.10h
  - Auger AUC monotone: R=0,2,4,6,8 → 5.4, 21.8, 29.3, 33.4, 36.0
- `closure_validation.json`:
  - MDA468 [0,6h] ad-hoc RMS: X=0.045, Y=11, Z=56 (SSA peak Z≈445)
  - MCF7  [0,0.6h] ad-hoc RMS: X=0.030, Y=78, Z=243 (SSA peak Z≈800)
- `ssa_exact_mda468.json`:
  - Exact Gillespie at t=1h (n=100): <X>=0.900, <Y>=75.4, <Z>=369.5
  - Bare eq (2.5) at same t: X=0.862, Y=80.7, Z=403 → 5–10% agreement
- `claim_audit.json`:
  - MCF7 stability ratio k₃k₅/(k₄k₆) = 1.000374 (UNSTABLE)
  - MDA468 stability ratio = 0.986850 (stable, marginal)
  - k₅=0 slowdown: MDA468 8.45×, MCF7 11.2× vs paper "approx 10×"

## Extraction status

- **`extraction/nougat.mmd`** is a **stub pointer file**, not a GPU-parsed nougat output.
- Reason: text was extracted from the JATS XML (`artifacts/paper.xml`) directly rather than
  from PDF-OCR. Equations, tables, and inline math are cleaner in JATS than in nougat for
  this paper.
- Stub file contains: paper.pdf sha256, decision to use JATS XML, and pointer to
  `artifacts/paper.xml` as the canonical extracted text.
- If a full GPU nougat parse is later desired, run on uicgpu A100 or spark; expected
  runtime ~2–3 min for a 649 KB paper.

## Verdict cross-check (2026-07-06 backfill)

- LUCID-100 queue tag: **REPLICATED**
- Audit (REPORT.md + this backfill): **PARTIAL** (coverage 8/10, agreement 7/10)
- **Verdict preserved: PARTIAL**. Queue tag flagged as inconsistent. See
  `failure_analysis.md` for reasoning.
