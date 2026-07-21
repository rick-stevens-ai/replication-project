#!/usr/bin/env python3
"""
From-scratch replication of the THEORY CORE of:
  Zhang, Wan, Deng, et al., "Observation of Moire Plasmonic Skyrmion Clusters",
  arXiv:2411.05576.

Reproducible analytic core (experiment / FDTD parts NOT reproduced):
  Eq.(1)  Axial (z) SPP field of two twisted hexagonal nanoslit groups:
            E_z(r) = e^{-|kz|z} { sum_{j=1}^{6} E~_j e^{-i(k_j(0).r - phi_j)}
                                 + sum_{j=1}^{6} E~_j e^{-i(k_j(th).r - phi_j - dphi)} }
          k_j(th) = R(th) k_t [cos phi_j, sin phi_j],  k_t^2 + kz^2 = k0^2.
          phi_j = 2 pi sigma_j / N  (geometric phase of jth nanoslit).
  Transverse E from Maxwell / div E = 0 for each evanescent SPP partial wave:
          i k_t (E_t.k^_j) - |kz| E_z = 0  ->  E_t = -i (|kz|/k_t) E_z  along k^_j.
  Eq.(2)  Normalized 3D polarization unit vector  E_bar = Re[E]/|Re[E]|.
  Eq.(4)  Skyrmion number density  s = E_bar . (dx E_bar x dy E_bar).
  Eq.(3)  Skyrmion number  Q = (1/4pi) INT_cell s d^2r.

Paper claims (main text):
  - Elementary single hex SPP lattice -> Q = +/-1 per cell.
  - Composite twist th = 38.21 deg -> skyrmion CLUSTER with Q = -3 per moire unit.

Topological charge computed with the Berg-Luscher lattice solid-angle method
(integer-robust) plus a finite-difference cross check.

PROVENANCE: Berg-Luscher solid-angle kernel adapted from Ollie's shared kernel
  ~/shared-kernels-cache/ollie_berg_luscher_topological_charge_kernel.py
CPU-only, numpy only.
"""
import json, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
WORK = os.path.join(ROOT, "work")
os.makedirs(WORK, exist_ok=True)

# ---- provenance: Berg-Luscher kernel (adapted) ----------------------------
def topo_charge_berg(n):
    """Berg-Luscher lattice solid-angle Q. n: (3, Ny, Nx). Integer-robust."""
    def solid_angle(a, b, c):
        num = np.einsum("i...,i...->...", a, np.cross(b, c, axis=0))
        den = (1.0
               + np.einsum("i...,i...->...", a, b)
               + np.einsum("i...,i...->...", b, c)
               + np.einsum("i...,i...->...", c, a))
        return 2.0 * np.arctan2(num, den)
    n1 = n[:, :-1, :-1]; n2 = n[:, :-1, 1:]
    n3 = n[:, 1:, 1:];   n4 = n[:, 1:, :-1]
    om = solid_angle(n1, n2, n3) + solid_angle(n1, n3, n4)
    return float(om.sum() / (4.0 * np.pi))

def topo_charge_fd(X, Y, n):
    dx = X[0, 1] - X[0, 0]; dy = Y[1, 0] - Y[0, 0]
    dnx = np.gradient(n, dx, axis=2); dny = np.gradient(n, dy, axis=1)
    dens = np.einsum("i...,i...->...", n, np.cross(dnx, dny, axis=0))
    return float(dens.sum() * dx * dy / (4.0 * np.pi))

# ---- field construction ---------------------------------------------------
def rot(th):
    c, s = np.cos(th), np.sin(th)
    return np.array([[c, -s], [s, c]])

def spp_E(X, Y, angles_deg, kt, kzabs, sigma, N, dphi, group_phase=0.0):
    """Complex 3-component E field from a set of evanescent SPP partial waves.
    E_z per wave = E~ e^{-i(k.r - phi_j - group_phase)} ; E~ = 1.
    Transverse: E_t = -i (kzabs/kt) E_z along k^_j (from div E = 0)."""
    Ex = np.zeros_like(X, dtype=complex)
    Ey = np.zeros_like(X, dtype=complex)
    Ez = np.zeros_like(X, dtype=complex)
    for j, ad in enumerate(angles_deg):
        a = np.deg2rad(ad)
        khat = np.array([np.cos(a), np.sin(a)])
        kx, ky = kt * khat
        phi_j = 2.0 * np.pi * sigma[j] / N
        phase = kx * X + ky * Y - phi_j - group_phase
        ez = np.exp(-1j * phase)                 # z-component
        et = -1j * (kzabs / kt) * ez             # transverse magnitude along khat
        Ez += ez
        Ex += et * khat[0]
        Ey += et * khat[1]
    return Ex, Ey, Ez

def build_field(theta_deg, dphi, sigma, N=6, kt=1.0, k0=1.0, span=None, Ngrid=421,
                composite=True):
    """Return X, Y, n (3,Ny,Nx) normalized real polarization unit vector.
    kt in units where lambda_spp = 1 -> kt = 2*pi; grid in units of lambda_spp."""
    kt = 2.0 * np.pi                     # |k_t| for lambda_spp = 1
    k0v = kt / 0.98                       # SPP: k_spp slightly > k0; kz small evanescent
    kzabs = np.sqrt(max(k0v**2 - kt**2, (0.15*kt)**2))
    kzabs = 0.30 * kt                     # representative evanescent decay scale
    if span is None:
        span = 3.0                        # lambda_spp
    xs = np.linspace(-span, span, Ngrid)
    X, Y = np.meshgrid(xs, xs)
    ang_a = [60.0 * j for j in range(6)]
    Exa, Eya, Eza = spp_E(X, Y, ang_a, kt, kzabs, sigma, N, dphi, group_phase=0.0)
    if composite:
        ang_b = [60.0 * j + theta_deg for j in range(6)]
        Exb, Eyb, Ezb = spp_E(X, Y, ang_b, kt, kzabs, sigma, N, dphi, group_phase=dphi)
        Ex, Ey, Ez = Exa + Exb, Eya + Eyb, Eza + Ezb
    else:
        Ex, Ey, Ez = Exa, Eya, Eza
    # Eq.(2): real part, normalized 3D polarization vector
    E = np.array([Ex.real, Ey.real, Ez.real])
    norm = np.sqrt((E**2).sum(axis=0))
    norm[norm == 0] = 1.0
    n = E / norm
    return X, Y, n

def Q_per_cell_scan(X, Y, n, half_frac=0.5):
    """Q integrated over the CENTRAL sub-window (one representative region),
    plus total-grid Q. Returns (Q_center_box, Q_total)."""
    Ny, Nx = n.shape[1], n.shape[2]
    q_tot = topo_charge_berg(n)
    return q_tot

# ---------------------------------------------------------------------------
def main():
    out = {"paper": "arXiv:2411.05576 Zhang et al., Moire Plasmonic Skyrmion Clusters",
           "provenance": "Berg-Luscher kernel adapted from ollie_berg_luscher_topological_charge_kernel.py",
           "model": "Eq.(1) twisted hex SPP interference; Eq.(2) norm 3D pol; Eq.(3,4) SND integral",
           "cases": []}

    # sigma_j = j : azimuthal geometric-phase winding (elementary skyrmion config)
    sigma = np.arange(6)

    # --- Case A: single hexagonal SPP lattice (elementary), expect |Q_cell| = 1 ---
    X, Y, n = build_field(0.0, dphi=0.0, sigma=sigma, span=1.0, Ngrid=401, composite=False)
    # integrate SND over exactly ONE primitive cell at the pattern center via FD box
    # find one cell: the hex SPP lattice period = 2*lambda_spp/sqrt(3) for kt=2pi.
    a_cell = 2.0 / np.sqrt(3.0)          # lambda_spp units (nearest-skyrmion spacing scale)
    def box_Q(X, Y, n, L):
        m = (np.abs(X) <= L/2) & (np.abs(Y) <= L/2)
        cols = np.where(m.any(axis=0))[0]; rows = np.where(m.any(axis=1))[0]
        sub = n[:, rows[0]:rows[-1]+1, cols[0]:cols[-1]+1]
        Xs = X[rows[0]:rows[-1]+1, cols[0]:cols[-1]+1]
        Ys = Y[rows[0]:rows[-1]+1, cols[0]:cols[-1]+1]
        return topo_charge_berg(sub), topo_charge_fd(Xs, Ys, sub)
    qb_A, qf_A = box_Q(X, Y, n, a_cell)
    q_tot_A = topo_charge_berg(n)
    out["cases"].append({
        "name": "elementary_single_hex_lattice",
        "theta_deg": 0.0,
        "Q_center_cell_berg": round(qb_A, 3),
        "Q_center_cell_fd": round(qf_A, 3),
        "Q_total_grid": round(q_tot_A, 3),
        "paper_claim": "elementary optical skyrmion Q = +/-1 per cell",
    })

    # --- Case B: composite twist theta = 38.21 deg -> skyrmion cluster ---
    theta = 38.21
    X, Y, n = build_field(theta, dphi=np.pi, sigma=sigma, span=3.0, Ngrid=601, composite=True)
    # moire supercell is much larger; integrate SND over central moire unit box.
    # sweep several box sizes to find the plateau (robust integer per moire unit)
    plateau = []
    for L in [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]:
        if L/2 > 3.0: continue
        qb, qf = box_Q(X, Y, n, L)
        plateau.append({"L": L, "Q_berg": round(qb, 3), "Q_fd": round(qf, 3)})
    q_tot_B = topo_charge_berg(n)
    out["cases"].append({
        "name": "composite_moire_cluster",
        "theta_deg": theta, "dphi": "pi", "sigma_j": "j (azimuthal winding)",
        "Q_box_plateau_scan": plateau,
        "Q_total_grid": round(q_tot_B, 3),
        "paper_claim": "moire skyrmion cluster Q = -3 per moire unit at 38.21 deg",
    })

    # --- twist-angle sweep of total-grid charge (qualitative moire control) ---
    sweep = []
    for th in [0, 10, 21.79, 30, 38.21, 46.83]:
        X, Y, n = build_field(th, dphi=np.pi, sigma=sigma, span=3.0, Ngrid=501,
                              composite=(th != 0))
        sweep.append({"theta_deg": th, "Q_total_grid": round(topo_charge_berg(n), 3)})
    out["twist_sweep_total_Q"] = sweep

    with open(os.path.join(WORK, "zhang2024_result.json"), "w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
