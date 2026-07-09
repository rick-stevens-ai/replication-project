# Artifacts summary — Brahme (2024) LUCID slot

## Provenance

- **Paper source URL:**
  `https://gavinpublishers.com/assets/articles_pdf/New-Radiation-Oncology-Optimization-Principles--Based-On-In-Vivo-Predictive-Assay-and-Recent-Developments-in-Molecular-Radiation-Biology.pdf`
- **DOI:** `10.29011/2574-7754.101625`
- **Venue:** *Annals of Case Reports* 9:1625 (Gavin Publishers), 2024.
- **paper.pdf SHA-256:** `b768585e326b83b9e51165978c9fe3a1a9711d369762ea65b442e9077fcd00b9`
- **paper.pdf size:** 4,693,885 bytes (4.69 MB), PDF 1.7.

## Files, sizes, roles

| Path | Size | Role | Notes |
|---|---:|---|---|
| `paper.pdf` | 4,693,885 B | Primary source | OA download from Gavin Publishers 2026-06-09 |
| `paper.txt` | 208,293 B | `pdftotext -layout` extract | 2,159 lines; used for manual re-read |
| `README.md` | 4,602 B | Slot README | Original slot metadata + reproducer |
| `PROGRESS.md` | 3,355 B | Chronological log | 2026-06-09 → 2026-06-25 events |
| `FIRST_PASS_REPORT.md` | 5,439 B | First-pass narrative | 2026-06-09 pass |
| `REPORT.md` | 15,133 B | Canonical narrative + retier banner | 2026-06-22 + 2026-06-25 |
| `artifacts/MANIFEST.md` | 2,569 B | Artifact manifest | Original |
| `smoke/p_plus_smoke.py` | 6,842 B | Eq.(1) reproducer | 216 LOC, numpy+matplotlib |
| `smoke/eq1_internal_consistency.py` | 5,270 B | 6-limit algebra harness | 144 LOC, 19/19 PASS |
| `figs/p_plus_smoke.png` | 170,962 B | 4-panel plot | δ sweep, γ_C sweep |
| `figs/p_plus_smoke.csv` | 71,233 B | 1001-row dose grid | Machine-readable |
| `extraction/marker.md` | (backfill) | pdftotext-derived stub | 2026-07-06 |
| `extraction/nougat.mmd` | (backfill, stub) | Pending GPU parse pointer | 2026-07-06 |
| `report/REPORT.tex` | (backfill) | LaTeX report | 2026-07-06 |
| `report/open_questions.json` | (backfill) | 5-object open-questions list | 2026-07-06 |
| `report/open_questions_section.tex` | (backfill) | LaTeX mirror | 2026-07-06 |
| `report/workflow.md` | (backfill) | Workflow narrative | 2026-07-06 |
| `report/artifacts_summary.md` | (backfill) | This file | 2026-07-06 |
| `report/failure_analysis.md` | (backfill) | Failure + critique | 2026-07-06 |

## Numerical headline results (audit)

```
delta=0.00 -> P+_max = 0.503 at D*=62.9 Gy
delta=0.20 -> P+_max = 0.512 at D*=63.1 Gy
delta=1.00 -> P+_max = 0.554 at D*=63.9 Gy
high LET  , delta=0.2 -> P+_max = 0.474 at D*=61.4 Gy
Algebra limits (L1..L6): 19/19 PASS, max|err|=1.1e-16
```

## Missing / pending

- `extraction/nougat.mmd` — no GPU parse attempted during this backfill;
  pending central Nougat corpus sweep. Resolvable by paper.pdf SHA-256
  `b768585e326b83b9e51165978c9fe3a1a9711d369762ea65b442e9077fcd00b9`
  against `/eagle/projects/AuroraGPT/stevens/scout_corpus/mmd/`.
- Figure 15 tabular insert (γ_C / σ_D/D̄ / RBE per modality) — not
  recovered by `pdftotext`; would need Marker or Nougat.
- No external accessions (no Zenodo, no Dryad, no PDB, no GEO, etc.)
  because the paper releases no data.

## Verdict + provenance summary

- **Priority-queue verdict:** REPLICATED (preserved).
- **Corpus retier (2026-06-25):** NO-GO for LUCID-100 promotion — the
  paper is a review/opinion piece in a predatory-adjacent venue with
  no reproducible primary artifact.
- **What was actually replicated:** Eq.(1) formalism only
  (Coverage 4/10, Agreement 7/10 on what is analytically checkable).
