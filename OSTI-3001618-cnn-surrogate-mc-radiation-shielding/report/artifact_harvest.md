# Artifact Harvest — OSTI 3001618

| Artifact | Source | URL | Size | Notes |
|---|---|---|---|---|
| paper.pdf | OSTI | https://www.osti.gov/servlets/purl/3001618 | 3.5 MB | The paper itself. Fetched on uicgpu (proxy) 2026-07-02. |
| ENDF/B-VII.1 HDF5 | OpenMC official (ANL Box) | https://anl.box.com/shared/static/9igk353zpy8fn9ttvtrqgzvw1vtejoz6.xz | 1.7 GB | Open nuclear-data library, substitute for JENDL-4.0 (paper); extracted to `/data/stevens/openmc-data/endfb-vii.1-hdf5` on uicgpu. |
| OpenMC 0.15.3 | conda-forge | conda install -c conda-forge openmc | (env) | Open-source Monte Carlo transport code; substitute for PHITS 3.33 (closed, license-controlled). |
| TensorFlow 2.15 | PyPI | pip install tensorflow==2.15 | (env) | Same framework used by the paper (paper says "TensorFlow v2"). |

**Paper-side artifacts that do NOT exist:**
- No code repository (no GitHub, no Zenodo).
- No trained model weights.
- No training dataset.
- No supplementary materials.

This is the reason the replication had to regenerate the entire training
set with an independent MC code before it could train and evaluate the
CNN. The paper's methods section is detailed enough that this is
possible; the burden shifts entirely to the replicator's compute.
