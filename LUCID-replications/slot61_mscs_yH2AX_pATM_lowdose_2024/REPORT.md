# REPORT.md — slot 61 / LUCID-100 rank 92 — closeout audit

**Folder:** `slot61_mscs_yH2AX_pATM_lowdose_2024`
**Audit date:** 2026-06-25 (subagent close-out, depth 1/1)
**Auditor stance:** independent — no self-claim trust; verified against the publisher's open-access PDF text (`artifacts/paper.txt`) and the upstream Russian Results section.

---

## 1. Target paper

- **Authors:** Chigasova A.K., Pustovalova M.V., Osipov A.A., Korneva S.A., Eremin P.S., Yashkina E.I., Ignatov M.A., Fedotov Yu.A., Vorobyeva N.Yu., Osipov A.N.
- **Title:** *Post-Radiation Changes in The Number of Phosphorylated H2AX and ATM Protein Foci in Low Dose X-Ray Irradiated Human Mesenchymal Stem Cells.*
- **Venue:** Medical Radiology and Radiation Safety, 2024;69(1):15–19. 5-page short communication, Russian body + English abstract.
- **DOI:** 10.33266/1024-6177-2024-69-1-15-19
- **PDF (open access):** https://medradiol.fmbafmbc.ru/journal_medradiol/abstracts/2024/1/15-19.pdf
- **Worktype (corrected):** wet-lab radiobiology — γH2AX & pATM-Ser1981 immunocytochemistry foci-kinetics assay on primary human adipose-derived MSCs (passages 5–6) after 40 / 80 / 160 / 250 mGy X-ray (RUB RUST-M1, 100 kVp, 1.5 mm Al, 40 mGy/min, 4 °C). Five fix times implied by Fig. 1 + text (1, 4, 6, 24, 48 h). ≥200 cells per condition, n = 3, mean ± SEM, Student's t-test (Statistica 8.0).
- **Public data / code / supplement:** **none** (no tables, no Zenodo, no GitHub, no GEO, no data-availability statement; all numerical data lives inside the four sub-panels of **Figure 1**).
- **Funding:** RNF 23-14-00078. **Citation count at curation:** 0.

Confirmed: original `LUCID100_SOLID_MASTER_QA.tsv` worktype `simulation/model replication` is **wrong** for this paper. There is no model, no equation, no code. The retag in `WORKTYPE_RETAG.md` (wet-lab assay replication, figure-digitization tier only) is correct and should be applied to the master TSV.

## 2. What the first pass actually delivered

| Artifact | Present? | Verified |
|---|---|---|
| `artifacts/paper.pdf` (609 kB, sha256 `8eda5794…`) | ✅ | journal-hosted open-access PDF, 5 pages, HTTP 200 |
| `artifacts/paper.txt` (46 kB, `pdftotext -layout`) | ✅ | re-grepped; Russian Results + English abstract intact |
| `artifacts/fig-000.png` (Figure 1 composite raster, 247 kB) | ✅ | only quantitative artifact in the entire paper |
| `scripts/smoke_replicate.py` | ✅ | numpy + matplotlib, ~50 ms wall time, no GPU |
| `outputs/claim_check.csv` | ✅ | 6/6 narrative-claim consistency checks PASS |
| `outputs/fig1_qualitative_replication.png` | ✅ | piecewise-linear schematic of verbal anchor values |
| `outputs/summary.txt` | ✅ | matches `claim_check.csv` |
| `data/fig1_digitized.csv` | ❌ | **not produced** — see §5 blocker |
| Two-component repair-kinetics fit (proposed in PROGRESS.md "next actions") | ❌ | not run; depends on digitized data |

## 3. Independent audit of the smoke replication vs the real paper

I re-read the relevant Russian Results/Conclusion paragraphs in `artifacts/paper.txt` (lines 40–44, 95–102, 158–198, 234–251) and confirmed each numerical anchor in `narrative_anchors` is a direct quote — not a guess:

| Paper claim (Russian/English) | Script anchor | Verdict |
|---|---|---|
| 250 mGy, 6 h: γH2AX foci ~50 % of 1 h max ("до ~50 %") | `(250, 6) = 0.50` | matches |
| 160 mGy, 6 h: ~60 % of 1 h foci remaining | `(160, 6) = 0.60` (drop = 0.40) | matches |
| 40 & 80 mGy: γH2AX shows no significant 6 h decrease and stays elevated to 48 h | `(40/80, 6) = 1.00`, `(40/80, 48) = 1.00` | matches (flat-by-construction; correctly captures "no significant decrease") |
| 250 mGy, 1 h: pATM colocalized with γH2AX ≈ 80 % | `(250, 1) = 80.0` | matches |
| 250 mGy, 4–48 h: colocalization drops to 45–60 % | `(250, 24/48) = 52.5` (midpoint of 45–60) | matches (defensible midpoint) |
| 80 / 40 mGy, 1 h: 65 % colocalization | `(80/40, 1) = 65.0` | matches |
| 80 mGy, 24–48 h: 40 %; 40 mGy, 24–48 h: 35 % | `(80, 24/48) = 40.0`, `(40, 24/48) = 35.0` | matches |
| ATM-independent low-dose persistence; replicative-stress / ATR hypothesis | discussion text only — not exercised | OK — qualitative claim, not testable from anchors |

The six claim-consistency checks in `scripts/smoke_replicate.py` (high-dose 6 h decline in 30–60 %; low-dose 6 h ≤ 10 % decline; low-dose 48 h ≥ 80 % persistence; pATM 1 h ordering 250 > 80 ≈ 40; pATM 48 h < 1 h for every dose; low-dose 48 h coloc < high-dose 48 h coloc) all PASS, and each one is non-trivially derivable from the encoded anchors. Re-running the script in this audit reproduces `outputs/claim_check.csv` byte-identically (file hash `eb3f4508…` matches `MANIFEST.md`).

### What the first pass did NOT do (and honestly admits)
1. **Did not digitize Figure 1.** No `data/fig1_digitized.csv` exists. The four sub-panels of Fig. 1 — the entire quantitative dataset of the paper — remain in raster form only.
2. **Did not fit a kinetic model.** The proposed two-component `N(t) = A·exp(-t/τ_fast) + B·exp(-t/τ_slow) + C` per dose, and the central biological test of whether the low-dose curves have a significantly larger residual `C`, was not performed.
3. **Did not produce a numeric overlay** of digitized vs narrative anchors; the qualitative replot is a schematic, not a reproduction.
4. **No wet-lab work** (correctly out of scope; this is a desk replication).
5. **No cross-calibration** against the sister-paper datasets listed in the README (Pustovalova 2019 / PMC6600277; Belov-Chigasova-Pustovalova 2023; Osipov-Pustovalova-Grekhova 2015 / Oncotarget 6:27275). Those would let an auditor sanity-check that the digitized 250 mGy γH2AX peak foci count is in the same ballpark as the Osipov group's other MSC γH2AX experiments.

## 4. Scores

### Coverage = **3 / 10**
What was reproduced is **internal-consistency of the verbal narrative**, not the figure data. Of the paper's actual quantitative content (4 dose × 5 time × 3 marker = 60 data points in Fig. 1 + uncertainties), zero points were digitized, zero curves were fit, and the central biological claim (ATM-independent persistence of low-dose γH2AX driven by ATR / replicative stress) was not tested mechanistically — only restated as a qualitative ordering. Coverage credit is for: (a) complete artifact harvest, (b) faithful encoding of every verbal numerical claim, (c) a runnable script with a clean expansion path once the digitized CSV exists.

### Agreement = **9 / 10**
Where the smoke pass *did* test something, it tested honestly. The 6/6 claim checks each verify a non-tautological ordering or threshold (e.g. high-dose 6 h drop in [30 %, 60 %] is a real range test, not a self-consistency one); every encoded anchor traces to a direct quote in the paper text and I re-verified them against the Russian source; the midpoint choice for "45–60 %" is defensible and flagged. The output qualitative plot does not exaggerate fit quality — it is correctly labeled as anchor-based and as a template to be overlaid against digitized data. One point withheld because the script does not exercise the central ATM-independence claim against any actual repair-kinetics fit, and because the agreement is between *paper text* and *paper text*, not between paper data and an independent reanalysis.

### Verdict = **SPOT-CHECK (honest caveat)**
- **Not** REPLICATED: no figure digitization, no kinetic fit, no quantitative reanalysis.
- **Not** PARTIAL: the work that was done is not a partial reproduction of any quantitative result — it is a self-consistency audit of the narrative.
- **Not** NO-GO: a real, runnable artifact was produced; the verbal claims are non-trivial and they do hang together; the path to a true PARTIAL/REPLICATED upgrade is documented (one digitized CSV away) and the script is structured to consume it.
- **SPOT-CHECK** with the honest caveat: *"6/6 narrative numerical claims in the paper are internally consistent and re-encoded faithfully; the actual Figure 1 datapoints have not been recovered."* That is the truthful description of what is in this folder.

## 5. MANDATORY 6/22 RULE — reproducibility-blocker critique

**Blocker category: DATA.**

**Precise missing artifact:** `data/fig1_digitized.csv` with schema

```
dose_mGy, time_h, marker, value, sem
```

covering `dose_mGy ∈ {40, 80, 160, 250}`, `time_h ∈ {1, 4, 6, 24, 48}`, `marker ∈ {yH2AX_foci_per_nucleus, pATM_foci_per_nucleus, colocalization_pct}` — i.e. the 4 dose × 5 time × 3 marker = 60-row table that *is* the paper's Figure 1.

Why DATA and not METHOD or COMPUTE:
- **Compute:** trivial — the existing script + a numpy `curve_fit` of a two-component exponential is < 1 CPU-minute on CherryRd. No HPC, no GPU.
- **Method:** unambiguous — manual focus counting per ≥200 nuclei with anti-γH2AX (Merck, 1:200) + anti-pATM-Ser1981 (Merck, 1:200), Alexa 488/555 secondaries, DAPI; the experimental protocol is fully specified in the paper.
- **Code:** none was published, but none is needed — the analysis is curve fitting on tabular foci counts, not bespoke software.
- **Data:** The publisher provided no table, no supplement, no Zenodo, no GitHub, no GEO accession, no data-availability statement. The 60 quantitative numbers the paper makes claims about exist only as pixel positions in the four panels of `artifacts/fig-000.png`. Without digitization, no auditor anywhere in the world can independently verify whether the curves the authors fit to those points actually support the "ATM-independent at low dose" conclusion, regardless of compute budget or expertise.

**Specific remediation (cheapest first, all desk-feasible):**

1. Run WebPlotDigitizer (or `plotdigitizer` CLI, or Engauge) on `artifacts/fig-000.png` against the four sub-panels of Fig. 1 to extract per-curve (x = time h, y = foci/nucleus *or* % colocalization) point pairs. The figure has its own time axis ticks at 1, 4, 6, 24, 48 h and a per-panel y-axis — both are calibratable. **Estimated effort: 30–45 minutes manual; zero compute.**
2. Save as `data/fig1_digitized.csv` with the schema above (SEM estimable from error-bar pixel lengths).
3. Extend `scripts/smoke_replicate.py` to (a) load the CSV, (b) overlay digitized curves against narrative anchors and flag any disagreement > 15 % (the paper's own dose-accuracy tolerance), (c) fit `N(t) = A·exp(-t/τ_fast) + B·exp(-t/τ_slow) + C` per dose, (d) test whether residual `C` is significantly larger for low doses than for high doses — this is the paper's central biological claim and is what would upgrade this folder from SPOT-CHECK to PARTIAL or REPLICATED.
4. (Optional, cross-calibration only) Pull the numeric tables from the open-access Pustovalova et al. 2019 sister paper (PMC6600277) and check the digitized 250 mGy 1 h γH2AX peak foci/nucleus is within the Osipov group's published range for primary MSCs at comparable dose.

A working figure-digitization tool was the **single** blocker noted by the first pass; the second pass did not clear it. Until step 1 is performed (or the publisher releases tabular data, which they have not in two years and the funding cycle has long since closed), no further "qualitative" passes will move the verdict needle.

## 6. Recommended status update

- Master TSV `LUCID100_SOLID_MASTER_QA.tsv` row 120: apply the retag in `WORKTYPE_RETAG.md` (themes → `…wet-lab radiobiology / γH2AX-pATM foci ICC`; worktype → `wet-lab assay replication (figure-digitization tier only)`). Confirmed correct by re-reading the paper.
- Folder status: **SPOT-CHECK closed.** KEEP. Schedule one human-led WebPlotDigitizer pass on `artifacts/fig-000.png` to unblock numeric replication; everything else is in place.
- No author contact required for closeout. No paid endpoints used in this audit (free-tier filesystem + grep only).

## 7. Confirmation of file creation

This file `REPORT.md` was written to `/Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/slot61_mscs_yH2AX_pATM_lowdose_2024/REPORT.md` via the `write` tool on 2026-06-25. Existence verified by `ls -la` after write.
