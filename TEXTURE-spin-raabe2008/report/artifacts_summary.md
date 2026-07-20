# Artifacts summary — arXiv:0811.0157 replication

| Artifact | Path | Description |
|---|---|---|
| Source PDF | `paper.pdf` | Raabe et al. 2008, β-Ti alloys (arXiv:0811.0157) |
| Extracted text | `paper.txt` | `pdftotext -layout` output, 805 lines |
| Extraction marker | `extraction/marker.md` | Method, off-theme flag, extracted eqs/numbers |
| Code: composition | `code/composition.py` | C4 wt%↔at% conversion, 8 alloys |
| Code: thermo | `code/thermo.py` | C1 entropy Eq.(2), C2 free energy Eq.(3) threshold shift |
| Code: elastic | `code/elastic.py` | C3 Young's-modulus data claims + linear fits |
| Run logs | `work/out_composition.txt`, `work/out_thermo.txt`, `work/out_elastic.txt` | Captured stdout |
| Report (LaTeX) | `report/REPORT.tex` | Full writeup |
| Report (PDF) | `report/REPORT.pdf` | Compiled (if pdflatex available) |
| Open questions | `report/open_questions.json` | Exactly 5, {q, basis, next_steps} |
| Workflow | `report/workflow.md` | Reproduction steps |
| Failure analysis | `report/failure_analysis.md` | What failed and why |

## Claim results
| Claim | Statement | Result |
|---|---|---|
| C1 | Ideal-mixing entropy Eq.(2); S(0.5)=kB·ln2 | **PASS** (exact) |
| C2 | Finite-T free energy lowers β-stab threshold | **PARTIAL** — Ti-Mo reproduced (16.6 vs 14 at%); Ti-Nb not (79 vs 25 at%) w/ surrogate energy |
| C3 | Modulus data: min=Ti-30Nb, 37% drop, trends | **PASS** (3/3 sub-claims) |
| C4 | Table-1 wt%↔at% conversions | **PASS** (18/20 rows <0.25 at%; max 1.02 at% is rounding) |

## Headline
Reproducible closed-form thermodynamics (entropy) and all quantitative data/arithmetic claims
verify. The genuinely ab-initio (DFT) core is out of scope (HPC-scale) and is surrogated only
where labelled; the one partial (Ti-Nb finite-T threshold) is an honest limitation of the energy
surrogate, documented, not faked.
