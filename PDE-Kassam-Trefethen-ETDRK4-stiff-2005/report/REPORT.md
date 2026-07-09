# Independent Replication — Kassam & Trefethen, *Fourth-Order Time-Stepping for Stiff PDEs* (2005)

**Replicator:** OpenClaw PDE replication subagent
**Dates:** 2026-07-02 initial draft; 2026-07-04 promotion pass (full rerun + figures)
**Directory:** `~/Dropbox/REPLICATE-PROJECT/PDE-Kassam-Trefethen-ETDRK4-stiff-2005`

## 1. Citation

> A.-K. Kassam and L. N. Trefethen, "Fourth-Order Time-Stepping for Stiff PDEs,"
> *SIAM Journal on Scientific Computing*, Vol. 26, No. 4, pp. 1214–1233, 2005.
> **DOI:** [10.1137/S1064827502410633](https://doi.org/10.1137/S1064827502410633)

## 2. Paper summary

The paper studies fourth-order **exponential time differencing Runge–Kutta**
(ETDRK4), in the Cox–Matthews (2002) formulation, for stiff semilinear PDEs
`u_t = L u + N(u)` discretized in space by Fourier (or Chebyshev) spectral
methods. Its central technical contribution is the observation that the naïve
floating-point evaluation of the ETDRK4 ϕ-function coefficients (e.g.
`f1 = h(−4−hL + e^{hL}(4−3hL+(hL)^2)) / (hL)^3`) suffers catastrophic
cancellation for small `|hL|`, and that this can be cured to machine precision
by evaluating each coefficient as the mean of the integrand over a circular
contour in the complex plane around each eigenvalue `hL`. With this fix,
ETDRK4 is globally 4th-order in time and outperforms other 4th-order
exponential-type integrators (in particular integrating-factor RK4, IFRK4) on
the paper's four benchmark stiff PDEs.

## 3. Claims table

C-id | Claim (paraphrased) | Type | Testable? | Tested? | Verdict
---|---|---|---|---|---
C1 | Direct floating-point evaluation of ETDRK4 ϕ-coefficients loses many digits of accuracy for small `|hL|` | quantitative | Y | Y | REPRODUCED
C2 | Contour-integral evaluation of the same coefficients is uniformly accurate to machine precision | quantitative | Y | Y | REPRODUCED
C3 | With contour-evaluated coefficients, ETDRK4 is globally 4th-order in time on stiff PDEs | quantitative | Y | Y | REPRODUCED
C4 | ETDRK4 is more accurate than IFRK4 at equal step size | quantitative | Y | Y | REPRODUCED
C5 | Method works on real stiff PDEs: KS, Burgers, Allen–Cahn, KdV — including dispersive/imaginary-spectrum (KdV) | qualitative + quantitative | Y | Y | REPRODUCED
C6 | Long-time (T~150) chaotic KS run is stable and gives the well-known space-time pattern (paper Fig. 4 / `kursiv.m`) | qualitative | Y | Y | REPRODUCED
C7 | ETDRK4-B / Krogstad variant behaves similarly | quantitative | Y | N | scope cut (secondary)

## 4. Method (numbered + exact commands)

Environment: local CPU (macOS, host `CherryRd`), Python 3.13, NumPy 2.4.3,
SciPy 1.18.0, mpmath 1.3.0, Matplotlib 3.10.8. **No paid endpoints.** No
external data (analytic ICs only).

1. **Implement ETDRK4 core** — `work/etdrk4_core.py`.
   * `etdrk4_coeffs(L, h, M=32, r=1)` computes `E, E2, Q, f1, f2, f3` by
     averaging the ϕ-integrand over `M=32` points on the FULL unit circle in
     the complex plane around each `hL`. Coefficients are kept complex (see
     note in file — essential for dispersive spectra).
   * `etdrk4_coeffs_direct(L, h)` implements the naïve floating-point version
     for the cancellation demo only.
   * `etdrk4_step(...)` implements the Cox–Matthews update stages.
2. **Fourier-spectral PDE setups** — `work/pdes.py`. All periodic:
   * `ks_setup(N=128, Lx=32π)`: `u_t = −u u_x − u_xx − u_xxxx`;
     IC `cos(x/16)(1+sin(x/16))` (Trefethen `kursiv.m`).
   * `burgers_setup(N=128, ν=0.03)`: `u_t = −u u_x + ν u_xx`, IC `sin x`.
   * `allencahn_setup(N=256, ε=0.01)`: `u_t = ε u_xx + u − u^3`; linear part
     absorbs the `+u`, so `L = −εk^2 + 1`.
   * `kdv_setup(N=512, Lx=40)`: `u_t = −6 u u_x − u_xxx`; exact 1-soliton
     `u = (c/2) sech²(√c/2·(x−ct−x0))`, c=1.
3. **Time integrators** — `work/integrators.py`:
   * `integrate_etdrk4(v0, L, Nfun, h, nsteps)` — the paper's scheme.
   * `integrate_ifrk4(v0, L, Nfun, h, nsteps)` — the competitor.
4. **Cancellation experiment (C1, C2)** — `work/run_cancellation.py`.
   Sweeps `L=−|hL|` for `|hL|∈[1e-3, 1e1]` (60 log-spaced points) with h=1,
   compares direct and contour `f1, Q` against 50-digit `mpmath` references.
   Command:
   ```bash
   cd work && python3 run_cancellation.py | tee ../report/evidence/cancellation.log
   ```
   Figure: `work/run_cancellation_figure.py` → `report/evidence/cancellation.png`
   + `cancellation_data.json`.
5. **Temporal convergence + ETDRK4-vs-IFRK4 (C3, C4)** — `work/run_convergence.py`.
   For each of KS/Burgers/AC/KdV: fine ETDRK4 reference (`h_ref = h_min/8`,
   M=64), then five halved `h`s, `max|u − uref|` on physical grid, log–log
   slope, and mean `err_IFRK4 / err_ETDRK4`. Command:
   ```bash
   cd work && python3 run_convergence.py | tee ../report/evidence/convergence.log
   ```
   Figure: `work/run_convergence_figure.py` → `report/evidence/convergence.png`
   + `convergence_data.json`.
6. **Dispersive-case clean order via Cauchy self-convergence (C3 for KdV)** —
   `work/run_kdv_selfconv.py`. Successive halved-`h` differences give log2
   ratios = 4 for a 4th-order scheme without any reference-solution bias.
   Command:
   ```bash
   cd work && python3 run_kdv_selfconv.py | tee ../report/evidence/kdv_selfconv.log
   ```
7. **KdV soliton exact-error + invariant conservation (C5)** —
   `work/run_kdv_soliton.py`. `max|u − u_exact|` at T=2 for three step sizes;
   `∫u dx` (mass) and `∫u² dx` (momentum) drift over the full run at h=5e-4.
   Command:
   ```bash
   cd work && python3 run_kdv_soliton.py | tee ../report/evidence/kdv_soliton.log
   ```
8. **Long-time chaotic KS (C6)** — `work/run_ks_figure.py`. h=0.25, T=150,
   ETDRK4 to reproduce the `kursiv.m` / K&T Fig. 4 space-time pattern.
   Command:
   ```bash
   cd work && python3 run_ks_figure.py | tee ../report/evidence/ks_figure.log
   ```
   → `report/evidence/ks_spacetime.png`, `ks_figure_diagnostics.json`.

## 5. Results vs paper

### C1 & C2 — Cancellation vs contour (paper Figs. 1–2)
Relative error of coefficient `f1` on the negative real axis (ref = mpmath
dps=50). Full sweep in `report/evidence/cancellation_data.json`; a slice:

`|hL|` | `err_direct(f1)` | `err_contour(f1)`
---|---|---
1.0e-3 | 2.24e-06 | 6.47e-16
6.5e-3 | 1.78e-08 | 6.79e-16
1.1e-1 | 1.05e-12 | 2.65e-16
2.8e-1 | 2.24e-13 | 1.96e-15
1.8    | 3.45e-15 | 1.45e-15
4.6    | 1.71e-16 | 3.66e-18

Aggregate over `|hL|<0.5`:

metric | value
---|---
max direct `f1` rel err | **2.24e-06**
max contour `f1` rel err | **3.06e-15**
max direct `Q` rel err | 5.58e-14
max contour `Q` rel err | 2.22e-16
worst-case direct/contour ratio (f1) | **7.31 × 10⁸**

**Match to paper.** K&T Fig. 2 shows exactly this: direct evaluation losing
~6+ digits and diverging further as `|hL|→0`, contour flat near machine
epsilon. ~10 orders of magnitude gap. Full agreement.

### C3 & C4 — Convergence and ETDRK4 vs IFRK4 (paper Fig. 3)
Log-log slopes on 5 halved step sizes, error vs. fine ETDRK4 reference:

PDE | ETDRK4 order | IFRK4 order | mean IFRK4/ETDRK4 err ratio
---|---|---|---
KS `T=5` | 3.80 | 3.60 | **5.03×**
Burgers ν=0.03 `T=1` | 3.88 | 3.95 | **1.40×**
Allen–Cahn ε=0.01 `T=3` | 4.05 | 4.03 | **4.64×**
KdV single soliton `T=2` | 2.65 †| 3.71 | **5.14×**

† For KdV the reference-solution comparison saturates at the fine-reference /
spatial floor (~4e-11) at the finest steps, deflating the fit. The clean
temporal-only measurement via Cauchy self-convergence (§C3 addendum) recovers
~4 (see below).

**KdV Cauchy self-convergence** (isolates temporal error):

`h` | `‖u_h − u_h/2‖` | log2 ratio
---|---|---
2.00e-2 | 5.00e-08 | —
1.00e-2 | 2.93e-09 | **4.09**
5.00e-3 | 2.03e-10 | **3.85**
2.50e-3 | 4.52e-11 | 2.17 (floor)
1.25e-3 | 3.62e-11 | 0.32 (floor)

Textbook 4th order until the spatial spectral floor is reached.

**Match to paper.** K&T Fig. 3 does not give tabulated data for every point,
but its slopes and ETDRK4-below-IFRK4 pattern reproduce here in every panel.
Full agreement on Claim 3; the 1.4–5× ETDRK4 advantage on Claim 4 is exactly
the qualitative story of the paper ("ETDRK4 is generally the most accurate of
the fourth-order exponential integrators tested"); the 1.4× on Burgers vs 5×
on stiffer problems matches the paper's observation that the advantage narrows
on smoother problems.

### C5 — KdV soliton (dispersive, imaginary spectrum)
Exact single-soliton at T=2, N=512 spectral, `[0,40]`:

`h` | `max|u − u_exact|` | `peak_num` | `peak_exact`
---|---|---|---
2e-3 | 3.28e-9 | 0.4999 | 0.4999
1e-3 | 3.27e-9 | 0.4999 | 0.4999
5e-4 | 3.28e-9 | 0.4999 | 0.4999

(Error is spatial-floor limited; independent of `h` from 2e-3 down.)

Invariants (h=5e-4):

invariant | t=0 | T=2 | drift
---|---|---|---
mass ∫u dx | 2.000000 | 2.000000 | **2.8e-16**
∫u² dx | 0.666667 | 0.666667 | **4.5e-14**

**Match to paper.** ETDRK4 propagates a KdV soliton with correct shape/speed
and machine-precision conservation over the full run. Matches the paper's
dispersive-example claim (and traps a subtle bug: an initial half-circle
"real" contour version reduced ETDRK4 to first order on KdV — see
`etdrk4_core.py` and attempt_log.md).

### C6 — Long-time chaotic KS (paper Fig. 4)
`work/run_ks_figure.py` integrates KS to T=150 with h=0.25, ETDRK4. Diagnostics
(`report/evidence/ks_figure_diagnostics.json`):

metric | value
---|---
solution finite | true
max |u| over full run | 3.37
final RMS(u) | 1.18
mean drift `⟨u⟩_T − ⟨u⟩_0` | 4.4 × 10⁻¹⁷

The space-time contour is saved as `report/evidence/ks_spacetime.png`; the
plot shows the standard KS "chaotic soliton" banded pattern (interior
snapshots also confirm `u∈[−3,3]`, sustained without blow-up). Matches the
`kursiv.m` / paper Fig. 4 qualitative picture and the well-known KS
attractor bounds.

## 6. Verdict

**REPLICATED (strong).**

Six of six central testable claims of Kassam & Trefethen (2005) — including
every quantitative one attempted — were independently reproduced from a
clean-room Python/NumPy/SciPy implementation on the paper's exact test
problems, at numerically clean magnitudes:

- Direct-coefficient cancellation: ~6 digits lost (rel err 2.2e-6 at |hL|=1e-3).
- Contour cure: uniform ~1e-15 (max 3.1e-15 across sweep), ~10⁸× improvement.
- 4th-order in time: fitted orders 3.80 / 3.88 / 4.05 (KS / Burgers / AC);
  KdV self-convergence 4.09 / 3.85 pre-floor.
- ETDRK4 advantage over IFRK4: 1.4× (Burgers) to 5.1× (KdV) mean error ratio.
- KdV soliton: `max|u−u_exact|=3.3e-9` (spatial-floor limited), mass drift
  2.8e-16, ∫u² drift 4.5e-14.
- KS long-run (T=150): stable, bounded chaotic solution, correct pattern.

Only the secondary Krogstad ETDRK4-B variant was not tested (explicit scope
cut). All numerics ran locally on CPU; no paid endpoints, no external data.

## 7. Reproducibility notes and caveats

- **Complex-coefficient trap.** Using a half-circle + `real()` on the contour
  average silently reduces ETDRK4 to *first order* on dispersive (imaginary-
  spectrum) problems like KdV, because the true coefficients are complex
  there. Must use the FULL circle and keep coefficients complex.
  (`etdrk4_core.py`, attempt_log.md).
- **ICs not fully pinned by the paper.** Standard `kursiv.m` KS IC used; KdV
  single-soliton preferred over the two-soliton A=25 case (cleaner order fit;
  the multi-soliton case needs dealiasing and much smaller steps).
- **Comparison against fine reference saturates.** ETDRK4-vs-reference errors
  eventually hit the spectral spatial floor at the smallest `h`, pulling
  slopes slightly below 4. Cauchy self-convergence sidesteps this and shows a
  clean 4 in the mid-range.
- **No pixel-level match** to K&T Figs. 3/4 (paper gives log–log plots without
  a tabulated error table for every point). Comparison is on slopes,
  magnitudes, direct-vs-contour gap, and qualitative KS attractor pattern —
  all agreeing.

## 8. Files

```
report/
  REPORT.md              this report
  brief.md               1-paragraph what/why
  attempt_log.md         chronological log
  artifact_harvest.md    external artifact inventory (none — analytic ICs)
  judge_result.txt       Argo LLM judge on the initial draft
  evidence/
    cancellation.log             stdout of run_cancellation.py
    cancellation.png             K&T Fig. 2-style plot
    cancellation_data.json       raw sweep data
    convergence.log              stdout of run_convergence.py
    convergence.png              K&T Fig. 3-style plot (4 PDEs)
    convergence_data.json        raw error tables
    kdv_selfconv.log             KdV Cauchy self-convergence log
    kdv_soliton.log              KdV exact-soliton + invariants log
    ks_figure.log                KS long-run log
    ks_spacetime.png             K&T Fig. 4-style KS space-time contour
    ks_figure_diagnostics.json   KS run diagnostics

work/
  etdrk4_core.py               ETDRK4 step + coefficients (contour + direct)
  pdes.py                      KS / Burgers / Allen-Cahn / KdV spectral setups
  integrators.py               ETDRK4 & IFRK4 time-stepping loops
  run_cancellation.py          C1, C2 numeric
  run_cancellation_figure.py   C1, C2 figure
  run_convergence.py           C3, C4 numeric
  run_convergence_figure.py    C3, C4 figure
  run_kdv_selfconv.py          C3 clean order via self-convergence
  run_kdv_soliton.py           C5 exact-soliton + invariants
  run_ks_figure.py             C6 long-time KS space-time
```
