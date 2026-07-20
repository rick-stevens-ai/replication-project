# Failure Analysis --- Gerguri et al. 2026 surrogate replication

## Verdict: PARTIAL
Gap named: **no DFT+U first-principles total-energy comparison** (scoped out of this run);
the tight-binding + mean-field surrogate reproduces the *mechanism qualitatively* but not
the quantitative U threshold or true structural energetics.

## What worked (honest agreements)
1. **q=1/3 favored at small U.** Surrogate chi_{1/3} > chi_{1/2} for U=0-4, matching the
   paper's U=0 result (q=1/3 over q=1/2 when Ce-4f is valence).
2. **Correlation-driven crossover to q=1/2.** As U raises the Ce-4f flat band, q=1/2
   overtakes q=1/3 at U~=5, near the paper's U*=6 eV.
3. **Near-degeneracy at the crossover.** chi_{1/2} and chi_{1/3} are within ~5-15% around
   U=4-5, echoing the paper's "nearly degenerate at 6 eV".
4. **Correct failure mode for f-as-core.** Removing Ce-4f valence states makes q=1/4 (CO*)
   the winner and strongly suppresses q=1/3 -- exactly the paper's reported f-as-core DFT
   behavior (q=1/3 suppressed, q=1/2 not the ground state, a q=1/4 CO* appears).

## What did NOT reproduce / limitations
1. **No DFT+U.** We never computed real correlated total energies of relaxed Pmma / Imma /
   q=1/4 supercells. The whole first-principles pillar of the headline is surrogated.
2. **Quantitative U mismatch.** Crossover at U~=5 in arbitrary t-units, mapped by hand
   (eps_f = eps_f0 + kU*U); not a genuine 6 eV. Parameters (t_f, eps_f0, k_U, filling)
   were chosen to expose the mechanism, so the exact threshold is not predictive.
3. **Phonon channel omitted.** The paper attributes the structural instability to imaginary
   phonon modes in the q_z=1/2 plane; our electronic-only surrogate cannot capture the
   lattice-driven part of the selection.
4. **Landau curvature, not self-consistency.** Order selection uses the sign/size of the
   quadratic CDW susceptibility, not a self-consistent free-energy comparison at finite
   order parameter. CDW transitions can be first order; the true ground state could differ.
5. **2D single layer.** Real material is 3D (a x a x 2c); no interlayer / c-axis physics,
   no loop-current (iCDW) imaginary order parameter, no superconductivity/TRS-breaking link.

## First failed approach (recorded)
Initial version minimized the CDW condensation energy over a delta sweep. The band energy
was monotone in delta (minimum pinned at the sweep edge) and q=1/2 won for *every* U and
even in the f-as-core control -- which contradicts the paper. Root cause: without a
competing (interaction) cost term, larger delta always lowers the one-body energy, so the
absolute condensation energy is not a valid order-selection criterion. Fixed by switching
to the *curvature at delta->0* (mean-field susceptibility), which correctly ranks competing
q-vectors and recovered the paper's trend and failure mode.

## How to close the gap
Run real DFT+U (see report/open_questions.json next_steps): Wannierize to fix t in eV,
relax the three supercells with Ce-4f as valence, sweep U=0-9 eV, add phonons, and use
self-consistent order parameters.
