# Workflow — Gander & Stuart 1998 Replication

**Paper:** Gander & Stuart, *Space-Time Continuous Analysis of Waveform Relaxation for the Heat Equation*, SIAM J. Sci. Comput. **19**(6):2014–2031, 1998 (DOI 10.1137/S1064827596305337).
**Set:** PDE-100, top-up list rank 77 (208 citations).
**Verdict:** REPLICATED.
**Replication date:** 2026-07-02.

---

## Stage 0 — Paper acquisition

- SIAM (publisher) PDF is paywalled.
- Fell back to the author's copy: `stuart.caltech.edu/publications/pdf/stuart39.pdf`
  (MD5 `a5aebcbf1b51887995c676f3bbf44439`).
- Text extracted into `extraction/marker.md` for downstream reading and claim mining.

## Stage 1 — Claim extraction

- Identified four testable claims from the paper (C1–C4 in the claims table).
- C1: two-subdomain contraction factor `ρ = α(1−β)/(β(1−α))` (Lemma 2.3, Thm 2.4, Thm 2.8).
- C2: rate is robust to mesh refinement at fixed physical overlap (headline result).
- C3: N equal-overlap subdomains: rate ≤ `1 − 4r(1−r)sin²(π/(2(N+1)))` (Thm 3.10), with initial
  stagnation while boundary information propagates inward.
- C4: larger overlap ⇒ faster convergence; §4 numerics.

## Stage 2 — Test problem lock-in (paper eq. 4.1)

- Domain: `x ∈ (0, 1)`, `t ∈ (0, 3)`.
- PDE: `u_t = u_xx − exp(−(t−1)² − (x−1/4)²)`.
- Boundary conditions: `u(0,t) = e^(−2t)`, `u(1,t) = e^(−t)`.
- Initial condition: `u(x, 0) = 1`.
- Discretization: centered 2nd-order FD in space; backward Euler in time; `Δx = Δt = 0.01`.
- All numerics below use exactly this problem unless noted.

## Stage 3 — From-scratch implementation (`work/`)

- Language: Python 3, `numpy` only for the solver; `matplotlib` for figures.
- **`solve_full`**: backward-Euler heat solver on `[0, 1]`, Dirichlet BCs applied every
  time step, hand-rolled Thomas tridiagonal solve per step. This produces the reference
  "true" solution against which the DD algorithm is measured (matches the paper's own
  definition of the error).
- **`solve_subdomain`**: same discretization on a sub-interval, time-dependent Dirichlet
  data at both ends supplied from the neighbor's previous-iterate interface trace over the
  entire time strip — this is the space-time continuous overlapping SWR update
  (paper eqs 2.4–2.7, 2.21–2.24, 3.2–3.3).
- Explicit no-code-reuse commitment: authors distribute no code; every solver line is
  independent.

## Stage 4 — Experiments

1. **`run_two_subdomain` (C1, C4).**
   `Ω₁ = [0, β]`, `Ω₂ = [α, 1]`, initial guess constant-in-time equal to the IC value
   (as specified in the paper). Measured the interface error at grid point `b` vs the
   full-domain solution per iteration; fit the geometric decay to obtain the per-double-
   iteration factor and compared to `ρ`. Overlaps
   `(α, β) ∈ {(0.40, 0.60), (0.45, 0.55), (0.48, 0.52)}`, `Δx = Δt = 0.01`.

2. **`mesh_robust.py` (C2).**
   Fixed overlap `(α, β) = (0.4, 0.6)`; swept `Δx = Δt` through `{0.02, 0.01, 0.005, 0.0025}`
   (8× refinement); measured per-double-iteration factor at each mesh; verified invariance.

3. **`run_N_subdomain` (C3).**
   8 equal subdomains with 35% overlap, snapped to grid; Jacobi-style parallel sweeps;
   measured max interface error (proxy for `‖ξᵏ‖∞`) vs the Thm 3.10 bound; recorded
   stagnation phase length.

## Stage 5 — Judging panel (free Argo)

- Three independent free-Argo LLM referees at `localhost:44497`:
  - `argo:gpt-5.2`
  - `argo:gemini-2.5-pro`
  - `argo:gpt-4.1`
- Each was given the paper claims C1–C4 and the numeric evidence and asked for a
  per-claim verdict plus an overall verdict.
- `argo:claude-opus-4.8` and `argo:claude-opus-4.7` were also attempted but hit an
  Argo chat-endpoint response-serialization quirk; the gpt/gemini panel was used
  (all free endpoints, no paid usage).
- Result: **3 / 3 REPLICATED, unanimous.**
- Full referee texts in `evidence/judges/`.

## Stage 6 — Report assembly

- Numeric tables (C1, C2, C3) generated from `evidence/results.json` and
  `evidence/mesh_robust.json` produced by the from-scratch solver.
- Figures written to `evidence/fig41_two_subdomain.png`, `evidence/fig42_eight_subdomain.png`.
- Markdown report at `report/REPORT.md`; LaTeX version at `report/REPORT.tex`.
- Wave summary token emitted for the coordinator.

## Reproduce (single-line)

```bash
cd ~/Dropbox/REPLICATE-PROJECT/PDE-Gander-Stuart-waveform-relaxation-heat-1998/work \
  && python3 -m venv .venv \
  && . .venv/bin/activate \
  && pip install numpy scipy matplotlib \
  && python swr_heat.py \
  && python mesh_robust.py \
  && python make_figs.py
```

Compute cost: trivial (1D, ~99 interior nodes × 300 time steps × tens of iterations);
runs locally on a laptop in seconds. No GPU / HPC required.
