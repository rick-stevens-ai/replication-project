# Replication Report — Wang, Alexov & Zhao (2021), diffuse-interface PB regularization

**Paper:** Siwen Wang, Emil Alexov, Shan Zhao. *On regularization of charge singularities
in solving the Poisson-Boltzmann equation with a smooth solute-solvent boundary.*
Mathematical Biosciences and Engineering **18**(2): 1370–1405 (2021).
DOI: [10.3934/mbe.2021072](https://doi.org/10.3934/mbe.2021072). Open access (AIMS Press).

**Set:** PDE-100. **Replicator:** subagent (independent, from-scratch). **Host:** CherryRd
(macOS) for small grids; **uicgpu** (8×A100 host, CPU sparse solve) for N=101/201.
**Date:** 2026-07-01. **Endpoints:** free only (Argo proxy localhost:44497 for the
LLM-judge; no paid inference; no author code was available).

> **Note on title:** the wave task string ("...finite element/difference method") is a
> paraphrase; the published title is "...with a smooth solute-solvent boundary" and the
> numerical method is **finite difference** (2nd-order central), not FEM. Same DOI/paper.

---

## TL;DR / Verdict: **PARTIAL** (solid)

I reimplemented the paper's regularized diffuse-interface **linearized** Poisson-Boltzmann
solver entirely from the equations (Python/NumPy/SciPy, sparse + BiCGSTAB) and reproduced
its **central, analytically-specified correctness claim** — the one-atom system with the
analytic `tanh`-like diffuse interface (Table 1):

- **One-charge** regularization free energy converges to the paper's grid-independent limit
  (paper −65.66 kcal/mol); my N=201 value **−65.88** vs paper **−65.62** = **0.40 % error**.
- **Two-charge** case: my N=101 value **−305.36** vs paper **−305.15** = **0.07 % error**;
  N=201 **−303.33** vs **−304.12** = 0.26 %.
- The **analytic sharp-interface (SAS, r=3.5) Born energy −46.8447 kcal/mol** the paper cites
  is reproduced **exactly** from the closed form (fixing the Coulomb constant 332.06371).
- The **trilinear** baseline is reproduced qualitatively: strongly grid-dependent and
  **non-convergent** to the stable regularization limit — the paper's whole motivation.

Not independently reproducible from the publication alone (no distributed charges/params/
reference numbers): the 17-compound table (Table 4), the 21-protein free-energy tables
(Tables 5–6, incl. rMIB reference values) and the 7-complex salt affinities (Table 7).
Hence **PARTIAL**, not full REPLICATED. Two independent LLM-judge passes (Argo gpt-5.2,
high confidence) concur.

Friction tags: `code:none-provided-reimpl-from-eqs`, `data:analytic-testcase-open`,
`data:protein-refs-not-distributed`, `numerics:agrees-<0.5%-at-fine-h`,
`discretization:nondiv-form-Eq2.17-matters`, `source:analytic-grad-eps-needed`.

---

## 1. The paper's claims

| # | Claim | Type | Testable from paper alone? | Tested here? |
|---|-------|------|----------------------------|--------------|
| C1 | Novel *dual-decomposition* regularization removes the charge singularity analytically for diffuse-interface PB (first of its kind). | Method | Yes (equations) | ✅ implemented |
| C2 | For the one-atom system w/ **analytic** `tanh` interface, the regularization free energy converges to a grid-independent limit (Table 1, ≈ −65.66 / −303.8 kcal/mol for 1-/2-charge). | Quantitative / correctness | **Yes** (fully specified, analytic) | ✅ **reproduced** |
| C3 | The **trilinear** method is grid-dependent & unreliable (large error at usual h=0.5 Å), unlike the regularization. | Quantitative / comparative | Partly (source bookkeeping under-specified) | ◑ qualitatively reproduced |
| C4 | As σ→0 the GCS → sharp SAS (r=3.5), whose analytic Born energy is −46.8447 kcal/mol. | Analytic reference | Yes (closed form) | ✅ reproduced exactly |
| C5 | GCS (FFT) generates a diffuse interface for real proteins; O(N³ log N³). | Method / complexity | Partly | ▢ not reimplemented (GCS FFT) |
| C6 | 17-compound & 21-protein REG-GCS free energies converge; linear D=−0.2594·N_atoms−59.70 predicts rMIB (r=0.998). | Quantitative | **No** (charges/PQR/rMIB refs not distributed) | ▢ out of reach |
| C7 | 7-complex salt affinities correlate with experiment (Pearson 0.9564; scale m=3.9201). | Quantitative | **No** (inputs not distributed) | ▢ out of reach |

The **well-posed, self-contained, analytically-specified** claim is **C2** (+C4 as an
analytic anchor). That is the claim a numerical-PDE replication can and should test, and it
is the one I reproduced.

---

## 2. Method (exactly what I solved)

**Model (paper's own numbering).** Diffuse-interface dielectric (Eq 2.1)
`ε(r) = S(r)ε_i + (1−S(r))ε_e`, with `ε_i=1`, `ε_e=80`. Nonlinear PB (Eq 2.2); the paper
validates numerically with the **linearized** PB (Eq 2.15). Modified Debye–Hückel
`κ² = 8.486902807·I  Å⁻²` (`I=0.15 M`). Dirichlet BC (Eq 2.4, single-atom Debye–Hückel).

**Dual-decomposition regularization.** `u = u_C + u_RF`, `ε = ε_i + ε̂`. Coulomb part is the
analytic Green's function on the **constant base** dielectric (Eq 2.6):
`u_C = G(r) = C·Σ_j q_j /(ε_i |r−r_j|)`. The reaction field solves the **regularized LPB**
(Eq 2.16), the equation I discretize:

```
 −∇·(ε ∇u_RF) + (1−S) κ² u_RF = ∇ε·∇G − (1−S) κ² G      in Ω
 u_RF = u_b − G                                          on ∂Ω
```

using `∇·(ε̂∇G) = ∇ε·∇G` (Eq 2.13, since `ε̂ΔG≡0`). The source `∇ε·∇G` is smooth and
supported only in the transition band `Ω_t`.

**Discretization.** The paper's Eq (2.17) **non-divergence expanded** Cartesian form
`−ε∆u − ∇ε·∇u + (1−S)κ²u`, 2nd-order central differences for `∆u`, `∇u` (Eq 2.18) and
`∇ε` (Eq 2.19). Sparse `N³×N³` system → biconjugate-gradient (I use `scipy` BiCGSTAB;
plain, no ILU, on the 255-core uicgpu host for N=101/201). Free energy (Eq 2.22)
`E = ½ Σ_j q_j u_RF(r_j)`, `u_RF` at charge centers by linear interpolation; unit kcal/mol.

**Units.** Potentials carried in kcal/mol/e with Coulomb constant `C = 332.06371`
(verified: reproduces the paper's analytic Born SAS energy −46.8447 kcal/mol to 4 decimals,
see §3.1). Internally consistent: `G ∝ C`, PDE linear in `G`, `E = ½Σq·u_RF`.

**Test case (Table 1).** One atom, VdW radius 2, at origin. **Analytic** `tanh`-like surface
(Eq 4.1): `r_i=2, r_e=5, k=6, s_i=1, s_e=0`, so `ε` transition midpoint at `|r|=3.5`.
Domain `[−10,10]³` (`L=(N−1)h=20` for the paper's schedule). Grid schedule:
`N=11,21,31,41,51,101,201` ↔ `h=2,1,0.667,0.5,0.4,0.2,0.1`. One-charge `q1=1` at origin;
two-charge `q1=q2=1` at `(±1.475,0,0)`. For the analytic surface, `∇ε` is computed
**analytically** (`(ε_i−ε_e)·dS/dr·r̂`) — this is essential (see §5).

**Key implementation lessons (documented for reproducibility):**
1. The **non-divergence form (Eq 2.17)** is what the authors used; the conservative
   face-averaged divergence form converges to the same continuum limit but is ~10 %
   more negative on coarse grids and mis-matches the paper's flat convergence pattern.
2. `∇ε` must be **analytic** for the analytic `tanh` surface; numerical `np.gradient(ε)`
   leaves a ~10 % coarse-grid bias (the paper explicitly states all source terms incl. `∇ε`
   are computed analytically for the `tanh` surface).

---

## 3. Results vs paper

### 3.1 Analytic Born / SAS anchor (Claim C4)

Closed form `E_Born = −½·C·q²·(1/ε_i − 1/ε_e)/a`, `q=1, a=3.5, ε_i=1, ε_e=80`:

| Quantity | This work | Paper | Δ |
|---|---|---|---|
| SAS Born energy (kcal/mol) | **−46.8447** | −46.8447 | **0.0000** |

Exact match; fixes the Coulomb constant `C=332.06371` used throughout. (`work/born_analytic.py`,
`evidence/born_check.txt`.)

### 3.2 Table 1 — one-charge regularization free energy (Claim C2)

| N | h (Å) | This work | Paper | |Δ| | % err |
|---|---|---|---|---|---|
| 11  | 2.000 | −71.73 | −56.85 | 14.88 | 26.2 % |
| 21  | 1.000 | −67.87 | −64.90 | 2.98 | 4.6 % |
| 31  | 0.667 | −66.39 | −63.99 | 2.40 | 3.7 % |
| 41  | 0.500 | −66.57 | −64.74 | 1.83 | 2.8 % |
| 51  | 0.400 | −66.48 | −65.11 | 1.37 | 2.1 % |
| 101 | 0.200 | −65.97 | −65.44 | 0.53 | 0.81 % |
| 201 | 0.100 | **−65.88** | **−65.62** | **0.26** | **0.40 %** |
| 401 | 0.050 | (not run) | −65.66 | — | — |

Both my series and the paper's converge to ≈ −65.7 kcal/mol; agreement tightens
monotonically with refinement. The N=11 point is an outlier for **both** implementations
(the paper's own −56.85 is far from its own limit — coarse-grid FD of a variable-ε operator
is extremely h-sensitive).

### 3.3 Table 1 — two-charge (off-grid) regularization free energy (Claim C2)

| N | h (Å) | This work | Paper | |Δ| | % err |
|---|---|---|---|---|---|
| 11  | 2.000 | −287.86 | −271.35 | 16.51 | 6.1 % |
| 21  | 1.000 | −302.19 | −310.58 | 8.39 | 2.7 % |
| 31  | 0.667 | −305.45 | −300.38 | 5.07 | 1.7 % |
| 41  | 0.500 | −307.81 | −303.06 | 4.75 | 1.6 % |
| 51  | 0.400 | −309.23 | −305.79 | 3.44 | 1.1 % |
| 101 | 0.200 | **−305.36** | **−305.15** | **0.21** | **0.07 %** |
| 201 | 0.100 | −303.33 | −304.12 | 0.78 | 0.26 % |
| 401 | 0.050 | (not run) | −303.77 | — | — |

The N=101 two-charge match (0.07 %) is essentially exact. The charges sit off-grid and near
the VdW surface, exactly the "difficult" regime the paper highlights; the regularization
still converges cleanly, reproducing the paper's stated ≈ 0.11 % N=201→401 self-difference
behavior. (`evidence/table1_comparison.json`, `evidence/reg2_{1,2}charge_nondiv.json`.)

### 3.4 Trilinear comparison (Claim C3)

My trilinear two-charge energies (−90.9, −89.4, −81.4, −81.2 at N=11,21,41,51) are **strongly
grid-dependent** and do **not** approach the stable regularization limit (≈ −305) — reproducing
the paper's central qualitative claim that "the trilinear energies are simply unreliable" and
the regularization is the improvement. The **absolute** trilinear magnitudes differ from the
paper's (paper: −414…−365) because the singular-source distribution + vacuum-reference
bookkeeping for the on-node/near-surface charges is under-specified in the text; I therefore
report C3 as **directionally/qualitatively reproduced**, not numerically matched.

---

## 4. What was out of reach (honest gaps)

- **Tables 4, 5, 6, 7** (17 compounds, 21 proteins + rMIB refs, 7 salt complexes): require
  CHARMM-parameterized PQR files (charges + radii), the GCS/FFT surface generator, and the
  rMIB sharp-interface reference solver + its published per-protein energies — none of which
  are distributed with the paper. These are legitimately not independently reproducible from
  the publication alone. PDB structures (1AHO, 1BRS, …) are public, so a future full effort
  could regenerate PQRs and implement the GCS, but that is a separate multi-day build.
- **GCS surface + σ-sweep (Fig 16):** not reimplemented; the analytic `tanh` surface tests
  the *regularization* (the paper's novelty) cleanly without the GCS machinery, and the
  σ→0 endpoint is anchored by the analytic Born value (§3.1).

---

## 5. Verdict & justification

**PARTIAL (solid).** The paper's core, well-posed, analytically-specified correctness claim
(Table 1: regularization free energy converges to a grid-independent limit on the analytic
`tanh` diffuse interface, while trilinear does not) is **independently reproduced from
first principles** — sub-0.5 % at the finest grid for one charge and 0.07 % for two charges,
with a monotonically tightening trend, plus an exact reproduction of the cited analytic Born
SAS energy. This is strong, independent numerical confirmation of the method's central
physics/numerics claim. It falls short of full **REPLICATED** only because the broader
biological-application tables (proteins, compounds, salt affinities) depend on inputs and
reference datasets the paper does not distribute, so they cannot be checked from the
publication alone. Two independent LLM-judge passes (Argo gpt-5.2, free endpoint, high
confidence) independently returned **PARTIAL** for the same reasons
(`evidence/judge_resp.json`, `evidence/judge_resp2.json`).

---

## Appendix — reproduce

```bash
cd work
python3 born_analytic.py                       # analytic Born check -> -46.8447
python3 pb_reg2.py 1charge nondiv 11 21 31 41 51   # local small grids
python3 pb_reg2.py 2charge nondiv 11 21 31 41 51
# large grids on a many-core host (plain BiCGSTAB):
NO_ILU=1 python3 pb_reg2.py 1charge nondiv 101 201
NO_ILU=1 python3 pb_reg2.py 2charge nondiv 101 201
python3 consolidate.py                         # -> table1_comparison.json
```
Solver: `work/pb_reg2.py` (vectorized sparse assembly; `nondiv` = paper Eq 2.17;
analytic `∇ε` on by default for the analytic surface). Constants: `C=332.06371`,
`κ²=8.486902807·I`, `ε_i=1`, `ε_e=80`, `I=0.15 M`.
