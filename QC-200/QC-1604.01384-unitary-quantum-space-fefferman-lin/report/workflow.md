# Workflow — arXiv:1604.01384 replication

## Narrative

1. **Paper acquisition** — pulled PDF from `https://arxiv.org/pdf/1604.01384`
   (v2, 21 Nov 2016, 350 KB) into `work/paper.pdf`, mirrored as `paper.pdf`
   at the root.
2. **Extraction** — ran `pdftotext` for a quick reading pass into
   `work/paper.txt`, and then a PyMuPDF (fitz) pass into
   `extraction/marker.md` (labeled Marker surrogate) and a
   `pdftotext -layout` pass into `extraction/nougat.mmd` (labeled Nougat
   surrogate). Marker/Nougat CLIs are not installed on this host or on any
   paired host reachable at run time; the surrogate pattern mirrors sibling
   QC-200 directories.
3. **Author + title verification** — first two lines of `paper.txt` confirm
   title "A Complete Characterization of Unitary Quantum Space" and authors
   Bill Fefferman + Cedric Yen-Yu Lin (arXiv:1604.01384v2).  The task hint
   "SCOUT title starts Bill..." was author-name bleed and is resolved.
4. **Claim triage** — grep'd the extracted text for
   `intermediate measure|deferr|purif|BQSPACE|BQU|ancilla|constant.*overhead`.
   Selected the deferred-measurement + purification lemma (Theorem 19 core)
   as the one numerically checkable claim.  Complexity-class equalities
   (Theorem 6, Corollary 3) are proof-only and not amenable to numerical
   reproduction on a laptop.
5. **Environment** — created `.venv/`, installed `qiskit 2.5.0`,
   `qiskit-aer 0.17.2`, `numpy 2.5.1`, `pymupdf 1.27.2.3`.
6. **Reproduction code** — wrote `report/evidence/reproduce.py`:
   * Two circuit families: quantum teleportation (2 mid-circuit meas + 2
     classical corrections) and a repeat-until-success ancilla primitive
     (1 mid-circuit meas).
   * For each, an analytic mid-circuit distribution + a
     `Statevector.from_instruction` deferred-circuit distribution.
   * TV distance metric, threshold `< 1e-14`.
   * 20 Haar-random input states per experiment, seed `20260705`.
7. **Run** — ~2 seconds wall time on CherryRd; wrote
   `report/evidence/reproduction_results.json`.  All 40 trials pass with
   `max TV = 2.22e-16`; qubit overhead 0 (teleportation) / 1 (RUS).
8. **Reporting** — authored `report/REPORT.tex` (compiled to `REPORT.pdf`
   via pdflatex; TeX Live 2024 on macOS), `report/open_questions.json`
   (5 items with q/basis/next_steps), and this workflow +
   artifacts_summary + failure_analysis triple.

## Tools + code + versions

| Tool / package        | Version    | Where               | Purpose                              |
|-----------------------|------------|---------------------|--------------------------------------|
| Python                | 3.13.7     | CherryRd / .venv    | driver                               |
| numpy                 | 2.5.1      | .venv               | linear algebra                       |
| qiskit                | 2.5.0      | .venv               | circuits, statevector, if_test       |
| qiskit-aer            | 0.17.2     | .venv               | statevector reference simulator      |
| PyMuPDF (fitz)        | 1.27.2.3   | .venv               | marker.md surrogate                  |
| poppler / pdftotext   | system     | /usr/local/bin      | paper.txt + nougat.mmd surrogate     |
| pdflatex (TeX Live)   | 2024       | /usr/local/bin      | REPORT.tex -> REPORT.pdf             |
| curl                  | system     | /usr/bin            | arXiv PDF fetch                      |
| grep / head / tail    | system     |                     | triage / audit                       |

### Written / added

| File                                        | Bytes  | Purpose                                        |
|---------------------------------------------|--------|------------------------------------------------|
| `work/paper.pdf` + `paper.pdf`              | 350 KB | source paper                                   |
| `work/paper.txt`                            | ~150 KB| pdftotext dump (reading + grep)                |
| `work/build_extractions.py`                 | 2.2 KB | builds marker.md + nougat.mmd surrogates       |
| `extraction/marker.md`                      | 76 KB  | Marker surrogate (PyMuPDF)                     |
| `extraction/nougat.mmd`                     | 90 KB  | Nougat surrogate (pdftotext -layout)           |
| `report/evidence/reproduce.py`              | 17 KB  | full reproduction driver                       |
| `report/evidence/reproduction_results.json` | ~20 KB | per-trial records + aggregate                  |
| `report/REPORT.tex` + REPORT.pdf            | ~230 KB| detailed section-by-section LaTeX report       |
| `report/open_questions_tex.tex`             | 4.8 KB | Q1..Q5 as LaTeX                                |
| `report/open_questions.json`                | 4.5 KB | Q1..Q5 as JSON                                 |
| `report/workflow.md`                        | this   | this file                                      |
| `report/artifacts_summary.md`               | –      | artifact inventory                             |
| `report/failure_analysis.md`                | –      | honest gaps                                    |

## Effort estimate

- **Human/agent turns:** ~15 tool calls end-to-end (fetch, triage, install,
  code, run, extract, LaTeX, compile, audit).
- **Wall clock:** ~10 minutes (including qiskit + qiskit-aer install).
- **Compute time:** simulation run wall time 2.03 s (single core).
  Qubit counts used: 2--3.  No GPU / no HPC.
- **Lines of code written:** ~450 (Python), ~180 (LaTeX), ~200 (docs).
- **Free-endpoint LLM inference:** none used for the reproduction itself
  (self-verdict; the ground-truth is a bit-exact statevector comparison).

## Reproducibility

```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-200/QC-1604.01384-unitary-quantum-space-fefferman-lin
python3 -m venv .venv && source .venv/bin/activate
pip install --upgrade pip
pip install qiskit==2.5.0 qiskit-aer==0.17.2 numpy pymupdf
python work/build_extractions.py
python report/evidence/reproduce.py
```

Deterministic (seed 20260705); expected exit line:
`verdict = REPLICATED`, `max_TV = 2.220e-16`.
