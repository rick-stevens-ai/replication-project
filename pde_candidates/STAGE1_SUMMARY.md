# Stage 1 Summary — PDE Corpus Heuristic Pass

**Date:** 2026-04-24
**Host:** m1-mac-mini (Argonium source is fully local, 8.4 GB)
**Wall time:** ~6 minutes (incl. corpus recon)

## Corpus Reality Check (Important)

The task brief expected ~22K abstract+full-text extracts at `~/Dropbox/PIPELINE/PDE/papers/`. Actual state on disk:

| Location | Expected | Reality |
|----|----|----|
| `~/Dropbox/PIPELINE/PDE/papers/*.txt` | 21,856 text extracts | **21,855 files, all 0 bytes** (never populated — not Dropbox stubs, truly empty) |
| `~/Dropbox/PIPELINE/PDE/papers/*.pdf` | 22,085 PDFs | 8,649 present, Dropbox online-only (0 B local footprint) |
| `~/Dropbox/PIPELINE/PDE/PDE.jsonl` | metadata | **empty file** |
| `~/Dropbox/PIPELINE/PDE/PDE.ids` | arXiv/DOI IDs | **empty file** |
| `~/Dropbox/Argonium/PDE-EQNs/` | 6,842 PDFs in subdirs | ✅ present + **25,921 .txt files, 8.4 GB, fully local, topic-organized** |
| `~/Dropbox/Argonium/PDEs.1/` | — | 833 PDFs, no txts |

Sha sampling showed **zero overlap** between PIPELINE and Argonium. The Argonium corpus is the usable one.

**Critical data-shape finding:** the `.txt` files are **abstract-only dumps** (Semantic-Scholar style, sha256-keyed). They do **not** contain titles, authors, year, DOI, journal, or full text — just the abstract body, typically 500–3000 chars. That invalidates the title/author/year extraction part of the brief. Signals available for heuristic scoring:

1. Abstract text (keyword matching)
2. Topic label from subdirectory (60 topic categories)

## What Was Produced

All outputs under `~/Dropbox/REPLICATE-PROJECT/pde_candidates/` (syncs to CherryRd via Dropbox):

| File | Rows | Size | Description |
|----|----|----|----|
| `pde_corpus.csv` | 17,044 | 9.4 MB | Deduped corpus with sha, topic, synthetic title, abstract (500 char), wordcount, score |
| `shortlist_300.md` | 300 | ~80 KB | Ranked top 300 with rationale + sha lookup appendix |
| `domain_balance.json` | — | — | Family-level counts for top 300 vs full corpus |
| `_dedup.json` | 17,044 | 12 MB | Intermediate data (usable for re-scoring without re-parsing) |

## Pipeline Details

- **Parsed:** 23,232 unique shas → 17,234 with >150 bytes of content (the rest were 0-byte or near-empty placeholders inside Argonium subdirs)
- **Deduped:** content-hash on first-15-words of abstract (titles are absent, so this replaces the title-hash approach in the brief) → 190 near-duplicates merged → **17,044 unique papers**
- **Scored** 0–85 on the brief's rubric (recency 15 pts effectively disabled — see below)

## Score Distribution

| Threshold | Count |
|----|----|
| ≥ 40 | 1 |
| ≥ 30 | 20 |
| ≥ 20 | ~320 |
| ≥ 10 | ~6.8 K |
| median | 10 |
| max | 41 |

Scores are much more compressed than the brief anticipated because:
1. **Recency (15 pts) rarely fires** — abstracts don't routinely cite their own publication year; when a year is present it's usually a cited work, not this paper. Top-300 picks ended up ranked almost entirely on methods + domain + reproducibility signals.
2. **Abstracts are short** — often only 1 keyword category fires beyond the topic-match.

This means the top 300 is still a useful shortlist for Rick's review, but the scores are better read as **ordinal relative rank** than as absolute quality measures.

## Top 300 — Family Balance

| Family | Count |
|----|----|
| Elliptic (Laplace/Poisson/Dirichlet/Green/biharmonic) | 80 |
| Finite Element / Mesh / DD / Multigrid | 46 |
| Fluid / CFD / Navier–Stokes | 44 |
| Hyperbolic / Shock / KdV / Wave | 27 |
| Parabolic / Time-Dependent | 20 |
| Spectral / Galerkin / High-Order | 15 |
| Quantum / Schrödinger / Klein-Gordon / NR | 13 |
| Finite Volume / Difference | 10 |
| Stochastic / Brownian | 10 |
| Climate / Weather / Atmos | 9 |
| Electromagnetics / Maxwell | 8 |
| Analysis / Stability / Convergence | 4 |
| Finance / Black–Scholes | 2 |
| Other/Applied (Cole-Hopf, Telegraph, BEM…) | 12 |

**Flags:**
- ⚠️ **Over-weighted:** Elliptic (80/300 ≈ 27%). Driven by the Argonium subdir structure splitting elliptic work across 5+ categories (Laplace, Poisson, Dirichlet problem, Green's function Poisson, Biharmonic, Elliptic PDEs FEM) — each contributing hits. If Rick wants even coverage we should cap elliptic at ~40 and let others in.
- ⚠️ **Thin:** Analysis/Stability/Convergence (4), Finance (2).
- ⚠️ **Missing from dedicated family but embedded in others:** "Biomedical/Cardiovascular" — didn't get its own count because there's no topic subdir for it. But cardiovascular-flavored papers did make top 300 via the Navier–Stokes topic (see rank 3). Similarly "ML-Enhanced/Operator Learning" — no topic subdir exists, but the method is cross-cutting (PINN/FNO/neural-operator abstracts appear under Poisson, high-order, spectral, etc.; see ranks 10, 19, 8).

## Obstacles & Known Limitations

1. **No title/author/year/DOI/journal metadata in the text files.** The `filename/title/abstract/authors/year/doi/journal/wordcount/score` CSV schema from the brief is filled in, but `title` is synthetic (first ~15 words of abstract), `authors/doi/journal` are empty, and `year` is best-effort (max of any 4-digit year mentioned in the abstract; mostly `—`).
2. **PIPELINE corpus is unusable as-is.** 17K PDFs are Dropbox online-only (would need bulk download + OCR/extraction). Their txts were never generated. If Rick wants the PIPELINE papers included, that's a separate ~1–2 hour job: `find … -name '*.pdf' | xargs dropbox-cli download`, then `pdftotext` each.
3. **Short abstracts under-score.** A paper with a 300-char blurb can't hit enough keyword categories to break 20 pts even if it's great.
4. **Dedup is content-based, not true-duplicate-based.** Two different papers with near-identical first sentences ("We consider the numerical solution of …") could collapse. Only 190 merges happened, so this is probably fine.

## Recommendations for Stage 4 (deep read ~100 picks)

1. **Metadata enrichment first.** Before deep-reading, resolve each sha → real title/authors/year via Semantic Scholar batch API (`POST /graph/v1/paper/batch` supports 500 shas per request → ~35 requests for the whole top 300, ~2 minutes of wall time). This unlocks proper recency scoring, author-level credibility filtering (famous groups vs student work), and journal prestige.
2. **Re-rank top 300 after adding year.** Papers 2020+ should naturally rise; the current top is heavily code/benchmark/method-keyword driven.
3. **Rebalance the final 100.** Suggested caps for even coverage:
   - Elliptic: 15 (down from 80 share)
   - Fluid/CFD: 15
   - FEM/Mesh: 15
   - Hyperbolic: 12
   - Parabolic: 10
   - Spectral/High-order: 8
   - Quantum: 8
   - FV/FD: 5
   - Stochastic: 5
   - Climate/Weather: 4
   - EM/Maxwell: 3
   - **Reserved ML-operator / PINN slot (cross-cutting): 15** — hand-picked from any family where PINN/FNO/neural-operator keywords appear.
4. **Fetch the PDFs for the final 100.** At that point, 100 PDFs from Argonium (already local) + any PIPELINE-exclusive ones (fetch on demand) is a tractable set for LLM deep-read.
5. **Revisit PIPELINE PDFs only if** Rick wants broader 2024-2025 coverage that Argonium might miss. A quick `ls -lt` check on Argonium file dates would tell us the freshness window.

## Deliverable Paths

```
~/Dropbox/REPLICATE-PROJECT/pde_candidates/
├── pde_corpus.csv          (17,044 rows, schema per brief)
├── shortlist_300.md        (ranked, with rationale + sha lookup)
├── domain_balance.json     (family counts + imbalance flags)
├── STAGE1_SUMMARY.md       (this file)
└── _dedup.json             (intermediate — useful for Stage-4 re-scoring)
```
