"""
Minimal tractable replication of the tight-binding (TB) model and symmetry
analysis in:

  S. Bhowal & N. A. Spaldin, "Magnetic octupoles as the order parameter for
  unconventional antiferromagnetism", arXiv:2212.03756 (v1, Dec 2022);
  earlier arXiv version 2205.09500; published Phys. Rev. X (2024).

System: rutile MnF2, a prototypical NON-RELATIVISTIC-SPIN-SPLIT (altermagnetic)
antiferromagnet.  Space group P4_2/mnm; two inequivalent-environment Mn sites
with antiparallel spins along [001].

We implement (NOT the DFT / Elk multipole machinery, which is out of scope), the
tractable *minimal four-band + spin (eight-band) tight-binding model* given in
Eqs. (2)-(6) and Table I of the paper, plus the reciprocal-space symmetry
representation of the O32- magnetic octupole (kx ky mz).

All model parameters are taken verbatim from the paper (Table I, Appendix B):
    d-d hoppings (Ry):  t1=0.0036, t2=-0.0038, t3=0.0040, t4=0.0034
    onsite (Ry):        e1=-0.1385, e2=-0.0339
    exchange:           2J ~ 5 eV  =>  J ~ 2.5 eV
Lattice constants of rutile MnF2 (a=c not needed numerically because the model
uses reduced coordinates kx a, ky a, kz c; we set a=c=1 and work in units of
(pi/a) along the path, which is exactly how the analytic k-dependence enters).

Ry -> eV conversion: 1 Ry = 13.605693 eV.
"""

import numpy as np

RY_TO_EV = 13.605693122994

# --- Table I / Appendix B parameters (verbatim, in Rydberg) --------------------
T1 = 0.0036
T2 = -0.0038
T3 = 0.0040
T4 = 0.0034
E1 = -0.1385
E2 = -0.0339

# 2J ~ 5 eV  ->  J ~ 2.5 eV.  Convert to Ry so all terms are consistent.
TWO_J_EV = 5.0
J_RY = (TWO_J_EV / 2.0) / RY_TO_EV   # J in Ry

# Pauli matrices
s0 = np.eye(2)
sx = np.array([[0, 1], [1, 0]], dtype=complex)
sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
sz = np.array([[1, 0], [0, -1]], dtype=complex)


def abgd(kx, ky, kz, a=1.0, c=1.0,
         t1=T1, t2=T2, t3=T3, t4=T4, e1=E1, e2=E2):
    """alpha,beta,gamma,delta(k) -- Eq. (3).  k in absolute units (1/length)."""
    alpha = e1 + 2 * t1 * np.cos(kz * c)
    beta = e2 + 2 * t2 * np.cos(kz * c)
    gamma = 8 * t3 * np.cos(kx * a / 2) * np.cos(ky * a / 2) * np.cos(kz * c / 2)
    delta = -8 * t4 * np.sin(kx * a / 2) * np.sin(ky * a / 2) * np.cos(kz * c / 2)
    return alpha, beta, gamma, delta


def H_orbital(kx, ky, kz, **kw):
    """Four-band spinless Hamiltonian, Eq. (2):
        Ht = alpha*I + beta*(Sz x sx) + gamma*(Sx x s0) + delta*(Sx x sx)
    Basis order {Mn1-dxz, Mn1-dyz, Mn2-dxz, Mn2-dyz}.
    Sigma = sublattice Pauli, sigma = orbital Pauli."""
    a, b, g, d = abgd(kx, ky, kz, **kw)
    I4 = np.eye(4, dtype=complex)
    Ht = (a * I4
          + b * np.kron(sz, sx)   # Sigma_z x sigma_x
          + g * np.kron(sx, s0)   # Sigma_x x sigma_0
          + d * np.kron(sx, sx))  # Sigma_x x sigma_x
    return Ht


def eig_orbital(kx, ky, kz, **kw):
    """Analytic four eigenvalues, Eq. (4):
        E-_pm = alpha - sqrt(beta^2 + (delta +/- gamma)^2)
        E+_pm = alpha + sqrt(beta^2 + (delta +/- gamma)^2)
    Returned sorted ascending, plus the raw labelled set."""
    a, b, g, d = abgd(kx, ky, kz, **kw)
    root_p = np.sqrt(b**2 + (d + g)**2)
    root_m = np.sqrt(b**2 + (d - g)**2)
    Em_plus = a - root_m   # E-_+  (uses delta - gamma? paper writes (delta +/- gamma))
    Em_minus = a - root_p
    Ep_plus = a + root_m
    Ep_minus = a + root_p
    vals = np.array([Em_minus, Em_plus, Ep_minus, Ep_plus])
    return np.sort(vals), dict(Em_plus=Em_plus, Em_minus=Em_minus,
                               Ep_plus=Ep_plus, Ep_minus=Ep_minus)


def H_full(kx, ky, kz, J=J_RY, **kw):
    """Full 8-band spinful Hamiltonian, Eq. (5):
        H = s0 x Ht + J * (Sspin_z x (Sigma_z x sigma_0))
    Basis: spin (up,down) outer, then sublattice, then orbital."""
    Ht = H_orbital(kx, ky, kz, **kw)
    Sspin_z = sz  # spin Pauli
    exch = J * np.kron(Sspin_z, np.kron(sz, s0))   # 8x8
    H = np.kron(s0, Ht) + exch
    return H


def spin_projected_bands(kx, ky, kz, J=J_RY, **kw):
    """Diagonalise H_full and return (energies, <Sz> per eigenstate).

    The exchange term is diagonal in spin AND commutes with Ht's spin structure
    (Ht is spin-independent), so eigenstates are pure spin.  We compute <Sz>
    as +/-1 to label up/down bands."""
    H = H_full(kx, ky, kz, J=J, **kw)
    w, v = np.linalg.eigh(H)
    Sz_op = np.kron(sz, np.eye(4))
    sz_exp = np.real(np.einsum('ij,ji->i', v.conj().T @ Sz_op, v))
    return w, sz_exp


def spin_splitting_topvalence(kx, ky, kz, J=J_RY, **kw):
    """Delta E_s for the top pair of spin-polarised valence bands.

    Following Eq. (6): eigenvalues are those of E-_pm with beta -> J+beta for the
    spin channel.  The top valence spin-split pair is
        E_up  = alpha - sqrt((J+beta)^2 + (delta - gamma)^2)   [Mn sublattice up]
        E_dn  = alpha - sqrt((J+beta)^2 + (delta + gamma)^2)
    (up/down assignment fixed by sign convention; we return E_up - E_dn.)"""
    a, b, g, d = abgd(kx, ky, kz, **kw)
    bj = J + b
    E_up = a - np.sqrt(bj**2 + (d - g)**2)
    E_dn = a - np.sqrt(bj**2 + (d + g)**2)
    return E_up - E_dn


def spin_splitting_approx(kx, ky, kz, J=J_RY, **kw):
    """Analytic approximation Eq. (6):
        Delta E_s ~ (32/eps) * t3 * t4 * sin(kx a) * sin(ky a)
    with eps = J + beta ~ J + e2 + 2 t2 (kz=0 plane), a=1 in our reduced units."""
    t3 = kw.get('t3', T3); t4 = kw.get('t4', T4)
    e2 = kw.get('e2', E2); t2 = kw.get('t2', T2)
    a = kw.get('a', 1.0)
    eps = J + e2 + 2 * t2                      # kz=0 => cos(0)=1
    return (32.0 / eps) * t3 * t4 * np.sin(kx * a) * np.sin(ky * a)


# --- Reciprocal-space octupole representation ---------------------------------
def octupole_O32_recip(kx, ky, mz=1.0):
    """Reciprocal-space representation of the ferro-type O32- magnetic octupole,
    xy*mz -> kx*ky*mz.  This is the paper's central symmetry claim linking the
    octupole to the NRSS."""
    return kx * ky * mz


if __name__ == "__main__":
    # quick self-test
    kx = ky = 0.3
    print("orbital eig:", eig_orbital(kx, ky, 0.0)[0] * RY_TO_EV)
    print("dEs exact (eV):", spin_splitting_topvalence(kx, ky, 0.0) * RY_TO_EV)
    print("dEs approx(eV):", spin_splitting_approx(kx, ky, 0.0) * RY_TO_EV)
