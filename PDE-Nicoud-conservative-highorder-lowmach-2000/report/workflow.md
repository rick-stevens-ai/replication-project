# Workflow — Nicoud (2000) Replication

Chronological workflow for the independent replication of Nicoud, F. (2000),
*Conservative High-Order Finite-Difference Schemes for Low-Mach Number Flows*,
J. Comput. Phys. 158(1), 71–97.

## Stage 0 — Framing

1. Read the paper abstract + method sections; distill claim table (C1–C4).
2. Decide scope: verify **numerical foundations** (C1 spatial order, C2 discrete conservation) with a 1-D operator-level test battery. Explicitly exclude C3 (2nd-order time; we use RK4, strictly stronger for our error budget) and C4 (3-D LES/combustion applications; out of scope for a single-night operator-level replication).
3. Choose the minimum test set that stresses both claims: three method-of-manufactured-solutions (MMS) tests — T1 operator convergence, T2 fully time-integrated variable-density scalar transport, T3 long-time conservation.

## Stage 1 — Design

4. Design test T1 (single-shot operator convergence): manufactured `φ(x) = sin(2πx)·cos(4πx) + 0.3 sin(6πx)`; measure error of (a) the 4th-order conservative divergence vs analytic `dφ/dx`, and (b) the 4th-order 2nd derivative vs analytic `d²φ/dx²`; grid ladder `N ∈ {32, 64, 128, 256, 512}`; report log₂ ratios in both L2 and L∞.
5. Design test T2 (time-integrated variable-density scalar transport with analytic reference): steady `ρ(x) = 1 + 0.4 sin(2πx)`, face velocity `u_f = M/ρ_f` with `M = 1` (so mass flux is exactly constant). Scalar `φ` satisfies `∂(ρφ)/∂t + ∂(Mφ)/∂x = 0`; along characteristics, `φ` is constant, so the reference solution is `φ_exact(x,T) = φ_0(X_0(x,T))`. Invert travel-time integral `τ(x) = ∫ρ/M ds` via cubic spline on `2×10⁵` points. RK4 in time at CFL = 0.2, final `T = 0.2`.
6. Design test T3 (long-time conservation): same steady field, Gaussian initial bump, `N = 128`, integrate to `T = 2.0` (~1067 RK4 steps), monitor totals `Σρ h`, `Σ(ρu)_f h`, `Σρφ h`.
7. Choose implementation: pure NumPy, double precision, periodic 1-D staggered mesh.
8. Choose LLM judge: Argo-hosted `argo:claude-opus-4.7` (per brief), fall back if the Argo proxy schema-validation bug hits (it did — fell back to `opus-4.6`).

## Stage 2 — Implementation

9. Implement `work/nicoud_scheme.py` (~330 lines) with:
   - Staggered-mesh utilities (centers, faces, periodic index arithmetic).
   - 4th-order center↔face interpolation (weights `(9/16, -1/16)`).
   - Conservative divergence with weights `(27, -1)/24`.
   - 4th-order 2nd derivative stencil `(-1, 16, -30, 16, -1)/(12h²)`.
   - RK4 time integrator for `∂(ρφ)/∂t = -div(Mφ)` in conservative form.
   - Characteristic-reference builder (travel-time integral + spline inverse).
   - Test drivers T1, T2, T3, dumping to `report/evidence/results.json`.
10. Implement `work/llm_judge.py`: POST to Argo `chat/completions`, temperature 0, structured JSON request; parse verdict; write to `report/evidence/judge_verdict.json`.

## Stage 3 — Execution

11. Run the full test battery: `python3 work/nicoud_scheme.py > work/run.log 2>&1`. Wall time 2.46 s on `cherryrd`.
12. Run the judge: `python3 work/llm_judge.py`. Latency 9.2 s.
13. Handle Argo proxy fault: `opus-4.7` and `opus-4.8` both return a `SystemMessage | UserMessage | AssistantMessage | ToolMessage` schema-validation error; verified against 5 models — opus-4.5, opus-4.6, sonnet-4.6, and gpt-4o respond cleanly. Fall back to `opus-4.6` and document the fallback in the judge script and evidence file.

## Stage 4 — Verification

14. Inspect `results.json`: check that measured orders for T1 monotonically approach 4 (they do: 3.97 → 3.99 → 4.00 → 4.00 in both L2 and L∞, both operators).
15. Inspect T2: check that spatial order of the full time-integrated solve also approaches 4 (it does: 3.90 → 3.97 → 3.99 → 4.00).
16. Inspect T3: verify final drift for mass and momentum is exactly 0 and scalar drift is `1.11e-16 ≈ 5 ε_mach` after 1067 steps.
17. Cross-check the judge verdict: it agrees, `REPLICATED` on both claims.

## Stage 5 — Reporting

18. Draft `report/REPORT.md` with paper summary, claim table, method, results, judge verdict, and verdict.
19. Draft `report/brief.md` (one-paragraph summary), `report/attempt_log.md` (chronology), `report/artifact_harvest.md` (external artifacts touched).
20. Emit backfilled artifacts: `REPORT.tex`, `open_questions.json` (this stage), `workflow.md` (this file), `artifacts_summary.md`, `failure_analysis.md`.

## Stage 6 — Compliance

21. Confirm no paid endpoints used: all LLM traffic to Argo proxy `127.0.0.1:44497`, key `stevens`; no Anthropic-direct, OpenAI-direct, or OpenRouter traffic. All numerical work on local NumPy (~2.5 s wall). uicgpu not needed — problem is too small.

## Summary

Total wall time: ~2.5 s numerics + ~9 s judge + minutes of human/agent design and reporting. Single-machine, single-implementation, single-night replication. Verdict: **REPLICATED** on C1 (4th-order spatial accuracy) and C2 (discrete conservation), independently confirmed by the LLM judge. See `REPORT.md` §5 and the GENUINE CRITIQUE in `REPORT.tex` §6 for scope caveats.
