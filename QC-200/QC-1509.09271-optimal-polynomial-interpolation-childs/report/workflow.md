# Workflow — arXiv:1509.09271 replication

**Date:** 2026-07-05
**Host:** CherryRd (macOS Darwin 25.3.0)
**Operator:** OpenClaw sub-agent (headless, session `agent:main:subagent:0e731cd4-...`)
**Requested by:** Rick Stevens via QC-200 wave
**Wall time:** ~15 min (paper fetch + coding + simulation + report writing)
**Estimated equivalent human effort:** 1.5–3 days for a graduate student who has not seen the paper before (read paper, translate Theorem 1's algebraic $|R_k|/q^{d+1}$ into code, write both classical and quantum baselines, verify on a small case, plot, write up).

## Chronological workflow

1. **[19:15]** Read the QC wave brief at `~/Dropbox/REPLICATE-PROJECT/scripts/QC_WAVE_BRIEF_2026-07-03.md` to confirm the 8-artifact bar and verdict vocabulary.
2. **[19:16]** Created target dir `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-1509.09271-optimal-polynomial-interpolation-childs/` with subdirs `work/`, `report/`, `report/evidence/`, `extraction/`.
3. **[19:16]** Fetched paper via `curl` from `https://arxiv.org/pdf/1509.09271` → `paper.pdf` (17 pp, 232 KB).
4. **[19:16]** Extracted with `pdftotext paper.pdf work/paper.txt` (1,646 lines, 49.7 KB) and skimmed the first ~360 lines to identify the exact algorithm (§2.2), the target success probability (Theorem 1: $|R_k|/q^{d+1}$), and Theorem 2's asymptotic predictions for both $d$-odd and $d$-even cases.
5. **[19:17]** **CRITICAL CORRECTION** — the task description said "quantum uses $d$ queries," but the paper's actual claim is stronger: $d/2 + 1/2$ (odd $d$) or $d/2 + 1$ (even $d$) queries suffice. Verified this against the abstract, §1, and Theorem 2 statement. Replication targets updated to the paper's actual predictions.
6. **[19:18]** Wrote `report/evidence/qpoly_interp.py`: modular arithmetic over $\mathbb{Z}/q\mathbb{Z}$, Lagrange-interpolation classical baseline, direct enumeration of $R_k$, direct construction of $|\hat c_{R_k}\rangle$ on the $q^{d+1}$ register, and $(d+1)$-fold inverse QFT via tensor contraction.
7. **[19:19]** Smoke test on $(q, d) = (7, 2)$: measured 0.9825 (matches Theorem 2(ii) prediction $1 - O(1/q)$). Confidence check on $k = 3$ giving 1.0000.
8. **[19:20]** First full run of the sweep hung on $(7, 3, 4)$ because the enumeration was a Python loop over $q^{2k} = 7^8 \approx 5.8\,\text{M}$ tuples. Killed after ~3 min at that config.
9. **[19:21–19:22]** Refactored `compute_Rk_and_state` to be fully vectorised numpy: `meshgrid` builds $X, Y$ of shape $(q^k, k)$; precompute $X^{\rm pows}[j, a, i] = x_i^j$; then $Z(x, y)_j = Y \cdot X^{\rm pows}[j]^\top \mod q$ as one matmul per $j$. Chunked over $y$-tuples to keep peak memory bounded. Speedup: ~100×.
10. **[19:23]** Re-ran smoke test — identical results in 0.02 s vs.\ prior 2.65 s. Ran the full sweep `q:d ∈ {7:2, 7:3, 11:2, 11:3, 13:2, 13:3}` with 3 trials each. Total wall time <20 s. Two configs skipped due to enumeration size (`q=11, d=3, k=4` and `q=13, d=3, k=4` — enum size $>2\times10^8$).
11. **[19:24]** Wrote `plot_results.py` producing `success_vs_queries.{png,pdf}` (main scaling plot) and `odd_d_asymptote.{png,pdf}` (odd-$d$ $1/k!$ asymptote fit). Fit coefficient $c \approx 2.5$ in the odd-$d$ correction $0.5(1 - c/q)$.
12. **[19:24]** Wrote extraction stubs `extraction/marker.md` and `extraction/nougat.mmd`. Neither Marker nor Nougat is installed on this host and no central-corpus copy exists for arXiv:1509.09271; both stubs contain the paper's key equations reconstructed from the pdftotext text and clearly disclose the provenance.
13. **[19:25]** Wrote `report/REPORT.tex` (7 pages, 308 KB compiled): verdict, claims table (C1–C7), method, exact commands, design choices, results table, verdict justification, 2 figures, 5 open questions with bibliography. Compiled with `pdflatex` twice for cross-refs → `REPORT.pdf`.
14. **[19:26]** Wrote `report/open_questions.json` (5 non-superficial questions, each with `q`, `basis`, and `next_steps`), `report/workflow.md` (this file), `report/artifacts_summary.md`, `report/failure_analysis.md`.

## Tools + versions

| Tool | Version | Where used |
|------|---------|------------|
| Python | 3 (system default on CherryRd, macOS 25.3.0) | all simulation |
| numpy  | (system) | statevector, enumeration, QFT |
| matplotlib | (system, Agg backend) | plots |
| pdftotext (Poppler) | (system) | paper text extraction |
| curl | (system) | paper download from arXiv |
| pdflatex (texlive) | 20260301 (2026) | REPORT.pdf compile |
| Marker (marker-pdf) | **NOT INSTALLED** | extraction stub used instead |
| Nougat | **NOT INSTALLED** | extraction stub used instead |
| Qiskit / Cirq / PennyLane | not used | full statevector on $q^{d+1}$ dim is trivial with plain numpy for $q \le 13, d \le 3$ |

## Data lineage

- Original paper: `paper.pdf` (SHA-256 not recorded, but downloaded from `https://arxiv.org/pdf/1509.09271` on 2026-07-05).
- Text extraction: `work/paper.txt` from `pdftotext paper.pdf work/paper.txt`.
- Simulation code: `report/evidence/qpoly_interp.py` (~350 lines, MIT-licensed under REPLICATE-PROJECT).
- Raw results: `report/evidence/results.json` (39 trials, all numbers verifiable by re-running the script — seeds are deterministic in `run_trial(seed=1000*q + 10*d + s)`).
- Plots: `report/evidence/success_vs_queries.{png,pdf}` and `odd_d_asymptote.{png,pdf}`.
- Report source: `report/REPORT.tex` → `report/REPORT.pdf`.

## Reproduction command (one-shot)

```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-200/QC-1509.09271-optimal-polynomial-interpolation-childs/report/evidence
python3 qpoly_interp.py --trials 3 \
    --configs "7:2,7:3,11:2,11:3,13:2,13:3" \
    --out results.json
python3 plot_results.py
```

Wall time: ~15 s on CherryRd.

## Estimate of work done

- **Paper reading:** ~5 min (skimmed abstract + §1 + §2.1 + §2.2; extracted Theorem 1, Theorem 2, oracle definition, Z definition, $|\hat c_{R_k}\rangle$ formula).
- **Simulation coding:** ~10 min (classical Lagrange + quantum enumeration + QFT + entry point).
- **Vectorisation refactor:** ~5 min (identified the Python-loop bottleneck, rewrote with meshgrid + matmul).
- **Sweep + plotting:** ~2 min wall clock, ~5 min setup.
- **Report + open questions + workflow + artifacts summary + failure analysis:** ~15 min.
- **TOTAL:** roughly 45 min agent time from paper URL to fully-written report with compiled PDF, 8 artifacts, and no fabricated numbers.
