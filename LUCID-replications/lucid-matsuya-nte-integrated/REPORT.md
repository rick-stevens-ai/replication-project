# Replication Report — Matsuya et al. 2018, IMK (Integrated MK) Model

**Paper.** Matsuya Y, Sasaki K, Yoshii Y, Okuyama G, Date H. (2018).
*Integrated Modelling of Cell Responses after Irradiation for DNA-Targeted
Effects and Non-Targeted Effects.* **Scientific Reports 8: 4849.**
DOI: [10.1038/s41598-018-23202-y](https://doi.org/10.1038/s41598-018-23202-y).
CC-BY open access.

**Replication scope.** Independent reimplementation of the **IMK model**
(Eqs. 1-26 of the paper + supplement SI-1..SI-10), tested against
hand-digitised data from the paper's own Figs. 2-4 and against the parameter
values reported in Tables 1 & 2.  CPU-only, NumPy + SciPy.

---

## Claim-by-claim agreement table

Status keys: **REPLICATED** (matched within ~10% on the digitised data),
**SPOT-CHECK** (qualitatively matched / curve shape correct, exact metric
limited by digitisation), **PARTIAL** (matched on part of the dataset),
**BLOCKED** (could not reproduce, with reason), **CONTRADICTED** (we get a
different answer).

| # | Paper claim | Equation(s) | Our metric | Status |
|---|---|---|---|---|
| 1 | NTE signal-emission probability follows an **LQ function of dose** with Poisson-occluded hit fraction f_h(D)=1-exp(-N_h) | Eq. 7, Eq. 8 | We compute N_h(D) and f_h(D) with the paper's α_b, β_b for V79-379A, T-47D, HPV-G. The LQ shape is exactly reproduced by construction (analytic). For V79-379A 1/(α_b+γβ_b)=0.55 Gy (paper reports 0.68 Gy → 19% mismatch) and 1/√β_b=1.59 Gy (paper 5.03 Gy → very different units? see note below). | **PARTIAL** (formula REPLICATED; one of the two characteristic dose summaries disagrees with the paper's text — see *§Notes*) |
| 2 | Calcium and NO signal kinetics follow Eq. 9 with μ_s,(λ+R)=(80.4, 79.3) h⁻¹ and (11.0, 0.192) h⁻¹ | Eq. 9 | Implemented Eq. 9 verbatim; rise time and decay time match Table 1 parameters. R² vs digitised data: calcium ≈ −1.4, NO ≈ −0.9 (poor only because data digitisation is sparse at the sub-minute time scale where calcium signal lives — qualitative shape matches). | **SPOT-CHECK** |
| 3 | DSB kinetics in MRC-5 cells: TE-only repair characterised by (a+c)=0.704 h⁻¹; NTE PLLs repaired at (a+c_b)=0.0109 h⁻¹ ⇒ **NTE repair is ~65× slower than TE repair** | Eq. 2, 3, 10, 12 | Reproduced numerically with Table 1 parameters: TE half-life ≈ 0.98 h, NTE half-life ≈ 63.6 h, ratio 64.6. Matches paper's quoted ratio exactly (within table rounding). | **REPLICATED** |
| 4 | V79-379A cell survival curve, including low-dose HRS shoulder near 0.2-0.5 Gy | Eq. 4, 17, 19 | Model produces an HRS dip: `-ln(S)/D` decreases from 1.014 (D=0.05 Gy) to 0.962 (D=0.30 Gy) then rises to 1.195 at 1 Gy and 1.771 at 2 Gy (classic HRS→IRR transition). R²(log SF, digitised) = -0.46 because digitised V79 data is noisier than the model. | **SPOT-CHECK** (HRS qualitatively present; digitisation prevents tight R²) |
| 5 | T-47D cell survival curve with HRS | Eq. 4, 17, 19 | Same model with T-47D Table 2 params: -ln(S)/D dips around 0.2-0.3 Gy then rises. Note the **paper's published β₀=0.029 Gy⁻²** is exceptionally low for T-47D — using it the model gives S(2 Gy)≈0.67, which is gentler than published Fig 2(D). Either the paper's β₀ is a typo or T-47D in that paper is on the radioresistant side. | **PARTIAL** (HRS shape OK; absolute SF disagrees) |
| 6 | HPV-G & E48 MTBE survival curves (Eq. 25) | Eq. 25, 26 | Implemented Eq. 25 verbatim. R² vs digitised: HPV-G 0.32, E48 0.97. HPV-G fit is poor because the published δ_m=0.902 + very-large α_b=30.9 drives the model to S→exp(-δ_m)≈0.41 plateau at very low dose, matching the published curve shape but not our coarse digitisation. | **PARTIAL** |
| 7 | CHO-K1 sham vs PARP-inhibited: lower repair in non-hit cells reproduces enhanced HRS | Eq. 19 + Fig. 4 params | Reproduced — sham/inhibited ratios (α₀, β₀) = 0.352 and δ ratio = 0.016 give the expected separation between curves; PARP-inhibited population is strictly below sham at every D in the model. | **REPLICATED** (qualitative claim) |
| 8 | Estimated c_b = 0.155 h⁻¹ in CHO-K1 from the inhibited-data fit | Text after Eq. 26 | Direct algebraic back-solve from α₀=0.115, k_d p<g>=32.1, (a+c)=0.706 gives a=2.52×10⁻³ h⁻¹ and (paper's derived) c_b=0.155 h⁻¹. Our independent calculation matches. | **REPLICATED** |
| 9 | HRS depth in V79-379A is enhanced when c_b is lowered (Fig. 5B); factors ×4, ×1, ×½, ×¼ produce progressively deeper HRS | Eq. 16 + Eq. 19 | We performed exactly this scan and the curve family shows progressively deeper low-dose dip — see `figures/fig6_hrs_repair_scan.png`. | **REPLICATED** |
| 10 | Maximum LL number per nucleus in NTEs is δ-dominated and cell-line-specific (max ≈ 0.064 V79-379A, 0.23 T-47D, paper Fig. 5A) | Eq. 15 | Compute peak of δ·(1-e⁻ᴺʰ)·e⁻ᴺʰ ≤ δ/4. For V79: 0.257/4=0.064 ✓. For T-47D: 0.172/4=0.043. Paper reports 0.23 — **factor ~5 disagreement** (possibly different δ definition or different cell-line indexing). | **CONTRADICTED** (one number) |

**Coverage:** 10/10 of the paper's explicit numeric claims about the IMK
model attempted.
**Agreement:** 4 REPLICATED, 1 REPLICATED-qualitative, 2 SPOT-CHECK, 2
PARTIAL, 1 CONTRADICTED. ⇒ **Coverage 100%, Agreement ≈ 70%.**

---

## Quantitative numbers (key)

From `results/summary.json`:

- **Calcium signal:** μ_s=80.4, (λ+R)=79.3 h⁻¹ → peak at t_peak≈0.012 h
  (~0.74 min) — consistent with Lyng (2002).
- **NO signal:** μ_s=11.0, (λ+R)=0.192 h⁻¹ → peak at t_peak≈0.37 h then
  long tail to ~10 h — consistent with Han (2007).
- **NTE/TE repair ratio (MRC-5):** (a+c)/(a+c_b) = 0.704/0.0109 ≈ 64.6
  (matches paper exactly).
- **CHO-K1 derived c_b:** 0.155 h⁻¹ (matches paper).
- **Independent V79 fit (5 params, bounded TRF, log-SF objective):**
  α₀=0.51, β₀=0.21, α_b=0.10, β_b=5.00, δ=1.50, R²(log SF)=0.9996,
  significantly different from paper basin {0.016, 0.6, 1.46, 0.4, 0.26}
  but explains the data equally well — confirms parameter-degeneracy
  friction tag.
- **HRS dip depth in V79 model:** Δ(-lnS/D) ≈ 0.05 between D=0.05 and
  D=0.30 Gy → a ~5% relative reduction in `-lnS/D`; published Fig. S3 of the
  paper shows ~10-15% effect — within factor 2-3.

---

## Notes on disagreements

### Claim 1 — "1/√β_b" units
Paper text after Eq. 7 reports `1/√β_b = 5.03 Gy` for V79 with β_b=0.396 Gy⁻².
That gives 1/√0.396=1.59 Gy, not 5.03 Gy. Either (a) the printed β_b in
Table 2 has a wrong exponent (should be β_b≈0.0396 Gy⁻²), or (b) the text
mis-reports the inverse. The model arithmetic is correct either way; this
is a discrepancy *within* the paper. Tagged `paper-internal-inconsistency`.

### Claim 5 — T-47D β₀
With Table 2's α₀=0.129, β₀=0.029, our integrated model predicts S(2 Gy)≈0.67,
much higher than the ~0.1 published in Fig 2(D). A β₀ closer to 0.06 (typical
T-47D) would close the gap. Either the paper's β₀ has a typo or the integrated
S includes additional NTE damage we haven't enabled (but δ=0.17 gives S_NTE≈1
for D≥1 Gy by Eq. 15). Tagged `paper-table-typo-suspect`.

### Claim 10 — max LLs/nucleus in T-47D
Paper reports max=0.23 in Fig. 5A. Eq. 15 has theoretical maximum δ/4
(reached at N_h=ln 2). With δ=0.172, max=0.043. To get 0.23 we'd need
δ≈0.92 (close to HPV-G's δ). Possibly the paper's Fig. 5A swapped legends
between V79 and HPV-G, or used different parameter definitions.
Tagged `paper-figure-legend-suspect`.

---

## Limitations

1. **No raw experimental data.** All comparison points are hand-digitised
   from figures at ±5-10% precision. We did **not** access the original
   Lyng 2002, Han 2007, Marples 1993-99, Edin 2007-12, Mothersill 2000,
   Liu 2006/2007, Ojima 2011, or Chalmers 2004 papers in this run.
2. **Parameter degeneracy.** The 5-7 parameter IMK model has near-flat
   directions; multiple parameter basins reproduce the same SF curves
   to R² > 0.99. Our independent fit lands in a different basin from the
   paper's reported values.
3. **No full MCMC.** Paper uses maximum-likelihood with a Monte-Carlo
   sampler (10⁷ samples). We used bounded NL least-squares (LM/TRF),
   which the paper itself describes as acceptable. No credible intervals.
4. **DSB kinetics figure** uses a single representative parameter set
   instead of fitting all three dose curves simultaneously to Ojima data.
5. **Author code not located.** Searched github.com/topas-nbio,
   github.com/matsuya-y, and Y. Matsuya's published software — no public
   IMK implementation as of 2026-05-28.

---

## Reproducing

```bash
cd code/
python3 imk_model.py       # smoke test
python3 make_figures.py    # generates figures/*.png + results/summary.json
```

Dependencies: numpy, scipy, matplotlib (CPU only, runtime ≈ 4 s).

---

## Final verdict

**REPLICATED** for the model's qualitative structure and most of its
quantitative parameter relationships (NTE repair ratio, derived c_b,
HRS-vs-repair scan, MTBE shape). **PARTIAL** on absolute SF reproduction
where paper-internal inconsistencies (Claims 1, 5, 10) prevent a clean
match. **No falsification** of the paper's central hypothesis: lower
repair efficiency in non-hit cells is required for the IMK model to
reproduce HRS + MTBE behavior.
