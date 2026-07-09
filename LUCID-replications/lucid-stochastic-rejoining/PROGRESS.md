# PROGRESS — LUCID replication: Stochastic Model of DNA Fragments Rejoining

**Started:** 2026-05-28 13:47 CDT
**Subagent:** Ollie (LUCID replication batch)
**Target paper:** Li Y, Qian H, Wang Y, Cucinotta FA (2012) *A Stochastic Model of DNA Fragments Rejoining.* PLoS ONE 7(9): e44293. doi:10.1371/journal.pone.0044293
**PDF (local):** `~/Dropbox/XFER/LUCID-replication-targets/7a9fc394e8a779038074bd3b9df6b06e1b5a6e51.pdf`

## Openness

| Check | Status |
|---|---|
| Paper open-access (PLoS ONE) | ✅ (CC-BY) |
| External data needed | ❌ — paper compares to published foci data only, no data file used here |
| Code provenance | Independent reimplementation; no author repo found |
| Endpoints | Free only (local CPU NumPy) |

## Plan & status

| Step | Status |
|---|---|
| Extract paper text + model spec | ✅ done |
| Implement Gillespie direct method for fragment rejoining | ✅ `code/gillespie_rejoining.py` |
| Smoke test (small simulations end correctly) | ✅ all 4 pass |
| Reproduce Fig 4 trend: γ-ray vs Fe-ion kinetics | ✅ 2.3× slowdown for high-LET reproduced |
| Reproduce Fig 3 trends (volume, count, length) | ✅ L\* jump 6.3× reproduced; V and count trends correct |
| Write REPORT.md with claim-by-claim table | ✅ `REPORT.md` |

## Model summary (as extracted)

- Species: DNA fragments of length n bp, in binding states; Ku protein E
  (abundant, constant); residue tags R (both ends blocked), r (one end blocked).
- Critical lengths: **Lm = 15 bp** (min to bind one Ku), **L\* = 45 bp** (above
  which two Ku can bind, one per end).
- 3 reaction channels per Gillespie step:
  1. Recruit Ku on a free end (rate k1 · E per available end).
  2. Join two fragments each with at least one bound Ku (rate k2/V per pair).
     Residue tag of product depends on (n_a, n_b) vs L\*:
     - both ≤ L\*  → R (both ends blocked)
     - mixed       → r (short end blocked)
     - both > L\*  → no residue (ignorable)
  3. Release residue (rate k3 per blocked end).
- Process stops when only one fragment remains (rejoining complete).
- 1 Gy ⇒ 25–35 DSBs ⇒ ~30 fragments. High-LET Fe ion: 70% long / 30% short.
  Low-LET γ: 97% long / 3% short.

## Compute

- CPU Python 3 + NumPy + Matplotlib on CherryRd (host of subagent run).
- No GPU, no network, no paid endpoints.

## Friction tags

- `simplification: single-residue-release` — the paper treats the R-state
  (both ends blocked) and r-state (one end blocked) somewhat loosely; we model
  blocked_ends as 0/1/2 counts with a single k3 per blocked end.
- `parameter: rate-values-not-quantified` — paper does not give numeric k1, k2,
  k3, V; figures use arbitrary units. We choose unit-consistent values that
  reproduce the qualitative biphasic kinetics and the L\* jump.
- `simplification: spatial-geometry` — paper itself uses well-mixed mass action
  with volume scaling, no explicit nucleus geometry. We follow that.
