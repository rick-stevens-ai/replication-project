# Artifact Harvest — OSTI 2881485

## Primary paper
| Type | Source | Size | Notes |
|------|--------|------|-------|
| PDF | https://www.osti.gov/servlets/purl/2881485 | 4 027 724 B | PRX Quantum 7, 020327 (2026), DOI 10.1103/lx8x-z29x |

## Author code + data release (Zenodo → GitHub)
| Type | Source | Size | Notes |
|------|--------|------|-------|
| Zenodo record JSON | https://zenodo.org/api/records/19695739 | — | concept DOI 10.5281/zenodo.19612185, release v0.0.2 (2026-04-22), license CC-BY-4.0 |
| GitHub source | https://github.com/y-oda2/ibmq-noise-modeling (tree v0.0.2) | — | linked as `isSupplementTo` |
| Release ZIP | https://zenodo.org/api/records/19695739/files/y-oda2/ibmq-noise-modeling-v0.0.2.zip/content | 8 423 674 B | md5:f7b46bf4e11fe6ccdee67fa07c80a97b |

### Contents of ZIP used for this replication
| File | Size | Purpose |
|------|------|---------|
| README.md | 7 610 B | figure-to-notebook + data-file mapping |
| notebooks/fig_09_vqe_H2.ipynb | 92 378 B | canonical Fig 9 pipeline (used here) |
| notebooks/imports_IBM_NM.py | 60 789 B | shared Python module |
| data/g_values.csv | 6 032 B | Bravyi–Kitaev H₂ coefficients g₀..g₅ over 54 R values (0.20-2.85 Å) |
| data/VQE_H2_theta_opt.p | 3 230 B | pickled dict `{'θopt': [...], 'Emin': [...]}` — noiseless-optimized θ per R |
| data/VQE_exp.p | 582 B | pickled ndarray, ibm_algiers hardware energies (54 R × 100k shots × 3 bases) |
| data/VQE_sim_IBM.p | 582 B | pickled ndarray, IBM FakeHanoi noise-model Aer sim energies |
| data/VQE_sim_NM.p | 582 B | pickled ndarray, custom non-Markovian (LME + SchWARMA/mezze) sim energies |
| data/optimal_schwarma_params.p | 227 B | fitted SchWARMA (b̂,â) coefficients from 1/f dephasing PSD |
| data/LME_calculations.nb | 101 062 B | Mathematica notebook with symbolic LME derivations |
| data/CDF_Ts.p | 4 077 B | T1/T2 across 7 IBM devices |
| data/CRp45_X_CRm45_X-Utom-circs-lagos.p | 1 207 382 B | ECR tomography circuits (Fig 7) |
| data/data_FIG4.p, data_FIG5.p, data_FIG7.p, data_FIG8.p | ~30 KB total | pickled fig-specific experimental data |
| data/figdata-corr_deph-{DD,FTTPS_PSD,PSDs}.p | ~470 KB | reconstructed dephasing PSDs |
| data/fttps_corr.p, ps_1f0.p, ps_exps_algiers_char.p, ps_sims_FIG3.p, gif_fttps_res.p, markov_plot_data.p | ~120 KB | additional FTTPS + characterization data |

## Software environments used
| Tool | Version | Source |
|------|---------|--------|
| Qiskit | 2.5.0 | conda `/data/stevens/envs/qexpr` (uicgpu) |
| Qiskit-Aer | 0.17.2 | same env |
| qiskit-ibm-runtime | 0.47.0 | installed via `pip install` into qexpr (needed for `FakeHanoiV2` because Qiskit 2.x dropped the v1 fake providers) |
| numpy / scipy | 1.26.x / 1.13.x | qexpr defaults |
| Marker | (env `/data/stevens/envs/marker`) | Datalab/marker-pdf, CUDA 12 |
| Nougat | (env `/gpustor/stevens/anaconda3/envs/nougat`) | facebookresearch/nougat 0.1.17 |
| pdftotext | 22.02.0 (poppler) | system on cherryrd |

## Endpoints used (all FREE)
| Purpose | Endpoint | Model |
|---------|----------|-------|
| LLM judge | http://<tailnet-aggregator>:4000/v1 (LiteLLM aggregator on cherryrd) | `argo:gpt-5.4` (Opus 4.8 was 502 at the time) |
| Compute | ssh uicgpu (8×A100 UICGPU) | local |

## Not fetched / out of scope
- IBM Quantum live hardware (would require IBM Q account + queue time; the paper's `VQE_exp.p` provides the same hardware measurements).
- `mezze` (JHU APL package) — not on PyPI, not on GitHub; required to independently regenerate the non-Markovian SchWARMA trajectories from `optimal_schwarma_params.p`. Would need author distribution.
