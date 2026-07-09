# Brief — OSTI-2588304

Guan et al. couple a CGCNN surrogate with lattice Monte Carlo to build a
thermodynamic phase diagram for the Lu-H-N high-pressure hydride system, motivated
by the retracted 2023 near-ambient-superconductivity claim in N-doped LuH₃.
Their headline scientific finding is that at moderate pressures the equilibrium
N solubility in the fcc LuH₃₋ₓNᵧ phase is very small (xN/xLu ≤ 0.02) — consistent
with the failed experimental reproductions of the superconductivity claim.

This replication (v2) exercises the method core end-to-end on both a synthetic
Lu(H,N,Va)₃ surrogate that matches the paper's qualitative Fig 2a structure and,
newly in v2, on 86 REAL Materials Project DFT-computed metal-hydride formation
energies (spanning 18 metals). CGCNN with the paper's exact Table I hyperparameters
reaches paper-target accuracy on the synthetic pipeline (MAE 2.94 meV/atom, R²=0.99)
and reaches 82.6 meV/atom / R²=0.64 on the real MP data (10× less training data,
much harder cross-metal transfer, still beats predict-mean baseline by 32%). An
extended MC + thermodynamic-integration pipeline reproduces the paper's
methodological class of F(T) calculations with correct positive-definite C_v and
monotonic F(T). Independent LLM-judge (Argo gpt-4.1) confirms verdict **PARTIAL** —
paper's methodology reproduced, its SI-specific numbers and full para-equilibrium
scientific conclusion (C6) not reached in this budget.
