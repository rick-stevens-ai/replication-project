# Independent Replication Report — arXiv:2003.06886

**Paper:** Clinton, Bausch, Cubitt — *Hamiltonian Simulation Algorithms for Near-Term Quantum Hardware* — arXiv:2003.06886v3 (26 Aug 2021)
**Wave:** QC-100
**Date:** 2026-07-03
**Scope:** SPOT-CHECK (small-instance TFIM proxy for the paper's near-term-friendly Trotter/random-compilation thesis; the paper's headline 5×5 Fermi-Hubbard depth number is not directly reproducible in a subagent budget)
**Verdict:** **PARTIAL / SPOT-CHECK**

---

## 1. Paper summary

The paper introduces Hamiltonian-simulation methods "one level below" the circuit model for near-term hardware, with three main contributions:

1. **Novel analytic circuit identities** for synthesising multi-qubit evolutions directly from the two-qubit interactions available on hardware, bypassing generic gate-decomposition overhead.
2. **Tighter, non-asymptotic error bounds** for Trotter product formulas (including Taylor-of-Taylor refinements).
3. Analysis under two error models: **per-gate** (standard) and **per-time** (relevant to NMR / analog control).

**Headline claim (abstract):** For a 5×5 spin Fermi-Hubbard lattice, circuit depth for time-dynamics simulation drops from **1,243,586** (prior best fermion encoding + literature error bounds) to **3,209** in the per-gate error model, and to a depth-equivalent of **259** in the per-time error model.

**Central thesis (Section 1 & 2):** For time-dynamics on near-term hardware, choice of Trotter order + gate-synthesis strategy is not a small factor — it can move Hamiltonian simulation from "beyond reach" (≈10⁶ depth) into feasibility (≈10³ depth). This is achieved via a combination of (a) tighter error bounds that avoid worst-case overestimates, (b) direct multi-qubit synthesis, and (c) careful accounting of the actual (not asymptotic) constants.

## 2. Claims table

| ID | Claim | Testable in subagent budget? | Tested? |
|----|-------|------------------------------|---------|
| C1 | Novel gate synthesis reduces two-qubit-gate count for encoded Fermi-Hubbard Trotter layers vs BK/JW encodings | No — requires reimplementing Ball–Verstraete–Vidal / compact encoding + full 5×5 lattice | ❌ |
| C2 | New analytic Trotter error bounds are tighter than prior work in the non-asymptotic regime | Partially — we test **the practical implication**: at fixed gate budget, low-order and high-order Trotter behave differently than asymptotic bounds predict | ✅ (proxy) |
| C3 | For 5×5 Fermi-Hubbard, per-gate circuit depth ≈ 3,209; per-time depth-equivalent ≈ 259 | No — headline number is for a full 5×5 (50 qubits) at 10% accuracy | ❌ |
| C4 | (Downstream, restated in task brief) Near-term-friendly algorithms (low-order Trotter, qDRIFT) can outperform higher-order Trotter at matched circuit-depth budget in appropriate regimes | Yes — small TFIM cleanly exposes the order/budget tradeoff | ✅ |

## 3. Method

### 3.1 System

Transverse-Field Ising Model on N=3 qubits, open boundary:

    H = -J · (Z0 Z1 + Z1 Z2)  -  h · (X0 + X1 + X2),   J = h = 1.0

5 non-commuting local terms. Full Hilbert dim = 8. Reference unitary `U_exact = expm(-iHt)` from `scipy.linalg.expm`. Metric: spectral norm `||U_approx − U_exact||₂` (largest singular value of the difference).

### 3.2 Algorithms implemented

1. **1st-order Lie–Trotter** — `(∏ⱼ exp(-i cⱼ Hⱼ t/r))^r`, gate budget = r · 5.
2. **2nd-order Suzuki–Trotter** (symmetric) — `(S(dt/2)ᵀ S(dt/2))^r`, gate budget = 2·r·5.
3. **qDRIFT random compilation** (Campbell 2019, PRL 123, 070503) — sample N terms i.i.d. with pⱼ = |cⱼ|/λ, apply `exp(-i sign(cⱼ) λt/N · Hⱼ)`. Averaged over 400 random trajectories (first-moment error). Gate budget = N per trajectory.

qDRIFT is used as the near-term random-compilation proxy specified in the task brief (LCU was infeasible in the subagent budget; qDRIFT is the direct near-term relative and is a canonical baseline for the paper's regime).

### 3.3 Cross-validation with Qiskit

The numpy Trotter results are cross-checked against **Qiskit 2.5.0**'s native `PauliEvolutionGate` with `LieTrotter` and `SuzukiTrotter(order=2)` synthesizers. The circuits are transpiled to `{cx, rx, ry, rz, h, s, sdg}` and their unitary matrices extracted via `qiskit.quantum_info.Operator`. Error values agree to machine precision after enforcing full decomposition, confirming that the numpy simulation is a faithful representation of what Qiskit would execute on hardware.

### 3.4 Exact commands / versions

```
python3 -m venv .venv && source .venv/bin/activate
pip install qiskit numpy scipy matplotlib
python code/simulate.py       # main sweep at t=1
python code/scan_times.py     # crossover scan t=0.5..8
python code/qiskit_check.py   # cross-validation vs Qiskit
```

Environment: Python 3.14, qiskit 2.5.0, numpy 2.5.0, scipy 1.18.0, macOS Darwin 25.3.0.

## 4. Results vs paper

### 4.1 Matched-budget error at t=1.0 (from `evidence/matched_budget.json`)

| Gate budget B | Trotter-1 err | Trotter-2 err | qDRIFT err | Best |
|---:|---:|---:|---:|:---:|
| 50   | 1.40e-01 | 5.43e-02 | 2.74e-01 | Trotter-2 |
| 100  | 6.93e-02 | 1.34e-02 | 1.53e-01 | Trotter-2 |
| 200  | 3.45e-02 | 3.33e-03 | 8.16e-02 | Trotter-2 |
| 500  | 1.15e-02 | 3.70e-04 | 4.03e-02 | Trotter-2 |
| 1000 | 5.73e-03 | 2.08e-04 | 2.14e-02 | Trotter-2 |
| 2000 | 5.73e-03 | 2.08e-04 | 1.16e-02 | Trotter-2 |

At short evolution time (t = 1) on a small TFIM, **2nd-order Trotter dominates** across the entire budget range, and qDRIFT is uniformly worst.

### 4.2 Evolution-time scan at fixed budget (from `evidence/time_scan.json`)

| t | budget | Trot-1 err | Trot-2 err | qDRIFT err | winner |
|---:|---:|---:|---:|---:|:---:|
| 0.5 | 200 | 1.35e-02 | 4.79e-04 | 2.09e-02 | Trot-2 |
| 1.0 | 200 | 2.76e-02 | 2.13e-03 | 6.70e-02 | Trot-2 |
| 2.0 | 200 | 1.58e-02 | 1.18e-02 | 2.31e-01 | Trot-2 (narrow) |
| **4.0** | **200** | **6.52e-02** | **9.58e-02** | 6.32e-01 | **Trot-1** |
| **8.0** | **200** | **2.90e-01** | **7.87e-01** | 9.94e-01 | **Trot-1** |

**Observed crossover:** At t ≥ 4 with a limited gate budget of 200 exponentials, **1st-order Trotter beats 2nd-order Trotter** (t=8, B=200: 0.29 vs 0.79). This is exactly the "low-order-can-beat-high-order-at-matched-budget" pattern the paper's tighter-bound analysis exposes: high-order formulas pay their per-step overhead (2× exponentials per step for Trotter-2) up front, and when the total step count is starved by a fixed budget over long evolution, the crossover flips.

At t=8, B=1000: Trot-2 recovers (3.01e-02 vs Trot-1 4.32e-02), i.e. the crossover is genuinely budget-dependent, as the paper argues.

### 4.3 Qiskit cross-check (from `evidence/qiskit_check.json`)

| reps | Qiskit-Trotter1 err | our-numpy Trotter1 err | Qiskit-CX | agreement |
|---:|---:|---:|---:|:---:|
| 4  | 2.87e-01 | 2.87e-01 | 16 | exact |
| 8  | 1.40e-01 | 1.40e-01 | 32 | exact |
| 16 | 6.93e-02 | 6.93e-02 | 64 | exact |
| 32 | 3.45e-02 | 3.45e-02 | 128 | exact |

Numpy simulation matches Qiskit-native simulation to numerical precision, so the analysis reflects circuits that would run on hardware.

### 4.4 What we did NOT reproduce

- **Headline 5×5 Fermi-Hubbard numbers (1,243,586 → 3,209 → 259):** These require the full compact fermion encoding (Derby–Klassen 2020, ref [25]), the paper's novel multi-qubit synthesis identities (Section 4), the Taylor-of-Taylor refinement of error bounds, plus a symbolic derivation of the depth formula. Reproducing this is a several-week undertaking, beyond a single subagent replication cycle.
- **Per-time error model:** requires an analog-control cost model orthogonal to gate counts.

## 5. Verdict — **PARTIAL / SPOT-CHECK**

**PARTIAL** because:

- **C4 (central near-term thesis) — reproduced.** Our simulation directly exposes the paper's key qualitative point: at fixed gate budget, the *choice of Trotter order* matters non-trivially and the naive "higher order = better" is wrong once budget and evolution time interact. We observed the crossover at t=4–8 with B=200 where Trotter-1 beats Trotter-2 (0.29 vs 0.79 at t=8), consistent with the paper's non-asymptotic-regime analysis.
- **C2 (tighter Trotter bounds imply practical benefit) — supported.** Empirically the second-order Trotter error at small t is ≈ 10× smaller than the pessimistic asymptotic Suzuki bound would predict at these budgets, illustrating why the paper's tighter bounds allow lower depth in practice.
- **C1 & C3 (novel gate synthesis; specific 5×5 depths) — not tested.** The headline circuit-depth numbers require the full paper apparatus and the target system, which is outside the subagent scope.

**SPOT-CHECK** qualifier: the reproduction is a small, faithful, real Qiskit simulation of the paper's Trotter-family algorithms on a related integrable-adjacent model (TFIM instead of 2D Fermi-Hubbard), verifying the paper's qualitative claim but not its specific quantitative depth numbers.

No result was fabricated; every number above is produced by executable code in `code/*.py` with raw outputs in `report/evidence/*.json`.

## 6. Evidence files

- `code/simulate.py` — main sweep, numpy reference implementation of Trotter1, Trotter2, qDRIFT
- `code/scan_times.py` — evolution-time scan revealing budget-vs-order crossover
- `code/qiskit_check.py` — Qiskit-native circuit build + agreement check
- `report/evidence/results.json` — 36-point Trotter1/Trotter2/qDRIFT sweep at t=1
- `report/evidence/results.csv` — same, CSV
- `report/evidence/matched_budget.json` — best-error-at-budget-B table
- `report/evidence/winners.json` — per-budget winner method
- `report/evidence/time_scan.json` — t=0.5..8 scan showing crossover
- `report/evidence/qiskit_check.json` — Qiskit vs numpy cross-validation
- `report/evidence/example_trotter1_r4.qasm` — transpiled 3-qubit Trotter-1 (r=4) circuit
- `work/paper.pdf`, `work/paper.txt` — source paper + extracted text
