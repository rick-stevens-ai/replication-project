#!/usr/bin/env python3
"""
Minimal 4-band (8-band with spin) tight-binding model of MnF2 altermagnet.
Reproduces Bhowal & Spaldin, arXiv:2212.03756 (PRX 14, 011019 (2024)), Sec III.D.

Basis order (orbital block): {Mn1-dxz, Mn1-dyz, Mn2-dxz, Mn2-dyz}
Sigma = Pauli in sublattice space, sigma = Pauli in orbital space.
Full 8x8 adds spin: H = S0 (x) Ht + J Sz (x) (Sigma_z (x) sigma_0).
"""
import numpy as np

RY = 13.6056980659  # eV per Rydberg

# Table I (NMTO), Rydberg -> eV
t1 = 0.0036 * RY
t2 = -0.0038 * RY
t3 = 0.0040 * RY
t4 = 0.0034 * RY
e1 = -0.1385 * RY
e2 = -0.0339 * RY
J = 2.5  # eV  (2J ~ 5 eV exchange splitting)

# lattice constants (rutile MnF2, standard)
a = 4.8734  # Angstrom
c = 3.3099  # Angstrom

# --- Pauli matrices ---
s0 = np.eye(2)
sx = np.array([[0, 1], [1, 0]], dtype=complex)
sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
sz = np.array([[1, 0], [0, -1]], dtype=complex)


def alpha(kx, ky, kz):
    return e1 + 2 * t1 * np.cos(kz * c)


def beta(kx, ky, kz):
    return e2 + 2 * t2 * np.cos(kz * c)


def gamma(kx, ky, kz):
    return 8 * t3 * np.cos(kx * a / 2) * np.cos(ky * a / 2) * np.cos(kz * c / 2)


def delta(kx, ky, kz):
    return -8 * t4 * np.sin(kx * a / 2) * np.sin(ky * a / 2) * np.cos(kz * c / 2)


def Ht(kx, ky, kz):
    """4x4 orbital/sublattice Hamiltonian, Eq (2)."""
    al, be, ga, de = alpha(kx, ky, kz), beta(kx, ky, kz), gamma(kx, ky, kz), delta(kx, ky, kz)
    return (al * np.eye(4)
            + be * np.kron(sz, sx)      # Sigma_z (x) sigma_x
            + ga * np.kron(sx, s0)      # Sigma_x (x) sigma_0
            + de * np.kron(sx, sx))     # Sigma_x (x) sigma_x


def H_full(kx, ky, kz):
    """8x8 Hamiltonian with AFM exchange, Eq (5): H = S0 (x) Ht + J Sz (x)(Sigma_z (x) sigma_0)."""
    H = np.kron(s0, Ht(kx, ky, kz))
    exch = J * np.kron(sz, np.kron(sz, s0))  # Sz (x) (Sigma_z (x) sigma_0)
    return H + exch


def eig4_analytic(kx, ky, kz, shift_beta=0.0):
    """Eq (4) eigenvalues; shift_beta lets beta -> J+beta for the spin-polarized branch."""
    al = alpha(kx, ky, kz)
    be = beta(kx, ky, kz) + shift_beta
    ga = gamma(kx, ky, kz)
    de = delta(kx, ky, kz)
    r_p = np.sqrt(be**2 + (de + ga)**2)
    r_m = np.sqrt(be**2 + (de - ga)**2)
    # E±^- = al - r,  E±^+ = al + r
    return np.array([al - r_m, al - r_p, al + r_m, al + r_p])


def spin_split_eq6_exact(kx, ky, kz):
    """Eq (6) first line: exact expression with beta->J+beta."""
    be = beta(kx, ky, kz)
    ga = gamma(kx, ky, kz)
    de = delta(kx, ky, kz)
    Jb = J + be
    return np.sqrt(Jb**2 + (de - ga)**2) - np.sqrt(Jb**2 + (de + ga)**2)


def spin_split_eq6_approx(kx, ky, kz):
    """Eq (6) last equality: (32/eps) t3 t4 sin(kx a) sin(ky a), eps = J + e2 + 2 t2 (kz=0)."""
    eps = J + e2 + 2 * t2 * np.cos(kz * c)
    return (32.0 / eps) * t3 * t4 * np.sin(kx * a) * np.sin(ky * a)


def spin_split_full8(kx, ky, kz):
    """Spin splitting of top valence pair from full 8x8 diagonalization.
    Returns E_up - E_down of the two topmost VALENCE bands (below the gap)."""
    H = H_full(kx, ky, kz)
    w = np.linalg.eigvalsh(H)  # sorted ascending, 8 values
    # The 8 bands split into a lower (valence-like, alpha - r) manifold of 4
    # and an upper (alpha + r) manifold of 4. Top valence = highest of lower 4.
    lower = w[:4]
    # top two valence bands are the two largest of the lower manifold
    top2 = np.sort(lower)[-2:]
    return top2[1] - top2[0]


if __name__ == "__main__":
    print(f"Params (eV): t1={t1:.4f} t2={t2:.4f} t3={t3:.4f} t4={t4:.4f} "
          f"e1={e1:.4f} e2={e2:.4f} J={J}")
    # sample along Gamma->M ([110]) at kz=0
    kmax = np.pi / a
    for f in [0.1, 0.25, 0.5, 0.75, 1.0]:
        kx = ky = f * kmax
        print(f"f={f:.2f}  eq6_exact={spin_split_eq6_exact(kx,ky,0)*1000:8.3f} meV "
              f" eq6_approx={spin_split_eq6_approx(kx,ky,0)*1000:8.3f} meV "
              f" full8={spin_split_full8(kx,ky,0)*1000:8.3f} meV")
