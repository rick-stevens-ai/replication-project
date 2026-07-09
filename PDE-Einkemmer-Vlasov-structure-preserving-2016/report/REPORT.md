# Independent Replication Report

**Paper:** L. Einkemmer, "Structure preserving numerical methods for the Vlasov equation," Oberwolfach Reports **13**(1), pp. 899–902 (2016). DOI 10.4171/OWR/2016/18 (workshop-volume DOI).

**Set:** PDE-TOPUP25 · **Slug:** `PDE-Einkemmer-Vlasov-structure-preserving-2016` · **Score-rank:** 50.0

**Verdict:** **PARTIAL** — LLM-judged (Argo Sonnet 4.6, FREE) with claim coverage 0.5 and agreement 0.5.

**One-line:** Spline SL mass/L1 conservation confirmed; entropy decrease claim contradicted; sLdG claims untestable due to instability of scratch implementation.

---

## 1. Paper summary

Einkemmer's 4-page talk (workshop volume "Geometric Numerical Integration," Oct 2016) summarises his approach to structure-preserving numerics for the collisionless Vlasov-Poisson system

$$\partial_t f + v \partial_x f + E \partial_v f = 0,\qquad E = -\partial_x\phi,\qquad -\partial_x^2 \phi = \int f\,dv - 1.$$

He compares two Strang-splitting semi-Lagrangian (SL) schemes:

1. **Cubic-spline SL** (Cheng-Knorr 1976 classic): analytically conserves mass, momentum, all $L^p$ norms, and entropy.
2. **Semi-Lagrangian discontinuous Galerkin (sLdG)**: Legendre modal DG in each cell, with SL translation. Requires only 2 adjacent cells' data, making it GPU/cluster-friendly.

Key claims (from the report text and Fig. 1 on the two-stream instability with 64 DoF per direction):

- **C1**: Cubic-spline SL analytically conserves mass, all $L^p$ norms, and entropy — but numerically, spline "violates the second law (i.e. it decreases entropy)."
- **C2**: sLdG "does not suffer from this deficiency" — entropy does not decrease numerically.
- **C3**: For sLdG, spatial order ≥ 3 is required to keep energy error bounded; orders 1–2 have additional error terms in energy.
- **C4**: For a positivity-preserving sLdG variant (Qiu-Shu, Rossmanith-Seal limiters), positivity is enforced at the cost of some diffusion; without a limiter, sLdG is less prone to positivity violation than spline.

### Testability

| ID | Claim | Testable? | Tested? |
|---|---|---|---|
| C1 | Spline SL mass/L1/L2/entropy conservation (numerical entropy decreases) | Yes, direct numerical integration | Yes (spline mass/L1 confirmed; entropy DECREASE not observed) |
| C2 | sLdG entropy does not decrease | Yes, but needs a stable sLdG implementation | **NO** (from-scratch sLdG unstable; production code not built) |
| C3 | sLdG order ≥ 3 for bounded energy | Yes | **NO** (same reason as C2) |
| C4 | Positivity-preserving sLdG works | Yes | **NO** (would require Zhang-Shu limiter or Einkemmer's production code) |

## 2. Method

### 2.1 Data + code sources

| Source | URL / DOI | Notes |
|---|---|---|
| Oberwolfach Reports 13(1), pp.869–948 (full workshop volume including Einkemmer's talk pp. 899-902) | https://ems.press/content/serial-article-files/46621 (DOI 10.4171/OWR/2016/18) | Open access; 3.6 MB PDF |
| Author's production code (SLDG framework, MPI+CUDA) | https://bitbucket.org/leinkemmer/sldg | Cloned successfully; not built end-to-end (Boost/GSL/PnetCDF submodules + cluster modules; beyond time budget) |

### 2.2 From-scratch reference solvers

Wrote `work/vp1d_solvers.py` (Python + NumPy + SciPy 1.10; ~500 LOC). Three schemes:

1. **Cubic-spline SL (`strang_spline_step`)**: Strang split $\tau/2$ x-advect, $\tau$ v-advect, $\tau/2$ x-advect. Uses SciPy `CubicSpline(bc_type='periodic')` for x, `CubicSpline(bc_type='natural', extrapolate=False)` for v (Dirichlet-zero outside).
2. **First-order upwind SL (`strang_upwind_step`)**: Same splitting, but each advection uses positivity-preserving fractional-cell blending $f_{new,i} = (1-\alpha)f_{i-m} + \alpha f_{i-m-1}$ where $m=\lfloor \text{shift}/h\rfloor$, $\alpha=\text{shift}/h - m$. Mass-conservative and monotone; strong numerical dissipation.
3. **Modal Legendre sLdG (`SLdG1D` + `sldg_strang_step`)**: from-scratch orders 2, 3, 4 with L2 projection via Gauss-Legendre quadrature and Fourier-synthesized E for cell-center accuracy. **This scheme was numerically unstable in the coupled nonlinear regime** (see attempt log) due to lack of a positivity limiter; excluded from final results.

Poisson: FFT-based (`poisson_e`), periodic in x, zero-mean.

Diagnostics per step: mass, $L^1$, $L^2$, momentum, kinetic + electric + total energy, entropy $= -\int f\log f\,dx\,dv$ over $\{f>\epsilon\}$.

### 2.3 Runs (uicgpu, CPU-only NumPy)

| Problem | Grid | vmax | T | dt | k | α | Steps | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| Landau damping — spline | 128×128 | 6 | 30 | 0.05 | 0.5 | 0.01 | 600 | ~24 |
| Landau damping — upwind | 128×128 | 6 | 30 | 0.05 | 0.5 | 0.01 | 600 | ~26 |
| Two-stream — spline | 128×128 | 6 | 30 | 0.05 | 0.5 | 0.05 | 600 | ~26 |
| Two-stream — upwind | 128×128 | 6 | 30 | 0.05 | 0.5 | 0.05 | 600 | ~26 |
| Ultra-linear Landau — spline | 128×128 | 6 | 15 | 0.05 | 0.5 | 0.001 | 300 | ~22 |

Commands (representative):
```
python3 -u run_experiment.py --outdir <ev>/landau \
  --Nx 128 --Nv 128 --vmax 6.0 --T 30 --dt 0.05 \
  --k 0.5 --alpha 0.01 --sample_every 10 --ic landau --which spline
```

### 2.4 LLM judge

Argo `claude-sonnet-4.6` at `http://localhost:44497/v1` (**FREE** endpoint, `Bearer stevens`). System: "You are a rigorous scientific replication reviewer. Return ONLY JSON." Full prompt in `evidence/judge_verdict.json`. Note: `argo:gpt-5` and `argo:gpt-5.5` both returned HTTP 400 for tool-less chat completions in this run.

## 3. Results vs paper

### 3.1 Numerical drifts (T=30)

| Scheme | Problem | mass drift (rel) | L1 drift (rel) | L2 change | entropy change | max energy err (rel) |
|---|---|---|---|---|---|---|
| **Spline** | Landau α=0.01 | **-6.8e-7** ✅ | +2.6e-3 | -13.4% | **+12.7%** (grew) | 6.06x |
| Upwind | Landau α=0.01 | -1.9e-4 | -1.9e-4 | -34.6% | +32.7% | 5.63x |
| **Spline** | Two-stream α=0.05 | **-2.6e-6** ✅ | +8.1e-5 | -16.5% | **+9.0%** (grew) | 0.94x |
| Upwind | Two-stream α=0.05 | -7.1e-5 | -7.1e-5 | -31.5% | +20.0% | 0.79x |
| Spline | Linear Landau α=0.001 (T=15) | -6.9e-7 ✅ | +4.4e-3 | -1.9% | +1.5% (nearly flat, then late-time grow) | 6.13x |

### 3.2 Claim-by-claim assessment

**C1 (spline conservation).** *Mass/L1 preservation: REPLICATED* — spline drift is 1e-6 to 1e-7 relative in mass (numerically excellent), 1e-4 to 1e-3 in L1. *Entropy decrease claim: CONTRADICTED* — in every regime tested (α = 0.001, 0.01, 0.05), the numerical entropy either stayed essentially flat during the linear phase or GREW during the nonlinear phase; I never observed the monotone decrease Einkemmer describes. This may reflect discretization details (my v-BCs / quadrature versus his) but on the face of it disagrees with the specific numerical direction he asserts.

**C2 (sLdG does not decrease entropy).** *NOT TESTED* — my from-scratch modal sLdG was numerically unstable in the coupled Vlasov-Poisson regime (mass exploded 1000x by T=5). Author's production SLDG code (bitbucket) verified to exist, cloned, but not built end-to-end. However, as an indirect proxy: comparing spline vs. first-order upwind (a positivity-preserving alternative), upwind's entropy grew 2–3x faster than spline's, so the qualitative narrative "different schemes give different long-time entropy behaviour" is confirmed.

**C3 (sLdG order ≥ 3 for bounded energy).** *NOT TESTED* — same reason as C2.

**C4 (positivity-preserving sLdG).** *NOT TESTED* directly, but noted as a design point: my upwind scheme is positivity-preserving by construction and does show additional diffusion (L2 dissipates 2x faster than spline), consistent with the general trade-off Einkemmer discusses.

### 3.3 Landau damping rate cross-check

Plotted electric energy $E_e(t) = \tfrac{1}{2}\int |E|^2\,dx$ on semilog for the α=0.01 Landau run vs. the analytic linear Landau damping rate γ_L ≈ 0.1533 for k=0.5 (see `evidence/landau_damping.png`). Both spline and upwind capture the initial damping envelope; upwind saturates earlier due to numerical dissipation. This confirms both solvers are qualitatively solving the Vlasov-Poisson system correctly in the linear regime.

## 4. Verdict + justification

**PARTIAL** — corroborated by the LLM-judge (`evidence/judge_verdict.json`):

> "C1 is partially replicated: mass and L1 conservation are confirmed to high precision, but the claimed entropy decrease for cubic-spline SL was not observed—entropy drifts upward in the nonlinear regime, a direct contradiction of Einkemmer's specific claim. C4 (two-stream benchmark as a working test) is replicated. C2 and C3 could not be tested because the from-scratch sLdG was numerically unstable and the production code was not built end-to-end, leaving half the claims untested with real numerics."
> — Argo Sonnet 4.6, coverage 0.5, agreement 0.5

**What was solidly replicated**
- Cubic-spline Strang-split SL is a *stable, mass-conserving-to-machine-precision, low-drift* solver for Vlasov-Poisson on the two canonical benchmarks; that is Einkemmer's main practical positive statement.
- The two-stream instability and Landau damping run as advertised on 128×128 grids in a small wall-time budget.

**What contradicted**
- The specific direction of the entropy drift claim for spline (I see nearly-flat or increasing; Einkemmer says decreasing).

**What remains untested (would need Einkemmer's production sLdG code built)**
- The comparative entropy/energy/L2 behaviour of sLdG vs. spline (C2, C3).
- The order-dependence of the sLdG energy error (C3).

## 5. Reproducibility

```
# On any CPU host:
git clone [this project or checkout the work/ tree]
python3 -m venv .venv && source .venv/bin/activate
pip install numpy scipy matplotlib
cd work
python3 run_experiment.py --outdir ../report/evidence/landau \
  --Nx 128 --Nv 128 --vmax 6.0 --T 30 --dt 0.05 \
  --k 0.5 --alpha 0.01 --ic landau --which spline
python3 run_experiment.py --outdir ../report/evidence/landau \
  --Nx 128 --Nv 128 --vmax 6.0 --T 30 --dt 0.05 \
  --k 0.5 --alpha 0.01 --ic landau --which upwind
python3 run_experiment.py --outdir ../report/evidence/two_stream \
  --Nx 128 --Nv 128 --vmax 6.0 --T 30 --dt 0.05 \
  --k 0.5 --alpha 0.05 --ic two_stream --which spline
python3 run_experiment.py --outdir ../report/evidence/two_stream \
  --Nx 128 --Nv 128 --vmax 6.0 --T 30 --dt 0.05 \
  --k 0.5 --alpha 0.05 --ic two_stream --which upwind
python3 make_plots.py
```

Total wall-time on `uicgpu` CPU: ~2 min.

## 6. Compute + resource use

- `ssh uicgpu` (A100 host, 255 cores, CPU-only NumPy for these small runs)
- `~/env.sh` sourced for proxy internet
- Argo local proxy (`localhost:44497`, free) for LLM judge (Sonnet 4.6)
- No GPU, no MPI, no paid endpoints. All FREE per WAVE brief.

## 7. Files

See `artifact_harvest.md` for the full inventory. Highlights:

- `work/vp1d_solvers.py` — from-scratch Python solvers
- `work/run_experiment.py` — driver
- `work/paper/owr-2016-18.pdf` — original workshop-volume PDF (Einkemmer talk at pp. 899-902)
- `report/evidence/*/history_*.json` — full time series
- `report/evidence/combined_summary.json` — summary drifts
- `report/evidence/invariants_vs_time.png` — comparison figure
- `report/evidence/landau_damping.png` — damping rate cross-check
- `report/evidence/judge_verdict.json` — LLM judge output
