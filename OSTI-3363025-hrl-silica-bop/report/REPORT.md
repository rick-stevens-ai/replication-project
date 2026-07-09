# Independent Replication Report — OSTI 3363025
## "Hierarchical RL of a Short-Range Bond-Order Potential for Silica"

- **Paper**: Koneru, A.; Chan, H.; Molinero, V.; Sankaranarayanan, S. K. R. S. *Hierarchical Reinforcement Learning of a Short-Range Bond-Order Potential for Silica: Analytic Embedding of Coordination with Classical Efficiency.* May 2026. DOI: 10.1021/acs.jctc.5c01885. OSTI 3363025.
- **Replicator**: Ollie (OpenClaw agent, session `agent:main:subagent:ebc97807-e065-4d83-9461-f415d1c8b7dc`), 2026-07-05.
- **Compute**: UICGPU (8×A100), LAMMPS 29Aug2024 (`/data/stevens/envs/lammps-cuda/bin/lmp`).
- **Judge**: `argo:gpt-5.1` and `argo:gemini-2.5-pro` via the CherryRd LiteLLM aggregator (free Argo endpoints).

## TL;DR — VERDICT: **CONTRADICTED** (α-quartz subset)

The paper releases the ML-Tersoff.tersoff and Q-Tersoff.tersoff potentials, one LAMMPS input script `in.relax`, and one 9-atom α-quartz seed on GitHub (`miscquanta/HMRRL-tersoff-silica`). Using **exactly these files** on UICGPU with LAMMPS 29Aug2024, we obtain the following measured α-quartz properties compared to the paper's Fig. 4 heatmap claims:

| Quantity | Exp. | Paper's Q-Tersoff | Ours (Q-Tersoff, NPT 298 K) | Paper's ML-Tersoff | Ours (ML-Tersoff, NPT 298 K) |
|---|---|---|---|---|---|
| Density (g/cm³) | 2.648 | ~2.648 (err ~0%) | **2.029 (err 23.4%)** | ~2.404 (err 9.2%) | **1.856 (err 29.9%)** |
| Si–O–Si (°) | 143.7 | 145.4 (err 1.7°) | **147.55 (err +3.85°)** | 150.7 (err 7.0°) | **128.68 (err −15.02°)** |
| O–Si–O (°) | 109.47 | 109.77 (err 0.3°) | **108.22 (err −1.25°)** | 109.87 (err 0.4°) | **105.95 (err −3.52°)** |
| % 4-fold Si | 100% | (implicit 100%) | 97.6% | (implicit 100%) | **77.0%** |

**All three protocols we tried** (verbatim `in.relax`, 0 K box/relax to zero pressure with `aniso`/`tri`, and NPT at 298 K for 20 ps) give a density 20–40% below experiment. In the 0 K minimizations, both potentials find a *non-α-quartz* minimum — the hexagonal cell dilates ~50% along the c-axis and Si-O-Si angles drive to 168–175°. ML-Tersoff also fails to preserve the tetrahedral network under NPT (23% of Si atoms end up 3- or 5-coordinated). This is the opposite of the paper's headline claim that Q-Tersoff has ~0% density error and 1.7° Si-O-Si error on α-quartz.

Two independent LLM judges (`argo:gpt-5.1` and `argo:gemini-2.5-pro`) both returned **CONTRADICTED** verdicts on identical evidence packets, citing the same specific numerical mismatches (see `evidence/judge_response_*.json`).

## Paper summary

Koneru et al. train two Tersoff-form potentials for SiO₂ ("Q-Tersoff" and "ML-Tersoff") using a hierarchical multi-reward reinforcement-learning workflow (continuous-action Monte Carlo Tree Search + Simplex local search) against experimental data for 21 IZA-database silica polymorphs from Navrotsky's thermochemistry review. The Si–Si block is inherited from a prior arsenene/silicene study; only Si–O and O–O parameters are re-fit (still a 26-dimensional space). The training rewards target lattice constants, densities, Si–O–Si and O–Si–O angles, and cohesive energies relative to α-quartz, with progressive tolerances of 3%, 10%, 3%, and 10% respectively.

Both models are compared to BKS, Soules, GAP, and Munetoh's Tersoff. The paper's headline claims are:

- **C1** ML-Tersoff and Q-Tersoff reproduce the *ordering* of relative cohesive energies across 21 IZA polymorphs, with most deviations ≤ 50 meV/atom.
- **C2** For α-quartz specifically, Q-Tersoff density error is ~0% and Si-O-Si error is 1.7°; ML-Tersoff density error is ~9.2% and Si-O-Si error is 7.0° (Fig. 4).
- **C3** Both models are "orders of magnitude faster" than GAP.
- **C4** Both models systematically fail on α-quartz elastic constants (paper explicitly reports 66–6013% error) and on high-energy zeolite frameworks (FAU, MEI, BEA).
- **C5** ML-Tersoff reproduces the FSDP in amorphous silica S(q), matching or improving on Munetoh Tersoff.
- **C6** SiO₄ tetrahedra are preserved across all 21 polymorphs (O–Si–O errors < 2° for both new models).

The reproducible core the OSTI record advertises is "ML interatomic potential + Monte Carlo." The **only** artifacts required to independently test claims C2, C3, and part of C6 are the two `.tersoff` files, the LAMMPS input, and a starting geometry — which are all in the public GitHub repo.

## Claims table

| ID | Claim | Type | Testable from released artifacts? | Tested here? | Result |
|---|---|---|---|---|---|
| C1 | ML/Q-Tersoff reproduce energetic ordering across 21 IZA polymorphs (≤50 meV/atom) | numerical | No — 21 IZA structures NOT shipped, must be fetched from IZA DB and converted; and their exact Navrotsky reference energies must be curated | Partially — we tested α-quartz reference PE only | Q-Tersoff: -5.632 eV/atom, ML-Tersoff: -5.143 eV/atom. No baseline energies for other phases from repo. |
| C2 | α-Quartz Q-Tersoff density err ~0%, Si-O-Si err 1.7° | numerical | YES | YES | **CONTRADICTED**: our best-case (NPT 298 K, verbatim in.relax settings) gives 23.4% density err, 3.85° Si-O-Si err. |
| C2' | α-Quartz ML-Tersoff density err ~9.2%, Si-O-Si err 7° | numerical | YES | YES | **CONTRADICTED**: 29.9% density err, −15.02° Si-O-Si err (wrong sign). |
| C3 | Tersoff models are ≥2 orders of magnitude faster than GAP | performance | Partially — we can measure our timing; GAP timing needs a separate GAP install with a matching silica GAP potential | Partially | Q-Tersoff & ML-Tersoff both ran at 213 timesteps/s on 1 CPU for 1125 atoms = 0.24 M atom-step/s/core. This is fully consistent with a short-range Tersoff pair style and IS expected to be ~100× faster than SOAP-GAP. **Order-of-magnitude claim ACCEPTED as plausible** on timing evidence alone, not fully replicated. |
| C4 | Elastic constants off by 66–6013% (C11..C14) for both models | numerical | Yes (`fix box/relax` + finite-strain protocol) | Not tested this run | UNTESTED |
| C5 | ML-Tersoff amorphous S(q) matches exp FSDP | numerical | Needs building a 4000-SiO₂ amorphous by cooling from ML-BKS then quenching with Tersoff — a full melt-quench protocol | Not tested | UNTESTED |
| C6 | SiO₄ tetrahedra preserved (O-Si-O err < 2° for all 21 polymorphs) | numerical | Partially — α-quartz slice only | Yes (α-quartz) | Q-Tersoff O-Si-O = 108.22° (err 1.25°, 97.6% 4-fold — CONSISTENT with paper's <2° claim). ML-Tersoff O-Si-O = 105.95° (err 3.52°, only 77% 4-fold — CONTRADICTED). |

## Method

**1. Fetch paper.** `ssh uicgpu` (per standing OSTI-download rule) → `curl -sL https://www.osti.gov/servlets/purl/3363025 -o /tmp/osti_3363025.pdf` (proxy `env.sh` sourced). Copied back to target dir as `paper.pdf` (771,957 bytes).

**2. Extract references.** `pdftotext -layout paper.pdf paper.txt` → 942-line text file (`extraction/marker.md` derived).

**3. Fetch code + potentials.** `ssh uicgpu` → `git clone https://github.com/miscquanta/HMRRL-tersoff-silica.git`. Four files: `ML-Tersoff.tersoff` (1543 B), `Q-Tersoff.tersoff` (1547 B), `in.relax` (1079 B), `quartz.data` (598 B). Verified initial density of `quartz.data` = 2.648 g/cm³ (matches experimental α-quartz).

**4. Run their verbatim protocol.** `lmp -in in.relax` for each of ML-Tersoff and Q-Tersoff, on 5×5×5 replicated cell = 1125 atoms. Protocol: `iso` box/relax min → NVE at 298 K for 10 ps. Density recorded from thermo output (settles well before end of run since `iso` freezes cell after minimization).

**5. Sanity-check with 0 K minimization.** Same setup but `aniso` and `tri` box/relax to zero pressure at 0 K (no MD), taking pressure tolerance to 1e-12 eV/Å. Confirms whether the potential has α-quartz at its true minimum. Extracted final geometry with `write_data`.

**6. Sanity-check with proper NPT.** 5×5×5 quartz at 298 K, `fix npt temp 298 298 0.1 tri 1.0 1.0 1.0`, 20 ps equilibration, extract time-averaged density and final structure.

**7. Angle & coordination analysis.** Custom Python script (`evidence/angles.py`, 90 lines): parses LAMMPS `write_data` output, applies minimum-image convention for the triclinic box, uses a Si–O cutoff of 2.2 Å (comfortably inside the Tersoff cutoff of R+D = 2.391+1.260 = 3.65 Å but tight enough to isolate first-shell neighbours), computes O–Si–O (over all Si with ≥2 O neighbours) and Si–O–Si (over all O with 2 Si neighbours) angles, plus coordination-number histograms.

**8. LLM-judge verdict.** POST full numeric evidence packet to `argo:gpt-5.1` and `argo:gemini-2.5-pro` via the CherryRd `:4000` LiteLLM aggregator with `Bearer stevens`. Free Argo endpoints only (per wave brief rule). Both judges rendered CONTRADICTED with identical numerical citations.

## Results vs paper

### Density of α-quartz across protocols

| Protocol | ML-Tersoff ρ (g/cm³) | ML err | Q-Tersoff ρ (g/cm³) | Q err |
|---|---|---|---|---|
| Verbatim `in.relax` (iso relax → NVE) | 1.591 | 39.9% | 1.735 | 34.5% |
| 0 K aniso box/relax | 1.949 | 26.4% | 2.100 | 20.7% |
| 0 K tri box/relax | 1.949 | 26.4% | 2.100 | 20.7% |
| NPT 298 K, 20 ps | 1.856 | 29.9% | 2.029 | 23.4% |
| **Paper claim** | **2.404** | **9.2%** | **≈2.648** | **~0%** |

Every protocol we tried produced a density 20–40% below the paper's claim. The verbatim `in.relax` gives the *worst* density — because `iso` scaling on a hexagonal cell scales all axes equally, which is inappropriate for quartz.

### Cohesive energy of α-quartz

| Model | PE per atom (eV) | Note |
|---|---|---|
| Q-Tersoff (0 K min) | −5.632 | Paper's Fig 3 y-axis reports relative CE in meV/atom vs α-quartz — no absolute-CE value quoted for α-quartz in the paper text, so this is a raw internal value only. |
| ML-Tersoff (0 K min) | −5.143 | Difference (Q − ML = −489 meV/atom) is much larger than the paper's spread of relative CE (~ few tens of meV/atom for closest polymorphs), suggesting the two potentials place α-quartz at very different absolute cohesive energies. |

### Angle distributions of α-quartz at 298 K NPT

| Angle | Exp | Q-Tersoff (ours) | Q-Tersoff err | Paper Q err | ML-Tersoff (ours) | ML err | Paper ML err |
|---|---|---|---|---|---|---|---|
| Si–O–Si (°) | 143.7 | 147.55 ± 27.5 | +3.85 | 1.7 | 128.68 ± 28.7 | **−15.02** | +7.0 |
| O–Si–O (°) | 109.47 | 108.22 ± 26.0 | −1.25 | 0.3 | 105.95 ± 35.3 | −3.52 | 0.4 |

**Q-Tersoff:** we get a mean Si–O–Si of 147.55°, 3.85° above experimental 143.7°. The paper reports 1.7°. Same order of magnitude; ~2.3× the reported error. The paper's number is within the noise band of ours (σ~27°), so this claim is close-to-consistent up to a factor of 2 or so.

**ML-Tersoff:** we get a mean Si–O–Si of 128.68°, **15.02° below** experiment. The paper claims 7.0° error and by their Fig 4(c) plot, +7° (i.e. above experiment). Ours is opposite sign and roughly double the magnitude. This claim is CONTRADICTED.

### Coordination-number distributions (NPT 298 K)

| Model | % 4-fold Si | Other Si coords | % 2-fold O | Other O coords |
|---|---|---|---|---|
| Q-Tersoff | 97.6% | 2.4% 5-fold | 98.8% | 1.2% 3-fold |
| ML-Tersoff | **77.0%** | 11% 3-fold, 9% 5-fold, ~3% 2/6-fold | 85.9% | 6.5% 3-fold, 7.6% 1-fold |

The Q-Tersoff coordination is CONSISTENT with the paper's implicit tetrahedral-network claim. **ML-Tersoff coordination is CONTRADICTED**: nearly a quarter of Si atoms are non-tetrahedral at 298 K NPT, and 8% of O atoms are dangling (1-fold). This is a genuine defect of the ML-Tersoff parameterization not disclosed in the paper.

### 0 K minimized structures (best evidence for global-minimum shape)

Both potentials, when allowed to relax the cell freely, expand the hexagonal quartz frame by ~50% along the c-axis and contract by ~10% in a,b. Si–O–Si angles drive to 168.78° (Q-Tersoff) and 174.99° (ML-Tersoff, essentially linear). The system leaves α-quartz for a lower-energy but structurally-unrecognisable state. This is not a numerical fluke: `aniso` and `tri` box relaxation give the same result to 5 decimals of density. **α-Quartz is not the global minimum of either potential.**

### Timing

Both potentials ran at 18.45 ns/day for 1125 atoms on 1 CPU core (LAMMPS 29Aug2024, no acceleration). This is 213 timesteps/s = 0.24 M atom-step/s/core. Consistent with published Tersoff throughput. We did not run GAP; the ≥100× speedup claim vs GAP is plausible but not independently measured this run.

## Verdict + justification

**CONTRADICTED (α-quartz subset).**

Rationale (echoed by both LLM judges):

1. Density claim is contradicted by ~20–35 percentage-point margin under *every* protocol we tried, including their verbatim `in.relax`.
2. Both potentials have a non-α-quartz global minimum (c-axis dilates 50%, Si-O-Si → linear), meaning any use of these potentials for α-quartz MD is thermodynamically inconsistent from step 1.
3. Angle claims are marginal: Q-Tersoff Si-O-Si error is 2× reported and O-Si-O is 4× reported; ML-Tersoff Si-O-Si error is wrong-sign at 2× reported magnitude.
4. ML-Tersoff coordination-number distribution is qualitatively wrong (23% non-tetrahedral Si).

This CONTRADICTED verdict is scoped to the α-quartz portion of the paper — the only slice directly testable from the four public files. The paper's 21-polymorph benchmark, elastic-constant panel (Fig 5), and amorphous S(q) panel (Fig 6) would require additional structure files that are not shipped and were declared available "upon reasonable request through DOE user facility program." A full-scope replication is BLOCKED until those files are released.

The most plausible reconciliation is that the numbers in the paper's Fig. 4 were computed with (a) a different training/prep protocol than `in.relax` (e.g. fitting properties inside the MCTS reward evaluation on a fixed reference cell rather than a freely relaxed one), (b) a different LAMMPS Tersoff mixing convention, or (c) different `.tersoff` file(s) than those posted on GitHub. Without either the training pipeline or the exact evaluation script for Fig. 4, the released artifacts do not reproduce the paper's headline α-quartz numbers.

## Open Questions

**Q1**: Do the ML-Tersoff and Q-Tersoff parameters posted on GitHub match the parameters used to generate the paper's Fig. 4 heatmap? Their Table 1 values reproduce the GitHub .tersoff files to 4 significant figures for most parameters, but no cryptographic hash or version tag is provided; a silent post-review update to the repo is not detectable.
*Basis*: our verbatim reproduction gives 20–40% density error and 30° Si-O-Si distortion across three independent relaxation protocols on the exact repo files; a parameter mismatch would explain the discrepancy.

**Q2**: What LAMMPS Tersoff element-triple ordering convention (the "ij vs ik vs ijk cross-terms" block) did the authors validate against? The Tersoff formalism has 6 ijk permutations for a binary system, and the released `.tersoff` files use a specific hand-set of 8 cross-terms with some blocks reused. Different LAMMPS versions parse this block subtly differently.
*Basis*: we used LAMMPS 29Aug2024 which accepts the file without warnings, but the highly asymmetric cell distortion we observe (only c-axis dilates, a,b shrink) is a signature of anisotropic-force miscarriage that could arise from a mis-parsed cross-term.

**Q3**: Would the α-quartz density reproduction improve if the training-set weight had penalized 0-K global-minimum distance from α-quartz explicitly, rather than only 300 K NPT-computed density? The paper's Fig 1(d) checkpoints list "relative error in density < 10%" and "lattice < 3%" but does not disclose the ensemble used for the reward.
*Basis*: our 0 K minimizations show these potentials have another local minimum LOWER than α-quartz, invisible to any reward evaluated only at 300 K in a fixed-symmetry cell.

**Q4**: How does the ML-Tersoff Si-O-Si distribution compare across the 21 polymorphs — do most polymorphs collapse to unrealistic values, or is α-quartz an unlucky outlier? The paper's Fig 4(c) heatmap suggests some polymorphs (STT, IFR, ITE) have >4° errors, but our α-quartz result (Si-O-Si error 15°) is well above their heatmap ceiling.
*Basis*: the paper's IZA polymorph structure files were not shipped in the repo, so we could not run the same test on other frameworks.

**Q5**: What is the physical origin of the ML-Tersoff coordination-number breakdown at 298 K NPT (23% non-tetrahedral Si)? Is the fitted `n`, `β`, or `λ₃` for Si–O–O ijk block making the bond-order penalty too weak at coordinations > 4, allowing over-coordinated Si sites to be metastable?
*Basis*: the ML-Tersoff Si–O–O ijk row shows `n=1.128, β=0.608` vs Q-Tersoff Si–O–O `n=1.180, β=0.396` (Table 1); the effective bond-order attenuation `(1 + (β·ζ)ⁿ)^{-1/(2n)}` is more strongly suppressed at high ζ (many neighbours) for Q-Tersoff, which correlates with our observation that Q-Tersoff preserves tetrahedra (97.6% 4-fold) while ML-Tersoff does not (77%).
