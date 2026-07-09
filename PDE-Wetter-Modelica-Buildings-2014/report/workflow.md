# Workflow — PDE-Wetter-Modelica-Buildings-2014

End-to-end pipeline for the independent replication of Wetter et al. (2014),
"Modelica Buildings library," JBPS 7(4):253–270 (DOI 10.1080/19401493.2013.765506).

Host: `uicgpu` (Ubuntu, 8×A100 host, Docker 28.1.1).
Working directory: `/gpustor/stevens/replicate/modelica-buildings/`.
Verdict: **REPLICATED**.

## Stage 0 — Paper and claim ingestion

1. Read the paper; extract the contribution class (open-source scientific
   tool paper) and enumerate testable claims.
2. Materialise a **Claims Table** (9 rows, C1–C9) covering:
   code availability, dependency structure, example suite, free-tool
   executability, TMY3 reader existence + fidelity, plausibility of coupled
   HVAC/envelope trajectories, versioned development, and solver-independence.

## Stage 1 — Environment

1. Clone the library from GitHub:
   ```bash
   git clone --depth 1 https://github.com/lbl-srg/modelica-buildings.git
   # HEAD sha: a131864 (2026-05-04, v14.0.0)
   ```
2. Pull the free-tool engine image:
   ```bash
   docker pull openmodelica/openmodelica:v1.22.0-ompython
   ```
3. Build a derived image with the Modelica Standard Library preinstalled
   (image tag `om-msl`):
   ```Dockerfile
   FROM openmodelica/openmodelica:v1.22.0-ompython
   RUN echo 'updatePackageIndex();' > /tmp/i.mos && \
       echo 'installPackage(Modelica, "4.0.0", exactMatch=false); getErrorString();' >> /tmp/i.mos && \
       omc /tmp/i.mos
   ```
   MSL "4.0.0" resolves to `Modelica 4.1.0+maint.om`.

## Stage 2 — Loadability + example enumeration (C1–C3)

1. Inside `om-msl`, load `Buildings/package.mo`; confirm no errors and that
   `uses(Modelica(version="4.1.0"))` is satisfied.
2. Enumerate `Buildings.Examples.*` (10 top-level entries: SimpleHouse,
   ChillerPlant, HydronicHeating, VAVReheat, VAVCO2, DualFanDualDuct,
   FanCoils, Tutorial/, ScalableBenchmarks, …). Verify presence.
3. Sanity-check the license file and repo metadata for C1.

## Stage 3 — End-to-end simulation (C4, C7)

1. Write `sim_yr.mos`:
   ```modelica
   loadModel(Modelica);
   loadFile("/work/Buildings/package.mo");
   simulate(Buildings.Examples.SimpleHouse,
            startTime=0, stopTime=31536000, numberOfIntervals=8760,
            tolerance=1e-6, method="cvode",
            outputFormat="mat", fileNamePrefix="SimpleHouse_1y");
   ```
2. Execute:
   ```bash
   docker run --rm \
     -v .../modelica-buildings/Buildings:/work/Buildings \
     -v .../out:/out \
     -v .../sim_yr.mos:/mnt/sim.mos \
     -w /out om-msl omc /mnt/sim.mos
   ```
3. Record wall-clock (1.48 s simulate, 1.81 s compile, 6.07 s total),
   variable count (851), and sample count (10,786).
4. Also do a 1-day DASSL probe as a cheap solver-diversity check (C9).

## Stage 4 — Result extraction

1. `extract_v2.py` parses the OpenModelica MAT (v4) file directly.
   *Gotcha:* OM's `name` matrix is column-major, each column a variable
   name null-padded to 44 chars.
2. Extract trajectories for: `zon.T`, `weaBus.TDryBul`,
   `heaWat.Q_flow`, `rad.Q_flow`, `weaBus.HGloHor`.
3. Compute derived quantities: annual means, extremes, integrated
   heating (kWh), HDD/CDD.

## Stage 5 — TMY3 ground-truth cross-check (C5, C6)

1. `verify_tmy3.py` parses
   `Buildings/Resources/weatherdata/USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.mos`
   with pure NumPy (no Modelica in the loop).
2. Compute reference annual mean Tdry, extremes, integrated GHI,
   HDD (base 18.3 °C / 65 °F), CDD.
3. Compare against the Modelica reader output from an
   **isolation model** `TestReadWeather` (Stage 6) rather than the
   SimpleHouse trajectory, so time-basis is uniform hourly.

## Stage 6 — Isolation model

1. `sim_multi.mos` builds a minimal `TestReadWeather` model that only
   contains a `Buildings.BoundaryConditions.WeatherData.ReaderTMY3` and
   exposes Tdry and HGloHor.
2. Simulate for one year with uniform hourly output.
3. This gives the correct like-for-like comparison against the direct
   TMY3 parse. The SimpleHouse trajectory numbers (post-hoc python
   time-averaged over adaptive-step samples) are **not** the right
   comparison basis — see the artefact note in REPORT.md §4.3.

## Stage 7 — External climate sanity checks

1. Compare Chicago-OHare HDD (6307 °F-day) against NOAA 1991–2020
   normals (6100–6500 °F-day) → inside band.
2. Compare annual GHI (1406.6 kWh/m²/yr) against NSRDB / EIA solar
   atlas (1400–1500 kWh/m²/yr) → inside band.
3. Cross-check embedded ASHRAE design values (99.6% heating -20 °C;
   0.4% cooling 33.3 °C) against ASHRAE 2009 Handbook entries.

## Stage 8 — Verdict + reporting

1. Apply the WAVE brief's rubric class-by-class.
2. Draft `REPORT.md` (canonical narrative) then `REPORT.tex` (with a
   dedicated **Genuine Critique** section listing what the run does and
   does not prove).
3. Emit standard `WAVE_RESULT` marker line at the bottom of the report.
4. Materialise this workflow doc plus `artifacts_summary.md`,
   `failure_analysis.md`, and `open_questions.json` for downstream
   consumption.

## Provenance

- All numerical outputs come from actual container runs on `uicgpu` on
  2026-07-04. Nothing was fabricated or hand-tuned.
- The Docker image tag `openmodelica/openmodelica:v1.22.0-ompython` and
  the derived `om-msl` image are the only external non-obvious
  dependencies; both are documented in Stage 1 for future
  reproducibility.
