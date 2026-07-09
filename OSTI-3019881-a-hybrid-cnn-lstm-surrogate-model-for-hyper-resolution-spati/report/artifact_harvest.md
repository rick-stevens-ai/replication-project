# Artifact harvest — OSTI 3019881

## Paper
| item | value |
|---|---|
| title | A hybrid CNN-LSTM surrogate model for hyper-resolution spatiotemporal flood forecasting in Norfolk, Virginia |
| authors | Y. Wang, J.L. Goodall, C. Kumar, D. McSpadden, S.A. Barbosa, B. Roy, A. Shahabi, N. Tahvildari |
| affiliations | UVA (Civil & Env Eng / Link Lab), ODU-JLab JIACES, JLab, ORNL, FIU |
| journal | J. Hydrology: Regional Studies **64**:103234 (2026) |
| DOI | 10.1016/j.ejrh.2026.103234 |
| OSTI ID | 3019881 |
| PDF | https://www.osti.gov/servlets/purl/3019881 |
| PDF md5 | 3fbb8ac27086c58b270ee559d9429738 |
| PDF bytes | 6,667,490 |
| license | CC BY-NC-ND 4.0 |

## Dataset + released artifacts
| item | value |
|---|---|
| HydroShare resource | 43244f815e7947e6bac6b6705a9f7941 |
| citation | Wang, Y. (2026). "CNN-LSTM Coastal Urban Flood Dataset and Source Code", HydroShare |
| license | CC BY 4.0 |
| files listed via `hsapi/.../files/` | 1 file: `Example Dataset.zip` (108,663,214 bytes, HS-checksum `df923c2210d720fdf7bd0602a97da2e2-2`) |
| local md5 of downloaded zip | 9bb7a12f1ae2819c2f035bcb198c540c |

### Zip contents
- `Example Dataset/input/` — 300× `.npy` arrays, shape (128, 128, 11), float64.
  - Naming: `<Event>_<hour>.<qtr>.npy` for two events: `Aug_29_2017` (Hurricane Harvey remnants era) and `Sep_30_2022` (Hurricane Ian era). 150 samples per event, 15-min stride.
- `Example Dataset/output/` — 300× `.npy` arrays, shape (128, 128, 4), float32 — four future 15-min water-depth maps (t+1..t+4), matching paper Table 3.

### Channel decoding (from stats)
| ch | interpretation | evidence |
|---|---|---|
| 0 | DEM (normalized) | constant across timesteps, spatially structured, 16k+ unique values |
| 1 | TWI (normalized) | constant across timesteps, spatially structured, 16k+ unique values |
| 2–9 | past water depth t−7..t | 8 channels, non-negative, mostly zero (only flooded pixels populated), aligns with paper's "8 past time steps" |
| 10 | forcing (rainfall or tide broadcast) | very few unique values (~20), non-negative, small — consistent with a scalar broadcast into a 128×128 map |

### Notable omission
- Despite the HydroShare title claiming "Source Code", the released zip contains **no `.py`, `.ipynb`, `.md`, or `.txt`** — only paired `(input.npy, output.npy)` tensors. The training script had to be reconstructed from the paper's textual description of the architecture (DeepLabv3+ encoder + LSTM head + upsample decoder) and hyperparameters (Adam lr=1e-4, MSE, batch=4, 200 max epochs, patience=20, dropout=0.2, 80/20 split).

## Physical model being emulated
- **TUFLOW** (Syme 2001) 2D unsteady flow model coupled to a 1D pipe/network solver, calibrated for Norfolk VA. Ground-truth water depths for training are TUFLOW outputs (no observational depth field is available city-wide).

## No independent GitHub code repo found
- `git grep` / `web_search` for the paper title + author found the HydroShare landing page and journal article; no separate GitHub repo linked.
