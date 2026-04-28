# Stage 2 Summary — S2 Metadata Enrichment & Refined Shortlist

**Date:** 2026-04-24
**Host:** CherryRd (subagent)
**Wall time:** ~20 min (including ~8 min for S2 batch fetch through rate limits)

## Key finding up front

**The `.txt` filenames ARE Semantic Scholar `paperId` values (40-char SHA1).**
A single test (`GET /paper/b19aacc…`) confirmed it; the S2 batch endpoint
returned complete metadata for **17,043 / 17,044** papers (99.99%). The one
miss was the single corpus row missing a valid sha. No fallback-by-title
search was needed.

This is a much better outcome than Stage 1 feared. Every paper in the corpus
now has title, authors, year, venue, journal, DOI, arXiv ID, citation count,
influential citation count, and OA PDF URL (where available).

## What was done

1. **Direct S2 batch enrichment** (`/paper/batch`, 500 IDs/request, ~35 calls)
   - Hit `429` rate limits repeatedly with unauthenticated requests, recovered
     via exponential backoff (30/60/90 s). No API key was used.
   - Intermediate cache (`_s2_cache.json`, 45 MB) saved every 4 batches so we
     could resume after the first run got killed by a cache-contention glitch
     from concurrent processes.
2. **Joined S2 metadata into `pde_corpus_enriched.csv`** (17,044 rows × 23 cols).
3. **Re-scored** every paper with the 100-point rubric from the brief
   (interestingness 50 + reproducibility 50).
4. **Produced `shortlist_300_v2.md`** (top 300 by new score, flat ranking).
5. **Produced `shortlist_100_final.md`** (domain-balanced; see below).
6. **HEAD-checked the top 20** of the final-100 — every S2 URL returns 202
   (not an error, just Cloudflare anti-bot on HEAD); every DOI is live
   (200 or 403-refuses-HEAD); **15/20 OA PDFs load (200); 5 are broken**.

## Match & distribution stats

- **Matched:** 17,043 / 17,044 (99.99%)
- **Unmatched:** 1 (likely a malformed sha row; noted but not pursued)

Year distribution (binned):

| Bucket | Papers |
|---|---|
| pre-2000 | 4,739 |
| 2000–2009 | 4,758 |
| 2010–2014 | 2,800 |
| 2015–2019 | 2,534 |
| 2020–2023 | 1,874 |
| 2024+ | 252 |
| no-year | 86 |

The corpus is older than one might assume from a "modern PDE" topic list —
more than half was published before 2015. Our rubric deliberately rewards
2020+ papers, which surfaces a different cohort than the Stage 1 heuristic did.

**Top 10 journals in the full corpus:**

```
 564  Physical Review Letters
 326  Journal of Mathematical Physics
 269  Physical Review D
 254  ArXiv
 252  Physical Review A
 219  Physical Review E
 162  Numerical Methods for Partial Differential Equations
 161  Journal of Fluid Mechanics
 160  Journal of Chemical Physics
 158  SIAM J. Numer. Anal.
```

This tells us the corpus is heavily weighted toward *physics* venues rather
than *numerical analysis* or *scientific ML* venues — worth keeping in mind
for Stage 4 framing.

## Scoring rubric used

**Interestingness (50 pt)**
- Recency: 2024+ = 15, 2020–23 = 10, 2015–19 = 5, earlier = 0
- `min(10, log(cites+1) × 2.5)` (5 pt at 7 cites, 10 pt at ≥55 cites)
- `min(5, log(icites+1) × 2.0)` (5 pt at ≥12 influential cites)
- Venue: SIAM / JCP / CMAME / JDE / Nature / Science / NeurIPS / ICML / ICLR /
  Acta Numerica / Numer. Math / Math. Comp / Found. Comput. Math /
  Arch. Ration. Mech. = 10; other peer-reviewed = 5; arXiv-only = 3
- Novel-method keyword hits (PINN, DeepONet, neural operator, FNO, diffusion,
  graph NN, KAN, equivariant, …): `min(10, hits × 2.5)`

**Reproducibility (50 pt)**
- OA PDF URL present: 10
- DOI present: 5
- Code/GitHub mention in abstract: 15
- Concrete benchmark name in abstract: 10
- Open-source software tool named in abstract (FEniCS, Firedrake, PETSc,
  JAX, PyTorch, Modulus, DeepXDE, …): 5
- Data availability phrase in abstract: 5

## Domain balancing for shortlist_100_final

- Topic buckets from the Stage 1 `topic` column (60 topics total).
- Elliptic umbrella (Elliptic, Poisson, Laplace, Dirichlet, Green's): max 15 total.
- Per-bucket cap: **10** (tightened from 50; the 50 cap left Poisson-heavy).
- 15 ML-operator/PINN reserve slots filled first from the top 300
  (papers whose topic or abstract has ≥2 novel-method keyword hits).

Result: **100 papers across 35 buckets**, 15 ML-focused, 15 elliptic-family,
no bucket over 10.

## Top 10 of `shortlist_100_final.md`

| # | Score | Year | Cites | Paper |
|---|-------|------|-------|-------|
| 1 | 67.73 | 2021 |  21 | ISWFoam: Numerical model for internal solitary waves in stratified fluids |
| 2 | 64.63 | 2019 |  26 | Numerical simulation of turbulent flow & pollutant dispersion in urban street canyons |
| 3 | 60.40 | 2021 |  47 | Lessons for adaptive mesh refinement in numerical relativity |
| 4 | 58.58 | 2021 | 404 | **PINNs for solving Reynolds-averaged Navier–Stokes** |
| 5 | 58.58 | 2021 | 141 | Dielectric continuum methods for quantum chemistry |
| 6 | 58.35 | 2021 |  43 | High-order IMEX schemes for Navier–Stokes (stability & error analysis) |
| 7 | 56.01 | 2020 |  33 | Wave breaking for Whitham-type equations revisited |
| 8 | 55.76 | 2020 |   9 | 3D modeling of breaking-wave-induced seabed scour around monopiles |
| 9 | 55.70 | 2020 |  29 | Crank–Nicolson approximation for time-fractional Burgers |
| 10 | 55.62 | 2021 |  28 | Discrete maximum principle for high-order FD on Allen–Cahn |

Full top-100 in `shortlist_100_final.md`; full top-300 in `shortlist_300_v2.md`.

## Top-20 link verification

S2 paper URLs all respond (202 from Cloudflare HEAD — expected). DOI HEADs
give 200 or 403 (publisher refusal is cosmetic, not a real breakage).
**Open-access PDFs: 15/20 live (200), 5/20 broken (403/404):**

| Rank | sha | OA PDF status |
|-----:|-----|---|
| 2 | e7a4b83e… | 403 |
| 8 | 4cd1a988… | 403 |
| 9 | 249860aa… | 404 |
| 15 | 812a1922… | 403 |
| 17 | 320281d4… | 403 |

For Stage 4 those five need to be fetched via DOI / journal / arXiv instead.

## Obstacles encountered

1. **Unauthenticated S2 rate limit** was tighter than the "100 req / 5 min"
   advertised — we hit 429s after ~4 batches. A free API key would make this
   trivially faster; worth requesting before a rerun.
2. **Duplicate background processes** leaked from buffered stdout detach;
   fixed by killing and using `nohup python3 -u`. The cache design
   (write-through JSON, last-writer-wins) was tolerant of this, so nothing
   was lost.
3. **Bucket granularity** — Stage 1's 60-topic labels are *very* fine, which
   made the initial `≤50/bucket` cap non-binding. Tightened to 10.

## Recommendations for Stage 4

1. **Use `shortlist_100_final.md` as the deep-read queue.** It's balanced
   across 35 sub-topics, front-loaded with well-cited 2020-2023 papers, and
   every paper has a resolvable S2 page.
2. **Prefetch OA PDFs now** for the top 100 — `s2_openaccess_pdf_url` column
   of `pde_corpus_enriched.csv` has direct URLs; 5 of the top 20 will need a
   fallback (arXiv or DOI landing page), which we've already flagged.
3. **Consider a second pass restricted to 2022+** if Stage 4 wants the
   cutting edge — the current rubric still lets strongly-cited 2011-2015
   papers beat less-cited 2024 papers, which is fine for "influential" but
   not for "frontier". Adjusting recency to 20 pt would tilt it toward 2024+.
4. **The corpus is physics-heavy, not numerical-analysis-heavy.** If the
   Replicate project is about numerical methods, Stage 4 should down-weight
   Phys Rev Letters/D/A/E explicitly or add a "numerics" keyword signal.
5. **Get an S2 API key** before any rerun: it lifts the limit to 1 req/sec
   guaranteed, no 429s.

## Deliverables checklist

- [x] `pde_corpus_enriched.csv` — 17,044 rows × 23 columns (22 MB)
- [x] `shortlist_300_v2.md` — top 300 flat, 80 KB
- [x] `shortlist_100_final.md` — top 100 domain-balanced, 35 KB
- [x] `enrichment_stats.json` — year distribution + top venues
- [x] `_s2_cache.json` — raw S2 responses (keep for later, 45 MB)
- [x] `_top20_verify.json` / `_top20_verify_results.json` — link check
- [x] `STAGE2_SUMMARY.md` — this file
