# Artifact harvest

| Artifact | URL / provenance | Size | Notes |
|---|---|---|---|
| Paper PDF (`work/paper.pdf`) | https://www.osti.gov/servlets/purl/2570716 (downloaded via uicgpu proxy on 2026-07-04) | 4,420,594 B | Full open-access text of Wang et al. 2025, *Adv. Water Resour.* 203:105024 (CC BY-NC). |
| Paper full text (`work/paper.txt`) | `pdftotext -layout paper.pdf paper.txt` | 1,081 lines | Layout-preserving text extraction; used for claim mining. |
| Freyberg problem geometry | Text of paper §3; grid 20 cols × 40 rows, 250 m cells, exponential covariogram, range=1 km, sigma=0.1823 in log-space (mean K=11.1 m/day). | — | Reproduced synthetically; MODFLOW-6 forward solver not invoked (would require MF6 install + Freyberg model file from PEST++ tutorial repo — deferred as out of scope for a single-agent replication). |
| PEST++ / PyEMU (referenced) | https://github.com/usgs/pestpp; https://github.com/pypest/pyemu | — | Not downloaded; would be needed for the paper's iterative-ensemble-smoother inverse-problem comparison (also out of scope here). |
| MODFLOW-6 (referenced) | https://github.com/MODFLOW-ORG/modflow6 | — | Not downloaded; we used a self-contained scipy sparse finite-volume solver as the reference forward model. |
| PyTorch 1.11 + CUDA on uicgpu (A100) | pre-installed | — | KL-DNN training. |
| scipy 1.10.1 sparse solver | `scipy.sparse.linalg.spsolve` | — | Reference PDE solves (2200 samples in 28 s). |

No new external network fetches beyond the OSTI PDF; the replication is fully self-contained given `numpy`, `scipy`, `torch`.
