# LUCID100 / Wave 4 / Slot 39

## Paper

- **Title:** Contribution of Nuclear Fragmentation to Dose and RBE in Carbon-Ion Radiotherapy
- **Authors:** Hartzell S, Guan F, Magro G, Taylor P, Taddei PJ, Peterson CB, Kry S
- **DOI:** [10.1667/rade-24-00164.1](https://doi.org/10.1667/rade-24-00164.1)
- **PMID:** 39862066
- **Venue:** *Radiation Research* 203(2):96–106 (Feb 2025)
- **Master TSV rank:** 70 · Backfill slot: 39 (Wave 4)
- **Worktype:** simulation/model replication

## Replication scope

The paper compares **four RBE models** — MKM (Kase et al.), Stochastic MKM (Sato & Furusawa),
RMF (Carlson et al.), and LEM‑I (Scholz/Elsässer) — across the carbon beam fragment spectrum
(H, He, Li, Be, B, secondary C, primary C, electrons, "other") in a water phantom under
monoenergetic and SOBP carbon beams scored with Monte Carlo. Their headline numerical
findings are:

1. Secondary fragments contribute **> 30 %** of total physical dose in a SOBP plan.
2. The four RBE models predict different absolute RBE *and* different fragment-by-fragment
   *trends*; secondary C always has the highest fragment RBE.
3. RBE magnitude tends to rise with fragment Z beyond secondary C, but rankings differ
   strongly by model and by beamline region (entrance, SOBP, tail).

## Accessibility (objective evidence in `artifacts/metadata/`)

| Resource | Status |
|---|---|
| Publisher PDF (Allen Press / BioOne) | Subscription required; Cloudflare blocks scripted access |
| Unpaywall / Europe PMC / PMC | **No OA copy**, no preprint, no repo copy (`is_oa=false`) |
| Author code repository | **Not found** (GitHub search returned 0 hits for plausible queries) |
| Author data deposit (Zenodo) | **Not found** (no Hartzell carbon-RBE deposit) |
| Companion 2026 paper (`10.1002/pro6.70059`, *Precision Radiation Oncology*) | Gold OA (CC‑BY‑NC‑ND) but PDF behind Cloudflare; appears to be the measurement-based follow-up using the same four-model framework |

**Verdict on direct replication:** the paper itself is closed access and ships *no* public
code/data/supplements. A bit-for-bit numerical replication of the published RBE tables and
figures requires the article body (model parameters, beamline geometry, fragment fluence
spectra), which we have not been able to obtain through any free public channel.

## What this replication does instead

A **first-pass, fragment-aware, smoke replication** that:

1. Re-implements the canonical published equations of MKM, SMKM, RMF and LEM‑I from
   the open primary literature cited by the paper.
2. Uses a *published* representative carbon-SOBP fragment energy / dose-fraction table
   (Tessonnier 2017 / Inaniwa 2010 style) baked into `data/fragment_spectrum_reference.csv`,
   not Monte Carlo we re-ran ourselves.
3. Computes per-fragment α, β, and resulting RBE for each model, plus the total
   dose-averaged RBE.
4. Reproduces the **three qualitative claims** above and quantifies the inter-model spread
   for a fixed fragment spectrum.

This is a *minimum-viable* smoke check that confirms the paper's mechanism (model-handling
of fragments drives most of the inter-model RBE spread) using only published, open
equations and a published reference fragment composition. It is explicitly **not** a
re-run of the Monte Carlo simulation.

For a full numerical replication we would need:
- TOPAS or Geant4-DNA setup for a 290 MeV/u carbon SOBP in water phantom (heavy MC).
- The exact reference-radiation α/β values used in the paper.
- Microdosimetric spectra (z*, y) scored from the MC for each fragment.

These are documented as a *job plan* in `reports/JOB_PLAN_heavy_MC.md` (heavy compute,
explicitly **not** run here on CherryRd).

## Layout

```
lucid100-nuclear-fragmentation-carbon-rbe/
├── README.md                       — this file
├── PROGRESS.md                     — step-by-step log
├── ARTIFACT_MANIFEST.md            — list of every artifact + sha256 + provenance
├── artifacts/
│   └── metadata/                   — OpenAlex / S2 / Unpaywall / EuropePMC JSON dumps
├── data/
│   └── fragment_spectrum_reference.csv   — open published reference dose-fractions
├── code/
│   ├── rbe_models.py               — MKM, SMKM, RMF, LEM-I as Python functions
│   └── smoke_replication.py        — driver: per-fragment RBE + total
├── figures/
│   ├── per_fragment_rbe.png
│   └── total_rbe_vs_model.png
└── reports/
    ├── FIRST_PASS_REPORT.md        — full verdict
    └── JOB_PLAN_heavy_MC.md        — what a real MC replication would need
```

## Reproduction

```bash
cd lucid100-nuclear-fragmentation-carbon-rbe
python3 code/smoke_replication.py        # writes figures/* and reports/smoke_results.json
```

No internet, no GPU, < 1 s wall clock, pure numpy + matplotlib.

## Constraints honoured

- No paid endpoints
- No author contact
- No heavy compute on CherryRd
- All external content retrievals logged with timestamps in `artifacts/metadata/`
