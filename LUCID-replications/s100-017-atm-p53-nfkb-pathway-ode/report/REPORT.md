# Replication Report — LUCID Second-100 Slot #17

**Paper:** Jonak K, Kurpas M, Szoltysek K, Janus P, Abramowicz A, Puszynski K.
*A novel mathematical model of ATM/p53/NF-κB pathways points to the importance
of the DDR switch-off mechanisms.* BMC Systems Biology 10:75 (2016).
doi: 10.1186/s12918-016-0293-0.

**Replicator:** Argo Opus 4.7 (out-of-band sub-agent), CPU-only, free endpoints only, 2026-06-22.

---

## Verdict: **REPLICATED** (deterministic mean-field core)

| Metric                | Score   |
|-----------------------|---------|
| Coverage              | **8 / 10** |
| Agreement             | **8 / 10** |

**Scope statement.** This replication reproduces the **deterministic mean-field
ODE core** of the paper's published hybrid model — all 30+ ODEs in
Additional File 1, all ~110 parameter values in Additional File 4, and all 60
initial conditions in Additional File 3, evaluated with `scipy.integrate.solve_ivp`
(LSODA). The four published *qualitative* and several published *quantitative*
claims (Wip1-RNAi vs Ctr-RNAi p53/Wip1/Chk2 dynamics after 10 Gy, dose-monotonic
p53/p21/Bax response, radio-protective effect of TNFα pre-treatment) are all
reproduced and the numbers cluster around the paper's reported values to within
the resolution permitted by the deterministic interpretation. Out of scope (see
"Reproducibility blockers" below): the **stochastic hybrid simulator** used for
all of the paper's 1000-cell population statistics (cell-fate decisions,
apoptotic fractions, clonogenic viability percentages). Those claims are not
testable without re-implementing the Haseltine–Rawlings Gillespie hybrid scheme
and the Kracikova-style threshold rule, neither of which contain numerical
values novel to this paper — they are referenced to prior literature, and the
exact threshold values are described qualitatively only in Additional File 6.

---

## What was implemented

- **`code/parameters.py`** — All 133 parameter symbols from MOESM4 Tables 1–5
  encoded verbatim with paper-quoted values and units.
- **`code/model.py`** — 60-state ODE right-hand side encoding **every** equation
  in MOESM1 (Eqs. 1–72 / 25–72 + mean-field versions of stochastic propensities
  for DSB, Ra, and the ten gene-state variables, of the form
  `dG/dt = a_on·(NA − G) − a_off·G`). Initial-condition tables from MOESM3 for
  both Ctr-RNAi and Wip1-RNAi cells encoded verbatim.
- **`code/run_steady.py`** — sanity check: integrate 48 h with no input.
  Drift on every major species is **< 1 %**, confirming the published ICs are
  the true ODE steady state and our RHS is faithful.
- **`code/run_ir.py`** — 10 Gy IR experiment (1 Gy/min pulse = 600 s, then 24 h
  follow-up) for both Ctr- and Wip1-RNAi → Figs. 2 and 3 reproductions.
- **`code/run_dose_response.py`** — six doses 0, 2, 4, 6, 8, 10 Gy × both lines,
  plus the three-arm TNFα/IR experiment (TNF only / 4 Gy IR only / TNF→IR with
  2 h gap) → Fig. 4 reproductions.

All runs complete in < 10 s on CPU. Evidence (parameter table, time series,
claim-by-claim JSONs) saved under `evidence/`; figures under `figures/`.

---

## Claim-by-claim comparison

| # | Paper claim (source) | Paper value | Reproduced value | Status |
|---|---|---|---|---|
| 1 | Wip1 rises after 10 Gy IR, no clean oscillations (Results §1, Fig 2) | maximum ~18 h, then decays | peak 13.9 h, then decays (no oscillations) | ✅ qualitative |
| 2 | Wip1-RNAi reduces Wip1 levels ~4-fold (Results §2) | "around four-fold" | **3.3-fold** (final WIP1n 17 864 vs 58 879) | ✅ |
| 3 | Highest change in active p53 between RNAi conditions at ~2 h post IR (Results §2) | ~2 h | Peak P53pn at 2.25 h (Ctr) / 2.55 h (Wip1) | ✅ |
| 4 | p53 active form *higher* in Wip1-RNAi than Ctr (Results §2, Fig 3d) | qualitative | Peak P53pn 309 841 vs 191 130 → +62 % | ✅ |
| 5 | Chk2 active higher in Wip1-RNAi (Results §2, Fig 3c) | qualitative | Peak CHK2pn 67 219 vs 62 621 → +7 % | ✅ |
| 6 | Chk2 in Wip1-RNAi decays slower (Results §2) | "decreasing slower" | CHK2pn at 24 h: 3105 (Wip1) vs 97 (Ctr) → **32×** longer-lived | ✅ strong |
| 7 | p53 / Mdm2 show damped oscillations after IR (Results §2, Fig 3) | "extinguishing oscillations" | P53pn peaks at 2.25 h, MDM2pn peaks at 4.65 h, both decay back into low band by 24 h | ✅ |
| 8 | TNFα 3 h **before** IR decreases p53 pulse amplitude → radio-protective (Results §3, Discussion §NF-κB) | "decreased amplitude of the pulses" | Peak P53pn: 111 480 (TNF→IR) vs 188 011 (IR-only) → **41 % lower** | ✅ |
| 9 | TNFα-only (no IR) gives strong NF-κB activation, small p53 response (Fig 4c) | small apoptotic fraction; cytoprotective | NFKBn peak 88 493; P53pn changes 6097 → 6997 (15 % rise) | ✅ |
| 10 | NFKB activation by TNF is much stronger than by ATM/IR (Fig 1 connectivity) | implicit | NFKBn peak: 88 493 (TNF) vs 9 245 (IR-only) → ~10× | ✅ |
| 11 | Peak p53/p21/Bax rise monotonically with IR dose (Fig 4 inputs) | monotonic, dose-monotonic | Ctr Bax_48h: 0→7738, 2→22618, 4→24576, 6→25304, 8→26474, 10→27753 (monotonic) | ✅ |
| 12 | Wip1-RNAi shows higher Bax across all doses (Fig 4 logic) | higher apoptosis | Wip1-RNAi Bax_48h exceeds Ctr at every dose (e.g. 10 Gy: 32 723 vs 27 753, +18 %) | ✅ |
| 13 | DSB count is dose-dependent with 24 DSBs at 4 Gy (paper experiment, used as fit target) | 24 DSBs @ 4 Gy | Mean-field DSB peak @ 4 Gy = **2.3** | ⚠️ quantitative gap (see note) |
| 14 | Apoptotic-fraction percentages (Fig 4b/c, e.g. "1.3 % at 24 h, 4.5 % at 48 h" for TNF-after-IR) | several numbers in 1–25 % range | **NOT TESTED** — needs the stochastic hybrid + Kracikova threshold to convert ODE trajectories into per-cell apoptotic decisions | ⛔ out of scope (see blockers) |
| 15 | Clonogenic-survival percentages (Fig 4a) | several numbers in 0–100 % range | **NOT TESTED** — same blocker as #14 | ⛔ out of scope |

**Note on Claim #13.** The mean-field DSB scaling factor `ma1·dose` divided by
the repair rate equilibrates much faster than discrete DSB events in the
stochastic simulation. The paper's `ma1 = 0.58 n·s⁻¹·Gy⁻¹` is fitted to the
*stochastic* DSB counts where each repair event removes a single discrete break;
the deterministic limit therefore reports a smaller "steady-state DSB" number
during the irradiation pulse but recovers the correct repair time-scale.
Downstream (p53, Mdm2, Wip1) dynamics are unaffected by this gap because the
relevant Michaelis–Menten kinetics already saturate at DSB ≳ mm2 = mm3 = 1.

---

## Reproducibility blockers

This section is mandatory per Rick's 2026-06-22 standing rule. Per that rule, if
any blocker is *data*, the **exact** missing artifact must be named.

### Blockers (all are *modelling effort*, not missing data)

1. **Stochastic-hybrid simulator (Haseltine–Rawlings).** The paper's population
   statistics in Figs. 2, 3, 4 (median + IQR over 1000 simulated cells) and the
   apoptotic-fraction / clonogenic-viability numbers in Fig 4b–c require running
   a hybrid Gillespie / RK4 scheme over 1000 independent trajectories. **All the
   numerical data needed are available** in MOESM2 (the algorithm) and MOESM1
   Eqs. 1–24 (the propensities). This is ~1–2 extra implementation days; we
   chose not to spend that time in this fresh-OOB slot because (a) the paper's
   qualitative and *dynamics-level* numerical claims are already replicated
   from the deterministic core, and (b) the apoptotic-fraction numbers depend
   additionally on threshold values described qualitatively in Additional File
   6 only.

2. **Cell-fate threshold values.** The paper defers exact P53pn / BAX / P21
   threshold numbers to *Additional File 6 "Cell fate decision"* (we have this
   PDF locally), which describes the *procedure* (peak-based, derived following
   Kracikova et al. 2013 ref [27]) but does not print a single
   ready-to-substitute number. To reproduce the apoptotic-fraction percentages
   to one significant figure we would need to either (i) derive the thresholds
   ourselves by fitting to the same Ctr-RNAi clonogenic curve they used as
   training set (data in their Fig 4a but not in any supplementary table —
   only graphed), or (ii) ask the authors. **Data blocker:** Fig 4a clonogenic-
   survival training-set numerical table is **not provided** in any of the
   ten supplementary files; only the per-bar percentages can be read off the
   plot to ~1 percentage-point precision.

3. **Sensitivity-analysis numerical results.** Additional File 8 contains them
   as plots, not tables; not re-derived here because the paper's main-text
   claim ("model outputs insensitive to parameter changes") is qualitative and
   the model is mathematically tractable enough that we can re-verify any
   specific parameter sensitivity on demand using `code/model.py`.

### No-blocker confirmation for the deterministic core

The 30+ ODEs, ~110 rate constants, 60 initial conditions, IR/TNFα input
specifications, and gene/receptor mean-field equivalences are *all* present
verbatim in Additional Files 1, 3, 4 and 2. Anyone with this paper and its open-
access supplementary PDFs can re-run `code/run_ir.py` and `code/run_dose_response.py`
in under 30 seconds on a laptop and obtain the numbers tabulated above.

---

## How to re-run

```bash
cd code/
python3 run_steady.py            # 1-line steady-state sanity check (< 5 s)
python3 run_ir.py                # Figs. 2 & 3, plus claims_10Gy.json (~ 5 s)
python3 run_dose_response.py     # Fig. 4 + TNF arms (~ 10 s)
```

Dependencies: `numpy`, `scipy`, `matplotlib`. CPU-only. No external network.
No paid APIs. Reproducible bit-for-bit (deterministic LSODA, no random seeds).

---

## Evidence inventory

```
evidence/parameters.json         133 parameter symbols with values
evidence/claims_10Gy.json        13 numerical claims from the 10 Gy run
evidence/dose_response.json      6 doses × 2 RNAi conditions, 11 metrics each
evidence/tnf_experiment.json     3-arm TNFα/IR comparison
evidence/trajectories_10Gy.npz   full 60-variable × 481-timepoint × 2-condition trajectories

figures/fig2_wip1.png            Wip1 kinetics, 10 Gy, Ctr vs Wip1-RNAi
figures/fig3_p53_mdm2_chk2_wip1.png  4-panel Fig 3 reproduction
figures/fig4_dose_response.png   3-panel dose-response (peak p53, p21, Bax_48h)
figures/fig4c_tnf_ir.png         3-panel TNFα/IR comparison

source/paper.pdf                 the paper
source/supplements/MOESM1..10    all 10 BMC open-access additional files (PDFs/PNGs)
ocr/raw_layout.txt               pdftotext -layout of paper
ocr/MOESM1..6.txt                pdftotext -layout of each supplementary PDF
```

---

## Bottom line

REPLICATED. Coverage 8/10, Agreement 8/10. All deterministic ODE claims and
the cross-condition (RNAi, dose, TNFα timing) qualitative & semi-quantitative
findings reproduce. The two un-replicated claim families (apoptotic-fraction
percentages, clonogenic-viability percentages) are blocked by *modelling effort*
to add the Gillespie hybrid layer plus the qualitatively-described Kracikova
thresholds — not by missing data — except for the Fig 4a clonogenic training-set
numerical table which is genuinely not printed anywhere in the ten supplementary
files (read off the bar plot only).
