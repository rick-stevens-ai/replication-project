# Failure analysis — arXiv:2502.16657 replication

Honest record of what went wrong during the build and how each issue was fixed.
None of these compromise the final results; they are documented so the reusable
kernel is trustworthy for sibling loop-current papers.

## F1. Wrong kagome bond geometry -> wrong spectrum (FIXED)
- **Symptom:** first `hamiltonian()` gave E(Gamma)=[-4,2,2] but M=[-1.41,0,1.41],
  K=[-0.51,0.02,0.48] with NO Dirac degeneracy and NO flat band away from a
  single k. The two lower bands never touched.
- **Root cause:** I hand-assigned inter-cell bond vectors (e.g.
  `d_ca_2 = TAU_A - TAU_C + A1 + A2`) that did not correctly enumerate the four
  nearest neighbors of each kagome site; the resulting NN graph was not the
  kagome lattice.
- **Fix:** switched to the textbook closed form
  `H_ab(k) = -2t cos(k . a_i/2)` using the three triangular half-bond vectors
  `a1/2, a2/2, a3=a2-a1`. Verified against known kagome facts: flat band at
  `+2t` everywhere (to 1e-6), Dirac touching at K at `-t` (gap ~1e-15), M-point
  saddle at `0`. Peierls phases are then added per bond as
  `-t[e^{i(k.d+phi_up)} + e^{i(-k.d+phi_dn)}]`.
- **Lesson (kernel rule):** always validate a new tight-binding Hamiltonian
  against its analytically known high-symmetry spectrum before using it.

## F2. Wrong flux pattern -> no gap, non-convergent Chern (FIXED)
- **Symptom:** the "staggered" pattern (up-triangle bonds +f, down-triangle -f)
  gave a tiny pseudo-gap (~0.02-0.04, grid-limited) between the two lower bands,
  and the Chern number did NOT converge across grid sizes (values 2,0,1,0 for
  nk=40,60,90,120 at f=0.5). The flat band also stayed pinned to the dispersive
  band at Gamma (g12 = 0).
- **Root cause:** the +f/-f staggering leaves a near-degeneracy of the two lower
  bands; that pattern breaks TRS but does not produce an isolated Chern band.
- **Fix:** used the **uniform directed** flux (same +f on every NN bond) — the
  Ohgushi-Murakami-Nagaosa kagome Chern insulator. This opens a robust gap
  (1.61 t at phi=pi/4) and gives a **converged** Chern set (+1,0,-1) identical
  for grids 30-90. The kernel docstring now recommends `flux_pattern='uniform'`
  for the LC-Chern demonstration and flags `'staggered'` as non-gapping.
- **Lesson:** a non-convergent Fukui-Hatsugai-Suzuki Chern number is a red flag
  for an ill-isolated (near-touching) band, not a numerical parameter to tune.

## F3. Naive scalar multipole proxy misclassified 2Q-1Q (FIXED)
- **Symptom:** `triangle_flux_from_config` v1 used dipole = sum(Phi_i). That gave
  2Q-1Q (1,1,0) -> dipole=2 -> "ferromagnetic", contradicting Table I (2Q-1Q is
  antiferromagnetic, moments cancel).
- **Root cause:** the net magnetic dipole of an M-point LC texture is NOT the
  linear sum of components; the paper explicitly says the 3Q FM moment survives
  only *because of the anharmonic coupling*, i.e. it is the fully symmetric
  triple product Phi1*Phi2*Phi3, and the 2Q moments cancel by triangle geometry.
- **Fix:** replaced with symmetry-correct invariants:
  dipole ~ Phi1*Phi2*Phi3 (A-type, nonzero only for 3Q), octupole via the E-type
  combination for sign-changing textures. Now 3Q=FM, 2Q-1Q=AFM,
  2Q-3Q=ferro-octupolar — all three Table I rows correct.
- **Caveat (honest):** this is still a symmetry-based proxy, not a direct orbital
  magnetization computed on the 2x2 (12-site) magnetic supercell. Computing the
  real lattice magnetization is listed as open question #2. The proxy reproduces
  the *classification*, which is what Table I asserts, but the absolute moment
  magnitudes are not claimed.

## F4. DOS Gaussian sum too slow (FIXED)
- **Symptom:** initial `dos()` looped over ~1M eigenvalues in pure Python for
  each broadening; the eta-scan hung > 60 s and was killed.
- **Fix:** vectorized `all_eigvals()` (stack of Hamiltonians, batched
  `eigvalsh`) and replaced the Gaussian sum with a fine histogram convolved with
  a Gaussian kernel. Full run now ~1-2 min.

## F5. Vision/PDF model verification unavailable (WORKED AROUND)
- The `image`/`pdf` model tools were credit-blocked (Anthropic balance) and the
  workspace vision path was restricted. Figure inspection by model was not
  possible.
- **Mitigation:** all physics is verified NUMERICALLY (band energies, gaps,
  Chern numbers, DOS fit) in `work/results.json`; the PNG figures are rendered
  from the same verified arrays, so visual inspection is not load-bearing for
  the verdict. `pdftotext` gave clean text so no vision was needed for ingest.

## Not a failure, but a scope note
The paper is a **perspective** with no primary numerical tables. "Agreement" is
therefore judged on reproducing the asserted physics correctly, not on
digit-matching. All asserted claims reproduced.
