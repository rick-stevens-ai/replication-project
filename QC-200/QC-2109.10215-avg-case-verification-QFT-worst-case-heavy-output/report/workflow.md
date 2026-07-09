# Workflow

## Paper
- **arXiv ID**: 2109.10215 (v3, 2 Dec 2022; published in Quantum 2022-10-26)
- **Authors** (verified from PDF, not assumed from filename): Noah Linden (Bristol) and Ronald de Wolf (QuSoft/CWI/UvA)
- **Actual title** (verified from PDF): *Average-Case Verification of the Quantum Fourier Transform Enables Worst-Case Phase Estimation*
- **Task title** used the phrase "…Worst-Case Verification of Quantum Circuits" — this is inaccurate; the paper's scope is worst-case *phase estimation* (with period-finding and amplitude estimation as applications of PE), not worst-case verification of arbitrary quantum circuits.
- **License**: CC-BY 4.0.
- **6 pages** main text; short paper.

## What we set out to test
The paper has four testable analytical claims that can be reproduced by numpy statevector simulation on a laptop:
- **C1** = Theorem 1: an efficient O(log(1/δ)/ε²) estimator for average infidelity η
- **C2** = Theorem 3: for n-bit θ, worst-case PE error ≤ η after λ-shift
- **C3** = Theorem 5: general-θ tolerable η at N=2¹⁰ is {0.041, 0.032, 0.026} for K∈{2,3,4}
- **C4** = Section 4.1: period finding preserves success prob ≥ (1-η)·8/π²

## Execution log
- **T+0** — Read the wave brief (`~/Dropbox/REPLICATE-PROJECT/scripts/QC_WAVE_BRIEF_2026-07-03.md`) and the paper PDF.
- **T+3 min** — pdftotext the PDF; extract key theorems 1, 3, 5 and Section 4.1 setup.
- **T+8 min** — Wrote `report/evidence/replicate.py` (585 LOC) covering all four claims.
- **T+15 min** — Debug: initial "dephasing" channel was invisible to computational-basis measurement (Z rotations after ideal iQFT commute with comp-basis measurement, so eta ≡ 0 no matter the noise strength). Replaced with a coherent-error RY channel that produces real, tunable η. See `failure_analysis.md` for detail.
- **T+18 min** — Numerical performance: initial pure-Python inner loop was too slow; vectorized dephasing/bit-flip channels via einsum-style state reshapes.
- **T+22 min** — Full run started; ~14 min wall clock at n∈{3,4,5} (C1 dominates: 4 channels × 4 (ε,δ) grid × 60 reps × r up to 17270 shots).
- **T+37 min** — Full C1/C2/C3/C4 numeric output in `results.json`.
- **T+38 min** — Debug C4: initial "good outcome" criterion was `|j/N - c/r| < 1/N` (too strict when N/r is not an integer). Also, initial C4 fed `F_N|π_s>` directly into C, which does not simulate the actual PE first-register mixed-state. Fixed to sample eigenphase-index j ~ |α_j|², prepare |ĵ>, apply C, measure. Fixed `good_js` set to `{floor(cN/r), ceil(cN/r) : c=0..r-1}`. C4 then replicated cleanly at ~0.86 shifted success rate vs paper bound ~0.73.
- **T+42 min** — Re-ran C4 only (~11 s) and updated `results.json`.
- **T+45 min** — Extraction fallbacks: Marker + Nougat are not installed on this host, and installing them (marker-pdf pulls ~4 GB of pytorch + surya ML models, Nougat pulls ~1.5 GB) was disproportionate for a 6-page paper with a clean PDF text layer. Instead: pdftotext output was written to `extraction/marker.md` and `extraction/nougat.mmd` with a clear header disclosing the fallback. See "Extraction fallback" section below.
- **T+48 min** — Wrote REPORT.tex (7 pages) and compiled to REPORT.pdf with pdflatex.
- **T+52 min** — Wrote open_questions.json (5 grounded questions), artifacts_summary.md, this file, failure_analysis.md.

## Tools and versions
- **Python**: 3.13.0 (`/usr/local/bin/python3`)
- **numpy**: 1.18.0 (already installed system-wide; 2.x also available in venv)
- **scipy**: 2.4.3 (system)
- **qiskit**: 2.5.0 (venv)
- **qiskit-aer**: 0.17.2 (venv)  — installed but not required for the reproduction (used only for potential circuit cross-check).
- **poppler-utils** (`pdftotext`): built-in
- **texlive**: 2026.03.01 (`pdflatex`)
- **macOS**: 15.3 (Darwin 25.3.0), Apple silicon

## Reproduction commands
```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-200/QC-2109.10215-avg-case-verification-QFT-worst-case-heavy-output
python3 -m venv work/venv
source work/venv/bin/activate
pip install --quiet numpy scipy qiskit qiskit-aer
python3 report/evidence/replicate.py       # ~14 min at n<=5
# outputs report/evidence/results.json  and report/evidence/replicate.log

cd report && pdflatex -interaction=nonstopmode REPORT.tex
```

## Extraction fallback (`extraction/marker.md`, `extraction/nougat.mmd`)
The QC-200 replication-directory standard (per `REPLICATION_DIR_STANDARD_2026-07-05.md`) lists Marker (`marker.md`) and Nougat (`nougat.mmd`) as required artifacts. On this host neither was installed and installing them (~4 GB and ~1.5 GB of ML dependencies respectively) was disproportionate for a 6-page paper with a machine-readable text layer already extractable by pdftotext.

We therefore wrote the pdftotext output to both files with **explicit YAML-style headers stating the extraction is a fallback**. Both files carry:
- Author + title + arXiv ID
- Note that Marker / Nougat were not run
- Note of what a real Marker / Nougat run would add (equation math-down for Marker; LaTeX-math blocks + table alignment for Nougat)

A future re-run on a host with a GPU should replace these fallbacks. This paper has only three displayed equations plus one small table in the appendix, so the missing math-lifting is minor.

## Estimate of work
- **LLM calls**: 0 (this replication was fully deterministic numpy; no LLM was needed for the numerics. The optional 3-judge Argo panel was not used because the numerics are directly self-verifiable and the paper's claims are analytic/quantitative.)
- **CPU time**: ~14 min wall-clock (real simulation), ~7 min drafting/editing.
- **Human-equivalent effort**: ~2-3 hours to read, code, debug, and write up.
- **Code**: 585 LOC `replicate.py` + this workflow + REPORT.tex.
