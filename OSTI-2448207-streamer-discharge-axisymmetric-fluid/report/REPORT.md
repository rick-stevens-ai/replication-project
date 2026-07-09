# Independent Replication — OSTI 2448207

**Massively parallel axisymmetric fluid model for streamer discharges**
Fierro, Alibalazadeh, Stephens, Moore (UNM / Texas Tech / Sandia).
SAND2024‑12794J · *Comput. Phys. Commun.* 2024 · DOI 10.1016/j.cpc.2024.109345 · OSTI 2448207.

Replication wave: OSTI‑100 (top‑up 50). Budget: efficient (<25 min), free endpoints only, no proprietary data / no paid tools.

---

## 1. Paper summary

An MPI/C++ finite‑volume, **electrostatic drift‑diffusion** (first‑order fluid) plasma solver in **2‑D r‑z axisymmetric** geometry with a fixed (non‑AMR) mesh, designed to scale to 10⁸ elements on ~10³ processors. Core equations:

- Species continuity `dn_s/dt + ∇·Γ = Q_src` (eq 1), flux `Γ = ±μ_s n_s E − D_s ∇n_s` (eq 2).
- Finite‑volume integration with divergence theorem (eq 4‑5); **1st‑order upwind advection** face fluxes (eq 6‑21), **2nd‑order central diffusion** face fluxes (eq 22‑26), forward‑Euler update (eq 27).
- **Poisson** `∇²φ = −ρ/ε₀` (eq 30‑31) via central differences (eq 32) solved with Trilinos/Belos **GMRES** (tol 1e‑6) + **MueLu** multigrid; `E = −∇φ` central (eq 35‑37).
- Local‑field source `Q_src = ᾱ μ_e |E| n_e` (eq 51); semi‑implicit sub‑iteration (2‑5 cycles) coupling n↔φ↔E (eq 48‑49).
- Validated against community streamer benchmark case 1 (ref [18], "CWI" model), plus spatial‑convergence and strong/weak scaling studies.

## 2. Claims table

| ID | Claim | Type | Testable? | Tested? | Result |
|---|---|---|---|---|---|
| C1 | Domains/grids self‑consistent: benchmark 4000×3200 @3.125µm and conv 12500×10000 @1µm both → 1.25 cm × 1.0 cm | arithmetic | yes | yes | ✅ exact |
| C2 | Courant numbers 0.538/0.272/0.110/0.055 for Δt=5/2.5/1/0.5 ps are **linear in Δt** | analytic | yes | yes | ✅ max dev 1.4% |
| C3 | Benchmark Courant ≈ 0.1 for Δh=3.125µm, Δt=0.5ps, v≈6×10⁵ m/s | analytic (CFL) | yes | yes | ✅ 0.096≈0.1 |
| C4 | Element counts: 12.8M, 0.8M, 125M, 268M, 524288, 33.5M | arithmetic | yes | yes | ✅ all exact |
| C5 | Base scheme (1st‑order upwind + central diffusion) → **linear (first‑order) error reduction with Δh** (Fig 7 "expected error reduction based upon the implemented discretization") | numerical (order of accuracy) | yes | yes | ✅ p = 0.995 (MMS) |
| C6 | Coupled streamer peak‑E relative error <1% at Δh≈4µm (4 ns); approaches 1% at 2µm (10 ns) | numerical (full sim) | yes | no | ⛔ full HPC sim + CWI data out of scope |
| C7 | Peak‑E and streamer length within bounds of 6‑code benchmark; peak‑E within 5% of CWI for all times | numerical (full sim) | yes | no | ⛔ needs proprietary CWI reference |
| C8 | 1st‑order upwind **overestimates** streamer velocity vs Koren flux‑limited (Fig 10) | numerical | yes | attempted | ⚠️ toy solver unstable; not reproduced |
| C9 | Strong scaling ~perfect ≤256 procs (2× procs → ~2× speedup); FV solve scales to 1024; field solver bottleneck ≥512 | HPC scaling | partly | no | ⛔ no cluster rerun |

## 3. Method (numbered, exact)

Environment: CherryRd, Python 3.14, numpy 2.4.3, scipy 1.18.0. PDF via `ssh uicgpu` HTTP proxy. LLM‑judge = free Argo `argo:gpt-5.2` (localhost:44497).

1. **Fetch** OA PDF: `curl -sL https://www.osti.gov/servlets/purl/2448207` on uicgpu (1.99 MB, md5 `41204e9adef92fa85c980f66c0d8d39f`); `pdftotext -layout` → 830 lines. (CherryRd is blocked on osti.gov, per brief.)
2. **Analytic/arithmetic checks** (`work/analytic_checks.py`): reproduce C1‑C4 from paper‑stated scalars (Courant linearity, CFL magnitude, element‑count products, domain = grid×Δh). → `evidence/analytic_checks.json`.
3. **MMS order test** (`work/mms_order.py`) — the substantive numerical replication of **C5**: reimplement the paper's **exact face treatment** — 1st‑order upwind advective flux (eq 18‑21) + 2nd‑order central diffusive flux (eq 23‑26) — as a discrete flux‑divergence operator `L[n]=d/dz(v·n − D·dn/dz)`. Manufacture smooth `n(z)=exp(sin(2πz/L))` with exact analytic `L[n]`; sweep Δh (nz = 64→4096, periodic to isolate scheme order); measure L∞/L2 error vs analytic and fit observed order `p = slope(log err, log Δh)`. → `evidence/mms_order_result.json`.
4. **Coupled nonlinear streamer toy** (`work/streamer1d_convergence.py`, `work/streamer1d_stable.py`) — attempt at C6/C8: 1D axial drift‑diffusion + tridiagonal Poisson + local‑field ionization, upwind vs Koren. **Unstable at fine Δh** with illustrative bounded transport (explicit source blow‑up); recorded honestly as a failed secondary check, not evidence.
5. **LLM‑judge** (`work/judge.py`): free Argo gpt‑5.2 scores claim coverage/verdict from the evidence. → `evidence/llm_judge.json`.

## 4. Results vs paper

### C1‑C4 — analytic self‑consistency (all pass)
- **C2 Courant linear‑in‑Δt:** implied `C/Δt` slopes = 0.1076, 0.1088, 0.110, 0.110 (per ps); mean 0.1091, **max relative deviation 1.4%** → the stated Courant sequence is consistent with linear scaling in Δt (as required for a fixed‑Δh drift problem).
- **C3 benchmark CFL:** `v·Δt/Δh = 6e5·5e‑13/3.125e‑6 = 0.096` ≈ paper's "≈0.1". ✅
- **C4 element counts:** 4000×3200=12,800,000; 1000×800=800,000; 12500×10000=125,000,000; 16384²=268,435,456 (≈268M); 512×1024=524,288; 32768×1024=33,554,432 (≈33.5M) — **all six exact.** ✅
- **C1 domains:** 12500×1µm = 1.25 cm (z), 10000×1µm = 1.0 cm (r); 4000×3.125µm = 1.25 cm, 3200×3.125µm = 1.0 cm — both grids reconstruct the stated **1.25 cm × 1.0 cm** domain exactly. ✅

### C5 — discretization order (MMS): **first‑order confirmed**
| nz | Δz | L∞ error |
|---|---|---|
| 64 | 1.56e‑2 | 8.20e‑1 |
| 128 | 7.81e‑3 | 4.15e‑1 |
| 256 | 3.91e‑3 | 2.09e‑1 |
| 512 | 1.95e‑3 | 1.05e‑1 |
| 1024 | 9.77e‑4 | 5.23e‑2 |
| 2048 | 4.88e‑4 | 2.62e‑2 |
| 4096 | 2.44e‑4 | 1.31e‑2 |

Successive observed orders: **0.983, 0.992, 0.996, 0.998, 0.999, 1.000** → fitted **p = 0.995 (L∞), 0.997 (L2)**. The error halves each time Δh halves — exactly the paper's stated "linear line … expected error reduction as a function of space step based upon the implemented discretization method" (Fig 7). This independently confirms the mechanism behind the paper's convergence claim (the 1st‑order upwind advection dominates the mixed‑order scheme, giving global O(Δh)). ✅

### C6‑C9 — not reproduced
The coupled peak‑E convergence (<1% at 4µm), the CWI‑benchmark agreement (within 5%), the upwind‑vs‑Koren velocity overestimate, and the strong/weak scaling numbers all require the paper's full nonlinear HPC computation (48 h on 64 procs for one benchmark run) with its local‑field transport tables and the proprietary community‑benchmark reference curves — outside the efficient/free‑only budget. My quick 1D nonlinear surrogate was numerically unstable at fine Δh and is reported as an unsuccessful attempt, not as evidence (no fabricated numbers).

### LLM‑judge (free Argo gpt‑5.2)
Coverage **60%**, overall agreement **moderate**, verdict **PARTIAL**. Judge note: the replication "strongly validates several numerical/arithmetic claims … and independently confirms that the stated base spatial discretization is first‑order accurate (via MMS) … however it does not reproduce the paper's key physics‑output claims tied to the full coupled streamer simulation."

## 5. Verdict justification

Everything independently checkable within the budget was reproduced and **agreed with the paper**: all arithmetic/CFL/scaling self‑consistency (C1‑C4 exact), and — most importantly — the paper's central **discretization‑order claim (C5)** was confirmed to high precision (observed order 0.995≈1.0) by reimplementing the paper's exact upwind+central face fluxes in an MMS test. The end‑to‑end streamer physics (C6‑C9) needs the full HPC run + proprietary benchmark data and was not rerun; my nonlinear surrogate did not stabilize, so I do not claim it. This is a solid partial: core method + all analytic claims reproduced, full‑simulation outputs out of reach.

## Verdict
**Verdict:** PARTIAL

---
WAVE_RESULT set=OSTI paper=2448207 verdict=PARTIAL dir=~/Dropbox/REPLICATE-PROJECT/OSTI-2448207-streamer-discharge-axisymmetric-fluid one_line=Streamer drift-diffusion FV code: all analytic/CFL/element-count claims reproduced exactly and the paper's first-order discretization claim independently confirmed via MMS (observed order 0.995); full HPC streamer benchmark + proprietary CWI data out of scope.
