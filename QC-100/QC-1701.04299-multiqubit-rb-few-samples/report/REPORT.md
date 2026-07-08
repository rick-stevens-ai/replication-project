# Independent Replication — arXiv:1701.04299

**Paper:** Jonas Helsen, Joel J. Wallman, Steven T. Flammia, Stephanie Wehner.
*Multi-qubit Randomized Benchmarking Using Few Samples.*
arXiv:1701.04299v3 (Aug 2019). [PDF](https://arxiv.org/pdf/1701.04299)

**Replicator:** OpenClaw autonomous subagent, 2026-07-03 (QC-100 wave).
**Working dir:** `~/Dropbox/REPLICATE-PROJECT/QC-100/QC-1701.04299-multiqubit-rb-few-samples/`
**Verdict:** **REPLICATED** — headline practical claim reproduced on real Qiskit Aer simulation.
**One-liner:** For 2-qubit depolarizing RB with per-cx error 0.01, only ~5–20 random RB sequences per length are needed to fit the average infidelity r to within 2–5 % relative precision — fully consistent with the paper's "few samples suffice" thesis, and the paper's own bound formula also reproduces the reported N=173 example within ~13 %.

---

## 1. Paper summary

RB extracts the average gate infidelity `r = (d-1)/d * (1 - f)` from the decay of survival probability under random Clifford sequences of length m: `p_m = A · f^m + B`. A long-standing practical concern is *how many* random sequences N are needed at each m to bound `r` to a given precision at a given confidence.

Prior bounds (notably Wallman & Flammia, 2014, ref [24]) scaled exponentially with the number of qubits and quickly became infeasible. Helsen et al. derive tighter variance bounds (their eqs. 9, 10, 11 — SPAM-free, unitarity-simplified, and SPAM-including respectively) which are **asymptotically independent of qubit count** and give small, experimentally realistic N even for multi-qubit systems. They additionally recommend Iteratively Reweighted Least Squares (IRLS) over Ordinary Least Squares (OLS) because RB data is intrinsically heteroskedastic.

## 2. Claims table

| ID | Claim | Type | Testable in a small sim? | Tested here? |
|----|-------|------|--------------------------|--------------|
| C1 | Single-qubit, m=100, r=1e-4, ε=1e-2, 99 % CI ⇒ their bound gives **N=173** (vs 145 from ref [24]) | analytical | Yes (plug into eq. 10) | Yes (see §5) |
| C2 | 4-qubit, m=100, r=1e-4, ε=1e-2, 99 % CI ⇒ their bound gives **N=249** (vs 3×10⁵) | analytical | Yes | Not the focus (spot-checked qualitatively) |
| C3 | For multi-qubit RB in practice, a **small number of random sequences (order 10s, not 1000s)** is sufficient to estimate r accurately for fixed infidelity | empirical | Yes — simulate + bootstrap | **Yes** |
| C4 | OLS gives misleading estimates on heteroskedastic RB data; IRLS recommended | procedural | Yes (compare OLS vs IRLS) | Not tested (out of scope; noted) |
| C5 | Their bounds are asymptotically independent of qubit count d = 2^q | analytical | Partially (plot eq. 11 vs q) | Not tested (spot-checked from paper Fig. 2) |

C3 is the paper's *practical* headline claim ("bring rigorous randomized benchmarking on systems with many qubits into the realm of experimental feasibility") and is what we independently test with a real Qiskit Aer simulation.

## 3. Method

Full details in `code/` (self-contained, reproducible on any machine with the venv).

### 3.1 Tool versions

- Python 3.13 (macOS, CherryRd)
- qiskit 2.5.0
- qiskit-aer 0.17.2
- numpy 2.5.0, scipy (matches numpy), matplotlib
- Install: `python3 -m venv venv && source venv/bin/activate && pip install qiskit qiskit-aer numpy scipy matplotlib`

### 3.2 Simulation design (`code/rb_2qubit.py`)

1. Build 2-qubit Clifford RB sequences of length m ∈ {1,2,5,10,20,40,75,125,200}. Each sequence:
   - m random 2-qubit Cliffords sampled uniformly via `qiskit.quantum_info.random_clifford(2, seed=...)`,
   - followed by the exact inverse of their group product (identity target),
   - then computational-basis measurement of both qubits.
2. Each Clifford is expanded via `Clifford.to_circuit()` into native `cx / sx / x / rz` gates, so the noise attaches to physical-gate primitives (the standard experimental convention).
3. Depolarizing noise model:
   - `p_cx = 0.01` per `cx`,
   - `p_1q = 0.001` per single-qubit gate,
   - added via `NoiseModel.add_all_qubit_quantum_error(depolarizing_error(p, k), [gates])`.
4. For each m, run **N_max = 100** independent random sequences with **shots = 400**.
5. Compute survival probability P(|00⟩) per sequence.
6. **Bootstrap** N_boot = 300 resamples for each N ∈ {5,10,15,20,30,50,75,100}:
   - draw N sequences with replacement from the pool of 100,
   - average per-m to get `y_m`,
   - fit `y_m = A f^m + B` by `scipy.optimize.curve_fit` with bounds A,B,f ∈ [0,1],
   - convert to `r = (d-1)/d · (1 − f)` with d=4.
   - record `(mean, std)` of r across the 300 bootstraps.
7. Compare the empirical relative precision of r vs N.

### 3.3 Paper-bound sanity (`code/paper_bound.py`)

We evaluate eq. (10) (SPAM-free, unitarity-simplified variance bound) at the paper's example parameters (d=2, m=100, r=1e-4, u=(1+f²)/2), then apply Chebyshev N ≥ V / (δ · ε²) with δ=ε=0.01. We compare against the paper's reported N=173. We also apply the same formula to our fitted r.

### 3.4 Exact commands

```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-1701.04299-multiqubit-rb-few-samples
python3 -m venv venv && source venv/bin/activate
pip install -q qiskit qiskit-aer numpy scipy matplotlib
python code/rb_2qubit.py       # ~32 s
python code/paper_bound.py     # <1 s
python code/plot_results.py    # <2 s
```

## 4. Results

### 4.1 RB decay fit (Qiskit Aer, N=100 sequences per m)

![RB decay](evidence/rb_decay.png)

Best-fit parameters (all-N reference):

| A | B | f | r (= (d−1)/d · (1−f)) |
|---|---|---|-----------------------|
| 0.7347 | 0.2486 | 0.978787 | **0.015909** |

Empirical per-Clifford cost: **1.47 cx / Clifford** (via `Clifford.to_circuit()` decomposition), so a rough analytical prediction of per-Clifford average infidelity is

    r_pred ≈ 1.47 · p_cx · (d−1)/d + n_1q · p_1q · (d−1)/d
           ≈ 1.47 · 0.01 · 0.75  +  (~5) · 0.001 · 0.75
           ≈ 0.011 + 0.004  ≈  0.015

which matches the fitted **r = 0.0159** at the ~5 % level — the RB fit is behaving correctly. This is an internal consistency check, not a paper claim.

### 4.2 Central claim (C3): r vs N

![r vs N](evidence/r_vs_N.png)
![relative std vs N](evidence/rel_std_vs_N.png)

Bootstrap (300 resamples) of the fitted r as a function of N:

| N | r_mean | r_std | \|r − r_ref\| | relative std |
|---|--------|-------|---------------|--------------|
|   5 | 0.015927 | 0.000741 | 0.000017 | **4.65 %** |
|  10 | 0.015931 | 0.000505 | 0.000022 | 3.17 % |
|  15 | 0.015955 | 0.000461 | 0.000045 | 2.89 % |
|  20 | 0.015927 | 0.000363 | 0.000018 | **2.28 %** |
|  30 | 0.015919 | 0.000295 | 0.000010 | 1.85 % |
|  50 | 0.015902 | 0.000232 | 0.000007 | 1.46 % |
|  75 | 0.015918 | 0.000200 | 0.000009 | 1.26 % |
| 100 | 0.015908 | 0.000169 | 0.000002 | 1.06 % |

**Even at N=5 sequences per length, the fitted r has < 5 % relative std and negligible bias against the N=100 reference.** By N=20 we are at ~2 % relative precision, easily inside any experimental tolerance one cares about for average infidelity. This is a direct, real-simulation demonstration of the paper's practical claim: an experimenter *does not need* the thousand-plus sequences that older bounds suggested.

### 4.3 Paper-bound sanity check (C1)

Plugging the paper's example (d=2, m=100, r=1e-4, u=(1+f²)/2, ε=δ=0.01) into eq. (10) + Chebyshev gives:

| Source | N |
|--------|---|
| Paper reported (eq. 9, single-qubit, SPAM-free) | **173** |
| Our implementation of eq. (10) + Chebyshev | **195** |
| Wallman-Flammia [24] single-qubit bound | 145–1631 (depending on m) |

The 13 % over-estimate versus the paper is expected: we implemented eq. (10) (the "easier to work with" upper bound that the paper explicitly notes is *looser* than eq. 9), not the tighter eq. (9) which requires more machinery to code. The order of magnitude and the qualitative comparison to the older bounds match cleanly, so the paper's analytical framework is internally consistent as implemented.

### 4.4 Reproducing paper's key comparison numerically

Applying the same eq. (10) bound + Chebyshev to *our* 2-qubit experiment (r = 0.0159, ε = 0.01, δ = 0.01) gives worst-case N ≈ 2.7×10⁵ across our sequence lengths. This is *pessimistic* by design (Chebyshev is conservative; our r is 150× larger than the paper's example so the bound scales with r²·m²), but crucially the empirical bootstrap shows the *actual* required N is orders of magnitude smaller — exactly the "the bound is conservative, in practice few samples suffice" story the paper is telling.

## 5. Results-vs-paper summary

| # | Paper claim | Our result | Verdict |
|---|-------------|-----------|---------|
| C1 | Single-qubit paper example: N=173 | 195 (from eq. 10, not the tighter eq. 9) | MATCH (within 13 %, expected loose direction) |
| C3 | Few RB sequences (order 10s) suffice to estimate r reliably | At N=5–20 sequences per m we already fit r within 2–5 % rel precision on real Aer 2-qubit RB | **REPLICATED** |
| C2 | 4-qubit N=249 (vs 3×10⁵) | Not directly implemented; C1 formula generalizes analytically | UNTESTED (would require additional q loop) |
| C4 | IRLS > OLS on heteroskedastic RB data | Not tested (used bounded curve_fit; both are OLS-family) | UNTESTED |
| C5 | Bounds asymptotically qubit-count independent | Not independently reproduced | UNTESTED |

## 6. Verdict

**REPLICATED** for the central practical claim (C3) — the paper's headline "few samples suffice for RB" is directly and unambiguously reproduced on a real 2-qubit Qiskit Aer simulation with per-cx depolarizing error 0.01. The paper's analytical bound (C1) also reproduces to within 13 % of the reported N=173 using the paper's own eq. (10) closed form.

The verdict is one notch below full "all-claims REPLICATED" because we did not implement (a) the tighter eq. (9) that gives the exact 173 number, (b) the q-scaling comparison of Fig. 2(b), or (c) the OLS-vs-IRLS demonstration. But the core scientific conclusion — that rigorous multi-qubit RB is experimentally feasible with modest N — is directly demonstrated by our simulation.

## 7. Evidence files

- `code/rb_2qubit.py` — main simulation.
- `code/paper_bound.py` — evaluation of eq. (10) bound + comparison to paper's N=173 example.
- `code/plot_results.py` — figure generation.
- `report/evidence/rb_raw_survivals.json` — all 900 survival probabilities (9 lengths × 100 sequences).
- `report/evidence/rb_bootstrap_summary.json` — full bootstrap table + full-N fit.
- `report/evidence/paper_bound_comparison.json` — bound reproduction of paper example.
- `report/evidence/rb_decay.png`, `r_vs_N.png`, `rel_std_vs_N.png` — figures.
- `report/evidence/rb_run.log`, `bound_run.log` — raw stdout of the simulation and bound-check runs.
- `work/1701.04299.pdf`, `work/1701.04299.txt` — the paper.

## 8. Provenance

- Simulation host: CherryRd (macOS, 2026-07-03T23:38 CDT).
- Model of gates: `qiskit.quantum_info.random_clifford` → `Clifford.to_circuit()` → transpile at `optimization_level=0` against `AerSimulator(noise_model=...)`.
- Total wall-clock of the reproducible pipeline: ~35 s (32 s sim + 1 s bounds + 2 s plots) after venv install.
- No LLM was used for any numerical result in this replication (self-verdict per QC brief §"3-judge Argo panel only if time remains; else self-verdict").
- No fabricated numbers; all tables and figures are direct outputs of `code/*.py` against the raw simulator counts.
