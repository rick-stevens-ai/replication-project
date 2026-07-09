# Friedland, Jacob, Kundrát (2010) — Abstract (verbatim)

**Citation:** Friedland W, Jacob P, Kundrát P. *Stochastic simulation of DNA double-strand break repair by non-homologous end joining based on track structure calculations.* Radiat. Res. 173(5):677–688 (2010). DOI: 10.1667/RR1965.1. PMID: 20426668.

**Open-access status (EuroPMC, queried 2026-06-21):** `isOpenAccess: N`, `inPMC: N`, `hasPDF: N`. Article is paywalled (bioone.org returns a 1151-byte challenge page for the canonical PDF URL).

**Abstract** (retrieved from EuroPMC + Helmholtz Munich PuSH frontdoor for source_opus=2206):

> A Monte Carlo simulation model for DNA repair via the non-homologous end-joining pathway has been developed. Initial DNA damage calculated by the Monte Carlo track structure code PARTRAC provides starting conditions concerning spatial distribution of double-strand breaks (DSBs) and characterization of lesion complexity. DNA termini undergo attachment and dissociation of repair enzymes described in stochastic first-order kinetics as well as step-by-step diffusive motion considering nuclear attachment sites. Pairs of DNA termini with attached DNA-PK enter synapsis under spatial proximity conditions. After synapsis, a single rate-limiting step is assumed for clean DNA ends, and step-by-step removal of nearby base lesions and strand breaks is considered for dirty DNA ends. Four simple model scenarios reflecting different hypotheses on the origin of the slow phase of DSB repair have been set up. Parameters for the presynaptic phase have been derived from experimental data for Ku70/Ku80 and DNA-PK association and dissociation kinetics. Time constants for the post-synaptic phase have been adapted to experimental DSB rejoining kinetics for human fibroblasts after (137)Cs gamma irradiation. In addition to DSB rejoining kinetics, the yields of residual DSBs, incorrectly rejoined DSBs, and chromosomal aberrations have been determined as a function of dose and compared with experimental data. Three of the model scenarios obviously overestimate residual DSBs after long-term repair after low-dose irradiation, whereas misrejoined DSBs and chromosomal aberrations are in surprisingly good agreement with measurements.

**Keywords (Helmholtz PuSH):** Heat-labile sites; Monte-Carlo; Human fibroblasts; Chromosome-Aberrations; Rejoining kinetics; Liquid water; DSB repair; Radiation; Model; Cell.

## Qualitative model architecture extractable from the abstract

1. **Input from PARTRAC** = spatial DSB distribution + lesion complexity tag per DSB (clean vs dirty).
2. **Presynaptic phase** = first-order stochastic attachment/dissociation of Ku and DNA-PK at each DNA terminus, plus discrete diffusive motion on a lattice of nuclear attachment sites.
3. **Synapsis** = two termini, both carrying DNA-PK, within spatial-proximity threshold → form a synapsis.
4. **Postsynaptic phase**
   - **Clean ends:** single rate-limiting ligation step.
   - **Dirty ends:** stepwise removal of nearby base lesions and strand breaks before ligation.
5. **Four model scenarios** for the slow phase (not enumerated in the abstract).
6. **Outputs:** DSB rejoining kinetics, residual DSBs, mis-rejoined DSBs, chromosomal aberrations vs dose.

## Headline qualitative claims (testable at the abstract level)

| ID | Claim |
|----|-------|
| C1 | Stochastic NHEJ on PARTRAC spatial input reproduces a biphasic (fast + slow) DSB rejoining curve. |
| C2 | Pre-synaptic parameters derived from Ku/DNA-PK assoc/dissoc data. |
| C3 | Post-synaptic time constants fitted to 137Cs γ DSB rejoining in human fibroblasts. |
| C4 | Three of four scenarios overestimate residual DSBs at long times after low-dose IR. |
| C5 | Mis-rejoined DSBs vs dose match measurements "surprisingly well". |
| C6 | Chromosomal aberrations vs dose match measurements "surprisingly well". |
| C7 | Dirty ends are the source of the slow rejoining component (via step-wise lesion removal). |

Numerical values for rate constants, the four scenarios' parametrisation, exact fast/slow time-constants, mis-rejoin fractions at specific doses, or aberration yields are **not present** in the abstract and could not be obtained without paywalled full text.
