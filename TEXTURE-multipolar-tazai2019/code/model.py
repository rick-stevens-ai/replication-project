"""
model.py — 2D periodic Anderson model (PAM) for CeB6, Gamma8 quartet.
Replicates the tractable core of Tazai & Kontani, arXiv:1901.06213 (2019).

Basis ordering for the 4x4 f-block: index = (sigma, l) with
  sigma in {up=0, dn=1} (pseudospin), l in {1,2} (orbital).
Operators are written as sigma_a (x) tau_b Kronecker products (sigma acts on
pseudospin, tau acts on orbital). We use ordering |sigma>(x)|l>, i.e.
row/col index = 2*sigma + (l-1).
"""
import numpy as np

# ---------------- Pauli / identity 2x2 ----------------
s0 = np.array([[1, 0], [0, 1]], dtype=complex)
sx = np.array([[0, 1], [1, 0]], dtype=complex)
sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
sz = np.array([[1, 0], [0, -1]], dtype=complex)


def kron(a, b):
    return np.kron(a, b)


# ---------------- Band-structure parameters (SM Eq. S1) ----------------
T1, T2, T3, T4, T5 = -0.5, -0.889, 0.292, -0.229, 0.687
E0 = 1.33
# 2|t1_ss| = 1 energy unit -> |t1_ss|=0.5 -> consistent with t1=-0.5.

# s-f hybridization / on-site f level / filling controls
TSF = 0.78
EF = -2.0
MU = -2.45
TEMP = 0.01
A1 = np.sqrt(18.0 / 14.0)
A2 = np.sqrt(18.0 / 14.0)  # set equal to A1 (SM: escape 2D artifact)


def eps_c(kx, ky):
    """Conduction (s-electron) band dispersion, Eq. S1."""
    return (
        T1 * (np.cos(kx) + np.cos(ky))
        + T2 * (np.cos(kx + ky) + np.cos(kx - ky))
        + T3 * (np.cos(2 * kx) + np.cos(2 * ky))
        + T4 * (
            np.cos(2 * kx + ky) + np.cos(2 * kx - ky)
            + np.cos(2 * ky + kx) + np.cos(2 * ky - kx)
        )
        + T5 * (np.cos(2 * kx + 2 * ky) + np.cos(2 * kx - 2 * ky))
        + E0
    )


def hyb(kx, ky):
    """
    s-f hybridization matrix elements. Returns V (2x2 in [orbital l, spin sigma]-ish)
    We build the full Hamiltonian below; here return the four amplitudes.
    Main-text Eq.2:  V_{f l up} = -A_l tsf (sin ky + (-1)^l i sin kx)
    l=1 -> (-1)^1 = -1 ; l=2 -> +1  (matches SM S2: f1 has -i, f2 has +i).
    V_{f l dn} = -conj(V_{f l up}).
    """
    v1up = -A1 * TSF * (np.sin(ky) - 1j * np.sin(kx))   # l=1
    v2up = -A2 * TSF * (np.sin(ky) + 1j * np.sin(kx))   # l=2
    v1dn = -np.conj(v1up)
    v2dn = -np.conj(v2up)
    return v1up, v2up, v1dn, v2dn


def H_full(kx, ky):
    """
    Full single-particle Hamiltonian in basis
      [ c_up, c_dn, f_{up,1}, f_{up,2}, f_{dn,1}, f_{dn,2} ]  (6x6)
    Pseudospin conserved in hybridization (sigma=Sigma), so up/dn decouple in c-f mixing.
    """
    H = np.zeros((6, 6), dtype=complex)
    e = eps_c(kx, ky)
    # conduction diagonal (both spins)
    H[0, 0] = e
    H[1, 1] = e
    # f diagonal
    for i in range(2, 6):
        H[i, i] = EF
    v1up, v2up, v1dn, v2dn = hyb(kx, ky)
    # c_up couples to f_{up,1} (idx2), f_{up,2} (idx3)
    H[0, 2] = np.conj(v1up); H[2, 0] = v1up
    H[0, 3] = np.conj(v2up); H[3, 0] = v2up
    # c_dn couples to f_{dn,1} (idx4), f_{dn,2} (idx5)
    H[1, 4] = np.conj(v1dn); H[4, 1] = v1dn
    H[1, 5] = np.conj(v2dn); H[5, 1] = v2dn
    return H


# ---------------- Multipole operators (SM Eqs. S5, S6) ----------------
# 4x4 f-block in ordering index = 2*sigma + (l-1), i.e. sigma (x) tau.
def _op(sigma, tau):
    return kron(sigma, tau)


def raw_multipoles():
    """Un-normalized 4x4 multipole matrices, keyed by name. IR labels attached."""
    ops = {}
    # Electric (even rank)
    ops["1"]    = ("Ga1+", _op(s0, s0))
    ops["O20"]  = ("Ga3+", 4.0 * _op(s0, sz))
    ops["O22"]  = ("Ga3+", 4.0 * _op(s0, sx))
    ops["Oxy"]  = ("Ga4+", -_op(sz, sy))
    ops["Oyz"]  = ("Ga5+", -_op(sx, sy))
    ops["Ozx"]  = ("Ga5+", -_op(sy, sy))
    # Magnetic (odd rank)
    ops["Jz"]   = ("Ga2-", _op(sz, -1.2 * s0 - 0.67 * sz))
    ops["Tza"]  = ("Ga2-", _op(sz, -1.0 * s0 - 7.0 * sz))
    ops["Txyz"] = ("Ga3-", -10.0 * _op(s0, sy))
    ops["Tzb"]  = ("Ga4-", -6.7 * _op(sz, sx))
    ops["Jx"]   = ("Ga5-", _op(sx, 1.2 * s0 - 0.34 * sz + 0.58 * sx))
    ops["Jy"]   = ("Ga5-", _op(sy, 1.2 * s0 - 0.34 * sz - 0.58 * sx))
    ops["Txa"]  = ("Ga5-", _op(sx, s0 - 3.5 * sz + 6.1 * sx))
    ops["Tya"]  = ("Ga5-", _op(sy, s0 + 3.5 * sz + 6.1 * sx))
    ops["Txb"]  = ("Ga5-", _op(sx, -5.8 * sz - 3.4 * sx))
    ops["Tyb"]  = ("Ga5-", _op(sy, -5.8 * sz + 3.4 * sx))
    return ops


def normalized_multipoles():
    """Return dict name -> (IR, normalized 4x4 matrix) with sum|Q_LM|^2 = 1 (S7)."""
    out = {}
    for name, (ir, M) in raw_multipoles().items():
        nrm = np.sqrt(np.sum(np.abs(M) ** 2))
        out[name] = (ir, M / nrm)
    return out


# 16 basis operators list (the operator set spanning 4x4 Hermitian space)
MULTIPOLE_NAMES = [
    "1", "O20", "O22", "Oxy", "Oyz", "Ozx",
    "Jz", "Tza", "Txyz", "Tzb", "Jx", "Jy", "Txa", "Tya", "Txb", "Tyb",
]

if __name__ == "__main__":
    # sanity: dims + hermiticity + orthonormal count
    ops = normalized_multipoles()
    print("n operators:", len(ops))
    for n, (ir, M) in ops.items():
        herm = np.allclose(M, M.conj().T)
        print(f"{n:5s} IR={ir:5s} herm={herm} tr={np.trace(M).real:+.3f} "
              f"norm={np.sqrt(np.sum(np.abs(M)**2)):.3f}")
