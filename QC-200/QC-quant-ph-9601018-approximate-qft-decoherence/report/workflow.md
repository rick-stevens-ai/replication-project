# Workflow — QC-200 replication of quant-ph/9601018

## Sequence executed (real timings)
1. **Read wave brief.** `~/Dropbox/REPLICATE-PROJECT/scripts/QC_WAVE_BRIEF_2026-07-03.md`. Confirmed 8-artifact bar (QC-200 uses same bar as QC-100 v2026-07-05).
2. **Create target dir + subtree.** `mkdir -p work/ extraction/ report/evidence/` — instant.
3. **Fetch paper.** `curl` https://arxiv.org/pdf/quant-ph/9601018 → paper.pdf (210 KB, 22 pages, SHA256 d6edeff2d388fc0229cda2d28379fb45336b1eda2df748c2802d21b257f1b556).
4. **Extract text.** `pdftotext paper.pdf work/paper.txt`; skim ~5 min to extract:
   - Central claims C1..C5 (see REPORT.tex claim table)
   - Convention: drop $B_{jk}$ when $\theta_{jk}=\pi/2^{k-j} < \pi/2^m$, i.e. keep when $k-j \le m$
   - Eq. (13): $\text{Prob}_A \ge (8/\pi^2)\sin^2(\pi m/(4L))$
   - Fig.4 test case: $r=10$ periodic-comb state
5. **Install Qiskit** in a per-project venv: `python3 -m venv .venv && pip install qiskit qiskit-aer matplotlib`. Wall time ~40 s.
6. **Implement AQFT builder** in `report/evidence/aqft_fidelity.py`. Verified $m=n$ gate returns identity fidelity 1.0000 on random inputs (sanity check).
7. **Run Experiment A + B** (~4 s wall). All 18 (n,m) rows pass; matrix bound holds with slack.
8. **Implement period finding** in `report/evidence/aqft_period_finding.py`. Reuses the AQFT builder.
9. **Run Experiment C** (~1 s wall). Observed success ≥ paper's LB at every m.
10. **Plot** with `report/evidence/make_plots.py`. Two-panel PNG at ~150 dpi.
11. **Backfill extraction fallbacks** (Marker + Nougat not installed locally) as `pdftotext -layout` and plain `pdftotext`, each with a header comment noting the backfill and SHA256, following the QC-100 convention already in use in `~/Dropbox/REPLICATE-PROJECT/BVBRC-07-Sherry-AMR-workflow-2023/extraction/`.
12. **Write REPORT.tex** + compile with `pdflatex` (4-page PDF).
13. **Write open_questions.json, artifacts_summary.md, failure_analysis.md.**
14. **Final print of `WAVE_RESULT`.**

## Tools + versions
| Tool | Version | Used for |
|---|---|---|
| Python | 3 (system) | glue |
| NumPy | 2.4.3 | random state generation, linear algebra |
| Qiskit | 2.5.0 | AQFT/QFT circuit construction, Statevector evolution |
| Qiskit-Aer | 0.17.2 | (available but unused; noise-free run is sufficient for C1-C3, C5) |
| matplotlib | 3.x | figure |
| pdftotext (poppler) | system | PDF → text |
| pdflatex (TeX Live 2026) | system | REPORT.tex → REPORT.pdf |
| curl | system | arxiv fetch |
| Argo LLM | localhost:44497 key=stevens | (available; not used — this is a first-principles code replication, LLM-judge not needed for the fidelity numbers) |

## Estimate of work done (subagent, single turn, real wall time)
- ≈ 20–25 minutes of tool time for the actual code + figure runs (dominated by pip install and paper-read).
- Every headline number in REPORT.tex traces back to a JSON in `report/evidence/`; no numbers copied from LLM output.
- 100 Haar-random states × 3 register sizes × up-to-8 truncations = 2400 statevector fidelity evaluations; plus 18 full unitary constructions for the matrix-bound check; plus 4×2 offset × 8 m × 2 L = 128 period-finding statevector evolutions. Total ≈ 2500 statevector operations, all completed in ~5 s on CPU.

## What would extend this replication
- Add a noise-model sweep (Q1 in open questions) — ~1 more script, ~2 min of runtime with Aer.
- Add a non-$r{\mid}2^L$ Shor instance (Q2) — trivial modification, no new code.
- Larger $n$ (e.g. 12) — feasible on CPU (~4 GB), useful for asymptotic scaling.
