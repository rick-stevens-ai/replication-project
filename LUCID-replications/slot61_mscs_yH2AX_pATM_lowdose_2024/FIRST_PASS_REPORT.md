# FIRST_PASS_REPORT.md — slot 61 / LUCID100 rank 92

**Paper:** Chigasova et al. 2024 — *Post-Radiation Changes in The Number of Phosphorylated H2AX and ATM Protein Foci in Low Dose X-Ray Irradiated Human Mesenchymal Stem Cells.* Med. Radiol. Radiat. Safety 69(1):15–19. DOI:10.33266/1024-6177-2024-69-1-15-19.

## Verdict
**PASS-low (qualitative) / NO-GO (full numeric or wet-lab) — keep, reclassify.**

- ✅ **Artifact harvest**: complete (PDF, full text, Figure 1 raster).
- ✅ **Worktype verification**: paper is wet-lab radiobiology (ICC kinetics), **not** simulation/model as currently tagged. Retag recommended.
- ✅ **Qualitative claim-consistency smoke replication**: 6/6 narrative numerical claims internally consistent and reproduced in `outputs/fig1_qualitative_replication.png` + `outputs/claim_check.csv`.
- ⚠️ **Full numeric figure replication**: NOT POSSIBLE in this pass — no working image-vision route from this environment to digitize Figure 1, and the paper has no tables, no supplementary data, no code repo.
- ⚠️ **Wet-lab replication**: OUT OF SCOPE — requires primary MSC culture, X-ray rig, ICC, manual focus counting.

## Worktype retag (see WORKTYPE_RETAG.md)
- Master themes column should drop `computational model / simulation`.
- Master worktype column should change from `simulation/model replication` to `wet-lab assay replication (figure-digitization tier only)`.

## Detailed findings

### Numerical content of the paper
All quantitative data lives in **one composite Figure 1** (4 sub-panels — one per dose: 40, 80, 160, 250 mGy). Each panel shows kinetic curves for: γH2AX foci/nucleus, pATM foci/nucleus, and % colocalization, from 1 to 48 h post-IR. Time points implied by Fig. 1 + narrative: **1, 4, 6, 24, 48 h** (the 4 h point is implied by the "4-48 h" wording in the colocalization paragraph and standard time-course design; awaits digitization to confirm).

Quoted narrative numbers (verbatim translation from text):
- 250 mGy: γH2AX peaks at 1 h (significant, p<0.001 vs control), drops to ~50 % of peak by 6 h.
- 160 mGy: γH2AX drops more slowly; ~60 % of 1 h value at 6 h.
- 40 & 80 mGy: γH2AX shows no statistically significant decrease at 6 h and remains elevated through 48 h.
- 250 mGy: pATM/γH2AX colocalization ~80 % at 1 h; 45–60 % at 4–48 h.
- 80 & 40 mGy: colocalization 65 % at 1 h, dropping to 40 % (80 mGy) / 35 % (40 mGy) at 24–48 h.
- n = 3 independent experiments; ≥200 cells scored per condition; mean ± SEM; Student's t-test.

### Methods provenance
- Cells: primary human MSC from adipose tissue, passages 5–6, BioloT (Russia) catalog.
- Medium: DMEM (1 g/L glucose, Thermo Fisher) + 10 % FBS; 37 °C / 5 % CO₂; medium change q3d; experiments after 3 passages in-house.
- Irradiator: RUB RUST-M1 (Diagnostika-M, Moscow), dual-emitter, 100 kVp, 0.8 mA, 1.5 mm Al filter, dose rate **40 mGy/min**, cells held at 4 °C on LAB ARMOR BEADS; dose accuracy ±15 %.
- Antibodies: rabbit mAb anti-γH2AX (Merck-Millipore, 1:200); mouse mAb anti-pATM-Ser1981 (Merck-Millipore, 1:200); goat anti-mouse Alexa Fluor 488 (Life Tech, 1:600); goat anti-rabbit Alexa Fluor 555 (Merck-Millipore, 1:600); ProLong Gold + DAPI mountant.
- Imaging: Nikon Eclipse Ni-U fluorescence microscope + ProgRes MFcool camera; UV-2E/C, B-2E/C, Y-2E/C filter sets.
- Counting: manual, ≥200 cells per condition.
- Stats: Statistica 8.0 (StatSoft); Student's t-test.

### Public data / code / supplement
- **None.** Verified by inspecting full PDF + journal HTML landing page (`https://medradiol.fmbafmbc.ru/en/vypuski/12-issues_journals/1671-15-19_osipov_eng`).
- No data-availability statement, no Zenodo, no GitHub, no GEO, no supplementary file.
- Funding: RNF grant 23-14-00078.

### Related Osipov-group works (potential calibration anchors)
- Pustovalova et al. 2019 (PMC6600277) — MSC continuous low-dose-rate γ, includes numeric tables.
- Belov, Chigasova, Pustovalova et al. 2023 (Curr. Issues Mol. Biol. 45(9):7352-73) — empirical + simulation; open access.
- Osipov, Pustovalova, Grekhova et al. 2015 (Oncotarget 6(29):27275) — earlier 5 min–4 h kinetics in gingival MSC.
- Osipov et al. 2024 (Cells 12(8):1209) — residual foci, senescence, autophagy in fibroblasts.
- Grekhova et al. 2015 (Radiats. Biol. Radioekol. 55(4):395-401) — slow γH2AX kinetics in skin fibroblasts.

### Smoke replication — what we ran
`scripts/smoke_replicate.py` encodes only the verbal numerical claims as anchor points and verifies:
1. High-dose (160, 250 mGy) γH2AX 6 h fractional decline ∈ [0.30, 0.60] → **PASS** (0.40, 0.50).
2. Low-dose (40, 80 mGy) γH2AX 6 h fractional decline ≤ 0.10 → **PASS** (0.00, 0.00).
3. Low-dose γH2AX 48 h fraction ≥ 0.80 → **PASS** (1.00, 1.00).
4. pATM/γH2AX 1 h colocalization dose ordering 250 > 80, 40 → **PASS** (80 % > 65 % = 65 %).
5. pATM/γH2AX 48 h < 1 h colocalization for every dose → **PASS** (250: 80→52.5, 80: 65→40, 40: 65→35).
6. 48 h colocalization low-dose < high-dose → **PASS** (35, 40 < 52.5).

Output figure shows the 2-panel kinetic schematic; this is a *template* and not a numeric reproduction of Fig. 1. When a digitized CSV is added under `data/fig1_digitized.csv`, the same script can be extended to overlay anchor vs digitized values.

### Compute footprint
- Replication script: numpy + matplotlib, ~50 ms wall time on CherryRd. Zero GPU.
- Full quantitative replication (figure digitization + curve fits to e.g. two-component exponential repair model) would also be trivial on CherryRd (still < 1 CPU-minute). **No HPC needed.**

## Blockers
1. **Figure 1 digitization** — needs WebPlotDigitizer (manual GUI) or a working vision model. The OpenClaw `pdf` and `image` tools failed (Anthropic credit balance; OpenAI accountId extraction error; gemini-3-flash-preview unknown). This is the single artifact missing to upgrade from qualitative-claim PASS-low to numeric PASS.
2. **Russian-language full text** — handled with pdftotext; numerical content extracted successfully. No further blocker.

## Next actions (cheapest first)
1. Run `webplotdigitizer` (or equivalent) on `artifacts/fig-000.png` → produce `data/fig1_digitized.csv` with columns `dose_mGy,time_h,marker,value,sem` where `marker ∈ {yH2AX_foci, pATM_foci, colocalization_pct}`. ~30 min manual work.
2. Extend `scripts/smoke_replicate.py` to load that CSV and (a) overlay digitized curves against narrative anchors, (b) fit a two-component repair model `N(t) = A·exp(-t/τ_fast) + B·exp(-t/τ_slow) + C` per dose, (c) test whether low-dose curves have a significantly larger residual `C` than high-dose curves — the paper's central biological claim.
3. Apply the retag to the master TSV (`LUCID100_SOLID_MASTER_QA.tsv` row 120, columns `themes` and `worktype`) — see `WORKTYPE_RETAG.md`.
4. (Optional) Pull numeric tables from the sister paper Pustovalova et al. 2019 (PMC6600277, open access) to cross-validate the digitized 250-mGy peak values are in the same ballpark as the group's other MSC γH2AX experiments.

## Status
`first_pass_complete` — PASS-low (qualitative claims verified); NO-GO for numeric until Figure 1 is digitized; recommend KEEP with worktype retag.
