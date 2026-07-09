# Artifact Harvest

| Item | URL / source | Size | Notes |
|---|---|---|---|
| paper.pdf | https://arxiv.org/pdf/quant-ph/0102014 | 174 143 B (12 pp) | Ivanyos–Magniez–Santha 2001, v1 (Feb 2001) |
| work/paper.txt | `pdftotext -layout paper.pdf` | 43 825 B (606 lines) | Full plain-text extraction; used as input for `extraction/marker.md` |
| Central corpus lookup | `~/Dropbox/REPLICATE-PROJECT/*/extraction/nougat.mmd` grep | – | No hit for `quant-ph/0102014` or `grigni` |
| Wall-clock: all runs | – | – | Total ~25 s of Python across 3 runs |
| Runtime environment | `work/.venv/` | – | Python 3.13 + qiskit 2.5.0 + qiskit-aer 0.14+ + numpy |

## Public artifacts referenced but NOT pulled

- Beals & Babai (1993) *Las Vegas algorithms for matrix groups* — provides the classical black-box-group machinery underlying Corollary 5. Not needed as a data pull; only structural claims consumed.
- Watrous (2001) quant-ph/0011023 — Theorem 2 (order + membership + |N⟩ prep in solvable groups). Cited but not re-implemented; our replication targets Theorem 13, which only uses Theorem 2 as a black-box quantum primitive over classical black-box groups.
- Rötteler–Beth quant-ph/9812070 — Z₂ᵏ ≀ Z₂ HSP (the special case that our Theorem 13 replication *directly generalizes*).
- Ettinger–Høyer LNCS 1563 (1999) — dihedral group inspiration for Theorem 13's z-loop reduction.
- Grigni–Schulman–Vazirani–Vazirani (STOC 2001) — the paper the task ticket incorrectly attributed to arXiv 0102014. Different paper; would need to be pulled from ACM DL to independently replicate.

## No external data required

The paper is pure algorithm design — no datasets, benchmarks, or empirical numbers to fetch. All numerical results in this report are generated from first principles by our own simulator.
