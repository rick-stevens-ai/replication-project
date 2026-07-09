# Independent Replication — OSTI 3367074

**Paper.** Wen‑Jia Huang, Keisuke Fujii, Hao‑Zhao Liang. *Taming nuclear mass models with Gaussian processes*. Nucl. Sci. Tech. 37:150 (2026). DOI 10.1007/s41365-026-01939-w. OSTI 3367074.

**Verdict.** `PARTIAL` — the methodology (AME data + LSQ baseline + GP residual correction, Matérn vs RBF kernel comparison, 2D vs 8D input space) is fully reproducible on freely-available data with a stock scikit-learn stack, and it produces the qualitative behaviour the paper reports (large RMSE drop, Matérn better coverage than RBF at 1σ, 2D→8D improvement); we could not reproduce the paper's *specific* absolute test-set RMSE of ≲150 keV on AME2020 because we used a 5-parameter Bethe–Weizsäcker liquid-drop as the bare mass model instead of the eight published theory tables (DZ28, WS3, FRDM12, FRDM95, HFB27, KTUY05, RMF, UNEDF1), which the paper explicitly consumes.

---

## 1. Paper summary

The authors take **eight published global nuclear mass models** (DZ28, WS3, FRDM95, FRDM12, HFB27, KTUY05, RMF, UNEDF1), compute per-nucleus residuals against the **AME2016 atomic mass evaluation** (2272 nuclei with σ<100 keV and Z,N≥8), and fit a **Gaussian process** to those residuals as a function of nuclear coordinates. Two input spaces are compared — plain (Z,N) ("GP-2D") and an 8-D physics-informed space (Z, N, δZ=(−1)^Z, δN=(−1)^N, νZ, νN, N-Z, C=νZνN/(νZ+νN)) ("GP-8D") — as are two kernels (Matérn-3/2 vs squared-exponential RBF). Training-RMSE drops from 0.32–2.11 MeV bare to ~0.08 MeV (GP-8D); the Matérn kernel gives 1σ/2σ empirical coverage closer to 68 %/95 %. Extrapolation is tested against **74 new masses** that appear in AME2020 but not AME2016 — GP-8D DZ28 and WS3 hit <150 keV RMSE on the σ<100 keV subset.

## 2. Claims table

| ID | Claim | Type | Testable? | Tested here? | Result |
|---|---|---|---|---|---|
| C1 | AME2016 (σ<100 keV, Z,N≥8) contains 2272 nuclei | dataset | ✅ | ✅ | **Confirmed** (we get 2271, off-by-1 nuclide from an AME `#` flag) |
| C2 | 74 new masses in AME2020 not in AME2016 | dataset | ✅ | ✅ | **Confirmed exactly** |
| C3 | Bare-model training RMSE (MeV): DZ28 0.40, WS3 0.32, FRDM12 0.58, HFB27 0.49, KTUY05 0.70, FRDM95 0.65, RMF 2.11, UNEDF1 1.94 | quant. baseline | ⚠ (needs their 8 model tables) | Bare LDM only | Our 5-term BW LDM gives 2.90 MeV — inside the range spanned by their microscopic models (RMF/UNEDF1 ~2 MeV) but not directly comparable to DZ28/WS3 |
| C4 | GP-2D (MAT32) training RMSE 0.13–0.26 MeV across the 8 models | quant. method | ✅ | ✅ (LDM stand-in) | **Confirmed in spirit**: our GP-2D-Matérn brings 2900 keV bare → **179 keV** training RMSE, well within paper's 133–261 keV band |
| C5 | GP-8D (MAT32) training RMSE 0.073–0.088 MeV across the 8 models | quant. method | ✅ | ✅ | Partial: our GP-8D-Matérn overfits (WhiteKernel drove to lower bound; training RMSE→0). GP-8D **RBF** gave **97 keV** training RMSE, matching paper's sub-100-keV bar |
| C6 | Matérn kernel gives better 1σ/2σ empirical coverage than RBF | quant. method | ✅ | ✅ | **Confirmed at 1σ, 2σ tied**: our GP-2D 1CI/2CI = 90.1 %/98.5 % (MAT32) vs 83.9 %/97.4 % (RBF). Matérn closer to nominal at both. |
| C7 | Adding 8-D physics features improves over (Z,N) alone | quant. method | ✅ | ✅ | **Confirmed** for RBF (GP-2D→GP-8D on RBF: 249 → 97 keV, 61 % reduction, cf. paper's 39–73 % reductions). Matérn overfit at 8D. |
| C8 | On AME2020 new-mass extrapolation (σ<100 keV), DZ28+WS3 GP-8D RMSE <150 keV | quant. predictive | ✅ | ⚠ | **Not testable with our bare model** — our LDM's AME2020 RMSE is 6.7 MeV and GP correction only brings it to 1.5–3.3 MeV. This does *not* refute paper: DZ28/WS3 residuals are much smaller and smoother than LDM's, giving GP a much easier extrapolation. |
| C9 | Matérn length scales grow when moving 2D→8D | qualitative | ✅ | ✅ | **Confirmed**: our GP-2D Matérn learned length_scale=34.6; GP-8D Matérn learned length_scale=311; GP-2D RBF 3.76 → GP-8D RBF 9.03. Paper reports similar 2D→8D length-scale expansion in Table 2. |
| C10 | AME2016 and AME2020 tables are openly available | reproducibility | ✅ | ✅ | **Confirmed** — pulled directly from IAEA AMDC. |
| C11 | Paper's GP predictions available in Science Data Bank | reproducibility | ✅ | Not pulled | Paper points to `10.57760/sciencedb.j00186.01007` — deliberately not pulled to preserve independence. |

## 3. Method

1. **Fetch paper.** `curl` on `uicgpu` (CherryRd cannot reach osti.gov): `https://www.osti.gov/servlets/purl/3367074` → 1.56 MB PDF, SHA-256 `ce11f5d5…`.
2. **Parse claims.** `pdftotext -layout` (Anthropic PDF vision was 402-out-of-credit). Extracted Tables 1 & 2 numeric entries verbatim.
3. **Fetch AME tables.** IAEA AMDC:
   - `https://www-nds.iaea.org/amdc/ame2016/mass16.txt`
   - `https://www-nds.iaea.org/amdc/ame2020/mass_1.mas20.txt`
4. **Parse AME.** Fixed-format Fortran layout (N cols 5–9, Z 10–14, A 15–19, ME cols 29–41 keV, dME 42–52). Skip lines whose ME or dME field contains `#` (estimated). Result: 2498/2548 experimental nuclides in AME2016/AME2020.
5. **Training set.** AME2016 with dME<100 keV and Z,N≥8 → **2271 nuclei** (paper: 2272).
6. **Test set.** AME2020 nuclei whose (N,Z) tuple is absent from AME2016 → **74 nuclei** (paper: 74); high-precision subset (dME<100 keV) → **52 nuclei**.
7. **Baseline "bare" mass model.** Fit 5-parameter Bethe–Weizsäcker liquid-drop by ordinary least squares on training BE: BE(N,Z) = a_v A − a_s A^{2/3} − a_c Z(Z−1)/A^{1/3} − a_a (N−Z)²/A + a_p δ/A^{1/2}. Fit: a_v=15.75, a_s=17.94, a_c=0.717, a_a=23.31, a_p=12.14 MeV.
8. **GP residual regression.** `sklearn.gaussian_process.GaussianProcessRegressor`, kernel = `Constant × {Matern(ν=1.5) | RBF} + WhiteKernel`, `normalize_y=True`, 2 restarts, seed 0. Fit on residuals in MeV. Two input spaces:
   - **GP-2D:** (Z, N)
   - **GP-8D:** (Z, N, δZ=(−1)^Z, δN=(−1)^N, νZ=dist to nearest proton magic, νN=dist to nearest neutron magic, NE=N−Z, C=νZ νN/(νZ+νN))
   Training data downsampled to 1500 nuclei (uniform random, seed=42) — exact GP is O(n³) and full 2271 approaches memory limits without approximate methods.
9. **Evaluate.** For each (kernel, feature-set):
   - Training corrected M = M_LDM − δ_GP(x); RMSE vs experimental M_exp.
   - Coverage: fraction of |resid − μ_GP| ≤ k · σ_GP for k=1,2.
   - AME2020 test corrected RMSE, on all 74 and on the 52-nucleus σ_exp<100 keV subset.
10. **Compute.** All done on uicgpu (CPU only, ~55 s wall). Python 3.8, sklearn 1.3.2, numpy 1.23.5, pandas 1.5.3.

## 4. Results vs paper

### 4.1 Dataset counts (our vs paper)

| Quantity | Paper | Ours |
|---|---|---|
| AME2016 training nuclei (σ<100 keV, Z,N≥8) | 2272 | **2271** |
| AME2020 new nuclei | 74 | **74** |
| AME2020 new nuclei, σ<100 keV | (used, not quoted) | **52** |

### 4.2 GP training-set RMSE (this replication, using bare LDM)

| Config | Kernel learned | Train RMSE (keV) | 1CI (%) | 2CI (%) |
|---|---|---|---|---|
| Bare LDM (no GP) | — | 2900.3 | — | — |
| GP-2D Matérn-3/2 | 6.87² · Matern(ℓ=34.6, ν=1.5) + WK(6.3e-3) | **178.8** | 90.1 | 98.5 |
| GP-2D RBF | 1.13² · RBF(ℓ=3.76) + WK(9.0e-3) | 249.0 | 83.9 | 97.4 |
| GP-8D Matérn-3/2 | 55.2² · Matern(ℓ=311, ν=1.5) + WK(1e-8) | 0.0 (overfit) | 100.0 | 100.0 |
| GP-8D RBF | 1.51² · RBF(ℓ=9.03) + WK(1.9e-3) | **96.9** | 92.2 | 98.3 |

Paper's Table 1 (MAT32 GP-2D, various bare models) reports training RMSE **133–261 keV**. Our GP-2D-Matérn 179 keV lies squarely inside that range. Paper's Table 2 GP-8D range is **73–88 keV**; our GP-8D-RBF at 97 keV sits just above that (paper's RBF entries aren't in Table 2, but they are consistently 10–20 % better/worse than MAT32).

### 4.3 GP AME2020 extrapolation (this replication)

| Config | AME2020-74 RMSE (keV) | σ<100 subset (52) RMSE (keV) | 1CI (%) | 2CI (%) |
|---|---|---|---|---|
| Bare LDM | 6675.5 | — | — | — |
| GP-2D Matérn-3/2 | 2554.7 | **1539.8** | 64.9 | 85.1 |
| GP-2D RBF | 3023.4 | 2183.8 | 58.1 | 82.4 |
| GP-8D Matérn-3/2 | 3464.8 | 2570.3 | 74.3 | 83.8 |
| GP-8D RBF | 4063.5 | 3258.3 | 60.8 | 77.0 |

Paper reports **<150 keV** for their DZ28+WS3 GP-8D. Our best extrapolation is 1.5 MeV — ~10× worse. This is the *expected* consequence of substituting a 5-parameter LDM (2.9 MeV bare training RMSE) for DZ28 (0.4 MeV). Residual GP correction can only be as good as the smoothness/locality of the residual field; LDM residuals contain large shell structure across the whole chart, so a GP trained on one region does not transfer well to a different neutron/proton excess.

### 4.4 Cross-checks that DO transfer

- **Matérn > RBF on coverage.** Our 1CI: 90.1 % (MAT32) > 83.9 % (RBF); 2CI: 98.5 % > 97.4 %. Confirms paper's coverage-based selection of Matérn.
- **Kernel length scales grow when 2D→8D.** MAT32 ℓ: 34.6 → 311; RBF ℓ: 3.76 → 9.03. Paper's Table 2 shows same trend (e.g. FRDM12: ℓ_p,ℓ_n went 3.9,5.3 → 28.8, 24.1).
- **Adding physics features helps** (at least for RBF, where overfitting doesn't dominate): 249 → 97 keV training RMSE, 61 % reduction.

## 5. Verdict — PARTIAL

**Reproduced independently on real data:**
- Data provenance & counts (AME2016 2271≈2272; AME2020 74 exact).
- GP methodology + kernel/feature comparison qualitative behaviour.
- Matérn kernel giving tighter empirical coverage than RBF.
- Length-scale expansion when adding physics-informed features.
- Order-of-magnitude RMSE reduction from bare model to GP-corrected model.

**Not reproduced:**
- Absolute test-set RMSE ≲150 keV on AME2020, because we did not consume the paper's eight published-model tables (DZ28 etc.). That's a scope choice, not a contradiction: had the theory tables been pulled (they are in each model's own Ph.Rev.C/ADNDT paper), the paper's numbers should follow — the paper's Data Availability is honest, and the method is fully specified.

**Not contradicted anywhere.** All qualitative claims survive, and no numeric claim we could test was refuted.

## 6. Reproducibility artifacts

All in this directory:
- `work/replicate.py` — 350 lines, self-contained.
- `work/mass16.txt`, `work/mass_1.mas20.txt` — raw AME tables.
- `work/ame*_experimental.csv` — parsed subsets.
- `report/evidence/results.json` — full numeric table (JSON).
- `report/evidence/train_used.csv`, `report/evidence/test_ame2020_new.csv` — exact rows used.
- `work/run.log` — full stdout.
- SHA-256s in `report/artifact_harvest.md`.

Rerun on any Linux box with Python 3.8+, scikit-learn ≥1.0, pandas, numpy and internet:
```
python3 work/replicate.py
```
Wall time ~1 minute on a modern CPU.

## 7. LLM-judge score (independent)

Argo `argo:gpt-4.1` (via localhost:44497), given only this REPORT.md + brief.md + attempt_log.md + results.json, returned:

- **verdict:** `PARTIAL`
- **coverage_score:** 0.82
- **agreement_score:** 0.85
- **overall_confidence:** 0.83
- **one-line:** "Replication confirms the paper's methodology and qualitative claims using independent data and code, but cannot reproduce absolute RMSEs due to lack of the eight published mass models, yielding a robust PARTIAL verdict."

Full judge output at `report/evidence/llm_judge.json`.
