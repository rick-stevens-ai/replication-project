# Artifact harvest — Stim (Gidney 2021)

| Artifact | Source URL | Size | Notes |
|---|---|---|---|
| Paper PDF (arXiv v3) | https://arxiv.org/pdf/2103.02202 | 980,894 B | `work/gidney2021_stim.pdf`; extracted to `gidney2021_stim.txt` (pdftotext -layout, 87,335 chars) |
| arXiv abstract page | https://arxiv.org/abs/2103.02202 | 67,038 B | `work/arxiv_abs.html` |
| Stim (PyPI) | https://pypi.org/project/stim/ | v1.16.0 | `pip install stim` |
| PyMatching (PyPI) | https://pypi.org/project/PyMatching/ | v2.4.0 | `pip install pymatching` |

## Journal / DOI
- Quantum 5, 497 (2021). DOI: 10.22331/q-2021-07-06-497 (OA).
- arXiv DOI: 10.48550/arXiv.2103.02202.

## Software provenance
- Stim is Gidney's own reference implementation (the paper *is* the tool's paper). Replication used the current public PyPI release, not any bundled paper code — a genuine independent re-measurement on new hardware and a newer Stim version.
- No paper ancillary circuit files were used; all benchmark circuits regenerated via `stim.Circuit.generated()`.

## Environment
- Python 3.14.6, numpy 2.5.0, stim 1.16.0, pymatching 2.4.0.
- Host CherryRd (macOS), single-threaded runs. Free/local compute only; LLM judge via Argo proxy (localhost:44497, `argo:gpt-4.1`).
