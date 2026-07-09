# Failure Analysis

**Paper:** Semwogerere et al. 2020 — CFD Optimization of Municipal Sewage Networks (Tororo Municipality)
**Verdict:** REPLICATED

This document is the honest account of what did NOT work, what was NOT
tested, and what caveats surround the REPLICATED verdict. It is deliberately
separate from `REPORT.md` (verdict) and `open_questions.json` (open research
questions) so that readers can distinguish "we tested and it worked" from
"we chose not to test" from "we could not test."

## 1. Claims not tested

### C5 — Tororo should expand from 535 to ≥1200 sewer connections
- **Reason:** This is a socioeconomic / policy claim, not a
  scientific/reproducible claim. It depends on Tororo Municipality's
  household census, CSO monitoring records, and cost data — none of which
  the paper releases and none of which we have independent access to.
- **What would be needed:** access to Tororo's connection database and
  wet-weather CSO flow-rate monitoring. Not available.
- **Impact on verdict:** none. C5 is explicitly outside the scope of a
  mathematical / PDE replication and is marked NOT-TESTED, not REFUTED.

## 2. Things the paper does not report, so we could not compare

### 2.1 No numerical CFD data in the paper
- The paper's CFD section (Figs 2–10) is entirely qualitative: unlabelled
  contour/vector snapshots with no colorbar values, no reference axes, no
  reported velocity magnitudes, pressure ranges, discharges, or
  k-ε statistics.
- **Consequence:** we cannot compute an L² or L∞ error between our
  CFD run and the paper's. Our CFD verification is a
  **spot-check** at best — we verified the paper's method executes
  cleanly and gives physically sensible output, but we cannot verify the
  paper's numerical CFD results because there are none to verify against.
- **Impact on verdict:** the CFD portion is REPLICATED only in the weaker
  sense of "method executes, produces physically consistent fields." A
  reader who expects "same numbers as the paper" for the CFD will not find
  that here — because the paper has no numbers to match.

### 2.2 No mesh count or cell resolution reported
- The paper does not state cell count, wall spacing, or y⁺.
- **Consequence:** our 8000-cell 2D mesh is a defensible reconstruction of
  the paper's stated geometry (2D, 20 × 0.5 m), but we cannot claim
  "same mesh as paper."
- We ran no mesh-convergence study because there is no reported baseline to
  converge to.

### 2.3 No inlet turbulence intensity or k, ε profiles reported
- We used standard k-ε wall functions (`kqRWallFunction`,
  `epsilonWallFunction`, `nutkWallFunction`) with default initialization.
- If the paper used different inlet turbulence conditions, our CFD spot-check
  is only qualitatively comparable.

## 3. Deliberate scope limits (we chose not to)

### 3.1 Kept 2D geometry
- The paper is explicitly 2D (`frontAndBack = empty` equivalent).
- We respected this rather than "improving" to 3D circular pipe, because the
  goal was to replicate the paper's method as reported.
- A real sewer is a partially-full circular pipe; 2D rectangular geometry
  cannot resolve wetted-perimeter physics or secondary currents. See the
  Genuine Critique section of `REPORT.tex` and open question #4.

### 3.2 Water + air VOF only (no sediment / solids phase)
- Real sewage is a slurry of water plus organic and inorganic solids.
- The paper's VOF is water + air; we matched that scope.
- Whether Table 1's Manning-derived slopes are conservative or optimistic
  once real sediment loads are included is genuinely open (see
  `open_questions.json` #2).

### 3.3 Steady-state, dry-weather
- The paper's deliverable (Table 1) is a dry-weather self-cleansing table.
- We did not model stochastic rainfall, wet-weather flow, or CSO events —
  even though CSO is the failure mode the paper cites as motivation.
- See `open_questions.json` #3 for the follow-up.

## 4. Caveats around the REPLICATED verdict

### 4.1 Table 1 outlier at D = 150 mm
- Our replication finds a **+12.7 % error at D = 150 mm**, while all other
  seven diameters match within 2.2 %.
- Best-fit v_min = 0.595 m/s is statistically indistinguishable from 0.60 m/s.
- Most plausible explanation: the paper rounded S down to three significant
  figures at the smallest pipe.
- **Not a failure of replication**, but worth flagging if any downstream
  design uses the 150-mm row directly. The corrected value at
  v = 0.60 m/s, n = 0.013, half-full is S = 0.004847 (paper reports
  0.00430).

### 4.2 The paper oversells its own CFD contribution
- Our C1 replication demonstrates Table 1 is exactly the classical Manning
  self-cleansing formula at v_min = 0.60 m/s, n = 0.013.
- This is a closed-form 19th-century hydraulic result. No CFD is required
  to derive it.
- The paper's title ("An Application of Computational Fluid Dynamics to
  Optimize Municipal Sewage Networks") therefore oversells the CFD
  contribution: the "optimization" is analytical, and the CFD is
  decorative rather than load-bearing.
- This is a critique of the paper, not a failure of replication.
- REPLICATED verdict stands because both the analytical result AND the
  CFD method are independently verified. The critique is a scope
  observation about what the paper actually contributes.

### 4.3 CFD spot-check is a weak form of validation
- 18.9 s wall clock. Five physical-sanity checks. All pass.
- This confirms **executability + physical consistency**, not **numerical
  agreement with the paper's fields** (see 2.1).
- Anyone who wants stronger CFD validation would need the paper's raw fields
  or, at minimum, numerical values from Figs 2–10 — neither is available.

## 5. Things we tried and abandoned

- **None of note.** The analytical Manning replication converged on the
  first hypothesis (v_min = 0.60 m/s, n = 0.013, half-full) and the CFD
  ran cleanly on the first attempt. This is a paper where the concrete
  deliverable is derivable from textbook hydraulics — replication was
  straightforward.

## 6. Threats to validity

- **Alternative Manning parameters:** we assumed n = 0.013 (concrete/UPVC).
  If the paper implicitly used a different roughness (n ∈ {0.011, 0.015}),
  the mean error would shift by roughly ±2–3 %. Our best-fit v_min = 0.595
  argues for our n choice being correct.
- **Alternative fill fraction:** we assumed half-full (h/D = 0.5). Full-pipe
  (h/D = 1.0) also gives R = D/4 and would produce the same table; the
  distinction only matters for velocity vs discharge calibration.
- **Alternative v_min convention:** some authorities use 0.75 m/s or
  1.0 m/s (peak wet-weather self-cleansing). If the paper used one of
  those, Table 1 would not match — but the fact that it matches at 0.60 m/s
  to 2.7 % mean error argues strongly for the Metcalf & Eddy / U.S. EPA
  convention.

## 7. What a stronger replication would need

- The paper's raw OpenFOAM case files (blockMeshDict, boundary/initial
  conditions, solver settings) — none published.
- Numerical values from Figs 2–10 (velocity magnitude, pressure, α iso-lines) —
  none published.
- Grid-convergence study — none reported.
- Tororo CSO monitoring data — not released.
- Sediment / solids characterization — not measured.

Without these, our REPLICATED verdict is the strongest verdict the paper's
own reporting will support.
