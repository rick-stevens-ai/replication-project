# Brief — PDE-Wetter-Modelica-Buildings-2014

**What:** Independent replication of Wetter et al. (2014), "Modelica Buildings library"
(J. Building Performance Simulation, DOI 10.1080/19401493.2013.765506, cited 769). Paper
introduces the LBNL Modelica Buildings library — an open-source Modelica library for
whole-building HVAC + envelope simulation with a curated set of validated components
(mixing volumes, radiators, weather-data readers, chillers, boilers, controls) exercised
by a shipped set of examples.

**Why:** The paper is a landmark open-source-tool paper. Code + library ship in a public
GitHub repo (`lbl-srg/modelica-buildings`, MIT/BSD 3-clause). The claim that the library
runs on OpenModelica with its bundled Chicago-OHare TMY3 weather data and produces
physically-sensible annual HVAC-and-envelope trajectories is directly testable.

**How:** Cloned Buildings v14.0.0 on uicgpu; built an `om-msl` Docker image on top of
`openmodelica/openmodelica:v1.22.0-ompython` with MSL 4.1.0 preinstalled; simulated the
canonical shipped example `Buildings.Examples.SimpleHouse` for a full year (31 536 000 s,
hourly output) driven by the bundled Chicago-OHare TMY3 `.mos` file; also ran a minimal
`TestReadWeather` model to isolate the weather-reader path. Cross-validated Modelica
outputs against direct Python parse of the same TMY3 file.

**Result:** REPLICATED. Full end-to-end simulation succeeds; extracted annual GHI, mean
`TDryBul`, and temperature extremes agree with a direct-file parse to 3–4 significant
figures. Zone-air temperature and radiator heat flow are physically plausible for a lightly-
heated 100 m² zone in Chicago.
