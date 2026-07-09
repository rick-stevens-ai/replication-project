# Artifact Harvest — OSTI-3020618

| Artifact | URL / accession | Size | Notes |
|---|---|---|---|
| paper.pdf | https://www.osti.gov/servlets/purl/3020618 | 5,596,644 B | md5 `114313e8161466469aa3a3f8be2da4c8`; PDF 1.7; fetched 2026-07-05 18:08 CDT via uicgpu proxy |
| paper (arXiv preprint) | https://arxiv.org/abs/2602.13826 | ~5.6 MB | Same as OSTI PDF (arXiv:2602.13826v1, 14 Feb 2026); not re-downloaded to save bandwidth |
| paper.txt (pdftotext -layout) | derived | 4969 lines | archived at `extraction/pdftotext.txt` and `extraction/marker.md` |
| Ref [47] Keeble & Rios 2020 | arXiv:1911.13092 | — | The primary deuteron NNQS paper — used only as *description of method*; no external download or reuse of their code (independent reimplementation from paper text). |
| Ref [48] Gnech et al. 2022 | arXiv:2202.05009 (PRL 129) | — | Source of Table 4.1 SJ pionless-EFT numbers. Not downloaded; not attempted in this wave. |
| Yamaguchi potential form | Yamaguchi 1954 PhysRev.95.1628 | — | Public-domain analytic form used for the S-only benchmark. |
| deuteron_results.json | this run | 17.8 kB | Full sweep numeric results |
| run.log | this run | 1.7 kB | Sweep log |
| nnqs_deuteron.py | this run | 13 kB | Replication code, all in-repo |

No external data downloads were needed beyond the OSTI PDF itself: the Yamaguchi potential is analytic and the exact-diagonalization benchmark is self-contained.
