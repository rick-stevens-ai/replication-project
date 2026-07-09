# LUCID100 slot 67 — Friedland, Kundrát & Jacob (2012)
## *Stochastic modelling of DSB repair after photon and ion irradiation*

| Field | Value |
| --- | --- |
| DOI | `10.3109/09553002.2011.611404` |
| PMID | `21823824` |
| Journal | International Journal of Radiation Biology, 88(1–2):129–136 (2012) |
| Authors | Werner Friedland, Pavel Kundrát, Peter Jacob (Helmholtz Zentrum München) |
| OA status | **Closed** (Unpaywall / OpenAlex: no OA copy, no repository preprint) |
| Citations (OpenAlex / S2) | 38 / 42 |
| Source PDF | not redistributable; only abstract + bibliographic metadata in `source/` |
| LUCID100 master rank | 98 (Wave 7, Tier B) — task header "slot 67" is the wave-7 backfill slot index |

### What the paper does

Refines the stochastic NHEJ DSB-repair model implemented in the proprietary
**PARTRAC** Monte Carlo track-structure code (Helmholtz Zentrum München) so
that the *same* parameter set reproduces measured rejoining kinetics after
both low-LET ⁶⁰Co γ and high-LET ¹⁴N-ion irradiation.  Two refinements drive
the result:

1. **Ongoing detectable-DSB production** in the initial phase — enzymatic
   processing of labile / heat-labile sites converts SSB pairs into observable
   DSB minutes after exposure.  This explains why the early rejoining curve is
   slower than naive monoexponentials predict.
2. **Limited repair-enzyme availability** for complex lesions during the slow
   phase — saturating the slow channel, especially for high-LET tracks where
   the complex-DSB fraction is high.

It is a methodological refinement of:
- Friedland, Jacob & Kundrát (2010) *Stochastic Simulation of DSB Repair by
  Non-Homologous End Joining* — RR1965; **already harvested in
  `../lucid-friedland-stochastic-nhej-track-slot64/`**.
- Friedland et al. (2011) — *Track structures, DNA targets and radiation effects
  in the biophysical Monte Carlo simulation code PARTRAC*, Mutat. Res.

### Code / data availability — what we found

| Asset | Available? | Notes |
| --- | --- | --- |
| Full paper PDF | ❌ closed-access (Taylor & Francis), no preprint, no repository | Abstract pulled from PubMed + S2 + OpenAlex |
| PARTRAC source code | ❌ proprietary | Helmholtz Zentrum München; no public release on GitHub or elsewhere (search 2026-06-09) |
| NHEJ model parameters | ❌ tabulated only in the closed PDF | RR1965 (2010) gives the precursor parameter set in tabular form (also closed) |
| Experimental rejoining kinetics input data | ⚠️ partly | The paper relies on N-ion vs ⁶⁰Co γ rejoining datasets (Stenerlöw 2000 and references); these are also closed-access journal papers |
| Companion analytical fits (Kundrát 2021) | ✅ open access — `slot64/source/kundrat2021_coupling.pdf` | DNA damage yields as analytical functions of LET / particle energy |

⇒ **Full quantitative re-implementation is infeasible without (a) the paper
text, (b) the PARTRAC source, and (c) the precise digitised kinetics tables.**
A *qualitative analytical smoke replication* is feasible and is included here.

### Smoke replication included

`code/smoke_friedland2012.py` implements a reduced **analytical** two-component
NHEJ rejoining model that captures the paper's three qualitative refinements
(fast/slow channels + labile-site delayed detection + larger slow fraction at
high LET) and fits literature-typical kinetics curves for ⁶⁰Co γ and a high-LET
nitrogen ion reference.

Outcome: **6/6 smoke checks pass** (see `results/smoke_fit_results.json` and
`figures/smoke_rejoining.png`).  This is a *behavioural* validation — it
confirms the analytical scaffold reproduces the qualitative photon-vs-ion
contrast the paper is built around, **not** a quantitative reproduction of any
specific figure in Friedland 2012.

### Folder layout

```
lucid100-friedland-stochastic-dsb-photon-ion-slot67/
├── README.md                ← this file
├── PROGRESS.md              ← timestamped progress log
├── MANIFEST.md              ← artefact manifest
├── FIRST_PASS_REPORT.md     ← first-pass report w/ AMBER verdict
├── code/
│   └── smoke_friedland2012.py
├── source/
│   ├── openalex_metadata.json
│   ├── unpaywall_metadata.json
│   ├── s2_metadata.json
│   └── references_table.md  ← annotated reference list (this paper has 14 refs)
├── results/
│   └── smoke_fit_results.json
├── figures/
│   └── smoke_rejoining.png
└── logs/
    └── (empty – no heavy runs)
```

### Verdict

**AMBER-KEEP** — relevant LUCID work, partially replicated qualitatively.  See
`FIRST_PASS_REPORT.md`.  Recommend QA retag from `candidate_curated` →
`first_pass_complete_amber_keep`.

### Next actions if a full replication were attempted

1. Obtain the paper PDF + RR1965 (2010) PDF via institutional access (Argonne
   library), digitise Tables 1–2 of model parameters.
2. Obtain Stenerlöw 2000 ⁶⁰Co vs N-ion rejoining kinetics (closed access) for
   actual reference fits.
3. Replace the analytical smoke model with a (small) Gillespie-style stochastic
   NHEJ simulation seeded by PARTRAC-published DSB-complexity distributions
   captured in the open-access Kundrát 2021 Frontiers paper.
4. Compute residuals at characteristic time points (15 min, 2 h, 24 h) and
   compare against Fig. 1–3 reproductions.

Steps (3) and (4) are feasible without HPC (laptop-scale).  Step (1)–(2)
require library access — not author contact, not a paid endpoint.

### Compute footprint

- Smoke ran on CherryRd in <1 s.  No heavy compute; no HPC job plan needed.
- Disk: <1 MB.
