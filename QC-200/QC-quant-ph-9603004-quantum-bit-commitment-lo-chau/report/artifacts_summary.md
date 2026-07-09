# Artifacts Summary — Lo & Chau QBC replication

Every file in the target directory, its size (approx), and what it is /
what it proves.

## Required 8-artifact checklist (Rick 2026-07-05 standard)

| # | Artifact | Present? | Path |
|---|---|---|---|
| 1 | `paper.pdf` (original PDF) | ✅ | `paper.pdf` |
| 2 | `extraction/marker.md` | ✅ (pdftotext -layout fallback) | `extraction/marker.md` |
| 3 | `extraction/nougat.mmd` | ✅ (pdftotext -raw fallback) | `extraction/nougat.mmd` |
| 4 | `report/REPORT.tex` + compiled `REPORT.pdf` | ✅ (5 pages) | `report/REPORT.{tex,pdf}` |
| 5 | `report/open_questions.json` + `## Open Questions` in report | ✅ (5 Q's, each `{q,basis,next_steps}`; also mirrored in REPORT.tex) | `report/open_questions.json`, `report/REPORT.tex` §Open Questions |
| 6 | `report/workflow.md` (workflow + tools + versions + effort) | ✅ | `report/workflow.md` |
| 7 | `report/artifacts_summary.md` (this file) | ✅ | `report/artifacts_summary.md` |
| 8 | `report/failure_analysis.md` | ✅ | `report/failure_analysis.md` |

## Inventory (with brief description)

### Paper
- **`paper.pdf`** (103 KB) — the original arXiv:quant-ph/9603004v2 PDF.
  Fetched via `curl -sL https://arxiv.org/pdf/quant-ph/9603004`.
  Authors verified inside the PDF as **Hoi-Kwong Lo & H. F. Chau**.

### Extractions
- **`extraction/marker.md`** — pdftotext `-layout` extraction (preserves
  column structure). Marker (VikParuchuri/marker) not installed in this
  environment; using the same convention as sibling QC-200 dirs.
- **`extraction/nougat.mmd`** — pdftotext `-raw` extraction (reading
  order, line-wrap removed). Same rationale for the fallback.

### Working directory (`work/`)
- `work/paper.pdf` — working copy of the PDF.
- `work/paper.txt` — default pdftotext extract (used for the initial skim).
- `work/paper_layout.txt` — source of `extraction/marker.md`.
- `work/paper_raw.txt` — source of `extraction/nougat.mmd`.
- `work/.venv/` — local Python 3.14 venv with qiskit 2.5.0, numpy 2.4.3,
  scipy 1.18.0, matplotlib. Not committed anywhere; regenerate with
  `python3 -m venv work/.venv && source work/.venv/bin/activate && pip install qiskit numpy scipy matplotlib`.

### Report (`report/`)
- **`report/REPORT.tex`** (13.4 KB) — full 5-page LaTeX report:
  paper summary, claims table (C1..C5), methods, results-vs-paper table,
  verdict, and the mandatory Open Questions section.
- **`report/REPORT.pdf`** (329 KB, 5 pages) — compiled with `pdflatex`
  (TeX Live 2026-03-01), two-pass build for hyperref cross-refs.
- **`report/REPORT.log`, `REPORT.aux`, `REPORT.out`** — LaTeX build
  intermediates.
- **`report/open_questions.json`** (4.8 KB) — the 5 open questions in
  machine-readable form, each `{"q": ..., "basis": ..., "next_steps": ...}`.
  All five arose from *this* replication (not copy-pasted from the
  paper's own future-work).
- **`report/workflow.md`** — step-by-step workflow, tool versions,
  effort estimate.
- **`report/failure_analysis.md`** — honest account of what failed and
  what didn't; where the replication left residual gaps.
- **`report/artifacts_summary.md`** — this file.

### Evidence (`report/evidence/`)
- **`lo_chau_replication.py`** (20 KB) — main script. Three parts:
  ideal 3-qubit protocol (C1, C2); ε-family sweep (C3);
  BB84 EPR-cheat sanity (C4). Pure Qiskit statevector + numpy SVD; no
  LLM in the numerics loop.
- **`plot_tradeoff.py`** (1.7 KB) — plots the ε-vs-P_cheat curve;
  writes `tradeoff_curve.png`.
- **`results.json`** (15 KB) — all numerics from the run in one JSON
  blob, keyed by `env`, `P1_ideal`, `P2_nonideal`, `P3_bb84_epr_cheat`.
  This is the single source of truth for the numbers cited in REPORT.tex.
- **`tradeoff_curve.csv`** (5.6 KB) — 41-row sweep of θ, F_bob, ε,
  P_cheat_uhlmann, 1-P_cheat, sqrt(ε).
- **`tradeoff_curve.png`** (105 KB) — 2-panel figure; used in REPORT.pdf.
- **`run.log`** (1.7 KB) — stdout of `lo_chau_replication.py`.

## Trace: how each REPORT number came from an evidence file
| REPORT.tex value | Source |
|---|---|
| $\|\rho^B_0-\rho^B_1\|_F = 3.14\times10^{-16}$ (C1) | `results.json` → `P1_ideal.bob_rho_frobenius_diff` |
| $F(\rho^B_0,\rho^B_1)=1.0000000000$ (C1) | `results.json` → `P1_ideal.bob_fidelity_before_U` |
| $U_A$ unitarity error $8.9\times10^{-16}$ (C1) | `results.json` → `P1_ideal.U_A_unitarity_error` |
| $\|\bra{\Psi_1}(U_A\otimes I)\ket{\Psi_0}\|^2 = 1.0000000000$ (C2) | `results.json` → `P1_ideal.overlap_prob_...` |
| $P_\mathrm{cheat}=F=1-\varepsilon$ across 41 pts, max error $2.2\times10^{-16}$ (C3) | `results.json` → `P2_nonideal.|1-P_cheat  minus  eps|_max` |
| Figure 1 | `report/evidence/tradeoff_curve.png` (from `plot_tradeoff.py` reading `tradeoff_curve.csv`) |
| $\|\rho^B - I/2\|_\infty = 1.1\times10^{-16}$ (C4) | `results.json` → `P3_bb84_epr_cheat.bob_marginal_is_maximally_mixed_max_norm` |
| Alice-outcome probs 0.5000/0.5000 (C4) | `results.json` → `P3_bb84_epr_cheat.alice_Z_outcome_prob{0,1}` |

## Reproducibility one-liner
```bash
cd QC-quant-ph-9603004-quantum-bit-commitment-lo-chau
python3 -m venv work/.venv && source work/.venv/bin/activate
pip install qiskit numpy scipy matplotlib
python3 report/evidence/lo_chau_replication.py
python3 report/evidence/plot_tradeoff.py
cd report && pdflatex -interaction=nonstopmode REPORT.tex && pdflatex -interaction=nonstopmode REPORT.tex
```
Wall time <15 s on a single laptop core.
