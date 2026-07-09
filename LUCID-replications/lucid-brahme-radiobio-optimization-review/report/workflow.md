# Workflow — LUCID slot: Brahme (2024) radiobio optimization review

Set: LUCID
Slot: LUCID-100 Wave 6 / slot 60 / master-TSV rank 91
Paper: Brahme A, "New Radiation Oncology Optimization Principles ...", *Annals of Case Reports* 9:1625, 2024. DOI 10.29011/2574-7754.101625.
Auditor host: CherryRd (Darwin 25.3.0, x64), Python 3, numpy, matplotlib.
Backfill host: same, 2026-07-06.
Endpoints: **none needed** — the paper contains no fittable data. All numerical work was CPU-only local Python.

## Chronology

1. **2026-06-09 (first pass, Ollie).**
   - Fetched paper.pdf (4.69 MB) from
     `gavinpublishers.com/assets/articles_pdf/New-Radiation-Oncology-Optimization-Principles--Based-On-In-Vivo-Predictive-Assay-and-Recent-Developments-in-Molecular-Radiation-Biology.pdf`.
   - `pdftotext -layout paper.pdf paper.txt` → 208 KB, 2,159 lines.
   - Attempt to use the internal `pdf` extraction tool failed:
     - Anthropic credit balance depleted for the model on record.
     - Gemini model-name mismatch on that day.
     - OpenAI extract plugin returned an error.
   - Fell back to manual read of `paper.txt`. Identified Eq.(1),
     definitions of P_B, P_I, γ_C, D_50, and the qualitative claims C3–C7.
   - Wrote `smoke/p_plus_smoke.py` (216 LOC): implements Eq.(1) on a
     canonical Källman/Brahme Poisson sigmoid, sweeps δ ∈ {0, 0.2, 1}
     and continuous δ ∈ [0,1] (41 steps), varies γ_C from 3.0 to 1.8
     to mimic the LET-driven penalty, dumps a 4-panel PNG + a 1001-row
     CSV of the dose grid.
   - Wrote `FIRST_PASS_REPORT.md` summarising the finding.

2. **2026-06-22 (second pass, Ollie subagent).**
   - Re-ran the smoke; identical numbers (deterministic, no RNG in the
     Poisson-sigmoid path).
   - Wrote `smoke/eq1_internal_consistency.py` (144 LOC): 6 algebraic
     limits (L1–L6) on 20,000 random (P_B, P_I) draws + reverification
     of the peak numbers from scratch. **19/19 checks PASS**,
     max|err| = 1.1 × 10⁻¹⁶.
   - Wrote the full `REPORT.md` (Coverage 4/10, Agreement 7/10,
     Verdict SPOT-CHECK formalism-only).

3. **2026-06-25 (retiering, Ollie).**
   - Rick's rule: hard-ceiling spot-checks belong in NO-GO because
     nothing beyond formalism can ever be reproduced from the paper.
   - Added the RE-TIER banner at the top of REPORT.md
     (NO-GO, was SPOT-CHECK).

4. **2026-07-06 (this backfill, Ollie subagent).**
   - No re-run of simulations; synthesised report/ items 4–8 from
     the existing REPORT.md + artifacts + re-read of paper.txt.
   - Kept every existing file.

## Tools & versions

| Tool | Version | Purpose |
|---|---|---|
| Poppler `pdftotext` | 24.x (Homebrew, CherryRd) | PDF → paper.txt (fallback for figure-embedded text) |
| Python | 3.13.x | Smoke scripts |
| numpy | 2.x | Vectorised Poisson-sigmoid arithmetic |
| matplotlib | 3.x | `figs/p_plus_smoke.png` (4-panel) |
| shasum | macOS system | paper.pdf SHA-256 |
| bash / zsh | macOS 25.3 | Orchestration |

No paid endpoints. No cluster compute. No LLM inference required for
the replication itself; LLM was used only for report authoring during
the backfill (Argo `localhost:44497` free tier — Rick's standing rule).

## Compute estimate

- Wall clock (smoke): < 2 s per run. Executed 3 times across the two
  passes and the backfill sanity check → aggregate ~ 6 s.
- Wall clock (report authoring 2026-06-22 pass): ~ 60 min agent time.
- Wall clock (backfill 2026-07-06): ~ 5 min agent time,
  writing report/ items 4–8 file-by-file.
- Peak RSS: negligible (single-thread numpy on 1001-point grids).
- LOC (Python): 216 (`p_plus_smoke.py`) + 144 (`eq1_internal_consistency.py`)
  = 360 LOC total. Zero external code dependencies beyond numpy/matplotlib.
- Agent steps (approximate): 12 tool calls (fetch + extract + write + run + report) in the first pass,
  8 in the second pass, 8 in this backfill.

## Reproducer

```bash
cd lucid-brahme-radiobio-optimization-review/smoke
python3 p_plus_smoke.py                # writes ../figs/p_plus_smoke.{png,csv}
python3 eq1_internal_consistency.py    # 19/19 PASS in < 1 s
```

## Repo layout after backfill

```
lucid-brahme-radiobio-optimization-review/
├── paper.pdf                              (4.69 MB, sha256 b76858...cd00b9)
├── paper.txt                              (pdftotext, 2159 lines)
├── README.md
├── PROGRESS.md
├── FIRST_PASS_REPORT.md                   (2026-06-09)
├── REPORT.md                              (2026-06-22 + 06-25 retier banner)
├── artifacts/MANIFEST.md
├── smoke/
│   ├── p_plus_smoke.py
│   └── eq1_internal_consistency.py
├── figs/
│   ├── p_plus_smoke.png
│   └── p_plus_smoke.csv
├── extraction/                            (2026-07-06 backfill)
│   ├── marker.md                          (pdftotext-derived stub)
│   └── nougat.mmd                         (pending GPU parse, sha256 pointer)
└── report/                                (2026-07-06 backfill)
    ├── REPORT.tex
    ├── open_questions.json
    ├── open_questions_section.tex
    ├── workflow.md                        (this file)
    ├── artifacts_summary.md
    └── failure_analysis.md
```
