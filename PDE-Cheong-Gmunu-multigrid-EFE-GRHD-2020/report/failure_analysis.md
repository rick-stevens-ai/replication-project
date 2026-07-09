# Failure analysis

## What worked

- **Independent FAS solver reproduction of algorithmic-heart claims.** After two bug fixes (piecewise-const → bilinear prolongation, FAS coarse-RHS sign), the standalone solver cleanly reproduces V1-vs-V-cycle speedup pattern, monotone-with-depth convergence, saturation at max useful depth, and 2nd-order spatial accuracy. All qualitative predictions from paper §4-§7.1 held up under independent implementation.

## What did NOT work / limitations

### 1. Gmunu source code unreachable
The paper says "open-source" but no repo URL is provided anywhere I could find:
- Not in the paper's own body/references.
- Not on corresponding author Patrick Cheong's academic page (kidcheong.github.io).
- Not returnable from GitHub/GitLab/Bitbucket search for "Gmunu Cheong general-relativistic multigrid".
- Not linked from follow-up papers (Cheong+2021 MNRAS 508, Cheong+2026 arXiv:2510.12978).

**Impact:** All application-level claims (C5 TOV eigenmodes, C6 shocktube, C7 unstable-TOV migration, C8 stable-TOV central-density evolution) are untestable without the full stack. This is the single biggest reason for PARTIAL rather than REPLICATED. If the code were located and buildable, a follow-up wave should target C5 (TOV eigenmodes vs Table 3) as the highest-value confirmatory benchmark.

### 2. First-attempt solver bugs (self-inflicted, fixed)

- **Bug A: piecewise-constant prolongation.** V-cycles stagnated because P-const introduces high-frequency error that GS cannot smooth on the fine grid. Fix: bilinear cell-centred prolongation. Lesson written to: this file.
- **Bug B: FAS coarse-grid RHS sign flip.** Had `rhs_c = -A_uc + dc` (should be `-A_uc - dc`). V-cycles diverged spectacularly. Fix: rederived FAS convention from Brandt's original formulation carefully.
- **Bug C (v1 only): weak source term.** Used compact-support ρ with ρ_max=1e-3, so ψ=1 was nearly the exact solution and initial residual was already 1e-4, making convergence indistinguishable from stagnation. Fix: switch to manufactured solution with a strong (c=10π) nonlinearity and known u_exact so we could see 8-9 orders of magnitude of residual drop.

### 3. LLM-judge 502s

- Argo `argo:claude-opus-4.7` returned upstream 502 on the full judge payload (short-payload sanity checks worked fine). Retried 4×, no success.
- Aggregator route `:4000/v1` returned a LiteLLM Pydantic validation error on the opus-4.7 route ("choices[0].message does not match any variant").
- opus-4.8 direct: also 502.
- **Fallback:** used `argo:claude-sonnet-4.5` (structured JSON, PARTIAL verdict) and cross-checked with `argo:gpt-5.2` via the aggregator. Both converged on PARTIAL with consistent reasoning; documented in `evidence/llm_judge.json`. Free-endpoints policy respected throughout.

### 4. Nougat not run

CherryRd lacks a Nougat install, and the DOI is not in the central Nougat corpus cache. pdftotext yielded a clean 2111-line extraction sufficient for claim-tabulation, so we shipped the placeholder rather than blocking on a 10-30 min Nougat cold-start. Transparent in `artifacts_summary.md`.

## What a future replicator should try

1. **Locate the Gmunu repo.** Email Patrick Cheong (chi-kit.cheong@ligo.org) or check his current institutional pages. If located, clone and try to reproduce Fig. 11 numbers exactly.
2. **Reproduce TOV eigenmode frequencies (Table 3).** Highest-value physics claim; would move verdict from PARTIAL → REPLICATED for the physics side.
3. **Cross-check my FAS solver against a professional MG library** (e.g. PyAMG's `smoothed_aggregation_solver` in nonlinear mode, or hypre's BoomerAMG) to rule out any residual bug in my implementation.
4. **Repeat on spherical polar grid** to match the paper's geometry more directly; the pole singularity may introduce convergence-rate degradations not visible in my Cartesian test.

## Same-failure-twice prevention

- **Multigrid FAS sign convention:** always start from Brandt 1977 / Trottenberg-Oosterlee-Schüller convention `A_c(u_c^new) = A_c(R u_h) + R (b_h - A_h(u_h))`; the "add restricted defect" is a `+`, and be extra careful whether your stored variable is `b_eff` or `-b_eff`. Recorded to `memory/failure-log.md` in workspace.
- **Weak-source problem trap:** if r0 is unusually small, ψ_init may already be the answer; use MMS with known u_exact to remove ambiguity.
- **Piecewise-const prolongation is broken for nonlinear MG in practice** — use bilinear (cell-centred 9-point) as default.
