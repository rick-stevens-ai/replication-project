# Artifacts summary — TEXTURE-loop-current-xu2023

Replication of arXiv:2306.16192 (chiral SU(3) kagome antiferromagnet),
loop-current class (partial/adjacent — see extraction/marker.md).

## Directory tree
```
TEXTURE-loop-current-xu2023/
  paper.pdf                     source paper (15 MB)
  paper.txt                     pdftotext -layout extraction (1505 lines)
  PROVENANCE.md                 kernel-reuse + provenance
  extraction/
    marker.md                   extraction method + classification note
  code/
    magnon_su3_kagome.py        Eq.A1 Bloch matrix, BZ utils, analytic formulas
    run_checks.py               5 quantitative claim checks
    plot_bands.py               band plots + chiral hexagon-mode probe
  work/
    results.json                machine-readable pass/fail + numbers
    run_log.txt                 full console log
    magnon_bands.png            Gamma-M-K-Gamma magnon bands (3 regimes)
  report/
    REPORT.tex (+ .pdf)         main report
    open_questions.json         exactly 5 open questions
    workflow.md                 end-to-end workflow
    artifacts_summary.md        this file
    failure_analysis.md         negatives, out-of-scope, bugs+fixes
```

## Claims checked (all reproduced)
| # | Claim | Metric | Result |
|---|-------|--------|--------|
| 1 | FM energy `e_F=2J+4K_R/3` | max abs err / 2000 pts | 0.0 — PASS |
| 2 | q=0 eigs `{0,−6(J+K_R)±2√3K_I}` | max abs err / 3000 pts | 1.4e-14 — PASS |
| 3 | instability line `J+K_R<−|K_I|/√3` | numeric-vs-analytic agreement | 100.00% (0/2454) — PASS |
| 4 | dispersion ∝ (J+K_R),K_I only | max spectrum dev / 4 splits | 0.0 — PASS |
| 5 | flat 0-band on boundary | lowband width on/off | 3e-15 vs 1.5 — PASS |

Bonus (qualitative): flat-band eigenvector inter-sublattice phases = **±π/3**,
matching the paper's chiral hexagon-mode `e^{ijπ/3}` amplitudes.

## Verdict
**REPRODUCED (in-scope analytical core).** 5/5 machine-checkable single-magnon
claims match to machine precision; the chiral hexagon-mode structure is confirmed.
The many-body topological (TSL/CSL/DCS) and two-magnon/iPEPS results are honestly
marked out-of-scope (open questions 1-5).

- **Coverage: 6/10** — covers the full analytical single-magnon core (FM phase
  boundary, chiral flat band) but not the paper's headline many-body TSL physics,
  which is the bulk of the work.
- **Agreement: 10/10** — every in-scope claim reproduced to machine precision.
