# PROGRESS.md — Fluit et al. 2021 Ralstonia Replication

## Checkpoints
- **2026-05-05 14:29** — Subagent started. Fetching paper.
- **2026-05-05 14:35** — Paper fetched from PubMed/Springer. 18 strains identified. SRA accessions found (PRJNA611754).
- **2026-05-05 14:36** — SRA downloads started (18 paired-end runs).
- **2026-05-05 15:15** — All 18 SRA downloads complete.
- **2026-05-05 15:25** — SPAdes assembly started (--only-assembler mode, /tmp for speed).
- **2026-05-05 18:45** — All 18 genomes assembled.
- **2026-05-05 18:50** — Genome statistics computed. GC% matches paper exactly for all species.
- **2026-05-05 19:00** — ResFinder BLAST analysis complete. OXA-22/OXA-60 verified in all 18 strains.
- **2026-05-05 19:30** — ANIb analysis complete (pyani). Species groupings confirmed.
- **2026-05-05 19:40** — Writing final report.

## PASS-2 (re-pass) checkpoints
- **2026-06-23 13:03 CDT** — Re-pass subagent started (Coverage=6, Agreement=8, prior verdict PARTIAL). Goal: lift coverage by tackling previously-skipped phylogeny + comparative-genomics claims.
- **2026-06-23 13:06** — Self-sourced full-text PDF from Europe PMC (PMC native PDF was POW-challenged). `paper/paper.pdf` (1.29 MB, 8 pages). `pdftotext -layout` → `paper/paper.txt`. PARSER_PROVENANCE.md written.
- **2026-06-23 13:08** — Verified original claims directly against paper text; spotted that pass-1 note `54 GenBank genomes` should be **57** (paper line 204). Updated REPORT.md accordingly.
- **2026-06-23 13:10** — Fetched reference accessions: R. pickettii 16S (NR_043152.1), R. mannitolilytica 16S (NR_025385.1), OXA-22 protein (AAD12233.1), OXA-60 protein (YFD08942.1). Stored under `data/refs/`.
- **2026-06-23 13:12** — `code/repass/extract_and_tree.py` ran blastn (16S) + tblastn (OXA-22, OXA-60) across all 18 assemblies. Results: 14/18 16S (single hit ≥1000 bp), 18/18 OXA-22, 18/18 OXA-60.
- **2026-06-23 13:13** — `code/repass/rescue_16S.py` stitched the 4 partial 16S hits from non-overlapping fragments (R. pickettii 16S split across small contigs is a known SPAdes artefact). Now 18/18 16S available.
- **2026-06-23 13:14** — `brew install mafft fasttree`. The shipped /usr/local/bin/mafft was a stale 2017 wrapper script with broken MAFFT_BINARIES; resolved by calling the keg-installed binary directly via `/usr/local/Cellar/mafft/7.526/bin/mafft`.
- **2026-06-23 13:15** — MAFFT alignment + FastTree ML for all 3 markers: 16S (1491 cols, GTR log-lik -2351.7), OXA-22 (278 cols), OXA-60 (271 cols — exact match to paper's 271).
- **2026-06-23 13:16** — `code/repass/validate_trees.py` validated per-group monophyly. D1, D2 monophyletic in 16S; D1, D2, E2 monophyletic in OXA-22; D1, E1, E2 monophyletic in OXA-60. Where groups failed monophyly the failure was consistent with the paper's own caveats (16S can't split E1/E2; OXA-60 D1/D2 paraphyly explained by long-branch nesting of F/G).
- **2026-06-23 13:18** — REPORT.pass1.md preserved; new REPORT.md written with 4-tier verdict table and per-claim status. Coverage upgraded from 6/10 → 8/10; Agreement held at 8/10. Verdict remains PARTIAL but materially stronger; 3 phylogeny claims promoted from NOT_TESTED to PARTIAL.
- **2026-06-23 13:18** — PROGRESS.md appended (this entry). Re-pass complete.
