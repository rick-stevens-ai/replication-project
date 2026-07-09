# FIRST_PASS_REPORT — LUCID100 slot 59

**Paper:** Brahme A. (2026) "Improving radiation therapy efficacy considering DNA repair, TP53 mutations, microscopic heterogeneity, and low- and high-dose apoptosis." *Front. Oncol.* 15:1703503. doi:10.3389/fonc.2025.1703503

**Worktype (master TSV):** `omics/signature replication`
**Worktype (actual):** **mechanistic / radiotherapy theory review** — single-author narrative review by Anders Brahme synthesising his "repairable–homologous–repairable" (RHR) DNA-damage-repair formulation, the dual-double-strand-break (DDSB) δ-ray physics he has previously published, and his clinical-fractionation / light-ion-roundup recommendations. **Retag recommended.**

**Verdict:** **GO — smoke-only / reduced replication**.

---

## 1. Paper structure

22-page, single-author, open-access (CC-BY) review with 18 figures, 1 table, 107 references. Sections:

1. Introduction
2. The DDSB δ-ray mechanism and its dose / LET dependence
3. (Table 1) — 15 narrative reasons δ-ray DDSBs dominate biological effectiveness
4. Radiation biology of TP53 in tumor vs normal tissue
5. RHR repair formulation, LDHS / LDA / HDA
6. Optimal weekly fractionation schedule
7. Light-ion therapy with low-LET "roundup"
8. Low- and high-LET secondary cancer risks
9. Adaptive biologically-optimised IMRT (BIOART)

No "Methods", no "Data availability", no "Code availability", no supplementary materials.

## 2. What is mathematically reproducible *from this paper alone*

Exactly one explicit equation:

> **Equation 1** (extreme-value / Gumbel rewriting of the Poisson TCP):
>
> `TCP(D) = exp( -exp( (m - D)/v ) ) = exp( -exp( (D0·ln N0 - D)/D0 ) ) = exp( -N0·exp(-D/D0) )`

with the explicitly stated statistical constants:

| Quantity | Paper's value | Smoke script value |
|---|---|---|
| Mean dose D̄ | `m + v·γ = D0·(ln N0 + γ)` | matched analytically |
| Median D50 | `D0·ln(N0 / ln 2)` | matched analytically |
| Variance | `π²·D0² / 6` | matched analytically |
| Relative SD σ_D / D̄ (for N0 = 10⁷) | ≈ 0.0768 (7.7 %) | **0.076821** ✔ |
| Skewness | ≈ 1.1395 | **1.139547** ✔ |
| Kurtosis | 5.4 | **5.400000** ✔ |
| TCP at analytic D50 | 0.5 by construction | 0.500136 ✔ (grid resolution) |
| Algebraic-form consistency | should be identical | max abs diff 3.3 × 10⁻¹⁶ ✔ |

`code/tcp_extreme_value_smoke.py` runs in <1 s on CPU and writes `results/tcp_eq1_smoke.json`, `figures/tcp_eq1_vs_dose.png`, `logs/tcp_eq1_smoke.log`. **All four numerical claims that the paper makes about Eq. 1 reproduce to ≥4 decimal places.**

## 3. What is *not* reproducible from this paper alone

Everything else of interest:

- The **RHR cell-survival formula** itself (only named; the equation is referenced as "(9): Figure 49" and "(7)" — Brahme's textbook / 2022 *Radiat Res* paper).
- The **CDN1 ("closest distance norm") fitting procedure** used for Figs 9, 10, 13, 17, 18 — explicitly cited as "(7, 9, 10): details there".
- The **apoptosis decomposition** (LDA, HDA, non-apoptotic misrepair) — formulas in refs (1, 7).
- The **optimal weekly fractionation P+ gains** (~12 %) of Fig. 14 — derived in refs (1, 3, 9, 78).
- The **secondary-cancer-risk model** in Figs 17–18 — uses ref (2) Eq. (10).
- All **experimental data points** plotted in Figs 5–18 — re-used from prior Brahme publications and from Hat (2016), Marples / Joiner LDHS literature, etc., none included as machine-readable supplements.
- Microscopic heterogeneity calculations (Figs 4, 11, 12) — refer to prior Monte Carlo work.

## 4. Openness scorecard

| Item | Status |
|---|---|
| Paper open access | ✅ CC-BY (Frontiers) |
| Supplementary materials | ❌ None |
| Code released by author | ❌ None (verified by full-text grep + landing-page inspection) |
| External data needed for full repro | Yes — Brahme's prior book + ≥4 of his prior papers (refs 7, 9, 10, 15); none currently in this workspace |
| Endpoints used | Free only (local CPU, no LLM, no paid API) |
| Openness score (1–5) | **2** (paper open, methods/data/code closed behind author's prior books and the "see ref X" pattern) |

## 5. Feasibility check for this slot's task brief

- "**equations / parameters / figures / tables**": Eq. 1 fully reproduced + 1 narrative table summarised. Figures 1–18 are *narrative* schematics of pre-existing curves, not self-contained datasets in this paper.
- "**public code / data availability**": Verified zero (no GitHub, Zenodo, OSF, supplementary, or data-availability statement appears in the text).
- "**whether a reduced model / equation / table / figure smoke replication is feasible**": **Yes for Eq. 1 (done).** Not feasible for the RHR fits or Fig. 14 weekly schedule without pulling refs 7 / 9 / 10 / 15.
- "**verify worktype**": Original tag `omics/signature replication` is wrong. **Retag to `mechanistic / radiotherapy theory review (RHR / extreme-value TCP)`.**

## 6. Recommendations / next actions

- ✅ **Done in this pass:** smoke replication of Eq. 1, manifest, README, progress JSON, retag flag.
- **No author contact** (per task brief).
- **No paid endpoints** used.
- **No heavy compute** needed — smoke ran on CPU in well under 1 s. No HPC job plan necessary.
- Optional future work (out of scope for this 1-shot slot):
  - Retrieve Brahme (2022, *Radiat Res*, ref 15) for the RHR survival formula and parameter table.
  - Retrieve Brahme's textbook (refs 7, 9) for the LDA/HDA decomposition.
  - Re-run a fuller cell-survival smoke once those parameters are in hand.
  - Cross-link to the existing `lucid-p53-repair/` slot (same workspace) which appears to overlap on the TP53 ↔ DDR theme.

## 7. QA back-channel

- **KEEP** the paper in LUCID100 — it is on-theme.
- **RETAG** worktype: `omics/signature replication` → `mechanistic / radiotherapy theory review (RHR / extreme-value TCP)`.
- **Flag** that the paper is a single-author conceptual review whose ambitious sections all defer to the same author's prior closed-source book/papers; treat as "concept paper, not a primary modelling paper".
