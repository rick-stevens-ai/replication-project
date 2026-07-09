# Artifact harvest — OSTI-3015376

All artifacts pulled to `uicgpu:/home/stevens/replicate/osti_3015376/`.

## Paper
| # | source | URL | size | dest |
|---|---|---|---|---|
| 1 | OSTI PURL | https://www.osti.gov/servlets/purl/3015376 | 5,718,090 B | `work/osti_3015376.pdf`  sha256=`2660fafad03e77af405293034dd61e30d6f27a0e8a4a32bc883f4ecbcbe42644` |

## Code
| # | source | URL | note |
|---|---|---|---|
| 2 | GitHub repo | https://github.com/zhbai/AerosolML | cloned to `uicgpu:~/replicate/osti_3015376/AerosolML/`; last push 2026-01-13 |
| 2a | `src/ADON/utils.py` | | BranchNet + TrunkNet + MyNet_ADON class defs |
| 2b | `src/ADON/Inference_ADON.py` | | inference driver — takes trained `.pth` + `saved_data.nc`, produces `output` tensor for 1 time slice |

## Data (Zenodo record 18226529, DOI 10.5281/zenodo.18226529, published 2026-01-12)
| # | filename | size | purpose |
|---|---|---|---|
| 3 | `lat.npy` | 172,928 B | 21,600 grid-column latitudes |
| 4 | `lon.npy` | 172,928 B | 21,600 grid-column longitudes |
| 5 | `lev.npy` | 704 B | 72 model pressure levels |
| 6 | `saved_data.nc` | 398,603,672 B | test-slice bundle: X_test (1,214,140×39 cloud-free features), cldfr_idx, mean_X, std_X, mean_y, std_y, basis (20×20 PCA), ymean (20) |
| 7 | `X_test5.npy` | 777,411,328 B | secondary test slice: 1,214,705×80 (partly pre/post redundancy) — column semantics undocumented |
| 8 | `model_Gelu_L1_500epoch_cbrt_DON53_PODloc_Ens1_4season_8days_43_20_sbatch.pth` | 1,307,346 B | **trained ADON-PCA weights** (500 epochs, cbrt transform, 43 in / 20 out, 4-season 8-days training set, sbatch checkpoint) |

## Environment
- host: `uicgpu` (8× A100, ai2 env)
- Python 3.11, PyTorch 2.5.1+cu121, xarray 2026.4.0, netCDF4 1.7.4, torchvision 0.20.1+cu121, numpy 1.26.4
- CUDA visible, 8 GPUs online

## Provenance / integrity
```
ssh uicgpu 'cd ~/replicate/osti_3015376/AerosolML/src/ADON && sha256sum *.npy *.nc *.pth 2>/dev/null'
```
(hashes captured in `evidence/sha256.txt`)
