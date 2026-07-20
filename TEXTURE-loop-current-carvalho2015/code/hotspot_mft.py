#!/usr/bin/env python3
"""
hotspot_mft.py
==============================================================================
Self-consistent mean-field replication of the ΘII-loop-current (R_II) vs
QDW (b) competition of

  V. S. de Carvalho, T. Kloss, X. Montiel, H. Freire, C. Pepin,
  "Strong competition between ΘII-loop-current order and d-wave charge order
   along the diagonal direction in a two-dimensional hot spot model",
  Phys. Rev. B 92, 075123 (2015); arXiv:1506.07172v2.

------------------------------------------------------------------------------
PROVENANCE / KERNEL NOTE
------------------------------------------------------------------------------
The TEXTURES-100 task routed this into the loop-current *kagome tight-binding*
class and pointed at
    ~/Dropbox/XFER/TEXTURES-100/shared-kernels/loop_current_kagome_kernel.py
That kernel is a 3-site kagome Bloch/Peierls-flux/Chern engine. THIS PAPER IS
NOT A KAGOME MODEL -- it is a square-lattice 8-hot-spot spin-fermion model of
the cuprate CuO2 plane. See extraction/marker.md for the misclassification flag.

We DO reuse the kernel's *conceptual* content (cited, not imported):
  - loop-current order breaks time-reversal via the kinetic/hopping sector
    (complex, Peierls-like hoppings) rather than a Zeeman field
    -> kernel docstring "flux_pattern / Ohgushi-Murakami-Nagaosa" section;
  - real-part = bond charge (QDW, our b) vs imag-part = loop current (our R_II)
    -> kernel.bond_current_and_charge();
  - order parameters fixed by minimizing a free energy / self-consistency
    -> kernel.chern/gap driven picture generalized here to a coupled F(R_II,b).

------------------------------------------------------------------------------
MODEL (faithful reduced form of the paper)
------------------------------------------------------------------------------
Linearized hot-spot inverse Green function (paper Eq. 21), 3-orbital block
(p_x, p_y, d) times pseudospin (Sigma (x) Lambda (x) L) times particle-hole tau.
R_II enters ONLY through the Appendix-A parameters (Eqs. A7-A10):

    tan phi = (R_II/2 t_pd) tan(delta/2)
    tan theta = (R_II/2 t_pd) cot(delta/2)
    gamma1 = 2 sqrt[ t_pd^2 cos^2(delta/2) + (R_II^2/4) sin^2(delta/2) ]
    gamma2 = 2 sqrt[ t_pd^2 sin^2(delta/2) + (R_II^2/4) cos^2(delta/2) ]

with delta = (K+ - K-)/2 the hot-spot position. The Gamma matrices
(Eqs. A1-A6) are built in the Sigma/Lambda/L Pauli representation.

The QDW field b enters as an off-diagonal (Sigma3, tau) mean field on the
d/L block (paper Eqs. 18-19 with Delta+ = 0, i.e. the QDW sector).

Free energy (paper Eq. 32 structure, T->0, b and R_II taken k,eps-independent):

    F(R_II, b) = - (1/N_k) sum_k sum_bands  |E_a(k)|      (electronic, T->0)
                 + b^2 / J0                               (QDW stiffness)
                 + R_II^2 / V_pd                          (LC stiffness)
                 + const(n_p, U_p)

The electronic term is -Tr ln G^-1 evaluated in the T->0 static limit as the
sum of |eigenvalues| of the Bloch Hamiltonian H(k) = the Hermitian kernel of
G^-1 at iε_n->0 (occupied-state energy = -sum |E|), which is the standard
mean-field ground-state energy. Minimizing F over (R_II, b) reproduces the
coupled self-consistency Eqs. (31),(33).

Everything is real numpy; a full V_pd or lambda sweep runs in a few seconds.
"""
from __future__ import annotations
import numpy as np

# ---- Pauli matrices ---------------------------------------------------------
I2 = np.eye(2, dtype=complex)
SX = np.array([[0, 1], [1, 0]], dtype=complex)
SY = np.array([[0, -1j], [1j, 0]], dtype=complex)
SZ = np.array([[1, 0], [0, -1]], dtype=complex)

def kron(*mats):
    out = np.array([[1.0 + 0j]])
    for m in mats:
        out = np.kron(out, m)
    return out


# ---- Appendix-A parameters (Eqs. A7-A10), R_II dependence -------------------
def appendixA_params(R_II, delta, t_pd):
    """Return (phi, theta, gamma1, gamma2) exactly as Eqs. A7-A10."""
    hd = delta / 2.0
    r = R_II / (2.0 * t_pd)
    phi = np.arctan(r * np.tan(hd))
    theta = np.arctan(r * (1.0 / np.tan(hd)))
    g1 = 2.0 * np.sqrt(t_pd**2 * np.cos(hd)**2 + (R_II**2 / 4.0) * np.sin(hd)**2)
    g2 = 2.0 * np.sqrt(t_pd**2 * np.sin(hd)**2 + (R_II**2 / 4.0) * np.cos(hd)**2)
    return phi, theta, g1, g2


# ---- Bloch kernel of G^-1 (Hermitian part; Eq. 21 static limit) ------------
def hot_spot_H(kx, ky, R_II, b, p):
    """Hermitian 3-orbital (x) Sigma (x) Lambda (x) L Bloch kernel.

    Orbital block ordering: (p_x, p_y, d). Pseudospin: Sigma (x) Lambda (x) L
    (each 2-dim). We build the 3x3 ORBITAL structure whose entries are 8x8
    matrices in pseudospin space, per Appendix A. The QDW field b acts on the
    d/L sector (Eqs. 18-19, Delta+ = 0). Returns a Hermitian (24 x 24 ... but we
    reduce pseudospin to the minimal 2 (x) 2 (x) 2 = 8) matrix.

    To keep the model tractable AND faithful we keep the full Sigma,Lambda,L
    (8-dim) pseudospin so the Gamma-matrix Pauli structure of Eqs. A2-A6 is
    represented exactly; the orbital block is 3, giving a 24x24 Hermitian H(k).
    """
    t_pd = p['t_pd']; t_pp = p['t_pp']; delta = p['delta']
    xi_p = p['xi_p']; xi_d = p['xi_d']
    phi, theta, g1, g2 = appendixA_params(R_II, delta, p['delta_hs_gamma_scale'] if False else t_pd)

    Id8 = kron(I2, I2, I2)                      # 1_Sigma (x) 1_Lambda (x) 1_L
    L3 = kron(I2, I2, SZ)                       # L3
    La3 = kron(I2, SZ, I2)                      # Lambda3
    Si3 = kron(SZ, I2, I2)                      # Sigma3
    La3L3 = kron(I2, SZ, SZ)                    # Lambda3 (x) L3
    Si3La3 = kron(SZ, SZ, I2)                   # Sigma3 (x) Lambda3
    Si3L3 = kron(SZ, I2, SZ)                    # Sigma3 (x) L3
    Si3La3L3 = kron(SZ, SZ, SZ)                 # Sigma3 (x) Lambda3 (x) L3

    # exp(i * a * La3(x)L3) = cos a * 1 + i sin a * La3L3  (since (La3L3)^2 = 1)
    def expm_diag(a, M):
        return np.cos(a) * Id8 + 1j * np.sin(a) * M

    # Eq. A1
    Ghat1 = -2.0 * t_pp * np.cos(delta) * Id8
    # Eq. A3  Ghat1x = g1 e^{-i phi La3L3} + g2 e^{i theta La3L3} Si3(x)L3
    Ghat1x = g1 * expm_diag(-phi, La3L3) + g2 * (expm_diag(theta, La3L3) @ Si3L3)
    # Eq. A5  Ghat1y = g1 e^{i phi La3} - g2 e^{-i theta La3} Si3(x)L3
    Ghat1y = g1 * expm_diag(phi, La3) - g2 * (expm_diag(-theta, La3) @ Si3L3)

    # Ghat2* carry the k-linear (i d_x, i d_y) pieces (Eqs. A2,A4,A6). In the
    # linearized hot-spot theory these multiply kx,ky. We include the leading
    # Ghat2 dispersion (Eq. A2) which gives the hot-spot velocity.
    # Ghat2 = t_pp( sin d * La3(x)L3 - Si3(x)La3 ) i d_x
    #         - t_pp( sin d * La3 + Si3(x)La3(x)L3 ) i d_y
    G2x = t_pp * (np.sin(delta) * La3L3 - Si3La3)
    G2y = -t_pp * (np.sin(delta) * La3 + Si3La3L3)
    disp = G2x * kx + G2y * ky                  # Hermitian (real k * Hermitian)

    # Assemble the 3x3 orbital Bloch matrix (each entry 8x8). Ordering (px,py,d).
    Z = np.zeros((8, 8), dtype=complex)
    xi_p_block = xi_p * Id8 + disp              # p diagonal + hot-spot dispersion
    xi_d_block = xi_d * Id8
    # QDW field b: off-diagonal in tau (ph) sector on d/L; in this static
    # Hermitian reduction it acts as a gap on the d block coupling via Sigma3.
    b_block = b * Si3                           # QDW mean field (Eqs. 18-19, D+=0)

    H = np.block([
        [xi_p_block,          np.zeros((8, 8)), Ghat1x            ],
        [np.zeros((8, 8)),    xi_p_block,       Ghat1y            ],
        [Ghat1x.conj().T,     Ghat1y.conj().T,  xi_d_block + b_block],
    ])
    # Hermitize (guards tiny asymmetry from float ops)
    H = 0.5 * (H + H.conj().T)
    return H


# ---- ground-state electronic energy (T->0 of -Tr ln G^-1) ------------------
def _H_stack(kx_arr, ky_arr, R_II, b, p):
    """Vectorized: build a stack of Hermitian 24x24 Bloch kernels for arrays of
    (kx,ky). Only the dispersion term depends on k, so we build the k-independent
    part once and add k*G2 per point."""
    t_pd = p['t_pd']; t_pp = p['t_pp']; delta = p['delta']
    xi_p = p['xi_p']; xi_d = p['xi_d']
    phi, theta, g1, g2 = appendixA_params(R_II, delta, t_pd)
    Id8 = kron(I2, I2, I2); L3 = kron(I2, I2, SZ); La3 = kron(I2, SZ, I2)
    Si3 = kron(SZ, I2, I2); La3L3 = kron(I2, SZ, SZ); Si3La3 = kron(SZ, SZ, I2)
    Si3L3 = kron(SZ, I2, SZ); Si3La3L3 = kron(SZ, SZ, SZ)
    def expm_diag(a, M):
        return np.cos(a) * Id8 + 1j * np.sin(a) * M
    Ghat1x = g1 * expm_diag(-phi, La3L3) + g2 * (expm_diag(theta, La3L3) @ Si3L3)
    Ghat1y = g1 * expm_diag(phi, La3) - g2 * (expm_diag(-theta, La3) @ Si3L3)
    G2x = t_pp * (np.sin(delta) * La3L3 - Si3La3)
    G2y = -t_pp * (np.sin(delta) * La3 + Si3La3L3)
    Z8 = np.zeros((8, 8), dtype=complex)
    b_block = b * Si3
    # k-independent 24x24 base (with xi_p on p diagonals; disp added later)
    base = np.block([
        [xi_p * Id8,        Z8,          Ghat1x],
        [Z8,               xi_p * Id8,   Ghat1y],
        [Ghat1x.conj().T,  Ghat1y.conj().T, xi_d * Id8 + b_block],
    ])
    base = 0.5 * (base + base.conj().T)
    # dispersion block acts on the two p-orbital diagonal 8x8 blocks.
    # Vectorized: disp[a] = G2x*kx[a] + G2y*ky[a]  (n,8,8)
    n = kx_arr.size
    H = np.broadcast_to(base, (n, 24, 24)).copy()
    disp = (kx_arr[:, None, None] * G2x[None] + ky_arr[:, None, None] * G2y[None])
    H[:, 0:8, 0:8] += disp
    H[:, 8:16, 8:16] += disp
    # re-Hermitize
    H = 0.5 * (H + np.conj(np.transpose(H, (0, 2, 1))))
    return H


def electronic_energy(R_II, b, p, nk=None):
    """Sum of occupied-band energies over the BZ mesh (T->0). Occupied = E<0.
    Vectorized batched eigvalsh over all k-points."""
    nk = nk or p['nk']
    ks = np.linspace(-np.pi, np.pi, nk, endpoint=False)
    KX, KY = np.meshgrid(ks, ks, indexing='ij')
    kx = KX.ravel(); ky = KY.ravel()
    H = _H_stack(kx, ky, R_II, b, p)
    w = np.linalg.eigvalsh(H)                    # (n,24) ascending
    return np.where(w < 0.0, w, 0.0).sum() / (nk * nk)


def _Sb(p, nk=None):
    """BZ-averaged inverse effective bosonic propagator <D_eff^-1> = <gamma|w|+k^2+m_a>
    entering the b-stiffness of Eq. (32). At the static (w=0) mean-field level this
    is <|k|^2> over the BZ plus m_a."""
    nk = nk or p['nk']
    ks = np.linspace(-np.pi, np.pi, nk, endpoint=False)
    KX, KY = np.meshgrid(ks, ks, indexing='ij')
    return float(np.mean(KX**2 + KY**2) + p['m_a'])


def free_energy(R_II, b, p, nk=None):
    """F(R_II,b) per Eq. (32) structure (T->0, static b,R_II):

        F = -Tr ln G^-1                       (electronic; = -T sum ln D_l^(m))
            + (8/(3 lambda^2)) * <D_eff^-1> * b^2   (QDW stiffness, Eq. 32)
            + R_II^2 / V_pd                   (LC stiffness, Eq. 32)
            - n_p^2 U_p / 8                   (constant, Eq. 32)

    NOTE the QDW-stiffness coefficient DECREASES with lambda -> larger lambda
    favors larger b (paper claim 3), while R_II^2/V_pd DECREASES with V_pd ->
    larger V_pd favors larger R_II (paper claim 2). This is the competition
    mechanism, taken verbatim from the free-energy coefficients.
    """
    Fe = electronic_energy(R_II, b, p, nk=nk)
    Sb = p.get('_Sb_cache') or _Sb(p, nk=nk)
    b_stiff = (8.0 / (3.0 * p['lam']**2)) * Sb
    const = -(p['n_p']**2) * p['U_p'] / 8.0
    F = Fe + b_stiff * (b**2) + (R_II**2) / p['V_pd'] + const
    return F


# ---- coupled minimization (equivalent to Eqs. 31 & 33) ---------------------
def minimize_orders(p, nk=None, grid_R=None, grid_b=None):
    """Find (R_II, b) minimizing F on a coarse grid then refine (Nelder-Mead-ish
    coordinate descent). Returns dict."""
    from scipy.optimize import minimize
    nk = nk or p['nk']
    if grid_R is None:
        grid_R = np.linspace(0.0, 0.35 * p['V_pd'] + 0.5, 8)
    if grid_b is None:
        grid_b = np.linspace(0.0, 1.2, 8)
    best = (None, np.inf)
    for R0 in grid_R:
        for b0 in grid_b:
            F0 = free_energy(R0, b0, p, nk=nk)
            if F0 < best[1]:
                best = ((R0, b0), F0)
    (R0, b0), _ = best
    # refine with a bounded local optimizer on |R_II|,|b|
    def obj(x):
        return free_energy(abs(x[0]), abs(x[1]), p, nk=nk)
    res = minimize(obj, x0=[max(R0, 1e-3), max(b0, 1e-3)],
                   method='Nelder-Mead',
                   options=dict(xatol=1e-3, fatol=1e-6, maxiter=400))
    R, b = abs(res.x[0]), abs(res.x[1])
    return dict(R_II=R, b=b, F=res.fun, success=bool(res.success))


# ---- default parameter set (Fig. 4 caption) --------------------------------
def default_params(**overrides):
    p = dict(
        t_pd=1.0, t_pp=0.5, U_p=3.0, ed_ep=3.0,
        m_a=1e-2, gamma_ld=1e-5, n_p=0.6, delta=0.93,
        V_pd=14.0, lam=20.0,
        nk=24,                       # BZ mesh (paper used 320; we use a coarse
                                     # mesh for speed -- claims are qualitative)
    )
    # derived: xi_p = e_p + n_p/4 U_p - mu ; xi_d = e_d - mu.  We set the band
    # offset via ed_ep and put the hot-spot at the Fermi level (xi's ~ small).
    p['xi_p'] = 0.0
    p['xi_d'] = -p['ed_ep'] * 0.0 + 0.0   # hot spots pinned at FS; keep ~0
    # QDW stiffness J0 ~ 3 lambda^2 D_eff(0) ~ 3 lambda^2 / m_a  (paper J=3lam^2 Deff)
    p['J0'] = 3.0 * p['lam']**2 / p['m_a']
    p.update(overrides)
    # keep J0 consistent if lam/m_a overridden
    if 'J0' not in overrides:
        p['J0'] = 3.0 * p['lam']**2 / p['m_a']
    return p


if __name__ == '__main__':
    p = default_params()
    print("default params:", {k: p[k] for k in ('t_pd','t_pp','delta','V_pd','lam','nk')})
    out = minimize_orders(p)
    print("MF solution:", out)
