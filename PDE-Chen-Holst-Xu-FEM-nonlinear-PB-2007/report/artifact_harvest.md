# artifact_harvest

## Public artifacts pulled

| Artifact | Source | URL | Size | SHA-256 |
|---|---|---|---|---|
| Paper preprint (arXiv v1) | arXiv | `https://arxiv.org/pdf/1001.1350` (canonical of 1001.1350v1) | 375 765 B (6-page front matter + full body follow) | `86e6c1fe458e88154561f5f685c12043011b2e457e2dadf31acc6998b9cbdac3` |

The arXiv preprint (`1001.1350v1`) is the openly-available author copy of the SIAM J. Numer. Anal. paper (DOI `10.1137/060675514`, which lives behind SIAM's paywall). All theorem statements, equation numbers (1.1, 2.1, 3.2–3.10, 6.4–6.5) and the split u = uˡ + uⁿ used in the replication were extracted directly from the arXiv PDF via `pdftotext -layout`.

## Software / OSS stack used

| Package | Version | Role |
|---|---|---|
| Python | 3.14.6 (local) | driver |
| scikit-fem | 12.0.2 | P1 Lagrange FEM assembly |
| numpy | 2.5.1 | numerics |
| scipy | 1.18.0 | sparse direct solver |
| meshio | latest pip | (only in venv, unused for this run) |
| Argo proxy (localhost:44497) | ANL-managed FREE endpoint | LLM-judge (model `argo:gpt-5`) |

No external datasets are required by this paper — it is a pure numerical-analysis paper, and the "data" is the paper's PDEs, coefficients (ε_m ≈ 2, ε_s ≈ 80, κ̄² = ε_s κ²) and the FEM error estimate to be checked. No paywalled resources were needed to complete the replication.

## Files produced by the replication

Under `work/`:
- `chen-holst-xu-2007.pdf` — the arXiv preprint (mirrored).
- `chen-holst-xu-2007.txt` — `pdftotext -layout` extraction.
- `rpbe_mms.py` — Test A driver: manufactured-solution 2D RPBE + 7-level convergence sweep.
- `rpbe_twoatom.py` — Test B driver: two-atom RPBE with u = uˡ + uⁿ split.
- `rpbe_mms_results.json`, `rpbe_twoatom_results.json` — machine-readable results.
- `judge.py`, `judge_response_raw.json`, `judge_verdict.md` — LLM-judge scoring.

Under `report/evidence/`: same files above, plus `rpbe_mms_run.log` and `rpbe_twoatom_run.log` capturing full stdout of the two runs (used by the LLM judge as ground truth).
