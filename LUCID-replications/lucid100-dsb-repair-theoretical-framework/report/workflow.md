# Workflow — lucid100-dsb-repair-theoretical-framework

## Paper
Murray, Cornelissen, Vallis, Chapman (2016).
*DNA double-strand break repair: a theoretical framework and its application.*
J. R. Soc. Interface **13**: 20150679. DOI 10.1098/rsif.2015.0679. PMC4759787. CC BY 4.0.

## Stages executed

### 1. Acquisition (2026-06-09, one-shot)
- Pulled full paper PDF from `https://europepmc.org/articles/PMC4759787?pdf=render`
  → `artifacts/paper.pdf` (649 KB, md5 `888349ba9763ec27c7185f6e3c8648e8`).
- Pulled JATS full text from EuropePMC REST → `artifacts/paper.xml` (104 KB).
- Cross-checked provenance via Semantic Scholar / Unpaywall
  → `artifacts/paper_unpaywall_s2_acquired.pdf` (byte-for-byte identical to primary).
- No supplementary data deposited by paper (`hasSuppl=N`).

### 2. Extraction (no GPU parse)
- Text extracted from XML (JATS) rather than PDF-OCR; equations and tables read directly.
- `extraction/nougat.mmd` is a **stub** pointer file — sha256 of paper.pdf,
  reason "text extracted from JATS XML, no GPU nougat pass needed".

### 3. Implementation
- `scripts/scripts_ssa.py` — vectorised tau-leap SSA for master equation (2.1),
  τ = 5×10⁻⁴ h (MDA468) / 5×10⁻⁵ h (MCF7), numpy-only.
- `scripts/ssa_exact.py` — pure-Python exact Gillespie cross-check on MDA468, [0,1h], n=100.
- `scripts/smoke_model.py` — ODE integrators for eqs (2.5), (4.1), (4.3–4.4); 6 qualitative checks.
- `scripts/closure_validation.py` — Section 3.1 / Fig 3 SSA-vs-ODE quantitative replication;
  writes JSON + per-line CSV trajectories.
- `scripts/claim_audit.py` — generator for machine-readable claim table
  (`artifacts/claim_audit.json`).
- Stack: pure CPython 3.13 + numpy + scipy. No GPU, no HPC, no paid endpoints.

### 4. Verification
- 6/6 qualitative checks PASS (smoke_results.json).
- SSA-vs-ODE RMS on MDA-MB-468 [0,6h]: X 0.045, Y 11, Z 56 (SSA peak Z≈445). ~13% relative.
- SSA-vs-ODE RMS on MCF7 [0,0.6h]: X 0.030, Y 78, Z 243 (SSA peak Z≈800). ~13% relative.
- Exact-Gillespie vs bare eq (2.5) on MDA468 at t=1h: 5–10% agreement.
- Stability analysis (claim_audit.py): MCF7 k₃k₅/(k₄k₆) = 1.000374 UNSTABLE;
  MDA468 = 0.987 stable-marginal.

### 5. Audit / verdict (2026-06-22)
- Testable-claim audit: 6 verified, 2 partial, 1 contradicted (new: MCF7 ODE instability),
  2 not tested (blocked by figure-only data).
- Verdict: **PARTIAL**. Coverage 8/10, Agreement 7/10.
- Preserves original 2026-06-09 first-pass verdict (upgraded to PARTIAL after full closure
  and stability analysis).

### 6. Backfill (this task, 2026-07-06)
- Added `report/REPORT.tex`, `open_questions.json` + `.tex`, `workflow.md`,
  `artifacts_summary.md`, `failure_analysis.md`.
- Added `extraction/nougat.mmd` stub.
- No re-simulation, no new fits — all existing artifacts preserved verbatim.
- Verdict cross-check: queue said REPLICATED, audit said PARTIAL.
  **Preserved audit verdict (PARTIAL)** and flagged mismatch in `failure_analysis.md`.

## Compute
- CherryRd (localhost), CPython 3.13 + numpy + scipy.
- Total runtime full audit ≈ 2 minutes CPU.
- No HPC, no GPU, no paid endpoints, no network after one-time PDF/XML pull.

## Data & code provenance
- Paper: CC BY 4.0 via PMC4759787.
- All local scripts and artifacts under this dir, git-visible.
- No author code, no author data (paper deposits none; upstream refs [12,17] also figure-only).

## What was NOT run
- Nelder–Mead refit of eq (3.3): blocked by figure-only Fig 4 data.
- Cross-validation, held-out prediction: blocked by same.
- Comparison against competing frameworks (Cucinotta, MEDRAS): out of scope for a
  single-paper replication; enumerated as open question Q3.
- Testable-extremes exploration (FLASH, ultra-low-dose, high-LET): enumerated as Q5.
