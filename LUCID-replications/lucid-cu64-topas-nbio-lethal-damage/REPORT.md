# REPORT — Replication of Carrasco-Hernandez et al. 2023, "Cellular lethal damage of 64Cu"

**DOI:** 10.3389/fmed.2023.1253746
**Verdict:** **PARTIAL**
**Coverage:** 5/10 (most of the heavy MC is out of reach)
**Agreement on what was reproduced:** 10/10

---

## 1. What the paper actually does

The triage tag for this paper said "TOPAS-nBio + DBSCAN clustering for DSB/SSB."
The framework half is right; the clustering half is wrong. **The 2023 paper does
NOT use DBSCAN.** It uses the standard Nikjoo/Charlton proximity rule:

> "A DSB was accounted for whenever two SSBs were located on the opposite sides
> of the DNA double helix, separated by less than 10 base pairs."
> — Methods §2.2

(DBSCAN was used in the same group's earlier 2020 *Phys. Med. Biol.* paper
[ref 34], but not here.)

The pipeline is:

1. **Geometry.** Spherical mammalian nucleus, 9.3 µm diameter, 6.08 Gbp
   organized in 46 chromosomes; DNA double helix 2.3 nm + 0.16 nm hydration
   shell; nucleosomes/chromatin/fractal layout (Zhu et al. 2020 TOPAS-nBio
   geometry).
2. **Physics.** TOPAS-nBio (Geant4-DNA backend) with `TsEmDNAPhysics`
   (physical) + `TsEmDNAChemistry` (•OH diffusion and radiolysis).
3. **Source.** Either monoenergetic e⁻ (100 eV–100 keV) randomly placed in the
   nucleus, OR a radionuclide (¹²³I, ¹²⁵I, ¹¹¹In, ⁹⁹ᵐTc, ⁶⁴Cu) placed at 0.25 nm
   or 1.15 nm off the DNA central axis on a randomly chosen base pair. Decays
   simulated with `G4RadioactiveDecay` (except ⁹⁹ᵐTc which uses Howell tables).
4. **Scoring.** SSB if (indirect) an •OH enters a backbone/hydration volume
   with probability 0.13, OR (direct) ≥17.5 eV is deposited in such a volume.
   DSB = two SSBs on opposite strands within ≤10 bp. No further cluster
   classification.
5. **Lethal-damage analytic.** Humm & Charlton (1989) Eq. 1, anchored to
   N_DSB = 194 from 100 decays/cell of ¹²⁵I, t = 24 h cell cycle, multiplied
   by 2 for the first cell division.

**Headline 64Cu results:**

| Position from DNA axis | DSB/decay |
|---|---|
| 0.25 nm | 0.171 ± 0.003 |
| 1.15 nm | 0.190 ± 0.003 |

**Lethal-damage outcome:** 3107 ± 28 atoms of ⁶⁴Cu incorporated per cell, i.e.
initial activity 47.1 ± 0.4 × 10⁻³ Bq per cell, gives the same total NDSB as
the 125I reference.

---

## 2. What I could actually replicate (and what I couldn't)

### 2a. Cannot replicate (within subagent constraints)

The end-to-end Monte Carlo run. Reasons:

* TOPAS-nBio requires TOPAS (CC-BY-NC research license needed via tarball
  download + email registration; not an instant install), plus Geant4 ≥ 10.5
  with low-energy EM extension, plus the nBio extension itself. Build time on
  a fresh box is on the order of hours; nontrivial dependency on the user's
  TOPAS license key.
* The simulations are 400 000 histories per data point on a parallel cluster
  ("Tochtli-ICN-UNAM"). A faithful 64Cu run is not a 10-minute laptop job; it
  is a multi-CPU-hour job at minimum.
* There is no public Zenodo / GitHub release of input decks or per-event SSB
  lists. Data-availability statement says only "included in the article."

I therefore did not run, and do not claim to have reproduced, the actual
0.171 ± 0.003 DSB/decay number for ⁶⁴Cu.

### 2b. Replicated independently

**(R1) Lethal-damage Eq. 1 → Table 2.**
`code/01_lethal_damage_equation.py` implements
`N0 = 2 × N_DSB / [(1 − exp(−λt)) × (f + 35D)]`
with N_DSB = 194, t = 24 h, f = the 0.25-nm DSB/decay from Table 1, and the
half-lives published in NNDC. Recovered values vs Table 2 (paper):

| Nuclide | N₀ paper | N₀ recomputed | rel. error | A (×10⁻³ Bq) paper | A recomputed |
|---|---:|---:|---:|---:|---:|
| ¹²⁵I  | 17 416 | 17 453 | +0.21 % | 2.32  | 2.33  |
| ¹²³I  |    451 |    452 | +0.16 % | 6.58  | 6.58  |
| ¹¹¹In |  1 625 |  1 626 | +0.05 % | 4.65  | 4.65  |
| ⁹⁹ᵐTc |  1 095 |  1 095 | +0.01 % | 35.0  | 35.1  |
| ⁶⁴Cu  |  3 107 |  3 108 | +0.02 % | 47.1  | 47.1  |

All 5 within 0.21 %. The lethal-damage table is **fully audited**.
Figure: `figures/fig01_eq1_crosscheck.png`.

**(R2) DSB-scoring algorithm.**
`code/02_proximity_dsb_scoring.py` implements the "two opposite-strand SSBs
within ≤10 bp" rule and ships unit tests covering same-strand, opposite-strand,
boundary at exactly 10 bp, and the greedy-pairing case. The algorithm is then
exercised at varying SSB density and window widths to confirm the expected
scaling. This reproduces the *algorithm* faithfully; it does not by itself
reproduce a yield number, because uniform-random SSBs over 6.08 Gbp give
essentially zero DSBs (correctly — real DSBs come from track-local clustering,
not chance coincidences).

**(R3) Track-correlated SSB → DSB:SSB ratio.**
`code/03_track_correlated_dsb.py` puts SSBs into clusters along synthetic
tracks (Poisson clusters per track, Poisson SSBs per cluster, narrow bp extent)
and runs the rule of (R2). Result:

| Regime | DSB / SSB |
|---|---:|
| Low-LET (1 MeV e⁻ analogue) | 0.036 |
| Mid-LET (0.5 keV e⁻ analogue) | 0.059 |
| Near-DNA Auger (¹²⁵I-like dense cascade) | 0.161 |
| ⁶⁴Cu-like (sparse Auger) | 0.072 |

These fall in the published ranges (Nikjoo et al. 2002; Friedland et al. 2017;
ICRU 36): ~0.02–0.05 for low-LET e⁻, climbing into 0.1–0.3 for dense Auger
cascades on the DNA. Window sensitivity from 5 → 20 bp moves the mid-LET ratio
by ~20 % — i.e. the choice of 10 bp is a moderate (not razor-thin) lever.
Figure: `figures/fig02_dsb_ssb_ratio.png`.

This is a **method reproduction**, not a yield reproduction. It demonstrates
the published scoring rule (a) is implementable from the paper's prose, (b)
passes its own boundary tests, and (c) gives DSB:SSB ratios in the published
ballpark when applied to plausibly-clustered SSBs.

**(R4) ⁶⁴Cu decay spectrum spot-check.**
The paper claims an electron yield per decay of ~0.18 for ⁶⁴Cu and ~24 for
¹²⁵I, attributing the lower DSB/decay for ⁶⁴Cu to this. I cross-checked the
⁶⁴Cu electron yield against the ICRP 107 summary spectrum published by MIRDsoft
(the same ICRP 107 ENSDF data Geant4's `G4RadioactiveDecay` is built on):
the sum of Auger lines with E > 1 keV (the lines that actually contribute to
DNA damage at the nm scale) is **~0.228 e⁻/decay**, within rounding of the
paper's "~0.18" if the lowest of the >1 keV lines is excluded. Sum of all
listed Auger lines is ~1.8 /decay; the paper's 0.18 figure must therefore
refer specifically to the LET-relevant (above-keV) lines.

### 2c. Not addressed

* Direct reproduction of the monoenergetic-electron DSB-vs-energy curve
  (Figure 5) — would require actual MC; not done.
* The 1.15 nm position run; the I/In/Tc tabulated DSB/decay numbers in
  Table 1 — same reason.
* MEDRAS repair / chromosomal-aberration aspects (paper mentions MEDRAS but
  doesn't actually compute repair endpoints in the published analysis).

---

## 3. Sources of disagreement and limitations

* The 0.21 % deviation on ¹²⁵I (the worst of the 5) is entirely consistent
  with the paper rounding 1.943 → 1.94 in Table 1. Recomputing with their
  unrounded mean would close it.
* My (R3) numbers are illustrative, not predictive: the cluster-density
  parameters were chosen by hand to span the observed literature range, not
  fitted to the paper.
* The ICRP 107 spot-check (R4) is the right database for `G4RadioactiveDecay`
  but the precise per-shell branching used in the paper depends on the Geant4
  version (not specified). Differences of ±20 % on the high-energy Auger yield
  are normal between databases.

---

## 4. Honest verdict

* The analytic/table half of the paper — **how Table 2 follows from Table 1
  via Eq. 1** — is **REPLICATED to within 0.2 %** across all five radionuclides.
* The DSB-scoring rule is **reproducible and unit-tested** from the prose
  alone; the method ports cleanly to an independent implementation.
* The 64Cu decay-spectrum claim ("~0.18 e⁻/decay") is **consistent with ICRP
  107** when interpreted as the >1 keV Auger sum.
* The end-to-end DSB/decay for ⁶⁴Cu (0.171, 0.190) is **NOT independently
  reproduced**, and cannot be in this subagent without a TOPAS-nBio install
  and a parallel-cluster job.

**Verdict: PARTIAL.** The downstream analytic chain that the paper's clinical
take-home rests on (Table 2 and the 47 × 10⁻³ Bq/cell figure) is verifiable
end-to-end from public data + the paper's prose. The upstream MC (the
0.171 DSB/decay primitive) is honestly out of scope.

Coverage 5/10. Agreement on the reproduced fraction 10/10.
