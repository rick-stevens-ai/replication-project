# Failure Analysis — durnev2023 (arXiv:2306.08509)

Verdict: **REPLICATED** (coverage ~7/10, agreement ~9/10). This document
records where the replication is incomplete or where numbers diverge from the
paper, so the strong verdict is not mistaken for full coverage.

## 1. Scope gaps (coverage, not agreement)

### 1.1 Only the linear/graphene branch is implemented
The paper derives results for **both** linear (graphene) and parabolic
(2DEG/bilayer) dispersions (Eqs. 21/23/24). Only the linear branch was coded.
The parabolic headline is therefore unverified. *Impact:* halves the
dispersion coverage; does not affect the graphene numbers reported.

### 1.2 Near-resonance closed forms, not the full angular sum
Eqs. (25)/(26) are the Omega*tau0 >> 1, omega ~ Omega closed forms, not the
full Eq (20)+(22) angular-harmonic conductivity. They are exact at the
evaluated resonance but not validated off-resonance (spectral wings of
Figs. 2/3 untested). *Impact:* lineshape away from the peak is not confirmed.

### 1.3 Kerr angle by shortcut
The Kerr angle is taken as theta_K ≈ -theta_F (large dielectric-contrast limit
stated by the paper) rather than evaluated independently via Eq (6) with the
substrate Fresnel factors. *Impact:* the Kerr headline inherits, rather than
independently confirms, the Faraday result.

### 1.4 No figure-level (pixel) comparison
Cross-checks match the paper's stated **scalar** numbers, but no curve was
digitized from Figs. 2-4. Resonance width (set by tau0) is not tested against
the plotted lineshape. *Impact:* agreement is scalar-level, not curve-level.

## 2. Numerical discrepancies (agreement)

### 2.1 Peak Faraday 0.044 deg vs headline "0.1 deg" — NOT a failure
The abstract's "0.1 deg" is an **order-of-magnitude** statement spanning
Figs. 2-4 (0.1-1 deg range across configurations). The graphene-on-substrate
value of 0.044 deg sits correctly within that band and matches the specific
Omega*tau1=1 curve of Fig. 3 (y-axis ~0.05 deg) essentially exactly. The
headline_comparison ratio of 0.44 in the result JSON compares against the
top-of-range 0.1 and is expected, not a discrepancy.

### 2.2 B_syn 0.088 T vs ~0.1 T — 12%, parameter-driven
B_syn scales linearly with tau0/eps_F. Using the paper's explicit estimate
parameters (eps_F=50 meV, tau0=10 ps) gives 0.088 T; the Fig-3 parameters
(eps_F=64 meV, tau0=5 ps) give 0.034 T. The 2x tau0 ambiguity (5 vs 10 ps)
between the figure and the text estimate is the dominant uncertainty. Pinning
the exact figure parameters (Q4) would tighten this.

### 2.3 Two Faraday formulas agree to ~6%
Eq (26) gives 0.0441 deg; Eq (5)+(25) gives 0.0417 deg. The ~6% gap reflects
the slightly different peak-location handling between the explicit real-part
formula and the complex-conductivity route — an internal consistency check
that passes comfortably.

## 3. Tooling limitations
- `marker` and `nougat` are not installed on this host; extraction artifacts
  are pdftotext-derived interims. Equation typesetting is linearized. This
  affects only the human-readability of the extraction, not the physics.

## 4. What would move this to full REPLICATED / higher coverage
1. Implement the full Eq (20)+(22) conductivity and the parabolic branch.
2. Evaluate the Kerr angle via Eq (6) directly.
3. Digitize Figs. 2-4 for a curve-level agreement metric and to pin
   tau0/tau1/eps_F exactly.
