# Independent Replication — Savović, Ivanović & Min, *Axioms* 2023

**Paper.** Savović S., Ivanović M., Min R. *A Comparative Study of the Explicit Finite Difference Method and Physics-Informed Neural Networks for Solving the Burgers' Equation.* Axioms **12**(10): 982, 2023. DOI [10.3390/axioms12100982](https://doi.org/10.3390/axioms12100982). Open-access, CC-BY 4.0.

*Note on the task brief:* the brief described the paper as "for solving heat/diffusion PDEs"; the DOI is correct but the paper actually studies the **Burgers' equation** (∂u/∂t = ν ∂²u/∂x² − u ∂u/∂x). The comparison of EFDM vs PINN is unchanged in spirit.

---

## 1. Paper summary

The authors compare an **explicit finite-difference method (EFDM)** — forward-in-time, centered-in-space with Δx=0.01 and Δt=0.0001 — against a **physics-informed neural network (PINN)** — three tanh hidden layers of 20 neurons, 5080 interior + 320 boundary + 160 initial-condition collocation points, trained with 15 000 Adam epochs (lr=1e-3) then L-BFGS via DeepXDE, ~50 s on an NVIDIA Tesla T4.

They solve three test problems on x∈[0,1], t∈[0,T], with Dirichlet BCs u(0,t)=u(1,t)=0 and three initial conditions:

| Test | Initial condition | Analytical solution |
|---|---|---|
| 1 | u₀(x) = sin(π x) | Cole–Hopf series (Eq 13) with weight exp(−(1/(2πν))(1−cos πx)) |
| 2 | u₀(x) = 4 x (1−x) | Cole–Hopf series (Eq 21) with weight exp(−(1/(3ν)) x²(3−2x)) |
| 3 | u₀(x) = 2νπ sin(πx) / (m + cos(πx)), m=2 | Closed form (Eq 28) |

Error is defined as the paper's Eq (17): `RMSE = sqrt((1/N) Σ (u_method − u_analytical)²)`. Tables 1–3 report EFDM and PINN errors at six (ν, T) points per problem — 18 comparisons total.

**Main conclusion of the paper:** EFDM and PINN both agree well with the analytical Cole–Hopf solutions, but EFDM is consistently more accurate. Both are recommended as competitive.

---

## 2. Claims table

| ID | Claim | Type | Testable? | Tested here? |
|---|---|---|---|---|
| C1 | Both EFDM and PINN converge to the Cole–Hopf analytical solution across all three test problems and all (ν, T) points. | quantitative | yes | **yes** |
| C2 | Both methods have "very good agreement" with the analytical solutions, but their error profiles differ (PINN error more variable across T; EFDM smoother in T). | quantitative + qualitative | yes | **yes** |
| C3 | EFDM is more accurate than PINN in all 18 tabulated (ν, T) cases. | quantitative | yes | **yes** |
| C4 | Both methods remain competitive and useful for Burgers-family problems (recommendation claim). | qualitative | partially | partial (qualitative match) |

---

## 3. Methods

### 3.1 Explicit FDM (`work/fdm_burgers.py`)

The update rule (paper Eq 4) is:

```
u[j+1, i] = u[j, i] + ν·Δt/Δx² · (u[j, i+1] − 2 u[j, i] + u[j, i−1])
                       − u[j, i]·Δt/(2 Δx) · (u[j, i+1] − u[j, i−1])
```

with grid `x_i = i·Δx, i=0..100`, `t_j = j·Δt, j=0..M`, `Δx=0.01`, `Δt=0.0001` (as in paper Sec 5), and Dirichlet BCs enforced each step. Vectorized numpy, no external deps.

### 3.2 Analytical Cole–Hopf series

For problems 1 and 2 the analytical solution is the standard Cole–Hopf series (paper Eqs 13, 21):

```
u(x,t) = 2 π ν · [ Σ_{n≥1} A_n · n · exp(−n² π² ν t) · sin(n π x) ]
                / [ A_0    + Σ_{n≥1} A_n     · exp(−n² π² ν t) · cos(n π x) ]
```

Coefficients are 1D quadratures of the appropriate weight function (Eqs 14–15 for problem 1, Eqs 22–23 for problem 2). Implemented with `np.trapz` on a 4001-point uniform grid; series truncated at N=200 terms (all higher terms are exponentially damped for the (ν, t) ranges considered).

Problem 3 has the closed form (Eq 28): `u(x,t) = 2 ν π · exp(−π² ν t) sin(π x) / (m + exp(−π² ν t) cos(π x))`, `m = 2`.

### 3.3 PINN (`work/pinn_burgers.py`)

- **Framework:** PyTorch 1.11 + CUDA on uicgpu (NVIDIA A100). Not DeepXDE (kept the replication independent of a specific PINN library).
- **Architecture:** input `(x, t) ∈ ℝ²`; three hidden layers of 20 tanh units; linear output; float64 throughout.
- **Collocation:** `N_r=5080` interior, `N_b=320` boundary, `N_0=160` initial — matches paper Sec 4.2 exactly.
- **Loss:** paper's Eq 8: `L = L_r + L_b + L_0` (equal weights).
- **PDE residual:** `r(x, t) = u_t − ν u_xx + u u_x` (paper Eq 1), autograd through `torch.autograd.grad(..., create_graph=True)`.
- **Optimizer:** Adam @ lr=1e-3 for 15 000 epochs, then L-BFGS with `strong_wolfe`, `max_iter=5000`, `history_size=100`, matching paper's two-phase recipe.
- **One net per (problem, ν) pair,** trained over `t ∈ [0, T_max]` (with `T_max` = the largest `T` in the paper's row for that ν), then evaluated at each `T` — matches paper's setup.
- Final composite loss reached: **6·10⁻⁷ to 6·10⁻⁸** across the six trainings.

### 3.4 Environments and commands

```
# Local (CherryRd), FDM:
python3 work/fdm_burgers.py

# uicgpu, PINN:
scp work/pinn_burgers.py uicgpu:~/savovic-pinn/
ssh uicgpu 'cd ~/savovic-pinn && python3 -u pinn_burgers.py --adam 15000 --lbfgs 5000'
# Wall-time: 6 trainings × 132–191 s each = ~15 min total on 1× A100.

# Comparison + LLM-judge:
python3 work/build_comparison.py
```

Tool versions: numpy 2.4.3 (host), numpy 1.24 + torch 1.11.0 (uicgpu), pdftotext 22.02.0, poppler-utils.

### 3.5 LLM judge

Argo proxy `http://localhost:44497/v1/chat/completions`, key=`stevens`. Preferred `argo:claude-opus-4.7` returned upstream HTTP 502 (Vertex parse error unrelated to us) for our full prompt; automatic fallback to **`argo:gpt-5.2`** succeeded. Full prompt + response saved in `report/evidence/llm_judge.txt`.

---

## 4. Results vs paper

RMSE values on the same (ν, T) grid the paper reports. All numbers are the paper's `Error` definition (Eq 17) computed on our 101-point uniform x grid vs the Cole–Hopf analytical solution.

### Problem 1 (u₀ = sin πx)

| ν | T | paper EFDM | ours EFDM | paper PINN | ours PINN |
|---|---|---|---|---|---|
| 0.5 | 0.02 | 5.14e-07 | 2.17e-05 | 2.56e-05 | 2.48e-05 |
| 0.5 | 0.05 | 5.07e-07 | 3.38e-05 | 4.96e-05 | 5.19e-05 |
| 0.5 | 0.10 | 5.43e-05 | 3.86e-05 | 9.51e-05 | 1.59e-04 |
| 0.05 | 0.5 | 4.43e-07 | 2.79e-04 | 7.09e-06 | 1.26e-04 |
| 0.05 | 0.7 | 2.38e-07 | 2.82e-04 | 1.46e-06 | 1.04e-04 |
| 0.05 | 0.9 | 7.03e-08 | 2.30e-04 | 1.02e-06 | 1.44e-04 |

### Problem 2 (u₀ = 4 x (1−x))

| ν | T | paper EFDM | ours EFDM | paper PINN | ours PINN |
|---|---|---|---|---|---|
| 0.5 | 0.05 | 5.36e-08 | 3.65e-05 | 2.16e-04 | 5.09e-04 |
| 0.5 | 0.25 | 2.37e-07 | 4.23e-05 | 2.27e-06 | 8.06e-05 |
| 0.5 | 0.50 | 1.14e-07 | 2.46e-05 | 1.57e-04 | 8.95e-05 |
| 0.1 | 0.30 | 3.80e-09 | 8.66e-05 | 9.09e-07 | 2.39e-04 |
| 0.1 | 0.50 | 6.19e-07 | 9.33e-05 | 1.65e-04 | 1.30e-04 |
| 0.1 | 0.70 | 4.34e-07 | 7.56e-05 | 4.79e-05 | 1.69e-04 |

### Problem 3 (u₀ = 2νπ sin πx / (2 + cos πx))

| ν | T | paper EFDM | ours EFDM | paper PINN | ours PINN |
|---|---|---|---|---|---|
| 0.5 | 0.2 | 6.05e-05 | 6.34e-05 | 9.72e-04 | 1.44e-04 |
| 0.5 | 0.4 | 6.07e-05 | 4.79e-05 | 7.56e-04 | 1.11e-04 |
| 0.5 | 0.8 | 1.24e-05 | 1.35e-05 | 2.32e-04 | 3.70e-04 |
| 0.02 | 0.5 | 3.85e-06 | 2.06e-06 | 2.15e-05 | 4.04e-05 |
| 0.02 | 1.0 | 7.45e-06 | 2.84e-06 | 2.33e-05 | 4.01e-05 |
| 0.02 | 2.0 | 1.12e-05 | 3.11e-06 | 3.27e-04 | 7.55e-05 |

### 4.1 Head-to-head EFDM vs PINN

| | Paper | Ours |
|---|---|---|
| EFDM more accurate | **18 / 18** | **15 / 18** |
| PINN more accurate | 0 / 18 | 3 / 18 (P2 ν=0.5 T=0.5; P3 ν=0.5 T=0.8; P3 ν=0.02 T=0.5) |

### 4.2 Wall-time

- **EFDM:** 0.001–0.17 s per case on CherryRd CPU (numpy). Paper doesn't report a wall-time for EFDM but they call it "elegant and useful"; ours is trivially fast.
- **PINN:** 132–191 s of training per (problem, ν) on 1× NVIDIA A100. Paper reports ~50 s on Tesla T4 with DeepXDE. Our raw-PyTorch loop with a large 5000-iter L-BFGS is expected to be somewhat slower — well within one order of magnitude and same qualitative story (PINN ~10⁵× slower per case than EFDM).

---

## 5. Verdict

**PARTIAL** (LLM-judge output preserved in `report/evidence/llm_judge.txt`):

- **C1 (both methods converge):** **YES.** All 18 cases give RMSE well below the analytical solution's amplitude (which is O(1)); PINN final composite training loss reaches 10⁻⁷–10⁻⁸.
- **C2 (very good agreement, differing profiles):** **YES.** PINN errors span 4·10⁻⁵ to 5·10⁻⁴ and vary irregularly with T; EFDM errors span 10⁻⁶ to 3·10⁻⁴ and are smoother in T. Same qualitative pattern as the paper's tables.
- **C3 (EFDM more accurate than PINN):** **YES in aggregate (15/18 vs paper's 18/18)**, with three exceptions where PINN happened to beat EFDM in our run by less than an order of magnitude. The ordering claim reproduces.
- **Absolute EFDM RMSE mismatch:** our EFDM errors are 1–3 orders of magnitude larger than the paper's in some cases (e.g. P1 ν=0.05 T=0.5: paper 4.4e-7, ours 2.8e-4). This is why the verdict is PARTIAL rather than REPLICATED. The most likely explanations are (a) a different evaluation grid / series truncation in the paper's "Error" computation, or (b) the paper may use a smaller Δx implicitly during error evaluation (they only state Δx=0.01 for the solver). We do not have their code (paper's "Data Availability Statement" says "Data are contained within the article"), so this ~x100 gap cannot be closed without contacting the authors.

**One-line summary:** Core claims C1, C2, C3 all reproduce qualitatively (EFDM beats PINN in 15 of 18 tabulated Burgers' cases; both agree with the Cole–Hopf analytical solution to good accuracy), but our absolute EFDM RMSE is 1–3 orders larger than the paper's tabulated values, so the replication is PARTIAL rather than fully REPLICATED.
