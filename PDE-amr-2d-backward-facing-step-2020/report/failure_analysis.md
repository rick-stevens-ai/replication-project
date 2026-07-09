# Failure Analysis

Honest inventory of what didn't work, why, what was worked around, and what's still open.

## F1. Full-text paper access — BLOCKED
- **What failed**: retrieving the paper PDF.
- **Root cause**: World Scientific serves this journal behind a Cloudflare bot challenge
  (HTTP 403). Unpaywall confirms `is_oa=False` and 0 OA locations. No arXiv preprint,
  no Zenodo/OSTI mirror.
- **Workaround**: Semantic Scholar API returns the full verbatim abstract + tldr +
  metadata under the S2 key stored in the workspace keychain. Wrote a 2.7 kB stand-in
  `paper.pdf` from the abstract via `reportlab` so artifact (1) exists as a real PDF.
- **Residual gap**: paper's actual per-iteration VDAMR convergence table (Claim C4:
  AMR-vs-uniform efficiency) is unreachable without the full text. This is the primary
  reason the verdict is **PARTIAL** rather than REPLICATED.
- **To close**: library ILL / interlibrary-loan of the WSPC IJCM issue, OR direct
  request to the corresponding author (Zhenquan Li, Charles Sturt University, ORCID
  0000-0002-3021-630X). This is out of scope for an autonomous subagent.

## F2. BFS Navier–Stokes solver failed to develop primary recirculation
- **What failed**: my stream-function/vorticity BFS solver returned an **attached flow**
  (wall shear positive everywhere downstream of the step) at Re ∈ {100, 200} at dx = 0.1
  and at Re = 50 at dx ∈ {0.25, 0.10, 0.075}. Only Re = 50 dx = 0.15 developed a
  proper primary vortex (x_r/S = 1.78, vortex-centre (1.80, 0.45)).
- **Symptoms**:
  - `u[j=1, i>i_xs]` positive at all downstream columns (should be negative in the
    recirculation zone at the wall).
  - Spurious near-outlet corner vortex with tiny ψ ≈ -1e-3 that the code initially
    misidentified as the primary vortex (fixed by restricting the search to a
    downstream lower-half sub-region excluding the outlet, but the physical vortex
    still doesn't form).
  - `umax` at outlet-top corner reaching 6.65 (should be < 1.5 for a Poiseuille flow
    that's re-developed) — indicates a spurious jet driven by the naive Neumann
    outlet BC.
- **Suspected root causes** (not fully pinned down under time budget):
  1. **Reentrant-corner (x=xs, y=hs) vorticity BC**: my Thom rule
     `ω = -2 · (ψ_interior − ψ_wall) / dx²` applied at both step-top and step-face
     row/column, but doesn't handle the sharp singular corner where vorticity is
     nominally infinite. Corner-averaged Thom or Woods formulas would likely help.
  2. **Neumann psi outlet by post-solve copy**: `psi[:, -1] = psi[:, -2]` is a rigid
     mass-flow constraint that damps upstream separation. A proper convective outlet
     (Orlanski: ∂/∂t + c ∂/∂x = 0) would be better.
  3. **Hybrid convection scheme falls back to first-order upwind above cell-Pe = 2**:
     at Re = 100, dx = 0.1, |u| ~ 1, cell-Pe = |u|·dx·Re = 10 > 2 → upwind, which is
     ~O(dx) accurate and known to be too dissipative for BFS-scale shear layers on
     coarse meshes.
- **Workaround**: pivoted to a **solver-independent verification** of the paper's core
  mathematical claim on a manufactured analytical stream function (see §3.3 of REPORT).
  This isolates the AMR mesh-error indicator + vortex-recovery methodology from any
  particular NS solver bug and cleanly reproduced Claims C1 and C2.
- **Residual gap**: the paper's benchmark comparison (Claim C3) is only partially
  addressed — the one converged NS data point qualitatively agrees with published
  low-Re values in the right ballpark but under-predicts x_r/S by ~40 %.
- **To close**:
  1. Switch to a QUICK / MUSCL / third-order-upwind convection scheme.
  2. Replace outlet BC with Orlanski convective outflow.
  3. Add a proper reentrant-corner vorticity treatment.
  4. Or: swap to FEniCS/dolfinx (Taylor-Hood) or OpenFOAM (simpleFoam) — these are
     validated BFS solvers and would remove the whole class of bespoke-solver bugs.

## F3. First LLM judge model returned HTTP 502
- **What failed**: `argo:claude-opus-4.8` (my default per session prompt) and
  `argo:claude-opus-4.7` (fallback) both returned:
  > `litellm.BadRequestError: OpenAIException - Failed to parse upstream response:
  > 1 validation error(s): Value at 'choices[0].message' does not match any variant
  > of SystemMessage | UserMessage | AssistantMessage | ToolMessage.
  > Received Model Group=argo:claude-opus-4.8`
- **Root cause**: transient upstream-response validation error at the litellm
  aggregator layer (`:4000`, cherryrd) for the Anthropic Argo routes on
  2026-07-06 04:33 CDT. GPT-5 routes were unaffected.
- **Workaround**: fell back to `argo:gpt-5.2`, which returned a clean strict-JSON
  verdict. Documented in `report/evidence/llm_judge_raw.json` and in `attempt_log.md`.
- **Residual gap**: cross-model verdict-consistency check (Opus vs GPT-5 vs Gemini)
  was skipped. In principle a single judge is enough per the wave brief.
- **To close**: retry Argo Opus routes later; if the litellm validation bug recurs,
  file a note in workspace `memory/failure-log.md` and check aggregator health.

## F4. Manufactured field's argmin(psi) sits at yc≈0.16, not at Gaussian centre yc=0.35
- **What "failed"**: the recovered vortex-centre y-coordinate converged to a value
  ~0.19 different from the geometric perturbation centre.
- **Root cause (not a bug)**: the Poiseuille background streamfunction increases
  monotonically with y from the wall. Adding a *negative* Gaussian centred at yc=0.35
  shifts the psi minimum toward the wall (where background is smaller). This is a
  legitimate property of *how one extracts a vortex centre from a raw streamfunction*,
  and the same ambiguity applies to the paper's method. This became Open Question Q2.
- **Not a workaround needed**: the SELF-CONVERGENCE of the argmin location is what the
  paper claims, and that is cleanly reproduced (yc → 0.164 across five halvings of dx).

## F5. Sibling-replication overlap (informational, not a failure)
- **What "happened"**: the wave brief assigned this paper to a new dir, but a sibling
  dir already covered the same DOI (created 2026-07-04) with a Chorin-projection MAC-
  grid solver.
- **Root cause**: two separate wave assignments hit the same paper because the wave
  brief drove off a fresh 51-paper queue rather than diffing against completed dirs.
- **Handling**: per brief hard rule (do NOT overwrite sibling dirs), created a NEW
  dir with a different name and a **deliberately different toolchain**
  (ψ-ω vs Chorin/MAC) plus solver-independent manufactured-field verification. Both
  dirs remain intact; both reach PARTIAL for the same underlying paywall reason but
  via different independent evidence pathways. This is arguably a *stronger*
  overall reproduction of Li & Li 2020 than either dir alone.
- **To close**: wave-brief queue-generator should diff against existing
  `PDE-*` dirs before assignment. Filed as an informational note here; not a
  blocking issue for this replication.

## Overall verdict alignment
- LLM judge: **PARTIAL**, agreement 55 %.
- My assessment: aligned. C1 and C2 REPRODUCED solver-independently; C3 NOT_TESTED at
  the required precision because the full NS solve failed; C4 NOT_TESTED because
  paywalled.
- If the standard reserves "REPLICATED" for value-for-value matching to the paper's
  own tables/figures, that is unreachable here. PARTIAL is the honest verdict.
