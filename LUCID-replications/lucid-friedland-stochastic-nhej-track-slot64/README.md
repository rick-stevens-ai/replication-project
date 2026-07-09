# LUCID Replication — Friedland, Jacob, Kundrát (2010) Stochastic NHEJ DSB Repair

**Slot:** LUCID100 backfill slot 64 (Wave 7, master-QA rank 95)
**Target paper:** Friedland W, Jacob P, Kundrát P. *Stochastic Simulation of DNA Double-Strand Break Repair by Non-homologous End Joining Based on Track Structure Calculations.* **Radiat Res** 173(5):677–688, 2010. DOI [10.1667/RR1965.1](https://doi.org/10.1667/RR1965.1). PMID 20426668.
**OA status:** **CLOSED** — Unpaywall confirms no OA and no repository copy as of 2026-02-09. PARTRAC code is **not public** (Helmholtz-internal).

## Scope and verdict (one line)

**Architectural smoke replication: PASS (qualitative).** Four-state stochastic NHEJ scheme implemented from the published abstract + open-access Friedland-group companion papers; reproduces biphasic fast/slow DSB rejoining kinetics consistent with γ-H2AX benchmarks and the residual-DSB phenomenology described in the abstract. **No** quantitative reproduction of the four model scenarios from RR1965 itself is possible without access to the closed PARTRAC inputs and the in-paper Tables.

See `FIRST_PASS_REPORT.md` for the full verdict, friction tags, and QA retag recommendation.

## What's in this folder

| Path | Purpose |
| --- | --- |
| `README.md` | This file |
| `FIRST_PASS_REPORT.md` | First-pass verdict, evidence, friction tags, QA retag recommendation |
| `PROGRESS.md` | Chronological log of what was tried, what worked, blockers |
| `ARTIFACT_MANIFEST.md` | Listing of all artifacts (PDFs, scripts, figures, results) with provenance |
| `source/rr1965_metadata.md` | Title, authors, journal, PubMed-derived full abstract for the target paper |
| `source/pubmed_20426668.xml` | Raw PubMed record |
| `source/henthorn2018_nhej.pdf` + `.txt` | Henthorn 2018 Sci Rep — OA, in-silico NHEJ model citing RR1965 |
| `source/kundrat2021_coupling.pdf` + `.txt` | Kundrát/Friedland/Ottolenghi 2021 Front Phys — OA, same group's later coupling paper |
| `source/li2014_nhej_complexity.pdf` + `.txt` | Li, Reynolds, O'Neill 2014 PLoS ONE — OA, NHEJ-complexity model with explicit min⁻¹ rate constants |
| `source/model_notes.md` | Curated extraction of the RR1965 model architecture and parameters reconstructed from the abstract + companions |
| `code/nhej_smoke.py` | Self-contained Gillespie stochastic NHEJ smoke replication |
| `code/run_smoke.py` | Driver: runs the smoke for two damage qualities, makes the figure, dumps results JSON |
| `results/smoke_summary.json` | Headline numbers from the smoke run |
| `results/rejoining_curves.csv` | Time × surviving-DSB-fraction curves |
| `figures/dsb_rejoining.png` | Biphasic rejoining kinetics figure |
| `logs/smoke.log` | Stdout/stderr from the smoke run |

## Rerun

```bash
cd ~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid-friedland-stochastic-nhej-track-slot64
python3 code/run_smoke.py
```

Runs in **<10 s** on a single laptop CPU core. Dependencies: `numpy`, `matplotlib`. No external data, no paid endpoints, no GPU, no compute outside CherryRd needed.

## What this replication is and is not

- **Is:** An architectural / scoping smoke that implements the *qualitative* structure of the RR1965 NHEJ model (Ku/DNA-PK attachment → synapsis → ligation, with a clean-end fast track and a dirty-end multi-step slow track) and checks that it reproduces the biphasic DSB rejoining phenomenology that the abstract describes (fast phase ~tens of minutes, slow phase ~hours, residual DSBs at 24 h).
- **Is not:** A faithful numerical reproduction of any of the four RR1965 scenarios, the Ku70/80 and DNA-PK on/off rates derived from fluorescence-recovery experiments, or the PARTRAC track-structure DSB inputs. The paper is closed and PARTRAC is not public; the four-scenario figures cannot be reproduced without the journal PDF, the in-paper rate-constant tables, and a track-structure code with NHEJ-compatible damage classification.

## Pointer to related already-done replications

- `lucid-partrac-analytical-formulas` — Kundrát 2020 Sci Rep, same group, replicates analytical DNA-damage formulas. Different paper, no overlap with this slot.
- `lucid-stochastic-rejoining` — Li 2012 PLoS ONE Gillespie DNA-fragment rejoining. Different model (fragment rejoining, not full NHEJ pathway).
- `lucid-slow-fast-nhej` — Qi 2021 Cancers slow-fast NHEJ ODE model. Conceptually adjacent (also a two-pool NHEJ pathway model), but uses a different DaMaRiS-derived pathway topology.
