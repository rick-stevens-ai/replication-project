# Artifact Harvest

## Paper
- **Title:** Nitsche's method for general boundary conditions
- **Authors:** Mika Juntunen, Rolf Stenberg
- **Venue:** Mathematics of Computation 78 (2009), no. 267, 1353–1374
- **DOI:** [10.1090/S0025-5718-08-02183-2](https://doi.org/10.1090/S0025-5718-08-02183-2)
- **PDF URL:** https://www.ams.org/journals/mcom/2009-78-267/S0025-5718-08-02183-2/S0025-5718-08-02183-2.pdf
- **Path:** `work/paper.pdf`
- **Size:** 465,204 bytes, 22 pages
- **md5:** `fd50163f25bdb130aa06fb2a8241fdda`
- **License / access:** AMS BRONZE open access (per Semantic Scholar `openAccessPdf.status`).
- **Note:** The AMS server serves the paywall HTML unless a browser-style `User-Agent` is sent; retrieved via `curl -A "Mozilla/5.0 ..."` from `ssh uicgpu`.

## Software / dependencies

| Component | Version | Source |
|---|---|---|
| Python | 3.14.6 | /usr/local/bin/python3 (macOS CherryRd) |
| scikit-fem | 12.0.1 | pip |
| numpy | 2.4.3 | pip |
| scipy | 1.18.0 | pip |
| pdftotext (poppler) | – | /usr/local/bin/pdftotext |

No external LLM API used inside the replication code (all Python numerical). LLM used only for report drafting.

## Related references pulled

- Stenberg's publication list (Aalto University): https://math.aalto.fi/~rstenber/Stenberg-Publications.pdf — used to confirm authoritative paper title/venue and to sanity-check that no free preprint version is posted separately.
- Semantic Scholar record: https://www.semanticscholar.org/paper/655bbc1cd240c85f078810fbdaf10e47b57e26ad — provided the `openAccessPdf.url` field.

## Evidence produced in this replication (under `report/evidence/`)

| File | What it contains |
|---|---|
| `results_final.json` | Full convergence + condition-number sweep (5 mesh sizes × 7 ε values, Nitsche; and 6 ε values, traditional). Also contains T1 consistency and T2 coercivity results. |
| `results_conv.json` | Earlier sweep run (pre corrected `g`, retained for provenance). |
| `results_coerc.json` | T2 coercivity λ_min table (n_x × ε). |
| `results_cons.json` | T1 consistency residual `‖A·Π_h u − b‖/√N` on the mesh sequence. |
| `mms_verify.json` | Manufactured-solution verification with nterms ∈ {1, 3, 21}, isolating discretization rates. |
| `gamma_sweep.json` | Stability-parameter sweep confirming Theorem 3.2's sharp bound `γ < 1/C_I`. |
| `aposteriori.json` | Simplified a posteriori estimator effectivity index. |

## No data downloads other than the paper itself.

This is a pure numerical replication: the paper's Sec. 6 defines its own manufactured problem analytically (Fourier series with 21 coefficients on Ω=(0,1)×(0,0.3)), so no external experimental datasets are needed.
