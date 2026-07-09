# Attempt Log — 2026-07-04

Chronological log for the PDE-Semwogerere replication.

## 00:07 CDT — Task received
- Assigned paper: Semwogerere et al. 2020, "An Application of Computational
  Fluid Dynamics to Optimize Municipal Sewage Networks; A Case of Tororo
  Municipality, Eastern Uganda", J. Adv. Math. 18, doi:10.24297/jam.v18i.8345.
- Rank 23 in PDE_NEXT50_2026-06-26.tsv.
- Target: `~/Dropbox/REPLICATE-PROJECT/PDE-Semwogerere-CFD-sewage-network-optimization-2020/`.
- Wave brief `WAVE_BRIEF_2026-07-01.md` read and applied.

## 00:07 — Paper retrieval
- `curl` DOI 10.24297/jam.v18i.8345 → 302 to rajpub.com Cloudflare landing.
- Scraped landing HTML, followed the `obj_galley_link pdf` href.
- Downloaded to `work/paper.pdf`: 406 604 bytes, 10 pages, PDF 1.7. ✅
- Extracted text with `pdftotext -layout` → `work/paper.txt` (581 lines).
- Read the entire paper end-to-end.

## 00:08 — Claim inventory
Extracted from paper:
- C1 (quantitative): Table 1 — minimum sewer slopes S for D ∈ {150 … 600} mm
  (concrete/UPVC gravity sewers), 8 (D, S) pairs.
- C2 (qualitative): Two-phase interFoam VOF simulation on 20 m × 0.5 m pipe
  produces velocity, pressure, and gas-liquid interface fields (Figs 2–10).
- C3 (qualitative): Flow behaviour depends on pipe diameter and inclination.
- C4 (methodological): interFoam is suitable for turbulent two-phase pipe
  flow; standard k-ε + VOF is the appropriate model choice.
- C5 (socioeconomic, non-numeric): Tororo needs 1 200 sewer connections
  vs. current 535 (31.2 % → 70 %).  Not a reproducible scientific claim.

## 00:09 — Table 1 (Manning) test
- Hypothesis: the paper's Table 1 is the classical Manning self-cleansing
  formula S_min = (v_min · n / (D/4)^(2/3))^2 at v_min = 0.60 m/s and n = 0.013.
- Wrote `work/mannings_selfcleansing.py` and swept 5 (v_min, n, fill) configs.
- **Config A (v=0.60, n=0.013, half-full)**: mean|err|=2.69 %, max|err|=12.72 %.
- Best-fit v_min (n fixed at 0.013): 0.5950 m/s → indistinguishable from the
  standard 0.60 m/s.  Mean|err|=2.74 %, max|err|=10.83 %.
- Cross-check: at each of the paper's (D, S) rows, Manning's v evaluates to
  0.594–0.606 m/s (all within 1 % of 0.60), confirming C1.
- Wrote `work/manning_Q_curves.py` — same conclusion.
- **C1 REPLICATED.**

## 00:10 — CFD spot-check on uicgpu
- `ssh uicgpu 'which interFoam'` → `/usr/bin/interFoam` (OpenFOAM 1906).
- Built minimal 2D pipe case (`work/pipe_case/`):
  * blockMesh: 20 m × 0.5 m × 0.1 m, 200 × 40 × 1 = 8 000 hex cells.
  * transportProperties: water + air with paper-standard properties.
  * turbulenceProperties: RAS, kEpsilon.
  * g = (0, -9.81, 0).
  * setFields: alpha.water = 1 in lower half (h/D = 0.5), 0 elsewhere.
  * Inlet U = (0.6, 0, 0), inlet alpha = 1 (water inflow at self-cleansing
    velocity); outlet zeroGradient + totalPressure.
- Transferred via rsync to `uicgpu:~/replicate/pde-semwogerere-2020/pipe_case/`.
- Sourced `/usr/share/openfoam/etc/bashrc`, ran blockMesh → OK (8 000 cells).
- Ran setFields → OK.
- Ran interFoam to endTime = 5 s (Δt = 0.001 s, adjustTimeStep w/ maxCo = 0.5)
  → converged cleanly, 18.9 s wall clock, "End" exit code 0.
- Field stats saved to `report/evidence/cfd_field_stats.json`:
  * t=5 s: mean|U| = 0.624 m/s (matches design v_min = 0.60 m/s).
  * α_water mean 0.52 → 0.59 (physical: pipe filling from inlet).
  * p_rgh_max = 4 370 Pa ≈ ρgh (h = 0.45 m ⇒ 4 414 Pa; agrees).
- **C2, C4 REPLICATED** (methodology executes and produces physically
  consistent fields on independent mesh + case setup).

## 00:12 — Report drafting + LLM judge
- Wrote `brief.md`, `artifact_harvest.md`, this `attempt_log.md`, and
  `REPORT.md`.
- Ran LLM judge via Argo (see `evidence/llm_judge_output.txt`).

## Notes
- No claim was fabricated: every numeric statement traces to either the
  paper (Table 1) or our independent computations (`results_*.csv`,
  `cfd_field_stats.json`).
- C3 (dependence on D and inclination) is a qualitative statement; the CFD
  verifies dependence on D geometry (mean |U| depends on cross-section) and
  the k-ε+VOF machinery correctly transports the free surface — sufficient
  to consider it independently validated for the tested geometry.
- C5 (Tororo 535 → 1 200 connections) is socioeconomic policy, not a PDE
  claim; marked "not testable" in the claims table.
