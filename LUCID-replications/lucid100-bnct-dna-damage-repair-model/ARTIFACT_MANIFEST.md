# Artifact Manifest — LUCID100 slot 42

| # | artifact | local path | source | size | hash/notes |
|---|---|---|---|---|---|
| 1 | Full paper PDF | `refs/paper.pdf` | https://iint.nuaa.edu.cn/_upload/article/files/89/af/226d111b4982ac6eb63ab3e4f1d5/7f7a82cd-5d80-4dd9-841d-f5f8e611a29e.pdf | 3,134,803 bytes | open-access mirror at NUAA; matches Wiley DOI 10.1002/mp.17446 |
| 2 | Plain-text extraction | (transient) `/Users/stevens/.openclaw/workspace/tmp_paper_mp17446.txt` | `pdftotext -layout` from artifact #1 | 658 lines | used for equations / parameters; not kept in workspace because the PDF is the source of truth |
| 3 | MEDRAS analytic code (Python) | `artifacts/medras_analytic/` | https://github.com/sjmcmahon/MEDRAS (shallow clone) | repo | author: Stephen J. McMahon (Queen's University Belfast). License in repo's `readme.md`. |
| 4 | Smoke script | `scripts/medras_bnct_smoke.py` | this work | 5,821 bytes | CPU-only, ~2 s runtime, uses #3 |
| 5 | Smoke output | `artifacts/smoke_output.txt` | `python3 scripts/medras_bnct_smoke.py` | text | LQ fits + RBE table + Eq. 6 mix curve |
| 6 | README | `README.md` | this work | – | overview, methods, QA recommendation |
| 7 | PROGRESS log | `PROGRESS.md` | this work | – | checklist + time log + blockers |
| 8 | First-pass report | `REPORT.md` (also linked as FIRST_PASS_REPORT.md) | this work | – | verdict, comparison table, evidence |

## Not harvested (and why)

- **MEDRAS Monte Carlo source.** Referenced in the paper but not on the public McMahon GitHub. Authors do not provide a code/data availability statement, and the paper has no Zenodo / OSF / supplementary materials link.
- **BNCT extension code (Yu/Geng/Tang).** Not released. The paper does not link to a code repository.
- **Geant4-DNA radial-deposition output tables** for α (10 energies) and ⁷Li (5 energies) at BNCT energies. Not released; would need to be regenerated.
- **TOPAS-nBio F and W dose-factor tables** for BPA / BSH microdistributions. Not released; would need to be regenerated.
- **Cited experimental data sets** (refs 4, 30–40, 41 in the paper — Hiratsuka 1991 melanoma, the various photon/proton/alpha cell-survival datasets used to validate the model). Not bundled here; secondary literature, not part of the replication target.
- **Supplementary material.** Wiley landing page for `10.1002/mp.17446` shows no supplementary data / code links beyond the standard article files (verified via web search; no supplement URLs surface).

## Verification commands

```bash
# Reproduce the smoke output:
cd /Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-bnct-dna-damage-repair-model
python3 scripts/medras_bnct_smoke.py | diff - artifacts/smoke_output.txt
```
