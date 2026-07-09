# Artifact Harvest — Zingaro 2021 replication

## Primary paper

- **PDF**: arXiv 2110.02114 v2 — downloaded from `https://arxiv.org/pdf/2110.02114v2`
  - Local path: `work/zingaro_2021_arxiv.pdf`
  - Size: 10,027,445 bytes (10.0 MB)
  - Pages: 39
  - Published venue: Discrete and Continuous Dynamical Systems - S 15(8) 2391-2427 (2022)
  - Related DOI: 10.3934/dcdss.2022052

## Reference software: lifex-cfd (LGPLv3)

- **Zenodo record**: 10.5281/zenodo.13941312 (v2.0.0, 2024-10-16)
- **AppImage binary** (Linux x86_64): `lifex_fluid_dynamics-2.0.0-x86_64.AppImage`
  - URL: `https://zenodo.org/api/records/13941312/files/lifex_fluid_dynamics-2.0.0-x86_64.AppImage/content`
  - Size: 142,931,136 bytes (143 MB)
  - SHA256: `e91843b49d9326b9d0f8788dee66df65d3d16b2af0655d79daca80418947ff63`
  - Host: uicgpu (`/home/stevens/zingaro-replication/work/`)
  - License: LGPLv3
- **Examples zip**: `lifex-cfd_examples.zip`
  - URL: `https://zenodo.org/api/records/13941312/files/lifex-cfd_examples.zip/content`
  - Size: 122,408,870 bytes (117 MB)
  - SHA256: `1075bd4ad5e60acd8a8d47c91e37ae1505e11049e50119b0f955c6dc4414c556`
  - Contains 4 pre-configured benchmarks:
    - `aorta/` — patient-derived aorta CFD (165 MB `.msh` mesh + boundary CSV)
    - `atrium/` — Zingaro-family LEFT ATRIUM run (390K-cell mesh, 125 MB;
      `la-displacement-3heartbeats.vtp` prescribed motion for 3 heartbeats;
      `la-boundary-data.csv` pulmonary-vein & mitral-valve pressures;
      `mv.vtp` immersed mitral-valve surface for RIIS)
    - `cylinder/` — oscillating-pipe benchmark (Hypercube-cylinder mesh, pulsatile Dirichlet inlet, `displacement_cylinder.vtp` for ALE, `cylinder_plane_closed.vtp` for RIIS valve)
    - `tgv/` — Taylor-Green vortex (analytical verification; **NOT** runnable
      with released AppImage: it uses the `Test fluid dynamics cube` subsection
      exposed only in dev/test binary)

## Reference paper for lifex-cfd release

- arXiv 2304.12032 — "lifex-cfd: an open-source computational fluid dynamics solver for cardiovascular applications" (Africa, Fedele, Regazzoni, Salvador, Africa, Zingaro, Bucelli, Dede', Quarteroni 2023)
- **License model verification**: LGPLv3, actively developed at Politecnico Milano MOX group (same authors as our target 2021 paper)

## Zygote geometry

- Referenced as `[55]` in Zingaro 2021 = Zygote Media Group Solid 3D Male
  heart model, commercial. NOT included in the Zenodo dataset by license.
- The Zenodo `atrium/data/la-390K.msh` mesh IS the Zygote-derived atrium
  chamber, provided as a redistributable pre-generated FE mesh.
- Full LH mesh (LA+LV+AA, 1.63M tetrahedra) referenced in Zingaro 2021
  Table 2 is NOT publicly released; the atrium-only subset (390k) IS.

## Compute host

- **uicgpu01** (Ubuntu 20.04, glibc 2.31, 255 cores, 2 TiB RAM, 532 GB free scratch,
  Open MPI 4.0.3, `/usr/bin/fusermount` available for AppImage)
- Runs launched from `~/zingaro-replication/work/`
- Proxy for outbound HTTP: `http://<lan-host>:3128` (sourced via `~/env.sh`)

## Local (CherryRd) artifacts

- `work/paper_text.txt` — pypdf-extracted full paper text (~96k chars, 2168 lines)
- `work/lv_surrogate.py` — independent 0D/1D surrogate (this replication)
- `report/evidence/surrogate/surrogate_biomarkers.json` — surrogate outputs
- `report/evidence/surrogate/surrogate_waveforms.npz` — waveforms V(t), Q(t), P_ao(t), mitral velocity
