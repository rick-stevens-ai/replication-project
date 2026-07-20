#!/usr/bin/env python3
"""
From-scratch replication of Malashevich, Souza, Coh & Vanderbilt,
"Theory of orbital magnetoelectric response", New J. Phys. 12, 053032 (2010)
[arXiv:1002.0300].

HEADLINE: the linear (orbital) magnetoelectric susceptibility alpha_da = dM_a/dE_d
of a 3D tight-binding ordinary ME insulator, computed under periodic boundary
conditions (k-space Chern-Simons / axion OMP), agrees with bounded-sample
(open boundary) finite-field calculations.

Model (Appendix A, table A1): spinless simple-cubic lattice, 2x2x2 primitive cell
=> 8 sites/cell, magnitude-1 complex NN hoppings t=e^{i phi}, random on-site
energies, two lowest bands treated as occupied. Broken TR + inversion.

Two independent calculations of the ME response:
  (A) BOUNDED SAMPLE (gauge-free, eq (3)): open-BC cube of LxLxL cells; apply
      E-field via H = H0 + E.r (r diagonal, paper's choice); orbital
      magnetization M_a = -(e/2cV) Tr[P_occ (r x v)_a], v = i[H,r];
      alpha_zz = dM_z/dE_z by finite differences; extrapolate L->inf.
  (B) k-SPACE Chern-Simons / axion OMP theta_CS, eq (47a):
      theta_CS = -(1/4pi) int d3k eps_ijk tr[A_i d_j A_k - (2i/3) A_i A_j A_k]
      with non-Abelian Berry connection A over the 2 occupied bands, in a smooth
      gauge built by projecting trial delta orbitals at the 2 lowest-onsite sites
      (paper's prescription). alpha_iso^CS = theta_CS e^2/(2 pi h c).

Berry/orbital machinery adapted from the gobel2024 Kubo/Berry kernel
(shared-kernels-cache/gobel2024_sd_skyrmion_kubo_Lz_kernel.py): velocity v=i[H,r],
occupied-projector traces, eigenbasis Berry connections.

Units: e = hbar = c = 1  (=> h = 2pi). alpha reported in these natural units.
"""
import json, os, time
import numpy as np

t0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "malashevich2010_result.json")

# ---------------------------------------------------------------- model (table A1)
# 8 sublattice positions in the 2x2x2 cubic cell (cell constant a = 1); spacing 0.5
SUB = np.array([
    [0.0, 0.0, 0.0],  # s0
    [0.5, 0.0, 0.0],  # s1
    [0.5, 0.5, 0.0],  # s2
    [0.0, 0.5, 0.0],  # s3
    [0.0, 0.0, 0.5],  # s4
    [0.5, 0.0, 0.5],  # s5
    [0.5, 0.5, 0.5],  # s6
    [0.0, 0.5, 0.5],  # s7
])
EONSITE = np.array([-6.5, 0.9, 1.4, 1.2, -6.0, 1.5, 0.8, 1.2])
PI = np.pi
# phases phi(i + axis/2 -> i): term  e^{i phi} c_i^dag c_{neighbor at i+0.5 axis}
# col x, y, z  (row = site). row0 x-phase is the scanned parameter phi (placeholder).
PHASE_X = np.array([np.nan, 1.3, 0.8, 0.3, 1.4, 0.6, 0.8, 1.9]) * PI
PHASE_Y = np.array([0.5, 0.2, 1.4, 1.9, 0.8, 1.7, 0.6, 0.3]) * PI
PHASE_Z = np.array([1.7, 0.5, 0.6, 1.0, 0.3, 0.7, 1.2, 1.4]) * PI

# +axis neighbour sublattice index for each site (physical pos = site + 0.5 axis)
NX = [1, 0, 3, 2, 5, 4, 7, 6]
NY = [3, 2, 1, 0, 7, 6, 5, 4]
NZ = [4, 5, 6, 7, 0, 1, 2, 3]


def bloch_H(k, phi):
    """8x8 Bloch Hamiltonian H(k), convention II (r diagonal: Bloch phase carries
    the +0.5 sublattice bond displacement). k in radians (a=1)."""
    H = np.zeros((8, 8), dtype=complex)
    np.fill_diagonal(H, EONSITE)
    px = PHASE_X.copy(); px[0] = phi
    kx, ky, kz = k
    for i in range(8):
        # +x bond, displacement +0.5 x
        H[i, NX[i]] += np.exp(1j * px[i]) * np.exp(1j * kx * 0.5)
        # +y bond
        H[i, NY[i]] += np.exp(1j * PHASE_Y[i]) * np.exp(1j * ky * 0.5)
        # +z bond
        H[i, NZ[i]] += np.exp(1j * PHASE_Z[i]) * np.exp(1j * kz * 0.5)
    H = H + H.conj().T
    # (diagonal was added once, H+H^dag doubles it) -> fix diagonal
    np.fill_diagonal(H, EONSITE)
    return H


def bandstructure_gap(phi, N=12):
    """min direct gap between band-2 and band-3 (0-indexed 1|2) over BZ grid."""
    ks = 2 * PI * np.arange(N) / N
    gmin = np.inf
    Ev, Ec = np.inf, -np.inf
    for kx in ks:
        for ky in ks:
            for kz in ks:
                E = np.linalg.eigvalsh(bloch_H((kx, ky, kz), phi))
                gmin = min(gmin, E[2] - E[1])
                Ev = min(Ev, E[1]); Ec = max(Ec, E[1])
    return float(gmin)


# ---------------------------------------------------------------- (B) k-space theta_CS
def smooth_frame(k, phi, nocc=2):
    """Occupied Bloch frame in a smooth gauge: project trial delta orbitals at the
    two lowest on-site-energy sites (s0, s4) onto the occupied subspace and
    Lowdin-orthonormalize (paper Appendix A prescription)."""
    E, V = np.linalg.eigh(bloch_H(k, phi))
    P = V[:, :nocc]                       # occupied eigenvectors (8 x nocc)
    trials = np.zeros((8, nocc), dtype=complex)
    trials[0, 0] = 1.0                    # delta at s0 (E=-6.5, lowest)
    trials[4, 1] = 1.0                    # delta at s4 (E=-6.0, 2nd lowest)
    A = P @ (P.conj().T @ trials)         # project trials into occ subspace
    # Lowdin orthonormalize the projected trials -> smooth frame
    S = A.conj().T @ A
    w, U = np.linalg.eigh(S)
    Sinv = U @ np.diag(1.0 / np.sqrt(w)) @ U.conj().T
    return A @ Sinv                       # 8 x nocc smooth orthonormal frame


def berry_conn(kgrid_frames, N, ax):
    """Non-Abelian Berry connection A_ax,mn = i <u_m| d_ax u_n> via central diff on
    the periodic grid. kgrid_frames[ix,iy,iz] = (8 x nocc) smooth frame."""
    dk = 2 * PI / N
    nocc = kgrid_frames[0, 0, 0].shape[1]
    A = np.empty((N, N, N, nocc, nocc), dtype=complex)
    for ix in range(N):
        for iy in range(N):
            for iz in range(N):
                u = kgrid_frames[ix, iy, iz]
                if ax == 0:
                    up = kgrid_frames[(ix + 1) % N, iy, iz]
                    um = kgrid_frames[(ix - 1) % N, iy, iz]
                elif ax == 1:
                    up = kgrid_frames[ix, (iy + 1) % N, iz]
                    um = kgrid_frames[ix, (iy - 1) % N, iz]
                else:
                    up = kgrid_frames[ix, iy, (iz + 1) % N]
                    um = kgrid_frames[ix, iy, (iz - 1) % N]
                du = (up - um) / (2 * dk)
                A[ix, iy, iz] = 1j * (u.conj().T @ du)
    return A


def theta_CS(phi, N=10):
    """Chern-Simons axion angle theta_CS, eq (47a)."""
    ks = 2 * PI * np.arange(N) / N
    frames = np.empty((N, N, N), dtype=object)
    for ix in range(N):
        for iy in range(N):
            for iz in range(N):
                frames[ix, iy, iz] = smooth_frame((ks[ix], ks[iy], ks[iz]), phi)
    Ax = berry_conn(frames, N, 0)
    Ay = berry_conn(frames, N, 1)
    Az = berry_conn(frames, N, 2)
    dk = 2 * PI / N
    # d_j A_k via central differences of the connection field
    def deriv(F, ax):
        return (np.roll(F, -1, axis=ax) - np.roll(F, 1, axis=ax)) / (2 * dk)
    # eps_ijk tr[A_i d_j A_k - (2i/3) A_i A_j A_k], summed cyclically x,y,z
    integ = 0.0
    combos = [(0, 1, 2), (1, 2, 0), (2, 0, 1),
              (0, 2, 1), (2, 1, 0), (1, 0, 2)]
    sign = {(0, 1, 2): 1, (1, 2, 0): 1, (2, 0, 1): 1,
            (0, 2, 1): -1, (2, 1, 0): -1, (1, 0, 2): -1}
    Aarr = [Ax, Ay, Az]
    for (i, j, kk) in combos:
        s = sign[(i, j, kk)]
        djAk = deriv(Aarr[kk], j)
        for ix in range(N):
            for iy in range(N):
                for iz in range(N):
                    Ai = Aarr[i][ix, iy, iz]
                    Aj = Aarr[j][ix, iy, iz]
                    Ak = Aarr[kk][ix, iy, iz]
                    term1 = np.trace(Ai @ djAk[ix, iy, iz])
                    term3 = np.trace(Ai @ Aj @ Ak)
                    integ += s * (term1 - (2j / 3.0) * term3).real
    dV = dk ** 3
    theta = -(1.0 / (4 * PI)) * integ * dV
    return float(theta)


# ---------------------------------------------------------------- (A) bounded sample
def build_open_cluster(L, phi):
    """Open-BC cube: sites on simple-cubic grid, spacing 0.5, coords 0..L
    (2L+1 pts/edge = L eight-site cells). Returns H0, X,Y,Z (diagonal pos ops)."""
    npts = 2 * L + 1
    coords = []
    for iz in range(npts):
        for iy in range(npts):
            for ix in range(npts):
                coords.append((ix, iy, iz))
    coords = np.array(coords)              # integer half-lattice indices
    nsite = len(coords)
    index = {tuple(c): n for n, c in enumerate(coords)}
    H = np.zeros((nsite, nsite), dtype=complex)
    px = PHASE_X.copy(); px[0] = phi

    def sublat(c):
        return (c[0] % 2) + 2 * (c[1] % 2) + 4 * (c[2] % 2)
    # map (px%2,py%2,pz%2) triple -> sublattice row in SUB/EONSITE order
    tri2sub = {}
    for s, p in enumerate(SUB):
        tri2sub[(int(2 * p[0]) % 2, int(2 * p[1]) % 2, int(2 * p[2]) % 2)] = s
    for n, c in enumerate(coords):
        s = tri2sub[(c[0] % 2, c[1] % 2, c[2] % 2)]
        H[n, n] = EONSITE[s]
        # +x neighbour: term e^{i px[s]} c_i^dag c_j  (j at c+ (1,0,0) half-units)
        for axis, phases in ((0, px), (1, PHASE_Y), (2, PHASE_Z)):
            cj = list(c); cj[axis] += 1; cj = tuple(cj)
            if cj in index:
                j = index[cj]
                amp = np.exp(1j * phases[s])
                H[n, j] += amp
                H[j, n] += np.conj(amp)
    R = coords.astype(float) * 0.5        # physical positions
    return H, R[:, 0], R[:, 1], R[:, 2]


def orbital_Mz(H, X, Y, Z, nocc, Efield=(0, 0, 0)):
    """Orbital magnetization M_z = -(1/2V) Tr[P_occ (x v_y - y v_x)], v=i[H,r].
    Applies H -> H + E.r. V normalised per cell later. e=c=hbar=1."""
    Ex, Ey, Ez = Efield
    Ht = H + np.diag(Ex * X + Ey * Y + Ez * Z)
    E, V = np.linalg.eigh(Ht)
    Xop = np.diag(X.astype(complex)); Yop = np.diag(Y.astype(complex))
    vx = 1j * (Ht @ Xop - Xop @ Ht)
    vy = 1j * (Ht @ Yop - Yop @ Ht)
    op = Xop @ vy - Yop @ vx              # (r x v)_z
    op = 0.5 * (op + op.conj().T)
    Pocc = V[:, :nocc] @ V[:, :nocc].conj().T
    Mz_raw = np.trace(Pocc @ op).real     # sum over occupied of <r x v>_z
    return -0.5 * Mz_raw                  # M_z * V  (volume factored out separately)


def alpha_zz_bounded(phi, Ls=(3, 4, 5), Efield_amp=0.01):
    """alpha_zz via finite-field diff on open clusters + 1/L extrapolation.
    Uses M_z*V from orbital_Mz; alpha_zz = d(M_z)/dE_z with M_z = (M_z*V)/V,
    V = L^3 (L eight-site cells per edge, Vc=1)."""
    rows = []
    for L in Ls:
        H, X, Y, Z = build_open_cluster(L, phi)
        nsite = H.shape[0]
        nocc = int(round(nsite * 2.0 / 8.0))  # 2 of 8 bands filled
        Vvol = float(L) ** 3
        MzV_p = orbital_Mz(H, X, Y, Z, nocc, (0, 0, +Efield_amp))
        MzV_m = orbital_Mz(H, X, Y, Z, nocc, (0, 0, -Efield_amp))
        # alpha_zz = dM_z/dE_z, M_z = MzV / V
        a = (MzV_p - MzV_m) / (2 * Efield_amp) / Vvol
        rows.append({"L": L, "nsite": nsite, "nocc": nocc,
                     "alpha_zz": float(a)})
    # extrapolate in 1/L
    Lv = np.array([r["L"] for r in rows], float)
    av = np.array([r["alpha_zz"] for r in rows], float)
    if len(Lv) >= 2:
        p = np.polyfit(1.0 / Lv, av, min(2, len(Lv) - 1))
        alpha_inf = float(np.polyval(p, 0.0))
    else:
        alpha_inf = float(av[-1])
    return rows, alpha_inf


# ---------------------------------------------------------------- driver
def main():
    phi = 0.5 * PI     # representative value of the scanned phase
    res = {
        "paper": "Malashevich, Souza, Coh & Vanderbilt, New J. Phys. 12, 053032 (2010)",
        "arxiv": "1002.0300",
        "model": "spinless simple-cubic 2x2x2 (8-site) tight-binding ordinary ME insulator (Appendix A, table A1)",
        "quantity": "linear orbital magnetoelectric susceptibility alpha_da = dM_a/dE_d",
        "phi_scanned": phi,
        "units": "natural units e=hbar=c=1 (h=2pi); alpha in these units",
        "berry_machinery_credit": "adapted from gobel2024 Kubo/Berry kernel (shared-kernels-cache/gobel2024_sd_skyrmion_kubo_Lz_kernel.py): v=i[H,r], occupied-projector traces, eigenbasis Berry connections",
    }

    # band gap (must be insulating between band 2 and 3)
    gap = bandstructure_gap(phi, N=10)
    res["direct_gap_band2_3"] = gap
    res["insulating"] = bool(gap > 1e-3)
    print(f"[gap] min direct gap (valence|conduction) = {gap:.4f}  insulating={gap>1e-3}")

    # (A) bounded-sample finite-field alpha_zz
    rows, alpha_bounded = alpha_zz_bounded(phi, Ls=(3, 4, 5))
    res["bounded_sample"] = {"per_L": rows, "alpha_zz_extrap_Linf": alpha_bounded}
    print(f"[bounded] alpha_zz per L: " +
          ", ".join(f"L{r['L']}={r['alpha_zz']:.4f}" for r in rows) +
          f"  -> Linf={alpha_bounded:.4f}")

    # SAVE-EARLY (before the expensive/uncertain k-space CS term)
    res["runtime_sec_partial"] = round(time.time() - t0, 1)
    with open(OUT, "w") as f:
        json.dump(res, f, indent=2)
    print(f"[save-early] wrote {OUT}")

    # (B) k-space Chern-Simons axion OMP
    try:
        theta = theta_CS(phi, N=8)
        # isotropic alpha from theta: alpha_iso = theta e^2/(2 pi h c) ; e=c=1,h=2pi
        alpha_iso_CS = theta / (2 * PI * 2 * PI)
        res["kspace_chern_simons"] = {
            "theta_CS": theta,
            "alpha_iso_CS_natural_units": float(alpha_iso_CS),
            "note": "smooth-gauge projection of delta trials at 2 lowest-onsite sites; eq (47a)",
        }
        print(f"[kspace] theta_CS = {theta:.5f}  alpha_iso^CS = {alpha_iso_CS:.6f}")
    except Exception as e:
        res["kspace_chern_simons"] = {"error": str(e)}
        print("[kspace] ERROR:", e)

    res["runtime_sec"] = round(time.time() - t0, 1)
    with open(OUT, "w") as f:
        json.dump(res, f, indent=2)
    print(f"[done] wrote {OUT}  ({res['runtime_sec']}s)")
    return res


if __name__ == "__main__":
    main()
