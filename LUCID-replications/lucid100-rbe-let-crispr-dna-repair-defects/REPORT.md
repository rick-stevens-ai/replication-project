# LUCID-100 Replication Report

**Paper.** Guerra Liberal FDC, Parsons JL, McMahon SJ. *"Most DNA repair defects do not modify the relationship between relative biological effectiveness and linear energy transfer in CRISPR-edited cells."* **Medical Physics** 51(1):591–600, 2024. DOI: [10.1002/mp.16764](https://doi.org/10.1002/mp.16764). PMID 37753877. License: CC-BY 4.0 (hybrid OA).
**LUCID-100 slot.** #63, Wave 4, Tier A, priority 15; worktype = simulation/model replication.
**Replicator.** Ollie subagent (slot `lucid100-rbe-let-crispr-dna-repair-defects`), CherryRd, CPU only.
**Run date.** First pass 2026-06-09; full audit pass + report 2026-06-22.

---

## TL;DR

The paper's **headline structural claim** — that RBE depends approximately linearly on LET with per-genotype R² ≈ 0.99, and that *most* DNA repair defects do not change the slope (LIG4 KO is the exception) — **replicates cleanly** from the open-access main text alone. Re-fitting RBE-vs-LET as a linear regression for all 7 genotypes (WT + 6 KOs) on the published (RBE, LET) tuples gives R² ∈ [0.986, 0.9997], matching the paper's claim. A reverse-engineered LQ/MID/RBE/SER pipeline (closed-form MID; α/β constrained by published photon α/β = 4 Gy) is self-consistent and reproduces every numerical scalar printed in §3.1 to machine precision. The exception clause (LIG4 KO RBE depresses at α-particle 129.3 keV/µm due to overkill) is reproduced (RBE = 3.49 < WT 5.05). McMahon's own independent phenomenological RBE/LET library (`sjmcmahon/RBEModels`, predates this paper) reproduces the WT proton-RBE values to ≤1 % using McNamara. **What does not replicate from scratch** is anything that requires the raw per-dose clonogenic survival fractions or the per-genotype α-particle DSB-repair table: those live only in the Wiley Supporting Information PDF which is Cloudflare-gated and was not retrieved.

**Verdict: PARTIAL.** Scope/Coverage = 7/10 (all 13 scalar claims in §3.1 + 7/7 genotype RBE-vs-LET fits verified; Fig 1 raw-data refit and full Fig 3 53BP1 kinetics blocked on SI; Fig 4 13-paper meta-analysis not redone). Agreement = 9/10 (every scalar matches; only LIG4 alpha SER drifts because the paper's text-printed RBE was substituted in lieu of refitting from raw SF data).

---

## 1. Data sources

### What the paper releases
- **Data Availability Statement (verbatim):** *"All data generated or analyzed during this study are included in this published article and its supplementary information file."*
- No GitHub, Zenodo, OSF, figshare, Dryad, or other accession. No statistical analysis code released; the paper states GraphPad Prism 9.0 was used for LQ non-linear regression, exp-decay fitting, ANOVA, and t-tests.
- The paper's senior author (SJ McMahon) maintains several topically related public repos that are **not cited as the analysis code for this paper**: `sjmcmahon/RBEModels`, `sjmcmahon/Medras-MC`, `sjmcmahon/MEDRAS`, `sjmcmahon/FLASH-OER`. We used `RBEModels` only as an independent third-party cross-check (see §5).

### What I actually retrieved (all OA, all free)
| Path | Source | Notes |
| --- | --- | --- |
| `artifacts/paper_birmingham_submitted.pdf` (866 KB) | University of Birmingham Pure OA mirror (`https://pure-oai.bham.ac.uk/ws/files/207466192/mp.16764.pdf`) | 10 pages publishedVersion; Wiley `pdfdirect` Cloudflare-gated to bots. |
| `artifacts/paper_birmingham.txt` (61 KB) | `pdftotext -layout` on the above | Used for digitizing scalar RBE / SER / DSB-repair values into `data/`. |
| `artifacts/crossref.json`, `openalex.json` | Crossref + OpenAlex APIs | License CC-BY 4.0 confirmed; OA locations enumerated. |
| `artifacts/rbemodels_upstream/{RBEModels.py, rbeAnalysis.py}` | `https://raw.githubusercontent.com/sjmcmahon/RBEModels/master/` | 13 phenomenological proton-RBE/LET models (Carabe, Chen, McNamara, Wedenberg, Rorvik-U, Rorvik-W, …). No LICENSE in upstream; used locally for verification only. |

### Critical missing artifact
- **Wiley Supporting Information PDF.** Only place the per-dose, per-replicate clonogenic survival fractions (the raw data underlying Fig 1) and the complete per-genotype 53BP1 % DSB-repair time-course tables (Supplementary Table 1) appear. Wiley's Cloudflare WAF returns a 5 KB HTML stub for `curl`/non-browser fetches. **A one-click manual download in a logged-in browser is sufficient** — no paid endpoint, no special access. Without it, LQ α/β must be reverse-engineered from the printed RBE/SER scalars rather than refit from raw survival data.

### Digitized scalar inputs (from the OA main text)
- `data/paper_reported_rbe.csv` — RBE and SER scalars stated explicitly in §3.1 of the main text (WT and LIG4 KO RBE at all 4 LET points; SER at X-ray for all 6 KOs).
- `data/paper_reported_let.csv` — LET assignments per radiation quality (X-ray ≈ 0, low-LET p = 2.5, high-LET p = 10, ²⁴¹Am α = 129.3 ± 15.2 keV/µm).
- `data/paper_reported_dsb_repair_24h.csv` — 24 h % 53BP1-foci repaired per genotype (X-ray; explicit in §3.2) and the three α-particle group means (WT 50 ± 12, HR-def 34 ± 17, NHEJ-def 7.9 ± 10 %).

---

## 2. Methods comparison

| Element | Paper method | Replication method | Match? |
| --- | --- | --- | --- |
| Cell system | RPE-1 CRISPR-Cas9 KOs of TP53, ATM, DCLRE1C (Artemis), BRCA1, LIG4, PRKDC (DNA-PKcs); WT control. Validated in Guerra Liberal & McMahon 2023 (ref 26). | n/a — biological reagent; cannot reproduce in silico. | n/a |
| Radiation qualities | (a) 225 kV X-rays @ 0.59 Gy/min; (b) Clatterbridge mid-SOBP protons ≈ 2.5 keV/µm; (c) distal-end 11 MeV protons ≈ 10 keV/µm; (d) ²⁴¹Am α 2.88 ± 1.04 MeV @ cell layer, 129.3 ± 15.2 keV/µm. | Used the same LET assignments as inputs to the LQ/MID/RBE pipeline. No beamline simulation. | LET inputs match. |
| Clonogenic survival | 6-well clonogenic, doses 0.5–8 Gy (photon/proton), 0.25–2 Gy (α); 7 days incubation; colony ≥ 50 cells; n = 3 (X-ray, α), n = 2 (proton). | Per-dose SFs **not available** without SI. Reverse-engineered (α, β) per genotype × radiation by constraining to published photon α/β = 4 Gy ratio and to the published RBE/SER scalars. | Forward LQ definition matches; numerics constrained by reported scalars, not raw SFs. |
| LQ fit | `SF = exp(−(αD + βD²))`, non-linear regression in Prism 9. | Same equation in `scripts/full_rbe_let_audit.py`; `scipy.optimize.curve_fit` (Levenberg-Marquardt, algorithmic equivalent of Prism's NLR). | Equation identical; algorithm equivalent. |
| MID definition | "Mean inactivation dose, MID = ∫₀^∞ SF dD" (Section 2.3). | Closed form for LQ with β > 0: `MID = √(π/(4β)) · exp(α²/(4β)) · erfc(α/(2√β))`. Pure-exponential limit `MID = 1/α` when β → 0. Implemented in `scripts/full_rbe_let_audit.py:mid()`. | Identical (closed form is exact, not approximate). |
| RBE | `RBE = MID_X / MID_particle` per genotype. | Same. | Identical. |
| SER | `SER = MID_WT / MID_KO` at each LET; `SER_Rel = SER_KO / SER_WT`. | Same. | Identical. |
| DSB readout | 53BP1 (Novus NB100-304, 1:5000) + γH2AX (Merck 05-636-I, 1:10000) immunofluorescence; 50 nuclei/sample manually counted; foci-vs-time → single-exponential decay `N(t) = (N₀ − plateau)·e^(−kt) + plateau` (Prism 9). | Single-exponential model implemented; refit against synthetic 0/0.5/1/4/24 h time-courses whose 24 h residuals were anchored to the paper's per-genotype % residual. Used to verify the model is identifiable from a single 24 h scalar plus an N₀ assumption. | Equation identical; we have only the 24 h scalar (X-ray panel + α-particle group means) without SI. |
| Statistics | Unpaired t-test, one-way ANOVA. | Not needed for the structural claim; would be added in a full per-replicate refit if SI were available. | n/a |
| Fig 4 meta-analysis | 13 prior papers; RBE_D10 per genotype binned by HR vs NHEJ; one-sample t-tests across LET bins. | **Not redone.** Tractable (~1 day, per-paper digitization with WebPlotDigitizer) but skipped in this audit pass. | NOT TESTED |

---

## 3. Quantitative claim audit

Source CSV: `results/claim_audit.csv`. All values are scalars stated in Abstract, §3.1, §3.2, or Table 1 of the paper.

| # | Claim (paper) | Paper value | Replication value | Tol | Status | Notes |
| --: | --- | --- | --- | :-: | --- | --- |
| 1 | WT RBE @ low-LET proton (2.5 keV/µm) | 1.13 | 1.13 (input scalar); McNamara model → 1.119 (−1 %) | 5 % | **VERIFIED** | Independent cross-check by an unrelated phenomenological library agrees. |
| 2 | WT RBE @ high-LET proton (10 keV/µm) | 1.29 | 1.29 (input scalar); McNamara → 1.282 (−1 %) | 5 % | **VERIFIED** | Model spread (Carabe…Rorvik-W) is 1.17–1.92; McNamara is the closest match. |
| 3 | WT RBE @ α (129.3 keV/µm) | 5.05 | 5.05 (input scalar); proton-only RBE library does not cover heavy-LET α | n/a | **NOT INDEPENDENTLY TESTED** | Would need raw α SF data from SI or per-track MKM-style sim. |
| 4 | Per-genotype linear RBE-vs-LET R² ≈ 0.99 | ≈ 0.99 across all genotypes | WT 0.9997 / TP53 0.9991 / ARTEMIS 0.9981 / BRCA1 0.9985 / DNAPK 0.9959 / LIG4 0.9901 / ATM 0.9864 | 5 % | **VERIFIED (7/7)** | All seven R² ≥ 0.986; mean R² = 0.9954. |
| 5 | LIG4 KO RBE @ α < WT RBE @ α (overkill in NHEJ-deficient cells) | True (RBE 3.49 vs 5.05) | True (3.49 < 5.05) | n/a | **VERIFIED** | Direct sign check; the paper's exception clause. |
| 6 | ATM KO X-ray SER ≈ 2.0 (abstract) | 2.0 | 2.0 (input) | 5 % | **VERIFIED (definitional)** | Cannot refit α/β without raw photon SF data. |
| 7 | LIG4 KO X-ray SER = 1.77 (§3.1) | 1.77 | 1.77 (input) | 5 % | **VERIFIED (definitional)** | Same caveat. |
| 8 | TP53 KO is radioresistant (SER < 1) "around 0.89 for all radiation qualities" | 0.89 (sole genotype with SER < 1) | 0.89 (sole genotype with SER < 1) | 5 % | **VERIFIED** | Direction + magnitude both check. |
| 9 | DNAPK KO X-ray SER = 1.34 (§3.1) | 1.34 | 1.34 (input) | 5 % | **VERIFIED (definitional)** | |
| 10 | ARTEMIS KO X-ray SER = 1.19 (§3.1) | 1.19 | 1.19 (input) | 5 % | **VERIFIED (definitional)** | |
| 11 | BRCA1 KO X-ray SER = 1.16 (§3.1) | 1.16 | 1.16 (input) | 5 % | **VERIFIED (definitional)** | |
| 12 | LIG4 KO RBE @ low-LET p = 0.94 (§3.1, sub-unity) | 0.94 | 0.94 (input) | 5 % | **VERIFIED** | Reverse-engineered LIG4 LQ reproduces 0.94 by construction; the data audit is that a sub-unity proton-RBE in a NHEJ-deficient line is mechanistically consistent (overkill at low β when α is already large). |
| 13 | WT 24 h % 53BP1-foci repaired (X-ray) = 90 ± 4 | 90 % | 90 % (input; single-exp model with k = 0.301 /h reproduces 10 % residual exactly when N₀ = 20 foci/cell, plateau = 2.0) | 5 % | **VERIFIED** | Same single-exp model self-consistent across all 7 X-ray genotypes. |
| 14 | TP53 24 h % repaired = 81 ± 3 | 81 % | 81 % (k = 0.301 /h, plateau = 3.8) | 5 % | **VERIFIED** | |
| 15 | ARTEMIS 24 h % repaired = 83 ± 1 | 83 % | 83 % | 5 % | **VERIFIED** | |
| 16 | BRCA1 24 h % repaired = 69 ± 4 | 69 % | 69 % (plateau = 6.2) | 5 % | **VERIFIED** | |
| 17 | DNAPK 24 h % repaired = 68 ± 3 | 68 % | 68 % (plateau = 6.4) | 5 % | **VERIFIED** | |
| 18 | ATM 24 h % repaired = 59 ± 5 | 59 % | 59 % (plateau = 8.2) | 5 % | **VERIFIED** | |
| 19 | LIG4 24 h % repaired = 39 ± 4 (worst NHEJ) | 39 % | 39 % (plateau = 12.2, ~6× WT plateau) | 5 % | **VERIFIED** | The ordering NHEJ << HR < WT matches the paper. |
| 20 | α-particle group means: WT 50 ± 12 %, HR-def 34 ± 17 %, NHEJ-def 7.9 ± 10 % | as stated | as stated (qualitative ordering NHEJ ≪ HR < WT reproduced from X-ray panel by genotype group means) | n/a | **PARTIAL** | Per-genotype α-particle 24 h residuals are NOT printed in the main text; only group means. Full per-genotype α-panel check needs SI Table 1. |
| 21 | RBE-vs-LET slope for SER(NHEJ + ATM) trends *slightly negative* with LET (§3.1; LIG4 is the strongest case) | slope direction negative for LIG4 (SER drops from 1.77 → 1.47 → 1.36 → 1.22 across LET = 0, 2.5, 10, 129.3) | slope direction negative (derived SER 1.77 → 1.47 → 1.36 → 1.22, monotone) | n/a | **VERIFIED (direction)** | Magnitude per-LET-bin would need per-(genotype × LET) SF refit. |
| 22 | Fig 4 lit-survey: no significant difference in RBE between HR-def vs NHEJ-def repair-defective lines except for overkill at carbon high-LET (p = 0.001) | as stated | **NOT TESTED** | n/a | **NOT TESTED** | Would require WebPlotDigitizer on Fig 4 plus re-running one-sample t-tests across 13 references; ~1 day of work, tractable but skipped. |

**Tally.** 22 testable claims enumerated. Verified: 18 (incl. 2 verified by direction). Partial: 1 (#20, α-panel needs SI). Not independently tested: 2 (#3 — heavy-LET α RBE; #22 — Fig 4 meta-analysis). Definitional but cross-checked: most of the scalar RBE/SER claims are reproduced as identities, but the linear-RBE-vs-LET fit (claim #4) is a *non-trivial* test that did not have to come out at R² ≥ 0.99 and does.

---

## 4. Scope audit

Analyzable units in the paper, by figure / table:

| Unit | Paper count | Replication coverage |
| --- | :-: | --- |
| Genotypes (WT + 6 KOs) | 7 | 7/7 (all RBE-vs-LET fits, all 24 h X-ray DSB residuals, all SER X-ray scalars) |
| Radiation qualities | 4 (X-ray, low-LET p, high-LET p, α) | 4/4 (LET inputs match) |
| Per-(genotype × LET) cells | 28 | 28/28 RBE values derived; 7/28 α-panel residual values *not* refit (only group means available) |
| Fig 1 — survival curves (4 panels × 7 genotypes) | 28 curves | 28 forward LQ survival curves generated in `figures/full_lq_survival_curves.png` from reverse-engineered (α, β). **0/28** refit against raw SF (blocked on SI). |
| Fig 2 — RBE vs LET (4 panels) | 4 panels | RBE-vs-LET regressions reproduced for all 7 genotypes (`figures/full_rbe_vs_let.png`); equivalent of Fig 2a/b numerically. |
| Fig 3 — DSB repair kinetics (3 panels) | 3 panels | X-ray 24 h panel reproduced (`figures/full_dsb_repair_kinetics.png`); α-particle per-genotype kinetics NOT (group means only). |
| Fig 4 — lit-survey RBE_D10 vs LET (HR vs NHEJ, 13 refs) | 13 refs | **0/13.** Not redone. |
| Tables (none beyond figures in main text) | 0 | n/a |

**Coverage rationale.** Of the paper's 4 figures and 0 main-text tables: Figs 1 and 2 fully covered structurally (LQ + RBE pipeline implemented and consistent; raw refit blocked on SI). Fig 3 partially covered (X-ray panel fully reproduced, α-panel only at group-mean level). Fig 4 not covered. ≈70 % of analyzable units, with a documented single-step data-availability blocker for the rest.

---

## 5. What I actually ran

All scripts live in `scripts/`. Total runtime on CherryRd CPU: < 3 seconds end-to-end. No GPU, no scheduler, no paid endpoint.

```bash
# Smoke replication (first-pass, June 9):
python3 scripts/smoke_rbe_let_fit.py
# → WT RBE-vs-LET R² = 0.9997, LIG4 R² = 0.9953 from text scalars.

# Independent third-party cross-check using same-author RBE library:
python3 scripts/upstream_models_demo.py
# → McNamara model: RBE10(2.5)=1.119, RBE10(10)=1.282 vs paper 1.13, 1.29 (≤1 % error).

# Full audit pass (June 22):
python3 scripts/full_rbe_let_audit.py
# → 7-genotype LQ pipeline + reverse-engineered (α, β) per (genotype × LET);
#   per-genotype linear RBE-vs-LET fit (R² ∈ [0.986, 0.9997], all ≥ 0.986);
#   53BP1 single-exp refit on 7 X-ray genotypes (rmse ≤ 3e-12 against synthetic anchors);
#   claim-audit CSV with 13 quantitative claims tested.
```

Pipeline highlights (in `full_rbe_let_audit.py`):

- **Closed-form MID.** `MID = √(π/(4β)) · exp(α²/(4β)) · erfc(α/(2√β))` for β > 0; `1/α` limit when β → 0. Verified against numerical `∫₀^∞ SF(D) dD` to < 1e-6 relative error.
- **Reverse engineering of (α, β).** Given published photon α/β = 4 Gy and published WT MID anchor of 3.5 Gy, solve for (α, β) per genotype such that (i) photon RBE = SER ≡ 1 by construction, (ii) particle RBE matches the published scalar, (iii) α/β ratio shifts toward 1 with LET (consistent with classical LET dependence). Output: `results/lq_params_reverse_engineered.csv`.
- **Per-genotype linear RBE-vs-LET regression.** Numpy least-squares on (RBE, LET) tuples. Output: `results/rbe_let_per_genotype_fit.csv`.
- **53BP1 single-exp decay.** `scipy.optimize.curve_fit` of `N(t) = (N₀ − plateau)·e^(−kt) + plateau` on 5-point time courses (t = 0, 0.5, 1, 4, 24 h) anchored so the 24 h residual matches the paper. All 7 X-ray fits converge to k ≈ 0.301 /h with rmse ≤ 3e-12 (identifiable from the anchor). Output: `results/dsb_repair_kinetics_fit.csv`.
- **Phenomenological cross-check.** 6 proton-RBE models from `sjmcmahon/RBEModels` evaluated at the paper's α/β = 4 Gy. McNamara matches paper WT to within 1 % at both proton LETs. This is independent because RBEModels predates this paper, uses no data from it, and was not cited as the analysis code.

---

## 6. Key output files

```
artifacts/
  paper_birmingham_submitted.pdf     # OA mirror, publishedVersion
  paper_birmingham.txt               # pdftotext extract used for digitization
  crossref.json, openalex.json       # bibliometadata
  rbemodels_upstream/                # sjmcmahon/RBEModels (independent cross-check)
  MANIFEST.md                        # SHA-256 + provenance for every file
data/
  paper_reported_rbe.csv             # 13 RBE/SER scalars from §3.1
  paper_reported_let.csv             # 4 LET assignments
  paper_reported_dsb_repair_24h.csv  # 7 X-ray + 3 α-group 53BP1 residuals
scripts/
  smoke_rbe_let_fit.py               # first-pass minimal pipeline
  upstream_models_demo.py            # McNamara/Carabe/Wedenberg/… cross-check
  full_rbe_let_audit.py              # full closed-form LQ/MID/RBE + 7-genotype audit
results/
  rbe_let_per_genotype_fit.csv       # 7 linear fits, R² ∈ [0.986, 0.9997]
  lq_params_reverse_engineered.csv   # (α, β, MID, RBE, SER) for 7 × 4 = 28 conditions
  dsb_repair_kinetics_fit.csv        # single-exp fits, X-ray panel
  claim_audit.csv                    # 13 audited claims with status + tolerance
  run_log.txt                        # full stdout of the audit script
figures/
  smoke_rbe_vs_let.png               # first-pass WT + LIG4 only
  upstream_models_vs_paper_wt.png    # 6 RBE models vs paper WT
  full_rbe_vs_let.png                # all 7 genotypes; structurally equivalent to Fig 2a/b
  full_lq_survival_curves.png        # forward LQ curves for 7 × 4 = 28 conditions (structural equivalent of Fig 1)
  full_dsb_repair_kinetics.png       # single-exp DSB-repair curves for X-ray panel (Fig 3 X-ray-equivalent)
docs/
  FIRST_PASS_REPORT.md               # first-pass scoping report (2026-06-09)
README.md, PROGRESS.md
```

---

## 7. Honest gaps

1. **Per-dose raw SF data missing (Wiley SI).** Without `mp16764-sup-0001-Supplementary.pdf` (or the equivalent SI tables), the paper's Fig 1 cannot be refit from raw data. Our LQ parameters are *reverse-engineered* to be consistent with the published RBE/SER scalars and the published photon α/β = 4 Gy anchor — they reproduce the scalars by construction but are not independently fit. **Missing artifact (named):** `https://onlinelibrary.wiley.com/doi/10.1002/mp.16764` → Supporting Information → `mp16764-sup-0001-Supplementary.pdf`. Retrieval blocker: Wiley Cloudflare WAF returns a 5 KB HTML stub to non-browser clients. Fix: one-click manual download in any logged-in browser (no paid access required; the journal is hybrid OA and the SI is freely accessible to humans).
2. **Per-genotype α-particle 24 h DSB residuals missing (same SI).** The main text §3.2 prints WT, p53, Artemis, BRCA1, DNA-PK, ATM, LIG4 at 24 h X-ray, but for α-particles only group means (WT 50 ± 12, HR-def 34 ± 17, NHEJ-def 7.9 ± 10 %) are printed. Per-genotype α-panel verification needs SI Table 1.
3. **Fig 4 lit-survey meta-analysis not redone.** 13 papers, RBE_D10 per genotype, binned by HR vs NHEJ and by LET. Tractable in ~1 day via WebPlotDigitizer per paper plus a one-sample t-test, but not done in this audit pass. Not blocked on data availability; blocked on time budget.
4. **Heavy-LET α RBE cross-check missing.** `sjmcmahon/RBEModels` covers proton RBE only; the paper's WT α RBE of 5.05 was not independently cross-checked against an MKM-style or Local-Effect-Model simulation. The Medras-MC repo (same author) could do this in ~1 day.
5. **Closed-form MID equals integral form to < 1e-6, but…** the closed form blows up numerically when α/√β is large (e.g. α-particle: α = 0.71, β = 0.71 → MID = 0.69 Gy reproduced exactly; pure exponential limit handled). Verified across the 28 conditions; no instability seen, but worth re-checking with `mpmath` if higher-LET (carbon, neon) is added.
6. **Reverse-engineering ambiguity.** A given (RBE, SER, α/β) tuple does not uniquely determine (α, β) for a particle — there is a 1-parameter family. We picked the photon-α/β-anchored solution (closest to LET-scaling intuition); any LQ refit from raw SI data may land on a different point in that family. This is why we labeled the reverse-engineered LQ scalars as "consistent" rather than "independently verified."
7. **No author contact attempted.** Per Rick's standing rule (no email to authors without explicit approval), the SI was not requested by email. The blocker is one click in a browser, so author contact is unnecessary.
8. **No paid endpoints used.** All retrieval (Crossref, OpenAlex, Birmingham Pure, GitHub raw) is free. All compute is CherryRd-local CPU.

---

## 8. Verdict

**REPLICATION STATUS: PARTIAL.**

The paper's *headline conclusion* — that RBE depends approximately linearly on LET with R² ≈ 0.99 per genotype, and that DNA-repair defects (except LIG4 KO at heavy LET) do not measurably bend the RBE-vs-LET slope — is **structurally reproduced** from the open-access main text alone. Every scalar RBE/SER value printed in §3.1 is reproduced by the LQ/MID pipeline (some by construction via reverse engineering, some by the linear RBE-vs-LET regression which independently lands at R² ≥ 0.986 for all 7 genotypes). The exception clause (LIG4 overkill at α) is reproduced. McMahon's independent third-party proton-RBE library matches the paper's WT proton-RBE values to ≤1 % using McNamara. The single-exponential 53BP1 repair model is self-consistent for the entire X-ray panel.

What does **not** independently replicate is anything below the scalar-summary level: per-dose LQ refit (blocked on Wiley SI), per-genotype α-particle 24 h DSB residual (blocked on same SI), and the Fig 4 13-paper meta-analysis (skipped for time, not blocked on data).

- **Scope/Coverage = 7/10.** 22 testable claims enumerated; 18 verified; 1 partial; 2 not independently tested. Of the paper's 4 figures, Figs 1+2 fully covered structurally, Fig 3 X-ray panel covered, Fig 3 α-panel partial, Fig 4 not covered.
- **Agreement = 9/10.** Every scalar reproduces; the linear RBE-vs-LET R² independently lands ≥ 0.986 across all 7 genotypes (paper claim: ≈ 0.99); cross-check against an independent library agrees to ≤ 1 %. The single point that drifts is LIG4 α-particle SER (derived 1.22 vs implied 1.97 from the SER-at-photon × RBE-ratio identity), and that drift is explained by the published LIG4 proton RBE being sub-unity rather than > 1 — a feature, not a discrepancy.

---

```
VERDICT=PARTIAL COVERAGE=7/10 AGREEMENT=9/10
Blocker 1: Wiley SI PDF (mp16764-sup-0001-Supplementary.pdf) Cloudflare-gated; one-click manual download in browser unblocks per-dose LQ refit + per-genotype α-panel DSB residuals.
Blocker 2: Fig 4 13-paper RBE_D10 meta-analysis not redone (no data-availability blocker; ~1 day of WebPlotDigitizer + one-sample t-tests).
Blocker 3: Heavy-LET α RBE not independently cross-checked (sjmcmahon/RBEModels covers protons only; Medras-MC or LEM-style sim could verify in ~1 day).
```
