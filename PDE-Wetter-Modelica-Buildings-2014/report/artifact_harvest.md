# Artifact Harvest — PDE-Wetter-Modelica-Buildings-2014

| Artifact | Source | Version / Rev | Size | Notes |
|---|---|---|---|---|
| Modelica Buildings library | `git clone --depth 1 https://github.com/lbl-srg/modelica-buildings.git` | `a131864` (2026-05-04, v14.0.0) | 237 MB (Buildings/) | Full checkout on uicgpu at `/gpustor/stevens/replicate/modelica-buildings/modelica-buildings/` |
| OpenModelica engine | Docker Hub `openmodelica/openmodelica:v1.22.0-ompython` | omc 1.22.0 | ~1 GB image | Pulled 2026-07-04; contains omc + Python bindings but no MSL preinstalled |
| Modelica Standard Library | `installPackage(Modelica, "4.0.0", exactMatch=false)` inside container | `Modelica 4.1.0+maint.om` | ~150 MB | Baked into a derived Docker image tagged `om-msl` |
| Chicago-OHare TMY3 | Ships in-repo at `Buildings/Resources/weatherdata/USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.mos` | 30-column TMY3, WMO 725300, period 1973–2005 | ~1.3 MB | 8760 rows, hourly; header names all 30 channels |
| Example model | `Buildings/Examples/SimpleHouse.mo` | v14.0.0 | ~10 KB | Canonical HVAC + radiator + envelope example in the library |
| Simulation results (1-year SimpleHouse) | Local — `out/SimpleHouse_1y_res.mat` | 851 vars, 10786 time samples | 424 KB | Extracted key trajectories saved to `SimpleHouse_1y_res.mat.summary.json` (see `report/evidence/`) |
| Simulation results (1-year TestReadWeather) | Local — `out/TestReadWeather_1y_res.mat` | 8764 samples | small | Isolates weather-reader path |
| NOAA HDD/CDD reference | ncei.noaa.gov / weather.gov climate normals for Chicago-OHare | 1991–2020 normal, 6100–6500 F-day HDD base 65°F | — | Used as external sanity check on TMY3 HDD |
| Chicago annual GHI reference | NSRDB / atlas.eia.gov | 1400–1500 kWh/m²/yr | — | Used as external sanity check on TMY3 GHI |

## Provenance of local artifacts

- `sim_simplehouse.mos` — .mos script that loads Buildings and simulates SimpleHouse (1 day probe run).
- `sim_yr.mos` — 1-year annual variant with hourly output (used for headline claims).
- `sim_multi.mos` — Minimal `TestReadWeather` model for isolated weather-reader validation.
- `extract_v2.py` — Python parser for OpenModelica MAT (v4) result files; column-major name matrix decode; computes integrals + HDD/CDD.
- `verify_tmy3.py` — Directly parses the raw TMY3 `.mos` file (bypassing Modelica), computes mean Tdry, min/max, HDD, CDD, annual GHI for cross-validation.
