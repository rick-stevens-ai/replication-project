# Workflow — QC-200 replication of Kempe-Kitaev-Regev (quant-ph/0406180)

## 1. Directory setup
```
mkdir -p ~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-0406180-.../{work,extraction,report/evidence}
```

## 2. Paper acquisition and verification
```
curl -sL -o work/paper.pdf https://arxiv.org/pdf/quant-ph/0406180
pdftotext work/paper.pdf work/paper.txt
```
- Verified title: "The Complexity of the Local Hamiltonian Problem"
- Verified authors: Julia Kempe (CNRS/LRI/Berkeley), Alexei Kitaev (Caltech), Oded Regev (Tel-Aviv). ✓
- v2, 30 pages, 2 Oct 2005.

## 3. Read the paper to the depth needed
- Abstract → 2-local Hamiltonian is QMA-complete; two proofs; second uses perturbation theory.
- Section 6.1 Perturbation theory → Schrieffer-Wolff-like self-energy expansion Σ_-(z), Eq. (12).
- **Section 6.2 The Three-Qubit Gadget** → the operational construction we replicate.
  - Target: `H_target = Y - 6 B1 B2 B3` (3-local via three PSD single-qubit Bs and a 2-local Y).
  - Add 3 mediator qubits.
  - `H = -(δ⁻³/4)(ZZ12+ZZ13+ZZ23 - 3I)` on mediators → gap `Δ = δ⁻³`, low subspace `C = span{|000⟩_m, |111⟩_m}`.
  - `V = X⊗I - δ⁻²(B1⊗σ^x_1 + B2⊗σ^x_2 + B3⊗σ^x_3)` with counter-term `X = Y + δ⁻¹(B1²+B2²+B3²)`.
  - Eq. (14): `Σ_-(z) = Y⊗I_C - 6 B1 B2 B3 ⊗ σ_eff^x + O(δ)`; ground state lives in |+⟩_eff sector where the effective Hamiltonian equals `Y - 6 B1 B2 B3` = `H_target`.
- Section 6.3 → simultaneous application of the gadget to all 3-local terms is what keeps the reduction polynomial (out of scope of our reproduction of a single gadget).

## 4. Extraction artifacts (surrogate; Marker/Nougat not installed)
- `extraction/marker.md` — PyMuPDF (fitz) v1.27.2.3 text dump with `---- page N ----` markers, header labels the actual tool.
- `extraction/nougat.mmd` — `pdftotext -layout` reflow, header labels the actual tool.
- `extraction/README.md` — declares the surrogate and lists tools.

## 5. Reproduction code
- Single file: `report/evidence/reproduce_gadget.py`.
- Dependencies: numpy 2.4.3, scipy 1.18.0 (only numpy actually used for eigh), matplotlib (Agg).
- Runs in <5 s on a single CherryRd core (max Hilbert dim = 2^6 = 64).
- Builds `H_target` and `H_gadget` as dense complex128 matrices, exact-diagonalises with `numpy.linalg.eigh`, projects gadget eigenstates onto |+⟩_eff / |-⟩_eff sectors, computes ground-state and gap errors vs `H_target` across a 10-point Δ sweep.
- Outputs:
  - `report/evidence/results.json` — full machine-readable table
  - `report/evidence/scaling.csv` — Δ, δ, err_gs, err_gap
  - `report/evidence/scaling.png` — log-log err vs Δ plot with paper's O(δ) reference line

## 6. Report
- `report/REPORT.tex` — 6-page detailed LaTeX report; compiled to `report/REPORT.pdf`.
- Includes: abstract, claims table (5 claims C1..C5, 3 numerically tested), method, results table, scaling fit, promise-gap verification, verdict, `## Open Questions` section, references to evidence files.
- `report/open_questions.json` — 5 non-trivial follow-on research questions grounded in what we observed.
- `report/artifacts_summary.md` (this dir's inventory).
- `report/failure_analysis.md` (friction, residual gaps, honest limitations).

## 7. Compile
```
cd report && pdflatex -interaction=nonstopmode REPORT.tex
```
Output: `report/REPORT.pdf` (6 pages, 344 KB).

## Tools and versions
| Tool          | Version   | Use                                              |
|---------------|-----------|--------------------------------------------------|
| Python 3      | 3.x (system) | glue                                           |
| numpy         | 2.4.3     | dense matrices, `linalg.eigh`                    |
| scipy         | 1.18.0    | (not directly used; imported for env check)      |
| matplotlib    | present   | log-log scaling plot                             |
| PyMuPDF (fitz)| 1.27.2.3  | marker.md surrogate extraction                   |
| pdftotext     | poppler   | nougat.mmd surrogate extraction, paper.txt       |
| pdflatex      | TeXLive 20260301 | REPORT.tex → REPORT.pdf                   |

## Work estimate
- Reading + gadget derivation understanding: ~15 min agent time.
- Coding first pass (missing sector projection): ~5 min.
- Debugging (discovered paired |+⟩/|-⟩ structure by inspecting spectrum): ~5 min.
- Final code + sweep + fit + plot: ~5 min run.
- Writing REPORT.tex + open questions + workflow + failure analysis: ~10 min agent time.
- Total elapsed: single agent turn, ~30 min wall.
- LLM cost: zero (Argo tokens used only for orchestration text; no external paid API).
