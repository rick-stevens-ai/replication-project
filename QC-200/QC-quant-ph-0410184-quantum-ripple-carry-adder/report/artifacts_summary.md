# Artifacts summary — QC-200 / quant-ph/0410184

## Inventory

| # | Path                                | What it is                                                   | Genuine? |
|---|-------------------------------------|--------------------------------------------------------------|----------|
| 1 | `paper.pdf`                         | Original arXiv PDF (v1, 9 pp, 111 KB, PDF 1.4)               | yes — fetched from arxiv.org |
| 2 | `paper.txt`                         | `pdftotext` dump of paper.pdf                                | yes |
| 3 | `extraction/marker.md`              | **Fallback**: pdftotext text with a marker-substitute header | partial — see critique |
| 4 | `extraction/nougat.mmd`             | **Fallback**: pdftotext text with a nougat-substitute header | partial — see critique |
| 5 | `code/cdkm_adder.py`                | Qiskit MAJ / UMA / simple / optimized adder implementations  | yes — original, transcribes Fig 1, 2, 4, 5 |
| 6 | `code/verify_adder.py`              | Truth-table verifier (all 2^(2n+1) input triples at n=3,4,5) | yes |
| 7 | `report/evidence/results.json`      | JSON dump of every gate count, depth, error count            | yes — real Qiskit run |
| 8 | `report/REPORT.tex`                 | Full LaTeX report with verdict                               | yes |
| 8a| `report/REPORT.pdf`                 | Compiled PDF (if pdflatex succeeded — see failure_analysis)  | see below |
| 9 | `report/open_questions.json`        | 5 non-superficial open questions with `next_steps`           | yes |
| 10| `report/workflow.md`                | Comprehensive workflow + tool versions + effort estimate     | yes |
| 11| `report/failure_analysis.md`        | Honest friction / gap analysis                               | yes |

## Traces (evidence)

`report/evidence/results.json` — machine-readable record of what actually ran:

- `simple_adder.{n=3,4,5}`: `cases_tested`, `errors`, `gate_counts`, `depth`
  → All zero errors. Simple adder gate counts differ from optimized as
  expected (it's the pedagogical Figure 4 version, not the size-optimized one).
- `optimized_adder.{n=4,5}`: `cases_tested`, `errors`, `gate_counts`,
  `expected_counts`, `matches_paper_size`, `depth_measured`, `depth_expected`
  → All zero errors AND all three gate types match the paper's closed forms
  exactly, AND depth matches exactly.
- `n=3` for the optimized adder is intentionally skipped (paper: Fig 5
  pseudocode requires `n ≥ 4`).

## Genuine critique

**What we did well:**
- The paper's Fig 5 pseudocode is unambiguous once you fix a qubit-index
  convention; a line-for-line translation gave a first-try correct adder.
- Truth-table verification is exhaustive at n=3,4,5 (2688 total triples,
  including all values of z), so there's no risk of a lucky sample masking
  a subtle bug (e.g., a specific carry pattern).
- Statevector (not Aer shots) means zero sampling noise — every "match" is
  a deterministic identity check.

**Weaknesses of this replication:**
1. **We did not test the three variants** (mod-$2^n$, incoming-carry, high-bit-only
   / comparator) tabulated in Table 1 of the paper. The main-adder verdict is
   solid, but the paper's Table 1 has 6 rows and we only covered the top row.
   Extending is straightforward (each variant is a documented tweak of Figure 5)
   but was out of scope for the timebox.
2. **Marker/Nougat fallback.** Neither structured-PDF parser is installed on
   CherryRd for this run, so both `extraction/marker.md` and
   `extraction/nougat.mmd` are pdftotext dumps with a header note. The
   downstream replication did not depend on them (we read the PDF directly),
   but strict readers of the 8-artifact bar should note this substitution.
3. **Depth interpretation.** The paper's depth accounting says `2n-1 Toffoli
   slices + 5 CNOT slices = 2n+4`, but places the negations without explicit
   time-slice assignment. Our `qc.depth()` also returns `2n+4` at n=4,5, which
   we interpret as evidence that the X gates fit inside the CNOT end-caps
   (see Open Question Q2), but we did not produce a slice-by-slice diagram to
   prove this structurally.
4. **No hardware-mapped test.** All results are on all-to-all logical
   connectivity. See Q1 for the follow-up.
5. **No comparison with the VBE adder** was rerun; we cite the paper's own
   comparison uncritically.

**What we did NOT hide:**
- The simple (Fig 4) adder's gate counts are visibly different from the
  optimized formulas — we reported both.
- The n=3 optimized case is skipped rather than fabricated. Table entries
  are honestly marked "skipped (paper: n≥4 only)".
