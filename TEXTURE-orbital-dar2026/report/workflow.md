# Workflow — dar2026 BdG altermagnet triplet replication

## Paper
Dar, Scheurer & Schrade, "Altermagnetic spin textures coupled to superconductors:
Domain wall spin-triplet superconductivity and supercurrent-induced torques",
arXiv:2607.15249v1 (cond-mat.supr-con, 16 Jul 2026).

## Task class
From-scratch computational replication (no author code — the paper states code is
"available upon request", no public repo). Method class: real-space
Bogoliubov–de Gennes (BdG) diagonalization of a proximitized altermagnetic domain
wall. Physics was already run; this pass is **packaging + honest verdict** (no
heavy re-run beyond one verification execution).

## Pipeline executed
1. **Read** the paper text (`textures-orbital-dar2026.txt`, 2823 lines) — the
   richest source — to establish the headline claim, the effective Hamiltonian
   (Eqs. 1,3,7,15,16), and the discriminating test (Fig. 4a vs 4b: fourfold
   modulation vanishes in the AFM limit).
2. **Read** the existing evidence: `work/dar2026_result.json` and the solver
   `work/dar2026_bdg.py`, plus `replication_recipe.json`.
3. **Verify** — re-ran the solver end-to-end with
   `/home/stevens/comfyui-env/bin/python dar2026_bdg.py` (~125 s: two 7744-dim
   dense `eigh` calls, AM + AFM). Printed output matched the saved JSON to all
   quoted digits (hermiticity 0.0, singlet max 2.437e-3, I_t max AM/AFM
   8.52/8.42e-11, angular modulation 0.119/0.122). No stale-JSON risk.
4. **Extraction artifacts** — `marker`/`nougat` not installed; produced honest
   `pdftotext` interims:
   - `extraction/marker.md` = `pdftotext -layout` (prose) + NOTE header.
   - `extraction/nougat.mmd` = hand-transcribed LaTeX "Key equations" block
     (Eqs. 1,3,7,15,16,17 + node conditions) followed by the raw reading-order
     `pdftotext` dump + `%` NOTE header.
5. **Report artifacts** — REPORT.tex (section-by-section + comparison table +
   verdict), open_questions.json (5 Qs + next_steps), workflow.md,
   artifacts_summary.md, failure_analysis.md.
6. **Evidence** — copied `dar2026_result.json`, `dar2026_bdg.py`,
   `replication_recipe.json` into `report/evidence/`.
7. **Validate** — JSON parse-checked; full artifact tree audited.

## Tools / versions
- `/home/stevens/comfyui-env/bin/python` — numpy 2.3.5, scipy 1.17.0.
- `pdftotext` (poppler) — extraction fallback. `marker`, `nougat`, `pdflatex`: ABSENT.
- Solver: dense `scipy.linalg.eigh` on the 4N^2 = 7744 real-space BdG matrix;
  scipy.sparse for construction.

## Effort estimate
- Physics run (pre-done): ~125 s wall clock per full AM+AFM pass; trivial compute
  (single workstation core, no GPU/HPC — matches recipe's "modest" target).
- Packaging pass (this work): ~40 min including the verification re-run.

## Compute target
Local spark / workstation CPU. No HPC routing needed (small dense matrices).
