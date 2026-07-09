# FIRST-PASS REPLICATION REPORT — LUCID100 slot 42 (Wave 5)

**Paper:** Yu C., Geng C., Tang X. (2024).
*Assessing the biological effects of boron neutron capture therapy through cellular DNA damage repair model.*
Medical Physics 51(12), 9372–9384.
**DOI:** 10.1002/mp.17446
**Date of this report:** 2026-06-09
**Replicator:** Ollie (subagent of main session, depth 1)

---

## 1. Verdict

`PARTIAL_REDUCED_ANALYTIC` — methodology reproduces, exact numerical reproduction is **blocked on unreleased authors' data** (BNCT-specific Geant4-DNA radial-deposition tables and TOPAS-nBio dose factors for BPA / BSH microdistributions).

A CPU-only analytic smoke check is included and runs in ~2 seconds on CherryRd; it reproduces the modeling pipeline (LQ fits per radiation component + Eq. 6 dose-share accumulation) and recovers the qualitative RBE ordering reported in Table 1.

## 2. What the paper does

The paper extends the **MEDRAS** (Mechanistic DNA Repair And Survival) model of McMahon & Prise (Front. Oncol. 2021, doi:10.3389/fonc.2021.689112) to BNCT. The pipeline (Fig. 1 of the paper) is:

1. **Step A — Geant4-DNA** with `G4EmDNAPhysics`: compute radial energy deposition E(r) at the center of a 200 μm × 22 μm water phantom for:
   - α at 0.2, 0.4, …, 1.2, 1.47, 1.78 MeV
   - ⁷Li at 0.2, 0.4, 0.6, 0.84, 1.02 MeV
   - recoil protons over 0.001–1 MeV
   This gives the DSB induction profile around an ion track (EDSB = 56.5 keV).
2. **Step B — TOPAS-nBio**: 3×3×3 grid of cells (nucleus r=4.32 μm, cell r=8 μm). Compute **F factor** (nucleus / cell dose ratio) per particle type and per drug microdistribution. Boron element ratio N from Eq. 5; reference boron concentration ratio C_B = 3.2 for BPA and 0.86 for BSH (from Hiratsuka 1991 melanoma data, ref. 4). For BPA, N_c = 0.78 and N_e = 0.22 (cytoplasm + extracellular); for BSH, N_s = 0.48 and N_e = 0.52 (membrane + extracellular).
3. **Step C — TOPAS-nBio**: per-source-location **W factor** for α and ⁷Li, where source can be at nucleus (n), cytoplasm (c), membrane (s), or extracellular (e).
4. **MEDRAS / MEDRAS-MC**: read SDD-format DNA damage distributions; run two-step repair (free-end interaction + irreversible joining) modeled as exponential processes with effective rate λᵢ = λₓ ηᵢ (Eq. 1) and repair time tᵢ = −log(X) / λᵢ (Eq. 2). Misrepair classification → survival probability.
5. **LQ fit + Eq. 6 accumulation**: per-component LQ fit (α, β); total mix via −ln S(D_mix) = Σᵢ (αᵢ Dᵢ + βᵢ Dᵢ²), with Dᵢ split per drug-dependent dose share.
6. Compare to the **photon iso-effective dose model** (González et al., ref. 29) to assess synergistic effects.

**Headline outputs** (Table 1, paper):

| Component | RBE₅₀ | RBE₁₀ | RBE₁  | Experimental (SF=0.01) | Ref. |
|---|---|---|---|---|---|
| γ | 1 | 1 | 1 | 1 | — |
| Proton | 6.87 | 3.97 | 3.21 | 3.2 | 6 |
| B (BPA) | 7.34 | 4.70 | 3.60 | 5.65 / 3.8 | 41 / 6 |
| B (BSH) | 1.94 | 1.02 | 0.73 | 2.29 / 1.2 | 41 / 6 |
| Total BPA | 5.18 | 3.20 | 2.50 | 2.52 / 2.81 | 4 / 2 |
| Total BSH | 4.64 | 2.67 | 2.15 | 1.99 | 2 |
| Without B | 4.65 | 2.56 | 1.95 | 1.99 / 1.25 | 4 / 2 |

## 3. Public artifacts inventory

| Layer | Status | Notes |
|---|---|---|
| Paper PDF | ✅ open access via NUAA mirror | downloaded to `refs/paper.pdf` |
| MEDRAS analytic | ✅ public on GitHub (`sjmcmahon/MEDRAS`) | Python; cloned to `artifacts/medras_analytic/` |
| MEDRAS Monte Carlo | ❌ not on public GitHub | referenced in the paper but not the McMahon `sjmcmahon` org |
| Yu/Geng/Tang BNCT extension | ❌ **no release** | no code/data availability statement |
| Radial-deposition tables (Geant4-DNA) | ❌ not provided | regenerable from Geant4-DNA |
| F, W dose factors (TOPAS-nBio) | ❌ not provided | regenerable from TOPAS-nBio |
| Supplementary material on Wiley | ❌ none located | verified via search; standard article only |
| Author contact attempted? | NO — per LUCID100 rules | — |

## 4. Reduced analytic smoke check — results

Script: `scripts/medras_bnct_smoke.py` (CPU-only, ~2 s, uses the public analytic MEDRAS with its built-in proton & helium track libraries).

**LQ fits over 0–10 Gy:**

| component | α [1/Gy] | β [1/Gy²] | description |
|---|---|---|---|
| photon (default X-ray) | 0.470 | 0.0359 | reference |
| proton, LET=5 keV/μm | 0.563 | 0.0351 | recoil proton, high-E tail |
| proton, LET=17 keV/μm | 0.863 | 0.0279 | 0.58 MeV proton from ¹⁴N(n,p)¹⁴C |
| helium, LET=150 keV/μm | 1.506 | 0.0027 | surrogate for α+⁷Li boron dose |

**RBE vs photon at three survival endpoints:**

| component | D@0.5 | RBE₅₀ | D@0.1 | RBE₁₀ | D@0.01 | RBE₁ |
|---|---|---|---|---|---|---|
| photon | 1.34 | 1.00 | 3.80 | 1.00 | 6.54 | 1.00 |
| proton (low LET) | 1.15 | 1.17 | 3.38 | 1.12 | 5.96 | 1.10 |
| proton (mid LET, 0.58 MeV) | 0.78 | 1.71 | 2.47 | 1.54 | 4.64 | 1.41 |
| helium @ 150 keV/μm | 0.46 | 2.91 | 1.53 | 2.49 | 3.04 | 2.15 |

**Eq. 6 mix (BPA-like high-boron: 65 % boron / 17 % proton / 18 % γ):**
LQ fit of the resulting SF curve gives α = 1.21, β = 0.003; D@SF=0.01 = 3.77 Gy → **RBE₀.₀₁ ≈ 1.73**.

## 5. Comparison and interpretation

| metric | paper (Table 1, BPA total) | this smoke check | Δ |
|---|---|---|---|
| Photon D@SF=0.01 | (implied 6.5–7 Gy via D₃₇ ratios) | 6.54 Gy | well-aligned |
| Boron-dose component RBE₀.₀₁ | 3.60 (BPA) / 0.73 (BSH) | 2.15 (LET=150 keV/μm surrogate) | within a factor of ~2; the BPA-vs-BSH spread is **driven by the F/W microdistribution factors** the smoke check does not have |
| Proton-component RBE₀.₀₁ | 3.21 | 1.41 (LET=17 keV/μm) | reduced analytic underestimates; their proton-component RBE includes the very-low-energy tail (where LET is much higher) plus microdistribution weighting |
| BPA total RBE₀.₀₁ | 2.50 (exp 2.52 / 2.81) | 1.73 | same order of magnitude; same direction of all trends |

**Qualitative trends reproduced:**

- ✅ High-LET component (α+⁷Li surrogate) gives RBE > proton component > low-LET proton > photon.
- ✅ Eq. 6 accumulation produces a flatter (more shoulderless) SF curve dominated by α-term when the boron share is large — matches Fig. 7.
- ✅ Methodology (LQ fit per component, then Eq. 6) is straightforward to replicate from the paper text.

**Trends NOT reproducible without the unreleased data:**

- ❌ The exact BPA-vs-BSH ordering and the BSH boron-dose RBE of 0.73 (which is <1, because BSH cannot enter the cell and most α+⁷Li never reach the nucleus). This depends on `F_α,BSH = 0.29`, `F_Li,BSH = 0`, `W_α,BSH,c = 0.42`, `W_α,BSH,e = 0.58` — none of which are derivable analytically; they come from TOPAS-nBio MC.
- ❌ Synergistic-effects panel (Fig. 8) requires the BNCT-extended MEDRAS-MC pipeline.

## 6. Compute footprint

- **Local (CherryRd):** smoke script ran in ~2 s, ~50 MB RAM, single thread, no GPU. Within LUCID100 "no heavy compute on CherryRd" rules. ✅
- **Heavy compute (NOT run):** Geant4-DNA + TOPAS-nBio + MEDRAS-MC pipeline. See README §"Heavy-compute job plan" for the recommended target (uicgpu or chiatta00; both have plenty of CPU; Geant4-DNA does not need GPUs).

## 7. QA retag recommendation (`LUCID100_SOLID_MASTER_QA.tsv`)

```
slot 42 (Wave 5 / A14)  →  partial_reduced_analytic
note: PARTIAL — paper PDF + public MEDRAS analytic code harvested;
      reduced analytic smoke check reproduces methodology (LQ fits +
      Eq. 6) and qualitative RBE ordering; exact Table 1 reproduction
      blocked on authors' unreleased Geant4-DNA radial-deposition
      tables, TOPAS-nBio F/W microdistribution factors, and the
      BNCT extension of MEDRAS-MC. No data/code availability statement
      in the paper, no supplement, no Zenodo. KEEP.
```

## 8. Next actions if escalated

1. Provision Geant4-DNA + TOPAS-nBio on **uicgpu** (no queue, plenty of CPU/RAM) or **chiatta00** (CPU-only path is fine).
2. Regenerate the radial-deposition tables and F/W dose factors per §2.3.1–2.3.3.
3. Optional: request MEDRAS-MC from the McMahon group (Stephen McMahon is acknowledged in the paper). Per LUCID100 rules, no author contact at this stage.
4. Re-run the analytic pipeline (already in `medras_bnct_smoke.py`) with the regenerated per-particle-energy SF curves; compare numerically to Table 1 entries.

## 9. Files produced

- `README.md`
- `PROGRESS.md`
- `REPORT.md` (this file; also serves as the `FIRST_PASS_REPORT`)
- `ARTIFACT_MANIFEST.md`
- `refs/paper.pdf`
- `artifacts/medras_analytic/` (cloned)
- `artifacts/smoke_output.txt`
- `scripts/medras_bnct_smoke.py`
- `~/.openclaw/workspace/memory/subagent-progress/lucid100-slot42-mp17446.json`


---

## Audit Note (2026-06-20)

Independently re-scored on 2026-06-20 by a 3-judge LLM panel (argo:gpt-5, argo:gemini-2.5-pro, argo:claude-opus-4.6) per AUDIT_PROTOCOL.md (median Coverage/Agreement, majority verdict, ties → most conservative).

| Judge | Verdict | Coverage | Agreement | Note (≤200 chars) |
|---|---|---:|---:|---|
| `claude-opus-4.6` | PARTIAL | 3 | 4 | Smoke check reproduces LQ+Eq6 methodology and qualitative RBE ordering using public MEDRAS analytic code with surrogate LET values. Exact Table 1 reproduction blocked: authors' Geant4-DNA radial ta... |
| `gpt-5` | SPOT-CHECK | 3 | 3 | Only analytic MEDRAS mixing reproduced; no Geant4-DNA/TOPAS-nBio BNCT microdistribution factors; Table 1 RBEs not matched; qualitative ordering OK. Tools exist but weren’t run; numeric replication ... |
| `gemini-2.5-pro` | PARTIAL | 3 | 2 | Reduced analytic check confirms the paper's final calculation method. Full replication is blocked by missing author-provided MC simulation data, preventing verification of key quantitative claims. |

**Aggregated audit verdict:** **PARTIAL** (median Coverage = 3/10, Agreement = 3/10). This is an external audit overlay; the replicator's self-scored verdict above is preserved unchanged. Audit identified this as a thin / coverage-limited report (median Coverage ≤4 or at least one SPOT-CHECK call). Suggested follow-ups: see the report's own next-actions / blockers section.

## Open Questions & Reproducibility Blockers

- Primary blocker: the paper's **Geant4-DNA radial-deposition tables `E(r)` for each ion energy** (α at 0.2, 0.4, …, 1.47, 1.78 MeV; ⁷Li at 0.2, 0.4, 0.6, 0.84, 1.02 MeV; recoil protons over 0.001–1 MeV in the 200 µm × 22 µm water phantom; EDSB = 56.5 keV). These are referenced as inputs to Step A but never released — no Wiley supplement, no Zenodo, no GitHub deposit by the Yu/Geng/Tang group. Without them the per-particle DSB induction profile cannot be regenerated except by re-running Geant4-DNA from scratch.
- Secondary blocker: the **TOPAS-nBio F-factor and W-factor matrices** (`F_α,BPA`, `F_Li,BPA`, `F_α,BSH = 0.29`, `F_Li,BSH = 0`, plus the per-source-location W tensor for α and ⁷Li at nucleus/cytoplasm/membrane/extracellular). These set the BPA-vs-BSH split (paper Table 1: BPA total RBE₀.₀₁ = 2.50 vs BSH total = 2.15) and the sub-1 BSH-boron RBE of 0.73. Not provided; would require a full TOPAS-nBio re-run of the 3×3×3 cell-grid microdosimetry per drug distribution.
- Tertiary blocker: the **BNCT extension of MEDRAS-MC** that wires the Geant4-DNA + TOPAS-nBio outputs into the MEDRAS two-step repair model. The public `sjmcmahon/MEDRAS` repo ships the analytic LQ + Eq. 6 stack but NOT the BNCT-specific Monte Carlo extension. No release link in the paper, no code/data availability statement.
- Open question: would running the public MEDRAS-MC (without the BNCT extension) on author-published SDD files for proton + α tracks at matching LET give the same proton-component RBE₀.₀₁ ≈ 3.21 the paper reports, or does the missing BNCT extension change the misrepair-classification step in a non-trivial way?
- Open question (next-pass-able on uicgpu/chiatta00 CPU): does the qualitative RBE ordering (high-LET α+⁷Li > proton component > low-LET proton > photon) survive when the analytic surrogate is replaced with a real Geant4-DNA-driven track-structure simulation, and at what LET threshold does the BSH RBE drop below 1?

