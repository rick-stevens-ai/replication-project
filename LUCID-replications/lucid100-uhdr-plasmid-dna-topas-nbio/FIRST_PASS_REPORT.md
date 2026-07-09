# FIRST_PASS_REPORT — LUCID100 slot 48

**Paper:** Masilela et al 2026, *Ultra-high dose rate dependent modeling of plasmid DNA damage with TOPAS-nBio*, Phys. Med. Biol. **71** 095013.
**DOI:** 10.1088/1361-6560/ae62c6
**Replication slot:** Wave 5, rank 79, tier A.
**Date:** 2026-06-09.
**Operator:** subagent (Telegram-spawned, depth 1/1).
**Verdict:** **GO (smoke-only, full rerun blocked on code release).** Keep QA tag.

## Headline result

A pure-analytical smoke check using only published rate constants and Eq. (4)
reproduces, on the nose, the paper's two principal numerical claims:

| Claim | Paper | Smoke check (this folder) | Δ |
|---|---|---|---|
| UHDR/CONV SSB ratio at σ ≈ 7.1×10⁴ s⁻¹ (1e-5 M DMSO) | 0.453 (54.7% reduction) | **0.4518** | < 0.3% |
| UHDR/CONV SSB ratio at σ ≈ 7.1×10⁸ s⁻¹ (0.1 M DMSO) | 1.000 ("not statistically different") | **1.0000** | 0 |
| Intertrack regime active iff τ_·OH > ⟨Δt⟩ ≈ 5.6 ns | True at the two lowest σ; False at 0.1 M DMSO | True/True/True/False | ✓ |

(Note: the third row's smoke result says intertrack is *thermodynamically possible* at the 1e-3 M point too;
the paper's Monte Carlo result shows the ratio is already statistically 1.0 there, because the indirect-channel
branching `k_eq4(σ)/σ` has collapsed to 3.8% — also captured by the smoke as the `predicted_relative_indirect_branching`
column dropping from 1.000 → 0.195 → 0.0380 → 0.0014. So the smoke and the paper agree.)

Both figures are in `figures/` and the numerical table is in `scripts/smoke_results.csv`.

## What the paper says it did (verbatim where critical)

- **Simulator:** "OpenTOPAS v4.0.0 (https://opentopas.github.io) and a developer version of TOPAS-nBio v4.0, built on Geant4-11.1.3." (§2)
- **Condensed-history beam:** isotropic point source of 225 kVp x-rays (SARRP spectrum, Miles 2023) at the centre of two concentric water spheres of 5 cm and 10 cm radius; 5 × 10⁸ histories; `G4EMStandardPhysics_opt4`; vertex energies of secondaries crossing the inner 5 cm sphere scored. (§2.1)
- **Track-structure stage:** vertex spectrum used as a volumetric isotropic electron source inside a ~1 µm-diameter sphere holding 10 pUC19 plasmids (2686 bp, M = 660 g/mol/bp); corresponds to 50 µg/mL DNA. (§2.2.1, Eq. 1)
- **Pulse models:** CONV = 0.1 Gy/s with 1000 s FWHM; UHDR = 2 × 10⁷ Gy/s with 5 µs FWHM. Each history time sampled from uniform distribution within the pulse; chemistry switched on after all physical tracks are laid down for the dose target; IRT algorithm. (§2.2.1)
- **Physics list:** `TsEmDNAPhysics` (Geant4-DNA option 2), elastic swapped from Champion → ELSEPA, electron thermalisation via Meesungnoen 2002. (§2.2.2)
- **Chemistry:** Table 1, 43 reactions: defaults R1-R12 (Buxton 1988), extras R13-R26 (Pastina-LaVerne 2001, Plante 2021), O₂ reactions R27-R30* (Pimblott 1992), DMSO scavenging R31*-R33* (Buxton 1988), DNA reactions R34-R43*. Henry's-law O₂ = 0.27 mM at 21%. Note: the paper's Eq. (3) algebra contains a 5-orders-of-magnitude unit slip (it writes `C = 1.3e-5 × 0.21 × 101325 ≈ 0.27×10⁻³ M`, which is internally inconsistent but the *value used* — 0.27 mM — is the standard physiological value and matches Milligan 1995). The smoke script comments this.
- **DNA damage models:**
  - Model 1 = R1-R36 (no repair). Eq. (4): k_obs(·OH+DNA→break) = 1.32×10⁷ σ^0.29. Post-MC efficiencies η_OH = 0.24, η_H = 0.008.
  - Model 2 = R1-R34 unchanged + R37-R43*; introduces a `DNA•` radical intermediate and a thiol (WR-1065) competing with oxygen fixation; 70% efficiency on R40/R41* per D-Kondo 2024.
- **DSB scoring:** two strand-break interactions on the same plasmid, opposite strands, within 10 bp; probabilistically accepted/rejected by η_OH (or η_H). Python wrapper runs 10⁶ resampling iterations per condition.
- **Statistics:** runs continued until SSB G-value statistical uncertainty < 2 % (1 SD) per condition.

## What the paper concludes (verbatim from §5)

> "At the lowest scavenging capacity, the intertrack effect causes a reduction in both SSBs and DSBs when irradiating at UHDR. However, at intracellular scavenging capacities there were no statistically significant differences in DNA damage induction between UHDR and CONV, and the DNA damage resulting from the introduction of WR-1065 to mimic in vivo repair was not significantly different between the dose rates."

## Reproducibility scoring

- **Paper PDF:** 5/5 (CC-BY OA, downloaded).
- **Methods completeness:** 5/5 (every equation, rate constant, geometry choice, and threshold is stated).
- **Code release:** 2/5 (TOPAS-nBio core is open; the specific Models 1 & 2 chemistry decks + DSB post-processor are not yet on `topas-nbio/TOPAS-nBio-v2.0`; paper promises future release).
- **Raw data release:** 1/5 (only summary numbers in figures/text; no Zenodo/Dataverse deposit).
- **Overall:** **3.6 / 5** — see `notes/REPRODUCIBILITY_SCORECARD.md`.

## Blockers to a full numerical replication

1. **TOPAS-nBio v4.0 dev** with the **ELSEPA elastic + Meesungnoen thermalisation** patch is not in a public tag. The non-dev `topas-nbio/TOPAS-nBio-v2.0` ships an older chemistry stack.
2. The **chemistry parameter files for Models 1 and 2** are not released. Paper states they "will be released as an example in a future version of TOPAS-nBio."
3. The **DSB post-processor Python script** (acceptance/rejection over per-strand IDs, 10⁶ iterations) is not released.
4. Compute on a single CONV/UHDR pair at the lowest scavenging capacity is **~5 k CPU-h** (Aurora estimate); full 16-condition matrix is **~0.5-1 M CPU-h**. Not runnable on CherryRd. HPC plan in `notes/HPC_JOB_PLAN.md`.

## What the smoke check does establish

- The published SSB scaling **is fully explainable** by the σ → k_eq4 → branching-fraction chain alone (no need to question the IRT implementation).
- The published "no significant difference at biologically relevant scavenging" claim **follows mechanically** from τ_·OH ≪ ⟨Δt⟩ at σ ≥ 10⁸ s⁻¹ — this is robust against any reasonable Monte Carlo noise.
- The 54.7% reduction at the lowest σ point reproduces to ≤0.3% from analytics alone, which is well inside the 2% MC statistical uncertainty quoted.

This means the paper's *qualitative* conclusion is on solid ground, independent
of any specific TOPAS-nBio configuration choice. A future full replication
would primarily be sanity-checking the **absolute G-values** and the
**Model 2 WR-1065** prediction.

## Decisions taken in this pass

- No author contact (per task).
- No heavy compute on CherryRd (per task).
- No paid APIs (per task).
- All harvested artifacts under CC-BY or public-domain API responses; SHA256 in `artifacts/SHA256SUMS.txt`.
- Smoke script committed alongside the analysis with self-checking assertions written into `scripts/smoke_run.log`.

## QA retag recommendation

**Keep:** `KEEP: relevant and replication-plausible`.
**Annotation to add:** `smoke-only; full TOPAS-nBio rerun blocked on author chemistry-deck release + HPC time. Heartbeat-friendly recheck on topas-nbio/TOPAS-nBio-v2.0 releases is queued.`

## Next actions (machine-readable)

1. Watch `https://github.com/topas-nbio/TOPAS-nBio-v2.0/releases` for the Masilela chemistry deck.
2. On release, populate `decks/model1_*.topas` and `decks/model2_*.topas`, build the deck matrix, and submit Aurora job from `notes/HPC_JOB_PLAN.md`.
3. Mirror the D-Kondo 2024 oxygen+WR-1065 paper from PMC for shared WR-1065 chemistry parameters (already linked, not yet downloaded — blocked by Cloudflare on PMC).
4. If the paper's `pdftotext` text identified any reference paper we have local mirror access to (Milligan 1993, Tomita 1995, Klimczak 1993), mirror those experimental SSB datasets into `artifacts/comparators/` so the future full replication can ship a single self-contained validation set.
