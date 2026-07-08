# OSTI 1559043 — Replication Report (v6)

**Paper:** Jaravel et al. 2019, *Numerical study of the ignition behavior of a
post-discharge kernel in a turbulent stratified cross-flow.*

**Status:** **CLOSED** — full 5-ms / AMR-L=1 sweep finished on uicgpu (8× A100,
CUDA build). All 4 φ cases reached `stop_time = 5.0e-3 s` with the
paper-faithful single-criterion ignition test. **Self-score: Coverage 8/10,
Agreement 8/10, Overall 8/10.**

> **PDF report:** `report/1559043_replication_report_v6.pdf`
> **Analyzer:** `replication-pelec/uicgpu_ensemble_v5/analyze_v6.py`
> **Per-run summary:** `replication-pelec/uicgpu_ensemble_v5/summary.json`
> **Figures:** `replication-pelec/uicgpu_ensemble_v5/figures/`
> **Raw filtered logs:** `replication-pelec/uicgpu_ensemble_v5/raw_runs/phi_*_run.log`
> **inputs.inp per φ:** `replication-pelec/uicgpu_ensemble_v5/inputs/phi_*_inputs.inp`

---

## What changed since v5

| Aspect | v5 (Apr-28) | v6 (this report, May-26) |
|---|---|---|
| Compute | Polaris preemptable queue | **uicgpu 8× A100 80GB, CUDA, interactive** |
| φ=1.0, φ=1.2 completion | 32 % (~1.6 ms, preempted) | **100 % (full 5 ms)** |
| Window | 5 ms target, 4 of 4 short | **5 ms reached on all 4** |
| AMR | L=1 (125 μm effective) | **L=1 (unchanged)** |
| Realizations per φ | 5 (jittered, partial) | **1 (deterministic)** |
| Total runs | 20 (mixed completion) | **4 (complete)** |
| Aggregate IP shape | (0, 0, 1, 1) | **(0, 0, 1, 1)** |

**Key honest caveat:** v6 trades ensemble breadth for window completion. v5 had
N=5/φ but only the φ=0.6/0.8 runs reached 5 ms; v6 has N=1/φ but every run
reached 5 ms. Both yield the same IP shape (0/0/1/1) and the same L1 distance
to the paper's IP curve (0.65). The v6 contribution is **decisive evidence
that φ=1.0 and φ=1.2 ignite and stay ignited over the full 5-ms window**, not
just to the v5 preemption point at ~1.6 ms.

---

## Methodology

**Solver:** PeleC v25.12 (master, May 2026), CUDA build on uicgpu A100s. SUNDIALS
chemistry integrator. drm19 (21 species, methane–air) mechanism. AMR L=1 (one
refined level, refinement ratio 2 → 125 μm effective). Domain
32×16×16 mm, base grid 128×64×64.

**Configuration:** identical `inputs.inp` per φ except `prob.equiv_ratio` and
the `stop_time = 5.0e-3` / `amr.max_level = 1` overrides at the bottom (which
override the earlier `1.0e-3` / `0` values per AMReX inputs-file semantics).
Hot post-discharge kernel (T=3300 K, r=0.2 cm) seeded at the splitter
interface in a turbulent stratified crossflow (T=456 K, P=1 atm).

**Realization count:** **N=1 per φ**. The inputs file has no jitter or
random-seed parameter, so the run is deterministic given the same build and
GPU. We launched 4 jobs in parallel (one per φ, one GPU each) via
`runs_uicgpu/master.log`-driven shell launcher.

**Ignition criterion (paper-faithful, identical to v5):**

> A run is **ignited** iff `T_max(t_end) > 2000 K`, i.e. a self-sustaining
> hot region remains at the end of the 5-ms window. A kernel that
> transiently spikes to 3300 K (the seed value) but quenches back to inflow
> temperature (456 K) is **not** counted as ignited.

This is the single, end-of-window test from v5 §3. No dual-criterion shenanigans.

---

## Per-run results

| φ   | t_final (ms) | T_global_max (K) | T_late_max (K)¹ | T_end (K) | P_end (atm) | Ignited? |
|-----|--------------|------------------|------------------|-----------|-------------|----------|
| 0.6 | 4.999 | 3363 | 620  | 456  | 1.00 | **no** (quenched, fully diluted to inflow) |
| 0.8 | 5.000 | 3375 | 2262 | 459  | 1.02 | **no** (late plateau then quench) |
| 1.0 | 5.000 | 3383 | 3023 | 2666 | 3.32 | **yes** (sustained) |
| 1.2 | 5.000 | 3390 | 3140 | 2705 | 3.38 | **yes** (sustained) |

¹ `T_late_max = max(T_max(t))` for `t > 1.5 ms`.

The pressure rise (1.0 → 3.3 atm) for the ignited cases is itself a clean
indicator: the unburnt cases stay at injection pressure (≈1 atm), while
sustained combustion produces a confined ~3× pressure rise consistent with
constant-volume heat release.

The φ=0.8 case is the most interesting numerically: it reaches a late
reactive plateau (T_max ≈ 2262 K between ~1 and ~3 ms) and then collapses
back to inflow temperature. This is the "marginal" regime where the paper
sees 20 % IP — a small jitter ensemble would catch the occasional success
here.

## Ignition probability table

| φ   | N | N_ignited | IP_v6 | Wilson 1σ band | Paper IP | Δ vs paper |
|-----|---|-----------|--------|------------------|----------|------------|
| 0.6 | 1 | 0 | **0.00** | [0.00, 0.50] | 0.00 | 0.00 |
| 0.8 | 1 | 0 | **0.00** | [0.00, 0.50] | 0.20 | −0.20 |
| 1.0 | 1 | 1 | **1.00** | [0.50, 1.00] | 0.65 | +0.35 |
| 1.2 | 1 | 1 | **1.00** | [0.50, 1.00] | 0.90 | +0.10 |

**L1 distance to paper IP curve: 0.65** (identical aggregate to v5; the v6
realization sits inside v5's Wilson band for every φ).

**The v6 IP curve qualitatively matches the paper** (monotone S-shape,
sharp φ≈0.9 transition) but is **steeper** and **saturates early**. The
divergences are exactly the same as v4 and v5:

- **φ=0.8 (−0.20):** Our marginal case quenches. Paper sees 1 of 5 ignite.
  With N=1 this is the expected outcome 80 % of the time; we'd need an
  ensemble (or longer windows) to recover the 0.2 probability.
- **φ=1.0 (+0.35):** Paper sees 65 %; we see 100 %. Likely cause is
  under-resolved turbulent quenching at our 125 μm effective resolution
  vs the paper's deeper AMR.
- **φ=1.2 (+0.10):** Paper sees 90 %; we see 100 %. Same root cause but
  smaller.

## Comparison with paper Fig 3

![IP vs phi (v6 vs paper)](replication-pelec/uicgpu_ensemble_v5/figures/ip_vs_phi.png)

The two curves bracket the same transition; the v6 curve is the sharp
step-function limit of the paper's smoother sigmoid.

## T_max(t) trace — all 4 φ overlaid

![T_max all phi](replication-pelec/uicgpu_ensemble_v5/figures/tmax_timeseries_phi_all.png)

All traces share the initial kernel spike (T=3300 K at t=0). After ~0.5 ms
the φ=0.6 trace collapses; φ=0.8 sustains a ~2200 K plateau through ~3 ms
and then collapses; φ=1.0 and φ=1.2 climb to and stay at ~2700 K through
5 ms.

The combined panel (T_max + P_max) is at
`replication-pelec/uicgpu_ensemble_v5/figures/tmax_pmax_panel.png`.

## Score

| Axis | v4 | v5 | v6 | Justification |
|---|---|---|---|---|
| Coverage | 7/10 | 8/10 | **8/10** | All 4 φ → 5 ms with AMR L=1. Lost a point vs v5's stated ceiling of 9 because realization count dropped from 5 to 1 (no jitter ensemble). |
| Agreement | 7/10 | 8/10 | **8/10** | IP curve qualitatively matches; L1=0.65 unchanged. Monotone S-curve, correct ignition/quench split at φ≈0.9. |
| Overall | 7/10 | 8/10 | **8/10** | Net: same agreement as v5, full window completion, but at lower statistical depth. |

The v5 self-stated ceiling of "9/10 once φ=1.0 hits 5 ms" assumed the v5
ensemble would be completed (N=5/φ at 5 ms). v6 met the window requirement
but at N=1/φ, so we don't claim the extra point; honest call is to hold at
8/10.

## Limitations

1. **N=1 per φ** — no jitter ensemble, so the Wilson bands are wide ([0, 0.5]
   or [0.5, 1.0]) and we cannot resolve the paper's 0.2 / 0.65 / 0.9
   intermediate probabilities.
2. **Resolution** — 125 μm effective (AMR L=1) is finer than v4's 250 μm
   but still coarser than the paper's L=2 nested refinement near the
   kernel and reaction zone.
3. **Synthetic turbulent inflow** — same as v4/v5; not the paper's
   tabulated DNS inflow.
4. **drm19 chemistry** — paper uses a richer methane–air mechanism.
5. **Single hardware target** — runs are on one A100 each; we did not
   verify cross-hardware reproducibility (uicgpu A100 vs Polaris A100 vs
   Aurora Intel Max).

## Follow-ons (not in v6 scope)

- Re-run the 5×4 jitter ensemble on uicgpu now that the per-φ wallclock
  is known (φ=0.6: ~17 h; φ=1.2: ~11 days at AMR L=1 on 1× A100). With 8
  GPUs we can launch 8 realizations in parallel; the bottleneck is
  φ=1.0/1.2 wallclock, not GPU availability.
- Push AMR to L=2 (62.5 μm effective) at fixed φ=1.0 and see whether the
  N=1 IP shifts off 1.0 — would directly test the "under-resolved
  turbulent quenching" hypothesis.
- Cross-validate one φ=1.0 run on Aurora and on Polaris with identical
  inputs to confirm hardware/build invariance.

## Reproducibility pointers

- **Run dirs (uicgpu):** `/data/stevens/projects/pelec-build/runs_uicgpu/phi_{0.6,0.8,1.0,1.2}/`
  with `run.log`, `inputs.inp`, `chk*` checkpoints, `plt*` plotfiles.
- **Launcher:** `~/Dropbox/REPLICATE-PROJECT/1559043-ignition-kernel-turbulent/replication-pelec/uicgpu_ensemble_v5/master.log`
  (4 parallel `nohup PeleC ... &` invocations, one per GPU).
- **Filtered logs synced to cherryrd:** `replication-pelec/uicgpu_ensemble_v5/raw_runs/`
  (only TIME / Temp / pressure / MASS / STEP / FUEL lines; full logs are 150 MB
  and remain on uicgpu).
- **Analyzer:** `replication-pelec/uicgpu_ensemble_v5/analyze_v6.py`
- **Per-run JSON:** `replication-pelec/uicgpu_ensemble_v5/summary.json`
- **PDF:** `report/1559043_replication_report_v6.pdf`

---

*Generated 2026-05-26 by Ollie (OpenClaw subagent, argo/claude-opus-4.7,
free Argo proxy).*
