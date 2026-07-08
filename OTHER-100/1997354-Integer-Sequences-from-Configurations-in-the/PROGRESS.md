# PROGRESS — OSTI 1997354 (Integer Sequences from Configurations / Edge Covers)

## Timeline
- **Pass 1 (Apr 18 – Apr 30 2026)** — initial replication: 13 formulas
  implemented, brute-force agreement, 21 of the paper's OEIS sequences
  cross-checked, achievability gaps confirmed.  Self-scored 10/10/10/10
  in `REPORT.pass1.md`.
- **Repass (Jun 23 2026)** — system flagged Coverage=7 / Agreement=8
  / PARTIAL. Audit identified 19 OEIS sequences from Table 3 that
  pass 1 had *named* in tables but never *verified* term-by-term, plus
  closed-form polynomials and several stated numerical examples that
  pass 1 only spot-checked. Repass closes those gaps.

## Repass deliverables (Jun 23 2026)
- `PARSER_PROVENANCE.md` — pdftotext-based canonical parse, paper-typo log.
- `code/repass/repass.py` — single script, 7 verification steps,
  ~1.5 s runtime on cherryrd CPU.
- `results/repass/*.json` — raw outputs for each verification step.
- `results/repass/verdict_table.csv` — 69 per-claim verdicts.
- `results/repass/summary.json` — category counts.
- `REPORT.md` — updated, with `REPORT.pass1.md` preserved verbatim.

## Repass headline numbers
| Category | PASS | FAIL | OBSERVED |
|---|---|---|---|
| OEIS-Table-3 (19 new sequences) | **19** | 0 | 0 |
| First-row-shared (A024023, A103453, cross-checks) | **8** | 0 | 0 |
| Table-3 closed forms (24 polynomials) | **24** | 0 | 0 |
| Theorem-12 per-case brute force (6 topologies) | **6** | 0 | 0 |
| Asymptotic E1(m,n) ~ (2^m-1)^(n-1) (5 values of m) | 0 | 0 | **5** |
| Stated numerical examples (5 captions) | **5** | 0 | 0 |
| Symmetry (E1(2,6)=E1(6,2)) | **1** | 0 | 0 |
| Theorem 8 (E vs brute, A048291 diagonal) | **1** | 0 | 0 |
| **TOTAL** | **64** | **0** | **5** |

(`OBSERVED` = qualitative leading-order check — ratios converge to the
expected leading coefficient of the closed-form, e.g. 2.999... → 3 for
m=3 ⇒ leading coeff 3, 6.998... → 7 for m=4 ⇒ leading coeff 7. No
strict pass/fail because the paper only asserts asymptotic order, not
the leading coefficient.)

## Honest negatives surfaced by the repass
1. **Paper typo in Table 3, row E3_3(5,n).** The printed closed form
   `−3^(n−1)` should be `−3^(n+1)`. Discrepancy = 8·3^(n−1) per term.
   The recurrence (Theorem 12 + Theorem 11) is correct; OEIS A340434's
   registered formula (Howroyd, Nov 2025) confirms `−3^(n+1)`.
2. **OEIS offset shift.** All 19 Table-3 OEIS sequences include an
   extra leading term at n = m − 1 (via symmetry), not n = m as the
   table caption implies. Pass 1's alignment scheme missed this; repass
   corrects it.

## Compute used
- Host: `CherryRd` (free / personal)
- CPU only: ~1.5 s for the full repass script, ~15 s for the pass-1 pytest re-run
- Network: 26 small HTTP GETs to `oeis.org` (b-files for OEIS sequences)
- No GPU, no paid API, no private data.
