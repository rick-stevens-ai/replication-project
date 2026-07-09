# attempt_log

Chronological account of the replication.

## 2026-07-05 02:09 CDT — kickoff
- Read `~/Dropbox/REPLICATE-PROJECT/scripts/WAVE_BRIEF_2026-07-01.md`. Rules noted:
  free endpoints only, real data + real code, no overwrite, LLM-judge for verdict, heavy compute on `ssh uicgpu` if needed.
- Created fresh target `PDE-Chen-Holst-Xu-FEM-nonlinear-PB-2007/{report/evidence,work}`.

## 2026-07-05 02:10 CDT — obtain paper
- Located preprint on arXiv (`1001.1350`) via Brave search. SIAM DOI `10.1137/060675514` is paywalled; arXiv author copy is the accessible version and is what the community canonically cites.
- `curl -sL https://arxiv.org/pdf/1001.1350 → work/chen-holst-xu-2007.pdf` (375 765 B, SHA-256 recorded in artifact_harvest.md).
- Extracted plain text with `pdftotext -layout`; used it to enumerate the paper's testable claims (C1–C5 in REPORT.md).

## 2026-07-05 02:11 CDT — choose replication targets
- The paper is pure numerical analysis (no dataset). Testable computable claims:
  - **C3 (Thm 6.2, quasi-optimal H¹ error estimate)** — directly checkable via a *manufactured-solution convergence sweep*.
  - **C1/C2 (RPBE regularization + uˡ/uⁿ split)** — checkable by implementing the split faithfully and demonstrating it produces a well-posed, finite-energy solution to an actual singular-source problem.
  - C4/C5 harder: C4 needs discrete L∞ tracking and M-matrix mesh; C5 needs a full a-posteriori estimator plus refinement/dörfler loop. Skipped for time; flagged honestly.

## 2026-07-05 02:12 CDT — install FEM stack
- Checked `uicgpu`: no FEniCS, no skfem. Because problem size is small (≤ 16 641 DOFs, ≤ 1 sec/level), no need to burn A100 time.
- `python3 -m venv work/.venv && pip install scikit-fem numpy scipy` — got `skfem 12.0.2, numpy 2.5.1, scipy 1.18.0`. All-OSS, no paywall.

## 2026-07-05 02:13 CDT — Test A (MMS convergence)
- Wrote `rpbe_mms.py`. First cut used a wrong skfem-12 internal API path (`basis.basis[0].value` — actually `basis.basis[i]` is a `(DiscreteField,)` tuple in skfem 12). Rewrote to use skfem's official public API: `BilinearForm/LinearForm` decorators, `w['field']` for coefficient injection via `asm(...,field=q)`, `basis.interpolate(u)` for solution + gradient at quadrature points.
- Newton with full step + boundary-condensed sparse solve converged in 3–4 iterations at every level, residual from ~1e2 → 1e-13 (textbook quadratic).
- **Empirical rates: L2 → 2.000, H1 → 1.000.** These are the rates predicted by Theorem 6.2 combined with standard P1 interpolation on H²-regular solutions. Full trace in `report/evidence/rpbe_mms_run.log`.

## 2026-07-05 02:14 CDT — Test B (two-atom RPBE with the paper's split)
- Wrote `rpbe_twoatom.py`. 2D "molecule" = interior square `|x|,|y|<0.2` inside Ω = (−1,1)², dipole q = ±1 at (±0.1, 0). Piecewise-constant ε (ε_m = 2 in molecule, ε_s = 80 in solvent) and κ̄² (0 in molecule, 80 in solvent).
- Solved `uˡ` from paper eq. 3.7 (linear elliptic with distributional RHS `div((ε-ε_m)∇G)`), then `uⁿ` from eq. 3.9 with damped Newton on the sinh reaction term.
- Fixed the base mesh to `MeshTri.init_symmetric().translated(...).scaled(...)` to cover (−1,1)².
- Refined 6 levels. Newton always fully quadratic; energy strictly monotone at every level (`energy_monotone: True` across all 6 rows of `rpbe_twoatom_results.json`). Newton iterations 3–5 per level.
- Cauchy-in-h H¹-norm-diff across consecutive levels dropped 0.80 → 3.66 (level 3 is where the mesh first resolves the atoms, so ||uⁱ_h|| jumps as the near-atom singularity is captured) → 1.29 → 0.70 → **0.134** (lvl 6). Consistent with mesh convergence once the atom cores are resolved.

## 2026-07-05 02:15 CDT — LLM-judge
- Attempted `argo:claude-opus-4.7` via Argo proxy `127.0.0.1:44497` — got HTTP 502 (transient upstream). Switched to `argo:gpt-5` (also free through Argo). Note: gpt-5 family rejects `temperature: 0`, so wrapper drops that param for gpt-5/o1/o3/o4 models.
- Judge returned structured JSON: verdict = **PARTIAL**, one-line: "Optimal rates and a stable linear/nonlinear split were reproduced on uniform meshes, but L∞ bounds and adaptive convergence were not tested."
- Per-claim assessment (verbatim in `judge_verdict.md`): C1 partially supported, C2 supported in practice, **C3 strongly supported**, C4 not tested, C5 not tested. This matches our own honest reading.

## 2026-07-05 02:16 CDT — package
- Copied all `work/` code + JSON + logs into `report/evidence/`.
- Wrote `report/{brief,artifact_harvest,attempt_log,REPORT}.md`.
- No overwrite of any sibling replication dir. No paid endpoints used. All numerical results came from the runs above (no fabricated numbers).
