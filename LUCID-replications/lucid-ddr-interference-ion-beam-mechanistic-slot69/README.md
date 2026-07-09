# LUCID Replication — Liew et al. (2021) UNIVERSE for combined DDR-interference + ion-beam therapy

**Slot:** LUCID100 backfill slot 69 (Wave 7, master-QA rank 100)
**Target paper:** Liew H, Meister S, Mein S, Tessonnier T, Kopp B, Held T, Haberer T, Abdollahi A, Debus J, Dokic I, Mairani A. *Combined DNA Damage Repair Interference and Ion Beam Therapy: Development, Benchmark and Clinical Implications of a Mechanistic Biological Model.* **Int J Radiat Oncol Biol Phys** 112(3):802–817, 2022 [online 2021-10-25]. DOI [10.1016/j.ijrobp.2021.09.048](https://doi.org/10.1016/j.ijrobp.2021.09.048). PMID 34710524.
**OA status:** **CLOSED** (Elsevier/IJROBP). Unpaywall: `closed`, no PMC, no repository. **Code: NOT public.**

## Scope and verdict (one line)

**Architectural + headline-mechanism smoke replication: PASS.** UNIVERSE's photon + DDR-interference half is fully implemented from the OA twin paper (Liew 2019 IJMS) and reproduces the right cell-survival magnitudes, the correct dose-curve steepening under ATM-inhibitor, and — via a bounded LET surrogate — the target paper's central mechanistic claim that *the DDRi-induced radiosensitisation effect shrinks at high LET*. Quantitative reproduction of the ion-beam SOBP measurements and the patient-plan recalculations from the 2021 paper is **not** possible without the closed HIT FLUKA/treatment-planning stack and the un-released UNIVERSE source code.

See `FIRST_PASS_REPORT.md` for the full verdict, friction tags, and QA retag recommendation.

## What's in this folder

| Path | Purpose |
| --- | --- |
| `README.md` | This file |
| `FIRST_PASS_REPORT.md` | First-pass verdict, evidence, friction tags, QA retag recommendation |
| `PROGRESS.md` | Chronological log of what was tried, what worked, blockers |
| `ARTIFACT_MANIFEST.md` | Listing of all artifacts with provenance |
| `source/model_notes.md` | Curated model extraction (equations, parameters, references) |
| `source/semantic_scholar_metadata.json` | Raw S2 record incl. full abstract |
| `source/liew2019_ddr_hypoxia_photon.{pdf,txt}` | **PRIMARY OA TWIN.** Liew 2019 IJMS 20:6054 — defines the DDR-interference extension exactly as inherited by the 2021 paper |
| `source/mein2019_universe_rbe.{pdf,txt}` | UNIVERSE ion-beam RBE for ⁴He — basis for the 2021 paper's ion-beam half |
| `source/liew2022_universe_repair.{pdf,txt}` | UNIVERSE with explicit Kiefer–Chatterjee track-structure description |
| `source/liew2022_universe_flash.{pdf,txt}` | UNIVERSE sub-millisecond / FLASH extension (context) |
| `source/liew2020_hypoxia_direct_indirect.{pdf,txt}` | UNIVERSE direct/indirect action extension (context) |
| `source/scholz2020_lemiv_part1.{pdf,txt}` | Independent LEM-IV review (context, for cross-comparison of the GLOBLE-family approach) |
| `code/universe_smoke.py` | Self-contained UNIVERSE photon-MC + LET surrogate library |
| `code/run_smoke.py` | Driver: runs (1) 5-cell-line photon SF, (2) ATMi steepening, (3) LET sweep |
| `results/smoke_summary.json` | All headline numbers from the smoke run |
| `results/photon_survival_no_ddri.csv` | SF vs. dose for 5 cell lines (no DDRi) |
| `results/photon_survival_atmi.csv` | SF vs. dose for H460/H1437 at 4 ATMi RSF values |
| `results/lq_fits.csv` | LQ alpha, beta, alpha/beta fitted to UNIVERSE photon output |
| `results/let_sweep_ddri.csv` | RBE_noDDRi, RBE_DDRi, ratio across LET 2–120 keV/µm |
| `figures/photon_no_ddri.png` | Photon SF curves, 5 cell lines |
| `figures/photon_atmi.png` | Photon SF curves with ATMi RSF (Liew 2019 Table 3 reproduction) |
| `figures/let_sweep_rbe_ratio.png` | Headline mechanistic test: RBE-ratio vs LET |
| `logs/smoke.log` | Stdout/stderr from the smoke run |

## Rerun

```bash
cd ~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid-ddr-interference-ion-beam-mechanistic-slot69
python3 code/run_smoke.py
```

Runs in **<20 s** on a single CherryRd CPU core. Dependencies: `numpy`, `matplotlib`. No external data, no paid endpoints, no GPU, no heavy-compute hosts needed.

## What this replication is and is not

- **Is:** A faithful from-equations implementation of the *photon + DDR-interference* core of UNIVERSE (Eqs. 1–7 of Liew 2019 IJMS) — i.e. the *same* mathematical engine that the 2021 IJROBP paper extends to ions. The smoke reproduces (i) the 5-cell-line photon survival magnitudes, (ii) the correct dose-curve steepening with ATM-inhibitor RSF, and (iii) the central mechanistic claim of the target paper that DDRi loses effectiveness at high LET. Items (i)–(iii) are the bulk of the model science the 2021 paper rests on.
- **Is not:** A reproduction of the closed Heidelberg FLUKA-coupled ion-beam track-structure MC, the helium spread-out-Bragg-peak in-vitro measurements presented as the paper's novel experimental data, or the helium-patient treatment-plan recalculations. None of those artefacts are public, and CherryRd is not in scope for FLUKA SOBP simulations. The LET dependence in the smoke is therefore a **bounded surrogate** calibrated against the published UNIVERSE ⁴He RBE curves (Mein 2019), not a track-structure MC.

## Pointer to related already-done replications

- `lucid-mariotti-split-dose-gamma-h2ax` — adjacent γH2AX / DSB-induction smoke
- `lucid-mcmahon-2016-medras-original` — MEDRAS, an alternative DSB-clustering / cell-survival model
- `lucid-friedland-stochastic-nhej-track-slot64` — PARTRAC NHEJ smoke (track-structure neighbour to UNIVERSE)
- `lucid-friedrich-gldm-dsb-clustering-loops-slot63` — Friedrich GLDM/giant-loop DSB clustering, the direct progenitor framework of UNIVERSE
