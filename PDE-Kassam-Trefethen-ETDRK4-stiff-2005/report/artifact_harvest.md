# Artifact Harvest — ETDRK4 replication

The paper is analytical + provides MATLAB in the text; **no external dataset**
is required. All numerical inputs are procedurally generated inside this
directory. Nothing downloaded.

| Artifact | Source | Notes |
|---|---|---|
| Paper (K&T 2005) | https://epubs.siam.org/doi/10.1137/S1064827502410633 | Read for equations only; we did not vendor a PDF. DOI: 10.1137/S1064827502410633 |
| kursiv.m style KS driver | Trefethen, *Spectral Methods in MATLAB* / K&T 2005 §4 | Reimplemented from equations (see `work/pdes.py:ks_setup`). |
| ETDRK4 update formula | K&T 2005 §2, Cox & Matthews (2002) | Reimplemented in `work/etdrk4_core.py:etdrk4_step`. |
| ϕ-function reference values | Computed on the fly via `mpmath` dps=50 | Independent of the paper; used to score direct vs contour evaluation. |

## Tool versions

| Tool | Version |
|---|---|
| Python | 3.13 (host default) |
| NumPy | 2.4.3 |
| SciPy | 1.18.0 |
| mpmath | 1.3.0 |
| Matplotlib | 3.10.8 |

## Deterministic seeds
None required — all initial conditions are analytic (deterministic).
