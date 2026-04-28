"""
Replication of Fregoso, Morimoto, Moore (2017) OSTI 1523841:
"Quantitative relationship between polarization differences and the
zone-averaged shift photocurrent."

Target: reproduce Fig. 1(b) for the Rice-Mele model.

Central identity (Eq. 9):
    e * Rbar_cv = a * (P_c - P_v) + W_cv * e * a

where:
    - P_n: Berry-phase polarization of band n (King-Smith–Vanderbilt)
    - Rbar_cv = (1/N) sum_k R_cv(k): zone-averaged shift vector
    - W_cv: integer winding number of interband dipole phase

Rice-Mele Bloch Hamiltonian (Eq. D2, with a = 1):
    H(k) = sigma_x * t*cos(k/2) - sigma_y * delta*sin(k/2) + sigma_z * Delta

We work in units e = a = t = 1 and fix Delta.
"""

import numpy as np
import matplotlib.pyplot as plt

# Pauli matrices
sx = np.array([[0, 1], [1, 0]], dtype=complex)
sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
sz = np.array([[1, 0], [0, -1]], dtype=complex)


def H_RM(k, t, delta, Delta):
    """Rice-Mele Bloch Hamiltonian (2x2), a=1."""
    return sx * (t * np.cos(k / 2)) - sy * (delta * np.sin(k / 2)) + sz * Delta


def eig_bands(k_arr, t, delta, Delta):
    """Diagonalize H(k) on a k-mesh. Returns (E[N,2], U[N,2,2]).

    U[k] has columns = eigenvectors in ascending-energy order.
    Phase gauge: fix first nonzero component real-positive.
    """
    N = len(k_arr)
    E = np.zeros((N, 2))
    U = np.zeros((N, 2, 2), dtype=complex)
    for i, k in enumerate(k_arr):
        H = H_RM(k, t, delta, Delta)
        w, v = np.linalg.eigh(H)
        # Gauge fix: make first component real & positive
        for b in range(2):
            phase = v[0, b]
            if abs(phase) > 1e-12:
                v[:, b] *= np.conj(phase) / abs(phase)
        E[i] = w
        U[i] = v
    return E, U


def berry_phase_polarization(U_band, sewing=None):
    """Discretized Berry phase (King-Smith-Vanderbilt) with optional sewing matrix.

    For the paper's Rice-Mele gauge H(k) uses cos(k/2), sin(k/2) so has
    period 4*pi instead of 2*pi. Under k -> k+2*pi, H transforms by V with
    V = diag(1,-1). Pass sewing=V so the BZ-closing overlap is
    <u(k_{N-1}) | V | u(k_0)>.
    Returns P in units of e*a (here e=a=1).
    """
    N = len(U_band)
    prod = 1.0 + 0.0j
    for j in range(N - 1):
        prod *= np.vdot(U_band[j], U_band[j + 1])
    u_closed = U_band[0] if sewing is None else sewing @ U_band[0]
    prod *= np.vdot(U_band[-1], u_closed)
    return np.angle(prod) / (2 * np.pi)


def shift_vector_2band(k_arr, t, delta, Delta):
    """Analytic shift vector for Rice-Mele (Eq. D7 / general Eq. C5).

    Use the d-vector formula (Eq. C5) for H = d . sigma:
        d = (t cos(k/2), -delta sin(k/2), Delta)
    Shift vector component along k (a,b both = k):

        R_cv = -|d| * [ d . (d' x d'') ] / ( |d|^2 |d'|^2 - ((|d|^2)'/2)^2 )

    Derivatives are w.r.t. k.
    """
    k = np.asarray(k_arr)
    d1 = t * np.cos(k / 2)
    d2 = -delta * np.sin(k / 2)
    d3 = np.full_like(k, Delta)
    # first derivatives
    d1p = -0.5 * t * np.sin(k / 2)
    d2p = -0.5 * delta * np.cos(k / 2)
    d3p = np.zeros_like(k)
    # second derivatives
    d1pp = -0.25 * t * np.cos(k / 2)
    d2pp = 0.25 * delta * np.sin(k / 2)
    d3pp = np.zeros_like(k)

    d = np.stack([d1, d2, d3], axis=-1)
    dp = np.stack([d1p, d2p, d3p], axis=-1)
    dpp = np.stack([d1pp, d2pp, d3pp], axis=-1)

    dmag = np.linalg.norm(d, axis=-1)
    dpmag2 = np.sum(dp * dp, axis=-1)
    # (|d|^2)' = 2 d . d'
    dsq_prime = 2.0 * np.sum(d * dp, axis=-1)
    # d' x d''
    cross = np.cross(dp, dpp)
    triple = np.sum(d * cross, axis=-1)

    denom = (dmag**2) * dpmag2 - (dsq_prime**2) / 4.0
    # Sign fixed by comparison with paper Eq. D8: R|_{k->0} = -t*Delta/(2*delta*E)
    R = dmag * triple / denom
    return R


def check_analytic_limits(t=1.0, delta=0.3, Delta=0.5):
    """Compare analytic formula with paper Eq. D8-D10 limits."""
    import math
    E0 = math.sqrt(t**2 + Delta**2)
    Epi = math.sqrt(delta**2 + Delta**2)
    R0_paper = -t * Delta / (2 * delta * E0)
    Rpi_paper = -delta * Delta / (2 * t * Epi)
    R0_num = shift_vector_2band(np.array([1e-8]), t, delta, Delta)[0]
    Rpi_num = shift_vector_2band(np.array([np.pi - 1e-8]), t, delta, Delta)[0]
    print(f"  k->0:  paper={R0_paper:+.6f}  mine={R0_num:+.6f}  diff={R0_num-R0_paper:+.2e}")
    print(f"  k->pi: paper={Rpi_paper:+.6f}  mine={Rpi_num:+.6f}  diff={Rpi_num-Rpi_paper:+.2e}")


def shift_vector_numerical(k_arr, t, delta, Delta):
    """Numerical shift vector from eigenvectors (fallback / check).

    R_cv(k) = d(phi_cv)/dk + A_cc - A_vv
    where A_nn = i <u_n|d/dk u_n> (Berry connection, smooth gauge)
    and phi_cv = arg <u_c | dH/dk * (factor) | u_v>
    But easier: use the definition with numerical overlap phases.

    Actually, use Eq. 3 directly with:
      A_cv = i <u_c | d_k u_v>   (complex)
      phi_cv = -arg(A_cv)        (matching definition A_nm = |A_nm| e^{-i phi_nm})
      R = d phi_cv/dk + A_cc - A_vv   (all real)

    Use finite differences on a DENSE k-mesh with smooth gauge.
    """
    E, U = eig_bands(k_arr, t, delta, Delta)
    N = len(k_arr)
    dk = k_arr[1] - k_arr[0]

    # Smooth gauge: align phase via max-overlap with previous k
    for i in range(1, N):
        for b in range(2):
            ov = np.vdot(U[i - 1, :, b], U[i, :, b])
            if abs(ov) > 1e-14:
                U[i, :, b] *= np.conj(ov) / abs(ov)

    # Berry connections via finite differences
    A_cc = np.zeros(N)
    A_vv = np.zeros(N)
    A_cv = np.zeros(N, dtype=complex)  # i <u_c | d_k u_v>
    for i in range(N):
        ip = (i + 1) % N
        im = (i - 1) % N
        dU_v = (U[ip, :, 0] - U[im, :, 0]) / (2 * dk)  # valence = band 0
        dU_c = (U[ip, :, 1] - U[im, :, 1]) / (2 * dk)  # conduction = band 1
        A_vv[i] = np.real(1j * np.vdot(U[i, :, 0], dU_v))
        A_cc[i] = np.real(1j * np.vdot(U[i, :, 1], dU_c))
        A_cv[i] = 1j * np.vdot(U[i, :, 1], dU_v)

    # phi_cv from A_cv: A_nm = |A_nm| e^{-i phi_nm}  =>  phi_nm = -arg(A_nm)
    phi = -np.angle(A_cv)
    # derivative of phi with unwrapping
    phi_unwrap = np.unwrap(phi)
    dphi = np.gradient(phi_unwrap, dk)

    R = dphi + A_cc - A_vv
    # Winding number
    W = (phi_unwrap[-1] - phi_unwrap[0]) / (2 * np.pi)
    return R, W, E, A_cc, A_vv


def compute_point(delta, t=1.0, Delta=0.5, N=4001):
    """For a given delta, compute P_c, P_v, Rbar_cv (mean of R_cv),
    and winding W. Returns dict."""
    # k in [-pi, pi), uniform grid; do NOT include endpoint to avoid double count
    k = np.linspace(-np.pi, np.pi, N, endpoint=False)
    E, U = eig_bands(k, t, delta, Delta)
    V = np.diag([1.0, -1.0]).astype(complex)  # sewing matrix for periodic gauge
    P_v = berry_phase_polarization(U[:, :, 0], sewing=V)
    P_c = berry_phase_polarization(U[:, :, 1], sewing=V)

    # Shift vector - analytic formula
    R_anal = shift_vector_2band(k, t, delta, Delta)
    Rbar_anal = np.mean(R_anal)  # = (1/2pi) integral, with dk=2pi/N

    # numerical (for winding number, A_nn, and sanity)
    R_num, W, _, A_cc_num, A_vv_num = shift_vector_numerical(k, t, delta, Delta)
    Rbar_num = np.mean(R_num)
    # Polarization from ANALYTIC Berry connection (paper Eq. D4), integrated
    # numerically. In paper's gauge: A_vv = t*delta*(E+Delta)/(4*E*(E^2-Delta^2)),
    # A_cc = t*delta*(E-Delta)/(4*E*(E^2-Delta^2)). These are closed-form and
    # gauge-unique, avoiding KSV-vs-paper gauge mismatches.
    Ek = np.sqrt(t**2*np.cos(k/2)**2 + delta**2*np.sin(k/2)**2 + Delta**2)
    A_vv_anal = t*delta*(Ek + Delta) / (4*Ek*(Ek**2 - Delta**2))
    A_cc_anal = t*delta*(Ek - Delta) / (4*Ek*(Ek**2 - Delta**2))
    P_v_int = np.mean(A_vv_anal)
    P_c_int = np.mean(A_cc_anal)

    return dict(
        delta=delta,
        Pv=P_v, Pc=P_c, dP=P_c - P_v,  # KSV
        Pv_int=P_v_int, Pc_int=P_c_int, dP_int=P_c_int - P_v_int,  # direct integral
        Rbar_anal=Rbar_anal,
        Rbar_num=Rbar_num,
        W=W,
    )


def main():
    t = 1.0
    Delta = 0.5
    N = 4001
    print("--- Analytic limit checks (Eq. D8, D9) ---")
    for dval in [0.3, 0.7, -0.4]:
        print(f"delta={dval}, Delta={Delta}, t={t}")
        check_analytic_limits(t=t, delta=dval, Delta=Delta)
    # Avoid a neighborhood of delta=0 where the gap closes and R has a pole.
    deltas_pos = np.linspace(0.04, 1.0, 50)
    deltas = np.concatenate([-deltas_pos[::-1], deltas_pos])

    Pv_arr = np.zeros_like(deltas)
    Pc_arr = np.zeros_like(deltas)
    dP_arr = np.zeros_like(deltas)
    dP_int_arr = np.zeros_like(deltas)
    R_arr = np.zeros_like(deltas)
    Rn_arr = np.zeros_like(deltas)
    W_arr = np.zeros_like(deltas)

    for i, d in enumerate(deltas):
        res = compute_point(d, t=t, Delta=Delta, N=N)
        Pv_arr[i] = res["Pv_int"]
        Pc_arr[i] = res["Pc_int"]
        dP_arr[i] = res["dP"]       # KSV (wrapped)
        dP_int_arr[i] = res["dP_int"]  # direct integral of A (smooth)
        R_arr[i] = res["Rbar_anal"]
        Rn_arr[i] = res["Rbar_num"]
        W_arr[i] = res["W"]

    # Unwrap dP across the jump at delta=0 so we can directly compare to Rbar
    # The paper's identity: e * Rbar_cv = a*(P_c - P_v) + W_cv * e*a
    # With e=a=1: Rbar = dP + W. Choose principal branch for dP from KSV,
    # then Rbar - dP should be an integer (=W).
    resid = R_arr - dP_int_arr
    # Round to integer to get W from the identity check
    W_identity = np.round(resid)

    # Save data
    import os
    outdir = os.path.dirname(os.path.abspath(__file__))
    np.savez(os.path.join(outdir, "..", "figures", "rice_mele_data.npz"),
             deltas=deltas, Pv=Pv_arr, Pc=Pc_arr, dP=dP_arr,
             Rbar_anal=R_arr, Rbar_num=Rn_arr, W_num=W_arr,
             W_identity=W_identity, t=t, Delta=Delta, N=N)

    # --- Figure 1(b) replica ---
    fig, ax = plt.subplots(1, 1, figsize=(6.5, 4.5))
    mask_neg = deltas < 0
    mask_pos = deltas > 0
    ax.plot(deltas[mask_neg], dP_int_arr[mask_neg], 'C0-', lw=2,
            label=r'$a(P_c - P_v)$ (Berry connection, paper Eq. D4)')
    ax.plot(deltas[mask_pos], dP_int_arr[mask_pos], 'C0-', lw=2)
    ax.plot(deltas[mask_neg], R_arr[mask_neg], 'C1--', lw=1.6, alpha=0.9,
            label=r'$e\bar{R}_{cv}$ (d-vector, W=0 branch)')
    ax.plot(deltas[mask_pos], R_arr[mask_pos], 'C1--', lw=1.6, alpha=0.9)
    ax.plot(deltas[mask_neg], Rn_arr[mask_neg], 'C2:', lw=1.8,
            label=r'$e\bar{R}_{cv}$ (numerical, full with $W_{cv}\cdot ea$)')
    ax.plot(deltas[mask_pos], Rn_arr[mask_pos], 'C2:', lw=1.8)
    ax.axhline(0, color='k', lw=0.5)
    ax.axvline(0, color='gray', lw=0.5, ls='--')
    ax.set_xlabel(r'$\delta/t$')
    ax.set_ylabel(r'units of $ea$')
    ax.set_ylim(-1.7, 1.7)
    ax.set_title(rf'Rice–Mele: Fig. 1(b) replica ($\Delta/t={Delta}$, $N_k={N}$)')
    ax.legend(loc='best', fontsize=9)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(outdir, "..", "figures", "fig1b_rice_mele.pdf"))
    fig.savefig(os.path.join(outdir, "..", "figures", "fig1b_rice_mele.png"), dpi=150)

    # --- Identity check figure: Rbar - dP should be integer W ---
    fig2, ax2 = plt.subplots(1, 1, figsize=(6, 4.2))
    ax2.plot(deltas, resid, 'o-', ms=3, lw=1, label=r'$e\bar{R}_{cv} - a(P_c-P_v)$')
    ax2.plot(deltas, W_identity, 'k--', label='rounded integer')
    ax2.set_xlabel(r'$\delta/t$')
    ax2.set_ylabel('residual (should = integer $W_{cv}$)')
    ax2.set_title(r'Identity check: $e\bar{R}_{cv} = a(P_c-P_v) + W_{cv}\,ea$')
    ax2.legend()
    ax2.grid(alpha=0.3)
    fig2.tight_layout()
    fig2.savefig(os.path.join(outdir, "..", "figures", "identity_check.pdf"))
    fig2.savefig(os.path.join(outdir, "..", "figures", "identity_check.png"), dpi=150)

    # --- Band structure at representative delta ---
    k_plot = np.linspace(-np.pi, np.pi, 801)
    fig3, ax3 = plt.subplots(1, 1, figsize=(5, 3.5))
    for dval in [0.3, 0.7]:
        E_plot, _ = eig_bands(k_plot, t, dval, Delta)
        ax3.plot(k_plot / np.pi, E_plot[:, 0], label=rf'$\delta={dval}$, valence')
        ax3.plot(k_plot / np.pi, E_plot[:, 1], label=rf'$\delta={dval}$, conduction')
    ax3.set_xlabel(r'$ka/\pi$')
    ax3.set_ylabel('E/t')
    ax3.set_title(rf'Rice–Mele bands ($\Delta/t={Delta}$)')
    ax3.legend(fontsize=8)
    ax3.grid(alpha=0.3)
    fig3.tight_layout()
    fig3.savefig(os.path.join(outdir, "..", "figures", "bands.pdf"))
    fig3.savefig(os.path.join(outdir, "..", "figures", "bands.png"), dpi=150)

    # Print summary stats
    mask_pos = deltas > 0.05
    mask_neg = deltas < -0.05
    print(f"=== Rice-Mele replication summary (Delta/t={Delta}) ===")
    print(f"N_k = {N}, N_delta = {len(deltas)}")
    print(f"delta > 0: mean(Rbar - dP) = {np.mean(resid[mask_pos]):+.6f}"
          f"  (expect integer, likely 0)")
    print(f"delta < 0: mean(Rbar - dP) = {np.mean(resid[mask_neg]):+.6f}"
          f"  (expect integer, likely -1 or +1)")
    print(f"|Rbar_anal - Rbar_num| max = {np.max(np.abs(R_arr - Rn_arr)):.3e}")
    print(f"W_num (endpoints of numerical phi): min={W_arr.min()}, "
          f"max={W_arr.max()}, mean={W_arr.mean():+.3f}")
    # Check identity to integer
    err = np.max(np.abs(resid - W_identity))
    print(f"Max |resid - round(resid)| = {err:.3e}  "
          f"(identity Eq.9 holds ↔ ~ 0)")


if __name__ == "__main__":
    main()
