# Workflow — arXiv:2107.02789 replication

## Sequence
1. **Fetch paper** (`work/paper.pdf`, `work/paper.txt`) from arXiv.
2. **Read Sections II–III** to extract:
   - Standard QAOA layer form `exp(−iβH_M)·exp(−iγH_C)`.
   - CD layer form (Eq. 9 for MaxCut): CD pool `A = {Z_iY_j, Y_iZ_j}` over nearest-neighbour pairs; digitized as product of two-qubit exponentials.
   - Approximation ratio definition `R = ⟨H_C⟩_min / cut_max` (paper uses positive sign convention; we use `R = −⟨H_C⟩/cut_max` with `H_C = Σ 0.5(Z_iZ_j − I)`, algebraically equivalent).
3. **Choose test instances** to fit CPU statevector budget:
   - `K4_n4_3reg`: matches paper's 4-qubit Fig. 3a point exactly.
   - `n6_3reg_a` (networkx seed=1), `n8_3reg_a` (seed=2): independent instances from the same 3-regular family used in Fig. 3b.
   - Brute-force verify cut maxima (4, 9, 10 respectively).
4. **Implement** `code/dcqaoa_maxcut.py`:
   - QAOA ansatz on statevector: apply `H^{⊗n}` init, then per-layer `exp(−iγZZ)` over edges + `exp(−iβX)` over qubits.
   - DC-QAOA ansatz: identical + per-layer `exp(−iα ZY)·exp(−iα YZ)` over edges (Trotter form).
   - COBYLA optimizer, 25 random restarts, rhobeg=0.3, maxiter=500, uniform `[−π,π]` init.
5. **Run sweep** over `p ∈ {1,2,3,4}` × 3 graphs × {QAOA, DC-QAOA} = 24 configurations, ~10 min wall.
6. **Compare** to paper Fig. 3a (K₄ point) and Fig. 3b (depth scaling).
7. **Plot** approximation ratio vs p for all three graphs, both variants.
8. **Verdict + evidence** written to `report/REPORT.md`.
9. **Backfill (2026-07-06)**: LaTeX report, honest critique, 5 open questions, workflow, artifact summary.

## Data flow
```
arXiv 2107.02789 PDF
        ↓ (manual read of ansatz + CD pool)
code/dcqaoa_maxcut.py  ────────►  report/evidence/maxcut_results.json
                                  report/evidence/maxcut_stdout.log
        ↓
code/plot_results.py   ────────►  report/evidence/approx_ratio_vs_p.png
        ↓
report/REPORT.md  (verdict, tables, comparison)
        ↓ (backfill)
report/REPORT.tex  +  report/open_questions*.  +  report/workflow.md  +  ...
```

## Environment
- macOS Darwin 25.3.0, Python 3.14.6, `.venv/`.
- Qiskit 2.5.0, qiskit-aer 0.17.2, numpy 2.4.3, scipy 1.18.0, networkx, matplotlib.
- Runtime: ~10 min CPU (statevector only, no shots, no hardware).

## Reproducibility
```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2107.02789-digitized-counterdiabatic-qaoa
python3 -m venv .venv && source .venv/bin/activate
pip install qiskit qiskit-aer numpy scipy networkx matplotlib
PYTHONUNBUFFERED=1 python -u code/dcqaoa_maxcut.py
python code/plot_results.py
```

Numbers are deterministic to within a few 1e-3 given the fixed COBYLA seed schedule and generous restart budget on the 8-qubit landscape.
