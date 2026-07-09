# Artifact Harvest — OSTI 2448207

| Artifact | Source URL | Size | Checksum (md5) | Notes |
|---|---|---|---|---|
| OA PDF (SAND2024‑12794J) | https://www.osti.gov/servlets/purl/2448207 | 1,987,154 B | 41204e9adef92fa85c980f66c0d8d39f | Fetched via `ssh uicgpu` proxy (CherryRd blocked on osti.gov). PDF v1.5. |
| Extracted text | (local) work/osti_2448207.txt | 830 lines | — | `pdftotext -layout`. |

## Public code / reference data
- **Paper code:** No public repository is cited in the OA text (SAND report; code is the authors' in‑house MPI/C++ FV tool built on Trilinos/Belos/MueLu). Not released → cannot pull the exact implementation.
- **Reference benchmark ("CWI" case 1):** Bagheri et al. community streamer benchmark (ref [18] in paper). The digitized reference curves live behind the benchmark publication/figures; not fetched (heavy figure OCR + not needed for the analytic/order replication). No proprietary data was required for the checks performed.

## Third‑party tools used (all free/local)
- Python 3.14, numpy 2.4.3, scipy 1.18.0 (local CherryRd).
- Argo proxy `argo:gpt-5.2` (free, localhost:44497) for LLM‑judge scoring.
- uicgpu used only as an HTTP proxy for the PDF fetch (no heavy compute needed; the replication is analytic + a 1D MMS sweep that runs in <2 s locally).
