# Workflow — QC-2401.11056 GM-QAOA replication

## 0. Environment (single-machine, free)
- Host: CherryRd (macOS, x86_64), Python 3.14.6, single core.
- Fresh venv at `.venv/` inside the replication dir.
- `pip install --quiet qiskit numpy scipy matplotlib` (Qiskit installed for cross-check; reported numbers use the NumPy simulator).
- No external LLM in the loop for the numerical claims.

## 1. Paper acquisition
- `curl -L https://arxiv.org/pdf/2401.11056v3 -o work/paper.pdf`
- `pdftotext work/paper.pdf work/paper.txt` for method reading.

## 2. Reimplementation from operator definition
- Coded the Grover mixer from its rank-1 exact form: `U_GM(β) = I + (e^{-iβ}-1) |s><s|`, with `|s> = H^{⊗n}|0>`. This avoids importing any GM-QAOA package and puts the physics under our own control.
- Coded the X-mixer as the tensor product of `exp(-iβX)` per qubit.
- Diagonal cost operator: `<ψ|C|ψ> = Σ_x |ψ(x)|² · C(x)` — exact expectation, no shot noise.

## 3. Experiments (all in `code/gm_qaoa.py`)
### E1 — Permutation invariance (C1, C2)
- Graph A: 6 nodes, 8 edges (ring + 2 chords), p=2, β=(0.7,1.3), γ=(0.4,1.1).
- Graph B: 5 nodes, 7 edges (ring + 3 chords), p=3, β=(0.55,0.90,1.25), γ=(0.20,0.75,1.10).
- Compute `<C>_GM` and `<C>_X` at fixed angles on identity permutation, then on 12/8 uniform-random permutations. Record deviation from identity value.

### E2 — Grover-binary Eq. (8) (C3)
- Binary cost c(x) = -1 on k marked bitstrings, 0 elsewhere, n=6 (N=64).
- For r ∈ {1,2,3,4} set k = floor(ρ_Th(r) · N), run GM-QAOA with all angles = π.
- Measure total probability mass on marked states; compare to `sin²((2r+1)·arcsin(√ρ))`.

### E3 — MAX-CUT approximation ratio (C4)
- Graph A. For each p ∈ {1,2,3} and each mixer, 40 COBYLA restarts from random angles.
- Report best `<C>` and ratio `<C>/cost_max` per (mixer, p).

## 4. Verification and evidence capture
- All numeric results dumped to `report/evidence/results.json` (per-permutation and per-restart).
- Cross-checked C3 closed-form values by evaluating `sin²((2r+1)·arcsin(√ρ))` in a separate numpy expression.
- Wall time ~82 s single-core.

## 5. Reproduction command (single copy-paste)
```
python3 -m venv .venv
.venv/bin/pip install --quiet --upgrade pip
.venv/bin/pip install --quiet qiskit numpy scipy matplotlib
.venv/bin/python code/gm_qaoa.py
```

## 6. Deliverables
- `report/REPORT.md` — narrative report (original, preserved).
- `report/REPORT.tex` — LaTeX version with critique section (this backfill).
- `report/open_questions.json`, `report/open_questions_section.tex` — 5 concrete follow-ups.
- `report/workflow.md` — this file.
- `report/artifacts_summary.md` — one-line per deliverable.
- `report/failure_analysis.md` — honest critique of what is thin.
- `extraction/nougat.mmd` — extraction stub (not the numerical evidence path).
