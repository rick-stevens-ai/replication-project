# Artifacts summary — arXiv:1509.09271 replication

Total size: ~944 KB across 20 files. Everything self-contained; no external dependencies beyond system numpy/matplotlib/pdftotext/pdflatex.

## The 8 required artifacts (per REPLICATION_DIR_STANDARD_2026-07-05)

| # | Artifact | Path | Status | Size |
|---|----------|------|--------|------|
| 1 | Original PDF | `paper.pdf` | ✓ present | 232 KB |
| 2 | Marker parse | `extraction/marker.md` | ✓ present (stub — Marker not installed on host; see failure_analysis.md §1) | 6.1 KB |
| 3 | Nougat parse | `extraction/nougat.mmd` | ✓ present (stub — Nougat not installed on host; see failure_analysis.md §1) | 4.9 KB |
| 4 | LaTeX report + compiled PDF | `report/REPORT.tex` + `report/REPORT.pdf` | ✓ present, compiles cleanly | 17 KB tex, 308 KB pdf (7pp) |
| 5 | Open questions (JSON + `## Open Questions` section in report) | `report/open_questions.json` + REPORT.tex §7 | ✓ present, 5 questions each with `q`/`basis`/`next_steps` | 4.8 KB |
| 6 | Workflow doc | `report/workflow.md` | ✓ present | 6.4 KB |
| 7 | Artifacts inventory | `report/artifacts_summary.md` (this file) | ✓ present | ~2 KB |
| 8 | Failure analysis | `report/failure_analysis.md` | ✓ present | ~3 KB |

## Evidence + code

| File | Purpose | Size |
|------|---------|------|
| `report/evidence/qpoly_interp.py` | Main simulation: classical Lagrange baseline + quantum enumeration of $R_k$ + inverse QFT + measurement | 15 KB |
| `report/evidence/plot_results.py` | Generates success-vs-queries plot and odd-$d$ asymptote plot | 3.5 KB |
| `report/evidence/results.json` | 39 raw trials + 13 per-config summaries, one JSON blob | ~30 KB |
| `report/evidence/results_smoke.json` | Early sanity check (naive Python loop version) | ~2 KB |
| `report/evidence/results_smoke2.json` | Sanity check post-vectorisation (identical values, 100× faster) | ~1 KB |
| `report/evidence/success_vs_queries.pdf` + `.png` | Main figure: success probability vs. $k$ for each $(q, d)$ | 12 KB + 60 KB |
| `report/evidence/odd_d_asymptote.pdf` + `.png` | Secondary figure: odd-$d$ asymptote $\to 1/k!$ fit | 8 KB + 45 KB |

## Intermediate / downloaded

| File | Purpose | Size |
|------|---------|------|
| `work/paper.txt` | pdftotext extraction of `paper.pdf`, source for extraction stubs and quote lookups | 50 KB |

## Report build artifacts (retained for auditability)

| File | Purpose | Size |
|------|---------|------|
| `report/REPORT.aux` | pdflatex aux (cross-refs) | 1 KB |
| `report/REPORT.out` | pdflatex hyperref outline | 1 KB |
| `report/REPORT.log` | pdflatex compile log | ~15 KB |
| `report/tex.log` | wrapper log around pdflatex invocation | ~15 KB |

## Traces / verification points

- **Sanity trace 1:** measured success probability = enumerated $|R_k|/q^{d+1}$ to floating-point precision in all 39 trials (see `results.json`, fields `p_success_theory` vs. `p_success_measured`). This validates both the enumeration and the QFT.
- **Sanity trace 2:** naive-loop implementation (`results_smoke.json`) and vectorised implementation (`results_smoke2.json`) give bit-identical success probabilities for $(q, d) = (7, 2)$ — refactor did not change semantics.
- **Sanity trace 3:** classical Lagrange interpolation recovered $c$ correctly in all 39 classical trials (field `classical_ok = true` throughout).
- **Sanity trace 4:** for the classical-baseline query count $k = d+1$, measured success is exactly 1.0000 in all 21 such trials — the algorithm degenerates to the ideal $|\hat c\rangle$ preparation, as it should.
- **Sanity trace 5:** for odd $d = 3$, $k = (d+1)/2 = 2$, the measured success at $q = 7, 11, 13$ is $0.333, 0.383, 0.399$ — monotonically increasing and fitting $0.5(1 - c/q)$ with $c \approx 2.5$, matching Theorem 2(i) prediction $1/k! \cdot (1 - O(1/q)) = 0.5 \cdot (1 - O(1/q))$.

## Reproduction check

Someone else can rerun this replication end-to-end with:

```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-200/QC-1509.09271-optimal-polynomial-interpolation-childs
python3 report/evidence/qpoly_interp.py --trials 3 \
    --configs "7:2,7:3,11:2,11:3,13:2,13:3" \
    --out report/evidence/results.json
python3 -c "import json, sys; r=json.load(open('report/evidence/results.json')); print('SUMMARY:'); [print(f\"q={s['q']} d={s['d']} k={s['k']} P={s['avg_p_success_measured']:.4f}\") for s in r['summary']]"
```

Expected output: 13 lines, exact values ~$\pm 10^{-14}$ of what is in the report.

## Provenance

- Paper: fetched from `https://arxiv.org/pdf/1509.09271` on 2026-07-05, 17 pages, 232 KB, arXiv v2 (2016-03-01).
- Authors verified against extracted title page: Andrew M. Childs (UMD/QuICS), Wim van Dam (UCSB), Shih-Han Hung (QuICS), Igor E. Shparlinski (UNSW).
- Task description said "quantum uses $d$ queries" — this is the older Boneh–Zhandry (2013) result; the Childs et al. paper we replicated is the STRONGER $d/2 + 1/2$ result. Corrected in Method §2.1 of REPORT.tex and used the paper's actual predictions for the verdict.
