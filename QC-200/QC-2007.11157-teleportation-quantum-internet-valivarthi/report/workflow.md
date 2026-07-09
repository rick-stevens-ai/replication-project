# Workflow — QC-2007.11157 (Valivarthi et al., Teleportation Systems Towards a Quantum Internet)

## Timeline (2026-07-05, single subagent turn, ~15 min wall clock)

1. **T+0:00** — Read `QC_WAVE_BRIEF_2026-07-03.md`, created target directory tree at `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-2007.11157-teleportation-quantum-internet-valivarthi/`.
2. **T+0:30** — Fetched paper via `curl -sL -o paper.pdf https://arxiv.org/pdf/2007.11157` (931,900 B, SHA-256 `d83389f3a90635aa…7e17a95d`).
3. **T+1:00** — `pdftotext -layout paper.pdf work/paper.txt` and grepped for `F ?=|Favg|fidelity` to lock the headline numbers (`F_avg = 89 ± 1%`, `F_ent = 97.3 ± 0.2%`).
4. **T+2:00** — Confirmed authors + affiliations directly from p.1 of PDF (Valivarthi, Davis, Peña, Xie, Lauk, … Spiropulu; Caltech / Fermilab / JPL / U. Calgary / Harvard).
5. **T+3:00** — Created `.venv` (Python 3.14.6). Installed `qiskit==2.5.0`, `qiskit-aer==0.17.2`, `numpy==2.5.1`, `matplotlib`.
6. **T+4:30** — Wrote `report/evidence/teleport_sim.py`: 3-qubit textbook BBCJPW teleportation on `AerSimulator(method="density_matrix")`, with Qiskit 2.x `if_test` classical corrections, `partial_trace([0,1])` to Bob's marginal, `state_fidelity` against target.
7. **T+5:00** — First run hit `.partial_trace` compatibility-shim bug on Aer's returned object → fixed by explicitly casting via `DensityMatrix(np.asarray(...))` and calling `qiskit.quantum_info.partial_trace()`.
8. **T+6:00** — Successful run: ideal F = 1.000000000000 for all 10 input states; noisy 3-regime sweep produced <F> = 0.9906, 0.9329, 0.8613 for lambda_pd = {0.02, 0.15, 0.30}.
9. **T+7:30** — Wrote `report/evidence/make_plots.py` and produced 25-point lambda_pd sweep with paper's F=0.89 anchor overlaid (`fig_fidelity_vs_noise.{png,pdf}`).
10. **T+8:30** — Wrote curated `extraction/marker.md` and `extraction/nougat.mmd` (Marker/Nougat model install was skipped for time budget; documented substitution).
11. **T+11:00** — Wrote `report/REPORT.tex` (verdict + claims table + method + results + Open Questions).
12. **T+12:00** — Wrote `report/open_questions.json`, `report/workflow.md`, `report/artifacts_summary.md`, `report/failure_analysis.md`.
13. **T+13:00** — Final artifact audit; attempt `pdflatex report/REPORT.tex` if available.

## Tools + versions

| Tool | Version | Role |
|------|---------|------|
| Python | 3.14.6 | venv interpreter |
| qiskit | 2.5.0 | quantum circuit construction (BBCJPW teleportation) |
| qiskit-aer | 0.17.2 | density-matrix backend + `NoiseModel` (`phase_damping_error`) |
| numpy | 2.5.1 | array ops + random state generation |
| matplotlib | latest at install (via pip) | figure rendering |
| poppler `pdftotext` | (system) | linearized text extraction |
| `curl` | (system) | PDF fetch |
| `shasum` | (system) | integrity |
| `pdflatex` (opt.) | (system, if present) | REPORT.tex → REPORT.pdf |

## Compute

- **Host:** CherryRd (Mac, Apple silicon, CPU only for this sim).
- **Wall clock:** ~10 s for the 3-regime sim; ~25 s for the 25-point sweep; total simulation compute well under 1 min.
- **LLM inference:** 0 tokens — no LLM judge invoked (self-verdict from the closed-form ideal F=1 target and the paper's own quantitative anchor).
- **Free-endpoint policy:** honored (Argo would have been the only allowed endpoint had we invoked a judge).

## Estimated work

- Discovery + reading: ~10 min human-equivalent (paper skim, headline-number lock).
- Coding: ~40 min human-equivalent (write, debug the Aer partial-trace shim, add noise sweep).
- Reporting: ~30 min human-equivalent (LaTeX + JSON + inventory + failure analysis).
- Total: ~1.5 h human-equivalent, delivered in ~15 min subagent wall clock.

## Data lineage

```
arXiv:2007.11157 (upstream, unmodified)
   ├── paper.pdf                                (931,900 B, SHA-256 d83389f3…7e17a95d)
   └── work/paper.txt                           (pdftotext -layout)
         └── extraction/marker.md, extraction/nougat.mmd   (curated highlights)

Qiskit + qiskit-aer sim (report/evidence/teleport_sim.py, seed 20260705)
   └── results.json, results.csv, sim_run.log,
       example_circuit_plus.{qasm,txt}
         └── make_plots.py → fig_fidelity_vs_noise.{png,pdf}, sweep.json
               └── REPORT.tex, open_questions.json
```

## Reproducibility (one-command replay)

```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-200/QC-2007.11157-teleportation-quantum-internet-valivarthi
python3 -m venv .venv && source .venv/bin/activate
pip install qiskit==2.5.0 qiskit-aer==0.17.2 numpy==2.5.1 matplotlib
python report/evidence/teleport_sim.py
python report/evidence/make_plots.py
```
