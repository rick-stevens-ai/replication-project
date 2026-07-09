# Artifact manifest — LUCID100 slot 59 (Brahme 2026)

Generated 2026-06-09 by subagent during first-pass harvest.

| Path | Role | Source / provenance | Size |
|---|---|---|---|
| `artifacts/brahme2025_frontiers.pdf` | primary source (review paper, OA) | `https://www.frontiersin.org/articles/10.3389/fonc.2025.1703503/pdf` (CC-BY) | 28 MB |
| `artifacts/brahme2025_frontiers.txt` | pdftotext extraction (used for analysis) | `pdftotext` of the above | 103 KB |
| `artifacts/crossref_brahme2025.json` | bibliographic metadata | `https://api.crossref.org/works/10.3389/fonc.2025.1703503` | 30 KB |
| `artifacts/semanticscholar_brahme2025.json` | metadata + references list | Semantic Scholar Graph API (DOI lookup, fields: title, authors, year, venue, abstract, openAccessPdf, references.title, externalIds) | 19 KB |
| `code/tcp_extreme_value_smoke.py` | smoke replication of Eq. 1 (first pass, preserved) | hand-written from paper text (Eq. 1 and the paragraph immediately after it) | 7 KB |
| `code/brahme2025_full_replication.py` | **FULL closed-form replication (final pass)** — Eq. 1 + Fig. 12 microdosimetry + Fig. 5/6 narrative + closed-form γ50 | hand-written from paper text | 18 KB |
| `results/tcp_eq1_smoke.json` | first-pass numerical pass/fail record | output of the smoke script | 1 KB |
| `results/brahme2025_full_replication.json` | **final-pass full ledger** — every reproducible claim with paper value, reproduced value, delta, pass flag | output of the full-pass script | ~5 KB |
| `figures/tcp_eq1_vs_dose.png` | TCP(D) curve (N0=1e7, D0=1 Gy) | refreshed by full-pass script | ~40 KB |
| `figures/tcp_eq1_pdf.png` | implied Gumbel dose-of-cure PDF (visualises skew/kurt) | full-pass script | ~30 KB |
| `figures/hex_vs_poisson.png` | hex-vs-Poisson microdosimetry visualisation (Fig. 12 caption) | full-pass script | ~30 KB |
| `logs/tcp_eq1_smoke.log` | first-pass run log | output of the smoke script | 1 KB |
| `logs/brahme2025_full_replication.log` | full-pass run log | output of the full-pass script | ~5 KB |
| `report/REPORT.md` | **CANONICAL FINAL VERDICT** — four-tier (SPOT-CHECK ✅), Coverage 2/10, Agreement 10/10, claim-by-claim table, named-blocker section | hand-written | ~16 KB |
| `README.md` | overview + how-to-rerun | hand-written | — |
| `PROGRESS.md` | timeline (updated with final-pass entry) | hand-written | — |
| `FIRST_PASS_REPORT.md` | first-pass scoping (preserved; superseded by `report/REPORT.md`) | hand-written | — |
| `ARTIFACT_MANIFEST.md` | this file (updated) | hand-written | — |

## Things explicitly NOT in this folder

- No supplementary materials — the paper has none.
- No author-released code or data — none exist (verified by grep on full text and by inspection of the Frontiers article landing page).
- No experimental cell-survival or apoptosis data points — all referenced through Brahme's prior book / papers (refs 7, 9, 10, 15).
- No author contact (per task brief: "No author contact").
