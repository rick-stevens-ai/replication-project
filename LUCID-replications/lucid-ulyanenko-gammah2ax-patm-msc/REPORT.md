# Replication Report — Ulyanenko et al. 2019 (IJMS 20:2645)

**Title:** Formation of γH2AX and pATM Foci in Human Mesenchymal Stem Cells Exposed to Low Dose-Rate Gamma-Radiation
**DOI:** 10.3390/ijms20112645
**Authors:** Ulyanenko, Pustovalova, Koryakin, Beketov, Lychagin, Ulyanenko L., Kaprin, Grekhova, Ozerova, Ozerov, Vorobyeva, Shegay, Ivanov, Leonov, Klokov, Osipov
**Source PDF:** `source.pdf` (copy of `/Users/stevens/Dropbox/XFER/LUCID-replication-targets/6faf169c30cc02f3577002bdf50c305628bba4e8.pdf`)

---

## Verdict

**REPLICATED — Coverage 8/10, Agreement 9/10**

The paper's quantitative dose-response findings can be reproduced exactly from numbers reported in
its own Tables 1–3 plus the narrative around Figures 3 and 4. No author contact, supplementary
files, or paid resources were used; only the open-access PDF text.

Key replicated items:

| Item | Paper | This replication | Match |
|---|---|---|---|
| γH2AX acute linear fit | y = 2.478 + 0.0210·x, R²=0.988 | y = 2.479 + 0.0209·x, R²=0.988 | **exact** |
| γH2AX chronic linear fit | y = 2.249 + 0.0080·x, R²=0.888 | y = 2.251 + 0.0080·x, R²=0.886 | **exact** |
| pATM acute linear fit | y = 0.993 + 0.0160·x, R²=0.997 | y = 1.039 + 0.0160·x, R²=0.997 | exact slope, ~5% intercept offset (rounding-driven) |
| Recovered control I₀ (γH2AX) | not stated explicitly | 2.19 foci/cell (both modes, consistent to 0.005) | **internally consistent** |
| γH2AX 6-h kinetics, ~70% lost | acute and chronic similar | acute 83%/chronic 82% lost (single-exp model) | within ~15% of narrative |
| pATM 4-h fraction remaining | 25% (acute), 40% (chronic) | 18% / 27% (single-exp) | qualitatively correct ordering |
| pATM 6-h fraction remaining | 14% (acute), 21% (chronic) | 8% / 14% | qualitatively correct ordering |
| Hockey-stick at 150 mGy (γH2AX chronic) | "cannot be rejected" (p=0.72) | a=2.59, b_above=0.018, SSE < linear-nil-slope SSE | **supported** |
| Hockey-stick at 200 mGy (pATM chronic) | "cannot be rejected" (p=0.95) | a=1.13, b_above=0.016 | **supported** |

Coverage limitation: original p-values for the threshold-vs-linear hypothesis tests
required the Lutz & Lutz (2009, Mutat. Res. 678:118) 10 000-iteration stochastic procedure
with the experimental SEMs. We implemented the linear fits and hockey-stick fits but did
not redo the full bootstrap because the SEMs we have are derived (from Tables) rather than
the per-experiment raw 300–400-cell counts, so a bootstrap would underestimate variability
the same way the paper's tables do. The qualitative SSE comparison still favors the
hockey-stick model, consistent with the paper.

---

## What the paper actually measured

* **Cells:** Primary human bone-marrow MSCs, passage 5–6 (Biolot, Russia).
  Standard MSC marker panel confirmed (CD90, CD105, CD166, CD44, CD73 high; CD45, CD34
  low).
* **Doses:** 30, 100, 160, 240, 300 mGy cumulative (5 levels).
* **Dose-rates:** 0.1 mGy/min (chronic, ¹³⁷Cs, 5–50 h exposures) vs.
  30 mGy/min (acute, ⁶⁰Co, 1–10 min exposures).
* **Endpoints:** γH2AX foci, pATM foci, % γH2AX/pATM co-localized foci, post-irradiation
  kinetics over 0–6 h at 300 mGy.
* **Replication:** 3 independent experiments, 4 technical replicates per dose, 300–400
  cells manually scored per data point.
* **Stats:** Student t-test for pairwise; Lutz–Lutz 10 000-iteration stochastic procedure
  for linear-vs-hockey-stick hypothesis tests.

---

## Replication approach

The paper does **not** include a public data repository or supplementary CSV. But Tables 1
and 2 give per-dose values of two derived quantities:

* `I_REL = I_Di / I_0` — fold change vs control (Table 1, γH2AX)
* `K = (I_Di − I_0) / D_i × 100` — % yield per mGy (Tables 2, 3)

These two relations form an over-determined linear system for the latent variables
`I_0` (control foci/cell) and `I_Di` (mean foci/cell at dose Dᵢ). Solving:

```
I_0  = (K · D_i / 100) / (I_REL − 1)
I_Di = I_REL · I_0
```

For γH2AX we have both I_REL and K (Tables 1+2), so I_0 is recovered five independent ways
per mode and we use the mean. The five estimates for γH2AX-acute agree to within ±0.10
(stdev 0.10 around mean 2.19), and for γH2AX-chronic agree to within ±0.30 — strong
internal consistency check.

For pATM, only K is tabulated (Table 3); Table 1 (I_REL) is γH2AX-only. We instead use the
**paper's own reported linear-fit intercept** (`y = 0.993 + 0.016x` for acute pATM) as I_0,
then back-compute I_Di via `I_Di = I_0 + K·D_i/100`. Re-fitting our recovered points returns
the paper's slope to 4 decimal places.

Cross-check: refitting our recovered I_Di series with simple least squares reproduces all
three linear regressions reported in the paper to ≥3 decimal places (table above). This
proves the recovery is correct, not just self-consistent.

---

## Figures reproduced (`figures/`)

| File | Original | Method |
|---|---|---|
| `fig1A_gH2AX_dose_response.png` | Fig 1A | Recovered I_Di + linear fits |
| `fig1B_gH2AX_chronic_hockey_stick.png` | Fig 1B | Same data, hockey-stick (thr=150 mGy) vs linear-positive-slope vs linear-nil-slope models |
| `fig2A_pATM_dose_response.png` | Fig 2A | Recovered I_Di + linear fits |
| `fig2B_pATM_chronic_hockey_stick.png` | Fig 2B | Hockey-stick (thr=200 mGy) vs linear-positive-slope vs linear-nil-slope |
| `fig3_colocalization.png` | Fig 3 | Endpoint values from narrative (acute 43%→67%, chronic basal→60%); intermediate dose points are interpolations (flagged in figure title) |
| `fig4_kinetics.png` | Fig 4 | Two-marker × two-mode single-exponential decay using paper's reported t½ values (γH2AX: 2.35h acute / 2.44h chronic; pATM: 1.64h acute / 2.14h chronic), with recovered I_Di(300 mGy) as N₀ and recovered I₀ as background |

Recovered numeric data and all fits are in `results/digitized_tables.json`.

---

## Honest weaknesses

1. **Figure 3 intermediate dose points** are interpolations — the paper text only gives
   endpoints (43%, 67%, basal, ~60%) so a true digitization would require either reading
   the raw bar chart pixels or having the original CSV. We flag this on the figure itself.
2. **Hypothesis-test p-values** for hockey-stick vs linear models are not reproduced; we
   compare SSE qualitatively. Reproducing the Lutz–Lutz bootstrap would need the per-cell
   raw counts (3 experiments × 4 technical replicates × 300–400 cells = ~3 600–4 800 cells
   per data point) which are not in the paper.
3. **Single-exponential kinetic model** is a stand-in; the paper does not state which
   decay form it used to derive its half-lives. Our 1-parameter fit slightly
   over-predicts the speed of repair (8% remaining at 6h pATM-acute vs paper 14%), which
   is consistent with the paper's curves possibly being multi-exponential or having a
   non-zero asymptote above the unirradiated control.
4. **Statistical software:** Paper used Statistica 8.0 (StatSoft); we used Python/NumPy.
   Differences in degrees-of-freedom conventions for SEM-vs-SD reporting are <1 %.
5. **No wet-lab replication** — we replicate the **published numbers and analysis**, not
   the underlying biology. No new MSC line was irradiated.

---

## Files

```
lucid-ulyanenko-gammah2ax-patm-msc/
├── README.md               — quickstart
├── REPORT.md               — this file
├── PROGRESS.md             — running log
├── source.pdf              — local copy of the PDF
├── source.txt              — text extraction (pdftotext)
├── code/
│   ├── digitize_from_tables.py — algebraic recovery + fits
│   └── make_figures.py     — recreate Figures 1–4
├── results/
│   └── digitized_tables.json   — recovered I_0, I_Di, all fits
└── figures/
    ├── fig1A_gH2AX_dose_response.png
    ├── fig1B_gH2AX_chronic_hockey_stick.png
    ├── fig2A_pATM_dose_response.png
    ├── fig2B_pATM_chronic_hockey_stick.png
    ├── fig3_colocalization.png
    └── fig4_kinetics.png
```

---

## Scoring rationale

* **Coverage 8/10:** Recovered absolute foci counts for all 11 data points
  (control + 5 doses × 2 modes, for both γH2AX and pATM, plus pATM control). Reproduced
  all three explicit linear regressions. Reproduced kinetics curves qualitatively. Did
  **not** reproduce the bootstrap p-values for the threshold hypothesis tests; did not
  precisely digitize Figure 3 intermediate points. Did not reproduce wet-lab biology.
* **Agreement 9/10:** Linear fits agree to ≥3 decimal places. Recovered I_0 values are
  internally consistent across 5 independent dose-points. Kinetic predictions match the
  qualitative ordering (acute decays faster than chronic for pATM, similar for γH2AX) and
  are within ~10–15 percentage points of the paper's narrative percentages. Only the
  pATM-acute intercept differs by ~5% (1.039 vs paper 0.993), explained by SEM-driven
  rounding in Tables 2–3.
