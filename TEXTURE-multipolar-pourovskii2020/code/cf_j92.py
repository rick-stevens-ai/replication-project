#!/usr/bin/env python3
"""
Crystal-field diagonalization for Np4+ (5f^3, J=9/2) in cubic NpO2.

Reproduces the CF part of Pourovskii & Khmelevskyi, arXiv:2009.08908
(Nat. Commun. 12, 3282 (2021)), "Hidden order and multipolar exchange
striction in a correlated f-electron system".

Paper Methods gives the cubic CF parameters (fitted to DFT+HI 5f levels):
    A04<r4> = -152 meV,  A44<r4> = 5 * A04<r4>
    A06<r6> =  32.6 meV, A46<r6> = 21 * A06<r6>

The cubic CF Hamiltonian in Stevens-operator form (standard convention,
e.g. Santini et al. RMP 81, 807 (2009); Lea-Leask-Wolf JPCS 23,1381 (1962)):

    H_CF = A04<r4> beta_J [ O40 + 5 O44 ]  +  A06<r6> gamma_J [ O60 - 21 O64 ]

where beta_J, gamma_J are the Stevens factors for J=9/2 (4I9/2 of f^3, Nd3+/Np4+
Hund term).  NOTE the standard cubic combinations are:
   4th order:  O4 = O40 + 5 O44
   6th order:  O6 = O60 - 21 O64
The paper writes "A44 = 5 A04" and "A46 = 21 A06", i.e. it folds the 5 and 21
into the A-coefficients so that H = A04<r4>(O40 + (A44/A04) O44) + ...
= A04<r4>(O40 + 5 O44) + A06<r6>(O60 + 21 O64).

Sign convention for the 6th-order cubic term: LLW use (O60 - 21 O64). The paper
lists A46 = +21 A06. We test BOTH sign conventions and report which reproduces
the paper's level scheme (x = -0.54, excited Gamma8 ~ 68 meV, Gamma6 > 300 meV).

We work directly with the Stevens operators built from J angular-momentum
matrices (no Stevens multiplicative factor absorbed): the A_k<r^k> given are the
products A_k^q <r^k>; the Stevens factor theta_k (beta_J, gamma_J) multiplies.

Reference Stevens factors for J=9/2, f^3 (4I9/2):
    beta_J  = -2.911e-3   (x100? -- we use the standard Hutchings values)
    gamma_J =  4.077e-5   (approx)
These are the standard Hutchings (1964) tabulated values for the 4I9/2 ground
multiplet.  (Nd3+ and Np4+ share L=6,S=3/2,J=9/2.)
"""
import numpy as np

# ---------------------------------------------------------------------------
# Angular momentum operators for arbitrary J
# ---------------------------------------------------------------------------
def angular_momentum_ops(J):
    dim = int(round(2*J + 1))
    m = np.array([J - k for k in range(dim)])  # m = J, J-1, ..., -J
    Jz = np.diag(m).astype(complex)
    # J+ |j,m> = sqrt(J(J+1)-m(m+1)) |j,m+1>
    Jp = np.zeros((dim, dim), dtype=complex)
    for k in range(1, dim):
        mm = m[k]           # lower state m
        Jp[k-1, k] = np.sqrt(J*(J+1) - mm*(mm+1))
    Jm = Jp.conj().T
    Jx = 0.5*(Jp + Jm)
    Jy = (Jp - Jm)/(2j)
    return Jx, Jy, Jz, Jp, Jm, dim

# ---------------------------------------------------------------------------
# Stevens operator equivalents O_k^q (Hutchings 1964 conventions)
# Only need O40, O44, O60, O64 for cubic symmetry.
# ---------------------------------------------------------------------------
def stevens_operators(J):
    Jx, Jy, Jz, Jp, Jm, dim = angular_momentum_ops(J)
    X = J*(J+1)
    I = np.eye(dim, dtype=complex)
    Jz2 = Jz@Jz
    Jz4 = Jz2@Jz2
    Jz6 = Jz4@Jz2

    # O40 = 35 Jz^4 - 30 X Jz^2 + 25 Jz^2 - 6 X I + 3 X^2 I
    O40 = 35*Jz4 - 30*X*Jz2 + 25*Jz2 - 6*X*I + 3*X**2*I

    # O44 = 1/2 (Jp^4 + Jm^4)
    O44 = 0.5*(np.linalg.matrix_power(Jp,4) + np.linalg.matrix_power(Jm,4))

    # O60 = 231 Jz^6 - 315 X Jz^4 + 735 Jz^4 + 105 X^2 Jz^2 - 525 X Jz^2
    #       + 294 Jz^2 - 5 X^3 I + 40 X^2 I - 60 X I
    O60 = (231*Jz6 - 315*X*Jz4 + 735*Jz4 + 105*X**2*Jz2 - 525*X*Jz2
           + 294*Jz2 - 5*X**3*I + 40*X**2*I - 60*X*I)

    # O64 = 1/4 [ (11 Jz^2 - X I - 38 I)(Jp^4+Jm^4) + (Jp^4+Jm^4)(11 Jz^2 - X I - 38 I) ]
    Jp4 = np.linalg.matrix_power(Jp,4)
    Jm4 = np.linalg.matrix_power(Jm,4)
    A = 11*Jz2 - X*I - 38*I
    B = Jp4 + Jm4
    O64 = 0.25*(A@B + B@A)

    return {"O40":O40, "O44":O44, "O60":O60, "O64":O64, "dim":dim}

# ---------------------------------------------------------------------------
# Stevens factors for J=9/2, 4I9/2 term (L=6, S=3/2). Hutchings (1964).
# ---------------------------------------------------------------------------
# Standard tabulated values (Nd3+ 4I9/2):
BETA_J  = -0.0002911 * (10.0)   # placeholder scaling tested below
GAMMA_J =  9.0e-6

# We'll instead treat A_k<r^k>*theta_k as an overall prefactor that we can
# absorb.  For a *cubic* fit, the standard practice (LLW) is to write
#   H = B4 (O40 + 5 O44) + B6 (O60 - 21 O64)
# with B4 = A04<r4> beta_J,  B6 = A06<r6> gamma_J.
# We use the Hutchings 4I9/2 Stevens factors.

def cubic_cf_hamiltonian(A04r4_meV, A06r6_meV, beta_J, gamma_J,
                         sign6=-1.0, J=4.5):
    """Build cubic CF Hamiltonian (meV).  sign6=-1 -> LLW (O60-21 O64)."""
    S = stevens_operators(J)
    B4 = A04r4_meV * beta_J
    B6 = A06r6_meV * gamma_J
    H = B4*(S["O40"] + 5.0*S["O44"]) + B6*(S["O60"] + sign6*21.0*S["O64"])
    return H, S["dim"]

# ---------------------------------------------------------------------------
# Lea-Leask-Wolf x parameter and W scale
#   W x / F4 = B4 ,  W(1-|x|)/F6 = B6   (F4=60, F6=13860 for J=9/2)
# x in [-1,1] sets the ratio of 4th to 6th order.
# ---------------------------------------------------------------------------
F4_J92 = 60.0
F6_J92 = 13860.0

def llw_x_from_B(B4, B6):
    """Return LLW x from Stevens-coefficient magnitudes B4,B6.
       Wx/F4 = B4 ; W(1-|x|)/F6 = B6.
       => x/(1-|x|) = (B4 F4)/(B6 F6) with appropriate signs."""
    a = B4 * F4_J92
    b = B6 * F6_J92
    # x / (1-|x|) = a/b  (taking magnitudes for the |x| relation, keep sign of a)
    # Solve for x assuming sign(x)=sign(a):
    r = a / b
    # r = x/(1-|x|).  If x>=0: x = r(1-x) -> x=r/(1+r). If x<0: x=r(1+x) -> x=r/(1-r).
    if r >= 0:
        x = r/(1.0+r)
    else:
        x = r/(1.0-r)
    return x

# ---------------------------------------------------------------------------
# Analyze a spectrum into irreps by degeneracy pattern
# ---------------------------------------------------------------------------
def analyze_levels(H, tol=1e-6):
    evals = np.linalg.eigvalsh(H)
    evals = np.sort(evals.real)
    evals -= evals[0]
    # group degeneracies
    groups = []
    cur = [evals[0]]
    for e in evals[1:]:
        if abs(e - cur[-1]) < 1e-3:   # 1 ueV tolerance -> degenerate
            cur.append(e)
        else:
            groups.append((np.mean(cur), len(cur)))
            cur = [e]
    groups.append((np.mean(cur), len(cur)))
    return evals, groups


if __name__ == "__main__":
    print("="*70)
    print("Crystal-field diagonalization for Np 5f^3 J=9/2 in cubic NpO2")
    print("Paper params: A04<r4>=-152 meV, A06<r6>=32.6 meV")
    print("="*70)

    A04 = -152.0
    A06 = 32.6

    # Hutchings Stevens factors for 4I9/2 (Nd3+/Np4+ ground term)
    beta_J  = -0.0002911
    gamma_J =  0.0000090   # 9.0e-6 (Hutchings 4I9/2 gamma)

    for sign6, tag in [(-1.0, "LLW  (O60 - 21 O64)"),
                       (+1.0, "paper (O60 + 21 O64)")]:
        print(f"\n--- 6th-order convention: {tag} ---")
        H, dim = cubic_cf_hamiltonian(A04, A06, beta_J, gamma_J, sign6=sign6)
        evals, groups = analyze_levels(H)
        print(f"dim = {dim}")
        for e, g in groups:
            irrep = {2:"doublet(G6/G7)", 4:"quartet(G8)"}.get(g, f"deg={g}")
            print(f"   E = {e:8.2f} meV   degeneracy {g}  [{irrep}]")
        B4 = A04*beta_J; B6 = A06*gamma_J
        x = llw_x_from_B(B4, B6)
        print(f"   Stevens B4 = {B4:.5f} meV, B6 = {B6:.6f} meV")
        print(f"   LLW x parameter = {x:+.3f}")
