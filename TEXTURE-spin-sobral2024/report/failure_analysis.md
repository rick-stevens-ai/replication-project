# Failure Analysis — sobral2024 (arXiv:2410.10949)

## What failed / friction
1. **C2 metric mistake (fixed).** First tried to verify spin-rotation symmetry via individual
   eigenvector <Sz> of the 4x4 chargon(x)spin Hamiltonian -> got |pol|=1.0 (apparent failure).
   Root cause: for a spin-DEGENERATE doublet, eigh returns an ARBITRARY basis within the degenerate
   subspace, so a single eigenvector can have <Sz>=+/-1 even though the pair is unpolarized. Fix:
   verify spin-rotation symmetry via BAND DEGENERACY (within-doublet gap ~0), the physically correct
   test. Now within-band spin splitting = 2.7e-15 (spin-symmetric confirmed).
2. **LLM-judge endpoint.** opus-4.x aggregator parse error 2026-07-19; used free sonnet-4.6.

## Residual gaps (=> PARTIAL, reduced-scope)
- **Bare chargon only.** We implemented the App-C chargon DISPERSION; the physical ELECTRON spectral
  function (Fig.3) needs convolution with the spinon Green's function (Open Q1) -- not done.
- **No self-consistent SB mean field.** Which fractionalized phase (U(1) vs Z2 A1/B1/B2/A3) is
  energetically selected requires solving the SB gap equations (Open Q2) -- not done.
- **Gauge classification / spin-liquid taxonomy** not reproduced (deep group theory).
- **H0, t, t', mu illustrative**, not fit to the paper's specific values.

## What's needed to close
Spinon Green's function + convolution for A(k,omega) (Open Q1); self-consistent SB mean field (Open Q2);
gauge-field-restored electron transport (Open Q5). See open_questions.json.

## Honesty note
Verdict PARTIAL is correct: the CONCEPTUAL headline (spin-symmetric band splitting: split d-wave-
anisotropic Fermi surfaces with preserved spin-rotation symmetry) is reproduced exactly from the
App-C chargon equations, with a clean contrast against ordinary altermagnetism; the full many-body
machinery (SB mean field, spin-liquid classification, spinon-chargon electron spectral function) is
out of scope.
