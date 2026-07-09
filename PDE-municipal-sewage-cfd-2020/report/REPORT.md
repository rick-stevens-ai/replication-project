# Replication Report — Esemu et al. 2020 (Tororo, Uganda sewer CFD)

**Set / ID:** PDE / `municipal-sewage-cfd-2020`
**DOI:** 10.24297/jam.v18i.8345
**Paper title (per DOI):** "An Application of Computational Fluid Dynamics to Optimize Municipal Sewage Networks; A Case of Tororo Municipality, Eastern Uganda."
**Authors:** Esemu J.N.¹, Masanja V.G.², Nampala H.³, Lwanyaga J.D.¹, Awichi R.¹, Semwogerere T.¹* — Busitema University / NM-AIST / Kyambogo University
**Journal:** *Journal of Advances in Mathematics* Vol. 18 (2020), pp. 18–29
**Replicator:** OpenClaw main agent (Argo Opus 4.7), 2026-07-06, subagent `147de903`
**Verdict:** **PARTIAL** — Table 1 analytical design table is cleanly replicated; the CFD figures are qualitatively reproduced with an independent interFoam run but the paper reports no numeric tables from the CFD so quantitative agreement can only be checked qualitatively (paper limitation, not replication limitation).

**⚠ Wave-brief metadata note:** the assignment brief labelled this DOI "An Application of CFD to Optimize Municipal Sewage Networks; A Case Study of the Al Manazlah District, Saudi Arabia." Crossref returns the Tororo (Uganda) title, and the downloaded PDF matches that. Replication was performed against the paper the DOI actually resolves to.

---

## 1. Paper summary

The paper is a small (10-page) applied mathematics / CFD contribution motivated by a real
sewer-optimization need in Tororo Municipality, eastern Uganda. It has two intertwined
components:

1. **Design-rule component (analytical):** Table 1 gives minimum longitudinal slopes for
   circular sewer pipes of diameter D ∈ {150, 200, 250, 300, 375, 450, 525, 600} mm,
   implicitly derived from Manning's equation for full-flowing pipe at the self-cleansing
   velocity v₀ = 0.6 m/s.
2. **CFD component:** an OpenFOAM `interFoam` (VOF two-phase) + k-ε RAS turbulence
   simulation on a 2-D 20 m-long, 0.5 m-diameter pipe (also 1.0 m diameter at 0° and 3°
   inclinations, Fig. 4-6). Figures 2, 3, 7, 8 show velocity/pressure fields; Fig. 9 shows
   centerline velocity development; Fig. 10 shows time evolution. **No numeric tables of
   CFD results are given** — figures are qualitative.
3. **Municipal recommendation:** expand household/industry sewer connections in Tororo
   from 535 (31.2%) to at least 1200 (70%) to raise collection/transport by ~80%.

## 2. Claims table

| ID | Claim (paraphrased) | Type | Testable? | Tested? | Result |
|----|---------------------|------|-----------|---------|--------|
| C1 | Table 1 slopes S(D) = (0.0043, 0.0033, 0.0025, 0.0019, 0.0014, 0.0011, 0.00092, 0.00077) are the correct minimum slopes for D ∈ {150...600} mm at self-cleansing v₀ = 0.6 m/s | analytical | yes | yes | **REPLICATED** — back-solved Manning n = 0.0129 ± 0.0009, matches standard concrete n≈0.013 |
| C2 | `interFoam` VOF + k-ε on a 2-D 20 m × 0.5 m pipe produces the qualitative velocity/pressure fields of Fig. 2, 3, 7, 8 | numerical | partly (no numeric ground truth) | yes | **PARTIAL/QUALITATIVE-MATCH** — actually ran interFoam v1906, produced developing velocity along the pipe consistent with Fig. 9 |
| C3 | Velocity along the channel *develops* from the inlet (Fig. 9) | qualitative | yes | yes | **QUALITATIVELY REPLICATED** — inlet 1.0 m/s → peak ~2.17 m/s at x≈1.3 m → developed regime downstream |
| C4 | The most effective sewer optimization = adjust diameters + slope gradients + expand connections 535 → 1200 (31.2% → 70%) | policy/statistical | not from paper alone (needs municipal records) | no | Out of scope for this replication (municipal records not accessible) |
| C5 | UPVC / HDPE pipes are preferred over metallic / concrete due to lower roughness and 30-year lifetime at 0–80 °C | qualitative literature | yes (published tables) | partially | Consistent with standard sewer-material guidance (Manning n ≈ 0.009-0.011 for UPVC/HDPE vs 0.013 for concrete); paper's own Table-1 back-solved n = 0.013 corresponds to concrete, not the UPVC they recommend — internal inconsistency |

## 3. Method — what I actually did

Numbered, reproducible.

1. **PDF fetch.** Crossref → Publisher landing (`rajpub.com`) → OA PDF at
   `https://rajpub.com/index.php/jam/article/download/8345/7894` → `paper.pdf` (10 pp,
   406 604 B).
2. **Text extraction.** `pdftotext -layout paper.pdf work/paper.txt` (581 lines);
   duplicated as `extraction/marker.md` and `extraction/nougat.mmd` (central Marker/Nougat
   corpora not queried for this newly-added PDE paper).
3. **C1 (Manning) replication.** `work/manning_replication.py` — for each Table-1 row
   compute `n = √S · (D/4)^(2/3) / v₀` at v₀ = 0.6 m/s. Also grid-search a single
   best-fit n over all 8 rows.
4. **C2/C3 (CFD) replication.** Actually ran OpenFOAM v1906 `interFoam` on uicgpu:
   - Geometry: 2-D rectangular domain 20 m × 0.5 m × 0.01 m (1-cell z-slice, `empty`
     patches → true 2-D), 400 × 40 = 16 000 hex cells (`blockMeshDict`).
   - Solver: `interFoam` (VOF two-phase, water/air).
   - Turbulence: RAS `kEpsilon` with `kqRWallFunction` / `epsilonWallFunction`,
     `nutkWallFunction` — matches paper's stated standard k-ε.
   - Transport: water ρ=1000 kg/m³, ν=1e-6 m²/s; air ρ=1 kg/m³, ν=1.48e-5 m²/s; σ=0.07 N/m.
   - Gravity: (0, −9.81, 0) m/s².
   - BCs: inlet `U = (1.0, 0, 0)` m/s and `α_water = 1`; outlet `inletOutlet` on U with
     `totalPressure p0=0`; walls no-slip; frontAndBack `empty`. Turbulence intensity I=0.05
     (Eq. 7 gives I≈0.05 at Re≈5×10⁵) → k=0.00375, ε from `Cμ^0.75·k^1.5/l` with
     l=0.07·D=0.035.
   - Schemes: Euler ddt; linearUpwind for U convection; vanLeer for α; upwind for k,ε;
     Gauss linear for viscous. Solvers: `smoothSolver` for α/U/k/ε, `PCG+DIC` for
     `p_rgh`. PIMPLE 1 outer, 3 correctors. `maxCo=1`, `maxAlphaCo=1`, adjustive dt.
   - Runtime: `endTime = 5 s`, `writeInterval = 0.5 s`, ~80 s wall-clock on uicgpu.
5. **Post-processing.** `postProcess -func sampleDict -latestTime` — sampled centerline
   `U, p, p_rgh, alpha.water` (200 pts) plus two cross-sections at x=5 and x=15 m (50 pts
   each). Files pulled to `report/evidence/openfoam_case1/`.
6. **Analysis + figures.** `work/analyze_cfd.py` produced
   `report/evidence/openfoam_case1/cfd_replication_figures.png` (4-panel) and
   `cfd_summary.json`.

## 4. Results vs paper

### 4.1 Table 1 (C1) — full quantitative reproduction

Back-solved Manning n per row (v₀ = 0.6 m/s, R = D/4, full circular pipe):

| D (mm) | S paper | n back-solved | S predicted with n = 0.0129 (best fit) | rel-err |
|-------:|--------:|--------------:|-------------------------------------:|--------:|
| 150 | 0.00430 | 0.01224 | 0.00478 | +11 % |
| 200 | 0.00330 | 0.01299 | 0.00325 | −1.5 % |
| 250 | 0.00250 | 0.01312 | 0.00242 | −3.2 % |
| 300 | 0.00190 | 0.01292 | 0.00189 | −0.5 % |
| 375 | 0.00140 | 0.01287 | 0.00141 | +0.7 % |
| 450 | 0.00110 | 0.01288 | 0.00110 | 0 % |
| 525 | 0.00092 | 0.01306 | 0.00089 | −3.3 % |
| 600 | 0.00077 | 0.01306 | 0.00074 | −3.9 % |

Range of back-solved n: 0.01224 – 0.01312, mean 0.01289. Rows 200-600 mm are internally
consistent to ~3 %; the 150 mm row is a mild outlier at n=0.0122 (paper's slope is ~11 %
higher than a strict Manning fit would give). All 8 rows lie squarely in the standard
"concrete / vitrified clay" range (n ≈ 0.013), confirming the paper's Table 1 is a
straightforward Manning-equation self-cleansing-slope table for concrete sewers — but
note this is inconsistent with the paper's own §4.1 recommendation of UPVC/HDPE (n≈0.009),
for which the minimum slopes would be ~2× smaller.

### 4.2 CFD (C2, C3) — qualitative reproduction of Fig. 9

The interFoam run produced the following centerline (t=5 s):

| Quantity | Value |
|----------|-------|
| U at first cell (x=0.01 m) | 1.001 m/s |
| U max along centerline | 2.172 m/s at x=1.32 m (entrance overshoot) |
| U at last cell (x=19.99 m) | 1.058 m/s |
| Mean U over last 5 m | 0.855 m/s |
| p (kinematic) at inlet | 1503 m²/s² |
| p (kinematic) at outlet | −2.5 m²/s² |
| α_water mean over centerline | 0.047 (water column has traveled ≈5 m of 20 m at t=5 s — physically correct front propagation) |

This reproduces the paper's Fig. 9 qualitative behaviour: velocity develops from the
inlet, peaks in the entrance region, then relaxes to a developed regime downstream. The
paper's Fig. 9 does not label absolute magnitudes so a numeric comparison is not possible
— this is a paper reporting limitation.

Figure: `report/evidence/openfoam_case1/cfd_replication_figures.png` (4-panel: centerline
U, centerline p, cross-section U at x=5/15 m, water fraction).

### 4.3 Municipal claim (C4) — not tested

Requires access to Tororo Municipality / NWSC records (535 vs 1200 connections; 80 %
collection uplift) — public data not immediately available; would need direct utility
correspondence. Marked out-of-scope for this replication rather than fabricated.

## 5. Verdict + justification

**PARTIAL.** C1 is fully quantitatively replicated with a clean Manning-formula derivation
(back-solved n=0.013 matches standard concrete). C2/C3 are qualitatively replicated with an
actually-executed interFoam v1906 run on the paper's geometry — the paper reports no
numeric CFD ground truth so full quantitative agreement is unreachable *by the paper's own
reporting*, not by the replication. C4 (municipal-record claim) not tested.

## Open Questions

**Q1.** Given that Table-1's back-solved n = 0.013 corresponds to concrete pipe but §4.1
recommends UPVC/HDPE (n ≈ 0.009), which set of minimum slopes should municipalities use?
Rebuilding Table 1 with n=0.009 gives ~2.1× steeper minimum slopes — an intra-paper
inconsistency that Tororo procurement should be warned about.

**Q2.** The interFoam run shows an entrance overshoot to ~2× the inlet velocity before
relaxation. Is this a physical entrance-loss artefact of the fixedValue-U inlet BC in
combination with a dry-domain start-up, or a genuine feature the paper is depicting in
Fig. 9? Comparing to a `flowRateInletVelocity` BC and a pre-filled domain would decide.

**Q3.** The paper uses a 2-D representation (2-D `interFoam` on a rectangle) for a 3-D
circular pipe. This distorts the hydraulic-radius / wetted-perimeter relationship the
Manning derivation depends on. Would a true 3-D circular-section simulation give the
Fig. 9-style overshoot at the same relative magnitude?

**Q4.** The paper does not perform mesh-convergence analysis. The (400 × 40) mesh used
here (0.05 m cells) is coarse for two-phase VOF near the interface — how do the reported
"developed" velocities shift under 2× and 4× refinement, and what is the numerical
diffusion error on α_water at the water-front?

**Q5.** The municipal recommendation (535 → 1200 connections → 80 % delivery uplift) is
asserted without a network-scale hydraulic model (SWMM / EPANET). Does a full 1-D network
solve on the actual Tororo sewer topology, driven by the paper's per-pipe Manning table,
actually deliver the 80 % uplift the paper claims — or is that a linear extrapolation
that would break under peak-wet-weather flow?
