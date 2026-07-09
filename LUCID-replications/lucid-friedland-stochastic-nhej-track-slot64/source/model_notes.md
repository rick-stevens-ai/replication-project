# RR1965 NHEJ model — curated notes (from closed paper abstract + OA companions)

## Source paper
Friedland W, Jacob P, Kundrát P (2010) *Stochastic Simulation of DNA Double-Strand Break Repair by Non-homologous End Joining Based on Track Structure Calculations.* Radiat Res 173:677–688. DOI 10.1667/RR1965.1. PMID 20426668. **Closed access.**

## Model architecture (verbatim summary, from the PubMed-indexed abstract)

> A Monte Carlo simulation model for DNA repair via the non-homologous end-joining pathway has been developed. Initial DNA damage calculated by the Monte Carlo track structure code PARTRAC provides starting conditions concerning spatial distribution of double-strand breaks (DSBs) and characterization of lesion complexity. DNA termini undergo attachment and dissociation of repair enzymes described in stochastic first-order kinetics as well as step-by-step diffusive motion considering nuclear attachment sites. Pairs of DNA termini with attached DNA-PK enter synapsis under spatial proximity conditions. After synapsis, a single rate-limiting step is assumed for clean DNA ends, and step-by-step removal of nearby base lesions and strand breaks is considered for dirty DNA ends. Four simple model scenarios reflecting different hypotheses on the origin of the slow phase of DSB repair have been set up. Parameters for the presynaptic phase have been derived from experimental data for Ku70/Ku80 and DNA-PK association and dissociation kinetics. Time constants for the post-synaptic phase have been adapted to experimental DSB rejoining kinetics for human fibroblasts after (137)Cs gamma irradiation. In addition to DSB rejoining kinetics, the yields of residual DSBs, incorrectly rejoined DSBs, and chromosomal aberrations have been determined as a function of dose and compared with experimental data. Three of the model scenarios obviously overestimate residual DSBs after long-term repair after low-dose irradiation, whereas misrejoined DSBs and chromosomal aberrations are in surprisingly good agreement with measurements.

## Decomposition (reconstructed from abstract)

**Per-end state machine (first-order stochastic):**
1. **Naked DSB end** — empty
2. **Ku70/80 attached** — first NHEJ protein recruited
3. **Ku + DNA-PKcs attached** ("DNA-PK complex") — competent for synapsis
4. **Synapsed pair** — two DNA-PK-loaded ends in spatial proximity
5. **Post-synaptic processing:**
   - *Clean end:* single rate-limiting step → ligated
   - *Dirty end:* iterative removal of nearby base lesions / SSBs (multi-step) → then ligated
6. **Diffusive motion** — step-by-step random walk between nuclear attachment sites; relevant for finding a synapsis partner and for misrepair (joining of wrong ends).

**Synapsis criterion:** "spatial proximity." The closely related Henthorn 2018 in-silico NHEJ model (Sci Rep 8:2654, OA) uses **25 nm** between DNA-PK-loaded ends as the cutoff; this is consistent with the Friedland group conception and we adopt 25 nm as a placeholder.

## Rate-constant regime (from OA companions; *not* the verbatim RR1965 numbers)

**Li, Reynolds, O'Neill 2014 PLoS ONE** (DOI 10.1371/journal.pone.0085816) — citing RR1965 — fits a sibling NHEJ scheme with units **min⁻¹**:

| Parameter | Value (min⁻¹) | Meaning |
| --- | --- | --- |
| `ka1` | 4.5 | Ku and XL (XRCC4/Ligase IV) on-rate to free DSB end |
| `kd1` | 2.52 | Ku off-rate (fast equilibrium) |
| `kd2` | (≈2.5) | XL off-rate |
| `kLK` | 0.331 | Long-range synapsis formation rate, simple (clean) DSB |
| `kLD` | 0.263 | Long-range synapsis formation rate, complex (dirty) DSB |
| `kEP` | 4.23 | End-processing rate by DNA-PKcs/Artemis on complex ends |
| `kpD` | 2.76 | Release of DNA-PKcs after phosphorylation (no ATM inhibition) |
| `k̃pD` | 0.0056 | Release of DNA-PKcs under ATM inhibition (~500× slower) |

These give DSB rejoining half-times of **~10–30 min for simple breaks** and **hours for complex breaks**, which is the same fast/slow phenomenology that RR1965 fits to its ¹³⁷Cs fibroblast benchmark.

**Henthorn et al. 2018 Sci Rep** (DOI 10.1038/s41598-018-21111-8) — citing RR1965 — uses a model with the same topology, **25 nm synapsis radius**, motion of ends limited to <168 nm in 24 h, and reports **~7.3% residual DSBs at 24 h** independent of ion species/dose/LET in the studied range. RR1965's abstract reports that *three of four scenarios overestimate* residual DSBs at long times under low dose, so the "right" scenario in RR1965 sits at a similar few-percent residual level.

## What we can and cannot reproduce

| Result type | Reproducible without paper? | Reason |
| --- | --- | --- |
| Model architecture (state machine, synapsis criterion, scenarios concept) | **Yes (qualitative)** | From abstract + companions |
| Biphasic fast/slow DSB rejoining kinetics | **Yes (qualitative)** | From general NHEJ phenomenology |
| Few-percent residual DSBs at 24 h | **Yes (qualitative)** | From abstract; Henthorn 2018 cross-check |
| **Exact Tables of Ku/DNA-PK rate constants** | **No** | Behind paywall; not in any OA companion |
| **Exact four-scenario residual-DSB and misrejoin curves** | **No** | Same |
| **PARTRAC track-structure DSB inputs** | **No** | PARTRAC is not public |
| **Comparison to ¹³⁷Cs fibroblast PFGE/γ-H2AX data** | **No (quantitative)** | Need the in-paper digitized benchmark and the scenario parameters |
| **Chromosomal aberration yields** | **No** | Requires a chromatin-geometry + spatial-track model on top of NHEJ |

## Friction tags

- `closed-access-paper` (no OA, no repo copy)
- `partrac-not-public` (cannot regenerate the damage input)
- `parameters-elided` (Ku, DNA-PK, clean/dirty rate constants not in any OA secondary source we found)
- `four-scenarios-not-distinguishable` (the abstract identifies four scenarios but does not name them; we cannot replicate the four-way comparison)
- `companion-rate-constants-only` (numbers used by the smoke are Li 2014's, not RR1965's; same regime, different fits)
- `simplification: spatial-geometry` (smoke uses a 1D effective-distance abstraction instead of PARTRAC 3D nuclear geometry)
- `simplification: dirty-end-cleaning-collapsed` (smoke uses a single Erlang-distributed multi-step cleaning, rather than per-lesion step-by-step removal)
