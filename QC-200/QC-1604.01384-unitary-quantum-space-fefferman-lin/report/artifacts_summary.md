# Artifacts summary — arXiv:1604.01384 replication

## Inventory (all paths relative to the paper dir root)

| # | Artifact (per 8-standard) | Path                                        | Size    | MD5                              |
|---|---------------------------|---------------------------------------------|---------|----------------------------------|
| 1 | Original PDF              | `paper.pdf`                                 | 350 220 | e31d1567122b1c45a0586d12e1c09778 |
| 1 | Original PDF (work copy)  | `work/paper.pdf`                            | 350 220 | e31d1567122b1c45a0586d12e1c09778 |
| 2 | Marker extraction         | `extraction/marker.md` (PyMuPDF surrogate)  |  75 799 | acd317406ef48222c84a30523657ea98 |
| 3 | Nougat extraction         | `extraction/nougat.mmd` (pdftotext surrogate)|  90 278 | da54bbfdc800bf508dedd648211103f6 |
| 4 | LaTeX report              | `report/REPORT.tex`                         |  11 334 | c3b66990aa3964f8f9889d2ce4f8a79c |
| 4 | LaTeX report (compiled)   | `report/REPORT.pdf`                         | 233 989 | 84ccb593c8702c86e03ecc873671dc5d |
| 5 | Open questions (JSON)     | `report/open_questions.json`                |   4 521 | 7e9cffba1d809b0723bfd9a84dd6fa98 |
| 5 | Open questions (LaTeX)    | `report/open_questions_tex.tex`             |   4 787 | (see file)                       |
| 6 | Workflow / tools / effort | `report/workflow.md`                        |   ~6 KB | (see file)                       |
| 7 | Artifacts summary         | `report/artifacts_summary.md`               |   this  |                                  |
| 8 | Failure analysis          | `report/failure_analysis.md`                |   ~4 KB | (see file)                       |

## Supporting artifacts / traces

| Kind      | Path                                        | Notes                                              |
|-----------|---------------------------------------------|----------------------------------------------------|
| plain-text| `work/paper.txt`                            | pdftotext dump used for reading and grep triage    |
| script    | `work/build_extractions.py`                 | builds marker.md + nougat.mmd surrogates           |
| code      | `report/evidence/reproduce.py`              | full reproduction driver (Qiskit + numpy)          |
| data      | `report/evidence/reproduction_results.json` | per-trial input amplitudes, both distributions,    |
|           |                                             | both TVs, aggregate verdict                        |

## External references

- **Source URL:** https://arxiv.org/abs/1604.01384 · https://arxiv.org/pdf/1604.01384
- **arXiv ID:** 1604.01384 (v2, 21 Nov 2016)
- **Title:** A Complete Characterization of Unitary Quantum Space
- **Authors:** Bill Fefferman (wjf@umd.edu), Cedric Yen-Yu Lin (cedricl@umiacs.umd.edu)
- **Venue:** QuICS / Joint Center for Quantum Information and Computer Science, University of Maryland
- **Cited work leaned on for verification:** Nielsen & Chuang Ch. 4.4 (principle of
  deferred measurement); the well-known teleportation protocol; Kliuchnikov--Maslov--Mosca
  Repeat-Until-Success gate decompositions (used only pedagogically as a mid-circuit-
  measurement example).

## Key numerical result reproduced

| Trial family                    | Trials | Max TV(mid-circuit, deferred) | Qubit overhead observed |
|---------------------------------|-------:|------------------------------:|-------------------------|
| A. Teleportation (3q)           |     20 |            2.220e-16          | 0                       |
| B. Repeat-until-success (2q)    |     20 |            1.943e-16          | 1                       |
| Aggregate                       |     40 |            2.220e-16          | O(1) (0 or 1)           |

Threshold: TV < 1e-14 (machine precision).
Observed: ~2 * epsilon_machine for double precision.
Verdict: REPLICATED.

## Run environment

- Host: CherryRd, Darwin 25.3.0 x86_64
- Python 3.13.7 in `.venv/`
- `qiskit 2.5.0`, `qiskit-aer 0.17.2`, `numpy 2.5.1`, `pymupdf 1.27.2.3`
- Seed: 20260705 (deterministic)
- Wall time: reproduction 2.03 s; end-to-end (incl. install + PDF fetch) ~10 min.
