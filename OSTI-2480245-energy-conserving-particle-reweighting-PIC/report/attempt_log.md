# Attempt Log — OSTI 2480245

**2026-07-01 (night wave)**

1. Read WAVE_BRIEF_2026-07-01.md + OSTI100_TOPUP50 priority list. Only existing OSTI dir was 2997724 (skip). Walked ranks; picked **rank #2, OSTI 2480245** (energy-conserving particle reweighting for PIC) — self-contained numerical method with fully specified equations + test parameters, no proprietary DATA needed (only the code Aleph is proprietary, which we work around by reimplementing the operators).
2. OSTI purl times out from CherryRd (curl exit 28, twice). Fetched PDF successfully via `ssh uicgpu` (proxy internet), scp'd back → `work/paper.pdf` (5.5 MB, 5 pp). `pdftotext -layout` → `work/paper.txt` (1582 lines).
3. Extracted the full method: split (Sec 3.1, Fig 2, Eqs 4–5), merge (Sec 3.2, Fig 3, Eqs 6–12), target-weight (Eqs 2–3), and both numerical tests (4.1 exponential sheath Phi_w=-15V L=5um bump-on-tail; 4.2 0D H2 ionization growth, Nc 10..10000, beta~3.06/s, Bolsig+ compare).
4. Checked artifact availability: Aleph is Sandia proprietary; NO public code/data package. Decided on operator-reimplementation strategy.
5. Wrote `work/reweight.py` — faithful numpy reimplementation of the split/merge operators (Eqs 2–12) with the constant-element-field energy correction, imaginary-velocity rejection, symmetric displacement, Eq-9 merge cutoffs, Eq-11 KElost.
6. Wrote `work/test_conservation.py` — 20000 random splits + ~18600 merges in the Test-4.1 sheath field. Result: C1 mass 0.0, C2 COM 2.9e-16, C3 energy 4.4e-16, C4a mass 0.0, C4b momentum 4.0e-16, C4c KElost>=0 (0 negatives, 1388 cutoff rejections), C4d KElost median 0.062% / 95th 0.587%. **All 8 checks PASS.** (Fixed a numpy-bool JSON serialization bug.)
7. Wrote `work/test_growth_independence.py` — Test-4.2 structural abstraction (ionization rate nu=3.06/s, reweighting control loop, +-10% count bounds). Result: **beta=3.0507 s^-1 for every Nc in {10,100,1000,10000}, rel spread ~1e-15**; computational count stayed in [Nc,1.11*Nc]. Matches paper's ~3.06 s^-1 + "independent of Nc" + bounded-count claims.
8. Wrote `work/test_growth_stochastic.py` to probe the "precision improves with Nc" sub-claim. Could NOT isolate it — the abstract 0D model recovers beta to machine precision at all Nc (renormalization suppresses the noise that Aleph's DSMC would carry). Reported honestly as neither-confirmed-nor-refuted rather than over-claiming.
9. LLM-judge (free Argo **gpt-5.2** via localhost:44497) fed a structured prompt with all claims + results + honest limitations. Verdict: **PARTIAL**, coverage 0.78, agreement 0.80. Saved `evidence/llm_judge_verdict.json`.
10. Wrote report artifacts. Done.

## What worked
- Operator math is exactly reproducible; every conservation invariant holds to floating-point roundoff.
- uicgpu as an OSTI-fetch proxy when CherryRd direct fetch times out.

## What was out of reach
- Aleph (proprietary) → no full PIC sheath transient (Test 4.1 VDF plots) or full DSMC/Bolsig+ physics (Test 4.2 EEDF/reaction-rate curves).
- "precision-improves-with-Nc" sub-claim needs Aleph's stochastic DSMC noise structure.
