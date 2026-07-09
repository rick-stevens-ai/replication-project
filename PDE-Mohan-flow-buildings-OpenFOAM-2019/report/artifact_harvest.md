# Artifact harvest

## Paper
| Artifact | URL | Size | Checksum |
|---|---|---|---|
| Mohan et al. (2019) PDF (wayback capture) | https://web.archive.org/web/20221224023802if_/https://aip.scitation.org/doi/pdf/10.1063/1.5112334 | 1,835,796 B | sha256 `7c3b2878ab5245ce82fb9bccdcaeda9648146a5589b8f0017093feaee1b68a2f` |
| Extracted text | (local) pdftotext of above | 15,547 B | — |

Note: publisher endpoint returns HTTP 403 + JS anti-bot; Unpaywall says
`oa_status: closed`. Only reliable route is the 2022-12-24 wayback snapshot,
which contains the original AIP-served PDF bytes.

## Code / case files (not "downloaded" — shipped with distro)
| Artifact | Path | Notes |
|---|---|---|
| OpenFOAM 1906 tutorial `simpleFoam/windAroundBuildings` | `/usr/share/doc/openfoam-examples/examples/incompressible/simpleFoam/windAroundBuildings/` on uicgpu | Ubuntu package `openfoam-examples 1906.191111+dfsg1-2build1`. This IS the case the paper ran ("The present case is an example case available in OpenFOAM"). |
| Working copy | `/data/stevens/replicate-mohan-2019-buildings/case/` on uicgpu | Unmodified tutorial + 6-subdomain decompose + t=0..400 output |
| buildings.obj (triangulated building surface) | `constant/triSurface/buildings.obj` | 600,096 lines, 16,107 feature edges |

## Simulation outputs
| Artifact | Where |
|---|---|
| log.simpleFoam (full solver log, 400 iters) | uicgpu:.../case/log.simpleFoam ; mirrored to report/evidence/log.simpleFoam |
| log.snappyHexMesh, log.blockMesh, log.surfaceFeatureExtract | uicgpu:.../case/ |
| Reconstructed t=400 field (U, p, k, epsilon, nut) | uicgpu:.../case/400/ |
| Line profiles (12 .xy files, 6 stations × [U] + [k,epsilon,p]) | uicgpu:.../case/postProcessing/sampleDict/400/ ; mirrored to report/evidence/sampleDict/400/ |
| VTK volume + boundary snapshots | uicgpu:.../case/postProcessing/vtkWrite/ |
| EnSight write | uicgpu:.../case/postProcessing/ensightWrite/ |
| Streamlines (40 tracks, 18,543 samples) | uicgpu:.../case/postProcessing/sets/streamLines/400/ |
| Runtime post-processing rendered images | uicgpu:.../case/postProcessing/visualization/ |

## LLM judge
| Model | Endpoint | Prompt | Verdict |
|---|---|---|---|
| argo:gpt-5.2 (fallback after opus 4.8 502) | http://localhost:44497/v1 key=stevens | /tmp/mohan_judge_prompt.md (6.5 KB) | REPLICATED (see report/evidence/judge_verdict.txt) |

All URLs were fetched between 2026-07-04 08:09 and 08:22 CDT.
