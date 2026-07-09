# Artifact Harvest

All artifacts retrieved on 2026-07-04 from public GitHub. PDF of the paper
itself was blocked by Cloudflare on both CherryRd and uicgpu; the abstract
was pulled instead from the Semantic Scholar Graph API and the technical
content was cross-verified against the SeisSol repo source, docs
(`docs/tpv13.rst`), and `SeisSol/Examples/tpv12_13/`.

## Paper metadata (Semantic Scholar Graph API)

| Field | Value |
|---|---|
| Title | Off-fault plasticity in three-dimensional dynamic rupture simulations using a modal Discontinuous Galerkin method on unstructured meshes: implementation, verification and application |
| Authors | S. Wollherr, A. Gabriel, C. Uphoff |
| Journal | Geophysical Journal International |
| Year | 2018 |
| DOI | 10.1093/gji/ggy213 |
| S2 Paper ID | 5d42fce8b4559b63a60be4f524f269e035a7e31c |
| Citation count | 87 (as of 2026-07-04) |
| License | CC-BY (hybrid OA at OUP) |
| OA PDF (Cloudflare-blocked) | https://academic.oup.com/gji/article-pdf/214/3/1556/25597520/ggy213.pdf |
| Preprint (TUM mediatum) | https://mediatum.ub.tum.de/1462358 (submitted version) |

## SeisSol source code (github.com/SeisSol/SeisSol, master @ 2026-07-04)

| File | SHA-256 | Bytes | Role |
|---|---|---|---|
| `src/Kernels/Plasticity.cpp` | 05df619d9bee0de69006d31060f9470c273345f48c5629a8efb8dbd2ff4ab87a | 13409 | Reference DP return-mapping kernel (SPDX-FileContributor: **Wollherr, Uphoff**) |
| `src/Kernels/Plasticity.h` | 4ce460f29436526d94368add8ce4a1e6952b6e7f7f774fd6049cca6a358373f9 | 3229 | Kernel API |
| `codegen/kernels/plasticity.py` | 85a699b4fc76ce57b002daeb311d6ce26498f808304b2f0b5bc8d55f81159ad2 | 5034 | Codegen: switches between IP and NB variants via `PlasticityMethod` parameter |
| `codegen/matrices/plasticity-ip-matrices-3.json` | b144a31d52331a68b6dacdc5ca185401d5e7ee98107fa28e53ba9ae9bab596cb | 90228 | Integration-point matrices for order 3 (also present for orders 2, 4, 5, 6, 7, 8 → all seven orders shipped) |
| `codegen/matrices/plasticity-nb-matrices-3.json` | 680901e04c5fc8b776c7882c2de372953bb8aafa07b829300bd841e821e36f56 | 7968 | Nodal-basis matrices for order 3 (also 2, 4, 5, 6, 7, 8) |
| `docs/tpv13.rst` | ba0a718dbf8384890481f61fa062fe439b1e60a249f68ba07cc3c153fc48acaa | 2833 | Paper's benchmark description |
| `docs/tpv12.rst` | 26b00865d060c9f9c30b66eb5ccb7c7105000cbb19f4fda9ecb69e00e5e6e0d7 | 6274 | Paper's elastic-analogue benchmark |
| `docs/dynamic-rupture.rst` | c14f1a1388b5e9848f850c897d48cec7eccaee945b1ff2998ca4c715e3d30299 | 20590 | DG-DR framework docs |

## Benchmark inputs (github.com/SeisSol/Examples, master @ 2026-07-04)

| File | SHA-256 | Bytes | Role |
|---|---|---|---|
| `tpv12_13/parameters.par` | 8b250d8c26551c088d35d340a761dc504d2544ba7ce0e269e92df707cd878d24 | 3188 | SeisSol parameter file for TPV12/13 (Plasticity=1, Tv=0.03) |
| `tpv12_13/tpv12_13_material.yaml` | 6e945bb4ffb7b8aefa1ee04cbbec219d30df2359f5b883b33acc83913387458e | 296 | rho=2700, mu=2.9403e10, lambda=2.941e10, plastCo=5e6, bulkFriction=0.85 |
| `tpv12_13/tpv12_13_fault.yaml` | fbb8441797f3908cf49da755ecc13cbe8dbaa745b8916f94309c7d1a317e6dd8 | 803 | LSW friction, nucleation patch, mu_s/mu_d/d_c |
| `tpv12_13/tpv12_13_initial_stress.yaml` | e9a0a22f9fa52df953c973d7097240814386c7ce957931788694000fc4492dc4 | 791 | Depth-dependent LuaMap for background stress |

Every file listed above is CC-BY / BSD-3-Clause and stored in
`work/seissol_artifacts/`.

## Attempted but blocked

- Direct download of the GJI PDF via CherryRd or uicgpu (both returned
  Cloudflare Turnstile challenge pages of ~5.5 kB HTML, not the 15+ MB PDF).
- TUM mediatum PDF (`https://mediatum.ub.tum.de/doc/1462358/1462358.pdf`)
  returned HTTP 404; the mediatum landing page needs an interactive session.
