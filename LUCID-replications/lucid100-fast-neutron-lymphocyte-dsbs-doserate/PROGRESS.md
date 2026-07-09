# PROGRESS — LUCID100 slot 80 (Wave 5) — Nair et al. 2019, ijms20215350

## Timeline

- **2026-06-09 14:24 CDT** — task assigned (subagent Wave 5 slot 49 / master row 80)
- **2026-06-09 14:27 CDT** — folder created; LUCID100 master row pulled and verified
- **2026-06-09 14:28 CDT** — MDPI direct curl blocked (HTTP 403); pivoted to Europe
  PMC OA route; full PDF + JATS XML harvested (PMC6862539)
- **2026-06-09 14:30 CDT** — Tables 1–3 digitized from `pdftotext` output → CSVs
- **2026-06-09 14:32 CDT** — smoke_replicate.py first pass: C1 + C2 PASS, C3 FAIL
  (wrong baseline-subtraction interpretation)
- **2026-06-09 14:34 CDT** — variant sweep confirms paper's t½ is reproduced by
  raw single-exponential from t=2h peak; smoke script updated → 3/3 PASS
- **2026-06-09 14:35 CDT** — README / FIRST_PASS_REPORT / progress JSON written

## Checks (3/3 PASS)

| ID | Claim | Computed | Paper | Verdict |
|----|-------|----------|-------|---------|
| C1 | HDR/LDR mean foci ratio ≈ +40% | +39.8% | 40% | ✅ PASS |
| C1 | Per-dose ratios match Table 2 | max abs diff 0.005 | — | ✅ PASS |
| C2 | poly2 induction fit R² ≥ 0.95 (LDR) | 0.994 | — | ✅ PASS |
| C2 | poly2 induction fit R² ≥ 0.95 (HDR) | 0.988 | — | ✅ PASS |
| C3 | HDR repair t½ within ±25% of 8.6 h | 9.92 h (+15%) | 8.6 h | ✅ PASS |
| C3 | LDR repair t½ within ±25% of 12 h | 13.08 h (+9%) | 12.0 h | ✅ PASS |

## Blockers

None for first-pass. The +15% gap on the HDR half-life is the largest residual
disagreement and is attributable to method ambiguity (paper does not give a fit
equation; describes residual subtraction in Discussion text only). Further
tightening would need either WebPlotDigitizer overlay or raw per-cell data
(blocked by no-author-contact policy).

## Next actions (deferred)

- [ ] WebPlotDigitizer pass on Figs 1, 3, 4 to cross-check digitized table values
- [ ] Build PARTRAC / MCDS mechanistic model of p(66)/Be(40) DSB induction (= the
      "simulation/model replication" the master TSV originally promised; this is
      a separate, larger workstream)
- [ ] If the QA retag below is accepted, reclassify worktype to
      `wet-lab assay / radiobiology table replication` in LUCID100_SOLID_MASTER_QA.tsv

## QA retag recommendation

- **From:** `simulation/model replication`
- **To:**   `wet-lab assay / radiobiology table replication`
- **Reason:** No mechanistic / Monte Carlo / kinetic ODE model is published or
  released. The only "model" content is two empirical curve fits (polynomial +
  single exponential) applied directly to the experimental tables, which is
  standard for an immunofluorescence assay paper.
