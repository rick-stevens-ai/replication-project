# Workflow — Replication of Hotta 2006 (cond-mat/0611113)

## 1. Extraction
- `pdftotext -layout paper.pdf work/paper.txt` (8 pp, 797 lines).
- Read the full paper; identified the exactly-solvable core (local f-electron
  CEF+SO Hamiltonian, eqs 1-9; multipole operator algebra, eqs 16-22) vs the
  NRG-dependent results (chi(T), phonons, Figs 2-3) that are out of scope.
- Logged in `extraction/marker.md`.

## 2. Claim selection (5 machine-checkable)
1. SO splits 14 f-orbitals into j=5/2 (6) + j=7/2 (8), gap (7/2)*lambda.
2. j=5/2 CEF-splits into Gamma5 doublet + Gamma67 quartet; GS flips with sign(x).
3. 15 multipole operators orthonormal: Tr(Xg Xg')=delta.
4. 4u and 5u octupole do NOT mix for n=5 (j=5/2).
5. Reported mixing coefficients (p,q,r) are unit-normalized.

## 3. Implementation (`code/`)
- `multipole_ops.py` — builds J=5/2 angular-momentum matrices via ladder ops,
  then all dipole/quadrupole/octupole operators (eqs 17-22) with permutation-
  symmetrized products for the overbar operations. Checks orthonormality,
  4u/5u overlaps, and coefficient norms. -> Claims 3,4,5.
- `cef_levels.py` — builds the 14x14 single-electron H = H_so + H_CEF in the
  |m,sigma> basis. H_so from eqs (2)-(3); H_CEF from the Th Hutchings matrix
  (eq 8) parameterized by (W,x,y) via eq (9). Exact diagonalization
  (numpy.linalg.eigh), degeneracy clustering. -> Claims 1,2.

## 4. Execution (`work/`)
- `python3 code/multipole_ops.py | tee work/multipole_out.txt`
- `python3 code/cef_levels.py    | tee work/cef_out.txt`
- Environment: Python 3.14, numpy 2.4.3, scipy 1.18.0 (macOS, CherryRd).

## 5. Comparison (`report/comparison.json`)
- Quantitative match table for all 5 claims. All exact to machine precision
  (Claims 1-4) or within the paper's 3-digit rounding (Claim 5).

## 6. Reporting
- `report/REPORT.tex` (+ compiled `REPORT.pdf`), `open_questions.json` (5),
  `artifacts_summary.md`, `failure_analysis.md`, this file.

## Reproduce
```
cd TEXTURE-multipolar-hotta2006
python3 code/multipole_ops.py
python3 code/cef_levels.py
```
