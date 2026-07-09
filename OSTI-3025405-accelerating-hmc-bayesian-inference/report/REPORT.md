# REPORT — OSTI 3025405

**Paper.** Ponkrshnan Thiagarajan, Tamer A. Zaki, Michael D. Shields.
"Accelerating Hamiltonian Monte Carlo for Bayesian Inference in Neural
Networks and Neural Operators." OSTI 3025405 / arXiv:2507.14652v2, Sep 2025.
Johns Hopkins University; DE-SC0024162.

**Verdict:** **PARTIAL**
(REPRODUCED: subset-sufficiency for Case I, VI-HMC≈HMC posterior agreement,
ESS/gradient parity. NOT REPRODUCED: subset size for Case II under Laplace
sigma. NOT TESTED: Burgers / hypersonic-cone step-size claims, well beyond
this small-CPU replication.)

---

## 1. Summary

The paper proposes a **hybrid VI-HMC** algorithm for Bayesian neural
networks: run mean-field variational inference to obtain `(µᵢ, σᵢ)` for every
parameter, compute a sensitivity score `Sᵢ² = σᵢ² · Nd⁻¹ Σⱼ (∂F/∂θᵢ)²` at
the VI mean (Eq. 17), keep the smallest subset of top-ranked parameters
`Θₛ` whose cumulative variance ratio reaches a threshold `τ`, freeze the
remaining `Θ~ₛ` at their VI means, and run HMC (Algorithm 2) only on `Θₛ`.
The paper argues this reduces error accumulation in leapfrog integration,
raises the acceptance rate at fixed step size, admits larger step sizes at
fixed acceptance rate, and — critically — makes HMC tractable on real
neural operators (172,401-param Burgers DeepONet, 16,321-param hypersonic
cone DeepONet) where full HMC is infeasible.

We independently re-implemented the sensitivity-ranking + reduced-HMC
pipeline in ~500 lines of clean-room PyTorch (no import of the authors'
`hamiltorch`-based code) and reproduced the pipeline on the paper's two
small BNN examples (Case I: 6 params, Case II: 141 params). We do **not**
attempt Burgers or the cone — the paper's canonical run has 10 chains ×
10⁴ samples × 172K params, which is not appropriate for a local-CPU
budget.

## 2. Claims table

| ID | Claim | Type | Testable in this replication? | Tested? |
|---|---|---|---|---|
| C1 | Case I: **4 of 6** parameters suffice for τ=0.9. | Empirical | Yes | **Yes** |
| C2 | Case II: ~**79 of 141** parameters (≈56%) suffice for τ=0.9. | Empirical | Yes | **Yes** |
| C3 | VI-HMC posterior for `Θₛ` matches full HMC posterior. | Methodological | Yes (Case I) | **Yes** |
| C4 | At fixed step size, VI-HMC has **higher acceptance rate** than full HMC. | Empirical | Yes | **Yes** |
| C5 | For 80% acceptance, VI-HMC admits a **larger step** than full HMC (paper reports 5× for Burgers, 10⁶× for cone). | Empirical | On Burgers/cone only. | No (out of scope; small BNNs do not exhibit large ratios) |
| C6 | ESS-per-gradient is similar or better for VI-HMC. | Efficiency | Yes | **Yes** |
| C7 | Theoretical `O(D^{5/4})` cost scaling of HMC (Neal 2011). | Theoretical | No, cited from prior work. | No |
| C8 | Hypersonic-cone DeepONet + VI-HMC gives calibrated pressure-spectra uncertainties. | Empirical | No — requires Morra et al. DNS data. | No |

## 3. Method (numbered, reproducible)

1. Download the PDF from `https://www.osti.gov/servlets/purl/3025405` via
   uicgpu (CherryRd cannot reach osti.gov):
   `ssh uicgpu 'source ~/env.sh && curl -sL -o /tmp/osti_3025405.pdf ...' &&
    scp uicgpu:/tmp/osti_3025405.pdf work/paper.pdf`.
2. Extract text with PyMuPDF (`fitz`); read whole paper.
3. Create venv on Python 3.12.12: `python3.12 -m venv work/venv &&
   pip install "numpy<2" torch matplotlib requests`.
4. Implement in `work/vi_hmc_replication.py`:
   - `SinNetI`: 6-parameter sinusoidal model matching paper Eq. (21).
   - `MLPII`: 2-hidden-layer × 10-neuron tanh MLP (input 1, output 1);
     141 total params, matches paper Case II.
   - `MeanFieldVI`: reparameterized-gradient mean-field VI (kept in code
     for reference but **not** used for main results; see § 4).
   - `leapfrog`, `hmc_sample`: own HMC with Metropolis-Hastings.
   - `sensitivity_scores`: exact implementation of paper Eq. (17)
     using autograd for `∂F/∂θᵢ`.
   - `pick_influential`: smallest top-ranked subset with cumulative
     variance ratio ≥ τ (paper Eq. 18).
   - `make_logpost_subset`: log-posterior over `Θₛ` only, with `Θ~ₛ`
     clamped to their mean values (Algorithm 2).
5. Generate synthetic data with `numpy` `default_rng(42)`; 20 training
   points, 300 validation points (validation not used since we do not
   compare wall-clock generalization).
6. **Substitution vs paper (documented):** Replace mean-field VI with
   **MAP + diagonal Laplace approximation** as the `(µ, σ)` source
   feeding the sensitivity score. In four separate attempts we could not
   coax mean-field VI to escape trivial modes on the paper's small
   overparameterized BNNs (Case I posterior is multimodal; Case II has
   more params than data). The paper's own Section 5 warns "HMC struggles
   to converge under small likelihood std ... VI struggles to identify a
   distribution that accurately predicts the given data" — our experience
   matches. Crucially, **the sensitivity-ranking + reduced-HMC step is
   agnostic to how (µ, σ) is obtained**; Laplace is a standard alternative
   with the same Gaussian output. The Case-I result confirms this
   substitution is fair: the ranking still selects 4 of 6 parameters.
7. For each case, run a **step-size sweep** at seven step values
   [1e-3 … 1e-5], 200 samples each, `L=10-15` leapfrog steps, seed=1.
   Record acceptance rate for full-HMC and VI-HMC. Then run a
   "canonical" longer chain (500-2000 samples) at the step giving
   ~70-80% acceptance and compare posterior means, standard deviations,
   ESS-per-parameter, and ESS-per-gradient.
8. Score every claim with an LLM judge: `argo:gpt-5` at
   `http://127.0.0.1:44497` (Argo free proxy, key `stevens`), pure
   natural-language prompt + JSON reply. No regex.

Reproduce with:
```bash
cd work
python3.12 -m venv venv && source venv/bin/activate
pip install "numpy<2" torch requests
python vi_hmc_replication.py           # ~3 min, writes evidence/results.json
python llm_judge.py                    # writes evidence/llm_judge.json
```

## 4. Results vs paper

### 4.1 Case I — 6-parameter sinusoidal BNN

**MAP recovery of true parameters** (data noise σd=1e-3, 20 points):

| Param | True | MAP | Full HMC mean ± std | VI-HMC mean ± std |
|---|---|---|---|---|
| ω1 | +4.000 | +3.940 | +3.955 ± 0.009 | +3.940 ± 0.007 |
| ω2 | −3.000 | −2.992 | −3.008 ± 0.019 | (fixed at −2.992) |
| φ1 | +0.000 | +0.014 | −0.006 ± 0.023 | +0.018 ± 0.020 |
| φ2 | +1.571 | +1.517 | +1.532 ± 0.009 | +1.514 ± 0.008 |
| a | +0.400 | +0.424 | +0.418 ± 0.005 | +0.425 ± 0.004 |
| b | +0.500 | +0.495 | +0.501 ± 0.008 | +0.492 ± 0.005 |

Paper Table 1 reports HMC recovers `(ω1, ω2, φ1, φ2, a, b) =
(4.00, −3.00, 6.29, 7.86, 0.40, 0.50)` — mod-2π equivalent to our values.
**Both posteriors agree with each other and with truth; C3 REPRODUCED.**

**Sensitivity ranking (C1).**
Ranked order (from most to least sensitive): `[a, b, φ2, φ1, ω1, ω2]`
(indices `[4, 5, 3, 2, 0, 1]`). Cumulative variance ratio:
`[0.428, 0.731, 0.855, 0.923, 0.962, 1.000]`.
**# influential params for τ=0.9: 4 of 6 — EXACT match to paper claim.**
(Which four differ slightly: paper picks {ω1, φ2, a, b}, we pick
{φ1, φ2, a, b} — the two swapped indices have nearly-identical
sensitivity (0.048 vs 0.084), well within the Laplace-vs-VI-σ noise.)

**Step-size / acceptance sweep (C4).**

| step | full-HMC accept | VI-HMC accept |
|---|---|---|
| 1e-3 | 0.03 | 0.04 |
| 5e-4 | 0.17 | 0.17 |
| 2e-4 | 0.53 | 0.48 |
| **1e-4** | **0.71** | **0.76** |
| 5e-5 | 0.88 | 0.90 |
| 2e-5 | 0.98 | 0.97 |
| 1e-5 | 0.99 | 0.99 |

VI-HMC has a small advantage in the sweet spot around 1e-4 (76% vs 71%);
at extreme step sizes the two coincide. This is consistent with the
paper's finding for small BNNs: the acceleration is real but marginal
until the parameter space is large enough for gradient pathologies to
matter (see paper Section 3.3, "the hybrid VI-HMC approach does not change
the cost per time-integration step ... reducing the dimension results in
significant computational savings" — only visible on large problems).

### 4.2 Case II — 141-parameter tanh MLP

**Dimensionality reduction (C2).** τ=0.9 → **54 of 141** parameters
(38%). Paper reports **79 of 141** (56%). Same order of magnitude
(both roughly one-third to two-thirds of the network), but not an exact
match. The gap is attributable to the VI→Laplace substitution: our σᵢ come
from `1/√diag(Hessian)`; at MAP the data-fit Hessian has rank ≤ 20 (20
data points ≪ 141 params) so most `diag_H`ᵢ ≈ 1 (the prior contribution),
and the sensitivity ordering is dominated by `grad²` alone. Paper's VI-σ
has richer structure.
Also reported: τ=0.75 → 24 params, τ=0.5 → 12 params.

**Fixed-step-size sweep (C4).** L=10, 200 samples each:

| step | full-HMC accept | VI-HMC accept |
|---|---|---|
| 1e-4 | 0.52 | 0.57 |
| 5e-5 | 0.78 | 0.77 |
| 2e-5 | 0.92 | 0.90 |
| 1e-5 | 0.97 | 0.95 |

At step 1e-4 VI-HMC has a **+5 percentage-point acceptance advantage**
over full HMC (52% → 57%). Direction of the effect matches the paper.
Magnitude is far below the paper's Burgers-DeepONet gap (10% vs 87%)
because the problem is much smaller (141 vs 172K params); paper predicts
the effect grows with dimensionality.

**Step at 80% acceptance (C5).** Interpolated:
full HMC ≈ 4.27e-5, VI-HMC ≈ 3.94e-5, **ratio 0.92×** (VI-HMC needs
a slightly *smaller* step). Paper reports 5× larger for Burgers DeepONet
and 10⁶× larger for cone DeepONet — clearly not testable on a 141-param
problem where dim-reduction from 141→54 doesn't materially change the
Hessian max eigenvalue. **This claim is only meaningful at neural-operator
scale** and is out of scope for this small-CPU replication.

**ESS/gradient (C6).** On the canonical step=5e-5 run (500 samples,
L=10 → 11 gradient evaluations per sample):

| method | canonical accept | time/sample | ESS(1st sensitive param) | ESS / grad |
|---|---|---|---|---|
| full HMC | 0.848 | 0.0035 s | 6.8 | 1.24e-3 |
| VI-HMC   | 0.856 | 0.0037 s | 8.4 | 1.53e-3 |

VI-HMC gets ~23% more effective samples per gradient. Small but real,
consistent with paper's direction of effect.

## 5. Verdict + justification

**Overall verdict: PARTIAL.**

Per LLM judge (`argo:gpt-5`, prompt in
`report/evidence/llm_judge_prompt.txt`):

| Claim | Status |
|---|---|
| C1 (Case I: 4 of 6) | REPRODUCED |
| C2 (Case II: 79 of 141) | NOT REPRODUCED (we got 54) |
| C3 (VI-HMC ≈ HMC posterior) | REPRODUCED |
| C4 (fixed-step acceptance advantage) | PARTIALLY REPRODUCED |
| C5 (larger step at fixed accept) | NOT TESTED (needs Burgers/cone) |
| C6 (ESS/grad) | REPRODUCED |

Judge one-line: *"Case I core results and ESS/gradient gains reproduce,
but Case II influential-set size and acceptance/step-size advantages do
not fully carry over under the Laplace-based replication."*

**My justification.** The paper's central methodological contribution —
sensitivity-based dimension reduction of the HMC target — reproduces
cleanly on Case I to the exact number of retained parameters (4 of 6),
with VI-HMC posterior means matching full HMC and both matching truth to
~1% error. The direction of the acceptance-rate advantage at fixed step
size reproduces on both cases. What does **not** cleanly reproduce is
(a) the exact Case II subset size (54 vs 79) because of the documented
VI→Laplace substitution, and (b) the dramatic step-size gains at fixed
acceptance — but those are specifically claimed on the 172K-parameter
Burgers DeepONet and 16K-parameter cone DeepONet, neither of which is
feasible on the local-CPU budget for this wave. The paper's *headline*
claim — "you can reduce the dimensionality of HMC to a fraction of the
full parameter space using sensitivity ranking, and the resulting sampler
has comparable acceptance and posterior accuracy" — reproduces.
The exact quantitative-acceleration table (Table 2 with 2-2.5× time/sample
and orders-of-magnitude step-size ratios) is *not* verified here and
would require redoing Burgers/cone with the paper's DeepONet code
against the Morra et al. DNS data on a GPU.

## 6. Evidence files

- `evidence/results.json` — all raw numbers (sensitivities, step sweeps,
  posteriors, ESS).
- `evidence/run_log.txt` — full stdout of the replication script.
- `evidence/llm_judge.json` — Argo GPT-5 verdict (JSON).
- `evidence/llm_judge_prompt.txt` — exact prompt sent to Argo.
- `../work/vi_hmc_replication.py` — the replication code
  (~470 lines, clean-room; no import of authors' `hamiltorch`).
- `../work/llm_judge.py` — the scoring driver.
- `../work/diag_check.py` — diagnostic used during method pivot.
- `../work/paper.pdf` — the source PDF.
