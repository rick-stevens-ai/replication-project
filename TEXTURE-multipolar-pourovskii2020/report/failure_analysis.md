# Failure / Out-of-Scope Analysis

## Out-of-scope (cannot reproduce without proprietary/heavy machinery — NOT faked)

### OOS-1: The full ab initio pipeline
The paper's results all originate from a charge-self-consistent DFT+DMFT
(Hubbard-I) calculation in **Wien2k + TRIQS** with a force-theorem (FT-HI)
extraction of inter-site exchange. Reproducing this requires:
- a licensed/full-potential actinide DFT code (Wien2k),
- TRIQS + Hubbard-I solver,
- Np pseudopotential/APW setup, spin-orbit second variation, FLL double counting,
- the force-theorem two-site fluctuation derivative dSigma/drho.
None of this is available in this environment, and none of it is a "free
endpoint." **Marked out-of-scope; not attempted, not faked.**

### OOS-2: The 15x15 SEI matrix element magnitudes
The specific couplings (DD x-x = 1.6 meV; OO xyz->y(x^2-3y^2) = -1.5 meV;
DO z->z^3 = 0.95 meV; 38 distinct symmetry-reduced elements) are the direct
numerical output of OOS-1. We use their *reported* magnitudes only qualitatively
(in open_questions and to sanity-check orders of magnitude). We do **not**
fabricate a matrix.

### OOS-3: RPA dynamical susceptibility / INS S(q,E)
Fig. 3 S(q,E) requires the full Vq Fourier transform of the ab initio SEI
matrices fed through the RPA formula chi = (I - chi0 Vq)^{-1} chi0. Without the
SEI matrix (OOS-2) the absolute spectra cannot be produced. We instead reproduce
the *level positions* (6.1, 12.2 meV) that set the INS peak energies via the
tractable single-site model (C3), which is the physically meaningful, checkable part.

### OOS-4: Real-space 3k multipolar texture (Fig. 2)
The four-sublattice orientation of rank-5 triakontadipoles / rank-4
hexadecapoles / quadrupoles requires the upfolded J=9/2 density matrices from the
converged mean-field solution of the full Hamiltonian. Beyond the minimal model.

## Genuine model limitations (partial reproductions)

### LIM-1: Gamma6 doublet energy (126 meV vs >300 meV)
Our single-multiplet LLW model (J=9/2 only) reproduces the CF *ordering* and the
68 meV excited-Gamma8 scale, but places the Gamma6 doublet at 126 meV, well below
the paper's ">300 meV". Root cause: the LLW model omits **J-mixing** — the paper
explicitly notes admixture of excited J=11/2 and 13/2 multiplets into the Gamma8
wavefunctions, and uses an extended-Wannier basis that folds hybridization into
the CF. Both effects are absent from a single-J LLW diagonalization. This is a
known, expected limitation, quantified in open_questions Q1. **Partial, honest.**

### LIM-2: T0 is an input, not an output
We tuned the effective Gamma5 SEI Jex=6.44 meV to hit T0^MF=38 K. The paper
obtains T0 as an *output* of the ab initio SEI matrix. Our contribution is to
confirm the *second-order character* and the *xi^2(T) striction shape*, which do
not depend on the absolute Jex. Getting T0 as an output requires OOS-2.

### LIM-3: Diagonal-uniform SEI approximation for C3
The exact 2.00 ratio was obtained with the diagonal-uniform Gamma5 SEI (the
Santini-2006 semi-empirical form the paper itself references). The paper's full
Hamiltonian has large off-diagonal DO/OO couplings; whether the ratio survives
those is open (open_questions Q2). Note the paper states its own ab initio
excited-singlet energy "is in agreement with" this same semi-empirical estimate,
so the approximation is well-motivated.

## Debugging notes (things that went wrong and were fixed)
- **First CF attempt** (`cf_j92.py` with Hutchings Stevens factors on the raw
  A_k^q<r^k>) gave the right Gamma8-ground symmetry but wrong level ordering and
  x=+0.395 instead of -0.54. Root cause: ambiguity in the 6th-order cubic sign
  convention (O60-21 O64 vs +21) and in absorbing the Stevens theta_k factors.
  **Fix:** moved to the convention-independent LLW W,x parametrization, which is
  exactly how the paper reports its CF (x=-0.54). This cleanly reproduced the
  ordering and the correct sign of x.
- **Scratch operator code** left in the first draft of `jeff_exchange_split.py`
  caused a NameError (`J` undefined). **Fix:** rewrote with a clean, documented
  Gamma5 triad G_yz = sym(Jx, Jy^2 - Jz^2) (cyclic).
