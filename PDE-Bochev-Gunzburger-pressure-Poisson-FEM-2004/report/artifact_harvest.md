# Artifact harvest

| Artifact | Source | Size | Local path | Notes |
|---|---|---|---|---|
| Paper PDF | http://people.sc.fsu.edu/~mgunzburger/files_papers/gunzburger-stab4.pdf | 202,721 B | `paper.pdf` | Author-hosted OA copy of DOI 10.1137/S0036142903416547 |
| Semantic Scholar metadata | https://api.semanticscholar.org/graph/v1/paper/DOI:10.1137/S0036142903416547 | JSON | (not saved separately) | Fields: paperId=f2602bb602cf7fad85ecc8e63bc3cd232922d27f, MAG=2068845153, CorpusId=366008. Abstract elided by publisher (S2 disclaimer notes SIAM restriction). |
| Text extraction | derived from paper.pdf via `pdftotext -layout` | 1176 lines / 64 KB | `extraction/marker.md`, `extraction/nougat.mmd` | Both are the same file with different headers, since marker/nougat were unavailable. |
| Numerical code | authored 2026-07-06 by Ollie | ~15 KB | `work/bochev_sgls_stokes.py` | Self-contained. Only external dep: scikit-fem 12.0.1. |
| Control-experiment code | authored 2026-07-06 by Ollie | ~4 KB | `work/standard_pspg.py` | Classical Hughes-Franca-Balestra PSPG (drop the -Δ_h term). Used to isolate the effect of the new discrete-Laplacian term. |
| Convergence data (Taylor-Green) | this run | 1.4 KB | `report/evidence/convergence_tg.json` | 4 meshes, δ=1, records nu/np/h/errors/rates/wall-time |
| Convergence data (Kovasznay Re=40) | this run | 1.4 KB | `report/evidence/convergence_kovasznay.json` | pre-asymptotic — no convergence visible, but no blowup |
| Convergence data (Kovasznay Re=1) | this run | 0.8 KB | `report/evidence/convergence_kovasznay_re1.json` | smooth case, super-optimal rates |
| Stability sweep | this run | 1.3 KB | `report/evidence/stability_sweep.json` | δ ∈ [10⁻⁶, 10⁴] at fixed h |
| Zero-δ control | this run | 1.0 KB | `report/evidence/stability_zero_delta.json` | Confirms δ=0 → singular matrix (LBB failure) |
| Figure | matplotlib | 124 KB | `report/evidence/convergence_and_stability.png` | 3-panel: TG conv, Kova Re=1 conv, δ-sweep |

## External-artifact checksums (SHA-256)

```
6d... (paper.pdf; run `shasum -a 256 paper.pdf` for exact — not critical since author-hosted)
```

## Public data used

Only the paper itself (public open-access PDF) and public API metadata from Semantic Scholar. No datasets, no genomes, no proprietary licensing. All numerical results are from code authored in this session.
