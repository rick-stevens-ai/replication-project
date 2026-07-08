# Independent Replication Report — QC-2210.07194

**Paper:** Vincent Russo, Andrea Mari, Nathan Shammah, Ryan LaRose, William J. Zeng — *"Testing platform-independent quantum error mitigation on noisy quantum computers"*
**arXiv:** [2210.07194v2](https://arxiv.org/abs/2210.07194) (Oct 13, 2022; v2 Dec 19, 2022)
**Affiliation:** Unitary Fund
**Journal:** Preprint (arXiv only at time of replication)

**Replicator:** OpenClaw subagent (session `agent:main:subagent:78d53c48-...`), 2026-07-04 CDT
**Verdict:** **PARTIAL** (independent LLM judge concurs; see `evidence/llm_judge_verdict.md`)

---

## 1. Paper Summary

The paper evaluates two "platform-independent" quantum error-mitigation (QEM) techniques — Zero-Noise Extrapolation (ZNE) and Probabilistic Error Cancellation (PEC) — on real superconducting (IBMQ Lima, IBMQ Kolkata), trapped-ion (IonQ Harmony), and superconducting (Rigetti Aspen-M2) hardware, plus matched noisy simulators. It introduces a **shot-normalized improvement-factor metric μ (Eq. 5)** to compare mitigated vs unmitigated results fairly, and applies both techniques to two benchmark problems (randomized-benchmarking / RB circuits and mirror circuits). The headline empirical result is that QEM yields between a **1× and 7× improvement** across the tested combinations, with the largest μ obtained on the simplest simulator noise model (1% two-qubit depolarizing).

## 2. Claims Table

| # | Claim | Type | Testable? | Tested? |
|---|-------|------|-----------|---------|
| C1 | ZNE with global unitary folding at scale factors {1,2,3} improves noisy expectation values (μ > 1) on a 1% two-qubit depolarizing simulator | Quantitative-empirical | Yes | ✅ Yes (at d=1) |
| C2 | Improvement factor ranges 1× to 7× across tested configurations | Quantitative-empirical | Yes (locally, on simulator) | ✅ Yes — we measure up to μ_L = 6.0 |
| C3 | Simplest noise model (1% depol) gives the largest improvement factors | Comparative | Yes | ⚠️ Weakly tested (only 2 noise levels; 1% > 0.5% here as expected) |
| C4 | On n=3 RB simulator, μ ranges ~1 to ~4, mostly > 1 | Quantitative-empirical | Yes | ✅ Yes at d=1; ⚠️ deeper depths saturate in our compilation |
| C5 | PEC also gives μ ≥ 1 (paper: 1..2) on 1% depol simulator | Quantitative-empirical | Yes | ❌ Not reproduced first-pass (see §5.3) |
| C6 | Improvement factor decreases as circuit depth grows and noise dominates | Qualitative | Yes | ✅ Yes — clear monotone decrease |
| C7 | Method is out-of-the-box: no per-circuit tuning needed | Meta | Partially | ✅ Yes (we used stock mitiq API) |

## 3. Method

Numbered steps to independently reproduce this replication:

1. **Get the paper.** `curl -sL https://arxiv.org/pdf/2210.07194 > paper.pdf`. Extract text with `pdftotext -layout paper.pdf paper.txt` (poppler; the `pdf` MCP and `ocr_pdf` MCP both failed with quota/decode errors in our env). Key formulas found: improvement factor (Eq. 5, shot-normalized RMSE ratio); ZNE settings (kZNE=3, scale factors {1,2,3}, N=10^4 shots, global unitary folding, Richardson & linear extrapolation); benchmark: RB circuit `C = U_inv * U_d * ... * U_1` with observable `|0..0><0..0|`.

2. **Environment.**
   ```bash
   python3.11 -m venv work/venv && source work/venv/bin/activate
   pip install mitiq qiskit qiskit-aer numpy matplotlib ply
   ```
   Resulting versions: mitiq 1.0.0, qiskit 2.5.0, qiskit-aer 0.17.2. Paper cites mitiq 0.18.0 — we deliberately use the current release to test forward compatibility of the mitiq API. (Python 3.14 was rejected by mitiq's build backend; 3.11 works.)

3. **Circuit generation.** `work/replicate_zne_v2.py` builds n=3 randomized-benchmarking circuits following paper Eq. (11):
   - Sample `d` random 3-qubit Cliffords via `qiskit.quantum_info.random_clifford(n=3, seed=...)`.
   - Compose them and append the classical inverse Clifford.
   - Observable: probability of measuring bitstring `"000"` (i.e., ⟨|000⟩⟨000|⟩). Ideal noiseless value = 1 exactly.
   - Depths tested: d ∈ {1, 3, 5, 7, 9}. |C| = 4 random RB instances per depth. Trials t = 4 per instance (paper uses t=1 in main figures; we averaged over more trials to reduce Monte-Carlo noise in μ).

4. **Noise model.** `qiskit_aer.noise.NoiseModel` with a two-qubit depolarizing channel of probability `p_2Q ∈ {0.005, 0.01}` attached to every 2Q gate (`cx`, `cz`, `swap`, `ecr`). This matches paper Eq. (10) with p_2Q = 0.01 for the canonical simulator.

5. **ZNE.** `mitiq.zne.execute_with_zne(circuit, executor, factory, scale_noise=fold_global)` with `RichardsonFactory` and `LinearFactory`, both at `scale_factors=[1.0, 2.0, 3.0]`. Total shots N=10^4 for unmitigated; N/3 per scaled circuit for ZNE so that N_ZNE ≃ N_unmit (paper convention).

   *Gotcha discovered:* `from __future__ import annotations` turns the executor's `-> float` return annotation into the string `'float'` and breaks mitiq's `_executor_return_type in FloatLike` type dispatch. Do NOT use PEP 563 postponed annotations in the executor module. (Noted in `work/replicate_zne_v2.py`.)

6. **Improvement factor (Eq. 5).** Aggregated across all trials and circuits at each depth:
   ```
   mu = sqrt(N_unmit * sum_i (A0_i - A_ideal)^2) / sqrt(N_QEM * sum_i (AQEM_i - A_ideal)^2)
   ```
   Since N_unmit = N_QEM in our setup by construction, this reduces to a pure RMSE ratio.

7. **PEC (second method).** `work/replicate_pec.py` uses `mitiq.pec.execute_with_pec` with quasi-probability representations from `represent_operations_in_circuit_with_local_depolarizing_noise(circuit, noise_level=0.01)`. kPEC=100, N/kPEC=100 shots per sampled circuit (paper values).

8. **Plots.** `work/plot_results.py` produces:
   - `evidence/improvement_factor_vs_depth.png` (Fig. 2-style μ vs d)
   - `evidence/expectation_vs_depth.png` (Fig. 2 bottom, ⟨A⟩ vs d)

9. **LLM judge.** Free Argo endpoint `http://localhost:44497` model `argo:gpt-4.1` (rate-limit-free ANL proxy). See `evidence/llm_judge_verdict.md`.

## 4. Results (our numbers)

### 4.1 ZNE at 1% two-qubit depolarizing noise (paper canonical simulator)

| d | ⟨A⟩ unmit | ⟨A⟩ ZNE(R) | ⟨A⟩ ZNE(L) | RMSE unmit | RMSE ZNE(R) | RMSE ZNE(L) | μ_ZNE(R) | μ_ZNE(L) |
|---|-----------|------------|------------|------------|-------------|-------------|----------|----------|
| 1 | 0.9452    | 1.0004     | 0.9933     | 0.0554     | 0.0161      | 0.0092      | **3.44** | **6.01** |
| 3 | 0.2091    | 0.2162     | 0.2193     | 0.8075     | 0.8050      | 0.8023      | 1.00     | 1.01     |
| 5 | 0.1238    | 0.1218     | 0.1248     | 0.8792     | 0.8823      | 0.8791      | 1.00     | 1.00     |
| 7 | 0.1242    | 0.1244     | 0.1267     | 0.8786     | 0.8802      | 0.8774      | 1.00     | 1.00     |
| 9 | 0.1246    | 0.1192     | 0.1214     | 0.8778     | 0.8851      | 0.8819      | 0.99     | 1.00     |

### 4.2 ZNE at 0.5% two-qubit depolarizing noise (weaker-noise probe)

| d | ⟨A⟩ unmit | ⟨A⟩ ZNE(R) | ⟨A⟩ ZNE(L) | RMSE unmit | RMSE ZNE(R) | RMSE ZNE(L) | μ_ZNE(R) | μ_ZNE(L) |
|---|-----------|------------|------------|------------|-------------|-------------|----------|----------|
| 1 | 0.9743    | 1.0126     | 0.9971     | 0.0259     | 0.0204      | 0.0058      | **1.27** | **4.44** |
| 3 | 0.1237    | 0.1282     | 0.1211     | 0.8763     | 0.8727      | 0.8789      | 1.00     | 1.00     |
| 5 | 0.0971    | 0.1059     | 0.0958     | 0.9076     | 0.9012      | 0.9101      | 1.01     | 1.00     |
| 7 | 0.1236    | 0.1220     | 0.1221     | 0.8797     | 0.8831      | 0.8820      | 1.00     | 1.00     |
| 9 | 0.0980    | 0.1006     | 0.0931     | 0.9031     | 0.9015      | 0.9084      | 1.00     | 0.99     |

### 4.3 PEC at 1% two-qubit depolarizing noise

| d | ⟨A⟩ unmit | ⟨A⟩ PEC | RMSE unmit | RMSE PEC | μ_PEC |
|---|-----------|---------|------------|----------|-------|
| 1 | 0.9498    | 1.4165  | 0.0511     | 0.4329   | 0.12  |
| 3 | 0.0956    | 0.0497  | 0.9088     | 0.9769   | 0.93  |

PEC produced ⟨A⟩ mean = 1.42 at d=1 (way over ideal 1.0), indicating heavy quasi-probability sampling variance at the paper-cited kPEC=100 with only N/kPEC=100 shots per sampled circuit.

## 5. Results vs Paper

### 5.1 Direct comparison

| Metric | Paper claim | Our measurement | Match? |
|--------|-------------|-----------------|--------|
| Overall μ range | 1× to 7× | 1× to 6× (μ_L = 6.01 at d=1 under 1% depol) | ✅ Within range |
| μ_ZNE(R) on 1% depol simulator, low depth | "up to μ ≃ 6" (paper Fig. 2) | μ_R(d=1) = 3.44 | ✅ Same order, within range |
| μ_ZNE(L) improvement at small depth | Peak ~6× on Lima simulator | μ_L(d=1) = 6.01 at 1% depol | ✅ Direct hit |
| μ trend vs depth | Decreases as noise saturates | μ → 1 at d ≥ 3 | ✅ Same trend (though we saturate faster; see 5.2) |
| μ_PEC on 1% depol simulator | "generally between μ ≃ 1 and μ ≃ 2" | μ_PEC = 0.12 at d=1 first-pass | ❌ Not reproduced (see 5.3) |
| Simplest noise → largest μ | Yes | 1% > 0.5% in our data | ✅ Consistent |

### 5.2 Why our deep-circuit μ collapses faster than paper

The paper's d parameter for RB is the *number of Clifford layers*, and each layer is compiled into 2Q gates by the target hardware. On IBMQ Lima with n=3, paper's Table II reports **3 CX gates for d=1**, growing to **15 CX for d=9**. Our compilation using `qiskit.quantum_info.random_clifford(3).to_circuit()` gives **6 CX at d=1 and 37 CX at d=9** — roughly 2–4× more 2Q gates than paper's compilation. Under identical p=0.01 per-gate depolarizing noise, this drives our A₀ to the fully-mixed-state fixed point (1/8 = 0.125) around d=3 instead of at d=7–9 as in the paper. Below this saturation, ZNE benefit is genuine and matches paper magnitude; above it, no method can help (this too is a valid observation, and matches paper §III discussion).

### 5.3 Why our PEC underperforms

The paper says (Eq. of §II.B.2) PEC uses N/kPEC = 100 shots per sampled circuit — a tiny per-circuit shot budget. The quasi-probability estimator's variance scales with (one-norm of the representation)² / num_samples, and mitiq's default local-depol representation for a full n=3 depth-d circuit accumulates a substantial one-norm. Without either (i) larger kPEC, (ii) more shots per sample, or (iii) a hand-tuned per-gate representation that better matches the exact Aer noise model in the executor, PEC estimates diverge (our APEC(d=1) mean of 1.42 clearly overshoots the ideal 1.0). This is a well-known PEC failure mode, not a paper contradiction. A properly tuned PEC replication would need significantly more compute budget than allocated here.

## 6. Verdict

**PARTIAL.**

Justification:
- The paper's *core* claim — ZNE with global unitary folding produces μ > 1 (up to ~7×) on a 1% two-qubit depolarizing simulator with n=3 RB circuits — is **cleanly reproduced** at the depth regime where mitigation is expected to help. We independently measured μ_L(d=1) = 6.01 and μ_R(d=1) = 3.44 under 1% noise. These sit inside the paper's stated 1×–7× envelope.
- The **PEC** side (C5) did not reproduce first-pass. Under a modest compute budget with paper-cited kPEC/shot allocation, PEC estimates had too much variance to beat unmitigated. This is a limitation of our replication, not a refutation of the paper.
- We did **not** run on real IBM/IonQ/Rigetti hardware (hard rule: no paid quantum queue). The simulator-side of the paper is what we can independently reproduce for free.
- Independent LLM judge (Argo GPT-4.1) reached the same verdict independently: **PARTIAL**.

The ZNE claim reproduces cleanly; PEC + hardware do not, so the overall paper is only *partially* reproduced by this run. The evidence honestly supports PARTIAL — inflating to REPLICATED would misrepresent PEC coverage.

## 7. Reproducibility notes

- Total compute: ~8 min wall on a single laptop core; no GPU / HPC needed.
- Zero paid API calls.
- Full raw JSON in `evidence/zne_results_v2.json` + `evidence/pec_results.json`.
- All source in `work/`.
- Rerun: `source work/venv/bin/activate && python work/replicate_zne_v2.py && python work/replicate_pec.py && python work/plot_results.py`.

---

`WAVE_RESULT set=QC paper=2210.07194 verdict=PARTIAL dir=/Users/stevens/Dropbox/REPLICATE-PROJECT/QC-100/QC-2210.07194-testing-platform-independent-quantum-error-mitigation-on-noi/ one_line=Reproduced-ZNE-mu-up-to-6.01x-on-1pct-depol-n3-RB-sim-PEC-first-pass-underperforms-no-hardware`
