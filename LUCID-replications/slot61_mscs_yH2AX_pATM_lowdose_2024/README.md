# Slot 61 (Wave 7) — LUCID100 replication scoping

**Paper:** Chigasova A.K., Pustovalova M.V., Osipov A.A., Korneva S.A., Eremin P.S., Yashkina E.I., Ignatov M.A., Fedotov Yu.A., Vorobyeva N.Yu., Osipov A.N. *Post-Radiation Changes in The Number of Phosphorylated H2AX and ATM Protein Foci in Low Dose X-Ray Irradiated Human Mesenchymal Stem Cells.* Medical Radiology and Radiation Safety. 2024;69(1):15–19. (Published in Russian, with parallel English abstract.)

**DOI:** [10.33266/1024-6177-2024-69-1-15-19](https://doi.org/10.33266/1024-6177-2024-69-1-15-19)
**PDF source (open access, journal-hosted):** https://medradiol.fmbafmbc.ru/journal_medradiol/abstracts/2024/1/15-19.pdf
**Journal landing (English abstract):** https://medradiol.fmbafmbc.ru/en/vypuski/12-issues_journals/1671-15-19_osipov_eng
**Funding:** Russian Science Foundation grant 23-14-00078.
**Citation count (Semantic Scholar at curation time):** 0.

## Master QA context
- `LUCID100_SOLID_MASTER_QA.tsv` row: **rank=92, Wave 7, tier B, priority_score=13**, status `candidate_curated`.
- The user task references this entry as "slot 61"; the underlying master row is rank 92 — same DOI, same paper.
- Master worktype tag: `simulation/model replication`.
- **Worktype retag (this folder):** `wet-lab radiobiology assay — γH2AX/pATM immunocytochemistry kinetics in primary human MSC after low-dose X-ray; no model, no code, no equations`. See `WORKTYPE_RETAG.md`.

## What kind of paper this is
A 5-page short communication. Primary human adipose-derived MSC (passage 5–6, BioloT collection) irradiated on a RUB RUST-M1 X-ray rig (100 kVp, 0.8 mA, 1.5 mm Al, dose rate 40 mGy/min, 4 °C) at **40, 80, 160, 250 mGy**. Cells fixed at **1, 4, 6, 24, 48 h** post-IR (time points inferred from Figure 1 + narrative — see `FIRST_PASS_REPORT.md`). γH2AX (rabbit mAb, Merck) and pATM-Ser1981 (mouse mAb, Merck) immunocytochemistry with Alexa Fluor 488 / 555 secondaries; DAPI counterstain; ProLong Gold mountant. Imaged on Nikon Eclipse Ni-U + ProgRes MFcool, **manual focus counts on ≥200 cells per condition**, three independent experiments, mean ± SEM, Student's t-test in Statistica 8.0.

## What the paper reports
- Foci counts per nucleus for γH2AX, pATM, and their colocalization, plotted as kinetic curves (Fig. 1) over 1–48 h for the four doses.
- High doses (160, 250 mGy): γH2AX foci drop ~50–60 % by 6 h; colocalization with pATM ~80 % at 1 h (250 mGy), declining to 45–60 % by 24–48 h.
- Low doses (40, 80 mGy): no statistically significant γH2AX drop at 6 h; γH2AX remains elevated through 48 h; pATM colocalization 65 % at 1 h, falling to 35–40 % at 24–48 h.
- Verbal conclusion: maintenance of γH2AX at 24–48 h after low-dose IR is **ATM-independent** — authors hypothesize ATR-driven phosphorylation triggered by replicative stress from low-dose-stimulated proliferation + ROS-driven secondary DSBs.

## Data / code availability
**None.** No tables, no supplementary file, no Zenodo/GitHub link, no data-availability statement. All quantitative data lives in Fig. 1 (4 panels — one per dose).

## Replication path (what this folder contains)
This is a **wet-lab assay paper**, not a model. A like-for-like replication would require a primary MSC culture, an X-ray rig, ICC, manual focus counting, and an FTE for the assay work — out of scope for a desk replication.

The feasible desk-side replication is **figure-digitization + qualitative-claim verification**:
1. Harvest the PDF and extract Figure 1 as a raster image (done — `artifacts/fig-000.png`).
2. Manually digitize the four sub-panels with WebPlotDigitizer (or equivalent) to recover (dose × time × marker) → foci/nucleus and % colocalization. **Not done in this pass** — image-vision tooling and a digitizer GUI are not available in this environment; this is the single blocker for full numeric replication.
3. Re-encode the narrative numerical claims in a structured table and check internal consistency (e.g., 250 mGy γH2AX drops to ~50 % of 1 h max by 6 h; 160 mGy drops to ~60 % at 6 h; 40 & 80 mGy show no significant 6 h drop; pATM colocalization fractions at 1 h vs 24–48 h). **Done** — see `scripts/smoke_replicate.py`.
4. Produce the qualitative replot from those narrative anchor points so the figure shape can be visually compared to Fig. 1 once digitization is done. **Done** — `scripts/smoke_replicate.py` produces `outputs/fig1_qualitative_replication.png`.

## Files in this folder
- `README.md` — this file
- `WORKTYPE_RETAG.md` — recommended master-QA retag
- `PROGRESS.md` — log of work performed
- `MANIFEST.md` — artifact manifest with sha256 hashes
- `FIRST_PASS_REPORT.md` — verdict + detailed findings
- `artifacts/` — `paper.pdf`, `paper.txt`, `fig-000.png` (Figure 1 raster)
- `scripts/smoke_replicate.py` — minimal qualitative-claim consistency check + replot
- `outputs/` — generated plots/tables from the smoke script (created on run)

## How to run the smoke script
```bash
cd /Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/slot61_mscs_yH2AX_pATM_lowdose_2024
python3 scripts/smoke_replicate.py
```
No heavy compute. Pure Python + matplotlib + numpy. Runs on CherryRd in seconds.

## Related Osipov-group work (for cross-calibration of digitized values)
- Pustovalova et al. 2019 — γH2AX/pATM in MSC under continuous low-dose-rate γ (0.1 mGy/min). PMC6600277. Open access.
- Belov, Chigasova, Pustovalova et al. 2023 — *Curr. Issues Mol. Biol.* 45(9):7352-73 — dose-dependent HR/NHEJ shift, empirical + simulation. doi:10.3390/cimb45090465. Open access.
- Osipov et al. 2024 — *Cells* 12(8):1209 — residual foci, senescence, autophagy in X-ray fibroblasts. doi:10.3390/cells12081209.
- Osipov, Pustovalova, Grekhova et al. 2015 — *Oncotarget* 6(29):27275 — prior 5 min–4 h kinetics in gingival MSC, ATM-independent low-dose persistence. doi:10.18632/oncotarget.4739.
- Grekhova et al. 2015 — Radiats. Biol. Radioekol. 55(4):395–401 — slow γH2AX kinetics in human skin fibroblasts at low dose.

These are the same authors' adjacent datasets — useful sanity anchors once Fig. 1 is digitized.
