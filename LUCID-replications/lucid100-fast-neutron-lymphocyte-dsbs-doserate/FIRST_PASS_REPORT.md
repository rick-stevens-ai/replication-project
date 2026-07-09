# FIRST PASS REPORT — LUCID100 slot 80 (Wave 5)

**Paper:** Nair et al. 2019, *Int. J. Mol. Sci.* 20(21): 5350, doi:10.3390/ijms20215350
**Replication folder:** `/Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-fast-neutron-lymphocyte-dsbs-doserate/`
**Subagent:** Wave 5 max-rate backfill, slot 49
**Run date:** 2026-06-09 (America/Chicago)

## Verdict: **PASS-low**

Three reduced table/curve smoke checks pass against the published Tables 1, 2, 3
and the abstract+Discussion claims, using only digitized table values + numpy.
No supplements, no deposited code, no external data needed; first pass complete
without author contact, paid endpoints, or heavy compute.

## What we replicated (3/3)

| ID | Quantity | Our value | Paper | Δ |
|----|----------|-----------|-------|---|
| C1 | Mean HDR/LDR foci ratio (Table 1 → Table 2) | 1.398 (+39.8 %) | "40 % higher at HDR" | < 0.5 pp |
| C1 | Per-dose ratios match Table 2 (5 doses) | max abs diff 0.005 | published Table 2 | tiny |
| C2 | Poly-2 induction fit R² (LDR) | 0.9944 | "best fitted to a second-order polynomial" | passes ≥0.95 threshold |
| C2 | Poly-2 induction fit R² (HDR) | 0.9879 | same | passes ≥0.95 threshold |
| C3 | HDR repair half-life | 9.92 h | 8.6 h | +1.32 h (+15 %) |
| C3 | LDR repair half-life | 13.08 h | 12.0 h | +1.08 h (+9 %) |

Detailed JSON: `scripts/smoke_outputs/smoke_results.json`.
Overlay plot: `scripts/smoke_outputs/smoke_plots.png`.

## What we did NOT replicate (out of scope for first pass)

- ANOVA p-values (require per-cell foci counts, not in any deposit)
- Per-donor variability (only mean ± SD across 4 donors published)
- Automated foci scoring (Metafer / MetaCyte) — no raw images released
- Neutron-physics dosimetry / spectrum at iThemba LABS p(66)/Be(40) facility
- Any mechanistic Monte Carlo model of DSB induction vs dose rate — paper does
  not present one; it presents two empirical fits

## Artifact harvest summary

| Artifact | Status | Source |
|----------|--------|--------|
| Full OA PDF | ✅ 1.2 MB, 13 pp | Europe PMC `articles/PMC6862539?pdf=render` |
| JATS full-text XML | ✅ 119 KB | EPMC `/PMC6862539/fullTextXML` |
| Tables 1–3 as CSV | ✅ digitized from `pdftotext -layout` | local extraction |
| Supplementary material | ❌ none | EPMC `hasSuppl: N`; confirmed in PDF end matter |
| Code / scripts | ❌ none | authors used Excel 2013 + GraphPad Prism v5 |
| Raw foci counts | ❌ none | not deposited; not in PDF |
| Direct MDPI PDF | ❌ HTTP 403 (anti-bot) | OA route via EPMC was sufficient |

## Feasibility ladder

- **PASS-low (this report):** reduced table-curve replication from digitized tables — DONE
- **PASS-medium:** WebPlotDigitizer overlay of Figs 1, 3, 4 to validate digitized
  table values from a second extraction path; CherryRd-feasible, <1 hr
- **PASS-high:** mechanistic MCDS / PARTRAC simulation of p(66)/Be(40) DSB
  induction vs dose rate, predicting HDR/LDR ratios from first principles; would
  use uicgpu or Aurora batch (CPU is enough), and corresponds to the original
  "simulation/model replication" worktype label on the master TSV. **Not done in
  this pass; treated as out of scope.**

## Worktype QA retag (recommendation)

**LUCID100_SOLID_MASTER_QA.tsv row 80 (Wave 5, DOI 10.3390/ijms20215350):**

- Declared `worktype = "simulation/model replication"`
- Recommended `worktype = "wet-lab assay / radiobiology table replication"`

**Justification:** The published paper is a γ-H2AX immunofluorescence assay on
human peripheral-blood lymphocytes irradiated with p(66)/Be(40) fast neutrons at
the iThemba LABS cyclotron facility (South Africa). The only "modeling" content
is two phenomenological curve fits applied to the experimental means
(2nd-order polynomial for induction, single-exponential decay for repair). No
Monte Carlo simulation, no ODE / kinetic model, no agent-based or stochastic
model is described or released. The replication that is *actually* possible
from the published artifact is a table/curve smoke check (this report).

If the master TSV intends to retain a "simulation/model" track for this DOI,
that would need to be a *new* MCDS/PARTRAC build (PASS-high tier above), not
a replication of anything in this paper.

## Blockers / risks

- None that prevented first pass.
- A PASS-medium upgrade is bottlenecked on either (a) digitizer overlay of
  rasterized figures, or (b) author contact for per-cell CSVs (currently
  disallowed by task policy).

## Compute footprint

- All work was Python+numpy on CherryRd, total runtime <1 s. No GPU, no HPC, no
  external API writes. Network use: 1.3 MB PDF + 120 KB XML + 1 KB metadata JSON
  from `europepmc.org` and one blocked attempt to `mdpi.com`.
- **No heavy compute requested. No HPC job plan needed.**

## Next actions for downstream curators

1. Apply the worktype retag in the master TSV (or open a row to that effect).
2. Mark LUCID100 status `pass_low` (mirrors slot 14 nomenclature) with this
   folder as the artifact pointer.
3. If/when policy permits author contact, request per-cell foci CSVs from
   Charlot Vandevoorde (was iThemba LABS; now HZDR) — would unlock proper
   ANOVA replication and tighten the C3 half-life agreement.
4. Optional: schedule a separate PARTRAC/MCDS build job (Aurora or uicgpu) if
   the "simulation/model replication" label is to be honored as a new
   workstream rather than retagged.
