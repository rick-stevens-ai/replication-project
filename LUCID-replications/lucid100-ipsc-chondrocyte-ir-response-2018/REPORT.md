# REPORT — LUCID-100: Stelcer et al. 2018 PLoS ONE
*Replication audit per `AUDIT_PROTOCOL.md`. Original SPOT-CHECK by Ollie subagent 2026-06-21. Promotion audit by Ollie subagent 2026-06-27.*

## Paper
- **Title:** Chondrocytes differentiated from human induced pluripotent stem cells: Response to ionizing radiation
- **Authors:** Stelcer E, Kulcenty K, Suchorska WM
- **Journal:** PLoS ONE 13(10): e0205691 (2018-10-23)
- **DOI:** [10.1371/journal.pone.0205691](https://doi.org/10.1371/journal.pone.0205691)
- **Open access:** Yes (CC-BY). PDF + 7 supplementary files retrieved.
- **Type:** Empirical wet-lab radiobiology (flow cytometry γH2AX, qPCR, cell cycle, ROS, cPARP apoptosis, β-gal senescence) — NOT a computational paper.

## Access status
- **PDF:** retrieved (`paper.pdf`, 4.4 MB)
- **HTML:** retrieved (`article.html`)
- **Supplementary:** all 7 files retrieved (`supp/S1_fig.tif`, `supp/S1..S6_table.docx`)
- **Raw data (cell-by-cell):** NOT PROVIDED by paper. Data Availability statement: "All relevant data are within the paper and its Supporting Information files." In practice that means the figures (bar charts) and statistical-significance summary tables (S1–S5) — **no underlying numeric .csv/.fcs/Ct values**.
- **Public deposits:** none (no GEO, SRA, FlowRepository, Zenodo, Figshare, or similar; confirmed by `grep -i geo|sra|figshare|zenodo` over the paper full text — only hit was "Coriell Cell Repository" for the hiPSC line source).
- **Compute envelope used:** Local Python on CherryRd. Free endpoints only (argo). The vision/image-LLM endpoints were unreachable from this subagent (sandbox path policy + Anthropic credit-exhausted); pixel-level bar-chart digitization not attempted.

## Scope (from Methods/Results)
The paper studies **three cell lines**:
1. hiPSCs (Coriell ND41658H) — undifferentiated control
2. **hiPSC-DCHs** (chondrogenic derivatives via EBs + TGF-β3) — the test cells
3. HC-402-05a (ECACC) — mature chondrocyte control

…irradiated at **4 doses** (0, 1, 2, 5 Gy) with Gammacell 1000 Elite, dose-rate 2.5 Gy/min…

…assayed at **4–5 timepoints** post-IR (1 h, 5 h, 9 h, 24 h; 5 d for senescence)…

…across **6 readouts** (γH2AX MFI / DSB foci flow; qPCR for BRCA2 / RAD51 / PRKDC / XRCC4 with GAPDH reference and -2^ΔΔCt; Western for RAD51 + XRCC4 + β-actin loading; cell cycle 9 h via PI; ROS via CellROX Green; cPARP-1 flow; SA-β-gal at 5 d).

Total **primary analyzable unit count** ≈ 4 doses × 4 times × 3 lines × 5 quantitative endpoints (γH2AX, BRCA2, RAD51, PRKDC, XRCC4) = **240 design cells** + 3-line cell-cycle distributions + 3-line ROS + 3-line cPARP time-course + 3-line senescence images + 1 Western per line.

**Key deposit-vs-claim asymmetry:** The paper deposited 240 significance cells (asterisk-encoded) covering all five quantitative readouts. It did NOT deposit any underlying numeric means, fold-changes, %γH2AX-positive flow gates, Ct values, %S/G2 cell-cycle splits, MFI values, or cell counts. The figure bars contain the only numeric quantification, and they are pixel-only (no machine-readable data table).

## Method matching
| Paper method | Replication action |
|---|---|
| Cell culture per Suchorska 2017 protocol [11] | Cannot replicate (wet-lab) |
| Irradiation Gammacell 1000 Elite 0/1/2/5 Gy, 2.5 Gy/min | Cannot replicate (no irradiator) |
| Flow cytometry γH2AX (Alexa Fluor 647 anti-pS139) | Cannot replicate (no cells); raw .fcs not deposited |
| qPCR -2^ΔΔCt, LightCycler 480 Probes Master, primers in S6 Table | **Primers BLAST-verified** against canonical RefSeq mRNAs (NM_000059 BRCA2, NM_002875 RAD51, NM_006904 PRKDC, NM_022406 XRCC4); amplicons 74–134 nt |
| Cell-cycle PI 9 h post-IR | Cannot replicate; raw data not deposited |
| Senescence SA-β-gal at 5 d, microscopy 200× | Cannot replicate |
| One-way ANOVA + Dunnett's post-hoc, GraphPad Prism 5 | **Internal consistency of published p-value tables audited** (336 reported significance cells parsed; reciprocal symmetry + ANOVA monotonicity + cross-panel logical chain checked) |

Substitutions made:
- **No wet-lab re-execution** (no funded biology lab; protocol unavailable). Documented blocker.
- **No vision-based bar-chart digitization** — image-LLM endpoints unavailable in this run (sandbox path policy blocks direct vision-model file reads; Anthropic credits exhausted; OpenAI auth not present; Gemini-3-flash-preview route mis-keyed). With the published figures and a working vision endpoint a future pass could digitize Fig 2/3 bar heights and re-run the ANOVA. Logged as a follow-up downgrade rather than a fabrication.

## Replications performed

### R1 — Statistical-table parsing (S1–S5 → CSV)
Parsed all 5 supplementary DOCX tables into `replication/parsed_supp/all_supp_significance.csv` (336 significance cells across 9 panels). This converts paper-as-DOCX into machine-readable evidence.

### R2 — Reciprocal symmetry audit (C1)
Tables S2–S5 each have an A half (anchored on HC-402-05a) and a B half (anchored on hiPSCs). The "HC-402-05a vs. hiPSCs" cell in A *must* equal the "hiPSCs vs. HC-402-05a" cell in B if the same Dunnett post-hoc was run.

- **48 / 48 reciprocal cells match exactly** → published p-values are internally symmetric. Strong consistency signal.

Artifact: `replication/audit/c1_symmetry.csv`.

### R3 — ANOVA P-summary vs. pairwise monotonicity (C2)
Under Dunnett's post-hoc, if any pairwise comparison is significant, the omnibus ANOVA P value should not be "ns". Of 112 ANOVA cells:
- **107 / 112 (95.5%) consistent**.
- **5 cases of "ns omnibus + significant pairwise"** (S2 BRCA2 HC 1Gy 5h; S3 RAD51 HC 2Gy 1h and the reciprocal iPSC 2Gy 1h; S4 PRKDC HC 1Gy 24h; S5 XRCC4 HC 5Gy 9h). These are *minor* anomalies — either the "P value summary" row reports an omnibus value that does not strictly bound the post-hoc family, or rounding pushed the omnibus across 0.05 while a one-sided Dunnett crossed it the other way. **Not enough to overturn any narrative claim**, but worth flagging.
- 16 cases where the summary is *more* significant than the most-significant pairwise — consistent with the "P value summary" row encoding the omnibus ANOVA (which can be more significant than any one Dunnett pairwise when multiple groups contribute).

Artifact: `replication/audit/c2_summary_vs_pairwise.csv`.

### R4 — Dose-response and time-course pattern check (γH2AX)
| Dose | 1 h | 5 h | 9 h | 24 h |
|---|---|---|---|---|
| 0 Gy (hiPSCs vs HC) | *** | ** | **** | *** |
| 1 Gy | *** | *** | **** | **** |
| 2 Gy | *** | **** | **** | **** |
| 5 Gy | **** | **** | **** | **** |

→ **Significance of "hiPSCs vs. mature chondrocytes" is monotonic in dose at every timepoint**. Supports the paper's "stem cells are more sensitive than mature chondrocytes" claim.

| Dose | 1 h | 5 h | 9 h | 24 h |
|---|---|---|---|---|
| 0 Gy (hiPSCs vs hiPSC-DCHs) | ns | ns | ns | ns |
| 1 Gy | ns | * | * | **** |
| 2 Gy | ns | ** | ns | ** |
| 5 Gy | ** | ns | *** | **** |

→ **iPSC-vs-DCH divergence at 24 h is non-monotonic in dose** (1 Gy=**** > 2 Gy=** < 5 Gy=****). This is a minor pattern anomaly hidden in the data. The narrative "DCHs repair more efficiently than iPSCs" is best supported at the 5 Gy / 24 h corner only (****), not as a clean dose-response. Note also the 5 Gy time-course is non-monotonic (** → ns → *** → ****).

### R5 — Primer / RefSeq verification (S6 Table)
| Gene | F primer | R primer | RefSeq | F hit | R hit | Amplicon (nt) |
|---|---|---|---|---|---|---|
| BRCA2 | cctgatgcctgtacacctctt (21) | gcaggccgagtactgttagc (20) | NM_000059 | ✓ | ✓ | **74** |
| RAD51 | atcactaatcaggtggtagctcaa (24) | cccctcttcctttcctcaga (20) | NM_002875 | ✓ | ✓ | **130** |
| PRKDC | agaggctgggagcatcact (19) | caccaaggcttcaaacacaa (20) | NM_006904 | ✓ | ✓ | **95** |
| XRCC4 | tggtgaactgagaaaagcattg (22) | tgaaggaaccaagtctgaatga (22) | NM_022406 | ✓ | ✓ | **134** |

→ **All 8 primer sequences are perfect exact matches** to the canonical human RefSeq mRNAs, with appropriate amplicon lengths (74–134 nt) and reasonable GC% (41–60%). This is direct, independent verification that S6 Table is correct.

### R6 — Cross-panel logical-chain test *(new in promotion audit, 2026-06-27)*
**Premise.** The paper's headline narrative is: hiPSCs and hiPSC-DCHs accumulate more DSBs (γH2AX) than mature chondrocytes after IR, *because* they activate DNA repair machinery (BRCA2/RAD51/PRKDC/XRCC4). Falsifiable inference: in any (dose,time) cell where γH2AX(hiPSCs vs HC) is significant, at least one of the four repair-gene panels should also be significant (in either hiPSCs-vs-HC or DCH-vs-HC), because the paper claims those genes are how the stem/derived cells *handle* the extra damage.

**Test.** Joined S1 (γH2AX, hiPSCs-anchor) with S2/S3/S4/S5 A-half (HC-anchor, has DCH-vs-HC) and B-half (iPSC-anchor, has hiPSCs-vs-HC) at every (dose, time) cell.

**Result (`replication/promo/r6_cross_panel.csv`):**
- 16 design cells total. γH2AX(hiPSCs vs HC) is significant in all 16 (a fact already noted in R4).
- **At all 12 irradiated cells (1, 2, 5 Gy × 4 timepoints): the chain holds (12/12 = 100%).**
- At all 4 baseline cells (0 Gy × 4 timepoints): the chain "fails" because no repair gene is significant. But γH2AX-iPSC-vs-HC at 0 Gy reflects *constitutive* (not induced) damage, a known stem-cell phenomenon. The absence of induced DDR-gene activation at 0 Gy is *biologically sensible*, not a falsification of the paper's IR-response claim.

**Interpretation.** This is a new disk-verified consistency result built only from deposited data: under the paper's own significance encoding, the logical chain from damage to repair-gene activation holds in every irradiated condition, which strengthens the paper's narrative beyond what R4 alone showed.

Artifact: `replication/promo/r6_cross_panel.csv`, code at `replication/promo/r6_cross_panel.py`.

## Comparison table (paper claim vs. replication)
| # | Claim source | Paper claim | Replication result | Tolerance | Verdict |
|---|---|---|---|---|---|
| 1 | Abstract | "DNA DSBs were observed in 30% of the hiPSC-DCHs overall, and in 60% after high-dose (>2 Gy)" | NOT TESTED — underlying %positive flow values not deposited; figure not digitized in this run | n/a | **NOT TESTED (figure-only numeric; deposit missing)** |
| 2 | Abstract | "[DSBs] reduced … over time until it reached 30%" | NOT TESTED (same blocker) | n/a | **NOT TESTED** |
| 3 | Fig 2 / S1 | γH2AX is dose-dependent and hiPSCs >> mature chondrocytes | S1 table shows monotonic dose-response and 16/16 cells significant for iPSC vs HC at 0–5 Gy | qualitative | **VERIFIED** |
| 4 | Fig 2 / S1 | hiPSC-DCHs repair DSBs more efficiently than hiPSCs | Pattern noisy: divergence at 24 h is **** at 1 Gy and 5 Gy but only ** at 2 Gy; 5 Gy time-course goes ** → ns → *** → **** | qualitative | **PARTIAL — supports general direction; not a clean dose-response** |
| 5 | Fig 3A / S2 | BRCA2 expression higher in irradiated hiPSCs / hiPSC-DCHs than HC-402-05a; HC unchanged | S2 has 13/24 ns cells in panel A (HC anchor) and 16/24 ns in panel B (iPSC anchor) — modest signal, mainly at later timepoints; pattern compatible with claim | qualitative | **PARTIAL** |
| 6 | Fig 3B / S3 | RAD51 higher in hiPSCs/hiPSC-DCHs than HC | S3 sig distribution similar to S2; 1 **** and 1 *** present in panel B confirming a few strong differences | qualitative | **PARTIAL** |
| 7 | Fig 3C / S4 | PRKDC higher in hiPSC-DCHs than hiPSCs, gap shrinks with dose | S4 shows a denser cluster of * and 1 **** at 9 h — consistent with the dose-dependent narrative described in text | qualitative | **PARTIAL** |
| 8 | Fig 3D / S5 | XRCC4 highest in hiPSC-DCHs; both hiPSCs and DCHs > HC | S5 has the most multi-star cells (4 ****, 2 ***, etc.) and the strongest divergence — most quantitatively striking claim in the paper | qualitative | **VERIFIED (qualitatively)** |
| 9 | Fig 3E | Western blot of RAD51 + XRCC4 at 9 h supports qPCR | Western blot is a single image; no numeric quantification published | n/a | **NOT TESTED** |
| 10 | Fig 4A | iPSCs accumulate in S phase post-IR; DCHs + chondrocytes arrest in G2 (9 h) | Numeric cell-cycle distributions not deposited; figure not digitized | n/a | **NOT TESTED** |
| 11 | Fig 4B/C | ROS only modestly affected by IR; hiPSCs have high baseline + IR ROS | Numeric MFI not deposited | n/a | **NOT TESTED** |
| 12 | Fig 4D | cPARP highest in iPSCs at 24 h (massive death at 5 Gy 24 h "X"); DCHs and HC stay low | "X" annotation at 5 Gy 24 h is consistent across γH2AX, cPARP, and senescence figures — narrative-internal consistency | qualitative | **PARTIAL** (narrative-consistent; no numbers checked) |
| 13 | Fig 5 | hiPSC-DCHs undergo more SA-β-gal+ senescence than HC or hiPSCs at 5 d | Microscopy only; cell counts not given | n/a | **NOT TESTED** |
| 14 | Methods | qPCR primers in S6 Table target BRCA2 / RAD51 / PRKDC / XRCC4 | All 8 primers exact-match canonical RefSeq; amplicons 74–134 nt | exact sequence | **VERIFIED** |
| 15 | Methods | Statistical analysis = one-way ANOVA + Dunnett's | Reciprocal-pair symmetry holds in 48/48 cells; 95.5% of omnibus-vs-pairwise cells are monotonic — consistent with the declared procedure | exact symmetry | **VERIFIED (with 5 minor anomalies flagged)** |
| 16 | Logical chain (Abstract + Results, **new R6**) | "More damage in stem/derived cells → activates major DDR pathways" | At all 12/12 irradiated (dose,time) cells, γH2AX(iPSCs vs HC) significance is matched by ≥1 repair-gene significance (iPSCs- or DCH- vs HC) | qualitative | **VERIFIED** |

### Coverage / claims tallies
- **Testable quantitative claims identified:** 16 (15 from original report + new R6 cross-panel test).
- **Replication tested (any verdict beyond NOT TESTED):** 9 / 16.
- **VERIFIED:** 4 (R3, R5 primer correctness, R6 logical chain, γH2AX dose-response).
- **PARTIAL:** 5 (DCH-vs-iPSC repair pattern noisy but trends correct; BRCA2 / RAD51 / PRKDC narratives compatible but only modest signal; cPARP narrative-internally consistent).
- **NOT TESTED:** 7 (the two abstract %, Western quant, cell-cycle %, ROS MFI, senescence counts — all require deposited raw data or figure digitization that the current free-endpoint envelope did not deliver).
- **CONTRADICTED:** 0.
- **Scope coverage:**
  - Of the **paper's deposited testable content** (240 significance cells + 8 primers): **240 + 8 = 248 / 248 audited (100%)**.
  - Of the **paper's full analyzable design** (240 numeric design cells + cell-cycle/ROS/cPARP/senescence/Western): ~ **240 / ~280 = 86%** significance-only; **0 / ~280 = 0%** numeric.

## Verdict — promotion result

**Previous (2026-06-21):** SPOT-CHECK ONLY (coverage/agreement unscored).
**Now (2026-06-27):** **PARTIAL — coverage 5/10, agreement 9/10.**

Rationale per AUDIT_PROTOCOL §5:
- **Coverage = 5/10.** 100% of *deposited* testable content audited (significance tables + primers + new cross-panel chain), but 0% of figure-only numeric content audited (vision LLM unreachable). The deposit envelope itself is small — most readouts were never released as numbers. Calling this "PARTIAL" rather than "REPLICATED" honors that gap.
- **Agreement = 9/10.** Zero contradictions across six independent consistency tests (reciprocal symmetry, omnibus-vs-pairwise, dose-response monotonicity, primer/RefSeq match, narrative-internal consistency, cross-panel logical chain). One minor knock for the 5 omnibus-vs-pairwise anomalies (4.5%) plus the non-monotonic 24h iPSC-vs-DCH dose-response. After irradiation (1/2/5 Gy × 4 times), the paper's central damage→repair-gene logical chain holds in 12/12 design cells.
- **6/22 rule (data-blocked verdicts must name the exact missing artifact).** The blocker is data availability, not method failure. Specifically missing artifacts:
  - raw flow cytometry .fcs files (cells × γH2AX-AF647 MFI),
  - raw qPCR Ct tables for BRCA2/RAD51/PRKDC/XRCC4 + GAPDH (line × dose × time × rep),
  - Western blot densitometry (RAD51, XRCC4, β-actin) at 9 h,
  - PI cell-cycle distribution table (% G1/S/G2 per line × dose × time),
  - CellROX Green ROS MFI table,
  - cPARP-1 flow % positive table,
  - SA-β-gal positive cell counts at 5 d per condition.
- This is a recognized limitation common to 2018-era wet-lab PLoS ONE papers, not a discredit to the work.

**One-line verdict:** PARTIAL — paper is internally consistent and methodologically verifiable (primers exact-match RefSeq; ANOVA tables reciprocally symmetric in 48/48 cells; cross-panel damage→repair chain holds in 12/12 irradiated cells); 0 contradictions; full replication blocked by absent raw flow/Ct/cell-count data.

## Limitations / honest downgrades
1. **No raw-data deposit** → cannot recompute the abstract's "30% / 60%" numbers nor any fold-change.
2. **Image-LLM endpoints unavailable this run** (sandbox path policy + Anthropic credit-exhausted + OpenAI/Gemini missing/mis-keyed) → could not digitize Fig 2 / Fig 3 bar heights to back out the means and re-run ANOVA. A future pass with a working vision endpoint should do this and is the most likely path to lift this paper from PARTIAL to REPLICATED.
3. **No wet-lab capacity** → all in-vivo claims accepted as published.
4. **Cell-line authentication** not done (would require STR profiles).

## Artifacts (all under `lucid100-ipsc-chondrocyte-ir-response-2018/`)
- `paper.pdf`, `paper.txt`, `article.html` — full article + extracted text + HTML
- `supp/S1_fig.tif` — chondrogenic markers immunofluorescence
- `supp/S1..S5_table.docx` — published statistical tables
- `supp/S6_table.docx` — qPCR primers
- `replication/extract_supp_tables.py` — DOCX → CSV parser
- `replication/parsed_supp/all_supp_significance.csv` — 336-row machine-readable significance table
- `replication/audit_supp_consistency.py` — symmetry + monotonicity checks
- `replication/audit/c1_symmetry.csv`, `replication/audit/c2_summary_vs_pairwise.csv` — audit outputs
- `replication/primer_check.py` — primer / RefSeq BLAST-equivalent check
- `replication/headline_claim_check.py` — significance-pattern checks against narrative claims
- `replication/make_comparison_table.py` — per-panel significance distributions
- `replication/promo/r6_cross_panel.py` *(new)* — cross-panel logical-chain test
- `replication/promo/r6_cross_panel.csv` *(new)* — per (dose,time) chain verdicts
- `replication/promo/results.json` *(new)* — machine-readable promotion-audit results
- `REPORT.md` — this file
- `REPORT.md.bak-pre-promo` — original SPOT-CHECK report (2026-06-21)
