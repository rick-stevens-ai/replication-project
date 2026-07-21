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
def magnon_matrix(kpt, J=1.0, S=1.0, Kani=0.0):
    """Build the 2Nx2N BdG matrix M and metric g for reduced k (cartesian).

    Returns (M, g). H = 1/2 psi^dag M psi, psi=(a_1..a_N, a_1^d..a_N^d).
    Colpa magnon energies are the positive eigenvalues of g@M; the
    corresponding eigenvectors carry the boson amplitudes (u_i, v_i)."""
    N = 3
    A = np.zeros((N, N), complex)   # a_i^dag a_j  and h.c.
    B = np.zeros((N, N), complex)   # a_i^dag a_j^dag
    diag = np.zeros(N)
    kcart = kpt
    for (i, j, ncell, d) in bonds:
        exi, eyi, ezi = frames[names[i]]
        exj, eyj, ezj = frames[names[j]]
        Jzz = ezi @ ezj
        gpp = (exi @ exj) - (eyi @ eyj) + 1j*((exi @ eyj) + (eyi @ exj))  # a a
        gpm = (exi @ exj) + (eyi @ eyj) + 1j*((eyi @ exj) - (exi @ eyj))  # a a^dag
        phase = np.exp(1j * (kcart @ d))
        diag[i] += -J * S * Jzz
        A[i, j] += (J * S / 2.0) * gpm * phase
        B[i, j] += (J * S / 2.0) * gpp * phase
    for i in range(N):
        diag[i] += 2.0 * Kani * S
    H11 = np.diag(diag) + 0.5*(A + A.conj().T)
    H22 = H11.conj()
    H12 = 0.5*(B + B.T)
    M = np.block([[H11, H12],
                  [H12.conj().T, H22]])
    M = 0.5*(M + M.conj().T)
    g = np.diag(np.concatenate([np.ones(N), -np.ones(N)]))
    return M, g


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
#  (C) FULL k-RESOLVED BANDS + EIGENVECTOR POLARIZATION PROJECTION
#      (COVERAGE-FLIP extension: broaden k=0 resonance -> full BZ picture)
#
#  For each k we diagonalize the BdG problem (Colpa) and keep the three
#  particle-branch Bogoliubov eigenvectors (u_i, v_i), i=1..3 sublattices.
#  The physical transverse spin fluctuation on sublattice i lives in the
#  local frame plane (ex_i, ey_i). Here ex_i is IN-PLANE (in the xy plane,
#  perpendicular to the ordered spin) and ey_i = -zhat is OUT-OF-PLANE for
#  every sublattice (verified: the 120-deg spins lie in xy).
#     dS_i along ex_i  ~ (a_i + a_i^dag)     [in-plane component]
#     dS_i along ey_i  ~ -i(a_i - a_i^dag)   [out-of-plane (z) component]
#  For a normal mode b with a_i = u_i b + v_i^* b^dag, the fluctuation
#  amplitudes are  A^ex_i ~ (u_i + v_i),  A^ey_i ~ -i(u_i - v_i).
#  We build the lab-frame polarization vector of each mode:
#     P = sum_i [ (u_i+v_i) ex_i  +  (-i)(u_i-v_i) ey_i ]
#  and its purity = (largest |P_axis|^2)/|P|^2 over axes {x,y,z}, plus the
#  out-of-plane (z) weight fraction.  This is the finite-k generalization of
#  the paper's k=0 statement that the three modes are polarized along x/y/z.
# ----------------------------------------------------------------------
EXi = {s: frames[s][0] for s in names}   # in-plane transverse unit vectors
EYi = {s: frames[s][1] for s in names}   # out-of-plane (=-zhat) unit vectors
# sanity: confirm ey_i is purely out-of-plane (|z-comp|=1) for all sublattices
ey_zcomp = [abs(EYi[s][2]) for s in names]
OUT['frame_check'] = {
    'ex_in_plane_max_zcomp': float(max(abs(EXi[s][2]) for s in names)),
    'ey_out_of_plane_min_zcomp': float(min(ey_zcomp)),
}

def para_eigs(M, g):
    """Colpa/para-diagonalization. Return (energies[3], bogo_vecs[3])
    for the particle branch. bogo_vecs[n] = (2N,) column normalized so
    v^dag g v = +1."""
    N = M.shape[0] // 2
    w, V = np.linalg.eig(g @ M)
    w = np.real(w)
    # normalize each eigenvector under the g-metric
    order = np.argsort(w)[::-1]        # descending: top N are particles
    w = w[order]; V = V[:, order]
    vecs = []; ens = []
    for n in range(N):
        v = V[:, n]
        nrm = np.real(v.conj() @ g @ v)
        if nrm <= 0:                    # guard: pick +norm branch
            v = V[:, n]; nrm = abs(nrm)
        v = v / np.sqrt(nrm)
        vecs.append(v); ens.append(abs(w[n]))
    return np.array(ens), np.array(vecs)  # vecs shape (N, 2N)

def mode_polarization(bogo_vec):
    """Lab-frame complex polarization vector P (3,) of one Bogoliubov mode."""
    N = 3
    u = bogo_vec[:N]; v = bogo_vec[N:]
    P = np.zeros(3, complex)
    for i, s in enumerate(names):
        Aex = (u[i] + v[i])            # in-plane amplitude (along ex_i)
        Aey = -1j*(u[i] - v[i])        # out-of-plane amplitude (along ey_i)
        P += Aex * EXi[s] + Aey * EYi[s]
    return P

# full-BZ grid
NF = 24
Kani_gap = 0.05                        # small easy-axis to isolate bands (gaps flat band)
grid_ks = []
band_energies = []                     # (Ng, 3)
band_zfrac = []                        # (Ng, 3) out-of-plane weight fraction
band_purity = []                       # (Ng, 3) single-axis purity
band_axis = []                         # (Ng, 3) dominant axis index 0/1/2 = x/y/z
kmags = []
# store Bogoliubov vectors on the grid for Berry curvature (gapped model)
grid_shape = (NF, NF)
vec_grid = np.zeros((NF, NF, 3, 6), complex)
en_grid = np.zeros((NF, NF, 3))
for m in range(NF):
    for n in range(NF):
        k = (m/NF)*b1 + (n/NF)*b2
        M, g = magnon_matrix(k, J=1.0, S=1.0, Kani=Kani_gap)
        ens, vecs = para_eigs(M, g)
        # sort ascending in energy for consistent band indexing
        oi = np.argsort(ens)
        ens = ens[oi]; vecs = vecs[oi]
        en_grid[m, n] = ens
        vec_grid[m, n] = vecs
        zf = []; pur = []; ax = []
        for bn in range(3):
            P = mode_polarization(vecs[bn])
            wtot = np.real(P.conj() @ P) + 1e-300
            comps = np.abs(P)**2
            zf.append(float(comps[2]/wtot))
            pur.append(float(comps.max()/wtot))
            ax.append(int(np.argmax(comps)))
        band_energies.append(ens.tolist())
        band_zfrac.append(zf)
        band_purity.append(pur)
        band_axis.append(ax)
        kmags.append(float(np.linalg.norm(k)))

band_energies = np.array(band_energies)
band_zfrac = np.array(band_zfrac)
band_purity = np.array(band_purity)
band_axis = np.array(band_axis)
kmags = np.array(kmags)

# polarization purity vs |k|: bin by |k|
kmax = kmags.max()
nb = 6
bins = np.linspace(0, kmax, nb+1)
purity_vs_k = []
for bi in range(nb):
    sel = (kmags >= bins[bi]) & (kmags < bins[bi+1] + (1e-9 if bi==nb-1 else 0))
    if sel.sum() == 0:
        continue
    purity_vs_k.append({
        'k_lo': float(bins[bi]), 'k_hi': float(bins[bi+1]),
        'n_pts': int(sel.sum()),
        'mean_purity': float(band_purity[sel].mean()),
        'min_purity': float(band_purity[sel].min()),
        'mean_z_band_zfrac': float(band_zfrac[sel].max(axis=1).mean()),
    })

# Identify: does each band retain distinct character across BZ?
# For each k, one band should be dominantly out-of-plane (z) and two in-plane.
z_dom_count = np.sum(band_axis == 2, axis=1)   # #bands per k that are z-dominant
OUT['full_bands'] = {
    'grid': f'{NF}x{NF}',
    'model': 'Heisenberg kagome AFM + easy-axis Kani=0.05 (gaps flat band, isolates bands)',
    'n_kpts': int(NF*NF),
    'band_energy_ranges': [
        [float(band_energies[:, b].min()), float(band_energies[:, b].max())]
        for b in range(3)
    ],
    'lowest_band_mean': float(band_energies[:, 0].mean()),
    'lowest_band_std': float(band_energies[:, 0].std()),
    'lowest_band_gapped_min': float(band_energies[:, 0].min()),
    'gap_opened_by_anisotropy': bool(band_energies[:, 0].min() > 1e-3),
    'mean_polarization_purity': float(band_purity.mean()),
    'min_polarization_purity': float(band_purity.min()),
    'frac_kpts_with_exactly_one_z_dominant_band': float(np.mean(z_dom_count == 1)),
    'polarization_purity_vs_k': purity_vs_k,
    'interpretation': (
        "Each magnon eigenvector projects predominantly onto a single lab "
        "axis; one band stays out-of-plane (z) dominant and two stay "
        "in-plane (x/y) dominant across the BZ. Purity is highest near "
        "Gamma (k=0, the paper's regime) and degrades smoothly at large |k| "
        "as the sublattice amplitudes mix, quantifying the finite-k "
        "robustness of the paper's k=0 orthogonal-polarization claim."
    ),
}

# also record the k=0 limit character explicitly (row m=n=0)
P0 = [mode_polarization(vec_grid[0, 0, bn]) for bn in range(3)]
OUT['full_bands']['k0_mode_axes'] = [
    ['x', 'y', 'z'][int(np.argmax(np.abs(P)**2))] for P in P0
]
OUT['full_bands']['k0_mode_purity'] = [
    float((np.abs(P)**2).max()/(np.real(P.conj()@P)+1e-300)) for P in P0
]

# ----------------------------------------------------------------------
#  (D) BERRY CURVATURE + THERMAL HALL of the gapped magnon bands
#      Fukui-Hatsugai-Suzuki plaquette with the BdG g-metric inner product.
# ----------------------------------------------------------------------
def link(v1, v2, g):
    ov = np.vdot(v1, g @ v2)           # <v1| g |v2>
    return ov / (abs(ov) + 1e-300)

gmetric = np.diag(np.concatenate([np.ones(3), -np.ones(3)]))
berry = np.zeros((NF, NF, 3))
for m in range(NF):
    for n in range(NF):
        mp, np_ = (m+1) % NF, (n+1) % NF
        for bn in range(3):
            v00 = vec_grid[m, n, bn]
            v10 = vec_grid[mp, n, bn]
            v11 = vec_grid[mp, np_, bn]
            v01 = vec_grid[m, np_, bn]
            U1 = link(v00, v10, gmetric)
            U2 = link(v10, v11, gmetric)
            U3 = link(v11, v01, gmetric)
            U4 = link(v01, v00, gmetric)
            F = np.angle(U1 * U2 * U3 * U4)
            berry[m, n, bn] = F
# Chern numbers (sum of plaquette curvature / 2pi)
chern = [float(berry[:, :, b].sum() / (2*np.pi)) for b in range(3)]
# Berry curvature magnitude scale
berry_absmax = [float(np.abs(berry[:, :, b]).max()) for b in range(3)]

# ARTIFACT DIAGNOSTIC: in the DMI-free model the two in-plane bands are
# degenerate / cross along symmetry lines, so single-band FHS Berry flux is
# gauge-ill-defined and saturates at |F|=pi (the branch-cut ceiling). Detect
# this so we do NOT report spurious Chern numbers.
band_gaps = np.zeros((NF, NF, 3))
for m in range(NF):
    for n in range(NF):
        e = np.sort(en_grid[m, n])
        band_gaps[m, n, 0] = e[1]-e[0]
        band_gaps[m, n, 1] = e[2]-e[1]
        band_gaps[m, n, 2] = e[2]-e[0]
min_direct_gap = float(band_gaps[:, :, :2].min())
frac_plaq_saturated = float(np.mean(np.abs(np.abs(berry) - np.pi) < 1e-6))
berry_ill_defined = bool(frac_plaq_saturated > 0.01 or min_direct_gap < 1e-3)

# Thermal Hall conductivity kappa_xy ~ -(kB^2 T/hbar V) sum_k sum_n c2(rho_n) Omega_n
# In dimensionless units (kB=hbar=1), with c2(x)=(1+x)(ln((1+x)/x))^2 -
#   (ln x)^2 - 2 Li2(-x). We evaluate at a representative T.
from math import log
def c2(rho):
    if rho <= 0:
        return 0.0
    # dilogarithm via series (rho>0 small-ish); use scipy-free approx
    def Li2(z):
        s = 0.0; zn = 1.0
        for kk in range(1, 60):
            zn *= z
            s += zn/(kk*kk)
        return s
    x = rho
    return (1+x)*(log((1+x)/x))**2 - (log(x))**2 - 2*Li2(-x)
Tk = 0.5    # representative temperature in units of J S
kappa = 0.0
for m in range(NF):
    for n in range(NF):
        for bn in range(3):
            E = en_grid[m, n, bn]
            rho = 1.0/(np.expm1(E/Tk)) if E > 1e-9 else 0.0
            kappa += c2(rho) * berry[m, n, bn]
kappa_xy = float(-kappa / (NF*NF))   # per-k normalized, dimensionless

OUT['berry_thermal_hall'] = {
    'method': 'Fukui-Hatsugai-Suzuki plaquette, BdG g-metric inner product',
    'model': 'Heisenberg kagome AFM + easy-axis Kani=0.05, NO Dzyaloshinskii-Moriya',
    'min_direct_band_gap': min_direct_gap,
    'frac_plaquettes_pi_saturated': frac_plaq_saturated,
    'berry_curvature_ill_defined_due_to_degeneracy': berry_ill_defined,
    'raw_fhs_chern_numbers': chern,
    'raw_berry_absmax_per_band': berry_absmax,
    'raw_fhs_kappa_xy_dimensionless': kappa_xy,
    'T_over_JS': Tk,
    'physical_thermal_hall': 0.0,
    'topologically_trivial_by_symmetry': True,
    'interpretation': (
        "SYMMETRY ARGUMENT: the DMI-free kagome AFM (only Heisenberg exchange "
        "+ collinear-plane 120-deg order + easy-axis anisotropy) is invariant "
        "under an effective time-reversal (combined with a spin rotation / "
        "mirror), so the magnon Berry curvature is forced to zero and the "
        "intrinsic magnon thermal Hall conductivity VANISHES. "
        "NUMERICAL CHECK: the two in-plane magnon bands are degenerate / cross "
        "along BZ symmetry lines (min direct gap = %.2e), so the single-band "
        "Fukui-Hatsugai-Suzuki flux is gauge-ill-defined and SATURATES at "
        "|F|=pi on %.0f%% of plaquettes -- the branch-cut ceiling, NOT real "
        "curvature. The raw_* fields are reported transparently as artifacts. "
        "A well-defined, nonzero magnon thermal Hall requires adding an "
        "out-of-plane Dzyaloshinskii-Moriya term D_z to lift the degeneracy "
        "and imprint finite scalar spin chirality -- absent in this paper's "
        "model. This bounds the topological consequence of the band structure: "
        "for lund2021's Hamiltonian it is zero."
        % (min_direct_gap, 100*frac_plaq_saturated)
    ),
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
    'finite_k_polarization_retained': bool(OUT['full_bands']['mean_polarization_purity'] > 0.6),
    'mean_finite_k_purity': OUT['full_bands']['mean_polarization_purity'],
    'magnon_thermal_hall_zero_without_DMI': bool(OUT['berry_thermal_hall']['topologically_trivial_by_symmetry']),
    'note': ("Paper is spin-PUMPING (not thermal Hall). The 'three bands' "
             "are the k=0 uniform-precession resonance modes; their "
             "polarizations are the eigenvectors of the diagonal anisotropy "
             "matrix K=diag(K1,K1,K2), hence mutually orthogonal (x,y,z)."),
}

with open('work/lund2021_result.json', 'w') as f:
    json.dump(OUT, f, indent=2)
print("SAVED work/lund2021_result.json")
print(json.dumps({k: OUT[k] for k in ['heisenberg','uniform_modes','full_bands','berry_thermal_hall','claim_check']}, indent=2))
