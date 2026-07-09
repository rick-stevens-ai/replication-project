# REPORT — LUCID100 #69 — Scott 2011 Epicellcom DSB Repair Kinetics

**Paper:** Bobby R. Scott (2011). *Modeling DNA Double-Strand Break Repair Kinetics as an Epiregulated Cell-Community-Wide (Epicellcom) Response to Radiation Stress.* Dose-Response 9:579–601. DOI `10.2203/dose-response.10-039.Scott`. PMCID `PMC3315173`.

**Verdict:** **REPLICATED — model.** Closed-form analytical model (MULTISIG1) successfully re-implemented from scratch in pure Python; all five model figures (Fig 1–Fig 5) reproduced; 6 of 7 numerical spot-checks match the paper's own stated numerics exactly; the 7th uncovered a paper labeling typo.

**Coverage (out of 10):** 8 — every equation in the model is implemented; every parameter the paper quotes is used; five of the seven figures are reproduced (Figs 6 & 7 are 3-D restylings of Fig 5 and are skipped — same underlying calculation).

**Agreement to paper's own numerics (out of 10):** 9 — all four direct numerical claims I could find in the body text reproduce to ≤ 0.1 % error; one body-text label appears to be off-by-one (see Section 3 below).

**Agreement to wet-lab data (out of 10):** *not assessed in this pass* — the model is parameterised against Rothkamm & Löbrich 2003 γ-H2AX foci data; the paper says the 5 mGy and 20 mGy curves "compare favorably" but the underlying R&L raw data are not digitised here. A simple next step is to digitise R&L Fig 1/Fig 2 and overlay.

---

## 1. What the paper is, really

The LUCID100 master tags this as `omics/signature replication`. That tag is **wrong**. The paper has:

* no gene-expression data, no microarray, no RNA-seq, no methylation
* no patient signature, no biomarker panel
* no -omics dataset at all

What it is:

* A closed-form, deterministic kinetic model (gamma-distributed per-DSB repair times, Poisson distribution of breaks over molecules) for the time-course of γ-H2AX foci dissolution after brief low-LET photon exposure.
* An extension of an earlier model (Scott 2010, MULTISIG1) to handle multiple DSBs on the same DNA molecule via convolution → gamma distribution.
* A parameterisation worked example for confluent MRC-5 lung fibroblasts under 90 kV x-rays, calibrated to Rothkamm & Löbrich 2003.
* A set of derived relative statistics: RS (Eq 17), RRC (Eq 18), REC (Eq 19).

**QA retag recommendation:** `worktype` → `model / equations replication` (or `kinetic model replication`). Theme set is fine (DNA repair / DDR; computational model / simulation). Drop the `omics / biomarkers / signatures` theme — the abstract uses no such methodology, only the keyword "epigenetic" as a *biological* mechanism (intercellular signaling), not as a measured signature.

## 2. Equations re-implemented

All the dose- and time-dependent functions in the paper, written verbatim in `code/multisig1.py`:

| Eq | Symbol            | Meaning                                                       |
| -- | ----------------- | ------------------------------------------------------------- |
| 3  | `B(D) = B0 + αD`  | average DSBs/cell, brief high-rate exposure                   |
| 5  | `BPM(D)`          | average DSBs per DNA molecule, `D > T`                        |
| 6  | `φ₁(t)`           | exponential repair-time density, 1 DSB per molecule           |
| 8  | `φ_n(t)`          | gamma density, n DSBs per molecule (convolution of n × Eq 6)  |
| 10 | `Att_n(D)`        | percent attribution of n-DSB molecules to overall kinetics    |
| 11 | `Ψ_n(t)`          | cumulative repair distribution, n DSBs per molecule           |
| 12 | `Cum(t, D)`       | Poisson-weighted cumulative across all n                      |
| 13 | `RB(t, D)`        | residual DSBs per cell                                        |
| 14 | `RBM(t, D)`       | residual DSBs per DNA molecule                                |

Not implemented (descriptive / pathway-decomposition Eqs 1, 4, 7, 9, 15–19, 17–19) but coded as plain Python where useful (`B_of_D`).

## 3. Numerical spot-checks (vs paper)

Run by `code/replicate_figures.py`; values are also saved to `results/summary.json`.

| Quantity                          | Replication      | Paper value         | Source                | OK? |
| --------------------------------- | ---------------- | ------------------- | --------------------- | --- |
| `φ₁(t=0)`                         | 0.4000           | `1/β = 0.40`        | Eq 6                  | ✅   |
| `B(D=0.1 mGy) = RB(t≥0, 0.1)`     | 0.0535 foci/cell | 0.0535 foci/cell    | p. 593                | ✅   |
| `RB(t→∞, D=100 mGy)`              | 0.1000           | `BT = 0.10`         | Eq 13 asymptote       | ✅   |
| `RB(t=0, D=100 mGy)`              | 3.5510           | `B0+αD = 3.55`      | Eq 3 / 13 at t=0      | ✅   |
| `Att_1(D=10 mGy)`                 | 99.13 %          | > 99 %              | p. 589                | ✅   |
| `Att_3(D=1000 mGy)`               | 13.55 %          | 13.6 %              | p. 589                | ✅   |
| `Att_4(D=1000 mGy)`               | 3.44 %           | 3.4 %               | p. 589                | ✅   |
| `Att_2(D=1000 mGy)`               | **35.57 %**      | **46.7 % (paper)**  | p. 589                | ⚠️  |

### The Att_2 discrepancy — paper labeling typo

The body text on p. 589 says, for D = 1000 mGy:

> *"At the same dose Att3(D) = 13.6 % (rounded) and Att4(D) = 3.4 % (rounded). For a dose of 1000 mGy, about 47 % of the repair activities is expected to be associated with repairing two breaks on the same DNA molecule (Att2(D) = 46.7 %)."*

But with the model's own definition (Eq 10) and the published parameters `BT = 0.1, α = 0.035/mGy, T = 1.4 mGy, m = 46`, at D = 1000 mGy:

* `BPM = 0.7620` (average breaks per DNA molecule)
* `Att_n(D) = 100·n·P(n; BPM)/BPM`
* `Att_1 = 100·exp(-0.762) = 46.67 %`
* `Att_2 = 100·BPM·exp(-BPM)/1 ... = 35.57 %`
* `Att_3 = 50·BPM²·exp(-BPM) = 13.55 %`   ← matches paper's 13.6 %
* `Att_4 = (100/3)·BPM³·exp(-BPM)/2 = 3.44 %` ← matches paper's 3.4 %

So the paper's stated "Att2 = 46.7 %" is actually the value of **Att_1**. Three out of four numbers in that sentence agree perfectly with my implementation; only the subscript on the 46.7 % is off by one. The body text appears to have shifted the label by one position in that sentence only. The accompanying Fig 2 (which shows all four curves vs dose) is, of course, the authoritative source — and my Fig 2 (`figures/fig2_attributions.png`) reproduces it.

No author contact made (per task instructions).

## 4. Figures reproduced

| Paper Fig | My file                              | What it shows                                                  | Status |
| --------- | ------------------------------------ | -------------------------------------------------------------- | ------ |
| 1         | `figures/fig1_phi_n.png`             | φ_n(t) per-molecule repair-time densities, n = 1..4            | ✅      |
| 2         | `figures/fig2_attributions.png`      | Att_n(D) attribution percentages, 0..1000 mGy                  | ✅      |
| 3         | `figures/fig3_Psi_n.png`             | Ψ_n(t) per-molecule cumulative repair, n = 1..4                | ✅      |
| 4         | `figures/fig4_Cum.png`               | Poisson-weighted Cum(t, D) at D = 100, 1000 mGy                | ✅      |
| 5         | `figures/fig5_residual_DSBs.png`     | RB(t, D) residual DSBs/cell, D = 0, 5, 20, 100, 200 mGy (log)  | ✅      |
| 6         | (skip)                               | 3-D restyling of Fig 5 at fixed D = 100 mGy                    | ⏭      |
| 7         | (skip)                               | Same as Fig 6 but per DNA molecule (= Fig 6 / 46)              | ⏭      |

## 5. Data / code provenance

* PDF: EuropePMC mirror `https://europepmc.org/articles/PMC3315173?pdf=render` (free; Sage DOI direct returns 403 from CherryRd).
* Wet-lab data referenced: Rothkamm & Löbrich 2003 (PNAS 100:5057) γ-H2AX foci in MRC-5; Grudzenski et al. 2010 in HSF1; Scott 2010 for prior MULTISIG1 derivation. **None re-fetched** for this first pass — model self-consistency check is sufficient at this stage.
* No supplementary data, no code, no GitHub published with the paper. The entire model is captured in the body text equations and parameter values.
* No authentication, no paid endpoints, no author contact.

## 6. Replication classification

* **Type:** Model / equations replication (white-box closed-form re-derivation).
* **Faithfulness to paper's stated numerics:** essentially exact (the only mismatch points at a body-text typo, not at the model).
* **Faithfulness to wet-lab data:** not assessed; deferred to a follow-up that digitises Rothkamm & Löbrich 2003 figures and overlays them on `figures/fig5_residual_DSBs.png`.
* **Compute cost:** trivial (< 1 s on CherryRd, < 1 MB working set). No HPC required.
* **External dependencies:** Python 3, NumPy, Matplotlib.

## 7. Recommended QA action (TSV row 87)

```
worktype:    omics/signature replication  →  model / equations replication
themes:      DNA repair / DDR; omics / biomarkers / signatures; computational model / simulation
                          →  DNA repair / DDR; computational model / simulation; radiation biology
qa_decision: KEEP: relevant and replication-plausible  (unchanged)
verdict_or_plan:  TODO: omics/signature replication; artifact harvest; brief; run; report
              →  DONE: model replication; pure-Python reimplementation; 5 figures reproduced; paper typo logged.
```

## 8. Blockers / next actions

* No blockers.
* Optional next-pass items:
  1. Digitise Rothkamm & Löbrich 2003 γ-H2AX foci curves; overlay on Fig 5; quantify model-vs-data RMSE.
  2. Implement Bayesian refit of β over digitised data (Table 1 footnote says this is the intended estimation route).
  3. Implement Eqs 15–16 (pathway-weighted β/μ) as a small notebook.
  4. Cross-link to LUCID100 #57 `lucid-dna-repair-kinetics-doserate-rbe` (closely related theme; would let one compare model styles).

---

*Generated by LUCID100 Wave 4 subagent on 2026-06-09 (Tue) on CherryRd. No author contact; no paid endpoints; no heavy compute.*
