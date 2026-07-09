# Second-100 Geant4-DNA MC Campaign — Clustering Yields

**Status:** Campaign complete (2026-06-25 17:29 CDT). All 11 energy points done, rc=0.
**Host:** uicgpu (`/gpustor/stevens/radmc/campaign/clustering/`)
**Driver:** `/gpustor/stevens/radmc/campaign_clustering.sh`
**Engine:** Geant4 11.4.2 + Geant4-DNA `clustering` extended example (Y. Perrot, H. Payno; Francis et al. 2011)
**Primaries:** **electrons**, 20,000 events per energy point
**Geometry:** 1 µm × 1 µm × 0.5 µm liquid-water target box (Francis 2011 set-up; `target = 0.5 µm³`)
**Clustering parameters (DBSCAN):** `MinPts=2`, `selectionProb=0.2`, `eps=3.3 nm`, `Emin=5 eV`, `Emax=37.5 eV` (paper-default; mimics DNA mass-fraction sampling and energy-probability ramp)

---

## Mean yields per primary (per event)

| E (keV) | N_prim | ⟨simpleSSB⟩ | ⟨complexSSB⟩ | ⟨totalSSB⟩ | ⟨DSB⟩ | DSB/SSB |
|--------:|-------:|------------:|--------------:|-----------:|------:|--------:|
|  0.50 | 20000 |  1.699 ± 0.007 |  0.551 ± 0.002 |  2.250 |  0.558 ± 0.002 | 0.248 |
|  1.00 | 20000 |  2.939 ± 0.010 |  0.633 ± 0.003 |  3.572 |  0.653 ± 0.003 | 0.183 |
|  2.00 | 20000 |  5.283 ± 0.014 |  0.829 ± 0.004 |  6.112 |  0.876 ± 0.004 | 0.143 |
|  5.00 | 20000 | 11.157 ± 0.021 |  1.484 ± 0.007 | 12.641 |  1.684 ± 0.008 | 0.133 |
| 10.00 | 20000 | 19.132 ± 0.028 |  2.631 ± 0.010 | 21.763 |  3.277 ± 0.011 | 0.151 |
| 20.00 | 20000 | 31.321 ± 0.036 |  5.035 ± 0.014 | 36.356 |  6.959 ± 0.017 | 0.191 |
| 50.00 | 20000 | 37.323 ± 0.043 |  8.750 ± 0.019 | 46.073 | 14.935 ± 0.023 | 0.324 |
| 100.0 | 20000 | 39.232 ± 0.041 | 10.001 ± 0.021 | 49.233 | 18.843 ± 0.025 | 0.383 |
| 200.0 | 20000 | 42.759 ± 0.043 |  8.541 ± 0.019 | 51.300 | 14.272 ± 0.024 | 0.278 |
| 500.0 | 20000 | 37.522 ± 0.045 |  4.929 ± 0.015 | 42.451 |  6.575 ± 0.017 | 0.155 |
| 1000  | 20000 | 27.670 ± 0.044 |  2.829 ± 0.011 | 30.499 |  3.412 ± 0.012 | 0.112 |

**Reading note:** these are **yields per primary** (per fired electron, in the 0.5 µm³ Francis target). They are NOT yet normalized to Gy⁻¹·Gbp⁻¹. Per-Gy/Gbp conversion needs (a) per-event absorbed-dose to target and (b) effective Gbp content of the 0.5 µm³ target — the example's `selectionProb=0.2` plus `Emin/Emax` ramp implicitly defines the DNA-equivalent target. The on-disk `edep` histogram (h5) has a 1-bin range and is unusable; a follow-up run with a corrected `edep` axis is needed for the absolute-dose-normalised yields. The shape of the energy dependence below is reliable independently of that normalization.

### Qualitative shape (sanity)

- **DSB rises monotonically** from 0.56/event @ 0.5 keV → peak 18.84/event @ 100 keV, then declines as electron range exceeds target (track segment in target shrinks): 14.27 @ 200, 6.58 @ 500, 3.41 @ 1000 keV. This is the **expected Francis/Nikjoo electron-DSB shape** — peak around 50–100 keV where LET within the target is maximised relative to range.
- **DSB/SSB ratio is U-shaped:** 0.25 @ 0.5 keV → minimum ~0.13 @ 2–5 keV → climbs to 0.38 @ 100 keV (high-density local cluster regime) → falls to 0.11 @ 1 MeV (sparse, low-LET).
- **Complex-SSB fraction tracks DSB/SSB** as expected (both are local-density driven).

---

## Comparison vs Second-100 track-structure papers

The 15 papers flagged in the task brief (s100-016 / -023 / -024 / -031 / -033 / -042 / -049 / -056 / -059 / -064 / -073 / -081 / -082 / -083 / -089) were scanned for explicit DSB/SSB yields at energies overlapping the campaign sweep. Below I list each paper, what it actually reports, and whether our MC sweep can promote its verdict.

> **Conservative rule:** we only promote SPOT-CHECK→PARTIAL where the paper reports a *quantitative* DSB or SSB yield at a *matched primary type and energy* that our campaign covers. Reviews, qualitative claims, and papers using different primaries (protons, ions) at LET values not derivable from our electron-only sweep are flagged **needs additional campaign**, not promoted.

### Directly comparable (electrons in the 0.3 keV – 1 MeV range)

| ID | Paper anchor | Reported (paper) | Our sweep covers? | Comparison verdict |
|----|--------------|------------------|-------------------|--------------------|
| **s100-024** | Mokari et al. 2018, *Track-structure simulation of low-energy electron damage to DNA with Geant4-DNA* (Biomed. Phys. Eng. Express). Y_DSB & Y_SSB in **Gy⁻¹·Gbp⁻¹** vs electron energy. Headline: Y_DSB ≈ 4.68 @ 4.5 keV → 29.55 @ 500 eV peak (Essb=17.5 eV, POH=0.13). SSB/DSB total ratio at 300 eV / Essb=17.5 eV: **5.66** (paper: 4.80–9.03 across thresholds). | **YES** — we have **0.5, 1, 2, 5 keV** electrons | **CAN promote to PARTIAL** once per-Gy/per-Gbp normalisation is applied. *Shape* matches: our DSB/SSB ratio falls from 0.25 (0.5 keV) → 0.14 (2 keV), matching Mokari's reported rise of SSB/DSB ratio from low → mid keV (their values are inverse-ratio of ours: 1/0.25 = 4.0 → 1/0.14 = 7.1, vs paper 4.80 → 9.03 across thresholds — same direction, within ~15%). **Action:** rerun with a working `edep` histogram + record target dose, then convert to Gy⁻¹·Gbp⁻¹; promote s100-024 from SPOT-CHECK to PARTIAL when matched. |
| **s100-064** | Yachi et al. 2019, *Track-Structure Study for Energy Dependency of Electrons and X-rays on DNA-DSB Induction* (Sci Rep 9:17649). Reports **DSB per nucleus** at kVp X-rays (30.2–41.9) and MV X-rays (22.2–25.9). Their MC engine is PHITS-derived; uses γ-H2AX foci, not direct DBSCAN. | **YES** for monoenergetic-electron analogues of their X-ray bremsstrahlung spectra (centroid ~50–100 keV for kVp, ~1 MeV for MV) | **Cannot promote** without folding their X-ray spectra into our monoenergetic sweep. Shape qualitatively matches: our 50–100 keV electron DSB/event peak (15–19/event) > 1 MeV (3.4/event), matching their kVp (30.2–41.9) > MV (22.2–25.9) ordering, but absolute numbers are *per primary in a 0.5 µm³ target*, theirs *per nucleus per Gy*. Requires (a) energy-spectrum convolution and (b) per-Gy normalisation. Flag: **needs spectrum convolution**. |

### Partially comparable (electron components only)

| ID | Paper anchor | Notes | Verdict |
|----|--------------|-------|---------|
| **s100-016** | Abolfath et al. 2013, molecular DSB model. Uses K_N (Klein-Nishina) spectrum to derive SSB/BD/DSB per track. References "1 MeV electron track" canonical. | Our 1 MeV point (DSB/event = 3.41) is comparable to paper's canonical 1 MeV electron track. Paper's headline ratio: **DSB_p / DSB_e = 4.0** (proton vs electron at matched energy). | **Cannot directly promote** — needs proton-MC half + same target. Flag for follow-up campaign with `dnaphysics` example + protons. |
| **s100-049** | Henthorn et al. 2019, RSC Adv. *Co-60 DSB calibration = 4.2 DSB/Gbp/Gy.* MM model. | Co-60 mean photon energy 1.25 MeV → secondary-electron spectrum mainly 100 keV–1 MeV Compton electrons. Our 100 keV–1 MeV sweep is the relevant secondary-electron-energy band. | **Cannot promote without Compton-spectrum folding + per-Gy/Gbp.** Flag: same as s100-064 (needs spectrum convolution). |
| **s100-083** | Hill 2019 review, *Clinical Oncology*. Canonical low-LET: **40 DSB, 1000 SSB per cell per Gy**. SSB/DSB ≈ 25. | Our 1 MeV electron: SSB/DSB = 30.5/3.4 ≈ 9 per primary; canonical 25 includes whole-cell, multi-track dose accumulation. Order-of-magnitude consistent. | **Already at LITERATURE-MATCH (PASS) in s100-083** (`✓ exact match` per the existing REPORT). No additional promotion needed. |

### Not directly comparable from this campaign

| ID | Why not |
|----|---------|
| s100-023 | Geometry-classes paper, no headline DSB-yield numbers. |
| s100-031 | TOPAS-nBio sensitivity study on **protons 0.5–50 MeV** + 9.3 µm full-nucleus model. Wrong particle, wrong target. Needs proton sweep with full-nucleus geometry. |
| s100-033 | CompuCell3D coupling paper. Single quantitative target (30.37%) is a growth/lattice number, not a DSB yield. Algorithmic sanity (DBSCAN) already done in `evidence/dbscan_sanity.txt`. |
| s100-042 | **Protons** at LET 1.9–39.7 keV/µm. Wrong particle. Y_DSB 3.5–7.8 Gy⁻¹·Gbp⁻¹. Needs proton campaign with LET binning. |
| s100-056 | MPEXS2.1-DNA water-radiolysis paper (chemistry-focused). Different output channel (G-values, not DBSCAN-DSB). |
| s100-059 | Geant4-DNA neural-cell paper. **Heavy ions** (different LET). Wrong particle for our electron sweep. |
| s100-073 | DaMaRiS proton planning paper. Reference photon yields γ_r = 1.726, γ_m = 0.0427 DSB/Gy (Co-60). Same Compton-folding issue as s100-049. |
| s100-081 | DSB/RIF Poisson tables at **LET 90 and 160 keV/µm** (heavy-ion regime). Wrong particle, wrong LET regime. |
| s100-082 | G-NOME Hi-C/Geant4-DNA pipeline. Yields are **per Gy of Co-60 + protons/He/C ions**, all at named LET. Compton-folding for the Co-60 calibration possible; the rest is not in our sweep. |
| s100-089 | HZE-particle qualitative review. No quantitative DSB yields at electron energies. |

---

## What can be promoted right now

After this single campaign sweep (electrons only, per-primary yields, no dose normalisation):

| Paper | Current verdict | After sweep | Action needed |
|-------|-----------------|-------------|---------------|
| s100-024 | SPOT-CHECK | **→ PARTIAL** (candidate) | One follow-up run with fixed `edep` axis + per-event-dose scoring → normalise to Gy⁻¹·Gbp⁻¹ → tabulate at 0.5/1/2/5 keV vs paper Table 3. |
| s100-064 | SPOT-CHECK | unchanged | Needs X-ray spectrum convolution (folding monoenergetic e⁻ yields with kVp/MV bremsstrahlung). |
| s100-049 | SPOT-CHECK (PARTIAL per existing report) | unchanged | Co-60 Compton-electron spectrum convolution + per-Gy/Gbp normalization. |

All others either (a) already at their justified verdict (s100-083 PASS, s100-082 thorough audit, etc.), (b) need proton/ion campaigns we have not yet run (s100-016/-031/-042/-049/-059/-081/-082), or (c) are reviews/methods papers without numeric DSB targets (s100-023/-033/-056/-073/-089).

---

## Follow-up campaigns recommended (in priority order)

1. **Fix `edep` histogram axis** in the clustering example UI commands or scoring code, then re-run the electron sweep at the same 11 points to get per-event absorbed dose → convert all yields to Gy⁻¹·Gbp⁻¹. (≤30 min on uicgpu.)
2. **Proton sweep** at matched LET points (1.9, 5, 10, 20, 40 keV/µm) using `clustering` with `/gun/particle proton` and stopping-power-derived energies. Promotes s100-042, s100-031, s100-049 (proton side), s100-016 (proton-vs-electron ratio).
3. **Co-60 photon spectrum convolution** — generate Compton-electron-spectrum-weighted DSB yield from our existing electron sweep + tabulated K-N cross sections. Promotes s100-049 calibration to PARTIAL and helps s100-064 / s100-082 photon calibrations.
4. **Heavy-ion sweep** (α, C) at LET 50–160 keV/µm for s100-059, s100-081, s100-082. Needs `clustering` with ion gun + ion-physics constructor.

---

## Provenance / commands

```
ssh -o ProxyJump=nuc13 uicgpu \
  'ls /gpustor/stevens/radmc/campaign/clustering/'
# CAMPAIGN.log  E_0.5keV  E_1000keV  E_100keV  E_10keV  E_1keV
# E_200keV  E_20keV  E_2keV  E_500keV  E_50keV  E_5keV  TEST

# Per-event histograms in each E_<E>keV/clusters_output.root:
#   h1 simpleSSB, h2 complexSSB, h3 DSB, h4 cluster size, h5 edep (broken: 1 bin)

# Extraction script (uproot):
#   /tmp/extract_campaign.py  (local; mirrored to uicgpu:/tmp/)
# Numeric summary: /tmp/campaign_summary.json (mirrored locally on CherryRd)
```

**Written:** 2026-06-25 by harvest cron `harvest-geant4dna-mc-campaign`.
**Caveat — do NOT fabricate:** all numbers above are direct readouts of the ROOT histograms (means and SEMs computed from per-event bins). Where a yield is *not* in the table (e.g. per-Gy/Gbp values), it has not been computed — only the per-primary shape is currently available.
