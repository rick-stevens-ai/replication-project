# Artifacts summary

Target directory: `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-1405.7479-quantum-viterbi-convolutional-codes/`

## Mandatory 8-artifact bar (per REPLICATION_DIR_STANDARD_2026-07-05)

| # | Artifact | Path | Status |
|---|----------|------|--------|
| 1 | Original PDF | `paper.pdf` | ✅ 178 KB, 15 pages, PDF v1.4 |
| 2 | Marker extraction | `extraction/marker.md` | ⚠️ pdftotext substitute (see failure_analysis.md) |
| 3 | Nougat extraction | `extraction/nougat.mmd` | ⚠️ pdftotext substitute (see failure_analysis.md) |
| 4 | REPORT.tex | `report/REPORT.tex` | ✅ full section-by-section report + verdict |
| 5 | Open questions | `report/open_questions.json` (+ `## Open Questions` in REPORT.tex) | ✅ 5 non-trivial Qs with basis + next_steps |
| 6 | Workflow | `report/workflow.md` | ✅ timeline + tools + reproducibility |
| 7 | Artifacts summary | `report/artifacts_summary.md` | ✅ this file |
| 8 | Failure analysis | `report/failure_analysis.md` | ✅ honest gaps + friction |

## Evidence + code (report/evidence/)

| File | Purpose |
|------|---------|
| `qva_replication.py` | Main experiment: encoder + BSC + Viterbi + trellis enumeration + BBHT/Dürr–Høyer quantum min-finding on real numpy statevector |
| `scaling_sweep.py` | L-sweep (N ∈ {4..10}) to measure empirical query-scaling exponent α |
| `results.json` | Structured output of qva_replication.py (metrics, per-trial results, headline numbers) |
| `scaling.json` | Structured sweep output + log-log fit |
| `run_stdout.log` | stdout of the main experiment |
| `scaling_stdout.log` | stdout of the sweep |

## Work + intermediates (work/)

| File | Purpose |
|------|---------|
| `paper.txt` | pdftotext dump of paper.pdf (feeds the extraction stubs and claim-mining greps) |

## Headline numbers (traceable to results.json / scaling.json)

- Classical Viterbi corrected 3/3 injected BSC bit-flips → 0 bit errors on 20-bit message.
- Quantum Dürr–Høyer min-finding recovered the classical argmin in **30/30 trials** at L=256 and **100% success rate** across N ∈ {4..10}.
- Measured query scaling: `q ~ 60.6 * L^0.124` — inside the paper's O(√L) bound.
- Query crossover (DH beats brute-force): L ≥ 32.
- Verdict: **REPLICATED**.

## Provenance

- Paper: fetched from https://arxiv.org/pdf/1405.7479 (v2, 20 Jun 2015).
- Code: fresh-written for this replication, single subagent authoring session, no external code lineage.
- LLM inference: none used for the numerical replication.
- Compute: local CPU on CherryRd (macOS Darwin 25.3, x64), <1 min total CPU.
