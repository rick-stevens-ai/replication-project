# artifact_harvest.md

## Public data used

- **Ghia, Ghia & Shin (1982) benchmark tables** — Tables I & II from
  U. Ghia, K. N. Ghia, C. T. Shin, *High-Re Solutions for Incompressible Flow
  Using the Navier–Stokes Equations and a Multigrid Method*, J. Comput.
  Phys. **48**, 387–411 (1982). Publisher URL:
  https://doi.org/10.1016/0021-9991(82)90058-4 (paywalled abstract; table
  values are widely mirrored in follow-on cavity papers and textbooks).
  We hand-transcribed the Re = 100 / 400 / 1000 columns of Tables I (u along
  x=0.5) and II (v along y=0.5) into `work/ghia_data.py`. Those values are
  the exact numerical strings used in the paper and are cross-checked
  against Botella & Peyret (1998), Erturk (2005), and the OpenFOAM cavity
  tutorial reference figures. No download required — these are 17 float
  values per (Re, direction).

- **Zang, Street & Koseff (1994) paper** — J. Comput. Phys. 114(1) 18–33.
  DOI 10.1006/JCPH.1994.1146. Paywalled at the publisher but freely
  available as an author manuscript from Stanford's Environmental Fluid
  Mechanics Lab. Read for method description only; no numerical output
  from the paper was reused (we compare against Ghia, which is what ZSK
  themselves compare against in the paper's cavity section).

## Compute

- Host: `uicgpu` (8×A100, 255 cores, 2 TB RAM). Only CPU numpy was used;
  the runs are small enough (single-thread, ~1 min each) that GPU/multi-core
  was not needed.
- Environment: Python 3, `numpy 1.23.5`, `scipy 1.10.1`, `matplotlib 3.7.5`.
  No new packages installed; used the base `python3` on uicgpu.
- Wall time: ~5 min total for the three-Re sweep + local plotting/judge.

## LLM endpoints (all free per wave-brief hard rule)

- **Argo proxy** at `http://127.0.0.1:44497/v1/chat/completions` (auth
  header `Bearer stevens`). Requested model `argo:claude-opus-4.7` (bug —
  502 on nontrivial responses); fallback `argo:claude-opus-4.5` (used).

## Outputs (this replication)

- `work/zsk_solver.py` — ~300 lines, single-file solver.
- `work/ghia_data.py` — ~50 lines, reference data.
- `work/run_sweep.py` — sweep driver.
- `work/judge.py` — LLM-judge Argo call.
- `work/make_plots.py` — plotting.
- `work/cavity_N128_Re{100,400,1000}.npz` — full flow fields + centreline
  samples for each Re. Each file 402530 bytes.
- `work/sweep_metrics.json` — summary metrics (per-Re errors, wall time,
  divergence norms).
- `work/judge_verdict.json` — LLM-judge raw+parsed response.
- `report/evidence/*.png` — 3 figures (centerlines, streamlines, divergence).
- `report/REPORT.md`, `report/brief.md`, `report/attempt_log.md`,
  `report/artifact_harvest.md` — this documentation set.

## Checksums (sha256, quick sanity)

Run `shasum -a 256 work/*.py work/*.npz work/*.json` from the target dir
to regenerate. Not embedded here to keep this doc stable across re-runs.
