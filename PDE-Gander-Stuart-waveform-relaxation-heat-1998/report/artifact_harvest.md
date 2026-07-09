# Artifact Harvest

| Artifact | Source (URL) | Size | Checksum | Notes |
|---|---|---|---|---|
| paper.pdf | http://stuart.caltech.edu/publications/pdf/stuart39.pdf | 371,802 B | MD5 a5aebcbf1b51887995c676f3bbf44439 | Author (Stuart, Caltech) OA copy of the SIAM paper. Text-layer PDF; extracted cleanly with `pdftotext -layout` (no OCR needed). |
| (alt copy, not downloaded) | https://www.unige.ch/~gander/Preprints/SpaceTimeContAnalysis.pdf | — | — | Gander (Geneva) OA preprint; confirmed present, used as secondary availability check. |

## Notes on availability
- The publisher version (SIAM epubs, DOI 10.1137/S1064827596305337) is **paywalled** (HTTP 403). Two independent OA author copies exist (Caltech + Geneva); we used the Caltech copy.
- **No code or datasets** are distributed with the paper — this is a 1998 theory-plus-numerics paper. The "artifacts" to reproduce are the *test problem* (eq. 4.1) and the *two numerical experiments* (Figs 4.1, 4.2), both fully specified in the text. All solver code here is written from scratch (see `work/`).

## Generated evidence (this replication)
- `report/evidence/results.json` — Exp 1 (2-subdomain, 3 overlaps) + Exp 2 (8-subdomain) measured vs predicted rates, full per-iteration error traces.
- `report/evidence/mesh_robust.json` — C2 mesh-refinement study (dx from 0.02 to 0.0025).
- `report/evidence/fig41_two_subdomain.png` — reproduction of paper Fig 4.1.
- `report/evidence/fig42_eight_subdomain.png` — reproduction of paper Fig 4.2.
- `report/evidence/judges/{gpt-5-2,gemini-2-5-pro,gpt-4-1}.md` — three independent free-Argo LLM-judge referee reports.
