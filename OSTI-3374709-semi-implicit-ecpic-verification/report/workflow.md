# Workflow — OSTI 3374709 (semi-implicit ES-PIC verification)

End-to-end pipeline used for the independent replication. All steps run
on free endpoints (CherryRd local Python, uicgpu proxy for OA fetch,
Argo `argo:gpt-5.2` at `localhost:44497` for the LLM judge).

## Stage 0 — paper acquisition

- Fetched OA PDF from OSTI 3374709 / LBNL eScholarship item 8xt682g7
  (Phys. Plasmas 33, 053902 (2026), DOI 10.1063/5.0315721, CC-BY 4.0)
  via `ssh uicgpu` (osti.gov proxy path).
- Converted to text with `pdftotext` on uicgpu; copied back locally.
- Located under `~/Dropbox/REPLICATE-PROJECT/OSTI-3374709-semi-implicit-ecpic-verification/extraction/`.

## Stage 1 — claims decomposition

- Read the paper's §III VERIFICATION section end-to-end.
- Extracted 6 claims (C1–C6) into the report's claims table:
  - C1 (central): effective dielectric + plasma-mode down-shift
    (Eqs. 12/16)
  - C2: modified Bohm–Gross (Eq. 18)
  - C3: unconditional stability for `C_SI ≥ 1` (`ωΔt < 2/√C_SI`, Eq. 14)
  - C4: hybrid modes unaffected except via `ωpe,SI` (Eqs. 19–20)
  - C5: total energy conservation < 2.5% (Fig. 2)
  - C6: Landau damping rates preserved (§III.C)
- Scoped the replication to **C1** (with C3 as byproduct); explicitly
  deferred C4/C5/C6 and reduced C2 to its cold limit.

## Stage 2 — from-scratch code

- Wrote `work/sipic_dispersion.py` (~180 lines NumPy) — a 1D
  electrostatic PIC:
  - normalized units: `ωpe = 1, eps0 = 1, q = -1, m = 1`
  - periodic box, 32 cells, `N = 80,000` particles
  - leapfrog particle push
  - Cloud-In-Cell (linear) charge deposition and field gather
  - spectral (FFT) Poisson solve
- Added the SIPIC operator from Eqs. 9–10 directly: multiply the
  negative-Laplacian by `F = 1 + C_SI · ωpe² · Δt² / 4`
  (i.e. `eps_eff = eps0 · F`); down-shift `1/√F` matches Eq. 16.
- Chose to implement the physical operator from Eqs. 9–10 rather than
  the paper's κ-notation (Eq. 12/13), which is internally inverted;
  documented the choice as a caveat.

## Stage 3 — sweep and measurement

- Test problem: cold Langmuir oscillation, `vth = 0`, mode-1 position
  perturbation amplitude 0.02.
- Sweep: `a ∈ {0.5, 1, 2, 4, 8}` giving `ωpe·Δt ∈ {1, 2, 4, 8, 16}`
  at `C_SI = 4` (Table I).
- Validation control: classical PIC (`C_SI = 0`) at
  `ωpe·Δt ∈ {0.10, 0.20, 0.50}` to confirm the diagnostic recovers
  `ω ≈ ωpe`.
- Diagnostic: signed real part of the complex mode-1 Fourier
  coefficient of E each step; extract ω by FFT of the time series
  (Hann window, parabolic sub-bin interpolation, physical search band).
- Command:
  ```
  python3 work/sipic_dispersion.py report/evidence/sipic_dispersion_results.json
  ```

## Stage 4 — plotting

- `work/plot.py` renders measured vs Eq. 16 vs classical baseline
  across the `ωpe·Δt` sweep.
- Output: `report/evidence/sipic_downshift.png`.

## Stage 5 — LLM judge

- Free Argo `argo:gpt-5.2` (`localhost:44497`), temperature 0.
- Prompt: measured-vs-analytic table + a targeted question about
  whether the SIPIC down-shift is reproduced. No regex/pattern
  scoring.
- Command:
  ```
  python3 work/judge.py | tee report/evidence/llm_judge_verdict.txt
  ```
- Verdict: **REPLICATED** (verbatim quoted in REPORT.md §5).

## Stage 6 — report

- `report/REPORT.md` (Markdown, human-readable, 9 KB).
- `report/REPORT.tex` (LaTeX with a dedicated GENUINE CRITIQUE
  section calling out scope limits: only 1 of 6 claims, cold 1D limit,
  under-characterized 10% error at ωpe·Δt = 16, κ-notation judgement
  call, no cross-code check, single-judge single-prompt).
- Evidence artefacts under `report/evidence/`:
  - `sipic_dispersion_results.json` (raw numbers)
  - `sipic_downshift.png` (measured vs Eq. 16 plot)
  - `llm_judge_verdict.txt` (full LLM judge output)

## Stage 7 — backfill (this task)

- Wrote sibling artefacts required by the OSTI-100 harness:
  `REPORT.tex`, `open_questions.json`, `workflow.md`,
  `artifacts_summary.md`, `failure_analysis.md`.
- Sourced strictly from `REPORT.md`; no re-runs, no new analysis.

## Guardrails observed

- Free endpoints only (Argo `argo:gpt-5.2`, uicgpu OA proxy,
  local Python).
- From-scratch code — no paper code touched, no WarpX/Aleph builds.
- Single-writer discipline for evidence files.
- No fabricated numbers; every quantitative claim in downstream
  artefacts traces back to REPORT.md.
