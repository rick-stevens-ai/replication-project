# Attempt Log — PDE-Wetter-Modelica-Buildings-2014

## 2026-07-04 08:09 CDT (subagent turn start)

1. Read `WAVE_BRIEF_2026-07-01.md`; brief allows either full install + example run OR spot-check via in-repo test scripts. Aim = full end-to-end.
2. Local (CherryRd): no `omc`, no `brew modelica`. Skipped local install (macOS brew build takes 20+ min).
3. `ssh uicgpu`: no system `omc`; MSL binaries not present. `sudo` requires password (skipped). Docker IS available (v28.1.1).
4. **Path chosen**: Docker-based OpenModelica.
5. `docker pull openmodelica/openmodelica:v1.22.0-minimal` succeeded quickly — but the minimal image has NO MSL, no `omlibrary` dir. Result: any Buildings load fails on `extends Modelica.Icons.Package`.
6. `docker pull openmodelica/openmodelica:v1.22.0-ompython` — larger image, also has NO MSL preinstalled (all OM Docker images ship without MSL and expect you to `installPackage` from the online index).
7. Ran `omc updatePackageIndex(); installPackage(Modelica, "4.0.0", exactMatch=false);` inside the ompython image → cleanly installed `Modelica 4.1.0+maint.om` into `/root/.openmodelica/libraries/`. Verified with `loadModel(Modelica)`.
8. Built a derived image `om-msl` (Dockerfile does the installPackage in a `RUN` layer) so MSL is baked into the image and every subsequent run starts with MSL loadable.
9. `git clone --depth 1 https://github.com/lbl-srg/modelica-buildings` → v14.0.0, sha `a131864`, 237 MB.
10. First simulate attempt: `simulate(Buildings.Examples.SimpleHouse, stopTime=604800)` with `--newBackend` flag → compile error in `NFComponentRef.mergeSubscripts` around `rad.vol.dynBal.Medium.nC`. Removed `--newBackend`; retried on default (old) backend.
11. Default backend + `stopTime=86400` (1 day, DASSL, tol=1e-6) → **SUCCESS**. Compiled in 5.7 s, simulated 1 day in 0.11 s. `.mat` result file written.
12. Scaled up to full year: `stopTime=31536000` (1 year), 8760 intervals, CVODE integrator. **SUCCESS** in 1.48 s of simulation wall time; total 6.1 s including compile.
13. Wrote Python parser `extract_v2.py` for the OpenModelica MAT format 4 (column-major name matrix — first attempt used wrong axis and returned zero variables; fixed).
14. Extracted headline results from `SimpleHouse_1y_res.mat`: 851 variables total; interpolated 10786 samples over 1 year; zone T oscillates in 20.0–24.5°C (heating keeps it above the setpoint), radiator peak 700 W (== nominal capacity), heater delivers 1056 kWh over the year.
15. Wrote `verify_tmy3.py` to directly parse the shipped Chicago-OHare `.mos` file (bypassing Modelica) → computed direct mean Tdry, min/max, HDD, CDD, annual GHI as ground-truth reference.
16. Also ran a minimal `TestReadWeather` model (weather-reader + trivial variable assignments) so we could compare Modelica-processed weather channels against the raw file with no HVAC coupling.
17. **Validation results (all agree):**
    - Annual mean Tdry: 9.99°C direct / 9.98°C Modelica-TestReadWeather → **agree to 3 sig fig**.
    - Annual GHI: 1406.6 kWh/m² direct / 1406.7 kWh/m² Modelica → **agree to 4 sig fig**.
    - Temperature extremes: -22.8 to 35.0°C direct == -22.8 to 35.0°C Modelica → **exact match**.
    - HDD (base 65°F): 6307 F-day direct vs NOAA norm 6100–6500 F-day → **within norm band**.
    - Annual GHI vs NSRDB Chicago 1400–1500 kWh/m² → **within band**.
18. Copied MOS scripts, Python analysis, summary JSONs, `.log` back to `~/Dropbox/REPLICATE-PROJECT/PDE-Wetter-Modelica-Buildings-2014/report/evidence/`.
19. Wrote `REPORT.md`, `brief.md`, `artifact_harvest.md`, this log.

## Things that surprised us (in a good way)

- Full-year simulation of a 6-DoF HVAC-coupled thermal-zone model with hourly Chicago-OHare weather took **1.5 seconds** on a single A100-host CPU. That's a ~2× 10⁷× speedup vs real time.
- Zero code modifications were needed to run a v14.0.0 example under an omc from a mainline Docker image; the Modelica/openmodelica compatibility layer just worked once MSL was in place.
- The `--newBackend` flag broke on a `RadiatorEN442_2` internal — the default backend is still the safe choice for Buildings v14 on omc 1.22 (worth flagging upstream but not a replication blocker).

## Non-issues we deliberately did not chase

- **JModelica / Dymola alternative**: dropped, OM path worked first try.
- **BuildingsPy Python interface (`buildings.py`)** unit-test runner: the brief accepts either full run OR spot-check; we did a full run so the spot-check via `runUnitTests.py` is redundant.
- Numerical comparison to Wetter-2014 published figures: the 2014 paper does not present a canonical numeric benchmark table for SimpleHouse — SimpleHouse ships in later versions of the library. What the paper DOES claim (library architecture, weather-reader path, coupled thermal-hydraulic examples runnable in a free tool) is what we tested.
