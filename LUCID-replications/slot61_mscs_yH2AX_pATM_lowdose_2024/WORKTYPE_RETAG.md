# Worktype retag recommendation — slot 61 / master rank 92

| Field | Master value (LUCID100_SOLID_MASTER_QA.tsv row 120) | Recommended |
|---|---|---|
| themes | DNA repair / DDR; dose-rate / low-dose response; computational model / simulation | DNA repair / DDR; dose-rate / low-dose response; **wet-lab radiobiology / immunocytochemistry / foci kinetics** |
| worktype | simulation/model replication | **wet-lab assay (DSB foci ICC) — radiobiology** |
| verdict_or_plan | TODO: simulation/model replication; artifact harvest; brief; run; report | first_pass_complete: NO-GO for full numeric replication without figure digitization tool; PASS-low on qualitative claim consistency; wet-lab replication out of scope |
| qa_decision | KEEP: relevant and replication-plausible | **KEEP**, but reclassify as wet-lab; replication-plausible only at the figure-digitization + replot tier |

## Rationale
The paper has zero mathematical model, zero equations, zero simulation, zero code. It is a kinetic immunocytochemistry assay measuring two phosphoprotein foci markers (γH2AX, pATM) and their colocalization in primary human MSCs at four low-dose X-ray exposures across five time points (1–48 h). All data is reported as plotted curves in a single composite Figure 1. The earlier `computational model / simulation` theme tag appears to have been propagated from the adjacent Belov/Pustovalova 2023 *Curr. Issues Mol. Biol.* paper (which IS a hybrid empirical+simulation work), but this 2024 short-communication is purely empirical.

## Suggested edit to master TSV (single cell, row 120, column `themes`)
Replace:
```
DNA repair / DDR; dose-rate / low-dose response; computational model / simulation
```
with:
```
DNA repair / DDR; dose-rate / low-dose response; wet-lab radiobiology / γH2AX-pATM foci ICC
```
and column `worktype`:
```
simulation/model replication
```
with:
```
wet-lab assay replication (figure-digitization tier only)
```
