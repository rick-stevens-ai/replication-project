# Artifact harvest

| Artifact | URL / source | Size | Checksum |
|---|---|---:|---|
| `paper.pdf` (LA-4553-MS, May 1971, the SIAM article authored copy) | https://www.osti.gov/servlets/purl/4060961 (GREEN OA via Semantic Scholar Unpaywall) | 1,340,222 B (31 pp) | SHA-256 `fd92c5ccee14f40c2ed0fd7208f17cfaf079c41a1b9b2bf3f45f2943c5da35b9` |
| `extraction/marker.md` | pdftotext -layout of `paper.pdf` (see file header — marker/nougat unavailable on host) | 65 KB | derived |
| `extraction/nougat.mmd` | stub with paper key math + Table 1 verbatim; pointer to central corpus for future real Nougat parse | 5 KB | derived |
| Semantic Scholar record | https://api.semanticscholar.org/graph/v1/paper/DOI:10.1137/0708066 (S2 API key from Keychain) | — | — |
| Unpaywall record | https://api.unpaywall.org/v2/10.1137/0708066 (best_oa_location=null, but S2's OSTI link works) | 1,172 B | saved as `work/unpaywall.json` |

**Notes on data source:** The paper was originally published in *SIAM J. Numer.
Anal.* Vol. 8, No. 4 (Dec. 1971), which is behind SIAM's paywall. However,
because it originated as a Los Alamos technical report (LA-4553-MS, May 1971)
under an AEC contract, the full manuscript is on OSTI under DOE public-access
mandate. The OSTI copy is verbatim the same paper (same title, authors,
equations, and Table 1) — including the "Also issued as Stanford University
Report CS-71-195" note on the title page.

**Code (this replication):** all in `work/`:
- `capacitance_solver.py` — imbedding + capacitance-matrix on rectangle-with-hole
- `mms_convergence.py` — O(h^2) convergence study using a non-quadratic MMS
- `lshape_splitting.py` — splitting construction on the L-shape (paper §5)
- `diagnose.py` — sign-convention debug used to fix a factor-of-(-1) RHS bug

**Downloaded data:** none — the paper's numerical experiments are on
analytical manufactured solutions, requiring no external datasets.

**Sanity checks / cross-comparison:** every capacitance solve was
cross-checked against an independent `scipy.sparse.linalg.spsolve(A, y)` on
the full irregular-region operator. Agreement is at float64 machine
precision (~1e-15) in every case (see `report/evidence/`).
