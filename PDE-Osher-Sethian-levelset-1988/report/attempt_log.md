# Attempt Log — Osher & Sethian (1988) replication

2026-07-04 23:45 CDT — start.

1. Read `WAVE_BRIEF_2026-07-01.md`. Confirmed rules: real replication,
   free endpoints only (Argo :44497 key=stevens) for LLM judging,
   never regex for scoring, write only in target dir.

2. Created target dir tree:
   `~/Dropbox/REPLICATE-PROJECT/PDE-Osher-Sethian-levelset-1988/{report/evidence,work}`.

3. Downloaded the paper. Tried three known mirrors; Sethian's UC-Berkeley
   home page hosts the PDF at
   `https://math.berkeley.edu/~sethian/2006/Papers/sethian.osher.88.pdf`
   (38 pages, 82 425 bytes, sha256
   `508150b54de162a0cc1bb345c132e2209b706442317fced30055238f8c2c897a`).
   Two other candidate URLs returned HTML.

4. Read the paper. The bundled `pdf` tool refused the Dropbox path and
   then failed on the workspace copy (credit / model unavailable), so I
   used `pdftotext -layout` locally, giving a 1975-line clean text.
   Read Sections II (formulation, Eqn. 2.11), III.B (upwind HJ scheme
   Eqn. 3.11), III.C (curvature term treatment, Eqn. 3.14), III.D
   (initialization via signed distance), IV.A–F and V.A–D (experiments,
   the exact CFL "1 ≥ 2Δt/Δx · |H₁| + …" restriction, and the reported
   convergence table).

5. Selected three testable core claims (see REPORT.md).
   Implemented `work/levelset.py` in pure NumPy + SciPy + skimage
   (installed into a local venv per PEP-668, since system Python is
   externally managed).  Files:
     - `upwind_grad_norm` — Godunov/Rouy–Tourin form of Eq. 3.11
     - `central_curvature` — Eq. 3.14 central-difference κ
     - `step_constant_speed`, `step_mean_curvature` — forward-Euler
     - Experiments C1, C2, C2b, C3 with CSV + PNG outputs

6. Ran all four experiments end-to-end on local CPU
   (grids up to 301×301, ~12 500 steps for the finest C2 case;
    total wall-clock ≈ 2–3 minutes).  Results in
    `report/evidence/results.json`.

7. Convergence check (`work/convergence.py`) confirmed error decreases
   with dx: L∞ went 3.88e-3 → 1.54e-3 → 7.01e-4 as N went 101 → 201 → 301
   for the mean-curvature-flow circle; observed order ≈ 1.34, 1.93.

8. LLM-judge scoring via Argo `argo:gpt-4o` at
   `http://127.0.0.1:44497/v1/chat/completions` (free endpoint,
   Authorization: Bearer stevens).  Judge returned JSON with all four
   sub-claims pass and overall verdict REPLICATED. Full response saved
   to `report/evidence/llm_judge.txt`.

9. Wrote `REPORT.md`, `brief.md`, `artifact_harvest.md`, this log.

No blockers.  Final verdict: **REPLICATED**.
