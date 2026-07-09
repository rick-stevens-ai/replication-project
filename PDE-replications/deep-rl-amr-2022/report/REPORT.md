# Replication Report: Deep RL for Adaptive Mesh Refinement (2022)

**Report date:** 2026-06-25
**Working dir:** `/Users/stevens/Dropbox/REPLICATE-PROJECT/PDE-replications/deep-rl-amr-2022`

---

## 1. Paper Identification

- **Title:** *Deep Reinforcement Learning for Adaptive Mesh Refinement*
- **Authors:** Corbin Foucart, Aaron Charous, Pierre F. J. Lermusiaux (MIT MSEAS)
- **Preprint:** arXiv:2209.12351 (Sep 26, 2022)
- **Journal:** Journal of Computational Physics, vol. 491, art. 112381 (Oct 2023)
- **DOI:** 10.1016/j.jcp.2023.112381
- **PDF (open):** https://mseas.mit.edu/publications/PDF/Foucart_et_al_JCP2023.pdf
- **arXiv:** https://arxiv.org/abs/2209.12351

**Brief.** The paper formulates adaptive mesh refinement (AMR) for finite-element PDE discretizations as a *local, partially observable* Markov decision process (POMDP). Each mesh element is treated as an independent agent that decides whether to refine, derefine, or hold, based on local solution features (Laplacian magnitude, jump indicators) and a reward that balances solution-error reduction against degree-of-freedom (DOF) cost. Policy networks are trained with deep RL (PPO / DQN-style architectures discussed in the paper) directly from numerical simulation rollouts. Results are demonstrated on advection and Poisson-class test problems against standard threshold-based AMR (e.g., Dörfler marking, ZZ error estimator).

---

## 2. State of the Replication Directory

**Finding: the directory is an empty scaffold. No replication work has been performed.**

```
deep-rl-amr-2022/
├── analysis/   (empty)
├── data/       (empty)
├── paper/      (empty — no PDF, no README, no metadata)
├── replication/(empty — no code, no notebooks, no env file)
└── report/     (this report only)
```

- Directory created 2026-05-06 16:39 (mtime on all subdirs).
- Zero files anywhere in the tree prior to this report.
- No `paper/*.pdf`, no `replication/{src,env,Makefile,README}`, no `data/*`, no `analysis/*.{ipynb,py,md}`.
- No git history, no `.gitignore`, no notes file.

Conclusion: this slot was scaffolded in early May 2026 and never populated. There is no staged code to audit, no figures to compare against, no captured artifacts (model weights, mesh logs, reward curves) from any local run.

---

## 3. Verdict

### **VERDICT: NO-GO (not attempted)**

- **Coverage:** **0/10** — no paper PDF on disk, no code, no data, no analysis, no replication of any figure, table, or experiment.
- **Agreement:** **0/10** — no numerical comparison is possible because no replication output exists.

This is not a *failed* replication; it is an *un-started* replication. The verdict reflects the as-found state.

---

## 4. 6/22 Reproducibility-Blocker Critique (MANDATORY)

Even setting aside the empty workspace, the upstream paper itself has substantial reproducibility friction. Anyone trying to replicate Foucart et al. (2023) will hit the following **precise missing-artifact wall**:

1. **No public code release identified.** The paper acknowledges the MIT MSEAS group's internal FEM/AMR stack, but a search (arXiv, paper landing page, MSEAS website, GitHub, Papers-with-Code/CatalyzeX) surfaces **no companion GitHub repo, no Zenodo DOI, no supplementary code archive** as of 2026-06-25. The PDE solver and the RL training loop are described in prose + equations only.

   - **Named missing artifact:** the RL-AMR training code (policy network definitions, PPO/DQN hyperparameters, reward shaping, environment wrapper around the FEM solver) and the FEM solver kernel itself.

2. **No trained model weights.** No `policy.pt` / checkpoint is released, so the only path to the reported policies is re-training from scratch — which requires (1) above.

3. **No problem/benchmark dataset.** The advection and Poisson test cases are described mathematically, but exact initial conditions, boundary specifications, mesh seed, refinement-level caps, and random seeds for the stochastic training rollouts are not packaged as a downloadable test suite.

4. **No environment manifest.** No `requirements.txt`, `environment.yml`, `pyproject.toml`, or container image is referenced. Versions of the underlying FEM library (likely an in-house C++/Python stack from MSEAS, possibly tied to MFEM or a custom DG code) are not pinned.

5. **No evaluation script.** The figures (error-vs-DOF Pareto curves, comparison to threshold AMR) cannot be regenerated without an explicit driver that fixes seeds, runs both baseline and RL policies, and emits the comparison plots.

6. **Author contact required.** Practical re-implementation almost certainly requires emailing the authors (cfoucart@mit.edu / pierrel@mit.edu) for the code; that contact step was not attempted in this slot.

**Precise blocker (single line):** *No public source repository or trained policy checkpoints for Foucart et al. arXiv:2209.12351 / JCP 2023 — replication requires either author-supplied code or a full reimplementation of both the FEM solver and the RL training loop from the paper's prose.*

---

## 5. Recommended Next Steps (if this slot is revived)

1. Drop the JCP open-access PDF into `paper/` (link above) and write a 1-page `paper/NOTES.md` extracting equations 3–11 (POMDP definition + reward) and Section 4 hyperparameters.
2. Email Foucart / Lermusiaux requesting the RL-AMR training code and any reference checkpoints; record outcome in `replication/CONTACT.md`.
3. If code is denied or unavailable, demote the goal from REPLICATE to SPOT-CHECK: reimplement a single Poisson test case using `scikit-fem` or `FEniCS` + `stable-baselines3` PPO with the paper's reward; target only the qualitative error-vs-DOF Pareto trend, not exact numerics.
4. Otherwise mark this slot permanently NO-GO and remove the empty scaffold to avoid implying false progress.

---

## 6. Evidence

- Directory listing (2026-06-25): all five subdirs (`paper/`, `replication/`, `analysis/`, `data/`, `report/`) confirmed empty via `find . -type f` returning zero non-report results.
- Paper identification cross-checked against arXiv 2209.12351 abstract, MIT DSpace handle 1721.1/153763, and the MSEAS-hosted JCP 2023 PDF.
- Code-availability search (DuckDuckGo + CatalyzeX, 2026-06-25) returned no GitHub / Zenodo artifact for this paper.

---

**One-line summary:** `deep-rl-amr: NO-GO Coverage=0/10 Agreement=0/10 — empty scaffold, no code or PDF; upstream lacks public repo.`
