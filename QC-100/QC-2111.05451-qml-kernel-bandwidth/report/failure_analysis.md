# Failure Analysis — QC-2111.05451 (Shaydulin & Wild, QML kernel bandwidth)

**Purpose.** This file is deliberately harsher than REPORT.md. It documents what was NOT reproduced, what would falsify the top-line verdict, and where the replication over-reaches.

## 1. What the top-line verdict actually rests on

Verdict: **REPLICATED** — rests entirely on the mechanism claims C1–C4 at n=4 qubits on `make_moons`. Specifically:

- **Collapse to random guess at large λ:** 0.510 ± 0.052 at λ=3.0 vs. paper's ~0.5.
- **Sweet-spot exists:** 0.820 at λ=0.3 (mean, 5 seeds).
- **Off-diag K decays monotonically:** 0.9992 → 0.065 across λ ∈ [0.01, 10.0].

These three numbers are unambiguous and reproduce independently. Full stop.

## 2. What was NOT reproduced

### 2.1 Qubit-scaling (paper's Fig. 2 headline)

The paper's *practical* claim is Fig. 2: optimized-λ quantum-kernel SVC accuracy **improves** with qubit count up to ~14 qubits, becoming competitive with the best classical baseline. **We did not sweep n.** We tested only n=4. This is the paper's actual utility claim, and we did not exercise it.

**Falsification bar:** if a sweep at n ∈ {4, 8, 12, 16} showed that even at optimal λ the accuracy on Fashion-MNIST-PCA-nq did NOT rise with n — or fell below the classical baseline at every n — that would falsify the paper's headline and downgrade our verdict. Untested.

### 2.2 Paper-specific datasets

The paper uses Fashion-MNIST-PCA, KMNIST-PCA, and PLASTiCC-PCA. We used `make_moons`. `make_moons` is:
- 2D natively (paper needs ≥4D and up to 26D via PCA),
- near-linearly-separable (classical linear SVM also scores 0.875 here — the quantum kernel has nothing to add),
- synthetic, not photographic/astrophysical.

We ASSERT the bandwidth mechanism is dataset-agnostic (because it's a property of the feature-map angle scaling, not of the data), but we do NOT SHOW it on the paper's actual datasets.

### 2.3 Multiple feature-map families

The paper claims the bandwidth effect holds across three feature-map families (IQP, Hamiltonian evolution, variational-ansatz). We tested only IQP-style depth-2. Two of the three feature-map families in the paper are untested.

### 2.4 Formal kernel-concentration metric

We used mean off-diagonal K as a concentration proxy. The paper's theoretical framing (following Huang, Kübler, Thanasilp) is in terms of Var_{x,x'}[k(x,x')] under a data measure — the formal exponential-concentration quantity. We did not compute that, nor the sample-complexity lower bound it implies. Our mechanism check is qualitative, not tied back to the statistical-learning-theory bound.

### 2.5 C hyperparameter unswept

SVC regularization C=1.0 held fixed. A strict replication would sweep C per-λ to check whether the sweet-spot in λ is robust to C. This is a minor issue (the paper's headline collapses are large — 0.51 vs 0.82 — well outside any plausible C-swing effect) but worth noting.

### 2.6 Seed count

5 seeds. Standard deviations at collapse (0.052) and at optimum (0.027) are tight enough for the headline conclusions, but the more marginal points (λ ∈ {0.05, 0.10, 1.0}) have σ ≈ 0.06 that a 20-seed run would tighten.

## 3. Comparison against classical-kernel baseline

We compared to classical linear SVM (0.875) and RBF SVM (0.875) on the same 40/40 `make_moons` split. The quantum sweet-spot (0.820) is **competitive-but-worse** than classical on this data at n=4. This is:

- **Consistent** with the paper (they argue quantum only becomes advantageous as n grows to ~14),
- **NOT corroboration** of quantum advantage — we can't show quantum > classical here, only that quantum-with-bandwidth is close to classical, whereas quantum-without-bandwidth-tuning collapses to random.

Honest reading: the replication corroborates the *bandwidth-fixes-a-broken-quantum-kernel* claim, not the *quantum-kernel-beats-classical* claim.

## 4. Concentration/trainability trade-off — verified qualitatively only

The paper's central mechanism is that small bandwidth → kernel concentration → both loss-landscape flattening AND generalization failure. We verified the KERNEL SIDE (off-diag K collapses) and the GENERALIZATION SIDE (test accuracy collapses to 0.51). We did NOT verify the TRAINABILITY SIDE — we did not compute gradient variance of any variational quantity, because the paper's central experiment (kernel SVC) has no trainable quantum parameters. The paper's connection to *variational-circuit* barren plateaus is by analogy, and we neither confirm nor refute that analogy.

## 5. LLM judge weakness

Single judge (Argo GPT-5.2). Argo Opus 4.7 threw a validation error on the same prompt. A robust replication would run 3+ judges (Opus, GPT-5.2, Gemini-2.5-pro via aggregator) and require majority agreement. Given the numerical strength of the reproduction (0.510 ± 0.052 collapse vs. 0.820 optimum vs. 0.875 classical), single-judge is adequate but not ideal.

## 6. What would flip the verdict to PARTIAL / NO-GO

- **PARTIAL** if: a broader qubit-scaling test (n ∈ {4, 8, 12}) at optimized λ shows accuracy is FLAT or DECREASING with n on any real dataset — meaning the bandwidth trick fixes the mechanism but not the scaling.
- **NO-GO** if: on the paper's own Fashion-MNIST-PCA setup, the non-monotone accuracy-vs-λ shape does NOT appear — meaning make_moons was a lucky choice and the effect is dataset-specific.

Neither of these has been tested here. Current verdict = REPLICATED reflects that (i) what we DID test reproduces cleanly and (ii) the paper's mechanism is the most-checkable and most-load-bearing claim, but the reader should understand this is a *mechanism-level* replication, not a *practical-utility* replication.

## 7. Compute budget for a stronger replication

To upgrade REPLICATED → REPLICATED-WITH-SCALING would require:
- n ∈ {4, 8, 12} bandwidth sweeps: ~20 hr GPU (statevector at 12q is O(2^12) memory but O(N^2 · 2^12) for kernel).
- Fashion-MNIST-PCA + KMNIST-PCA + PLASTiCC-PCA, each with 200-500 samples: ~50 hr GPU total.
- 20 seeds: 4× the above.

Not done here (small-sim replication project scope). Reasonable follow-up if uicgpu A100s free up.

## 8. Bottom line

The **mechanism** replicates. The **scaling extrapolation** and **paper-dataset breadth** were not exercised. Verdict REPLICATED is honest given the scope; readers concerned with quantum utility rather than mechanism should treat this as PARTIAL evidence for the paper's practical claims.
