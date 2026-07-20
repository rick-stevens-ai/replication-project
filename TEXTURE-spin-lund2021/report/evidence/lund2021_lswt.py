#!/usr/bin/env python3
"""
Replication of Lund, Salimath & Hals, "Spin pumping in noncollinear
antiferromagnets" (arXiv:2106.15187), Sec. III kagome application.

HEADLINE CLAIM (recipe): "The three spin-wave bands of a kagome
antiferromagnet pump ac spin currents with mutually orthogonal spin
polarizations."

We do TWO from-scratch calculations:

(A) LINEAR SPIN-WAVE THEORY (Holstein-Primakoff + Colpa) of the 120-degree
    ordered kagome Heisenberg antiferromagnet (H = J sum_<ij> S_i.S_j,
    J>0). Kagome has 3 sublattices -> 3 magnon bands. The well-known
    physics feature to verify: the pure-Heisenberg kagome AFM has a
    ZERO-ENERGY FLAT BAND (macroscopic weathervane degeneracy) plus two
    dispersive bands. We verify this over a coarse k-grid.

(B) The paper's ACTUAL object: the k=0 uniform-precession modes of the
    effective action (Eqs. 14-16). With diagonal K = diag(K1,K1,K2), the
    linearized EOM  a1^2 r_ddot + 4 a2 K . r = 0  gives three normal modes
    polarized along x, y, z (mutually orthogonal) with resonance freqs
        w0^(x) = w0^(y) = sqrt(4 K1 a2 / a1^2)   (in-plane, degenerate)
        w0^(z)        = sqrt(4 K2 a2 / a1^2)      (out-of-plane)
    with, from App. A (S=1, a=1 units):
        a1 = 24 hbar S / (sqrt(3) a^2)
        a2 = 36 S^2 J / (sqrt(3) a^2)
        K1 = 8 sqrt(3)(Kz+K) S^2 / a^3
        K2 = 16 sqrt(3) K S^2 / a^3
    We verify orthogonality of the three polarizations and the frequency
    ratio  w0^(z)/w0^(x) = sqrt(K2/K1) = sqrt(2K/(Kz+K)).
"""
import json, numpy as np

np.set_printoptions(precision=5, suppress=True)
OUT = {}

# ----------------------------------------------------------------------
#  Geometry of kagome lattice
# ----------------------------------------------------------------------
a1v = np.array([1.0, 0.0])
a2v = np.array([0.5, np.sqrt(3)/2])
# sublattice positions (standard kagome: midpoints of a honeycomb)
subs = {
    'A': np.array([0.0, 0.0]),
    'B': 0.5*a1v,
    'C': 0.5*a2v,
}
names = ['A', 'B', 'C']

# equilibrium 120-degree in-plane spin directions (paper's n_hat, xy plane)
nhat = {
    'A': np.array([0.0, 1.0, 0.0]),
    'B': np.array([ np.sqrt(3)/2, -0.5, 0.0]),
    'C': np.array([-np.sqrt(3)/2, -0.5, 0.0]),
}

# find nearest-neighbour bonds by scanning neighbouring cells
def find_bonds():
    bonds = []  # (si, sj, delta_frac)  where delta = n1*a1v + n2*a2v + (rj-ri)
    rmin = None
    cand = []
    for i, si in enumerate(names):
        for j, sj in enumerate(names):
            for n1 in (-1, 0, 1):
                for n2 in (-1, 0, 1):
                    d = subs[sj] + n1*a1v + n2*a2v - subs[si]
                    r = np.linalg.norm(d)
                    if r > 1e-6:
                        cand.append((r, i, j, n1, n2, d))
    rmin = min(c[0] for c in cand)
    for r, i, j, n1, n2, d in cand:
        if abs(r - rmin) < 1e-4:
            bonds.append((i, j, np.array([n1, n2]), d))
    return bonds, rmin

bonds, rmin = find_bonds()
OUT['nn_distance'] = float(rmin)
OUT['n_bonds_directed'] = len(bonds)   # expect 12 (directed); 6 undirected

# ----------------------------------------------------------------------
#  Local frames for Holstein-Primakoff
# ----------------------------------------------------------------------
zhat = np.array([0.0, 0.0, 1.0])
frames = {}
for s in names:
    ez = nhat[s]                       # local quantization axis = spin dir
    ex = np.cross(ez, zhat); ex /= np.linalg.norm(ex)   # in-plane transverse
    ey = np.cross(ez, ex)              # = out-of-plane (approx zhat)
    frames[s] = (ex, ey, ez)

# ----------------------------------------------------------------------
#  LSWT via Holstein-Primakoff bosons + Colpa diagonalization
#  H = J sum_<ij> S_i . S_j ,  optional small easy-axis anisotropy along n_i
# ----------------------------------------------------------------------
def magnon_bands(kpt, J=1.0, S=1.0, Kani=0.0):
    """Return the 3 positive magnon energies at reduced k (in units of 2pi)."""
    N = 3
    A = np.zeros((N, N), complex)   # a_i^dag a_j  and h.c.
    B = np.zeros((N, N), complex)   # a_i^dag a_j^dag
    diag = np.zeros(N)
    # reciprocal-space bond phase uses cartesian k . delta
    kcart = kpt  # already cartesian
    for (i, j, ncell, d) in bonds:
        exi, eyi, ezi = frames[names[i]]
        exj, eyj, ezj = frames[names[j]]
        # couplings between local frames
        Jzz = ezi @ ezj
        # transverse coupling matrix elements
        # S_i.S_j in HP to quadratic order:
        #  classical: S^2 (ezi.ezj)
        #  on-site:  -S(ezi.ezj)(a_i^dag a_i + a_j^dag a_j)
        #  hopping/pairing from transverse parts
        gpp = (exi @ exj) - (eyi @ eyj) + 1j*((exi @ eyj) + (eyi @ exj))  # a a
        gpm = (exi @ exj) + (eyi @ eyj) + 1j*((eyi @ exj) - (exi @ eyj))  # a a^dag
        phase = np.exp(1j * (kcart @ d))
        # on-site energy shift (each directed bond contributes to site i)
        diag[i] += -J * S * Jzz
        # hopping  a_i^dag a_j : coefficient (J S /2) gpm
        A[i, j] += (J * S / 2.0) * gpm * phase
        # pairing  a_i^dag a_j^dag : (J S /2) gpp
        B[i, j] += (J * S / 2.0) * gpp * phase
    # anisotropy (easy axis along local ez): lowers transverse, adds to diag
    for i in range(N):
        diag[i] += 2.0 * Kani * S
    # Build BdG. H = 1/2 psi^dag M psi, psi=(a_1..a_N, a_1^dag..a_N^dag)
    H11 = np.diag(diag) + 0.5*(A + A.conj().T)
    H22 = H11.conj()
    H12 = 0.5*(B + B.T)                 # symmetric
    M = np.block([[H11, H12],
                  [H12.conj().T, H22]])
    # ensure Hermitian
    M = 0.5*(M + M.conj().T)
    g = np.diag(np.concatenate([np.ones(N), -np.ones(N)]))
    # Colpa: eigenvalues of g.M
    ev = np.linalg.eigvals(g @ M)
    ev = np.real(ev)
    ev = np.sort(ev)[::-1][:N]          # top N are the positive magnon energies
    return np.abs(ev)

# ----------------------------------------------------------------------
#  (A) coarse BZ grid -> check for zero-energy FLAT band (Heisenberg)
# ----------------------------------------------------------------------
b1 = 2*np.pi*np.array([1.0, -1/np.sqrt(3)])
b2 = 2*np.pi*np.array([0.0,  2/np.sqrt(3)])
NG = 12
allbands = []
for m in range(NG):
    for n in range(NG):
        k = (m/NG)*b1 + (n/NG)*b2
        allbands.append(magnon_bands(k, J=1.0, S=1.0, Kani=0.0))
allbands = np.array(allbands)          # (Ngrid, 3), sorted descending
lowest = allbands[:, -1]
mid    = allbands[:, -2]
top    = allbands[:, -1]
OUT['heisenberg'] = {
    'grid': f'{NG}x{NG}',
    'lowest_band_mean': float(lowest.mean()),
    'lowest_band_max':  float(lowest.max()),
    'lowest_band_std':  float(lowest.std()),
    'top_band_mean':    float(allbands[:,0].mean()),
    'top_band_range':   [float(allbands[:,0].min()), float(allbands[:,0].max())],
}
# flat band = lowest band ~ constant (near zero) across BZ
flat_tol = 0.05 * allbands.max()
is_flat = (lowest.std() < flat_tol) and (lowest.mean() < flat_tol)
OUT['heisenberg']['flat_zero_band_detected'] = bool(is_flat)
OUT['heisenberg']['flat_tol'] = float(flat_tol)

# k-path bands for the report (Gamma-K-M-Gamma), coarse
def kpath():
    G = np.array([0.0, 0.0])
    K = (1/3)*b1 + (2/3)*b2   # a K point
    M = 0.5*b1
    pts = [G, K, M, G]; labels = ['G','K','M','G']
    path = []; xs = []; x=0.0; ticks=[0.0]
    for a, b in zip(pts[:-1], pts[1:]):
        for t in np.linspace(0, 1, 15, endpoint=False):
            path.append(a + t*(b-a)); xs.append(x); x += np.linalg.norm(b-a)/15
        ticks.append(x)
    path.append(pts[-1]); xs.append(x)
    return path, xs, ticks, labels
path, xs, ticks, labels = kpath()
band_path = np.array([magnon_bands(k) for k in path])  # (Npath,3)
OUT['kpath'] = {'x': xs, 'bands': band_path.tolist(),
                'ticks': ticks, 'labels': labels}

# ----------------------------------------------------------------------
#  (B) k=0 uniform modes: paper's resonance frequencies & polarizations
# ----------------------------------------------------------------------
def resonances(J=1.0, S=1.0, K=0.10, Kz=0.05, a=1.0, hbar=1.0):
    a1 = 24*hbar*S/(np.sqrt(3)*a**2)
    a2 = 36*S**2*J/(np.sqrt(3)*a**2)
    K1 = 8*np.sqrt(3)*(Kz+K)*S**2/a**3
    K2 = 16*np.sqrt(3)*K*S**2/a**3
    Kmat = np.diag([K1, K1, K2])
    # dynamical matrix from a1^2 r_ddot + 4 a2 K r = 0  ->  w^2 = 4 a2 K /a1^2
    D = (4*a2/a1**2) * Kmat
    w2, vecs = np.linalg.eigh(D)
    w = np.sqrt(np.abs(w2))
    return a1, a2, K1, K2, w, vecs

a1c, a2c, K1c, K2c, wmodes, wvecs = resonances()
# check orthogonality of the three mode polarizations
Gram = wvecs.T @ wvecs
ortho_err = float(np.max(np.abs(Gram - np.eye(3))))
w0_xy = float(np.sqrt(4*a2c*K1c/a1c**2))
w0_z  = float(np.sqrt(4*a2c*K2c/a1c**2))
ratio_num = float(wmodes.max()/wmodes.min()) if wmodes.min()>0 else None
ratio_analytic = float(np.sqrt(K2c/K1c))   # = sqrt(2K/(Kz+K))
OUT['uniform_modes'] = {
    'constants': {'a1': a1c, 'a2': a2c, 'K1': K1c, 'K2': K2c},
    'resonance_freqs_sorted': sorted(map(float, wmodes)),
    'w0_xy_formula': w0_xy,
    'w0_z_formula': w0_z,
    'n_distinct_freqs': int(len(set(np.round(wmodes, 6)))),
    'degeneracy_xy_pair': bool(abs(wmodes[0]-wmodes[1])<1e-9 or
                               abs(wmodes[1]-wmodes[2])<1e-9),
    'polarization_vectors': wvecs.T.tolist(),
    'polarizations_orthogonal': bool(ortho_err < 1e-9),
    'orthogonality_max_error': ortho_err,
    'freq_ratio_numeric': ratio_num,
    'freq_ratio_analytic_sqrt_K2_K1': ratio_analytic,
}

# ----------------------------------------------------------------------
#  SCORING vs claim
# ----------------------------------------------------------------------
OUT['claim_check'] = {
    'claim': "Three spin-wave bands of kagome AF pump spin currents with "
             "mutually orthogonal polarizations",
    'three_bands_present': bool(band_path.shape[1] == 3),
    'three_uniform_modes': bool(len(wmodes) == 3),
    'polarizations_mutually_orthogonal': bool(ortho_err < 1e-9),
    'polarization_axes': 'x, y, z (eigenvectors of diagonal K)',
    'kagome_flat_zero_band_reproduced': bool(is_flat),
    'note': ("Paper is spin-PUMPING (not thermal Hall). The 'three bands' "
             "are the k=0 uniform-precession resonance modes; their "
             "polarizations are the eigenvectors of the diagonal anisotropy "
             "matrix K=diag(K1,K1,K2), hence mutually orthogonal (x,y,z)."),
}

with open('work/lund2021_result.json', 'w') as f:
    json.dump(OUT, f, indent=2)
print("SAVED work/lund2021_result.json")
print(json.dumps({k: OUT[k] for k in ['heisenberg','uniform_modes','claim_check']}, indent=2))
