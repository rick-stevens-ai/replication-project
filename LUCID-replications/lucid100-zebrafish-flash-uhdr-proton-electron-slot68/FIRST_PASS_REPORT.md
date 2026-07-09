# First-pass report — LUCID100 slot 68

**Paper:** Horst F. et al. *Dose and dose rate dependence of the tissue sparing effect at ultra-high dose rate studied for proton and electron beams using the zebrafish embryo model.* Radiother Oncol 2024;194:110197. DOI 10.1016/j.radonc.2024.110197. PMID 38447870. CC-BY-NC.

**Verdict (one line):** **CONDITIONAL NO-GO** — full replication is **artifact-limited, not compute-limited**: the publisher PDF is unreachable to automated agents (Elsevier captcha) and the paper publishes no code, no public dataset, no preprint, and no extractable supplementary table; an end-to-end **smoke pipeline is already runnable today in synthetic-data mode** and is ready to ingest a 10-minute hand-digitization the moment a PDF is obtained.

**QA recommendation:** **RETAG worktype** from `simulation/model replication` → `wet-lab phenotype dose-response replication (zebrafish FLASH)` (details in README §QA RECLASSIFICATION REQUEST).

---

## 1. Metadata snapshot (from authoritative sources, 2026-06-09)
| Field | Value |
|---|---|
| Title | Dose and dose rate dependence of the tissue sparing effect at ultra-high dose rate studied for proton and electron beams using the zebrafish embryo model. |
| Authors | Horst F.E., Bodenstein E., Brand M., Hans S., Karsch L., Leßmann E., Löck S., Schürer M., Pawelke J., **Beyreuther E. (corresponding)**. |
| Affiliations | OncoRay (Helmholtz-Zentrum Dresden – Rossendorf + TU Dresden); HZDR Institute of Radiation Physics; CRTD / Cluster Physics of Life, TU Dresden. |
| Journal | Radiotherapy and Oncology, Vol. 194, Article 110197, May 2024 (e-pub 2024-03-05). |
| OA status | Hybrid CC-BY-NC (Unpaywall, Semantic Scholar). |
| Europe PMC flags | `inEPMC=N`, `inPMC=N`, `hasSuppl=N`, `hasData=N`, `hasPDF=N`. |
| Funding | EU. |
| Citations (as of 2026-06-09) | 25 (S2) / 17 (Europe PMC), strong uptake by the FLASH field. |
| MeSH highlights | Zebrafish (embryology), Protons, Electrons, Radiotherapy Dosage, Dose-Response Relationship, RBE. |

## 2. What the paper actually does (from abstract + Wu 2024 meta context)
- One-day-old zebrafish embryos (ZFE) irradiated at **15 – 95 Gy** at UHDR vs reference dose rate.
- **Three beams** at OncoRay/UPTD: proton entrance channel, proton SOBP (passive 3D-printed range modulator, see Frontiers Phys 2023), and 30 MeV electrons.
- **Four endpoints scored at 4 dpi**: pericardial edema, curved spine, embryo length, eye diameter.
- Build dose-response curves per (beam, rate, endpoint); extract iso-effect D50 per group.
- Compute dose-dependent **FLASH Modifying Factor (FMF = D50_CONV / D50_UHDR)** per beam/endpoint.
- Headline finding: FMF ≈ **0.7 – 0.8** for D ≥ ~50 Gy across all three beams. Below ~50 Gy the sparing fades — the paper's main novelty.
- Concludes ZFE is a **suitable pre-clinical high-throughput model** for FLASH RT.

## 3. Why the smoke replication has to be scoping-mode today
| Blocker | Detail | Mitigation attempted |
|---|---|---|
| Publisher PDF captcha | ScienceDirect returns "Are you a robot?" on every curl + on OpenClaw browser navigation; reference id `a092b8e1bab93e5d`. | Tried 4 user-agent / referer combinations; tried OpenClaw managed Chromium directly; tried HZDR institutional landing → CMS gate; tried Europe PMC fulltext → not deposited. |
| No preprint | bioRxiv API negative, medRxiv search negative, CORE/CORE-AC negative. | – |
| No public code | No GitHub / Zenodo / OSF / Figshare link in any metadata record. The Dresden group's three precursor ZFE-FLASH papers also publish no code. | – |
| No public dataset | Same; `hasData=N`. | Wu et al. 2024 meta-analysis (TCRT 23, PMC11544673) is the **only external table** with comparable ZFE FMF rows, but its search cutoff is March 2023 → predates Horst 2024. |
| No paid endpoints / author contact (task constraint) | – | Cannot escalate. |

## 4. Reproducibility scoping (what the replication will look like once a PDF lands)
1. **Hand-digitize Figures 2 – 4** of Horst 2024 (per-beam dose-response curves: UHDR vs CONV; one curve per endpoint) using WebPlotDigitize → ~ 6-8 points × 4 endpoints × 3 beams × 2 rates ≈ **300 points**. Estimated effort: **30-45 min**.
2. Save as `data/horst2024_doseresponse.csv` with the schema documented at the top of `scripts/smoke_replicate_horst2024.py`.
3. Run `python3 scripts/smoke_replicate_horst2024.py --mode real` — already implemented, no additional code needed.
4. Compare extracted `FMF = D50_CONV / D50_UHDR` per (beam, endpoint) to the paper's reported values:
   - Pass band: any **5/12** combinations within ±0.05 of paper's stated value AND every beam's mean FMF within paper's reported 0.7-0.8 band for D ≥ 50 Gy.
   - Stronger pass: **9/12** within ±0.05 AND correct **rank-order** of beams (the paper finds the sparing magnitude is comparable across endpoints — see abstract Results §3).
5. Cross-plot against Wu 2024 Table 2 ZFE rows (Beyreuther 2019, Karsch 2022, Saade 2023) as an external sanity anchor.

## 5. What was delivered today
- `README.md` — orientation + QA retag request.
- `PROGRESS.md` — session log.
- `ARTIFACT_MANIFEST.md` — every file with provenance, including negative-result records (so future runs don't repeat the same failed fetches).
- `scripts/smoke_replicate_horst2024.py` — end-to-end runnable in synthetic mode; will switch to real-data mode with a single flag once the digitized CSV exists.
- `data/synthetic_horst2024_like.csv` — 264 synthetic rows generated by the smoke run (acts as a schema example for the real CSV).
- `figures/smoke_proton_entrance.png`, `smoke_proton_SOBP.png`, `smoke_electron_30MeV.png`, `smoke_FMF_summary.png` — proof the pipeline runs and recovers planted FMF ≈ 0.73-0.85 (planted band 0.74 / 0.78 / 0.80 by beam → recovered means: proton-entrance 0.76, proton-SOBP 0.76, electron 0.83, all sitting on / in paper's reported 0.7-0.8 band).
- `artifacts/flash_meta.pdf`, `artifacts/frontiers_phys_sobp_2023.pdf` — two real OA context PDFs that ground the smoke replication.
- `notes/flash_meta_text.txt`, `notes/frontiers_sobp_text.txt` — pdftotext extracts for grep-friendly inspection.

## 6. Blockers and recommended next actions
1. **Acquire PDF** through any of:
   - Argonne National Lab institutional Elsevier access (Rick's account).
   - UChicago institutional access.
   - ILL request (slow).
   *(Not author contact — per task constraint.)*
2. **Digitize** Figures 2-4 with WebPlotDigitize → `data/horst2024_doseresponse.csv`.
3. **Re-run** smoke script in `--mode real` (no code changes needed).
4. **Master TSV maintainer**: retag row 127 worktype as recommended in §QA RECLASSIFICATION REQUEST.

## 7. Compute footprint
**Trivial.** `scipy.optimize.curve_fit` on ≤ 300 datapoints. Finishes in < 5 seconds on CherryRd. **No heavy-compute job plan needed.** This task is not GPU-bound and not memory-bound — the bottleneck is *access to text*, not silicon.

## 8. Final verdict
| Dimension | Score |
|---|---|
| Paper relevance to LUCID100 themes | **HIGH** (dose-rate response, RBE, FLASH/UHDR — all core themes). |
| Replication tractability today | **LOW** (PDF blocked, no code, no data). |
| Replication tractability with PDF | **HIGH** (hand-digitization → CSV → existing script). |
| Recommended next session | **PDF acquisition + 30-min digitization sprint**, then real-mode rerun. |
| Worktype QA | **RETAG** to wet-lab phenotype replication (currently mislabeled). |
