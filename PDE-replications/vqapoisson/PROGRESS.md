# PROGRESS — VQAPoisson Replication

Started: 2026-05-28 09:42 CDT
Agent: Ollie (subagent, depth 1/1)

## Timeline

- **09:42** — Workspace created. Target repo identified via GitHub API:
  `ToyotaCRDL/VQAPoisson`, Apache-2.0, last push 2023-07-04. License OK to fork.
- **09:43** — Cloned upstream into `repo/`. Inspected `vqa_poisson.py` (521 lines)
  and `sample.ipynb`. Confirmed it is the PRA 104:052409 paper code.
- **09:44** — Diagnosed environment problem: upstream pins `qiskit==0.23.6` +
  `qiskit-aqua==0.8.2` (both EOL years ago) and Python 3.7.4. Decision: port to
  modern Qiskit rather than try to revive a 2020-era pin.
- **09:45** — Created Python 3.12 venv with `qiskit==2.4.1`, `qiskit-aer==0.17.2`,
  numpy 2.4, scipy 1.17, matplotlib.
- **09:46** — Wrote `scripts/vqa_poisson_modern.py`: same algorithm, replaces
  `QuantumInstance.execute` with `qiskit.quantum_info.Statevector.from_instruction`,
  renames `mct→mcx`, otherwise faithful. Wrote `scripts/run_experiment.py` —
  loops over Periodic/Dirichlet/Neumann, BFGS with analytic parameter-shift
  gradient, logs convergence, dumps PNG + JSON.
- **09:46** — Smoke test on n=3 Periodic: A is 8×8 symmetric (symm-err 0.0), all
  eigenvalues > 0 (≥ 1e-3, set by `c`), gradient finite, objective sane.
  Algorithm wiring is correct.
- **09:47** — Launched main experiment `n=3, L=4, seed=0, maxiter=300` for all
  three BCs. `sol_periodic_n3_L4.png` and `sol_dirichlet_n3_L4.png` written —
  both BCs converged. Neumann run in progress (~3+ min wallclock — Neumann has
  the densest gradient because both `_calc_grad_for_bc` branches fire).
- **09:49** — Checkpoint: parent monitor flagged missing `PROGRESS.md`/`README.md`
  at the project root. Files written without interrupting the Neumann run.

## Current status

**Replication complete.** All three BCs converged at n=3, L=4 with energy
errors ≤ 5×10⁻⁶; Periodic also confirmed at n=4, L=5. REPORT.md written.

- **09:50** — PROGRESS.md, README.md, REPORT.md (skeleton) written at parent's request.
- **09:53** — Neumann n=3 done in 135.8 s: rel L2 2.3×10⁻⁶, energy gap +2.1×10⁻¹².
  summary_n3_L4.json written. All n=3 plots and JSON in `results/`.
- **09:54** — Launched n=4, L=5 sweep in background (PID 71729).
- **10:04** — Periodic n=4 done in 446.7 s: 90 iter, rel L2 1.8×10⁻⁵, energy gap
  +1.3×10⁻¹¹. Plot `sol_periodic_n4_L5.png` written. Dirichlet n=4 started.
- **10:09** — Killed n=4 sweep at Dirichlet iter 14 (rel 0.12) to stay within
  wallclock budget. The Periodic n=4 result already demonstrates the algorithm
  scales; n=4 Dirichlet/Neumann recovery is left as future work.
- **10:10** — REPORT.md updated with n=4 Periodic row; PROGRESS.md finalized.

## Final artifacts

- `README.md`, `PROGRESS.md`, `REPORT.md` — documentation.
- `repo/` — untouched upstream clone.
- `scripts/vqa_poisson_modern.py` — port to Qiskit 2.x.
- `scripts/run_experiment.py` — BFGS driver, plot, JSON.
- `results/sol_periodic_n3_L4.png`, `sol_dirichlet_n3_L4.png`, `sol_neumann_n3_L4.png`
- `results/sol_periodic_n4_L5.png`
- `results/summary_n3_L4.json` — headline table for n=3.
- `logs/run_n3_L4.log`, `logs/run_n4_L5.log`.
