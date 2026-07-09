# Model notes — Liew et al. 2021 IJROBP (DOI 10.1016/j.ijrobp.2021.09.048)

## Identification of the model

The target paper masks its model name as "XXX (MODELX)" in the abstract (a journal artefact of double-blind review that survived into production). The companion conference abstract by the same authors (Liew et al., **IJROBP 111(3) Suppl., e526–e527, 2021**, DOI 10.1016/j.ijrobp.2021.07.829) and the follow-on IJMS paper (Liew et al., IJMS 23:6268, 2022, DOI 10.3390/ijms23116268) both explicitly call this model:

> **UNIVERSE — "UNIfied and VErsatile bio-response Engine"**

developed at DKFZ / Heidelberg Ion-Beam Therapy Center (HIT) by Liew, Mein, Mairani et al.

UNIVERSE is built on top of the **GLOBLE (Giant LOop Binary LEsion) framework** of Friedrich, Durante & Scholz (Radiat Res 178:385–394, 2012, DOI 10.1667/RR2964.1), with the DDR-interference extension first introduced for photons in Liew et al. 2019 IJMS (DOI 10.3390/ijms20236054), and the ion-beam extension first described in Mein et al. 2019 Radiat Oncol (DOI 10.1186/s13014-019-1295-z).

The 2021 IJROBP paper that this slot targets is therefore the **combination of the photon DDR-interference extension (Liew 2019) with the ion-beam track-structure extension (Mein 2019)**.

## Core mechanistic structure

### 1. Geometry
- Cell nucleus = cylinder of DNA content `DNA_c = 6 Gbp`.
- Nucleus is partitioned into `N_gl = DNA_c / DNA_gl ≈ 3000` chromatin "giant loops" of `DNA_gl = 2 Mbp` each (Yokota 1995; Sachs 1995).

### 2. DSB induction — sparsely ionising radiation (photons / electrons)
- DSB induction yield per Gy per Mbp: `α_DSB = 5 × 10⁻³ DSB / (Mbp · Gy)`  (≡ `α_DSB ≈ 30 DSB / (cell · Gy)` for a 6-Gbp nucleus). Constant across the clinical dose range (1–10 Gy).
- Expected total DSB:    `⟨N_tDSB⟩ = α_DSB · D · DNA_c`  …(1)
- Actual `N_tDSB` is sampled per Monte Carlo iteration from `Poisson(⟨N_tDSB⟩)`.
- The `N_tDSB` breaks are distributed uniformly across the `N_gl` loops.
- A loop with **exactly one** DSB is an **isolated DSB (iDSB)**; a loop with **two or more** is a **complex/clustered DSB (cDSB)**.

### 3. Cell survival
Given counts `N_iDSB` and `N_cDSB` per iteration, the survival probability is

    S = (1 − K_iDSB)^N_iDSB · (1 − K_cDSB)^N_cDSB     …(3) [Liew 2019], …(5) [Liew 2022]

with cell-line-dependent lethality parameters `K_iDSB` and `K_cDSB`. Mean over Monte Carlo iterations gives the surviving fraction (SF) at dose `D`.

Typical fitted values (Liew 2019 Table 1, 5 normoxic cell lines):
- A549:   K_iDSB = 4.8e-3, K_cDSB = 0.17
- H460:   K_iDSB = 3.3e-3, K_cDSB = 0.24
- H1437:  K_iDSB = 3.8e-3, K_cDSB = 0.14
- B16:    K_iDSB = 4.0e-3, K_cDSB = 0.13
- Renca:  K_iDSB = 1.7e-3, K_cDSB = 0.20

K_cDSB is typically 1–2 orders of magnitude larger than K_iDSB.

### 4. Hypoxia — Hypoxia Reduction Factor for DSB
- Only `α_DSB` is modified:   `α_DSB^O2 = α_DSB / HRF_DSB^O2`   …(4)
- Lethality parameters and repair rates remain invariant under change of [O₂].
- The parameterisation `HRF_DSB^O2 = (m·K + [O₂]) / (K + [O₂])` with `m = 2.94, K = 0.129%` fits the literature.

### 5. DDR interference (the radiosensitisation extension)
- Empirical finding (Hufnagl 2015; Liew 2019): **only `K_iDSB` is modified by DDR interference**, while `K_cDSB` stays fixed (complex DSBs are already "overwhelming" for any repair pathway).
- A single radiosensitisation factor RSF ≥ 1 is introduced:

      S_−Repair = (1 − RSF · K_iDSB)^N_iDSB · (1 − K_cDSB)^N_cDSB     …(7)

- RSF is fit per (cell line × DDRi-condition). Examples from Liew 2019 Table 3:
  - H460, ATMi 100 nM → RSF ≈ 1.73; 200 nM → 2.56; 500 nM → 4.21.
  - H1437, ATMi 100 nM → 1.77; 200 nM → 2.52; 500 nM → 3.77.
  - CHO V3 (DNA-PKcs−/−) → RSF ≈ 10; xrs-5 (Ku80−/−) → RSF ≈ 15.
- RSF is **invariant under change of oxygenation** (decoupled from HRF).

### 6. Ion-beam extension (Mein 2019; Liew 2022 §Methods)
For ion irradiation (protons, ⁴He), dose deposition is not homogeneous, so a track-structure step is added:

- Each ion track has a **radial dose distribution (RDD)** parametrised by Kiefer–Chatterjee:
  - Core: `D_c = (1 / (π r_min²)) · (LET/ρ − 2π K_p ln(r_max/r_min))`     …(6)
  - Penumbra: `D_p(r) = K_p · r^−2`     …(7)
  - `K_p = 1.25e-4 · (z*/β_ion)²`     …(8)
  - `z* = z_ion · (1 − exp(−125 β_ion z_ion^(−2/3)))`  (Barkas effective charge)     …(9)
  - `r_min = β_ion · r_c` with `r_c = 11.6 nm`
  - `r_max = e · E_kin^δ` with `e = 0.062, δ = 1.7`, E_kin in MeV/u
- RDD is diffusion-broadened (radical-diffusion convolution with a Gaussian of width σ).
- Tracks are sampled per Monte Carlo iteration; each track's dose is deposited into the cylindrical-domain nuclear geometry.
- A loop's DSB count is then sampled `Poisson(⟨dose-in-loop⟩ · α_DSB · DNA_gl)` plus an analytic correction for *intra-track DSB clustering* from very high local doses (Friedrich 2015 formula), which causes the **effective α_DSB to rise with LET**.
- Once the (N_iDSB, N_cDSB) of each iteration are obtained, **the same K_iDSB and K_cDSB are used as for photons** — i.e. survival under photon and ion irradiation is determined by the same lethality parameters, just by a different DSB-distribution mechanism.
- DDR interference: same RSF acts on `K_iDSB` for ion irradiation.

### 7. The 2021 IJROBP paper's specific contributions
Read from the (full) abstract (Semantic Scholar + Unpaywall) and the conference-abstract sibling:

- First **comprehensive in-vitro benchmark** of UNIVERSE+DDRi for protons and ⁴He ions over a clinically relevant LET range (≈2 to ≈100 keV/µm).
- New **own experimental data**: cell-survival measurements of DDR-competent and DDR-deficient cell lines in a He spread-out Bragg peak (SOBP) at HIT — "the first comprehensive measurement of cell survival of repair-competent and -deficient cell lines in a helium spread-out Bragg peak."
- Demonstrates that **only 3 parameters from photon data** (presumably K_iDSB, K_cDSB, and RSF) are needed to predict cell-survival for DDR-competent + DDR-deficient lines under proton / He irradiation.
- Headline mechanistic result: **the radiosensitising effect of DDRi decreases with increasing LET (and increasing dose)**, leading to **diminished RBE of ion-beam radiation for DDRi cells** vs. non-DDRi cells. Mechanism: at higher LET the cDSB fraction rises, and since K_cDSB is unaffected by DDRi, the relative gain from RSF on K_iDSB shrinks.
- **Patient-plan recalculation**: combined DDRi+particle therapy may better preserve the therapeutic window than DDRi+photon therapy. The clinical-translation suggestion is that DDR-deficient tumours might preferentially benefit from light-ion therapy, freeing limited heavy-ion capacities.

## Public code / data availability

- **No public source code** for UNIVERSE has been released by the Heidelberg group (verified via Semantic Scholar `openAccessPdf`, GitHub search for `UNIVERSE Mairani Liew`, and Unpaywall — no software-paper or repository link in any of the 4 OA UNIVERSE companion papers).
- **Experimental SOBP cell-survival data** in the target paper appear in journal figures only; no supplementary data table is OA.
- The target paper itself is **closed access** (Elsevier/IJROBP), Unpaywall status = `closed`, no repository copy, no PMC. Only the abstract is publicly accessible.
- The model is mathematically fully specified in the OA companion papers (Liew 2019 §4.4 for photons + DDRi; Mein 2019 §2 and Liew 2022 §4 for ions; Friedrich 2012 RR2964 for the underlying GLOBLE photon framework).

## Replicability assessment

**Feasibility of a reduced analytical/MC replication on CherryRd:** YES for the photon + DDRi half. **PARTIAL/NO** for the ion-beam half without considerable engineering.

| Component | Replicable? | Notes |
| --- | --- | --- |
| Photon GLOBLE/UNIVERSE cell-survival MC | **YES (full)** | ~50 lines of NumPy. Self-checks against the Liew 2019 Table 1 fits. |
| Photon + DDRi (RSF on K_iDSB) | **YES (full)** | Direct application of Liew 2019 Eq. (7). |
| Hypoxia (HRF_DSB) | YES (trivial) | Multiplies α_DSB. |
| Ion-beam track-structure (Kiefer–Chatterjee RDD + per-loop dose deposition) | **PARTIAL** | RDD math is fully open; deposition into 2-Mbp cylindrical domains needs ~200–500 lines + careful integration. Friedrich 2015 intra-track DSB clustering analytical formula is in a paywalled paper. |
| LET-dependent DSB-yield correction | **PARTIAL** | Requires Friedrich 2015 formula (closed). A bounded surrogate can be built from published LET vs. α plots. |
| 3D patient-plan recalculation | **NO** | Requires the HIT FLUKA-coupled treatment-planning system, helium beam data, MC dose engine, anonymised CT/RT-Plan. None public. |

**Smoke chosen:** Implement the photon + DDRi pillar exactly per Liew 2019 Eq. (1)–(7), and add a *minimal, justified surrogate* for the ion-beam LET dependence that captures the **qualitative headline finding** of the target paper — namely, that the RBE_DDRi/RBE_no-DDRi ratio decreases as LET (and therefore the cDSB fraction) increases. This is the key mechanistic claim of the 2021 IJROBP paper and can be made falsifiable by published LET-vs-RBE curves from Mein 2019 and Liew 2022.
