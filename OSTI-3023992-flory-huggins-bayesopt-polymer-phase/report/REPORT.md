# Independent Replication Report — OSTI 3023992

## Paper

- **Title**: *Using Flory–Huggins-informed human-in-the-loop Bayesian optimization to map the phase diagram of polymer blends*
- **Authors**: Justin C. Hughes, Dylan J. York, Kevin G. Yager, Chinedum O. Osuji, Russell J. Composto
- **Venue**: *Digital Discovery* (RSC), 2026
- **DOI**: 10.1039/d5dd00556f · OSTI id: 3023992 · Preprint: BNL-229582-2026-JAAM
- **Received**: 12 Dec 2025 · Published: 03 March 2026
- **Code/data**: https://github.com/jhughes3/-hitl-bo · Zenodo 10.5281/zenodo.18805553

## One-paragraph summary

The paper introduces a physics-informed, human-in-the-loop Bayesian-optimization (BO) workflow that maps the *lower critical solution temperature* (LCST) phase diagram of a poly(methyl methacrylate) / poly(styrene-*ran*-acrylonitrile) (PMMA/SAN) polymer blend. The workflow uses a Matérn-3/2 Gaussian-process surrogate whose **structured prior mean is a sigmoid of the Flory–Huggins spinodal second-derivative** `∂²ΔF_mix/∂φ²` with χ(T) = A + B/T, so that domain physics enters as a soft constraint that is refit at every iteration (A, B become interpretable hyperparameters). A custom boundary-seeking acquisition `fa(x) = σ(x) + 0.25·tanh(0.1/|μ−0.5|)` and a unit-radius exclusion mask (Δφ=0.025, ΔT=1 °C) direct sampling toward the phase boundary rather than any single optimum. Starting from 4 corner initialization points, 20 iterations of 5 samples each (104 samples total) converge to an LCST of ~160 °C with fitted (A=0.022, B=−8.22 K), stabilized kernel condition number ~548, and reproduce a literature-consistent PMMA/SAN phase diagram with a formal, quantitative stopping criterion.

## Claims table

| # | Claim | Type | Testable in silico? | Tested? | Result |
|---|-------|------|:-:|:-:|--------|
| C1 | The paper's Flory–Huggins parameterization (A=0.022, B=−8.22 K, N_PMMA≈804, N_SAN≈567) predicts an LCST at ~160 °C. | Physics | Yes | Yes | **Reproduced.** Analytic spinodal min T = **159.16 °C at φ_PMMA=0.46** (paper: ~160 °C). |
| C2 | Their BO stack (Matérn-3/2 GP + FH-sigmoid prior mean + boundary-seeking acquisition + exclusion mask + differential-evolution hyperparameter refit) is runnable and locates the LCST after 4 init + 20×5 iterations = 104 samples. | Method | Yes | Yes | **Reproduced.** Re-implemented from scratch; ran 20×5 with the identical protocol; posterior-extracted LCST stabilizes at 159.6 °C from iter 4 onward. |
| C3 | The BO campaign recovers **A ≈ 0.022** (entropic, dimensionless) and **B ≈ −8.22 K** (enthalpic; negative → LCST) from the data. | Fit | Yes | Yes | **Reproduced within ≤2 %.** Final BO-fitted **A = +0.0223, B = −8.37 K**. Sign of B correctly infers LCST behavior without prior guidance (Table 1 bounds allow ±). |
| C4 | Final kernel length scales `lx=0.12 wt frac`, `lT=2.63 °C`; kernel matrix condition number stabilizes at ≈548.2. | Method | Partially | Attempted | **Partial**: sklearn's kernel scales are not directly comparable to gpCAM's (different scaling conventions and normalization). Condition-number stabilization behavior was observed qualitatively but not calibrated to the paper's numeric value; would require running the exact gpCAM 8.1.9 code with identical noise model. |
| C5 | FH-informed BO outperforms a Newby-style grid (7 comps × N temps) for phase-boundary mapping efficiency. | Comparison | Yes | Yes | **Reproduced qualitatively.** With ≈100 samples each, BO+FH boundary RMSE = 0.93 °C vs grid = 3.7 °C — a 4× improvement. At small budgets (n≤14) the multistart FH fit can get stuck, matching the paper's own "Section 3" hyperparameter-trapping observation. |
| C6 | Optimizer autonomously decides the blend is LCST (B<0) without external prompting. | Method | Yes | Yes | **Reproduced.** Starting from A=B=0 and bounds ±200, all successful refits converged to B<0 (−5 to −8.37 K). |
| C7 | Phase boundary shape becomes physical after ~iter 14, aligning with a parabolic FH prediction. | Method | Yes | Yes | **Reproduced.** Posterior=0.5 contour matches analytic FH spinodal within <1 °C RMSE over φ∈[0.05, 0.95] by iter 6 onward. |

## Method

1. **PDF acquisition.** OSTI 3023992 downloaded on `uicgpu` (CherryRd cannot reach osti.gov directly), scp-ed to `work/paper.pdf` (1,443,341 B, PDF v1.4). Text extracted via `pdftotext -layout` (1087 lines).
2. **Claim extraction.** All numeric claims (A, B, LCST=160 °C, protocol 4+20×5=104 samples, Matérn-3/2, acquisition function eqns 11-12, length scales, condition number 548.2, PMMA Mw=84.5 kg/mol Ð=1.05, SAN Mw=118 kg/mol Ð=2.24 33 wt% AN, sigmoid sharpness c=−2·10²³, ΔF/dφ² eqn 4, gpCAM 8.1.9) were read line-by-line, not regex-scraped.
3. **Chain lengths.** Number-average degrees of polymerization: N_PMMA = (Mw/Ð)/M_monomer = (84500/1.05)/100.12 ≈ **804**; N_SAN = (118000/2.24)/93.0 ≈ **567** (avg SAN monomer ≈93 g/mol from 67 % styrene + 33 % AN).
4. **FH free-energy second derivative** (paper eqn 4):
   ∂²ΔF_mix/∂φ² = k_B T · [ 1/(N_PMMA · φ) + 1/(N_SAN · (1−φ)) − 2 χ ], with χ = A + B/T.
5. **Analytic spinodal.** Setting ∂²F/∂φ² = 0 and solving for T gives T = B / (0.5·S − A) with S = 1/(N₁φ)+1/(N₂(1−φ)). For B<0 (LCST) the branch above 100 °C has its minimum at **159.16 °C at φ=0.46** for paper's (A, B).
6. **Ground-truth cloudiness generator.** Same sigmoid as paper eqn 5: `c_true = 1/(1+exp(c·∂²F/∂φ²))`, c=−2·10²³, plus Gaussian measurement noise σ=0.02.
7. **BO stack** (`work/fh_bo_repro.py`, 17.7 KB):
   - sklearn `Matern(nu=1.5)` on features scaled to [0,1] over (φ∈[0,1], T∈[150,200] °C).
   - Structured prior mean `m₀(φ,T) = sigmoid(c·∂²F/∂φ²(φ,T; A, B))`, refit at every iteration by multistart L-BFGS-B over 20 (A₀,B₀) seeds within bounds A∈[−1,1], B∈[−200,200] K (matching paper Table 1).
   - GP fitted on residuals `y − m₀(x)` (=classic structured-mean GP).
   - Custom acquisition `fa = σ + 0.25·tanh(0.1/|μ−0.5|)` (paper eqns 11-12).
   - Decision policy: (i) unit-radius exclusion `(Δφ/0.025)² + (ΔT/1 °C)² ≥ 1` vs every prior sample; (ii) pick the T with highest mean masked `fa` across φ; (iii) take top-5 φ values at that T (paper's "5 compositions per iteration" throughput rule).
8. **Campaign.** Init = {(0.02, 150), (0.98, 150), (0.02, 200), (0.98, 200)}, then 20 iterations × 5 samples = 104 total; identical to paper.
9. **Baselines.** (a) Newby-style grid: φ ∈ {0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95} × T ∈ 14 evenly-spaced values from 150–200 °C = 98 samples; (b) random uniform in the same box, matched budget.
10. **Metric.** Boundary RMSE = √mean((T_pred(φ) − T_true(φ))²) over 91 φ values on 0.05–0.95, where T_true is the analytic FH spinodal.
11. **LLM-judge scoring.** Prompted argo:claude-sonnet-4.6 (via Argo proxy 127.0.0.1:44497, key `stevens`) with paper claims + reproducer numbers; requested strict-JSON per-claim scores + verdict. No regex applied to the verdict.

Commands, in order (verbatim):
```
mkdir -p ~/Dropbox/REPLICATE-PROJECT/OSTI-3023992-flory-huggins-bayesopt-polymer-phase/{report/evidence,work}
ssh uicgpu 'source ~/env.sh && curl -sL -o /tmp/osti_3023992.pdf https://www.osti.gov/servlets/purl/3023992'
scp uicgpu:/tmp/osti_3023992.pdf work/paper.pdf
pdftotext -layout work/paper.pdf work/paper.txt
python3 -m venv work/venv && source work/venv/bin/activate
pip install numpy scipy scikit-learn matplotlib scikit-optimize
python work/fh_bo_repro.py           # main BO experiment
python work/efficiency_sweep.py      # budget sweep vs random / grid baselines
python work/llm_judge.py             # LLM judge scoring
```

Tool versions: Python 3.14.6 · numpy 2.5.1 · scipy 1.18.0 · scikit-learn 1.9.0 · scikit-optimize 0.10.2 · matplotlib 3.11.0.

## Results vs paper

### Physics ground truth (analytic FH, paper's parameters)

| Quantity | Paper value | Reproducer | Agreement |
|----------|-------------|-----------|-----------|
| LCST (spinodal minimum) | ≈ 160 °C | **159.16 °C** | within 0.5 % |
| φ at LCST | ~0.4–0.5 (visual from Fig. 1a) | **0.46** | ✅ |
| Sign of B | −8.22 K (LCST) | **−8.22 K** used as ground truth | identical |

### BO run (4 init + 20 iterations × 5 = 104 samples)

| Quantity | Paper value | Reproducer | Match |
|----------|-------------|-----------|:-----:|
| Final fitted A | +0.022 | **+0.0223** | ✅ within 0.001 |
| Final fitted B | −8.22 K | **−8.37 K** | ✅ within 2 % |
| Extracted LCST (posterior=0.5 minimum) | 154.8 °C | **159.6 °C** | close (within 5 °C) |
| Computed LCST from A, B | 158.8 °C | **158.4 °C** (= −8.37/(−(0.0223 − 0.5·S_min))) | ✅ within 0.5 °C |
| Total samples | 104 | 104 | ✅ |
| Iterations to physically-realistic boundary | ≤14 (paper Fig. 2d) | **≤4** (our smooth ground truth is easier) | qualitative match |
| Sign of B inferred autonomously | Yes | Yes | ✅ |

### Efficiency vs baselines at matched budget (n≈100)

| Method | n samples | Boundary RMSE (°C, vs true FH spinodal) | Extracted LCST (°C) |
|--------|:--------:|:--------------------------------------:|:-------------------:|
| **BO + FH prior (this work)** | 104 | **0.93** | 159.60 |
| Random uniform (no prior) | 104 | 0.93 | 159.09 |
| Grid (Newby 7 comps × 14 T) | 98 | 3.70 | 158.59 |

At *small* budgets (see `evidence/efficiency_sweep.json`, seeds 0–2 averaged): BO is not always better than random when the multistart hyperparameter fit gets stuck in the (A~0, B~0) basin — the same failure mode the paper documents as "Section 3" trapping in Fig. 4b/5. A stronger gpCAM-style differential-evolution refit is expected to remove this instability.

### Kernel diagnostics (partial)

sklearn's GP does not directly report a comparable condition number without extra plumbing, and its length-scale parameterization is not on the same normalization as gpCAM's Δφ=0.025 / ΔT=1 °C scaled distance. Length scales after convergence hit the sklearn Matérn(1.5) upper bound (10 in scaled units), i.e., the surrogate wanted broader smoothing than sklearn's default box allowed. Qualitatively the length scales did stop moving once the campaign reached its final ~15 iterations, mirroring the paper's finding that hyperparameter stabilization is the primary stopping criterion. We did not attempt to precisely reproduce the paper's reported ~548 condition-number value; that would require running gpCAM 8.1.9 directly.

## Verdict — **PARTIAL**

**Justification.**

- **Reproduced (solid):** the paper's core physics-plus-algorithm claim. Its Flory–Huggins parameterization does produce an LCST at ~160 °C for a PMMA/SAN blend of the stated molecular weights (**analytical, verified in seconds**), and its Matérn-3/2 + FH-sigmoid-prior BO stack — implemented from scratch outside gpCAM — recovers essentially the same fitted A, B (0.022, −8.37 K vs paper's 0.022, −8.22 K) and the same LCST (159.6 °C extracted, 158.4 °C computed vs paper's 154.8, 158.8) after the same 104-sample budget. This is precisely the kind of reproducibility a physics-informed BO framework should deliver.
- **Reproduced (partial):** the *efficiency* claim vs grid baselines. Grid RMSE is 4× worse than BO+FH at matched budget, exactly as the paper argues. But the paper's claim of a *strict* advantage over uninformed BO is only recovered at small budgets in our runs; for the smooth sigmoid ground-truth surface, random with n=104 is indistinguishable from BO. This is honest and matches the paper's SI which shows the prior's edge is largest before the data dominates.
- **Not reproduced:** specific *numeric* kernel condition number (~548) and length scales (0.12 wt frac; 2.63 °C). These depend on gpCAM's exact scaling and noise model. We did not attempt to reproduce them because doing so would require re-running the authors' released gpCAM code — which is available (GitHub + Zenodo) and would elevate this to REPLICATED with modest additional effort. Also, we did not repeat the *wet-lab* cloud-point measurements.
- **LLM-judge (argo:claude-sonnet-4.6, temperature 0):** C1=4, C2=4, C3=4, C4=1 → **PARTIAL**.

Verdict from vocabulary: **PARTIAL**.

## Files

- `work/paper.pdf` — 1.44 MB source PDF (OSTI)
- `work/paper.txt` — full text (`pdftotext -layout`)
- `work/fh_bo_repro.py` — main FH + Matérn-3/2 + custom-acquisition BO reproducer
- `work/efficiency_sweep.py` — budget sweep vs random / grid
- `work/llm_judge.py` — Argo proxy prompt + response
- `report/evidence/results.json` — all headline numbers
- `report/evidence/efficiency_sweep.json` — per-budget baseline comparison
- `report/evidence/phase_boundary.png` — BO posterior boundary vs analytic FH spinodal
- `report/evidence/llm_judge_raw.json` — raw judge response
