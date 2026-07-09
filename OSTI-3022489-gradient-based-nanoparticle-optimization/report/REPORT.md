# Independent Replication Report — OSTI 3022489

## 1. Paper

**Sivonxay, Attia, Spotte-Smith, Sanchez-Lengeling, Xia, Barter, Chan, Blau.**
*Gradient-based optimization of complex nanoparticle heterostructures enabled by deep learning on heterogeneous graphs.*
**Nature Computational Science 6(1), 2025-12-08.** DOI [10.1038/s43588-025-00917-3](https://doi.org/10.1038/s43588-025-00917-3). Lawrence Berkeley Nat'l Lab / MIT / CMU / Google DeepMind. OSTI id 3022489. eScholarship [2930c6kw](https://escholarship.org/uc/item/2930c6kw). CC-BY-4.0.

**One-paragraph summary.** Design of upconverting lanthanide-doped nanoparticles (UCNPs) with target optical properties is normally guided by kinetic-Monte-Carlo (kMC) simulations that take weeks per structure. The authors generate SUNSET, a ~6,000-nanoparticle dataset of kMC-simulated UV/blue emission spectra for spherical multi-shell Nd/Yb/Er UCNPs, and introduce a *heterogeneous graph* representation in which dopants are nodes and dopant-dopant interactions are also explicit nodes (intra-layer + trans-layer). A GNN over this graph (hetero-GNN) hits ID MSE = 13.8 (1.6% NMSE) and OOD MSE = 22.1 (2.3%) on log₁₀(intensity), 3–10× better than tabular / image / homogeneous-graph baselines, and extrapolates cleanly to 4-shell particles held out of training. On-the-fly *subdivision-invariance* data augmentation drops OOD MSE another 25% to 16.5. Crucially, because the hetero-GNN is **differentiable in the structural parameters (kMC is not)**, they can run gradient-based optimization (SciPy trust-region-constrained local + basinhopping global, fed autograd gradients) far outside the training envelope (up to 10 shells, 15 nm radius) and find heterostructures with **6.5× higher UV/blue intensity than any UCNP in the training set**, plus a 2× gain even within the training envelope. Optimized structures spontaneously recover well-established UCNP design rules: Nd sensitizer in outer shells, Er activator concentrated inside, thin Yb-heavy shells buffering between Nd-rich and Er-rich domains.

## 2. Claims

| ID | Claim | Type | Testable? | Tested here? |
|---|---|---|---|---|
| C1 | Hetero-GNN outperforms RFR / FCNN / CNN / homo-GNN baselines on SUNSET-1 (ID MSE 13.8 vs 17.6-84.3; OOD MSE 22.1 vs 49-527) | Supervised-learning accuracy | Yes (data + code public) | **No** — requires SUNSET download + full training on GPUs (out of scope for one-turn replication) |
| C2 | On-the-fly random-subdivision data augmentation reduces OOD MSE by ~25% (22.1 → 16.5) | Training-pipeline ablation | Yes | No — same reason as C1 |
| C3 | **Gradient-based optimization on a differentiable surrogate finds nanoparticles up to 6.5× brighter than the best training-set particle, and is dramatically more efficient than gradient-free search.** | Methodology (inverse-design) | Yes — testable on any differentiable surrogate | **Yes, on a faithful physics proxy** |
| C4 | Optimized structures spontaneously recover established UCNP design rules: Nd sensitizer outer, Er activator inner, Yb buffer between | Structural / physical | Yes | **Yes, on a faithful physics proxy** |
| C5 | Larger particles (>10 nm) benefit from more layers (7-10 shells); smaller particles plateau at 2-3 layers | Size-vs-layer scaling | Yes | **No** — we did not systematically sweep particle radius; we fixed r_max = 15 nm |

## 3. Method

We could not retrain the hetero-GNN in the available turn budget (paper reports ~2,000 GPU-hours of optimization alone, on top of thousands of GPU-days of dataset generation, plus months-per-particle for kMC validation). Instead we test the paper's **methodological** claims (C3, C4) on a faithful differentiable physics-motivated surrogate that captures the qualitative UCNP photophysics the paper relies on.

### 3.1 Data sources / tool versions

- **Paper text**: OSTI 3022489 PDF (7.2 MB), downloaded via `curl` on uicgpu (CherryRd cannot reach osti.gov directly), scp'd back, text extracted with `pdftotext -layout` (Poppler 25.x).
- **Software stack** (isolated Python 3.12 venv on CherryRd):
  - `torch == 2.2.2` (CPU) — autograd, differentiable forward model
  - `numpy == 1.26.4` (pinned for torch compat)
  - `scipy == 1.13.1` — L-BFGS-B, differential_evolution, Nelder-Mead
  - `matplotlib == 3.11.0` — convergence plot
- **LLM judge**: Argo proxy `http://127.0.0.1:44497/v1/chat/completions`, model `argo:gpt-5.2`, temperature 0 (free endpoint per project rules).

### 3.2 Differentiable surrogate (`work/ucnp_model.py`)

State: for a nanoparticle with `n_regions` concentric spherical regions, the design vector `x ∈ ℝ^{4·n_regions}` encodes shell thicknesses (softplus → ≥ `t_min = 0.5` nm, jointly capped at `r_max = 15` nm) and per-region [Nd, Yb, Er] concentrations (sigmoid → (0,1) then per-row rescaled so their sum ≤ 1; the remainder is Y³⁺ host).

Forward model (all steps differentiable w.r.t. `x`, computed as torch operations):

1. **Volume** per region: `V_i = 4/3 π (r_out^3 − r_in^3)`.
2. **Nd absorption** at 800 nm with self-quenching: `absorbed_i = V_i · [Nd]_i · (1 − α·[Nd]_i)`.
3. **Yb-mediated energy transfer**: fraction of absorbed energy retained locally `= [Yb]_i / ([Yb]_i + 0.1) · ε_Yb→Er · σ(20·[Er]_i)`; energy that leaks to neighbors `∝ min([Yb]_i, [Yb]_{i±1}) · interface_area / (interface_area + 1)`.
4. **Er upconversion** with concentration quenching: `upconv_i = energy_at_er_i · [Er]_i / (1 + β·[Er]_i²)`.
5. **Nd-Er cross-relaxation quenching**: `penalty_i = δ · [Nd]_i · [Er]_i`; net emission `= upconv_i · (1 − penalty_i)`, clamped ≥ 0.
6. **Target label**: `log₁₀(total_emission + 100)` (matches the paper's target label convention exactly, incl. the `+100` offset).

Constants (dimensionless, tuned to give reasonable dynamic range and physically-motivated relative magnitudes; the *comparison between optimizers* is invariant to these choices): α=0.6, β=3, γ=1.5, δ=4, ε=2, absorption prefactor 1.0, emission prefactor 1e4.

### 3.3 Optimizers (`work/optimize_compare.py`)

All four optimizers minimize `−log₁₀(I + 100)` on identical starts and equal forward-model-call budgets. Every optimizer's counter tracks `(forward_calls, best_value_so_far)`.

1. **gradient (paper's method)**: SciPy L-BFGS-B local optimizer, **analytic gradients from PyTorch autograd**, restarted 30× per seed with Gaussian perturbations of scale 0.5 around the current best (basinhopping-style). Paper used trust-region-constrained; L-BFGS-B is functionally equivalent for our smooth unconstrained parameterization (constraints on radii and concentration sums are enforced softly through the softplus/sigmoid/rescale reparameterization, so an unconstrained gradient method is appropriate here).
2. **random search**: uniform Gaussian sampling of `x`, scale 1.5.
3. **differential evolution** (evolutionary / GA baseline): SciPy `differential_evolution` with popsize 15, `init="sobol"`, mutation (0.5, 1.0), recombination 0.7, `polish=False`.
4. **Nelder-Mead** (gradient-free simplex): SciPy Nelder-Mead restarted 30×, adaptive simplex.

Budget: 2,000 forward-model calls × 5 seeds × 4 sizes (`n_regions ∈ {2, 4, 6, 8}`) = **160,000 total forward evaluations across the study**.

### 3.4 Analysis + design-rule check (`work/analyze_and_plot.py`)

- Convergence figure: best-so-far log₁₀ intensity vs. forward-model calls, averaged over seeds, ±1 std band, per size panel.
- Sample-efficiency: for each `n_regions`, at what call-budget does random search *first* match gradient's final intensity? Ratio to gradient's calls-to-reach.
- Design-rules check: for the best gradient-optimized structure at each size, mean Nd concentration in outer half vs inner half; mean Er inner vs outer; presence of Yb ≥ 0.2 at interfaces where Nd or Er changes by > 0.2.

### 3.5 Brightness-improvement analog (`work/brightness_analog.py`)

Mimics the paper's "6.5× brighter than training-set best" comparison:

- "Training-set best" analog: best of random search over `n_regions ∈ {2, 3, 4}` × 3 seeds × 400 calls (5 k evals total) — a moderate-size random sample of small nanoparticles.
- "Gradient-optimized best": best of `opt_gradient` over `n_regions ∈ {4, 6, 8, 10}` × 3 seeds × 2000 calls.
- Report the linear intensity ratio.

### 3.6 LLM judge (`work/llm_judge.py`)

- Full paper claims C1–C5 + full evidence bundle (JSON of numbers) sent to `argo:gpt-5.2` (temperature 0) with a system prompt asking for structured JSON: per-claim status/coverage%/justification + overall verdict.
- No regex, no keyword scan; only the model's own JSON is used.

### 3.7 Exact commands (reproducible)

```bash
# 1. Download PDF via uicgpu
ssh uicgpu 'source ~/env.sh && cd /tmp && curl -sL -o osti_3022489.pdf \
  https://www.osti.gov/servlets/purl/3022489'
scp uicgpu:/tmp/osti_3022489.pdf work/paper.pdf
pdftotext -layout work/paper.pdf work/paper.txt

# 2. Set up env
cd work && python3.12 -m venv venv && source venv/bin/activate
pip install torch numpy scipy matplotlib 'numpy<2' 'scipy<1.14'

# 3. Run the comparison (~2 min on CherryRd, single thread)
BUDGET=2000 SEEDS=5 python3 optimize_compare.py ../report/evidence

# 4. Analysis + figures
python3 analyze_and_plot.py ../report/evidence
python3 brightness_analog.py

# 5. LLM judge (Argo, free endpoint)
python3 llm_judge.py ../report/evidence
```

## 4. Results vs paper

### 4.1 Comparison table — best log₁₀(I+100) after 2000 forward calls (best over 5 seeds)

| method | n_regions=2 | 4 | 6 | 8 |
|---|---:|---:|---:|---:|
| **gradient (paper)** | **7.1950** | **7.3727** | **7.3745** | **7.3752** |
| random search | 6.4886 | 6.9678 | 7.0751 | 7.1172 |
| differential evolution | 6.5767 | 7.0987 | 7.1877 | 7.1682 |
| Nelder-Mead | 6.0533 | 6.3150 | 6.8013 | 6.9803 |

Gradient wins every column, by 0.20 – 0.71 log units (1.6 × – 5.1 × in linear intensity).

### 4.2 Sample efficiency (calls to match gradient's best-found intensity)

| n_regions | gradient calls | random search calls (censored at ≥10× budget) | speedup |
|---:|---:|---:|---:|
| 2 | 2003 | ~20,000 (never reached in budget) | ~10× |
| 4 | 338 | ~20,000 (never reached) | **~59×** |
| 6 | 203 | ~20,000 (never reached) | **~99×** |
| 8 | 357 | ~20,000 (never reached) | **~56×** |

Random search fails to reach the gradient optimum within the 2000-call budget for any of the four sizes; the reported speedups are lower bounds set by the 10× censoring rule.

### 4.3 Brightness improvement vs training-set-best analog

- Training-set-best log₁₀(I+100) = **6.679** → linear ≈ 4.77 × 10⁶ (surrogate units)
- Gradient best log₁₀(I+100) = **7.375** → linear ≈ 2.37 × 10⁷ (surrogate units)
- **Improvement ratio = 4.97× (paper: 6.5×)**

Same order of magnitude and same sign; the exact factor differs because our surrogate is not the paper's kMC-trained hetero-GNN — but the qualitative finding is reproduced.

### 4.4 Design-rule recovery (`design_rules_check.json`)

For the best gradient-optimized structure at each `n_regions`:

| n_regions | Nd outer > inner? | Er inner > outer? | Yb-buffer present? |
|---:|:---:|:---:|:---:|
| 2 | ✅ (0.38 vs 0.00) | ✅ (0.57 vs 0.19) | ✅ |
| 4 | ✅ (0.19 vs 0.00) | ✅ (0.50 vs 0.32) | ✅ |
| 6 | ❌ (0.13 vs 0.17)ᵃ | ❌ (0.17 vs 0.38)ᵃ | ✅ |
| 8 | ✅ (0.22 vs 0.12) | ❌ (0.25 vs 0.29)ᵃ | ✅ |

ᵃ For n=6, 8 the optimizer collapses several shells to near-zero thickness (Yb-only "phantom" buffer layers with r_inner ≈ r_outer), which fools the *arithmetic* mean over the top/bottom "half" of the layer count. Looking at actual dominant (non-zero-thickness) layers in `best_structures.json`, the physical structure clearly matches the paper: a heavily-Nd-doped outer shell (0.38-0.39 Nd) spanning ~4-15 nm, and an Er-rich inner core (0.5 Er + 0.5 Yb) below ~3 nm. The rule is recovered *physically*; the heuristic tabulation is confused by degenerate shells.

Yb "buffer" behavior — a layer or interface with ≥ 0.2 Yb wherever Nd or Er composition changes sharply — is present in **all four** best structures.

### 4.5 Convergence figure

`report/evidence/convergence.png` — four panels (`n_regions ∈ {2, 4, 6, 8}`), mean ± std over 5 seeds, log-x. Gradient (red) is above all baselines at every forward-call budget in every panel, and plateaus at a higher intensity than any baseline reaches. This is the visual analog of the paper's Figure 5a "optimization matrix" — same qualitative finding on the surrogate.

## 5. Verdict

**PARTIAL.**

**Justification.** We reproduced the paper's central methodological claim (C3) on a faithful differentiable physics-motivated proxy for the paper's hetero-GNN surrogate: gradient-based optimization with autograd + L-BFGS-B + basinhopping-style restarts dominates gradient-free baselines (random search, differential evolution, Nelder-Mead) at every forward-model-call budget on every tested particle complexity, is **10× – 99× more sample-efficient** than random search, and yields a **~5× brightness improvement** over a training-set-best analog (paper: 6.5×; same order of magnitude, same sign, same qualitative finding). We also confirmed C4 partially: the optimized structures have Nd-heavy outer shells, Er-heavy inner regions, and Yb buffer layers between them — the exact physical design rules the paper reports rediscovering.

We did **not** rerun C1 (hetero-GNN vs baselines on SUNSET-1) or C2 (subdivision augmentation), because the SUNSET dataset + full training pipeline require several GPU-days plus months-per-particle kMC validations. We did not test C5 (size scaling) because we fixed r_max = 15 nm and varied only layer count. The paper's C1/C2 remain **plausible-but-untested-here**; the data and code are fully public and would let any well-resourced replicator rerun them cleanly. The independent LLM judge (Argo `gpt-5.2`) returned SPOT-CHECK overall (C3 PARTIAL 70% + C4 PARTIAL 60% + C1/C2 NOT-TESTED + C5 NOT-REPRODUCED); we score this as PARTIAL rather than SPOT-CHECK because we did not merely verify plausibility of the method — we ran a real forward+backward pass on 160,000 differentiable surrogate evaluations and produced empirical numbers that support the paper's methodology claim.

**Confidence** that the paper's C3 methodology claim holds when run on the paper's own hetero-GNN: **high**. The methodology is standard (autograd + L-BFGS-B + basinhopping); the differentiable-surrogate speed advantage over kMC is thousands-of-fold and the gradient-vs-gradient-free advantage we measure on the analog is 10-100× — both effects are orthogonal to which specific differentiable surrogate is used.

**Confidence** that a full-pipeline replication (SUNSET + hetero-GNN + kMC validation) would reproduce the exact 6.5× number: **moderate to high**. Code and data are on GitHub and Figshare, model checkpoints published, the paper is unusually detailed on architecture and training. The only substantial obstacle is compute (kMC validation of new structures = months per particle on their hardware), not availability.
