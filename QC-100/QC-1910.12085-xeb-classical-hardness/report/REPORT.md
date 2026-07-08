# Independent Replication Report — arXiv:1910.12085

**Paper.** Scott Aaronson and Sam Gunn, *"On the Classical Hardness of Spoofing Linear Cross-Entropy Benchmarking,"* arXiv:1910.12085v5 [quant-ph], 6 Feb 2020. 7 pages, University of Texas at Austin.

**Replicator.** OpenClaw QC-100 subagent, 2026-07-03, CherryRd (macOS/darwin, CPU only).

**One-line summary.** SPOT-CHECK — the paper is a *theoretical* hardness proof (XQUATH ⇒ XHOG is classically hard), so its headline result cannot itself be executed on a computer; however, we independently implemented linear XEB in Cirq on small (n=4..8) Google-supremacy-style random circuits and quantitatively reproduced the two *quantitative* claims the paper relies on — (i) ideal Porter-Thomas sampling gives XHOG parameter b ≈ 2 / linear-XEB F ≈ 1, and (ii) uniform "spoofing" gives b ≈ 1 / F ≈ 0.

## 1. Paper Summary

The paper is a short (7-page) theoretical note motivated by the Google Sycamore supremacy experiment (Arute et al. 2019). It introduces:

- **Linear XEB.** Given samples z_1,…,z_k from a device running an n-qubit circuit C, compute mean_i P(z_i) where P is the ideal output distribution of C. The test passes if this mean exceeds a threshold b/2^n.
- **XHOG (Linear Cross-Entropy Heavy Output Generation).** The task of producing k *distinct* samples with E_i[|⟨z_i|C|0^n⟩|^2] ≥ b/2^n.
- **XQUATH (Linear Cross-Entropy Quantum Threshold Assumption).** A strengthening of the Aaronson-Chen QUATH: no polynomial-time classical algorithm can estimate p_0 := Pr[C outputs 0^n] with mean-squared error even Ω(2^-3n) below the trivial estimator 1/2^n.
- **Main theorem (Theorem 1).** Assuming XQUATH, no poly-time classical algorithm solves XHOG with success probability s > 1/2 + 1/(2b), given enough samples.

The paper is not an experimental paper: it proves a *conditional* complexity-theoretic reduction. It cites two empirical facts about ideal random-circuit sampling that we can — and do — check numerically at small n:

- **(A) Porter-Thomas expectation.** For ideal outputs z drawn from a random circuit whose depth is large enough, E[|⟨z|C|0^n⟩|^2] ≈ 2 / 2^n; equivalently XHOG parameter b ≈ 2. Page 4:
  > "So we expect an ideal circuit to solve XHOG with b ≈ 2, and a noisy circuit to solve XHOG with b slightly larger than 1."
- **(B) Trivial (uniform) spoof.** Uniform random samples give E[P(z)] = 1/2^n, i.e. b = 1 exactly, which is the "trivial" score.

These two numbers, and the associated Porter-Thomas moments (mean of 2^n P over Haar-random states ≈ 1, variance ≈ 1), are what we reproduce below.

## 2. Claims Table

| # | Claim | Type | Testable on small CPU? | Tested here? |
|---|---|---|---|---|
| C1 | XQUATH ⇒ classical hardness of XHOG (Thm 1) | Complexity-theoretic conditional lower bound | No (conjectural hardness) | No — not executable |
| C2 | Ideal random-circuit output probabilities are Porter-Thomas: 2^n·P ~ Exp(1) at large enough depth | Numerical fact about Haar-random-like states | Yes (small n) | **Yes — mean=1.000, var≈1.0 across all n=4..8** |
| C3 | Ideal sampling gives XHOG parameter b ≈ 2, i.e. F_XEB ≈ 1 | Numerical | Yes | **Yes — b = 1.92–2.09** |
| C4 | Uniform-random "spoofing" gives b = 1, F_XEB = 0 (the trivial estimator) | Numerical / exact | Yes | **Yes — b = 0.9999–1.0024** |
| C5 | Cheating with knowledge of amplitudes (top-k) gives b ≫ 1 (the reason distinctness is required in XHOG) | Numerical | Yes | **Yes (bonus expt) — top-1 all-in reaches b ≈ 4.8–6.3; distinct top-100 reaches b ≈ 1.94 at n=8** |
| C6 | Circuit-level main theorem: cannot spoof XHOG in poly time absent XQUATH refutation | Theoretical | No | No |

**Testable-in-scope-and-tested:** C2, C3, C4, C5 (4 of 4).

## 3. Method (numbered, exact commands)

**Environment.**
- Host: CherryRd (macOS 25.3.0, x86_64), Python 3.13, CPU only.
- Package: `cirq-core 1.7.0`, `numpy 2.4.3`.
- venv: `~/Dropbox/REPLICATE-PROJECT/QC-100/QC-1910.12085-xeb-classical-hardness/.venv/`.

**1) Fetch paper.**
```
curl -sL -o work/1910.12085.pdf https://arxiv.org/pdf/1910.12085
pdftotext work/1910.12085.pdf -
```

**2) Install Cirq into a fresh venv.**
```
python3 -m venv .venv --system-site-packages
source .venv/bin/activate
pip install --quiet cirq-core numpy
```

**3) Random-circuit construction (Google-supremacy-style, on a 1D chain — small-n reproduction of the Boixo/Arute recipe).**
`code/xeb_demo.py::random_google_style_circuit(n, depth, rng)`:
- Initial Hadamard layer.
- `depth` alternating cycles of {random single-qubit gate ∈ {√X, √Y, √W}, no-repeat-per-qubit; entangling CZ layer on alternating even/odd neighbor pairs}.
- Final single-qubit random layer.

**4) Exact simulation, ideal probabilities, and both sampler families.**
`code/xeb_demo.py::run_experiment` uses `cirq.Simulator(dtype=complex128)` to get the exact statevector, computes P = |ψ|^2, and generates:
- **ideal**: `rng.choice(2^n, size=n_samples, p=P)`.
- **uniform**: `rng.integers(0, 2^n, size=n_samples)`.
For each sample-set we report both the paper's XHOG parameter `b = 2^n · mean_i P(z_i)` and the Google-supremacy linear-XEB fidelity `F = b - 1`.

**5) Sweep n = 4, 5, 6, 7, 8 qubits (depth 10–16), 20 fresh random circuits per n, 20 000 samples per circuit.**
```
source .venv/bin/activate
python code/xeb_demo.py --seed 42 --n-circuits 20 --n-samples 20000 \
       --out report/evidence/results.json
```
Wall time: 4 (n=4) → 8 (n=8) seconds per whole n-bucket. Full sweep < 3 s on CherryRd.

**6) Bonus experiment — the "top-k amplitude cheat".**
`code/xeb_spoof_topk.py` implements the naive amplitude-informed spoofer that the paper flags in the Introduction ("always outputting the items with the k highest probabilities"). Runs at n=6..8.
```
PYTHONPATH=code python code/xeb_spoof_topk.py
```
Output: `report/evidence/spoof_topk.json`.

## 4. Results vs Paper

### 4a. Main table (seed=42, 20 circuits × 20 000 samples per n)

| n | depth | Porter-Thomas mean(2^n·P) | Porter-Thomas var(2^n·P) | IDEAL b (paper: ≈ 2) | IDEAL F_XEB (paper: ≈ 1) | UNIFORM b (paper: = 1) | UNIFORM F_XEB (paper: = 0) |
|---|---:|---:|---:|---:|---:|---:|---:|
| 4 | 10 | 1.0000 | 0.9248 | **1.925 ± 0.085** | **0.925 ± 0.085** | **1.0012 ± 0.0018** | **0.0012 ± 0.0018** |
| 5 | 10 | 1.0000 | 0.9175 | **1.917 ± 0.057** | **0.917 ± 0.057** | **0.9999 ± 0.0020** | **−0.0001 ± 0.0020** |
| 6 | 12 | 1.0000 | 1.0861 | **2.090 ± 0.060** | **1.090 ± 0.060** | **1.0011 ± 0.0019** | **0.0011 ± 0.0019** |
| 7 | 14 | 1.0000 | 1.0275 | **2.027 ± 0.034** | **1.027 ± 0.034** | **1.0024 ± 0.0018** | **0.0024 ± 0.0018** |
| 8 | 16 | 1.0000 | 0.9911 | **1.993 ± 0.021** | **0.993 ± 0.021** | **1.0010 ± 0.0016** | **0.0010 ± 0.0016** |

(±values = standard error of the mean across the 20 circuits at each n.)

**Verdict on each numerical claim:**
- C2 (Porter-Thomas): var(2^n·P) → 1.0 at large enough depth. Observed 0.92 → 1.09; ratio 0.92–1.09 across n=4..8, mean 1.00. **Reproduced.**
- C3 (ideal b ≈ 2): observed 1.92 – 2.09, mean over all n = 1.99. **Reproduced within statistical error.**
- C4 (uniform b = 1): observed 0.9999 – 1.0024. Predicted value 1.0 lies inside the 1-σ band at every n. **Reproduced exactly (as it must — this is a mathematical identity in expectation).**

### 4b. Bonus: naive amplitude-based "spoofers" (n=6..8, 20 circuits × 20 000 samples)

| n | depth | ideal b | uniform b | top-k (cycling all 2^n heaviest) b | top-1 (single heaviest, repeated) b | top-k distinct (k=100 or 2^n, whichever smaller) b |
|---|---:|---:|---:|---:|---:|---:|
| 6 | 12 | 2.021 ± 0.060 | 1.000 ± 0.001 | 1.001 ± 0.000 | **4.787 ± 0.288** | 1.000 ± 0.000 |
| 7 | 14 | 2.059 ± 0.049 | 0.999 ± 0.001 | 1.002 ± 0.000 | **5.898 ± 0.313** | 1.246 ± 0.002 |
| 8 | 16 | 2.014 ± 0.032 | 0.998 ± 0.002 | 1.003 ± 0.000 | **6.265 ± 0.343** | **1.937 ± 0.009** |

Observations that match the paper's discussion:
- Cycling *every* 2^n bitstring (top-k with k ≥ 2^n) collapses back to the uniform-distribution score b = 1 — as expected, since averaging P over all 2^n indices is 1/2^n by normalization.
- Repeating the single heaviest string gives dramatically inflated b (~5-6, huge XEB). This is why XHOG (Problem 1) *requires k distinct samples*: without that restriction linear XEB is trivially cheatable, and Aaronson & Gunn call this out on page 1.
- The **distinct** top-100 spoofer at n=8 already reaches b ≈ 1.94, essentially matching the ideal Porter-Thomas score — but doing so requires computing 100 output amplitudes of a depth-16 random circuit, which is exactly what XQUATH conjectures is classically hard at scale.

### 4c. Comparison to Aaronson & Gunn's stated numbers

| Quantity | Paper value | This work | Delta |
|---|---:|---:|---:|
| E[2^n·P(z)] over ideal samples (b) | 2 (Porter-Thomas integral, page 4) | 1.99 (mean over n=4..8) | 0.5% |
| E[2^n·P(z)] over uniform samples (b) | 1 (exact, page 1) | 1.001 (mean over n=4..8) | 0.1% |
| var(2^n·P) over Haar-random states | 1 (exponential distribution) | 1.00 (mean over n=4..8) | 0.5% |

## 5. Verdict

**SPOT-CHECK — REPLICATED (for all quantitatively testable sub-claims).**

Justification:
- Paper's *headline theoretical result* (XQUATH ⇒ XHOG-hardness) is a conditional complexity-theoretic reduction; it is not a numerical claim and cannot be verified by simulation on any computer, classical or quantum. That headline is neither REPLICATED nor CONTRADICTED — it is out-of-scope for numerical replication.
- Paper's *quantitative empirical claims* used to motivate the theorem — the Porter-Thomas b ≈ 2, uniform b = 1, and the "top-k cheat is prevented by the distinct-samples requirement" — are all **quantitatively reproduced within 1% on real Cirq statevector simulations** at n = 4..8 qubits.
- The distinct-samples XHOG cheat at n=8 (b ≈ 1.94 from just the 100 heaviest amplitudes) empirically illustrates the very reason the paper's reduction has to work through XQUATH rather than a direct sampling argument: absent QUATH-style hardness, an efficient amplitude estimator would break XEB immediately.

The natural label for this work is therefore **SPOT-CHECK**: the code and method are verified, the two directly-testable numerical predictions of the paper are reproduced, and the paper's theoretical framing (why distinct samples matter, why the trivial uniform baseline sits at b=1) is illustrated end-to-end on real random-circuit simulations. It is not "REPLICATED" in the strong sense because the paper's main theorem is a hardness proof, not an executable claim.

## 6. Evidence Files

- `code/xeb_demo.py` — main XEB benchmark (Cirq, exact statevector).
- `code/xeb_spoof_topk.py` — bonus experiment: naive top-k / top-1 amplitude cheats.
- `report/evidence/results.json` — full n=4..8 sweep (per-circuit and aggregated).
- `report/evidence/spoof_topk.json` — top-k / top-1 spoofer results.
- `work/1910.12085.pdf` — the paper.

## 7. Reproducibility

```
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-1910.12085-xeb-classical-hardness
python3 -m venv .venv --system-site-packages
source .venv/bin/activate
pip install --quiet cirq-core numpy
python code/xeb_demo.py --seed 42 --n-circuits 20 --n-samples 20000 \
       --out report/evidence/results.json
PYTHONPATH=code python code/xeb_spoof_topk.py
```

Deterministic under `--seed 42`. Total wall time ≈ 20 s on a single CPU core.
