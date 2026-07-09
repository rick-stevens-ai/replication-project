# Testable claims — Tobias et al. 2013 (PLOS ONE 0057953)

Categorised as: (cov) already covered in pass-1 REPORT; (new) added in this re-pass; (blocked) requires unavailable raw data.

## A. Numerical / parameter-table claims

- **A1 (cov):** 9-reaction ODE model, listed parameter values, integrates to a steady state. — *covered, code/lucid_model.py*
- **A2 (cov):** DSB count scales linearly with LET; 28 DSBs at LET=170 keV/µm. — *covered*
- **A3 (new):** "ion fluence 3·10⁶ /cm² + 35 DSBs/Gy + LET 170 keV/µm → 28 DSBs/track" arithmetic consistency check (File S1). — **NEW**
- **A4 (new):** Theoretical free-diffusion coefficients Dcalc for GFP-tagged NBS1 (137 kDa) and MDC1 (257 kDa), starting from pure-GFP Dcalc=12 µm²/s, given by cube-root mass scaling. Paper: NBS1 Dcalc=7.0, MDC1 Dcalc=5.7 µm²/s. — **NEW (cheap)**
- **A5 (new):** "0.83 s for GFP to travel 6.3 µm" arithmetic from D=12 µm²/s (text Sec. "Protein mobility in untreated cells"). — **NEW (cheap)**
- **A6 (new):** "~40 s for NBS1, ~340 s for MDC1 to traverse 6.3 µm" from Deff=0.25 and 0.029 µm²/s. — **NEW (cheap)**
- **A7 (new):** Pan-nuclear MDC1 binding constants after high LET reported as k\*on = (74±2)·10⁻⁵ 1/s, koff = (193±4)·10⁻⁵ 1/s (text). Cannot re-derive without raw FRAP frames, but consistency with Sprague global-binding model can be checked via reported numerical signs/magnitudes. — *blocked-fit* (only the values themselves can be re-typed)
- **A8 (new):** Local MDC1 X-ray binding constants k\*on=(587±13)·10⁻³ 1/s, koff=(425±6)·10⁻⁵ 1/s. — *blocked-fit*

## B. Model-output / Figure-11 claims

- **B1 (cov):** τ₆₃ for NBS1 falls with LET; reported representative panels A,B,C. — *covered*
- **B2 (cov):** Inner-focus contribution at plateau grows with LET; "nearly 60% for uranium". — *covered* (we got 51% at LET=10290; new check at 14350 below).
- **B3 (cov):** All ATM activated within ~10 min at high LET. — *covered*
- **B4 (cov):** Bend in ATM curve near t≈300 s. — *covered (visual)*
- **B5 (new):** At LET=170 keV/µm only a small fraction of ATM is activated at long times (paper text); quantify. — **NEW**
- **B6 (new):** At LET=14350 keV/µm, inner-focus NBS1 fraction at plateau is ~60% (paper text: "nearly 60% for uranium"). Pass-1 only ran C at 10290. — **NEW (cheap, ODE)**
- **B7 (new):** Self-consistency of all 12 NBS1 scaling factors — pass-1 mentioned this but did not save numbers. Write per-panel implied-LET ledger to disk. — **NEW (cheap)**
- **B8 (new):** Mono-exponential time constants τ₆₃ for the full panel ladder (A..L), trending downward as scaling factor (and implied LET) increase. — **NEW (cheap)**
- **B9 (new):** Modified MDC1 model with cylindrical diffusive influx ∝ (4Dt)^(1/2) at low LET (Deff=0.029 µm²/s) gives improved low-LET MDC1 saturation behavior (paper Fig 12B claim). — **NEW (medium)**

## C. Empirical / FRAP-table claims

- **C1 (new):** Table S1 monotone trend: koff(NBS1) decreases from X-ray (0.047) to high-LET ions (~0.011) as inner-focus fraction grows. — **NEW (cheap, just statistical test on table values)**
- **C2 (new):** With CK2 inhibition, koff is much smaller (Ar+CK2i = 0.007, U+CK2i = 0.004) than without (Ar 0.016, U 0.011), consistent with inner-focus binding being slower. — **NEW (cheap)**
- **C3 (new):** koff at high-LET (Xe 8655, U 14350) approaches koff(Ar+CK2i)=0.007 (paper Fig 8A claim "approach values close to..."). — **NEW (cheap, quantitative gap test)**

## D. Wet-lab-only / unreproducible without raw data

- **D1:** Live-cell beamline microscopy (GSI heavy-ion accelerator). *Blocked: missing artifact = raw image stacks (.tif/.h5) at GSI, not published.*
- **D2:** FRAP recovery curves digitization for fitting (Sprague/Soumpasis). *Blocked: missing artifact = raw FRAP intensity-vs-time CSVs.*
- **D3:** Immunocytochemistry confocal images of NBS1/MDC1 foci size under CK2i (Fig 8B). *Blocked: missing artifact = raw confocal IF images.*
- **D4:** 53BP1 lag phase up to 100 s (Fig S2). *Blocked: digitization would be the only handle; not reliable enough for a numerical claim. (Qualitatively trivial.)*

## Re-pass scope

We reproduce A3, A4, A5, A6, B5, B6, B7, B8, C1, C2, C3 — 11 new testable claims, all cheap (arithmetic / stat / ODE evaluation, no fitting). Plus B9 (medium-cost modification).
