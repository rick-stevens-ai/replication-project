# Workflow — Bertozzi, Garnett & Laurent (2012) replication

**Paper:** arXiv:1204.1095v1 · SIAM J. Math. Anal. · DOI 10.1137/11081986X
**Type:** Analysis paper (no accompanying code exists) → replication = **independent re-derivation + from-scratch numerical verification** of Section 4's computable predictions.
**Verdict:** REPLICATED (unanimous 3-judge Argo free-tier).

---

## 0. Provenance
- Selected from PDE-100 wave, priority rank 48, score 51.08, cited 60, OA-PDF, repro-ok.
- Publisher HTML (SIAM/T&F/MDPI) Cloudflare-blocked → **arXiv full text + LaTeX source** used as canonical mathematical reference (correct choice for pure-math paper).

## 1. Read + claim extraction
- Read arXiv PDF end-to-end; identified Section 4 (Newtonian case α = 2−d) as the numerically verifiable core.
- Extracted 6 claims (C1–C6). C6 (existence/measure-theoretic global results for 2−d < α < 2) marked out-of-scope for numerical replication up front — recorded honestly rather than silently dropped.

## 2. Independent re-derivation (before touching numerics)
- Radial reduction: v(r) = −m(r)/r^(d−1), m(r) = ∫₀^r s^(d−1)ρ ds → shell ODE dr/dt = −m₀/r^(d−1) → closed-form r(t)^d = r₀^d − d·m₀·t.
- Change of variables z = r^d ⇒ dz/dt = −d·m ⇒ **inviscid Burgers on the half-line**, matching paper eqs. 4.2–4.4 exactly.
- Shock-time formula: t_shock = 1/(d·sup_z m'_init(z)) — re-derived from characteristic-crossing.

## 3. Three independent numerical implementations
Each method deliberately avoids reusing the others' code path, so agreement is genuine cross-check (with the caveat, noted in the critique, that all three assume radial symmetry + monotonicity).

| Method | File | What it tests |
|---|---|---|
| A. Closed-form shell ODE | `aggregation_newtonian.py::run_uniform_ball` | C1, C4 simultaneous-collapse to machine ε |
| B. N-particle Lagrangian (RK4, 1500 particles) | `aggregation_newtonian.py::run_particles`, `check_ordering*.py` | C2 ordering, C4 collapse-time at ~0.3% dt error |
| C. Inviscid Burgers via characteristics on uniform z-grid | `aggregation_newtonian.py::run_burgers_uniform`, `c3_shock_time.py` | C1 equivalence, C3 shock-time formula |

Auxiliary: `aggregation_newtonian.py::run_density_blowup` for C5 measurement of (dρ/dt)/ρ².

## 4. Non-uniform monotone test problems (C3)
- Gaussian ρ = e^(−4r²) and parabolic cap ρ = max(1 − (r/R)², 0)
- Built m_init(z) numerically on uniform-z grid, computed sup_z m'_init(z), compared t_shock formula against observed first blow-up (interior char-cross AND origin-reach — for monotone data these coincide).
- One diagnostic mis-step surfaced: initial `np.gradient` on non-uniform z-grid gave a wrong d=3 Gaussian shock time; **traced, fixed, documented** — clean uniform-grid solve in `c3_shock_time.py` matches theory to machine precision. Recorded in failure_analysis.md.

## 5. Multi-judge assessment (free Argo only)
- `judge.py` → `evidence/judge_verdicts.json`
- Judges: `argo:gpt-5.2`, `argo:gemini-2.5-pro`, `argo:gpt-4.1`
- Opus deliberately excluded per replication brief.
- Standing rule respected: free endpoints only, no paid calls.

## 6. Genuine-critique pass
Rather than accept unanimous REPLICATED and stop, the report includes a dedicated critique section (§5 of REPORT.tex) recording:
- Scope limitation to Newtonian α = 2−d (C6 explicitly not tested).
- Shared assumptions of the three "independent" methods (radial + monotone).
- Interpretation of the 10^(−16) rows in the C3 table (partly tautological — same sup_z m'_init on both sides).
- LLM-judge concordance = inter-rater reliability, not independent verification.
- The transient np.gradient error before the corrected solve.

## 7. Compute + tooling
- Local host: CherryRd.
- numpy 2.4.3 / scipy 1.18.0 (scipy imported but not used for dynamics).
- Judges via free Argo proxy (`http://localhost:44497/v1`, auth `stevens`).
- No paid endpoints; no cloud compute; no GPU needed (pure numpy on CPU).

## 8. Artefacts (see artifacts_summary.md)
Reports, code, evidence JSONs — all under `report/`, `code/`, `evidence/` in the paper directory.
