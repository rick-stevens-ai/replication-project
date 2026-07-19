# Failure / Gap Analysis — brazovskii2003

**Verdict: PARTIAL (mechanism-level REPLICATED), coverage 8/10, agreement 9/10.**

## Single most important caveat (why this is PARTIAL, not REPLICATED-full)
**This is a short ECRYS-2002 proceedings paper that presents its results "without
derivations" (l.173) and contains ZERO numerical tables.** There is therefore no
tabulated data to fit against: agreement is necessarily scored on **functional forms
and order-of-magnitude claims**, not on reproducing published numbers. This is an
intrinsic property of the source document, not a shortfall of the reimplementation —
but it is exactly why agreement caps at 9/10 (a form/scaling match cannot earn a
perfect data-fit score) and why the paper is classed PARTIAL rather than a full
numeric REPLICATED.

## What reproduced (high confidence)
- **Combined Mott–Hubbard Hamiltonian identity** `-Us cos2phi - Ub sin2phi =
  -U cos(2phi-2alpha)` to machine precision (max abs err 4.4e-16 over a phi grid),
  with the numerical ground-state minimum sitting at phi=alpha. EXACT.
- **Noninteger alpha-soliton charges** `q=-2alpha/pi` and `1-2alpha/pi` evaluated
  directly from alpha. EXACT.
- **Optical-edge ratio** `omega_t/(2*Delta) = pi*gamma/2 = 0.393` at gamma=0.25,
  confirming the edge lies well below the two-particle gap 2*Delta (the paper's
  central optics claim). MATCH.
- **Full dielectric response Eq.(2):** Fano antiresonance at omega_0 gives
  eps/eps_inf = 1 exactly; the combined-resonance and FE-soft-mode formulas confirmed
  as the Z->1 (criticality) limit of the exact denominator roots.
- **Curie law** eps(0)/eps_inf = 1 + A/(1-Z) reproduced exactly (1/|t| divergence to
  5.5e-16); amplitude A=900 matches the paper's own ~1e3 estimate.
- **Spin-Peierls gap** Delta_sigma ~ Uao^{2/3} and the core<<tail length hierarchy
  (xi_sigma/xi_rho = 7.37). MATCH.
All 10/10 verdict checks pass; live re-run on 2026-07-19 matched the saved JSON.

## The `≈`/`~` formulas: a methodological non-failure
The paper's combined-resonance `omega_0t^2 ≈ omega_0^2 + omega_t^2` and soft-mode
`omega_fe^2 ≈ (1-Z)/(omega_0^-2 + omega_t^-2)` carry `≈`. Testing them at an
arbitrary Z (e.g. Z=0.5) gives ~7% deviation and would be a **false miss**. They are
the leading-order Z->1 (T->T0, criticality) expansion of the EXACT roots of the
Eq.(2) denominator quadratic. Verified correctly by scanning Z=0.5->0.9999 and showing
the relative error decreases monotonically (7.0% -> 1.2e-5). Monotone convergence to
the stated limit IS the verification — this is not a discrepancy.

## What did NOT reproduce — scoped out (coverage-capping, EXPECTED)
1. **Quantum breather spectrum** between omega_t and 2*Delta (soliton-antisoliton
   bound states). The paper mentions this "sequence of quantum breathers" but gives
   **no closed form** — nothing to reimplement algebraically. Requires a sine-Gordon
   breather / optical-conductivity calculation (see open_questions Q1). This is the
   single largest reason coverage caps at 8/10. EXPECTED scope-out, not a shortfall.
2. **Microscopic mass renormalization** U -> U* and the origin of gamma (Krho) from
   electronic interactions (ripplon analogy) — given only as scaling relations, checked
   structurally but not derivable to absolute numbers (Q2).
3. **Temperature laws** omega_t(T), omega_cr(T) hence Z(T) — the paper invokes
   "reasonable suggestions"; the Curie/soft-mode forms were verified GIVEN 1-Z ~ t, but
   deriving that proportionality needs an LGD model (Q3).

## Free normalizations (tested ratios, not absolutes)
The prefactor C in Delta ~ C*U^{1/(2-2gamma)}, the plasma frequency omega_p*, and the
T-laws are not fixed by the paper; representative values were chosen. Only dimensionless
ratios and scaling exponents are tested. The experimental epsilon ~ 1e4 * T0/(T-T0) is
the number the paper itself only approximately matches (its own estimate is ~1e3=A) —
it is NOT a target this reimplementation must hit.

## Tooling gaps (NOT physics)
- `marker` / `nougat` not installed -> `extraction/marker.md` and `extraction/nougat.mmd`
  are honest pdftotext interims with in-file NOTE headers and the regenerate commands;
  key equations hand-transcribed into LaTeX in nougat.mmd + REPORT.tex.
- `pdflatex` not installed -> `REPORT.tex` shipped as source (compiles off-host).

## What would raise the verdict
Reimplementing the quantum breather spectrum (Q1) and deriving the T-laws from an LGD
free energy (Q3) would push coverage toward 9–10; obtaining experimental spectra and
refitting with the full Eq.(2) (Q4) would let agreement be scored against real data
rather than functional forms, potentially closing the PARTIAL -> REPLICATED gap.
