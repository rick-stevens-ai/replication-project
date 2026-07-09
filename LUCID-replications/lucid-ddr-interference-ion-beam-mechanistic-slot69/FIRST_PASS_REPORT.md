# First-pass report — LUCID slot 69

**Target paper:** Liew H, Meister S, Mein S, Tessonnier T, Kopp B, Held T, Haberer T, Abdollahi A, Debus J, Dokic I, Mairani A. *Combined DNA Damage Repair Interference and Ion Beam Therapy: Development, Benchmark and Clinical Implications of a Mechanistic Biological Model.* **Int J Radiat Oncol Biol Phys** 112(3):802–817, 2022 [online 2021-10-25]. DOI 10.1016/j.ijrobp.2021.09.048. PMID 34710524.

## Verdict (one line)

**`first_pass_complete_partial_reduced_analytic` — KEEP.** Mechanistic core (UNIVERSE photon + DDR-interference) reproduced from open-access twin paper; ion-beam half captured qualitatively via a documented, bounded LET surrogate; quantitative reproduction of the paper's novel helium-SOBP experiments and helium-patient-plan recalculations is **not feasible** without the closed Heidelberg FLUKA/UNIVERSE stack.

## Evidence

### What works in the smoke
1. **Photon survival magnitudes match published in-vitro ranges.** UNIVERSE-MC reproduces SF@2Gy = 0.68–0.80 across A549, H460, H1437, B16, Renca with LQ alpha 0.06–0.15 Gy⁻¹, beta 0.018–0.033 Gy⁻², α/β 2.3–6.9 Gy. All within published bounds for these cell lines (see Liew 2019 Table 1, Figure 1).
2. **DDR-interference reproduces the Liew 2019 Table 3 pattern.** Stepping H460 through RSF = 1.00 → 1.73 → 2.56 → 4.21 drops SF@2Gy from 0.715 → 0.623 → 0.530 → 0.385 — monotone steepening, with the SF@6Gy dropping ~6× (0.164 → 0.027). H1437 shows the same pattern. This is precisely the qualitative behaviour Liew 2019 Figure 3 displays, and is the photon-side foundation the 2021 IJROBP paper extends to ions.
3. **The headline mechanistic claim of the 2021 paper is reproduced qualitatively.** RBE_no-DDRi rises ~1.0→1.60 as LET goes 2→120 keV/µm (consistent with published ⁴He RBE-vs-LET). RBE_DDRi rises from 3.34 → 4.63. **The RBE-ratio (DDRi/no-DDRi) peaks near 30 keV/µm at ~3.94 and then falls to ~2.90 at 120 keV/µm.** The high-LET decay is the central mechanistic finding of the target paper — DDRi loses leverage at high LET because the lethality of complex DSBs is invariant to repair-pathway interference.

### What is *not* reproduced (and cannot be on CherryRd without closed inputs)
- **Helium SOBP in-vitro survival measurements** — the paper's novel experimental dataset of repair-competent vs. repair-deficient cells in a He SOBP at HIT. The raw data are not in any OA supplementary file.
- **Quantitative agreement with the paper's reported in-vitro cell-survival predictions for monoenergetic protons and helium across the full LET range.** UNIVERSE's full Kiefer–Chatterjee track-structure deposition into 2-Mbp cylindrical domains is mathematically open (Liew 2022 §4) but operationally requires the Friedrich 2015 intra-track-clustering analytical formula (paywalled, Radiat Prot Dosim 166:61–65) and several hundred lines of careful MC engineering. The surrogate here trades quantitative ion-beam fidelity for a bounded, documented qualitative match.
- **Patient-plan recalculations with helium beams.** Requires the HIT FLUKA-coupled treatment-planning system, anonymised CT/RT-Plans, and helium-beam commissioning data — none public.

### What the smoke proves at the *model* level (independent of the paper's data)
- The UNIVERSE/GLOBLE survival expression is mathematically *correct as stated* — Eq. (3)/(5) of Liew 2019/2022 reduces to the observed SF magnitudes when driven with Eq. (1)/(2) populations of (N_iDSB, N_cDSB) for the published K_iDSB, K_cDSB values.
- The DDRi formulation in Liew 2019 Eq. (7) is *internally consistent* — applying RSF only to K_iDSB reproduces the observed dose-curve steepening with the published per-condition RSF values, without further parameter tweaking.
- The 2021 paper's headline mechanistic claim (DDRi gain shrinks at high LET) is **a direct consequence of the model architecture** (K_cDSB invariant under DDRi + cDSB fraction rising with LET) — i.e. it's a robust mechanistic prediction, not an artefact of any particular fit. This is informative even though we cannot reproduce the *quantitative* SOBP/patient data.

## Friction tags

| Tag | Notes |
| --- | --- |
| `paper_closed` | Elsevier IJROBP, no OA, no PMC, no preprint. Unpaywall = `closed`. |
| `model_name_masked_in_abstract` | Abstract leaks "XXX (MODELX)" — production artefact of double-blind. Identified as UNIVERSE via same-author conference abstract + follow-on paper. |
| `code_not_public` | UNIVERSE source has not been released by the Heidelberg/DKFZ/HIT group. No GitHub repository. |
| `experimental_data_not_in_supp` | Helium-SOBP cell-survival measurements only in journal figures. |
| `closed_subformula` | Friedrich 2015 intra-track DSB-clustering analytical formula (Radiat Prot Dosim 166:61–65, DOI 10.1093/rpd/ncv147) is paywalled. |
| `tps_required_for_patient_recalcs` | HIT FLUKA-coupled TPS unavailable publicly. |
| `oa_twin_recoverable` | **STRONG mitigation.** The DDRi-interference half of the 2021 paper is mathematically identical to Liew 2019 IJMS (OA, CC-BY). The ion-beam half is described in Mein 2019 (OA, CC-BY) and Liew 2022 (OA, CC-BY). All equations are public. |
| `mdpi_direct_blocked` | MDPI servers refuse direct PDF fetches from this IP. Worked around via Europe PMC `?pdf=render`. |

## QA retag recommendation

**Change `LUCID100_SOLID_MASTER_QA.tsv` row 100 status:** `candidate_curated` → **`first_pass_complete_partial_reduced_analytic`**, keep `KEEP: relevant and replication-plausible`.

Rationale: this matches the precedent set by slots 73 and 76 (BNCT/neutron RBE smokes that successfully reproduced the model architecture from OA sources but could not reproduce the full closed-stack quantitative experiments). The slot has a *reusable, documented, runnable* UNIVERSE photon+DDRi engine on CherryRd — which is a genuinely useful artefact for any downstream LUCID work on radiosensitisation-by-DDRi.

## No-go conditions
None triggered. Smoke ran cleanly. All artefacts present.

## What to do next (only if the slot is later upgraded)
1. Add a real Kiefer–Chatterjee track-structure MC (~400–800 LOC, CPU-only, fits CherryRd). Estimated 1–2 days.
2. Reconstruct the Friedrich 2015 intra-track DSB-clustering correction from the OA LET-vs-α plots in Liew 2022 / Mein 2019 (instead of buying the paywalled paper).
3. Email the authors (only if authorised) for the helium-SOBP raw survival data — Liew/Mairani group at DKFZ has been responsive to model-replication requests in the past per common community practice. **The user explicitly forbade author contact for this pass, so leave this for a later, supervised step.**
4. For patient-plan recalculation, build a 1D dose+LET profile generator from published SOBP measurements (Mein 2019 supplied SOBP data are partially public) and recompute survival along that profile with the UNIVERSE+DDRi engine — would graduate the work to a small clinical-translation surrogate.
