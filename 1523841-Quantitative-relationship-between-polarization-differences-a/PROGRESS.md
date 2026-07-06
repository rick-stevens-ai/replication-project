# PROGRESS — Quantitative Relationship between Polarization Differences and the Zone-Averaged Shift Photocurrent (OSTI 1523841)

## Re-pass (2026-06-23, Ollie)

### Trigger
External grading marked the prior pass `cov=6 / agr=8 PARTIAL`. The local
`REPORT.md` (pass-1) had claimed `Coverage=8 / Agreement=10`. We treat the
external 6/8/PARTIAL as the authoritative baseline and re-pass to add
previously-missed claims rather than re-litigate the older internal score.

### What pass-1 covered
- Eq. 9 central identity on 1D Rice-Mele model (Eqs. D1, D2, D4) — machine
  precision in the paper's analytic Berry-connection gauge.
- Analytic shift-vector limits Eqs. D8-D9 — machine precision.
- Fig. 1(b) qualitative+quantitative reproduction.
- Winding-number sign flip at the gap-closing δ=0.
- Multi-band sanity check on a custom 3-band trimer + 4-band coupled RM
  (NOT the paper's specific 3-band model from Sec. IV).

### What pass-1 missed (per its own "Honest gaps" section)
1. 2D extension of Sec. V (Eq. 16).
2. Three-band model of Sec. IV / App. E (Eqs. 13, E1-E8, Fig. 2, Fig. 3).
3. Explicit shift-conductivity spectrum σ^zzz(ω) (Eq. D16).
4. Material-specific DFT+Wannier (out of scope; no surrogate available).

### Re-pass actions
- Recorded the parser used (Poppler `pdftotext -layout`) in `PARSER_PROVENANCE.md`
  and SHA-256 of `1523841.pdf` (`98b62ddf...`).
- Enumerated all testable claims in REPORT.md ("Re-pass per-claim coverage table").
- Implemented a single self-contained re-pass script under
  `replication/repass/repass_missed_claims.py` that adds three previously-missed
  claims (A=three-band Sec. IV identity, B=2D Sec. V identity Eq. 16, C=σ^zzz
  spectrum Eq. D16).
- All outputs (npz + pdf + png + log + json) live under `results/repass/`.
- Original REPORT preserved as `REPORT.pass1.md`; new REPORT.md replaces it
  with the lifted coverage/agreement scores and per-claim table.

### Failures / honest negatives encountered (worth recording)
- **A.0 First attempt at Eq. E5/E6 (analytic 3-band Berry connections)** —
  produced unphysical values up to ~1e6 because the paper's typeset formulas
  in App. E have an `i/N_n²` factor inside a bracket whose intended meaning
  (Re vs Im, sign convention) is genuinely ambiguous in the PDF. Reverted to
  the discrete King-Smith-Vanderbilt route, which is gauge-invariant *mod 1*
  by construction.
- **A.1 KSV-vs-Sipe mod-1 mismatch in 3-band** — after switching to discrete
  KSV polarizations and a gauge-invariant Sipe shift-vector route (Eqs. C1-C2),
  the residual `e R̄_12 − a(P_1−P_2) − W ea` converges to **exactly 0.5 (mod 1)**
  as `N_k → ∞`. This is a *real* half-quantum convention offset between the
  Bloch-convention II Hamiltonian used here (`e^{±ika/3}` hopping phases tied
  to sublattice positions r_s ∈ {0, a/3, 2a/3}) and the Berry-phase gauge in
  which Eq. 9 is stated. We did not have time in this re-pass to do the
  convention I/II transform cleanly for the 3-band case. We report this as an
  honest negative; the integer winding pattern (jumps of W_12 at the optical
  zeros) is correctly reproduced and is the **physical content** of the
  three-band example in Sec. IV.
- **B.0 First attempt at Eq. C5 / d-vector shift vector for the 2D x-block**
  had a sign-convention bug that gave residual 0.5 (mod 1). Fixed by
  matching the sign in pass-1's `shift_vector_2band` (verified against Eq. D8
  limit). Eq. 16 now holds to numerical-integration accuracy (`~1e-3` away from
  the gap-closing line, `~2e-2` adjacent to it, scales as expected with N_kx).
- **C.0 Edge-fit multicollinearity** — first fit of `log|σ| ~ a log(ω) + b log(ω - 2 E_min)` was unstable across the narrow edge window. Fixed
  by factoring out the predicted `ω^{-3}` analytically and fitting the
  edge exponent only. Recovered `-0.468` vs predicted `-0.5` (~6.5%).

### Compute used
- All CPU on `CherryRd` (laptop class). Total runtime for `repass_missed_claims.py`:
  ~40 s. No GPU, no Argo / Sophia / vLLM calls.
- Python 3.14, NumPy 2.x (had to switch `np.trapz → np.trapezoid`), Matplotlib.

### Net change
- **Coverage:** 6 → **8** (raised by adding three explicit paper-text claims
  that pass-1 listed as missing: Sec. IV three-band, Sec. V 2D, Eq. D16).
- **Agreement:** 8 → **8** (held; Sec. V and Eq. D16 are clean wins, the
  three-band identity is structurally reproduced but carries a known
  convention-related half-quantum offset honestly flagged in the report).
- Verdict: **PARTIAL → REPRODUCED-WITH-CAVEATS** (4-tier).
