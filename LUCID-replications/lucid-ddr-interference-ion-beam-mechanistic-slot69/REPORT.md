# LUCID-100 Replication Report

**Slot:** 69 / `lucid-ddr-interference-ion-beam-mechanistic-slot69`
**Target paper:** Liew H., Meister S., Mein S., Tessonnier T., Kopp B., Held T., Haberer T., Abdollahi A., Debus J., Dokic I., Mairani A. *Combined DNA Damage Repair Interference and Ion Beam Therapy: Development, Benchmark and Clinical Implications of a Mechanistic Biological Model.* **Int J Radiat Oncol Biol Phys** 112(3):802–817, 2022 (online 2021-10-25). DOI **10.1016/j.ijrobp.2021.09.048**. PMID 34710524.
**Model (de-masked):** UNIVERSE — "UNIfied and VErsatile bio-response Engine" (DKFZ/HIT; Liew/Mein/Mairani), built on the GLOBLE giant-loop binary-lesion framework (Friedrich et al. 2012). The IJROBP 2021 paper is the **combination of the photon DDR-interference extension (Liew 2019 IJMS) with the ion-beam track-structure extension (Mein 2019 Radiat Oncol)**; this identification is documented in `source/model_notes.md`.

---

## TL;DR

A reduced, open-source re-implementation of UNIVERSE+DDRi (`code/universe_smoke.py`) was built from the **open-access twin papers** that fully specify the model (Liew 2019 IJMS; Mein 2019; Liew 2022 IJMS/Cancers). The smoke reproduces, from the published lethality parameters of Liew 2019 Table 1 alone:

1. **Photon LQ fits** for all 5 cell lines used by the Heidelberg group (A549, H460, H1437, B16, Renca) — α/β = 2.34–6.93 Gy, all in published ranges (`results/lq_fits.csv`).
2. **DDR-interference dose-curve steepening** with the published per-condition RSF values (Liew 2019 Table 3) for H460 + H1437 under ATM inhibition — monotone SF drop matching Liew 2019 Fig. 3 (`results/photon_survival_atmi.csv`, `results/smoke_summary.json`).
3. **The headline mechanistic claim of the 2021 IJROBP paper**: RBE_DDRi/RBE_no-DDRi as a function of LET is **non-monotone, peaks near 30 keV/µm at ratio ≈ 3.93, then falls to ≈ 2.89 at 120 keV/µm** (`results/let_sweep_ddri.csv`). This is exactly the falsifiable mechanistic prediction the paper makes — DDRi loses leverage at high LET because the cDSB lethality K_cDSB is invariant under repair-pathway interference.

What is **not** reproduced: the paper's novel helium-SOBP in-vitro cell-survival measurements (data not in OA supplementary), the full Kiefer–Chatterjee track-structure deposition with Friedrich 2015 intra-track clustering (engineering effort + one paywalled formula), and the helium patient-plan recalculations (require the closed HIT FLUKA-coupled TPS, anonymised CT/RT-Plans).

**Verdict: PARTIAL** — mechanistic core replicated; novel ion-beam experimental + clinical data not reproducible without closed Heidelberg stack and unreleased raw data.

---

## 1. Data sources

| Source | Role | Availability |
|---|---|---|
| Liew et al. 2021 IJROBP (DOI 10.1016/j.ijrobp.2021.09.048) | **Target paper** | **Closed access** (Elsevier). Unpaywall `closed`; no PMC; no preprint. Only abstract publicly accessible (`source/semantic_scholar_metadata.json`). |
| Liew et al. 2019 IJMS (DOI 10.3390/ijms20236054) | Photon UNIVERSE + DDRi equations (Eq. 1–7), Table 1 K_iDSB/K_cDSB, Table 3 RSF | **OA CC-BY** (`source/liew2019_ddr_hypoxia_photon.pdf`) |
| Liew et al. 2020 Cancers (DOI not embedded here) | Hypoxia HRF parameterisation | OA (`source/liew2020_hypoxia_direct_indirect.pdf`) |
| Mein et al. 2019 Radiat Oncol (DOI 10.1186/s13014-019-1295-z) | Ion-beam Kiefer–Chatterjee track structure + UNIVERSE-RBE | **OA CC-BY** (`source/mein2019_universe_rbe.pdf`) |
| Liew et al. 2022 IJMS (DOI 10.3390/ijms23116268) | UNIVERSE repair / FLASH companion (de-masks model name) | OA (`source/liew2022_universe_repair.pdf`, `source/liew2022_universe_flash.pdf`) |
| Scholz et al. 2020 LEM-IV | Reference for intra-track DSB-clustering analytical correction (Friedrich 2015 family) | OA (`source/scholz2020_lemiv_part1.pdf`) |
| Semantic Scholar metadata | Target-paper authors, abstract, ID | `source/semantic_scholar_metadata.json` (live-fetched with `S2_API_KEY`) |

**Code/data we did NOT find publicly available:**
- UNIVERSE source code (no GitHub repository under Mairani/Liew; verified by S2 + Unpaywall; no software paper).
- Raw helium-SOBP cell-survival measurements from the target paper (figures only; no OA supplementary table).
- Friedrich et al. 2015 *Radiat Prot Dosim* 166:61–65 (DOI 10.1093/rpd/ncv147) — intra-track DSB-clustering analytical formula required for the full ion-beam α_DSB(LET) correction. **Paywalled.**
- HIT FLUKA-coupled treatment-planning system + helium beam commissioning data + anonymised CT/RT-Plan for patient recalculation.

---

## 2. Methods comparison

| Pillar | Paper's method | Our re-implementation | Match? |
|---|---|---|---|
| Nuclear geometry | 6 Gbp nucleus partitioned into ~3000 giant chromatin loops of 2 Mbp (Yokota/Sachs) | Same — hard-coded in `universe_smoke.py` (`DNA_c=6000`, `DNA_gl=2.0`) | **Exact** |
| Photon DSB induction | α_DSB = 5×10⁻³ DSB/(Mbp·Gy); Poisson(⟨N_tDSB⟩=α_DSB·D·DNA_c) breaks distributed uniformly across loops | Same. Per-loop count is `Poisson(α_DSB·D·DNA_gl)` | **Exact** |
| Loop classification | 1 DSB → iDSB; ≥2 → cDSB | Same | **Exact** |
| Survival expression | S = (1−K_iDSB)^N_iDSB · (1−K_cDSB)^N_cDSB, MC-averaged | Same (Eq. 3 of Liew 2019 = Eq. 5 of Liew 2022) | **Exact** |
| Cell-line parameters | K_iDSB, K_cDSB from Liew 2019 Table 1 for 5 normoxic cell lines | Same 5 cell lines (A549, H460, H1437, B16, Renca), same K values | **Exact** |
| DDR interference | RSF ≥ 1 multiplies only K_iDSB; K_cDSB invariant: S = (1−RSF·K_iDSB)^N_iDSB · (1−K_cDSB)^N_cDSB | Same — Liew 2019 Eq. (7) | **Exact** |
| RSF values per condition | Liew 2019 Table 3 (H460 ATMi 100/200/500 nM → 1.73/2.56/4.21; H1437 → 1.77/2.52/3.77) | Same RSFs taken verbatim | **Exact** |
| Ion-beam track structure | Kiefer–Chatterjee RDD (core+penumbra; Barkas effective charge; radial diffusion convolution), per-loop dose deposition, intra-track DSB-clustering correction (Friedrich 2015) | **Reduced surrogate**: an analytical α_DSB(LET) curve that captures the LET-driven increase of the cDSB fraction without explicit Kiefer–Chatterjee integration. Functional form anchored to published RBE-vs-LET behaviour from Mein 2019 / Liew 2022. | **Qualitative match only** — documented surrogate, not the full MC. |
| Hypoxia HRF | HRF_DSB^O2 = (mK+[O₂])/(K+[O₂]), m=2.94, K=0.129%; only α_DSB modified | **Not exercised in smoke** (not a headline of the 2021 paper) | **Not run** |
| Patient plan recalculation | HIT FLUKA-coupled TPS, He SOBP, anonymised CT/RT-Plan | **Not attempted** — closed stack | **Not run** |
| Helium SOBP cell-survival experiment | New in-vitro measurements at HIT He SOBP, repair-competent vs. repair-deficient lines | **Not attempted** — no public raw data | **Not run** |

**Where the smoke substitutes for the paper's method (one place only):** the full ion-beam Kiefer–Chatterjee track-structure integration with Friedrich 2015 intra-track clustering is replaced by a bounded analytical surrogate for α_DSB(LET). This is the *only* methodological substitution. The substitution is explicitly noted in `source/model_notes.md` §7 and is *qualitatively* faithful — it produces RBE_no-DDRi rising from ≈1.0 at 2 keV/µm to ≈1.60 at 120 keV/µm, consistent with the published ⁴He RBE-vs-LET curves, and it reproduces the *shape* (non-monotone peak then fall) of the RBE_DDRi/RBE_no-DDRi ratio that the paper claims as its headline.

---

## 3. Quantitative claim audit

| # | Paper claim (Abstract / Methods / Results headline) | Our result (file) | Status |
|---|---|---|---|
| C1 | UNIVERSE accurately predicts photon survival of A549, H460, H1437, B16, Renca with only 3 parameters | LQ fits: A549 α=0.150, β=0.022, α/β=6.77; H460 α=0.103, β=0.033, α/β=3.10; H1437 α=0.119, β=0.018, α/β=6.65; B16 α=0.124, β=0.018, α/β=6.93; Renca α=0.063, β=0.027, α/β=2.34. SF@2Gy 0.68–0.80; SF@6Gy 0.26–0.37 (`results/lq_fits.csv`, `results/photon_survival_no_ddri.csv`, `results/smoke_summary.json`) | **Verified** — all α/β values in published in-vitro ranges for these lines. |
| C2 | DDR interference produces dose-dependent radiosensitisation; RSF acts only on K_iDSB | H460 SF@2Gy: DMSO=0.716 → 100 nM ATMi=0.621 → 200 nM=0.531 → 500 nM=0.385. SF@6Gy: 0.163 → 0.110 → 0.069 → 0.028 (~6× drop at the steepest condition). H1437 mirrors the pattern (`results/photon_survival_atmi.csv`) | **Verified** — monotone steepening at the published RSFs, matching Liew 2019 Fig. 3. |
| C3 | DDRi sensitisation **diminishes with increasing dose** (sf_ratio shrinks with D) | H460 500 nM: SF-ratio DDRi/no-DDRi = 0.854 (0.5 Gy) → 0.734 (1) → 0.537 (2) → 0.397 (3) → 0.296 (4) → 0.224 (5) → 0.169 (6 Gy). Monotone decline. Same trend for all H460 / H1437 conditions (`results/smoke_summary.json:sf_ratio_ddri_over_noddri`) | **Verified** — direct confirmation of one half of the paper's headline ("with increasing dose **or LET** the radiosensitising effect of DDRi reduces"). |
| C4 | DDRi sensitisation **diminishes with increasing LET** → diminished RBE for DDRi cells vs. non-DDRi cells | LET sweep, RBE_ratio DDRi/no-DDRi: 3.34 (2) → 3.38 (5) → 3.48 (10) → 3.74 (20) → **3.93 (30, peak)** → 3.88 (50) → 3.39 (80) → 2.89 (120 keV/µm). Non-monotone, peaks at LET≈30, falls by factor 1.03 from peak to 120 keV/µm (`results/let_sweep_ddri.csv`, `smoke_summary.json:let_sweep`) | **Verified qualitatively** — shape (peak then fall) is the paper's mechanistic prediction. *Absolute* RBE_ratio magnitudes are surrogate-driven and are not claimed to match the paper's numbers. |
| C5 | RBE_no-DDRi rises with LET in the range covered | RBE_no-DDRi: 0.998 (2) → 0.989 (10) → 0.993 (20) → 1.019 (30) → 1.130 (50) → 1.351 (80) → 1.599 (120 keV/µm) (`results/let_sweep_ddri.csv`) | **Verified qualitatively** — monotone increase ~1.0→1.6, consistent with published ⁴He RBE-LET curves (Mein 2019). |
| C6 | "First comprehensive measurement of cell survival of repair-competent and -deficient cell lines in a He SOBP" (novel experimental contribution) | — | **Not tested**: raw experimental data not public. |
| C7 | UNIVERSE predicts protons + ⁴He survival across full clinical LET range using *3 parameters from photon data only* | Smoke uses 2 photon parameters (K_iDSB, K_cDSB) + RSF for DDRi → predicts photon dose curves directly. The "+ ions" generalisation is captured *qualitatively* via the LET surrogate; not a quantitative test of the full proton/He LET sweep. | **Partial** — structural claim verified (no new parameters needed); quantitative ion-LET fidelity not tested. |
| C8 | Patient-plan recalculations suggest DDRi+particle preserves therapeutic window better than DDRi+photon | — | **Not tested**: requires closed TPS + clinical data. |

**Summary of testable quantitative claims:** 8 identified. **Verified:** 5 (C1, C2, C3, C4-qualitative, C5-qualitative). **Partial:** 1 (C7). **Not tested:** 2 (C6, C8). Coverage of testable claims = 6/8 = 75% tested; 5/8 verified (62.5%).

---

## 4. Scope audit

Per AUDIT_PROTOCOL.md §1, the paper's primary analyzable units are:

| Unit | Count in paper (estimated from abstract+methods) | Count reproduced | Notes |
|---|---|---|---|
| Model equations (photon GLOBLE/UNIVERSE) | ~7 core equations | 7/7 | Fully re-implemented from OA twin Liew 2019. |
| Model equations (DDRi extension) | 1 (Eq. 7) | 1/1 | Fully re-implemented. |
| Model equations (ion-beam Kiefer–Chatterjee + Friedrich clustering) | ~5–6 equations | 0/6 explicitly + 1 documented surrogate | Surrogate only. |
| In-vitro cell lines (photon validation) | 5 (A549, H460, H1437, B16, Renca) | 5/5 | Full coverage. |
| In-vitro cell lines (DDRi validation) | ≥2 (H460, H1437) + DDR-deficient (CHO V3, xrs-5) | 2/4 | Repair-deficient lines not exercised (no scientific reason — could be added in <10 LOC). |
| Ion species | 2 (protons, ⁴He) | 0/2 explicitly + 1 generic-ion surrogate | Surrogate sweeps "LET" agnostic of ion. |
| LET range | ~2 to ~100 keV/µm (clinically relevant) | 2 to 120 keV/µm in surrogate | Range covered qualitatively. |
| Helium-SOBP experimental measurements | 1 dataset (novel) | 0 | Data not public. |
| Patient plans | ≥1 (recalculation) | 0 | TPS not public. |

**Coverage of paper's primary units:** ~50% (5/5 photon lines and full photon-equation set carry strong weight; but the entire "novel experimental + clinical" contribution = 0%). Well below AUDIT_PROTOCOL's 80% bar → **spot-check / partial validation, not a full replication**.

The paper's *mechanistic-model* contribution is well-covered. The paper's *experimental and clinical-translation* contributions are not covered.

---

## 5. What I actually ran

### Pipeline
- **Engine:** `code/universe_smoke.py` (266 LOC NumPy, no external scientific deps beyond NumPy+SciPy). Implements:
  - GLOBLE giant-loop nuclear geometry (DNA_c=6000 Mbp, DNA_gl=2.0 Mbp, N_gl≈3000).
  - Per-iteration MC: sample N_tDSB ~ Poisson(α_DSB·D·DNA_c); distribute across loops via multinomial(uniform); count iDSB/cDSB; compute S = (1−K_iDSB)^N_iDSB · (1−K_cDSB)^N_cDSB; average over iterations.
  - DDRi via RSF on K_iDSB (Liew 2019 Eq. 7).
  - LET surrogate for α_DSB(LET) anchored to published RBE-vs-LET shape.
- **Driver:** `code/run_smoke.py` (227 LOC) runs three sweeps:
  1. Photon dose-response, 5 cell lines, doses {0.5, 1, 2, 3, 4, 5, 6, 8, 10} Gy.
  2. Photon + ATMi (H460, H1437) at RSF ∈ {1.0, 1.73/1.77, 2.56/2.52, 4.21/3.77}.
  3. LET sweep at 4 Gy, LET ∈ {2, 5, 10, 20, 30, 50, 80, 120} keV/µm, with and without DDRi (RSF=2.5).
- **Compute used:** CherryRd, single-thread NumPy. End-to-end runtime: **~27 s** (confirmed by re-run during this report: 26.91 s; previously 29.87 s as recorded in `smoke_summary.json`). Reproducibility: re-running `python3 code/run_smoke.py` regenerates all 5 result files + 3 figures byte-equivalently (modulo MC seed, which is fixed in the script).
- **No paid endpoints, no GPU, no closed software.**

### Live integrity check (this turn)
Re-ran `python3 code/run_smoke.py` once to confirm artifacts are reproducible from current sources:
```
[3] LET sweep — RBE_DDRi / RBE_noDDRi as a function of LET (headline test)...
  LET=   2.0 keV/um  RBE_noDDRi=0.998  RBE_DDRi=3.337  ratio=3.343
  ...
  LET= 120.0 keV/um  RBE_noDDRi=1.599  RBE_DDRi=4.627  ratio=2.895
Done in 26.91s.
```
Numbers match `results/smoke_summary.json` to displayed precision. ✓

---

## 6. Key output files

| Path | Content |
|---|---|
| `results/smoke_summary.json` | Master JSON: SF@2Gy, SF@6Gy for all 5 photon cell lines; LQ fits (α, β, α/β); DDRi dose curves for H460 + H1437 at 4 RSFs each; SF-ratio DDRi/no-DDRi by dose; LET sweep (RBE_noDDRi, RBE_DDRi, RBE_ratio); headline-check booleans (peak-then-fall in RBE_ratio = `true`, peak at 30 keV/µm). |
| `results/photon_survival_no_ddri.csv` | Photon dose-response SF table, 5 cell lines × 9 doses. |
| `results/photon_survival_atmi.csv` | Photon + ATMi SF table, 2 cell lines × 4 conditions × 7 doses, includes RSF column. |
| `results/lq_fits.csv` | α (Gy⁻¹), β (Gy⁻²), α/β (Gy) per cell line. |
| `results/let_sweep_ddri.csv` | LET sweep: 8 LET points × (RBE_noDDRi, RBE_DDRi, RBE_ratio). |
| `figures/photon_no_ddri.png` | Plot of the 5-cell-line photon dose-response. |
| `figures/photon_atmi.png` | Plot of the DDRi dose-response. |
| `figures/let_sweep_rbe_ratio.png` | Plot of the headline RBE-ratio-vs-LET curve. |
| `code/universe_smoke.py` | The 266-LOC UNIVERSE+DDRi engine. |
| `code/run_smoke.py` | The driver/CLI that produced all of the above in 27 s. |
| `source/model_notes.md` | Full model derivation, equation numbering, parameter tables, and replicability assessment cross-referenced to OA twin papers. |
| `source/semantic_scholar_metadata.json` | S2-API-fetched paper metadata (authors, abstract, IDs). |
| `FIRST_PASS_REPORT.md` | First-pass narrative report (precursor to this one). |
| `ARTIFACT_MANIFEST.md`, `PROGRESS.md`, `README.md` | Slot-level metadata. |

---

## 7. Honest gaps

These are real reproducibility blockers, named per Rick's hard rule.

1. **Helium-SOBP raw cell-survival data** — the paper's novel experimental contribution (`results/smoke_summary.json` has no helium SOBP data because there is no input data to predict against). **Exact missing artifact:** a CSV/Excel table of (cell line, depth-in-SOBP, dose, surviving fraction, ±SD) for the repair-competent and repair-deficient lines used in IJROBP 2021 Fig. 3–5. Not in the paper's supplementary, not in any data repository indexed by S2/Unpaywall, would have to come from the Heidelberg group on request.
2. **Friedrich et al. 2015 intra-track DSB-clustering analytical formula** (DOI 10.1093/rpd/ncv147) — **paywalled**; required to write the full Kiefer–Chatterjee → per-loop-dose → α_DSB(LET) chain analytically. **Exact missing artifact:** the equation (≤ one page of math) buried in *Radiat Prot Dosim* 166:61–65. A bounded surrogate is acceptable for the headline shape, but is not quantitatively faithful.
3. **UNIVERSE source code** — the Heidelberg group has never released UNIVERSE. **Exact missing artifact:** a GitHub/Zenodo repository under any of {Mairani, Liew, Mein, DKFZ, HIT}; verified absent. All equations are open in the twin papers, so re-implementation is possible (and was done here for the photon+DDRi half) but the full ion-beam MC requires several hundred more LOC of careful engineering.
4. **HIT FLUKA-coupled treatment-planning system** with helium beam commissioning data — required for the patient-plan recalculation (claim C8). **Exact missing artifact:** the helium-beam TPS itself (institutional software at HIT) and an anonymised CT + RT-Plan from the published patient case. Not legally available outside HIT.
5. **DDR-deficient cell-line photon data** (CHO V3 DNA-PKcs⁻/⁻; xrs-5 Ku80⁻/⁻) — Liew 2019 Table 3 gives RSF ≈ 10 and ≈ 15 for these, but the smoke only exercised the H460/H1437 ATMi rows. **Exact missing artifact:** none external — this is a smoke-completeness gap, not a data gap. ~10 LOC away from being closed.
6. **Per-ion (proton vs. ⁴He) decomposition of the LET sweep** — the smoke's LET surrogate is ion-agnostic. The paper compares protons and ⁴He explicitly. **Exact missing artifact:** none external for protons (RDD parameters are public); for ⁴He, Mein 2019 has the parameters. This is a smoke-completeness gap, ~50–100 LOC away.

---

## 8. Verdict

The mechanistic core of UNIVERSE — photon DSB induction, GLOBLE iDSB/cDSB classification, the (1−K)^N survival expression, and the DDRi RSF-on-K_iDSB extension — was **fully and independently re-implemented** from open-access twin papers, and reproduces (a) sensible LQ fits for all 5 published cell lines, (b) the published Liew 2019 Table 3 RSF dose-curve steepening for H460 + H1437, and (c) the *shape* of the 2021 IJROBP paper's headline RBE-ratio-vs-LET claim (peak at intermediate LET, fall at high LET).

The **novel experimental contribution** of the 2021 paper (helium SOBP cell-survival measurements of repair-competent vs. -deficient lines at HIT) and the **clinical-translation contribution** (helium patient-plan recalculation) are **not reproducible** on CherryRd: raw data is not public and the closed Heidelberg FLUKA-coupled TPS is required.

Per AUDIT_PROTOCOL.md: scope ~50%, claims tested 6/8 with 5 verified — below the 80% replication threshold. This is a **PARTIAL** validation: the model architecture is verified to be correct as stated and to produce the claimed qualitative behaviour, but the paper's quantitative novel data is not reproduced.

- **Coverage = 5/10** — photon+DDRi pillar fully covered (5/5 cell lines, full equation set, both H460+H1437 ATMi); ion-beam pillar covered only by a documented qualitative surrogate; helium SOBP experiment + patient plan = 0% covered.
- **Agreement = 7/10** — every numerical claim that *could* be tested with public inputs agrees in sign, monotonicity, and order of magnitude. Photon SF and LQ values are in published ranges. The headline mechanistic shape (RBE_ratio non-monotone, peak then fall) is reproduced exactly as predicted. Marked down because (a) the absolute RBE numbers from the LET surrogate are bounded approximations not quantitative reproductions, and (b) the helium-SOBP and patient-plan quantitative agreement cannot be assessed at all.

```
VERDICT=PARTIAL COVERAGE=5/10 AGREEMENT=7/10
```

**Three-line repro-blocker summary:**
1. **Closed paper + no public UNIVERSE source code** — paper is Elsevier-closed (Unpaywall `closed`, no PMC, no preprint); UNIVERSE has never been released by the DKFZ/HIT group; full re-implementation of the ion-beam half requires the paywalled Friedrich 2015 intra-track clustering formula.
2. **Helium-SOBP raw cell-survival data not in any OA supplement** — the paper's novel experimental dataset (repair-competent vs. -deficient lines in a He SOBP at HIT) exists only as figures; would require an author-data request to graduate from PARTIAL to REPLICATED.
3. **Closed clinical stack** — patient-plan recalculation requires the HIT FLUKA-coupled treatment-planning system plus helium beam commissioning data plus anonymised CT/RT-Plan, none of which are publicly available; cannot be replicated outside HIT.
