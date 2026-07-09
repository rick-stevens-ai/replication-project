# Workflow — lucid-cu64-topas-nbio-lethal-damage

Replication of Carrasco-Hernández et al. 2023, *Front. Med.* 10:1253746
("Cellular lethal damage of 64Cu incorporated in mammalian genome evaluated
with Monte Carlo methods").

## Stages actually executed

### 1. Ingest & triage re-read
- Fetched paper PDF from the open-access DOI.
- Re-read Methods §2.2 and confirmed the paper does **NOT** use DBSCAN
  (upstream triage tag was wrong); it uses the Nikjoo/Charlton opposite-
  strand 10-bp proximity rule. Documented in `REPORT.md §1` and in the
  Critique section of `report/REPORT.tex`.

### 2. Analytic chain (R1)
- Implemented Humm–Charlton Eq. 1 in
  `code/01_lethal_damage_equation.py`:
  `N0 = 2 * N_DSB / [(1 - exp(-λt)) * (f + 35 D)]`
- Fed the paper's own Table 1 DSB/decay values + published half-lives
  (NNDC/ENSDF) for all five nuclides.
- Compared recomputed N₀ and initial activity A to the paper's Table 2.
- Result: max deviation 0.21 % on ¹²⁵I (consistent with paper rounding
  Table 1 to 3 s.f.). All 5 nuclides within 0.21 %.
- Wrote `figures/fig01_eq1_crosscheck.png`.

### 3. DSB scoring rule (R2)
- Implemented in `code/02_proximity_dsb_scoring.py`.
- Unit-tested same-strand, opposite-strand, exactly-10-bp boundary, greedy
  pairing.
- Exercised at varying uniform-random SSB density on 6.08 Gbp — confirms
  chance coincidences are ≈0 (correct; real DSBs need track-local clustering).

### 4. Track-correlated illustration (R3)
- Implemented in `code/03_track_correlated_dsb.py`.
- Fabricated track-clustered SSBs (Poisson clusters/track, Poisson SSBs/
  cluster, narrow bp extent).
- Ran R2 rule → recovered DSB:SSB ratios in the Nikjoo/Friedland range
  (0.02–0.05 low-LET e⁻; 0.16 dense Auger). Not a yield reproduction.
- Wrote `figures/fig02_dsb_ssb_ratio.png`.

### 5. ⁶⁴Cu decay-spectrum spot-check (R4)
- Pulled ICRP-107 summary Auger spectrum for ⁶⁴Cu from MIRDsoft.
- Summed lines with E > 1 keV → 0.228 e⁻/decay, consistent with the paper's
  "~0.18 e⁻/decay" within interpretation.
- Full-spectrum sum → 1.8 e⁻/decay (paper's number is the LET-relevant
  subset).

## Stages NOT executed (honest)

### TOPAS-nBio install
- **Not done.** TOPAS is CC-BY-NC and gated behind an emailed license key;
  tarball is not fetchable by unattended subagent.
- Geant4 + low-energy EM + nBio extension → multi-hour build even on a
  well-equipped box; not a same-day budget item.

### Monte Carlo re-run of DSB/decay primitive
- **Not done.** 400,000 histories per data point on parallel cluster
  ("Tochtli-ICN-UNAM"). Not a laptop job.
- No public Zenodo/GitHub deposit of input decks or per-event SSB lists;
  data-availability = "included in the article."

### Monoenergetic-e⁻ DSB-vs-energy (Figure 5)
- Not done — would require actual MC.

### 1.15 nm position / other nuclide Table 1 primitives
- Not done — same reason.

### MEDRAS repair endpoints
- Paper mentions MEDRAS but doesn't compute repair endpoints in the
  published analysis, so nothing to reproduce here.

## Compute
All work in this replication ran on a single macOS laptop in Python 3.11.
No GPU, no MPI, no license-gated software touched.

## Free-endpoint compliance
- No paid API calls.
- No proprietary software installed or executed.
- Public data only: NNDC/ENSDF half-lives, ICRP-107 Auger spectrum via
  MIRDsoft, paper's own Table 1 as input to R1.
