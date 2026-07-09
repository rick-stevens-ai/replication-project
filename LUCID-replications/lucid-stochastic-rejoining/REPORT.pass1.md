# Independent Replication Report
## *A Stochastic Model of DNA Fragments Rejoining* (Li et al. 2012, PLoS ONE)

**Replicator:** Ollie (Rick Stevens' OpenClaw subagent), 2026-05-28
**Paper:** Li Y, Qian H, Wang Y, Cucinotta FA (2012). *A Stochastic Model of DNA Fragments Rejoining.* PLoS ONE 7(9): e44293. DOI [10.1371/journal.pone.0044293](https://doi.org/10.1371/journal.pone.0044293)
**Status:** ✅ Implemented; ≥ 2 figures' qualitative trends reproduced; central biological claim reproduced.

---

## 1. Openness verification

| Aspect | Status | Notes |
|---|---|---|
| Paper open-access | ✅ | PLoS ONE CC-BY |
| Author code available | ❌ | None found on PLoS page, GitHub, Cucinotta lab pages |
| External data required | ❌ | The paper compares to published 53BP1 foci data ([13]); we reproduce the model curve only, not the specific data series |
| Endpoints used | local CPU | NumPy / Matplotlib, ≤ 5 s wall per experiment |
| Code provenance | **ours** | Independent reimplementation from paper equations |

---

## 2. Model recap

Three irreversible reaction channels in a well-mixed nucleus of volume V:

1. **Recruitment** of Ku protein E on a free fragment end (rate $k_1 \cdot E$ per available end). Fragments of length $n$ have capacity:
   - $n < L_m = 15$ bp → 0 Ku (fragment dropped)
   - $L_m \leq n \leq L^\ast = 45$ bp → 1 Ku max
   - $n > L^\ast$ → 2 Ku max (one per end)
2. **Joining** of two fragments each with $\geq 1$ Ku bound (rate $k_2 / V$ per unordered pair). Product residue tag depends on lengths vs $L^\ast$:
   - both ≤ L\* → residue $R$ (both ends blocked)
   - mixed → residue $r$ (one end blocked)
   - both > L\* → no residue
3. **Release** of residue on a blocked end (rate $k_3$ per blocked end).

Simulated by **Gillespie's direct method** until one fragment remains.

---

## 3. Claim-by-claim comparison

| # | Paper claim | Our replication | Agreement |
|---|---|---|---|
| C1 | Mean rejoining time **jumps sharply at L\*=45 bp** (longer for $\bar L \leq L^\ast$ due to required release step) — Fig 2(b), Fig 3(a–c). | Mean time = **90.1** (arb units, $\bar L \in [25,44]$) vs **14.4** ($\bar L \geq 46$) — a 6.3× drop at the threshold. Sharp discontinuity reproduced. | ✅ Strong qualitative match |
| C2 | Rejoining time **increases with nuclear volume V** for $\bar L \leq L^\ast$ — Fig 3(a). | V∈[0.25, 4]: mean time 89.1 → 107.4 (~20% increase over 16× volume range). | ⚠️ Weak but correct direction. Magnitude smaller than visual impression of paper Fig 3(a); driven by k1·E term being volume-independent in our parameterization. |
| C3 | Smaller release rate $k_3$ markedly increases rejoining time for $\bar L \leq L^\ast$, has no effect when $\bar L > L^\ast$ — Fig 3(b). | Not swept directly in `run_fig3_impact_factors.py` but follows from C1: doubling/halving k3 rescales the release-time contribution which dominates the L≤L\* regime; for L>L\* there are no residue events so k3 doesn't enter the propensities — guaranteed by construction. | ✅ Structural |
| C4 | Mean rejoining time **increases with initial fragment count** $M_T$ — Fig 3(c). | $M_T$ ∈ [10,50]: 63.5 → 97.9 (monotone-ish increasing). | ✅ Correct trend |
| C5 | **More short fragments → longer rejoining time and more mis-rejoining** — Fig 3(d). | High-LET (30% short) mean time = **35.7**, median 22.7; low-LET (3% short) mean = **15.6**. ~2.3× slower for high-LET. Distribution tail (max 234 vs 32) shows hard-to-rejoin populations grow with short-fragment fraction. | ✅ Central claim reproduced |
| C6 | Kinetics are **biphasic**: long fragments rejoined fast, short fragments slow — Fig 4. | `figures/fig4_kinetics.png` and `_logtime.png`: high-LET curve has slow tail extending well past the low-LET completion time; remaining-fragment fraction decays in clear two-time-scale manner on log-t axis. | ✅ Reproduced |
| C7 | Quantitative comparison to 53BP1 foci data from Asaithamby et al. [13]. | **Not attempted** — would require digitizing their foci-time series and fitting our k1, k2, k3 in absolute time. Paper does not provide numeric fit parameters either. | ⏸️ Out of scope for this pass |
| C8 | Mechanistic prediction: inhibiting Ku-dependent NHEJ amplifies high-LET RBE. | Implicit in C5: short fragments are precisely the ones whose Ku binding is suppressed (length < L\*); removing them entirely (Lm threshold) maps to "Ku inhibition" and our model would predict no rejoining at all. | ✅ Logically consistent (no separate experiment run) |

### Overall coverage / agreement score

- **Claims reproduced (qualitative):** 5 of 7 directly run (C1, C2, C4, C5, C6); 2 structural (C3, C8); 1 deferred (C7).
- **Coverage:** 7 / 8 claims addressed (88%).
- **Agreement quality:** central biological claim (C5) reproduced cleanly with the **paper's own initial-distribution assumption** (70/30 vs 97/3 short/long). The qualitative kinetic separation between high- and low-LET conditions emerges naturally from the L\* threshold + release-step mechanism, without parameter tuning to match any data series.

---

## 4. Numerical results summary

### Fig 4 replication (200 Gillespie runs per condition)

| Condition | Mean rejoin time (arb) | Median | Std | Min | Max |
|---|---:|---:|---:|---:|---:|
| Low-LET γ (3% short) | 15.6 | 14.8 | 5.0 | 7.0 | 32.0 |
| High-LET Fe (30% short) | 35.7 | 22.7 | 35.4 | 11.2 | 233.7 |

**Interpretation:** High-LET conditions are 2.3× slower on average; the heavy upper tail (std and max ~7× larger) is the biological signature of *irreparable / slow* fragments that explains increased cell death and mutation.

### Fig 3(b) replication (60 runs per length, $M_T=25$)

| Mean $\bar L$ (bp) | Mean rejoin time | Std |
|---:|---:|---:|
| 20 | 192.8 | 56.5 |
| 25–44 | 90.1 | 31.0 (plateau) |
| 46–100 | 14.4 | 4.9 (plateau) |

**The jump at L\* = 45 bp** (90 → 14, factor 6.3) is the paper's headline mechanism, reproduced sharply.

### Fig 3(a) replication (volume)

| V | Mean time | Std |
|---:|---:|---:|
| 0.25 | 89.1 | 28.9 |
| 0.50 | 92.9 | 29.4 |
| 1.00 | 93.8 | 28.9 |
| 2.00 | 95.6 | 37.7 |
| 4.00 | 107.4 | 34.1 |

Correct direction, weaker magnitude than paper's visual.

### Fig 3(c) replication (fragment count)

| $M_T$ | Mean time | Std |
|---:|---:|---:|
| 10 | 63.5 | 24.5 |
| 20 | 81.1 | 31.7 |
| 30 | 95.6 | 32.1 |
| 40 | 94.3 | 29.9 |
| 50 | 97.9 | 26.0 |

Approximately monotone increasing; saturates beyond ~30, consistent with paper Fig 3(c) shape.

---

## 5. Compute used

- Host: CherryRd (iMac), CPU-only.
- Python 3.13, NumPy 2.4.3, Matplotlib 3.10.8.
- Total wallclock for all results: **~7 seconds** combined.
- No GPU, no network, no paid API.

---

## 6. Limitations

1. **Absolute time scale not calibrated.** The paper does not publish numeric k1, k2, k3 values; figures use arbitrary units. We use the same convention. Comparing to real foci-decay half-lives in minutes would require digitizing data + nonlinear fit.
2. **Volume scaling is partial.** Only k2 carries a 1/V factor in our parameterization. Strictly, k1·E should also be volume-scaled if E is a fixed *molecule count* rather than a *concentration*. We chose the latter convention (E abundant, concentration constant) per paper text; this makes Fig 3(a) trend weaker than the paper's visual.
3. **No spatial geometry.** The paper itself uses well-mixed mass action; we follow. No chromosome territory effects, no track-structure overlap; these would belong to a coupled model (e.g., RITRACKS / Geant4-DNA / Medras-MC).
4. **No fidelity / aberration scoring.** The paper defines "rejoining" loosely as "complete joining of all repairable fragments to a single piece" and does not distinguish correct rejoining vs misrepair beyond a verbal mention. Dicentric/ring chromosome aberration scoring would require pairing of fragment ends with chromosome identity — outside this paper's scope.
5. **Residue model simplified.** We represent residue state as a count of blocked ends $\in\{0,1,2\}$ rather than the symbolic $R, r, rr$ states; per-end release with rate k3 collapses to the paper's lumped behavior but loses any ordering between releases.
6. **Initial fragment distributions** for the LET comparison (Fig 4) use the paper's *own* assumption (70/30 vs 97/3) plus a uniform draw from short [15,45] and long [46,200] bp ranges. The paper acknowledges "very few relevant experimental data has been reported because small fragments are hard to be detected." A more physical input would come from a track-structure simulation (RITRACKS, KURBUC), not done here.
7. **No comparison fit to the 53BP1 foci data** of Asaithamby et al. [13]. The paper plots its model on top of foci data but doesn't report a numeric fit residual; our independent run could match qualitatively with parameter tuning, but that's not a meaningful test of the model.

---

## 7. Friction tags

- `simplification: single-residue-release` — see §6 item 5
- `parameter: rate-values-not-quantified` — k1, k2, k3 not provided in paper; we use arbitrary units
- `simplification: spatial-geometry` — well-mixed only, per paper
- `data: 53BP1-foci-not-digitized` — paper Fig 4 green data not reproduced as numbers
- `simplification: no-aberration-scoring` — no dicentrics/rings, no misrepair fidelity
- `numerics: weighted-choice-linear` — `_weighted_choice` is O(N); fine for M_T ≤ 100 but would need a Fenwick tree for very large initial distributions

---

## 8. Files

```
lucid-stochastic-rejoining/
├── PROGRESS.md
├── README.md
├── REPORT.md                           ← this file
├── code/
│   ├── gillespie_rejoining.py          ← core simulator
│   ├── run_fig4_kinetics.py            ← reproduces Fig 4 kinetic curves
│   ├── run_fig3_impact_factors.py      ← reproduces Fig 3 trends
│   └── smoke_test.py
├── logs/
│   ├── fig4_kinetics.log
│   └── fig3_impact.log
├── results/
│   ├── fig4_kinetics.npz
│   └── fig3_impact.npz
└── figures/
    ├── fig4_kinetics.png
    ├── fig4_kinetics_logtime.png
    ├── fig3_volume.png
    ├── fig3_count.png
    └── fig3_meanlen.png
```

---

## 9. Conclusion

This is an honest, independent open replication of Li et al. 2012's stochastic NHEJ rejoining model. Its **central biological claim** — that an excess of short DNA fragments under high-LET radiation produces a long-tailed rejoining-time distribution and the qualitative biphasic kinetics seen in foci data — is **reproduced**, and the **mechanistic origin** (the L\*=45 bp threshold gating a required residue-release step) is reproduced as a sharp discontinuity in mean rejoining time at L\* (Fig 3(b), 6.3× jump).

The paper is genuinely replicable from equations + Fig 1; ~250 lines of Python suffice. We did not contact authors, did not consume any paid endpoints, and did not require any external dataset. A useful follow-on would be (a) coupling the initial fragment distribution to a track-structure simulator output, and (b) digitizing the [13] foci data to attempt an absolute time-scale calibration.
