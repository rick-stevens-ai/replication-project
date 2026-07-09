# Attempt Log — WaveTrain replication (2026-07-04)

Chronological. All times America/Chicago.

## 06:08 — Setup

- Confirmed target dir empty, sibling grep returned nothing.
- Fetched README from https://github.com/PGelss/wave_train — confirms package structure, install command (`pip install git+https://github.com/PGelss/scikit_tt` then `pip install wave_train`), and paper reference.
- `web_fetch` on the AIP PDF returned 403 (Cloudflare) — worked around by reading the paper's method from the GitHub README plus the docstring/param structure of the bundled `test_scripts/` (which effectively encode the paper's example configurations).

## 06:10 — Install

- Created `work/venv` on Python 3.14.6 first. `pip install ./wave_train` and `scikit_tt` both succeeded.
- Ran `wave_train/test_scripts/Exciton/tise_1.py` (via a batch-mode wrapper `run_tise_bench.py` that also compares against analytic).
- State=0 (E=0.0) and state=1 (E=0.08) computed correctly and match analytic exactly.
- Crashed at state=2 with `numpy._core._exceptions._UFuncOutputCastingError: Cannot cast ufunc 'add' output from dtype('complex128') to dtype('float64')` in `scikit_tt/solvers/evp.py:381`.
- Diagnosed: ALS deflation step `micro_op += shift*tmp.dot(np.conjugate(tmp.T))` computes a complex rank-1 outer product but tries to add it in-place to a float64 accumulator. NumPy ≥1.25 refuses the implicit cast. This is a real scikit_tt compat bug for any n_levels ≥ 3.

## 06:16 — Try downgrade first

- Recreated venv with Python 3.12 + `numpy<2` (`numpy==1.26.4`).
- Same crash — the check is enforced by NumPy 1.26 too. It really needs a source patch.

## 06:20 — Patch scikit_tt

- Edited `venv312/lib/python3.12/site-packages/scikit_tt/solvers/evp.py` line ~381:

  ```python
  # before:
  micro_op += shift*tmp.dot(np.conjugate(tmp.T))
  # after:
  update = shift * tmp.dot(np.conjugate(tmp.T))
  if np.iscomplexobj(update) and not np.iscomplexobj(micro_op):
      micro_op = micro_op.astype(np.complex128)
  micro_op = micro_op + update
  ```

- Re-ran. All states now compute for N=6 primary and the full scaling sweep.

## 06:25 — Runs

- N=6, n_levels=8 primary: ~3s wall, band = [0.080, 0.090025, 0.090025, 0.110008, 0.110046, 0.1199], analytic = [0.08, 0.09, 0.09, 0.11, 0.11, 0.12]. max |err| = 1.0e-4.
- Scaling sweep started; N=4 took 0.4s, N=6 2.5s, N=8 102s, N=10 78s, N=12 678s (~11 min).
- N=8 anomaly: cost jumps 40x from N=6→N=8 because the ALS `ranks=15` initial-guess cap is reached at the middle bond; N=10 then finishes faster because the ranks profile is already saturated (steady-state cost, and eigen band happens to converge in fewer sweeps). N=12 is heavy because the deflation shift term (shift=100 × Σⱼ|ψⱼ⟩⟨ψⱼ|) grows quadratically in number of previous states.

## 07:05 — Analysis

- Wrote `work/analyze_bench.py` to re-parse the wave_train log (which prints per-state energy in a fixed format) and pair energies with the analytic tight-binding formula.
- Extracted TT bond ranks per N: ranks are 1,2,4,8 at the boundaries (intrinsic single-particle sector) and grow toward the middle up to our ALS cap of 15. Boundary pattern (1,2,4,8) matches expected 2^k up to Krylov-like truncation.

## 07:15 — LLM judge

- Called Argo proxy (localhost:44497, `argo:claude-opus-4.7`) — got HTTP 502 "Failed to parse upstream response" (a real transient Argo/Claude interaction issue; retries + prompt-simplification did not help).
- Switched to `argo:gpt-5.4`. Verdict returned in JSON: **PARTIAL**, coverage=100%, agreement=78%. See `evidence/llm_judge.json`.

## 07:25 — Write-up

- Composed REPORT.md, brief.md, artifact_harvest.md.
- Wrote scaling table + per-N energy comparison table.
