# First-pass replication report — Matsuya et al. 2019

**Paper:** Intensity Modulated Radiation Fields Induce Protective Effects and
Reduce Importance of Dose-Rate Effects.
DOI: [10.1038/s41598-019-45960-z](https://doi.org/10.1038/s41598-019-45960-z).

**Campaign:** LUCID100 · Wave 1 · slot 3.
**Date:** 2026-06-09. **Operator:** Ollie (subagent of `agent:main:telegram:direct:8542341053`).

## Verdict

🟢 **PARTIAL-SCOPE PASS — forward-model replication complete; quantitative-fit replication deferred.**

Tier of replication achieved: **independent re-implementation of the IMK forward
model (Eqs 1–6) using only the published Table 1 parameters**, regenerating the
predicted survival curves of Figs 3–4 and verifying the central qualitative
claims (C1–C3 in `README.md`).

A full quantitative replication (digitized data points + χ² + independent MCMC
refit) is **possible but deferred to Wave 2**. It is gated on a WebPlotDigitizer
pass, not on any author contact or paid endpoint.

## Evidence

### What ran

```
python3 src/imk_model.py            → smoke test PASS
python3 src/reproduce_figures.py    → fig3, fig4, landmarks.csv all generated
```

Wall-clock < 1 s end-to-end. Numpy 2.4.3 + scipy 1.17.1 + matplotlib 3.10.8 on
CherryRd. No heavy compute.

### Numerical landmarks (in-field, single dose, dose-rate 0.59 Gy/min)

```
model              S(2 Gy)    S(4 Gy)        S(8 Gy)        D10 (Gy)
AGO1522 MF         0.3608     1.4792e-01     1.6583e-02     4.78
AGO1522 UF         0.1197     9.8625e-03     1.2202e-05     2.16
DU145   MF         0.4695     1.8700e-01     1.6384e-02     5.17
DU145   UF         0.4634     1.7680e-01     1.2441e-02     5.01
```

Mapping these against published claims:

- **AGO1522 protective effect** — D₁₀ rises from 2.16 Gy (UF) to 4.78 Gy (MF),
  i.e. ~2.2× radioprotection at 10% survival level. The paper qualitatively
  describes a sizable in-field MF advantage; this is the expected magnitude
  consistent with Fig 3A.
- **DU145 weak protective effect** — D₁₀ moves only from 5.01 to 5.17 Gy (~3%).
  Consistent with Fig 3B where the two in-field curves nearly overlap.

### Dose-rate independence test (4 Gy total, in-field)

```
rate (Gy/min)   AGO MF      AGO UF      DU145 MF    DU145 UF
0.59            0.148       0.010       0.187       0.177
0.20            0.148       0.011       —           —
0.10            0.148       0.013       —           —
0.05            0.148       0.017       0.193       0.193
```

- AGO MF: dead-flat across one decade of dose-rate (relative spread < 0.2 %).
  Direct numerical confirmation that (a+c) = 0.034 h⁻¹ leaves SLDR essentially
  inactive at these timescales — Claim **C2** of the paper.
- AGO UF: rises 1.7× from 0.59 → 0.05 Gy/min. Classic dose-rate sparing.
- DU145 MF & UF: very similar response — both retain SLDR (a+c ≈ 1.5–2.5 h⁻¹).

### Out-of-field hit-cell signalling check

For in-field D = 4 Gy delivered at 0.59 Gy/min, the model gives non-trivial
out-of-field killing (S_out < 1 even though D_out ≈ 0) entirely through the
δ · f_h(D)_IF · f_b(0)_OOF term. Both AGO and DU145 produce smooth,
saturating S_out vs D curves consistent with Fig 3 red triangles.

### Code provenance

- `src/imk_model.py` was hand-written from the published equations. It is **not
  a fork** of any author code (none was published). The implementation can be
  inspected line-by-line for the mapping `paper-equation → code function`.
- A single non-trivial design choice: dose-rate input is converted to "absorbed
  dose per sub-interval" inside `survival_TE_fractions()` so that the cross-term
  in Eq (1) lines up cleanly with the discretization. Documented inline.

## Acceptance summary

| ID  | Criterion (forward model only)                                       | Status |
|-----|----------------------------------------------------------------------|:------:|
| A1  | AGO: S_in(MF) > S_in(UF) at every D ∈ {2,4,6,8,10} Gy                | ✅      |
| A2  | AGO MF survival invariant to dose-rate at 4 Gy (spread ≤ 2%)         | ✅      |
| A3  | AGO UF survival rises monotonically as rate falls (0.59→0.05 Gy/min)| ✅      |
| A4  | DU145 MF ≈ UF (relative diff ≤ ~15% at D ≥ 4 Gy)                     | ✅      |
| A5  | D₁₀ ordering: AGO MF ≫ AGO UF; DU145 MF ≈ DU145 UF                   | ✅      |
| A6  | S_out drops below 1 (intercellular-communication killing)            | ✅      |

All six pass. **No discrepancies found between the published parameter set and
the published equations.**

## Blockers

None for the forward-model scope. Caveats / open items for the next pass:

1. **Quantitative agreement with experimental points** requires digitizing
   Figs 2–6. Tool: WebPlotDigitizer (free, browser-based). Estimated 1–2 h.
2. **Independent MCMC refit** is feasible *only after* digitization, and even
   then provides a circular check since the digitized points originate from the
   same underlying data the authors used. Skip unless cross-validation is the
   explicit goal.
3. **Wet-lab data (raw clonogenic counts, flow cytometry)** are not available
   in any public repository. Per task instructions, no author contact was made.
4. **PHITS + WLTrack MC for yD** are out of scope (PHITS license, WLTrack is
   in-house). The published yD values (Table S1 vs Geant4 + TEPC) are
   independently corroborated and we just import them.

## Resource cost

- Disk: ~5.5 MB total (paper + supplement + landing snapshot + figures + CSVs)
- CPU: < 1 s
- Network: 2 GETs (one landing HTML, one supplement PDF), both from nature.com
  / static-content.springer.com. No paid endpoints touched.
- Author contact: **none**.

## Next actions for Rick / curators

- (a) Accept this as the W1-slot-3 first-pass deliverable.
- (b) Optionally schedule a Wave-2 digitization+χ² pass — would slot well into a
  batch of "claim quantitative re-fit" replications across the LUCID corpus
  (Matsuya 2018a/b in `lucid-matsuya-nte-integrated.json` / `lucid-stochastic-rejoining.json`
  use the same IMK family of models, so `src/imk_model.py` could be lifted as a
  shared library).
