# Replication Friction Taxonomy
*Started 2026-05-27 — Ollie & Rick*
*Canonical list of distinct failure/friction modes encountered across the replication corpus*

## Purpose
A controlled vocabulary for tagging *why* a replication is partial, blocked, or harder than the paper suggests. Each tag captures one **structurally distinct** mode of friction so the meta-paper can quantify which kinds of obstacles dominate, and so future replicators can recognise patterns before sinking days into them.

Tags are additive: a single paper can be tagged with multiple Fn codes.

---

## F1 — Missing or unreleased code
The paper claims an algorithmic contribution but no implementation is published; no GitHub link, no supplementary code, no response from authors. Replicator must re-derive from text + equations alone.
- *Severity:* high (often kills exact replication)
- *Detect early:* check "Code Availability" statement before scheduling.
- *Example slots:* (none yet — most papers we've picked have *some* code).

## F2 — Code released but unbuildable
Code exists but cannot be built or run today. Dead URLs for dependencies, abandoned Python/CUDA/OS versions, missing build scripts, undocumented compiler flags.
- *Severity:* medium-high (slows; usually solvable with effort).
- *Detect early:* attempt fresh-env build before committing compute.
- *Examples:* IGM (Q1) `netCDF4==1.6.0` pin forced HDF5-from-source; `pyvista` imported but absent from `setup.py`.

## F3 — Hardcoded paths / institutional infrastructure
Code assumes specific cluster filesystems (`/glade/scratch/`, `/lustre/...`), institutional MATLAB licenses, or login-node-only Globus mounts.
- *Severity:* high when paired with F5 (data unrecoverable).
- *Detect early:* grep for absolute paths in the data-pipeline scripts.
- *Examples:* Yuval-O'Gorman (Q5) MATLAB train/test builder requires Cheyenne `/glade/scratch/` paths.

## F4 — Hyperparameter / training-recipe gaps
Architecture and loss are documented but optimisation details (learning-rate schedule, batching, augmentation, exact init) are partially specified. Reproduced numbers track qualitatively but miss quantitatively.
- *Severity:* medium (causes the typical "we got 0.7 they got 0.8" gap).
- *Detect early:* read appendix for explicit hyperparameter table; check if a config file is shipped alongside the code.
- *Examples:* Stage-1 PVMol-Gen classifier F1=0.66 vs paper 0.80; modal-space Zhang 2019 errors 20–35× higher.

## F5 — Data unreleased or unrecoverable
The training/test data referenced in the paper is not publicly downloadable today. Promised uploads never landed, mirrors went dark, or the dataset was always under restricted access.
- *Severity:* very high (blocks exact replication, forces methodology-only validation).
- *Detect early:* try a download of every linked dataset before spawning a replication subagent; treat dead links as a hard block.
- *Examples:* Yuval-O'Gorman OSF folder empty since 2020 ("uploading due to COVID-19"); Google Drive needs author permission. Pinned PINN-RANS Eivazi 2022 DNS/LES reference datasets unavailable from KTH.

## F6 — Custom optimizer / non-standard solver
The paper relies on a hand-built optimiser, custom L-BFGS variant, or in-house solver not shipped with the code. The architecture replicates but the training trajectory does not.
- *Severity:* medium-high (errors typically 10–100× larger absolute, qualitative trends preserved).
- *Detect early:* check whether the training loop uses stock library calls or invokes private functions.
- *Examples:* PINN-domain-decomp Kopaničáková 2023 MSPQN custom L-BFGS not released; we got 5–44× lower loss vs L-BFGS (right ordering) but absolute errors 100× off.

## F7 — Gauge / non-uniqueness in solution
The decomposition or representation the paper learns has gauge freedom (e.g., modal-decomposition sign ambiguity, latent-rotation invariance, eigenvalue permutation). Two correct solutions can disagree numerically while both being right.
- *Severity:* low-medium for science, high for paper-table-matching.
- *Detect early:* look for symmetry groups in the loss landscape; check if the paper reports a canonical-form post-processing step.
- *Examples:* Modal-space Zhang 2019 gauge freedom in modal decomposition; eigenvalue crossings reproduced qualitatively, absolute numbers diverge.

## F8 — Original-results inflation
Reproduced numbers are systematically worse than the paper reports, suggesting either (a) cherry-picked seeds/runs, (b) test-set leakage, or (c) framework-specific reporting differences (e.g., a particular TF/Keras version's metric definition). Distinct from F4 because the gap survives careful hyperparameter sweeps.
- *Severity:* medium (paper is "right" in spirit but headline numbers don't generalise).
- *Detect early:* if you fully match the recipe and still miss by >2× on multiple seeds, suspect F8.
- *Examples:* PVMol-Gen Stage-1 classifier remained 0.65 ± 0.04 across all sweeps in PyTorch vs paper 0.80 in TF/Keras — pointing at framework + training-stochasticity inflation.

## F9 — Upstream data-layout drift  *(new 2026-05-27)*
Code, data, and paper were all coherent at publication but a *transitively-depended-on public dataset* has since been moved, restructured, or de-versioned. The paper's pipeline references stable URLs that are no longer stable. Different from F5 (paper data unreleased) because here the paper's *own* data is fine — it's a third-party data dependency that drifted.
- *Severity:* medium-high; usually solvable in hours with detective work, but invisibly fatal to anyone running the "default workflow" from the README.
- *Detect early:* attempt the published quick-start tutorial in a fresh environment; if it fails on a data-fetch step (not an install step), F9 is the most likely cause.
- *Examples:* IGM (Q1 Jouvet 2023) shipped default config points at OGGM `igm_v2/` preprocessing URL which has since been removed; default RGI ID `RGI60-11.01450` refers to RGI v6 which OGGM has deprecated in favor of v7 with renamed IDs. Subagent resolved by downloading global RGI v7 attribute CSV and matching by glacier name.
- *Why this needed its own tag:*
  - F2 (unbuildable) is about *your* environment vs the code.
  - F5 (data unreleased) is about *the paper's* data.
  - F9 is about a *third party's* data, which the paper and code both correctly cited, that has since drifted underneath them. Different actor, different mitigation strategy (you don't email the paper authors, you go upstream).
- *Mitigation pattern:*
  1. Identify the drifted dataset (usually a public preprocessing service: OGGM, OpenML, HuggingFace mirror, etc.).
  2. Find the upstream replacement (often a renamed URL or a version-bumped ID scheme).
  3. Patch the config locally; document the patch in PROGRESS.md so the next replicator doesn't repeat.

---

## Aggregate friction tags by replication (live table)

| Paper / slot | Tags | Verdict |
|---|---|---|
| Q1 Jouvet IGM (Slot B) | F2, F9 | PARTIAL (emulator gap + upstream drift) |
| Q6 SOWFA-WindFarm Duthé 2023 (Slot G-RETRY) | F2, F9 | OK — 7 frictions, all resolved in ~25 min: 3× py_wake API drift (`TensorflowSurrogate`→`TensorFlowModel`, dropped `yaw=` kwarg, `weights_only=True` PyTorch 2.6 default unpickling PyG Data) + 1× silent PyG transform-discarded bug (`p(g)` instead of `g=p(g)`) + 1× predict.py signature drift — all F2 inside an actively-maintained (2025-07-07) repo; **F9 variant**: py_wake PyPI wheel ships *without* the 44 IEA34_130 surrogate .h5 files that the same project's DTU GitLab source includes, so `pip install py_wake==2.6.11` runs but the load surrogate is broken — resolved by git-cloning the upstream source and copying h5 directories into venv site-packages |
| Q5b Rasp 2018 (Slot F-RETRY) | F2, F5 | PARTIAL (Zenodo deposit is 0.5% of paper corpus; methodology + architecture sweep + vertical-R² structure all replicated; absolute R²≈3× below paper headline) |
| Q5 Yuval-O'Gorman (Slot C) | F3, F5 | PARTIAL (data unrecoverable) |
| Pinn-RANS Eivazi 2022 | F5 | PARTIAL |
| Pinn-DD Kopaničáková 2023 | F6 | PARTIAL |
| Modal-space Zhang 2019 | F4, F7 | PARTIAL |
| PVMol-Gen Fajar 2026 | F4, F8 | PARTIAL (SELFIES pivot) |

*(This table is curated by hand; add rows as new tags are assigned. Subagents should propose tags in their REPORT.md and Ollie ratifies into this file.)*

---

## Adding a new tag
1. **Confirm it's structurally distinct** from existing F1–Fn. If a new failure mode is "F4 but worse" or "F5 with a twist," don't add it — extend the existing tag's description with the new variant.
2. **Pick the lowest unused Fn** (no gaps, no reservations).
3. **Write the four standard fields**: short name, severity, detect-early, examples. Include a "why this needed its own tag" subsection when ambiguity vs existing tags is plausible.
4. **Backfill the aggregate table** for any past replications that should have carried the tag in hindsight.
5. **Note the date and source replication** in the section header.
