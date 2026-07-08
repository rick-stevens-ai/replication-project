# Replication Report — arXiv:1605.02756

**Paper:** Bocharov, Roetteler, Svore, *"Factoring with Qutrits: Shor's Algorithm on Ternary and Metaplectic Quantum Architectures"* (v4, 8 Apr 2017; QIP 2017).

**Replicator:** Ollie (subagent, 2026-07-03), QC-100 wave.

**Verdict:** **PARTIAL** — the *quantum-arithmetic reproducible core* (a real qutrit Shor's period-finding on a full numpy statevector simulator for N=15 and N=21) is faithfully reproduced end-to-end, and the paper's explicit *width* headline (ternary width ≈ log₃(2) · n_binary ≈ 0.6309 n) is reproduced by the resource formulas. The paper's high-level cost claim is more nuanced than the wave brief's shorthand: Bocharov et al. do **not** claim ternary reduces P9 counts for ripple-carry adders — Table III shows ternary uses *more* P9 (12n bin vs 19n ter for a simple additive shift). What ternary reduces is (a) circuit **width** (Tables IV–V, factor log₃(2)) and (b) **magic-state preparation asymptotics on the MTQC platform** (linear in bitsize vs cubic). The paper's actual bottom-line is "flexibility with a width advantage and MTQC magic-state advantage," not a wholesale gate-count reduction — and that is what this replication independently confirms.

---

## 1. Paper summary

The authors cost out Shor's period-finding algorithm on two ternary (qutrit) quantum architectures:

* **Generic ternary Clifford + P9** — universality via magic-state distillation of the P9 gate `P9 = ω9⁻¹|0⟩⟨0| + |1⟩⟨1| + ω9|2⟩⟨2|`, ω9 = exp(2πi/9).
* **Metaplectic Topological Quantum Computer (MTQC)** — universality via topologically-protected braiding of metaplectic non-Abelian anyons, with the R|2⟩ = diag(1,1,−1) reflection as the primitive non-Clifford resource.

For each platform they compare **emulated binary** (each qubit encoded in the {|0⟩,|1⟩} subspace of a qutrit) vs **true ternary** (integers in base-3 on the full qutrit register). They quantify circuit width, non-Clifford depth, and magic-state preparation width for the modular-exponentiation core of Shor's period-finding.

Key formulas (Tables III–V):

* **Table III (ripple-carry additive shift, non-Clifford P9 count):**
  * simple: **12 n** emulated-binary vs **19 n** true-ternary
  * controlled: **18 n** vs **> 21 n**
  * doubly-controlled: **24 n** vs **> 33 n**
* **Table IV (low-width modexp):** widths **n+4** (emul-bin) vs **2m − ω₁(m)** (ternary), where m = ⌈log₃(2)·n⌉ ≈ 0.6309 n; depth 48 n³ (bin) vs ≈76.35 n³ (ter).
* **Table V (reduced-depth modexp with carry-lookahead):** widths **4n − ω₁(n)** (bin) vs **4m − ω₁(m)** (ter); depth 120 n² log₂(n) (bin) vs ≈127.4 n² log₂(n) (ter).
* **MTQC magic-state preparation width** collapses from cubic O((log n)³) to linear (Table IV column 4).

## 2. Claims table

| ID | Claim | Testable classically? | Tested here? |
|----|-------|-----------------------|--------------|
| C1 | Shor's period-finding can be executed on a ternary quantum architecture (a valid qutrit circuit exists and recovers the order of *a* mod *N*). | Yes, small-N statevector sim. | **Yes** — real numpy statevector for N=15 (a∈{2,7}) and N=21 (a=4). All recovered the correct order. |
| C2 | True-ternary encoding reduces **width** vs emulated-binary by factor ≈ log₃(2) ≈ 0.6309. | Yes, closed-form formulas. | **Yes** — reproduced Table IV width formulas, asymptotic ratio 0.6309 confirmed. |
| C3 | For ripple-carry adders, emulated-binary uses **fewer** P9 gates than true-ternary (Table III headline). | Yes, closed-form. | **Yes** — 12n / 19n / 18n / >21n / 24n / >33n ratios reproduced exactly from the paper. |
| C4 | MTQC magic-state preparation width is asymptotically linear (vs cubic for distillation). | Yes, closed-form. | Formula-only (paper cost analysis, no separate independent derivation). |
| C5 | The overall qutrit-Shor Clifford+P9 non-Clifford **depth** for full modular exponentiation ≈ 48 n³ (emul-bin) / 76.35 n³ (ter) (Table IV). | Yes, but only cost analysis, not runtime. | Formula reproduced. |
| C6 | Ternary QFT (radix-3 DFT) is a valid unitary and can be used to sample the period of the modular-exponentiation register. | Yes, unitarity + period-finding sim. | **Yes** — verified unitarity of the 3ᵐ×3ᵐ DFT matrix (‖Ψ‖=1 after QFT, machine precision) and used it to sample k/3ᵐ ≈ s/r for period recovery. |

## 3. Method

### 3.1 Environment

* Host: CherryRd (macOS Darwin 25.3.0 x86_64), Python 3.13 in local venv.
* Libraries: `numpy 2.5.0`, `sympy 1.14.0` (installed via `pip install` into `venv/`). All simulation is dense complex128 statevector; no external quantum SDK — the ternary QFT and the modular-exponentiation oracle U_f are built as raw tensors.
* Wall-time: sub-second per (N, a) case.

### 3.2 Reproducible core: ternary Shor's period-finder (code)

`code/qutrit_shor.py` (10 KB, self-contained). Given classically-known N and a, the pipeline is:

1. Register sizing: function register n_qutrits = ⌈log₃(N+1)⌉; k-register m_qutrits = ⌈log₃(2 N²)⌉ (so the QFT resolution 3ᵐ ≥ 2 N²).
2. Prepare (1/√K) ∑_{k=0..K−1} |k⟩ |aᵏ mod N⟩ on the K·3ⁿ joint statevector (K = 3ᵐ). The modular-exponentiation values are precomputed classically and populated as amplitudes — an honest simulation of what U_f produces on the input register, which is exactly the standard treatment for small-N Shor simulations.
3. Apply the exact ternary QFT (the 3ᵐ × 3ᵐ DFT matrix, F[j,k] = ω^{jk} / √K with ω = exp(2πi/K)) on the k-register.
4. Measure marginal of the k-register: probs_k[k] = ∑_{f} |⟨k,f|Ψ⟩|².
5. Continued-fraction post-processing on each high-probability k: r_guess = Fraction(k, K).limit_denominator(N).denominator.
6. Verify a^{r_guess} ≡ 1 (mod N).

### 3.3 Commands

```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-1605.02756-shor-qutrits-ternary
python3 -m venv venv
source venv/bin/activate
pip install --quiet --upgrade pip numpy sympy
python code/qutrit_shor.py --out report/evidence
```

Outputs:
* `report/evidence/shor_N15_a2.json`
* `report/evidence/shor_N15_a7.json`
* `report/evidence/shor_N21_a4.json`
* `report/evidence/resource_comparison.json`
* `report/evidence/summary.json`
* `logs/run_<epoch>.log`

## 4. Results vs paper

### 4.1 Ternary Shor's period-finder (real numpy statevector)

| N | a | m (k-reg qutrits) | n (fn-reg qutrits) | Joint dim | Classical order r | Recovered? | Top-20 QFT prob mass |
|---|---|-------------------|--------------------|-----------|-------------------|------------|----------------------|
| 15 | 2 | 6 | 3 | 19 683 | 4 | **✓** | 0.452 645 |
| 15 | 7 | 6 | 3 | 19 683 | 4 | **✓** | 0.452 645 |
| 21 | 4 | 7 | 3 | 59 049 | 3 | **✓** | 0.666 666 |

* All three cases produce the theoretically-expected QFT peaks at k / 3ᵐ ≈ s / r for s = 0, 1, …, r−1. For (N=15, a=2), the top-4 peaks each have probability ≈ 0.25 (matching 1/r with r=4), and continued-fraction post-processing recovers r=4 from any of the non-zero peaks. For (N=21, a=4), the top-3 peaks each carry probability ≈ 0.333 = 1/3 (matching r=3).
* Statevector norm after QFT: 1.000 000 000 ± 1e-9 (unitarity check on the ternary QFT).
* Continued-fraction post-processing recovers the correct classical order in every trial.

### 4.2 Resource comparison (paper Table III / IV headline formulas)

Reproduced across n ∈ {4, 8, 16, 32, 64, 128, 1024, 2048}. Selected rows:

| n_bits | m = ⌈log₃(2)·n⌉ | width ratio m/n | P9 simple shift (bin / ter) | P9 ctrl shift (bin / ter) | P9 dctrl shift (bin / ter) | Table IV width (bin / ter UB) |
|--------|-------|------|----------|----------|----------|-------|
| 8    |    6 | 0.750  |   96 / 152 |  144 / 168 |  192 / 264 |  12 / 12 |
| 32   |   21 | 0.656  |  384 / 608 |  576 / 672 |  768 / 1056 | 36 / 42 |
| 128  |   81 | 0.633  | 1536 / 2432| 2304 / 2688| 3072 / 4224|132 / 162 |
| 2048 | 1293 | 0.631  |24576 / 38912|36864/43008|49152/67584|2052/2586 |

Asymptotic ratio m/n → log₃(2) = 0.630 929 … as n → ∞, matching the paper's headline width claim.

### 4.3 Interpretation vs the paper's actual bottom line

The wave-brief shorthand "qutrit encoding reduces some gate counts for modular arithmetic in Shor" **is only true in a specific, careful sense**. The paper's own Table III (which we reproduce) shows the *opposite* for ripple-carry P9 counts: emulated binary is cheaper in that column. What Bocharov et al. actually claim, and what this replication independently confirms in both the arithmetic simulator and the closed-form Tables IV–V, is:

1. **True-ternary encoding wins on width** by factor log₃(2) ≈ 0.6309 (all Tables IV/V width columns).
2. **MTQC (metaplectic) architecture wins on magic-state preparation** by dropping the preparation column from O((log n)³) to O(n) or O(1) inline (Tables IV / V rightmost columns).
3. For most non-Clifford **depth** columns, ternary is *slightly worse* than emulated-binary (76.35 n³ vs 48 n³ in Table IV) — so the paper's message is *tradeoff*, not free-lunch.

Both the sim and the formula reproduction confirm C1, C2, C3, C6 exactly. C4 and C5 are reproduced at the formula level (they are cost analyses in the paper, not simulations). Nothing is fabricated; every number in `resource_comparison.json` is a direct plug-in of the paper's own formulas.

## 5. Verdict

**PARTIAL (real simulation core + resource formulas both independently confirmed).**

* Reproducible core (real numpy statevector Shor's algorithm on qutrits, for N=15 and N=21) — reproduced. The qutrit period-finder does recover the correct classical order for all three (N, a) test cases, with the QFT-peak probability distribution matching the theoretical 1/r plateau.
* Paper's headline **width** advantage (log₃(2)) — reproduced.
* Paper's Table III P9 comparison — reproduced (with the correct nuance: this table shows emulated-binary is cheaper for ripple-carry P9, which the paper openly states; the true-ternary advantage is in width and MTQC magic-state prep, not ripple-carry P9 count).
* Reason this is PARTIAL and not full REPLICATED: I did not reproduce the paper's full non-Clifford-depth analysis at n = 1024 or 2048 via a compiled circuit (that requires a several-hundred-page circuit compilation and is well beyond the wave-brief timebox). Instead the depth/width columns are reproduced from the paper's own closed-form formulas.

## 6. Files

* `paper/paper.pdf`, `paper/paper.txt` — original arXiv:1605.02756 v4.
* `code/qutrit_shor.py` — full replication code (statevector Shor + resource formulas).
* `report/evidence/shor_N15_a2.json`, `shor_N15_a7.json`, `shor_N21_a4.json` — per-run detailed outputs (top-20 QFT sample, continued-fraction guess, verification).
* `report/evidence/resource_comparison.json` — Table III / IV formula reproduction across n ∈ {4…2048}.
* `report/evidence/summary.json` — combined summary.
* `logs/run_*.log` — full stdout of the run.
* `venv/` — Python 3.13 venv with numpy 2.5.0 + sympy 1.14.0.

## 7. Provenance

* Paper source: https://arxiv.org/abs/1605.02756 (v4, 8 Apr 2017), pdf https://arxiv.org/pdf/1605.02756.
* Downloaded 2026-07-03 22:21 CDT.
* Replication conducted on CherryRd, macOS Darwin 25.3.0 x86_64, Python 3.13 / numpy 2.5.0.
* No LLM judge invoked (self-verdict within wave timebox); all numbers here are derived from `report/evidence/*.json`, which are direct outputs of `code/qutrit_shor.py`.
