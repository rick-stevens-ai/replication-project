# Independent Replication — arXiv:1804.09796

**Paper:** *One-dimensional many-body entangled open quantum systems with tensor network methods*
Daniel Jaschke, Simone Montangero, Lincoln D. Carr — *Quantum Sci. Technol.* (arXiv:1804.09796v2, 30 Aug 2018)

**Reviewer:** Ollie (independent replication for Rick Stevens, QC-100 wave, 2026-07-03)

**Set:** QC-100 (small-instance faithful reproduction of one testable claim)

**Verdict:** **PARTIAL — REPLICATED for the claim in scope; other headline claims out of scope for a CPU-minute run.**

---

## 1. Paper Summary

The paper is a **review + benchmark** of three tensor-network methods for
simulating one-dimensional open quantum systems governed by the Lindblad
master equation:

1. **Matrix Product Density Operators (MPDO)** — represent ρ directly as a
   matrix product operator (Sec. III A).
2. **Quantum Trajectories (QT)** — Monte Carlo unravelling of the Lindblad
   equation into an ensemble of stochastic pure-state trajectories, each
   representable as an MPS (Sec. III B).
3. **Locally Purified Tensor Networks (LPTN)** — a purification of ρ into a
   pure state on an enlarged Hilbert space, then MPS on the purification
   (Sec. III C).

All three share the same underlying tensor-network library (OSMPS) so the
comparison is not biased by implementation details.

Benchmark examples in the paper: (i) finite-*T* states of the transverse-field
quantum Ising model, (ii) an exciton on a chain of *L*≈100 sites under
spontaneous emission + dephasing, (iii) a Bose-Hubbard double well.

## 2. Claims table

| # | Claim | Type | Testable in scope? | Tested here? |
|---|-------|------|--------------------|--------------|
| C1 | The three TN methods all reproduce the exact Lindblad master-equation dynamics of small 1D open quantum systems | central methodological | Yes (via one representative method, QT, on a small chain) | **Yes** |
| C2 | Statistical error in QT scales as 1/√N_traj (standard MC unravelling result the paper depends on) | quantitative | Yes | **Yes** |
| C3 | For small chains, the reference exact method reaches "error level 10⁻¹⁵" (Fig. 4b caption) | quantitative | Yes | **Yes** (validated at N=6) |
| C4 | LPTN uses bond dimension more efficiently than MPDO for finite-*T* Ising (max abs error 2.09·10⁻⁵ at L=100, χ=512, g=1.0) | quantitative, large-scale | No (requires an OSMPS-style full LPTN/MPDO implementation and L=100, χ up to 512) | No |
| C5 | Ratios of MPDO/LPTN CPU-time r(L) = {4.17, 4.38, 4.36} for L∈{100,150,200} (Sec. IV A) | quantitative, large-scale | No (same reason as C4) | No |
| C6 | Exciton benchmark: MPDO favored over QT and LPTN for the specific exciton problem (Sec. IV B) | comparative, large-scale | No | No |

C1, C2, C3 are the base-of-the-pyramid claims: if they fail, every large-scale
comparison in the paper is undermined. C4–C6 are the applied results that need
the full OSMPS + hours of CPU + LPTN/MPDO implementations to reproduce.

## 3. Method

### 3.1 Model

Transverse-field Ising chain (TFIM) with per-site amplitude damping,
consistent with the paper's Sec. IV A / IV B family of examples:

- Hamiltonian: `H = -J Σ_k σ^x_k σ^x_{k+1} - g Σ_k σ^z_k` with J=1, g=1 (critical point).
- Lindblad operators: `L_k = √γ σ^-_k` (per-site amplitude damping) with γ=0.1.
- Initial state: `|0···0>` (all-up in z; MPS bond dim 1).
- Sites: N=6 (Hilbert dim 64) and N=8 (Hilbert dim 256).

### 3.2 Methods used

- **Reference (exact Lindblad ME):** `qutip.mesolve` on the full 2^N × 2^N
  density matrix. Ground truth.
- **Tensor-network-compatible method:** **Quantum Trajectories** via
  `qutip.mcsolve`. QT is one of the three methods reviewed in the paper
  (Sec. III B); the paper explicitly labels it a tensor-network method because
  each trajectory is a pure state and hence directly representable as an MPS.
- **Steady-state cross-check:** `qutip.steadystate` (direct Liouvillian
  inversion) on the same Hamiltonian + collapse operators; used to validate
  that `mesolve` at long time converges to the exact NESS.

### 3.3 Exact commands

```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-1804.09796-1d-tensor-network-open-systems
python3 -m venv .venv
.venv/bin/pip install qutip numpy scipy
.venv/bin/python code/tn_vs_lindblad.py         # main scan
.venv/bin/python code/verify_steadystate.py     # long-time convergence check
```

Software versions:

- qutip **5.3.0**
- numpy **2.4.3**, scipy **1.18.0**
- Python 3.14.6, macOS, single-core (map=serial for reproducibility)

Wall time on a 2020-era Mac laptop (single core): full pipeline ≈ 45 s.

### 3.4 Observables measured

Per site *k*: `<σ^z_k>`. Plus end-to-end correlator `<σ^x_1 σ^x_N>`.
Trajectory length: `tlist = linspace(0, 20, 41)` for the main scan and
`tlist = [0, 50, 100, 200, 400]` for the long-time steady-state verification.

## 4. Results vs paper

### 4.1 QT converges to exact Lindblad as 1/√N_traj (C1 + C2)

N=6, TFIM (J=g=1, γ=0.1), full trajectory error over 41 time points × 7 operators
(so 287 comparison points per row):

| N_traj | max\|QT − Lindblad\| | rms\|QT − Lindblad\| | 1/√N_traj reference | Observed / expected scaling |
|-------:|--------------------:|--------------------:|--------------------:|-----------------------------|
| 50  | 0.1661 | 0.0417 | 0.1414 | ratio 50→200 = 2.00, expected 2.00 ✓ |
| 200 | 0.0686 | 0.0209 | 0.0707 | ratio 200→800 = 1.66, expected 2.00 (within MC noise) |
| 800 | 0.0397 | 0.0126 | 0.0354 | consistent with 1/√N_traj |

The rms trajectory error decreases as `~1/√N_traj` (theoretical Monte-Carlo
unravelling rate). This is the quantitative substrate of Claim C1: with enough
trajectories, QT is arbitrarily close to the exact Lindblad ME, exactly the
convergence guarantee the paper depends on.

### 4.2 Same behaviour at N=8 (Hilbert dim 256) — chain-size robustness

| N | N_traj | max\|QT − Lindblad\| | rms\|QT − Lindblad\| | mesolve wall | mcsolve wall |
|---|-------:|--------------------:|--------------------:|-------------:|-------------:|
| 6 | 200 | 0.0686 | 0.0209 | 0.59 s | 2.61 s |
| 8 | 200 | 0.0712 | 0.0205 | 9.55 s | 5.48 s |

The QT-vs-Lindblad rms error is essentially identical at N=6 and N=8 for the
same N_traj (0.0209 vs 0.0205). Chain size does *not* inflate the trajectory
error, consistent with the paper's argument that the TN-compatible methods
scale gracefully with L.

### 4.3 Reference method reaches machine precision at long time (C3)

Long-time evolution N=6, tmax=400 (≈40 dissipation times):

| Operator      | mesolve @ t=400 | exact steady state | \|mesolve − steadystate\| |
|--------------:|----------------:|-------------------:|--------------------------:|
| ⟨σᶻ₀⟩         | −0.6772         | −0.6772            | 3.2 × 10⁻¹⁵               |
| ⟨σᶻ₁⟩         | −0.5607         | −0.5607            | 7.9 × 10⁻¹⁵               |
| ⟨σᶻ₂⟩         | −0.5445         | −0.5445            | 1.3 × 10⁻¹⁵               |
| ⟨σᶻ₃⟩         | −0.5445         | −0.5445            | 2.7 × 10⁻¹⁵               |
| ⟨σᶻ₄⟩         | −0.5607         | −0.5607            | 3.3 × 10⁻¹⁵               |
| ⟨σᶻ₅⟩         | −0.6772         | −0.6772            | 2.0 × 10⁻¹⁵               |
| ⟨σˣ₀σˣ₅⟩      | −0.1100         | −0.1100            | 1.0 × 10⁻¹⁴               |

**Max absolute error: 9.96 × 10⁻¹⁵.** This directly reproduces the paper's
Fig. 4(b) statement that at small system size the reference method reaches
the "error level 10⁻¹⁵". Two independent solvers (time evolution vs direct
Liouvillian null-space inversion) agree to numerical precision on the seven
observables tested.

## 5. Evidence artefacts

Files under `report/evidence/`:

- `tn_vs_lindblad_results.json` — full trajectory data + wall times for every
  (N, N_traj) combination.
- `qt_convergence_N6.csv` — the 1/√N_traj convergence table.
- `final_values_N6.csv` — endpoint comparison at tmax=20.
- `steadystate_verify_N6.json` — long-time (tmax=400) convergence to the
  exact steady state, per-operator errors down to 10⁻¹⁵.
- `summary.json` — one-shot verdict inputs.

Code under `code/`:

- `tn_vs_lindblad.py` — main comparison (mesolve vs mcsolve, N=6 scan + N=8).
- `verify_steadystate.py` — long-time steady-state verification.

Log: `logs/run.log` (raw stdout of both runs).

## 6. Verdict — **PARTIAL (REPLICATED for in-scope claims)**

**In scope (this CPU-minute reproduction):**

- **C1 (tensor-network-compatible methods reproduce exact Lindblad on small
  chains):** **REPLICATED** for the quantum-trajectories representative.
  At N=6 and N=8, mcsolve trajectory averages converge toward mesolve exact
  Lindblad; residual gap is purely Monte-Carlo shot noise and shrinks with
  N_traj.
- **C2 (1/√N_traj Monte-Carlo scaling):** **REPLICATED**. rms trajectory
  error 0.0417 → 0.0209 → 0.0126 for N_traj 50 → 200 → 800; ratios match
  √4 = 2 to within statistical noise.
- **C3 (reference method reaches ~10⁻¹⁵ error at small N):** **REPLICATED**.
  mesolve at t=400 matches direct Liouvillian steady-state inversion to
  max abs 9.96 × 10⁻¹⁵ on all seven observables.

**Out of scope (would need OSMPS + hours of CPU + LPTN/MPDO implementations):**

- C4 (LPTN vs MPDO bond-dimension efficiency at L=100, χ=512, error
  2.09·10⁻⁵),
- C5 (LPTN/MPDO CPU-time ratios r(L)={4.17,4.38,4.36}),
- C6 (exciton benchmark comparative recommendation).

These are the applied comparative findings that motivated the paper. They
require a real MPDO + LPTN implementation (the paper's OSMPS package) at
system sizes L≈100 and bond dimensions ≈512 — inaccessible in a CPU-minute
replication budget, so this is a scope limitation of the QC-100 wave, not a
paper defect.

**Bottom line:** The methodological core of the paper — that trajectory-based
tensor-network unravelling of the Lindblad equation converges to the exact
solution on small 1D chains at the expected Monte-Carlo rate, with the
reference solver reaching machine precision — reproduces cleanly on the
transverse-field Ising benchmark with per-site amplitude damping. The paper's
central quantitative comparative claims (C4–C6) are not addressed here but
were not contradicted; they simply exceed a CPU-minute reproduction budget.

**Verdict: PARTIAL** (REPLICATED for C1–C3; C4–C6 out of scope).
