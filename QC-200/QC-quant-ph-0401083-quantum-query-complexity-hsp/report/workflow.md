# Workflow — QC-200 replication of arXiv:quant-ph/0401083

## Wave brief
`~/Dropbox/REPLICATE-PROJECT/scripts/QC_WAVE_BRIEF_2026-07-03.md`

## Paper resolved from arXiv ID
- arXiv:quant-ph/0401083 → "The quantum query complexity of the hidden subgroup problem is polynomial", Ettinger, Høyer, Knill (LANL / U Calgary), 14 Jan 2004, 8pp.
- Fetched via `curl -sL https://arxiv.org/pdf/quant-ph/0401083 -o paper.pdf` (109 KB, 8 pp, PDF 1.4).
- Text extracted with `pdftotext -layout paper.pdf work/paper.txt` (Poppler 24.x).
- Authors + title verified from fetched PDF header + Los Alamos affiliation confirmed against paper title page (matches the QC-200 wave metadata).

## Step-by-step
1. Read wave brief and prior QC-200 sibling (`QC-quant-ph-0102014-nonabelian-hidden-subgroup`) for structural template.
2. Fetched `paper.pdf` and `pdftotext`'d to `work/paper.txt` (390 lines).
3. Identified the concrete testable claim: **Theorem 2**, `Prob[H|H] ≥ 1 − 4r/2^(s/2)`. This is measurement-specific (paper's `Test` unitary) but the *information-theoretic* content — that a fixed measurement on s coset states distinguishes subgroups with error → 0 — is the natural small-instance testable core.
4. Wrote `report/evidence/hsp_query_complexity.py`: builds S_3, D_4, Z_2^3 as concrete permutation groups; enumerates all subgroups via subset-close; builds coset-state density matrices; runs Pretty-Good Measurement (PGM) analytically; produces confusion matrices for s=1..4.
5. Initial run with `complex128` OOM-risked on S_3 s=5 (dim 7776, 6× 967MB matrices in memory). Killed after 8 min at 1.7GB RSS. Simplified to `float64` (all amplitudes real in group basis), capped s=4 for all groups, reran. Full run: ~110 seconds wall.
6. Wrote `report/evidence/fit_scaling.py`: linear-fits `log_2(err_PGM)` vs `s`, reports empirical slope in bits/query and extrapolated `s*` for 1% error. Runs instantly.
7. Wrote `report/evidence/monte_carlo_check.py`: independent shot-based validation of the analytic PGM on `(D_4, s=3)`. 20k shots × 10 states, precomputed per-state distributions to keep runtime ≤ 15 s. Result: max analytic-vs-empirical diff 0.0055 < Hoeffding 95% CI half-width 0.0069 → PASS.
8. LLM-judge panel via Argo localhost:44497:
   - `argo:gpt-5.2` → verdict PARTIAL, confidence 0.72
   - `argo:claude-opus-4.7` → verdict SPOT-CHECK, confidence 0.85
   - Adjudicated verdict: SPOT-CHECK (per QC wave brief rule for info-theoretic papers).
9. Extraction artifacts (`extraction/marker.md`, `extraction/nougat.mmd`) filled with pdftotext fallbacks — Marker + Nougat not staged in the QC-200 wave time budget (would require torch model download; see `failure_analysis.md`). Both files carry an explicit fallback header banner so downstream consumers know.
10. Wrote `report/REPORT.tex`, `report/open_questions.{tex,json}`, `report/artifacts_summary.md`, `report/failure_analysis.md`, this `workflow.md`.
11. LaTeX compilation attempted — pdflatex present, will produce REPORT.pdf.

## Tools + versions
| Tool | Source | Purpose |
|---|---|---|
| `python 3.14.6` | Homebrew | driver + numerics |
| `numpy 2.x` | Homebrew site-packages | dense linear algebra (PGM eigh, kron) |
| `qiskit 2.4.3` | Homebrew site-packages | available but unused: PGM route is simpler and complete for this info-theoretic replication |
| `curl 8.x` | macOS | arXiv fetch |
| Poppler `pdftotext` | Homebrew | PDF → text fallback for extraction/{marker.md, nougat.mmd} |
| Argo LLM proxy | localhost:44497 | judge panel (`argo:gpt-5.2`, `argo:claude-opus-4.7`) |
| `pdflatex` | mactex | REPORT.tex → REPORT.pdf |

No paid endpoints used. All LLM calls to Argo (free).

## Estimated work
- Paper read + planning: ~15 min
- Simulation code + debug (first-run OOM, refactor to float64, cap s): ~45 min
- Full sim runs (S_3, D_4, Z_2^3 × s=1..4): ~2 min (after refactor)
- Scaling fit + MC cross-check: ~5 min
- Judge panel + adjudication: ~5 min
- Report writeup + LaTeX: ~40 min
- **Total wall time: ~2 hours** (single subagent turn)
