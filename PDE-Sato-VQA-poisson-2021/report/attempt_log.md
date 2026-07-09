# Attempt Log — PDE-Sato-VQA-poisson-2021

Wave: 2026-07-01 push.  Executor: subagent PDE-Sato-VQA-poisson-2021.

## Timeline

- **18:10 CDT** — Task received. Created target dir and read wave brief.
- **18:10** — Fetched paper PDF from arXiv (2106.09333). Confirmed 27 pages, saved to `work/sato_2021.pdf`.
- **18:11** — Extracted text with `pdftotext`, isolated key sections (formulation, ansatz spec, numerical experiments).
- **18:11** — Confirmed the authors' official code repo exists at https://github.com/ToyotaCRDL/VQAPoisson.
  Cloned it. It requires Qiskit 0.23 + qiskit-aqua (aqua is retired) — running unchanged is not viable on a modern stack.
  **Decision:** implement paper's math from scratch in numpy (statevector sim). For n≤6 this is faster than Qiskit anyway
  and lets us confirm the formulation, not just re-run the authors' bundled harness.
- **18:12** — Wrote `work/vqa_poisson_replicate.py`. Key pieces:
  - Alternating layered ansatz: (Ry×n + CNOT ladder)^L + final Ry×n. Params = (L+1)·n.
  - Poisson matrix builder for Dirichlet / periodic / Neumann.  Regularization ε=1e-3 on singular cases (paper spec).
  - `|f>` prepared per paper Eq. (45): step +1/√N / -1/√N.
  - Cost E_h = -½ ⟨f|ψ⟩² / ⟨ψ|A|ψ⟩  (paper Eq. 14, real-valued specialization).
  - Norm recovery r = 1/√⟨ψ|A²|ψ⟩  (paper Eq. 48).
  - L-BFGS-B optimizer (paper uses BFGS with analytic quantum-gradient; same class, numeric gradient here).
- **18:13** — Smoke test at n=2, single seed: cost → -0.35 (exact), ε_tr = 4·10⁻⁸, norms match to 8 digits, 9 iterations. ✅
- **18:13-18:15** — Full experiment: Dirichlet BC, n∈{2,3,4,5}, 10 trials each, L=5. Ran locally in ~90 s.
  All 40 trials converged. Results saved to `report/evidence/results_dirichlet.json`.
- **18:16** — Periodic BC spot-check at n=5, 5 trials: mean ε_tr = 0.0034, quantum norm 22.68 vs classical 22.89.
- **18:17** — Wrote report / brief / harvest. LLM-judge on Argo Opus for verdict.

## What worked
- Text extraction of arXiv PDF was clean enough to lift all key equations & experimental hyperparameters.
- Direct numpy statevector sim avoided a Qiskit-0.23/aqua dependency-hell; runs entirely offline, on free compute.
- The paper's numeric targets (ε_tr < 0.01 at n=5, norm ≈ 24.6 quantum vs 25.3 classical) reproduced within noise.

## What did not need to be done
- Qiskit installation and porting the authors' aqua-based `VQAforPoisson` class (dead dependency).
- Any GPU / uicgpu offload — problem is tiny (n≤5, dim=32).

## Deviations from the paper
- Optimizer: L-BFGS-B (scipy) vs. authors' BFGS with analytic quantum-derived gradient.  Same complexity class,
  and paper explicitly says "the discussion of classical optimization solvers is beyond the scope of this paper"
  and reports Tit as merely an empirical count.  Iteration counts I observed (n=5 ≈ 430) are of the same
  order as the paper's Fig. 6 for ε_tr=0.01 threshold (roughly 10^{2.5-3} = 300-1000).
- Statevector-only: no shot-noise Monte-Carlo (paper's Sec. IV.A also uses statevector; QASM only appears in Sec. IV.B.3
  for shot-noise scaling — out of scope for the core-claim replication).
