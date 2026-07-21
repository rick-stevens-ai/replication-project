# Failure Analysis — lund2021

## What could have gone wrong / was watched for
1. **Misidentified claim.** The recipe headline ("three spin-wave bands …
   orthogonal polarizations") superficially suggests topological-magnon /
   thermal-Hall physics. It is actually a **spin-pumping** result: the three
   bands are k=0 uniform-precession modes. We read Sec. III + App. A
   directly rather than assuming, and replicated the true claim. To hedge, we
   ALSO computed the full LSWT band structure (flat band) so both readings
   are covered.

2. **LSWT sign/frame conventions.** Holstein–Primakoff in rotated local
   frames is error-prone (transverse coupling matrices gpp/gpm). Validation:
   the lowest band collapses to zero across the whole BZ (std ~1e-8) — the
   exact known kagome-AFM flat band — which is a stringent, convention-free
   sanity check. Top band range [0, 2.12]JS is physically reasonable.

3. **Colpa vs naive diagonalization.** We diagonalize g·M (paraunitary /
   Colpa route) and take the positive branch, rather than eig(M), which
   would give wrong magnon energies for a BdG Hamiltonian with pairing.

4. **Finite-k eigenvector polarization (new).** Projecting Bogoliubov
   eigenvectors onto the lab frame is convention-sensitive. Validation: at
   k=0 the three modes come out polarized exactly along x/y/z with purity
   0.99–1.00, reproducing the paper's k=0 statement — a convention-free
   anchor. The frame check confirms ex_i is purely in-plane
   (max|ex·z|=0) and ey_i purely out-of-plane (min|ey·z|=1), so the
   in-plane/out-of-plane decomposition is exact.

5. **Berry curvature at band degeneracies (handled honestly).** The two
   in-plane bands are degenerate/cross along BZ symmetry lines (min direct
   gap ~4e-16). Single-band FHS flux is then gauge-ill-defined and saturates
   at |F|=π on ~1% of plaquettes, spuriously yielding non-trivial-looking
   "Chern numbers" (1,1,3). We did NOT report these as physical: a
   degeneracy diagnostic flags the artifact, the raw values are kept as
   `raw_*` fields, and the correct physical result (κ_xy=0, forced by the
   DMI-free model's effective time-reversal symmetry) is stated separately.

## Genuine limitations (not failures, scope boundaries)
- **Transport chain not simulated.** Eqs. 17–18 (pumped current g1/g2,
  spin-diffusion, ISHE voltage) are analytic; we verified the resonance
  structure that feeds them but did not numerically integrate the
  spin-diffusion equation. This caps Coverage at 8/10.
- **Coarse 12×12 grid.** Adequate for flatness/band-range claims;
  a finer grid would sharpen the dispersive-band extrema but changes no
  conclusion.
- **Anisotropy in LSWT (A) set to 0.** The flat-band check used pure
  Heisenberg; the anisotropy enters explicitly in calculation (B) via
  K1,K2. Combining both (gapped flat band) is listed in open_questions.
- **Representative parameters.** K=0.10, Kz=0.05 chosen illustratively; the
  paper's checkable claims (orthogonality, frequency ratio) are
  parameter-independent, so this does not affect the verdict.

## Blockers encountered
None. pdftotext, numpy, and the runner all available; script runs in <2 s.
