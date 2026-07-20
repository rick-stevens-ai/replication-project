# Extraction marker — arXiv:1705.06289

**Paper:** S. Chatterjee, S. Sachdev, M. S. Scheurer,
"Intertwining topological order and broken symmetry in a theory of
fluctuating spin density waves", Phys. Rev. Lett. (v3, 26 Sep 2017).

**Extraction method:** `pdftotext -layout paper.pdf paper.txt` (poppler,
`/usr/local/bin/pdftotext`). PDF native text layer present — clean extraction,
974 lines. No OCR needed. Vision/PDF-model route NOT used (text layer sufficient
and avoids credit-blocked routes).

## What the paper is about (scope)

The paper is a **SU(2) gauge theory of quantum fluctuations of spin-density-wave
(SDW) states** in the pseudogap phase of hole-doped cuprates on the **square
lattice**. Its central technical claim: quantum fluctuations of the magnetically
ordered SDW states (Néel D0, canted A0, planar spiral B0, conical spiral C0)
produce metallic states with an antinodal gap AND Z2/U(1) topological order that
"intertwines" with the observed broken discrete symmetries — including
**current-loop (loop-current) order** (phase C, Varma-type), Ising-nematic order
(phase B), and VBS (phase D).

The "loop-current" content is: (i) phase C carries broken time-reversal + mirror
(but not their product) → current-loop order (Table I / Table II symmetry
analysis); (ii) Appendix C computes bond kinetic energies K_ij and bond currents
J_ij from the effective chargon Hamiltonian (Eq. C14) and shows which Higgs
configurations support finite loop currents.

## Machine-checkable core (what CAN be reproduced with real code)

The paper is theoretical and has **no numeric tables of observables** to hit
directly. The two computationally concrete, checkable pieces are:

1. **Appendix B — square-lattice Hubbard SDW mean-field theory** (Eqs. B3–B6).
   A 2×2 mean-field Hamiltonian h_k couples (c_{k,up}, c_{k+K,down}) via the
   SDW field h = 2 U N0 and canting angle θ. Diagonalization gives the two
   Hubbard bands E_{k,±} (Eq. B6). Minimizing the mean-field free energy over
   (h, θ, K) at fixed filling n selects the magnetic phase (Néel/spiral/
   canted/conical/FM). This reproduces Fig. 2d–f / Fig. 3.

2. **Appendix C — bond kinetic energy & loop current** (Eq. C14):
   K_ij = -2 Re T_ij, J_ij = 2 Im T_ij, with T_ij = Z_ij t_ij <psi_i^dag psi_j>.
   Loop currents are the *imaginary* part of the bond bilinear — the same
   real=charge / imag=current decomposition used in the shared kagome kernel.

## Concrete claims selected for replication (see code/report)

- C1: The Bloch dispersion ξ_k = -Σ_p t_p (neighbor sum) - μ; 2-band SDW
  spectrum E_{k,±} (Eq. B6) is correctly reproduced; at K=(π,π), θ=0 (Néel)
  a gap of magnitude h opens at the AFM zone boundary (ξ_k = ξ_{k+K}).
- C2: The Néel insulator (n=1) is the ground state at large U (paper: "in the
  insulator (n=1) ... we find the insulator to be always in the Néel phase D0").
- C3: Self-consistent gap equation h = 2 U N0 with N0 = <S> from filled bands
  has the standard Hubbard-SDW mean-field behavior: nonzero solution above a
  U_c, with h growing ~ linearly at large U (insulator: full moment).
- C4: Hole-doping (n<1) with 2nd/3rd/4th-neighbor hopping (particle-hole
  breaking) drives incommensurate spiral order K away from (π,π) — the D0→B0
  transition (ρ_s → negative, Appendix A) — while electron-doping stays coplanar.
- C5: Loop-current diagnostic (Eq. C14): a COLLINEAR Higgs/SDW configuration
  gives zero bond current (Im T_ij = 0); TRS breaking / finite loop current
  requires a NON-COLLINEAR (canted/conical, θ≠0, incommensurate) configuration
  — the paper's statement "time-reversal-symmetry breaking necessarily requires
  a non-collinear Higgs phase".

## Key equations (verbatim locations)

- Eq. (B4): mean-field h_k (2×2), ξ_k = -Σ_j t_ij e^{ik·(r_i-r_j)} - μ, h=2U N0.
- Eq. (B5): tan(2φ_k) = h cosθ / (ξ_k - ξ_{k+K} - h sinθ).
- Eq. (B6): E_{k,s} = ½[ξ_k+ξ_{k+K} + s√((ξ_k-ξ_{k+K}-h sinθ)² + h²cos²θ)].
- Free energy: E_MF/Ns = Σ_s ∫ E_{k,s} n_F - U n²/4 + h²/(4U); n from ∫ n_F.
- Eq. (C14): K_ij = -2 Re T_ij, J_ij = 2 Im T_ij, T_ij = Z_ij t_ij <ψ_i^† ψ_j>.

## Kernel scope note

The provided shared kernel `loop_current_kagome_kernel.py` is a **kagome-lattice
Peierls-flux tight-binding** kernel (Fernandes et al. 2025). This paper is a
**square-lattice SDW mean-field / SU(2) gauge theory**. The kagome geometry does
NOT apply. What IS reused: (a) the real=charge / imag=current bond-bilinear
decomposition (`bond_current_and_charge`), directly transplanted to the square
lattice for the Eq.-C14 loop-current diagnostic; (b) the general
tight-binding + eigendecomposition-on-a-BZ-grid machinery. See PROVENANCE.md.
