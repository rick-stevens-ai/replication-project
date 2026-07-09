# Failure Analysis — PDE-Wetter-Modelica-Buildings-2014

Terminal verdict: **REPLICATED** — the replication succeeded end-to-end
and produced numbers that agree with independent ground truth to 3–4
significant figures on the weather-forcing path. This document exists
so that "success" is not a black box: it enumerates the gotchas, near-misses,
partial claims, and stated non-goals encountered along the way.

## 1. What did NOT fail

For the record, so the rest of this document is not read as failure-heavy:

- The library cloned cleanly (`git clone --depth 1` from GitHub, HEAD `a131864`).
- `Buildings/package.mo` loaded in OpenModelica 1.22.0 without errors
  once MSL 4.1.0 was preinstalled in the derived `om-msl` image.
- `Buildings.Examples.SimpleHouse` compiled (1.81 s) and simulated
  (1.48 s) for a full year without solver failure, non-convergence,
  or crash.
- The 1-day DASSL probe also succeeded.
- The Modelica ReaderTMY3 output agreed with a direct-parse ground
  truth to 3–4 significant figures on annual mean Tdry and integrated
  GHI, and to the last displayed digit on Tdry extremes.

## 2. Actual gotchas encountered

### 2.1 OpenModelica MAT (v4) result-file variable-name matrix

**Symptom.** Naive `scipy.io.loadmat` on `SimpleHouse_1y_res.mat` returns
usable numeric matrices, but the `name` matrix reads back as garbled
bytes if handled row-major.

**Root cause.** OpenModelica writes the `name` matrix column-major:
each *column* is one variable name, null-padded (`\x00`) to 44 bytes.
A row-major interpretation smears characters across variables.

**Fix.** `extract_v2.py` transposes and null-strips per column
before decoding. Documented in REPORT.md §3.3 explicitly so that
future replicators do not spend an afternoon on this.

**Impact.** No numerical impact once fixed; would have been a
silent-corruption failure if not caught.

### 2.2 Post-hoc time-averaging of an adaptive-step trajectory (the 7.80 °C artefact)

**Symptom.** Computing annual mean Tdry over the SimpleHouse trajectory
by naive `np.mean` on the extracted `weaBus.TDryBul` samples returns
7.798 °C, whereas the direct TMY3 parse and the isolation-model reader
both return ~9.98 °C. The two disagree by more than 2 °C.

**Root cause.** SimpleHouse's OM run emitted 10,786 samples (adaptive
step), not 8760 uniform hourly samples. The integrator naturally
concentrates samples in fast-transient regions (typically winter
mornings when the heater switches on) — so a plain arithmetic mean
weights those regions disproportionately and biases the "mean" cold.
The mean is a valid statistic of the sample sequence but is *not* the
correct time-integrated mean.

**Fix.** Two, applied together:
1. For like-for-like comparison against the direct TMY3 parse, use the
   **isolation model** (`TestReadWeather`, uniform hourly output). This
   returns 9.980 °C, matching the direct parse to 3 sig-fig.
2. Explicitly annotate the SimpleHouse column with an asterisk
   ("post-hoc python time-averaging artefact") in both REPORT.md §4.3
   and REPORT.tex §4.3, so any reader of the raw table understands
   why the three numbers disagree.

**Impact.** No wrong number reached the verdict path (the isolation
model was always the reference). But a casual skim of the SimpleHouse
column, without the annotation, would look like a validation failure
when it is actually a sampling artefact.

### 2.3 Modelica Standard Library dependency

**Symptom.** First attempt to load `Buildings/package.mo` in the stock
`openmodelica/openmodelica:v1.22.0-ompython` image failed with a
missing `Modelica` package.

**Root cause.** The stock OpenModelica image does not ship MSL
preinstalled; `Buildings` requires `Modelica 4.1.0`.

**Fix.** Built a derived `om-msl` image with a one-liner
`installPackage(Modelica, "4.0.0", exactMatch=false)` (which resolves
to `Modelica 4.1.0+maint.om`). Documented in workflow.md and REPORT.md.

**Impact.** Zero, once the image was built. Reproducers should build
`om-msl` before running `sim_yr.mos`.

## 3. Stated non-goals (deliberately not tested)

These are documented so the verdict "REPLICATED" is not interpreted as
covering claims we chose to defer.

### 3.1 Numerical robustness of the acausal fluid networks (paper §5.1)

- **What we did:** SimpleHouse ran successfully, which *implicitly*
  exercises the homotopy initialisation and near-zero-flow regularisation.
- **What we did not do:** targeted stress tests (flow reversal, warm-start
  vs. cold-start pairs, pathological Reynolds regimes).
- **Why:** deep partial; not in the paper's headline claim class for
  this contribution type.

### 3.2 Solver point-by-point comparison (C9)

- **What we did:** ran both DASSL (1-day) and CVODE (1-year) successfully.
- **What we did not do:** compared their trajectories element-wise on a
  common time grid.
- **Why:** neither integrator failed; a formal comparison is a follow-up
  study, not a replication-blocker.

### 3.3 Every example in `Buildings.Examples.*` (C3)

- **What we did:** enumerated all 10 top-level entries and simulated
  SimpleHouse end-to-end for a year.
- **What we did not do:** compile or simulate ChillerPlant, HydronicHeating,
  VAVReheat, VAVCO2, DualFanDualDuct, FanCoils, Tutorial/, or
  ScalableBenchmarks.
- **Why:** claim C3 as stated ("ships a suite of validated examples") is
  a presence claim, tested by enumeration; per-example validated
  simulation is a much larger effort belonging to a follow-up study.

### 3.4 Cross-tool numerical agreement

- **What we did:** ran OpenModelica 1.22.0.
- **What we did not do:** ran Dymola or JModelica; did not check whether
  Buildings v14 produces the same numbers in different Modelica
  implementations.
- **Why:** JModelica is deprecated and unmaintained; Dymola is commercial
  and outside the free-tool scope of the replication.

### 3.5 Bit-for-bit reproduction of v1.5 paper numbers

- **What we did:** replicated against v14.0.0 mainline (2026-05-04).
- **What we did not do:** downgrade to a v1.5-era Buildings release and
  reproduce the paper's specific 2014 output.
- **Why:** the paper does not publish reference trajectories or numerical
  checksums for its examples, so a bit-for-bit test is not defined even
  if we did downgrade. The v14 test is arguably a *stronger* claim
  (the library still works on modern MSL 12 years later), not a weaker
  one.

## 4. Latent risks in the successful run

These are things that *look* fine but could bite a future replicator.

- **Docker tag drift.** Our exact numbers depend on the specific
  `openmodelica/openmodelica:v1.22.0-ompython` tag remaining pullable
  and unchanged. If Docker Hub re-tags or removes the image, the
  numbers may not reproduce byte-for-byte.
- **Parser trust.** `extract_v2.py` is single-purpose; we did not
  cross-check against a second parser (`DyMat`, `buildingspy`). A
  subtle bug (e.g., a factor-of-1000 scaling error) would go unnoticed
  because all our internal cross-checks use the same parser.
- **HDD "inside band" is soft.** NOAA 1991–2020 normals are a rolling
  30-year climatology; TMY3 is a typical-year synthetic. Agreement
  within a ~400 °F-day band is what "inside band" means — this is a
  sanity check, not a strict validation.

## 5. Net position

The replication achieved everything it set out to test. The two gotchas
(§2.1 OM MAT format, §2.2 adaptive-step averaging) were caught and
fixed with no propagation to the verdict. The stated non-goals (§3)
are honest gaps, not silent failures. The latent risks (§4) apply to any
extension of this work.

Verdict retained: **REPLICATED.**
