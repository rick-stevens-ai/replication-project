# Artifacts Summary — PDE-Wetter-Modelica-Buildings-2014

Inventory of the tangible artifacts produced (or verified as present) by
this replication of Wetter et al. (2014), "Modelica Buildings library."

Host: `uicgpu` — working directory `/gpustor/stevens/replicate/modelica-buildings/`.
Deliverable directory: `~/Dropbox/REPLICATE-PROJECT/PDE-Wetter-Modelica-Buildings-2014/`.

## 1. Upstream code artifact

| Item | Location | Notes |
|---|---|---|
| Buildings library source | `~/.../modelica-buildings/` (git clone, depth 1) | HEAD sha `a131864`, v14.0.0, 2026-05-04, from `https://github.com/lbl-srg/modelica-buildings` |
| License | in-tree | BSD-3-clause style (per repo) |
| Weather-data pack | `Buildings/Resources/weatherdata/` | Includes `USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.mos` (30-col × 8760-row TMY3) |
| Examples package | `Buildings/Examples/` | 10 top-level entries: SimpleHouse, ChillerPlant, HydronicHeating, VAVReheat, VAVCO2, DualFanDualDuct, FanCoils, Tutorial/, ScalableBenchmarks, … |
| Conversion scripts | `Buildings/Resources/Scripts/Conversion/ConvertBuildings_from_*.mos` | Back-compat migration from earlier Buildings versions (v8+). Verified as present; not exercised. |

## 2. Environment artifacts

| Item | Detail |
|---|---|
| Base image | `openmodelica/openmodelica:v1.22.0-ompython` (Docker Hub) |
| Derived image | `om-msl` (MSL 4.0.0 → 4.1.0+maint.om preinstalled) |
| Dockerfile | Two-line derivation shown in `workflow.md` §Stage 1 |
| Modelica Standard Library version | `Modelica 4.1.0+maint.om` |

## 3. Scripts and generated inputs (evidence/)

Referenced throughout REPORT.md, expected to live under `evidence/` in
the deliverable directory:

| File | Purpose |
|---|---|
| `sim_yr.mos` | Full-year Modelica script for `Buildings.Examples.SimpleHouse` (CVODE, tol 1e-6, 8760 output intervals over 31,536,000 s) |
| `sim_multi.mos` | Isolation model `TestReadWeather` — ReaderTMY3 only, uniform hourly output (used for the like-for-like TMY3 vs. Modelica comparison) |
| `extract_v2.py` | Custom Python parser for OpenModelica MAT (v4) result files (handles column-major, null-padded `name` matrix) |
| `verify_tmy3.py` | Pure-NumPy independent parser of the shipped TMY3 `.mos` file — computes annual mean, extremes, GHI, HDD, CDD as ground-truth values |

## 4. Simulation output artifacts

| Artifact | Value / size | Notes |
|---|---|---|
| `SimpleHouse_1y_res.mat` | 851 variables × 10,786 time samples | OpenModelica MAT (v4); trajectories for zone, weather bus, radiator, heating water, etc. |
| Wall time (simulate) | **1.48 s** | 1 year hourly HVAC + envelope, single-threaded |
| Compile time | 1.81 s | Fresh model, full code-gen |
| Total (`omc` start → `.mat` on disk) | 6.07 s | End-to-end |

## 5. Derived quantitative results

### 5.1 Zone + HVAC (SimpleHouse, 1 year, Chicago-OHare TMY3)

| Quantity | Value |
|---|---|
| `zon.T` mean | 22.22 °C |
| `zon.T` min  | 20.00 °C |
| `zon.T` max  | 24.50 °C |
| `rad.Q_flow` peak | 700 W  (== `QHea_flow_nominal`) |
| `rad.Q_flow` mean | -164 W |
| Annual heating (∫ heaWat.Q_flow dt) | 1056 kWh (~10.6 kWh/m²/yr for 100 m² zone) |

### 5.2 Weather-reader validation

| Quantity | Direct TMY3 | ReaderTMY3 (isolation) | ReaderTMY3 (SimpleHouse) | Agreement |
|---|---|---|---|---|
| Annual mean Tdry | 9.987 °C | 9.980 °C | 7.798 °C * | 3 sig-fig (isolation) |
| Annual min Tdry  | -22.80 °C | -22.80 °C | -22.80 °C | exact |
| Annual max Tdry  | 35.00 °C | 35.00 °C | 35.00 °C | exact |
| Annual GHI       | 1406.6 kWh/m² | 1406.7 kWh/m² | 1406.5 kWh/m² | 4 sig-fig |

\* SimpleHouse figure is a post-hoc-averaging artefact of the adaptive-step
   trajectory; the isolation model with uniform hourly output is the
   correct like-for-like comparison. Documented in REPORT.md §4.3.

### 5.3 External climate cross-check

| Quantity | This work | External reference | Verdict |
|---|---|---|---|
| Chicago-OHare HDD (base 65 °F) | 6307 °F-day | NOAA norm 1991–2020: 6100–6500 | inside band |
| Chicago-OHare annual GHI       | 1406.6 kWh/m²/yr | NSRDB / EIA: 1400–1500 | inside band |
| 99.6% heating design DB        | -20 °C | ASHRAE 2009 (embedded in TMY3 header) | matches header |
| 0.4% cooling design DB         | 33.3 °C | ASHRAE 2009 (embedded in TMY3 header) | matches header |

## 6. Report artifacts (deliverable)

| File | Purpose |
|---|---|
| `REPORT.md` | Canonical narrative (13 KB): summary, claims table, method, results, verdict, reproducibility, attribution |
| `REPORT.tex` | LaTeX version + dedicated Genuine Critique section |
| `workflow.md` | Stage-by-stage recipe (this pipeline) |
| `artifacts_summary.md` | This inventory |
| `failure_analysis.md` | Gotchas and near-misses encountered during the run |
| `open_questions.json` | Five open research questions grounded in the paper's scope |

## 7. Claim-coverage snapshot

- Fully tested (7): C1, C2, C3, C4, C5, C6, C7.
- Partially tested (2): C8 (conversion scripts present, not exercised);
  C9 (both DASSL and CVODE ran, no point-by-point comparison).
- Untested (0).

## 8. Reproducibility

Any Linux + Docker host reproduces the whole run in ~5 minutes; recipe
in REPORT.md §6. The only non-obvious external dependency is the
`openmodelica/openmodelica:v1.22.0-ompython` image tag remaining
pullable from Docker Hub.
