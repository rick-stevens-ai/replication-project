# Artifact harvest

Everything pulled from public sources for this replication.

| # | Source | URL | Size / count | Local path | Notes |
|---|---|---|---|---|---|
| 1 | OSTI PDF | https://www.osti.gov/servlets/purl/3365708 | 1,475,908 bytes; PDF v1.4; 16 pages | `work/paper.pdf` | Downloaded via uicgpu (CherryRd cannot reach osti.gov). MD5 not computed but byte count matches upstream `Content-Length`. |
| 2 | Extracted text | (from above) | 1207 lines / 88 KB | `work/paper.pdf` → pdftotext → *in memory* (no separate file kept in tree) | `pdftotext -layout` from Poppler. Also copied to `~/.openclaw/workspace/tmp/osti_3365708.txt`. |
| 3 | Reference implementation (Julia) | https://github.com/oskar-leimkuhler/TNQE-Julia/ | Not cloned | — | Cited by paper's "Code availability" statement. We did not use it (Julia + ITensor toolchain out of scope for a pure-Python CPU replication). |

Compute artefacts produced entirely by this replication run:

| Path | Description |
|---|---|
| `work/venv/` | Local Python 3.14 venv (numpy 2.5.1, scipy 1.18.0) |
| `work/tnqe_replication.py` | From-scratch implementation (~600 lines): MPO builders, ED, MPS ops, two-site DMRG, LC-MPS generalized eigensolver |
| `report/evidence/results.json` | Numerical results (all four experiments) — energies, errors, S/H matrices |
| `report/evidence/run.log` | Stdout of the run |
| `report/evidence/llm_judge.json` | Argo Claude-Opus-4.8 verdict on the report |

No external data downloads other than the OSTI PDF. No chemistry inputs (would need PySCF STO-3G integrals for H2O and H6, which we did not pull).
