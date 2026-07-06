# LUCID Radiobiology Replications — Master Report Summary

Integrated into `REPLICATION_EVALUATION_REPORT.tex` on 2026-05-30 as Wave 6 (papers 67–76).

| # | Paper | Verdict | Coverage | Agreement | Source |
|---|---|---|---:|---:|---|
| 67 | Medras-MC DNA repair/survival | PARTIAL, mechanistic core replicated | 4 | 8 | `lucid-medras-mc/REPORT.md` |
| 68 | Li stochastic DNA fragments rejoining | REPLICATED | 9 | 8 | `lucid-stochastic-rejoining/REPORT.md` |
| 69 | Hu p53 DNA-damage-response | PARTIAL | 6 | 6 | `lucid-p53-repair/REPORT.md` |
| 70 | Cogno/Bauer/Durante lung fibrosis ABM/MC | PARTIAL | 5 | 6 | `lucid-lung-fibrosis-abm/REPORT.md` |
| 71 | Qi slow/fast NHEJ | REPLICATED pathway-level / partial full MC | 8 | 8 | `lucid-slow-fast-nhej/REPORT.md` |
| 72 | Matsuya integrated MK targeted/NTE | REPLICATED/PARTIAL | 10 | 7 | `lucid-matsuya-nte-integrated/REPORT.md` |
| 73 | PyFoci foci miscounting | PARTIAL | 6 | 7 | `lucid-pyfoci-miscounting/REPORT.md` |
| 74 | Herr GLOBLE photon cell killing | REPLICATED with data limitations | 8 | 9 | `lucid-globle-photon-cell-killing/REPORT.md` |
| 75 | UNIVERSE repair/dose-rate RBE | PARTIAL | 6 | 6 | `lucid-universe-repair-doserate-rbe/REPORT.md` |
| 76 | Kundrát PARTRAC analytical formulas | PARTIAL analytical-figure replication | 7 | 7 | `lucid-partrac-analytical-formulas/REPORT.md` |

## Cross-cutting finding
Compact mathematical radiobiology models and open code reproduced well; full Monte Carlo/track-structure workflows were blocked mainly by heavy TOPAS/Geant4 stacks, missing raw simulation outputs, or raw experimental overlays.

---

## Wave 7+8 — New LUCID replication reports (since 2026-06-09)

_Audited 2026-06-20 by Ollie subagent with 3-judge panel (argo:gpt-5, argo:gemini-2.5-pro, argo:claude-opus-4.6). Coverage/Agreement = median; verdict = majority (ties → most conservative)._

| # | Paper | Verdict | Coverage | Agreement | Source |
|---|---|---|---:|---:|---|
| 77 | Sangsuwan 2023 senescent fibroblasts oxidative stress + DNA repair LDR | PARTIAL | 5 | 7 | `LUCID-replications/lucid100-senescent-fibroblasts-oxidative-stress-dna-repair-ldrate/REPORT.md` |
| 78 | Yu/Geng/Tang 2024 BNCT MEDRAS extension (Med Phys) | PARTIAL | 3 | 3 | `LUCID-replications/lucid100-bnct-dna-damage-repair-model/REPORT.md` |
| 79 | Cantabella 2022 zebrafish brain chronic low-dose transcriptomics | SPOT-CHECK | 2 | 8 | `LUCID-replications/lucid100-zebrafish-brain-chronic-lowdose-transcriptomics/REPORT.md` |
| 80 | Clark-Hachtel 2024 tardigrade IR DNA repair upregulation (Curr Biol) | PARTIAL | 5 | 9 | `LUCID-replications/lucid100-tardigrade-ir-dna-repair-upregulation/REPORT.md` |
| 81 | Rumiantcev 2023 Ac225 vs Lu177 PSMA TOPAS/MEDRAS RBE | SPOT-CHECK | 3 | 6 | `LUCID-replications/lucid100-ac225-lu177-psma-topas-medras-rbe/REPORT.md` |
| 82 | Scott 2011 Epicellcom DSB repair kinetics (MULTISIG1) | REPLICATED | 8 | 9 | `LUCID-replications/lucid100-epicellcom-dsb-repair-kinetics/REPORT.md` |
| 83 | Belov 2023 HR shift low-LET DNA repair ODE | SPOT-CHECK | 2 | 6 | `LUCID-replications/lucid100-hr-shift-low-let-dna-repair/REPORT.md` |
| 84 | Jolly & Fielding 2025 targeted alpha single-cell MC DNA damage | SPOT-CHECK | 2 | 3 | `LUCID-replications/lucid100-targeted-alpha-single-cell-monte-carlo-dna-damage/REPORT.md` |
| 85 | Ma 2024 LDR cognitive impairment rat gamma (Frontiers PubH) | SPOT-CHECK | 4 | 9 | `LUCID-replications/lucid100-low-dose-rate-cognitive-impairment-rat-gamma/REPORT.md` |
| 86 | Guo 2022 industrial irradiation workers blood dose-response | PARTIAL | 5 | 8 | `LUCID-replications/lucid100-industrial-workers-blood-dose-response/REPORT.md` |
| 87 | Friedrich/Durante/Scholz 2012 GLOBLE static DSB clustering loops | PARTIAL | 4 | 6 | `LUCID-replications/lucid-friedrich-gldm-dsb-clustering-loops-slot63/REPORT.md` |
| 88 | Matsuya 2019 intensity-modulated radiation protective dose-rate (IMK) | SPOT-CHECK | 3 | 7 | `LUCID-replications/lucid100-intensity-modulated-protective-doserate/REPORT.md` |
| 89 | Taleei & Nikjoo 2013 biochemical DSB repair G1/S ODE | PARTIAL | 6 | 7 | `LUCID-replications/lucid100-biochemical-dsb-repair-g1-s/REPORT.md` |
