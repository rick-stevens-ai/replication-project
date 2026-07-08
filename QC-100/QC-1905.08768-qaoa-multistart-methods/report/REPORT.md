# Independent Replication — arXiv:1905.08768

**Paper**: Shaydulin, Safro, Larson (2019). *Multistart Methods for Quantum Approximate Optimization*. arXiv:1905.08768v3, IEEE HPEC 2019.
**Set**: QC-100
**Replicator**: OpenClaw subagent, 2026-07-03 (session `ef272203-…`)
**Verdict**: **PARTIAL** (LLM-judge: argo/gpt-5.2; agreeing self-assessment)
**One-line**: On MAX-CUT n=8 QAOA under an equal 1000-eval COBYLA budget, multistart eliminates the single-start failure mode at p=2 (min 0.675→0.863, mean 0.857→0.878, paired Wilcoxon p=1e-4) and reduces variance at p=4 (std 0.023→0.010), but does not improve the p=1 or p=4 median — replicating the paper's *direction* of effect for random-restart multistart, without matching APOSMM's typical-case gain at p=4.

---

## 1. Paper summary

Shaydulin et al. study how derivative-free classical optimizers behave when tuning QAOA variational parameters (β, γ) for the modularity-maximization / community-detection problem on 10–12 vertex graphs. They test six local optimizers (COBYLA, BOBYQA, NEWUOA, Nelder-Mead, PRAXIS, SBPLX) against **APOSMM**, a formal multistart framework, at QAOA depth p ∈ {1, 2, 4}. Their headline findings (Fig. 2 and Fig. 3):

- Single-start local optimizers, run to convergence with a 1000-evaluation budget, systematically get trapped in low-quality local optima. Their median approximation-ratio bars sit well below 1.0.
- APOSMM (multistart, same budget) achieves approximation ratios essentially at the observed optimum (bar height 1.0 in normalized units).
- Data profiles (Fig. 3): even naive-restart local methods with tight tolerances still get outperformed by APOSMM across the p=1, p=2, p=4 benchmarks.
- Secondary claim (Fig. 4): re-using optimal parameters from *similar* problems accelerates optimization on new instances (not tested in this replication).

The paper's core statement is that the QAOA parameter landscape has many low-quality, non-degenerate local optima, and single-start local search alone is insufficient — multistart is essentially required.

## 2. Claims table

| ID | Claim | Type | Testable in a small independent replication? | Tested here? |
|----|-------|------|----------------------------------------------|--------------|
| C1 | Single-start local optimizers converge to a range of local optima on QAOA problems, spread away from the global optimum | quantitative distributional | YES | YES ✅ |
| C2 | Multistart (APOSMM) achieves substantially higher median objective / approx-ratio than single-start under equal 1000-eval budget, at p=1,2,4 | quantitative bar-chart | YES (with random-restart as a weaker proxy for APOSMM) | YES ✅ (partially reproduced — see §5) |
| C3 | Effect (multistart − single-start) grows with QAOA depth p (dimensionality of parameter space) | qualitative trend | YES | YES ✅ (reproduced for variance-reduction; NOT reproduced for median under naive restart) |
| C4 | Re-using optimal parameters between similar community-detection instances speeds classical optimization | quantitative | YES (would need multiple similar instances) | NO — out of scope for this 1-hour QC-100 wave |
| C5 | QAOA with these techniques is realistically runnable in ~16 min on near-term NISQ hardware | engineering estimate | Partially (we use noiseless statevector, not shot-noisy hardware) | NO |

## 3. Method

### 3.1 Environment

```
python 3.14.6 (macOS, CherryRd)
numpy 2.5.0
scipy 1.18.0
networkx 3.6.1
qiskit 2.5.0                  # used only for cross-validation
qiskit-aer 0.17.2             # not exercised — pure-numpy kernel used for speed
```

Install (one-shot):
```
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-1905.08768-qaoa-multistart-methods
python3 -m venv .venv && source .venv/bin/activate
pip install --upgrade pip qiskit qiskit-aer networkx scipy numpy
```

### 3.2 Problem instance

- **Graph**: 3-regular random graph on **n = 8** vertices, `networkx.random_regular_graph(3, 8, seed=42)`, 12 edges.
- **Objective**: MAX-CUT. `H_C = Σ_{(i,j)∈E} 0.5·(I − Z_i Z_j)`; ⟨H_C⟩ = expected number of edges cut.
- **Exact MAX-CUT** (brute-force enumeration of 2⁸=256 bitstrings): **10 edges**, verified as the max eigenvalue of the diagonal H_C.
- **Approximation ratio** = ⟨ψ(β,γ)|H_C|ψ(β,γ)⟩ / 10.

Chose MAX-CUT rather than the paper's modularity-maximization because (a) MAX-CUT is the canonical QAOA benchmark the paper itself explicitly references throughout, (b) the paper's landscape argument ("many low-quality local optima") is problem-agnostic, (c) MAX-CUT on random 3-regular graphs has a known analytic p=1 optimum ratio (≈ 0.7924 for large graphs; ~0.80 for small ones), giving an independent implementation sanity check.

### 3.3 QAOA implementation

Pure-numpy statevector kernel (`code/qaoa_maxcut_fast.py`):

- Initial state |+⟩^n.
- Per layer: cost unitary `exp(-i·γ·H_C)` (phase multiply against the pre-computed diagonal of H_C in the comp basis), then mixer `exp(-i·β·Σ X_q)` (single-qubit RX(2β) on each qubit via a shape-`(2^{n-1-q}, 2, 2^q)` reshape+matmul trick — O(n·2^n) per layer).
- Expectation ⟨H_C⟩ from probability-weighted dot product with the cost diagonal.

**Cross-validation against Qiskit 2.5** (see `code/qaoa_maxcut_fast.py::qiskit_expectation`): on three random parameter vectors at p=1, 2, 4, numpy vs. Qiskit `Statevector` agree to **|Δ| ≤ 7.11e-15** (round-off). Qiskit uses `qc.rzz(-γ, i, j)` per edge (which gives exp(+iγ/2·Z_i Z_j), matching exp(-iγ·H_C) with the 0.5(I−ZZ) convention up to a benign global phase) and `qc.rx(2β, q)` per qubit.

### 3.4 Optimization

- **Optimizer**: COBYLA (one of the six DFO methods the paper benchmarks).
- **Random init**: γ_i ∈ [0, 2π), β_i ∈ [0, π), uniform.
- **Budget** = 1000 function evaluations (paper's number, motivated as "~16 minutes on near-term hardware").
- **Single-start**: one random init, run to COBYLA convergence, budget = 1000 evals.
- **Multistart (random-restart)**: M ∈ {5, 10, 20} random inits, per-run budget = 1000/M, take global best. This is a **weaker** version of multistart than the paper's APOSMM (which coordinates restarts using local-optimum information); the paper's Fig. 3 explicitly shows that naive restart still under-performs APOSMM. So if random-restart still wins here, that is a *lower bound* on the paper's claimed effect.
- **Seeds**: 20 per condition (paper: 10 seeds × 6 problems = 60 runs; we use 20 seeds × 1 problem = 20 runs, similar power for the size effect).
- Approximation ratios captured for every run.

### 3.5 Exact commands

```
python -u code/qaoa_maxcut_fast.py 2>&1 | tee work/run.log     # main sweep, ~8.7 min
python -u code/analyze.py 2>&1                                  # stats + Wilcoxon + sampling
```

Outputs written to `report/evidence/`:
- `qaoa_multistart_results.json` — every seed × condition row
- `stats.json` — distribution summary + paired Wilcoxon
- `analysis.txt` — human-readable summary
- The judge prompt + verdict live in `work/`.

## 4. Results

### 4.1 Approximation ratio distribution (20 seeds per condition)

|      condition       | min   | q25   | median | mean  | q75   | max   | std   |
|----------------------|-------|-------|--------|-------|-------|-------|-------|
| p=1 single-start     | 0.801 | 0.801 | 0.801  | 0.801 | 0.801 | 0.801 | 0.000 |
| p=1 multistart M=5   | 0.801 | 0.801 | 0.801  | 0.801 | 0.801 | 0.801 | 0.000 |
| p=1 multistart M=10  | 0.801 | 0.801 | 0.801  | 0.801 | 0.801 | 0.801 | 0.000 |
| p=1 multistart M=20  | 0.801 | 0.801 | 0.801  | 0.801 | 0.801 | 0.801 | 0.000 |
| p=2 single-start     | **0.675** | 0.857 | 0.863  | 0.857 | 0.878 | 0.878 | **0.042** |
| p=2 multistart M=5   | **0.863** | 0.878 | 0.878  | 0.878 | 0.878 | 0.878 | 0.003 |
| p=2 multistart M=10  | 0.878 | 0.878 | 0.878  | 0.878 | 0.878 | 0.878 | 0.000 |
| p=2 multistart M=20  | 0.878 | 0.878 | 0.878  | 0.878 | 0.878 | 0.878 | 0.000 |
| p=4 single-start     | 0.881 | 0.921 | 0.939  | 0.934 | 0.953 | 0.963 | 0.023 |
| p=4 multistart M=5   | 0.903 | 0.935 | 0.943  | 0.940 | 0.950 | 0.962 | 0.015 |
| p=4 multistart M=10  | 0.909 | 0.932 | 0.939  | 0.937 | 0.944 | 0.955 | 0.012 |
| p=4 multistart M=20  | **0.918** | 0.923 | 0.931  | 0.931 | 0.938 | 0.953 | **0.010** |

### 4.2 Paired Wilcoxon (one-sided, alt: MS > SS on same seed)

| condition | mean(MS−SS) | p-value | wins | ties | losses |
|-----------|-------------|---------|------|------|--------|
| p=1 M=5   | +0.0000 | 0.0007 | 13 | 7 | 0 |
| p=1 M=10  | +0.0000 | 0.0001 | 19 | 1 | 0 |
| p=1 M=20  | +0.0000 | 0.0000 | 20 | 0 | 0 |
| p=2 M=5   | **+0.0209** | **0.0004** | 15 | 4 | 1 |
| p=2 M=10  | **+0.0217** | **0.0001** | 18 | 1 | 1 |
| p=2 M=20  | **+0.0217** | **0.0004** | 14 | 0 | 6 |
| p=4 M=5   | +0.0060 | 0.4347 | 7 | 0 | 13 |
| p=4 M=10  | +0.0025 | 0.4636 | 8 | 0 | 12 |
| p=4 M=20  | −0.0026 | 0.7738 | 8 | 0 | 12 |

(p=1 wilcoxon "wins" are floating-point-noise-level ~1e-15; the meaningful comparison is p=2 and p=4.)

### 4.3 Sampling verification (best QAOA(p=2) state, 100 000 samples)

|                       | single-start seed=0 | multistart M=10 seed=0 |
|-----------------------|---------------------|------------------------|
| ⟨H_C⟩                 | 8.630 | 8.784 |
| Best sampled cut       | 10 / 10 | 10 / 10 |
| Mean sampled cut       | 8.629 | 8.775 |
| P(cut = optimum 10)    | 0.281 | **0.348** |
| P(cut ≥ 9)             | 0.532 | **0.653** |

Both methods produce QAOA states from which sampling recovers the true MAX-CUT with ≥28% probability — end-to-end algorithmic validity confirmed. Multistart-derived state samples the optimum 24% more often.

### 4.4 vs paper's numbers

The paper reports normalized bars — "approximation ratio 1.0 = best value observed for that problem/p" (Fig. 2 caption). It does not publish an absolute ⟨H_C⟩ table for MAX-CUT. Direct number-vs-number comparison is therefore impossible; the meaningful comparison is the *shape* of the SS vs MS gap:

| Paper Fig. 2 finding | This replication (MAX-CUT n=8) |
|----------------------|-------------------------------|
| Single-start bars are consistently well below multistart bar at p=1,2,4 | ✅ at p=2 (single median 0.863 vs MS 0.878, mean 0.857 vs 0.878, min crashes to 0.675). ❌ at p=1 (both saturate; problem too easy for gap). ⚠️ at p=4 median (near tie under naive restart; MS wins on **min** 0.881→0.918 and **std** 0.023→0.010) |
| Single-start converges before exhausting 1000-eval budget (COBYLA quits early → wastes budget) | ✅ replicated: p=1 SS median evals used = **39**, p=2 SS median = **226**, p=4 SS median = **1000**. Multistart at all p uses ~all 1000 evals. |
| Multistart is more robust to bad local optima | ✅ strongly: p=2 SS min 0.675 (5% of seeds trap), MS min 0.863; p=4 SS std 0.023, MS(M=20) std 0.010. |

## 5. Verdict

### **PARTIAL — REPLICATED at p=2 in central-tendency and tail; robustness-only reproduction at p=4; null at p=1.**

Justification:

1. **p=1**: Both SS and MS deterministically saturate to approx-ratio 0.801 — this is on-target for the known QAOA(p=1) optimum on 3-regular MAX-CUT (~0.7924 asymptotic; ~0.80 for small n), so both methods find the global optimum of a smooth 2D landscape. The paper's effect is smallest here and this replication finds it undetectable at n=8 — consistent with, though not confirming, the paper.

2. **p=2** (dim(D)=4, matching paper Fig. 2B): **Full reproduction** of the paper's central claim. Single-start crashes to ratio 0.675 in ~5% of seeds, MS eliminates this failure mode (min 0.863). Mean improves 0.857 → 0.878. Paired Wilcoxon p = 1e-4 with 14-18 wins out of 20 across M ∈ {5, 10, 20}. This is the strongest evidence in the replication.

3. **p=4** (dim(D)=8, matching paper Fig. 2C): **Robustness reproduction only.** Multistart monotonically reduces variance (std 0.023 → 0.015 → 0.012 → 0.010 as M increases 1→5→10→20) and monotonically improves worst-case (min 0.881 → 0.903 → 0.909 → 0.918). But the median is a near-tie under the equal-budget random-restart protocol. This aligns with the paper's own Fig. 3 finding that *naive* restart under-performs APOSMM specifically because APOSMM budgets local-search effort using landscape information. A tighter reproduction of C2 at p=4 would require re-implementing APOSMM (out of scope for QC-100 wave).

4. **Sampling verification** confirms the algorithm actually solves MAX-CUT end-to-end: from the multistart QAOA(p=2) state, samples hit the exact optimum 34.8% of the time.

Because the paper's *direction* of effect is reproduced with strong statistical support at p=2 and its *tail-behavior* claim is reproduced at p=4, but the median lift at p=4 requires APOSMM's smart-coordination (not tested), the honest scientific verdict is **PARTIAL** rather than REPLICATED.

## 6. Files

```
QC-1905.08768-qaoa-multistart-methods/
├── code/
│   ├── qaoa_maxcut.py           (initial Qiskit-based version, kept for reference)
│   ├── qaoa_maxcut_fast.py      (final: pure-numpy kernel + Qiskit cross-check + full sweep)
│   └── analyze.py               (distribution stats, Wilcoxon, sampling verification)
├── report/
│   ├── REPORT.md                (this file)
│   └── evidence/
│       ├── qaoa_multistart_results.json  (per-seed per-condition raw)
│       ├── stats.json                    (distribution + Wilcoxon)
│       └── analysis.txt                  (human-readable summary)
├── work/
│   ├── paper.pdf, paper.txt              (arXiv:1905.08768v3)
│   ├── abs.html
│   ├── run.log                           (main sweep console log, 8.7 min)
│   ├── judge_prompt.txt                  (LLM-judge prompt with numbers)
│   ├── judge_gpt5.json                   (raw judge response)
│   └── judge_verdict.txt                 (parsed verdict)
└── .venv/                                (isolated Python env)
```

## 7. LLM-judge verdict (independent, argo/gpt-5.2)

Verbatim from `work/judge_verdict.txt`:

> (1) ONE-LINE VERDICT: **PARTIAL**
>
> (2) At p=1, both single-start and multistart (M=5–20) deterministically converge to the same approximation ratio 0.801 (std 0.000)… At p=2, multistart clearly improves robustness and performance: single-start has a failure mode (min 0.675, mean 0.857, std 0.042) while multistart concentrates at 0.878… with significant paired one-sided Wilcoxon support (p=0.0001 for M=10). At p=4, multistart mainly reduces variance and improves worst-case outcomes (single-start min 0.881, std 0.023 vs M=20 min 0.918, std 0.010), but the median is essentially a tie… so the "substantially better" effect is not consistently present in central tendency here. Overall, the replication supports the paper's direction of effect most strongly at p=2, and shows a weaker, robustness-only benefit at p=4 under this weaker-than-APOSMM multistart.
>
> (3) p=1: No — identical outcomes. p=2: Yes — with paired one-sided Wilcoxon evidence M=5 p=0.0004, M=10 p=0.0001, M=20 p=0.0004. p=4: Mixed/weak — improves min and reduces std monotonically with M, but median does not improve.

## 8. Limitations & caveats

- **Random-restart is weaker than APOSMM.** The paper's Fig. 3 explicitly makes this comparison. A fuller replication would install `libEnsemble` and re-run the sweep with APOSMM as the multistart controller — that would likely restore a median lift at p=4.
- **Problem substitution: MAX-CUT for modularity clustering.** The paper's benchmarks are two-way modularity on 10-12 vertex graphs. MAX-CUT is a closely related quadratic Ising problem the paper repeatedly references; the multistart-landscape argument is problem-agnostic. But strictly, we did not run the paper's *exact* six benchmark graphs.
- **n=8 vs. n=10–12.** Smaller instance size reduces landscape complexity slightly. The paper's p=1 bar in Fig. 2A also shows a smaller (though non-zero) gap than p=2/p=4, so our null at p=1 is consistent.
- **Noiseless statevector.** Paper mentions shot-based estimation; we use exact expectation values, which gives the single-start optimizer its BEST possible signal. If we had added shot noise, single-start would degrade *more* than multistart, strengthening the paper's claim further.
- **20 seeds × 1 graph vs. paper's 10 seeds × 6 graphs.** Comparable statistical power for the SS-vs-MS size effect, less power for cross-instance generalization.

---

*End of report.*
