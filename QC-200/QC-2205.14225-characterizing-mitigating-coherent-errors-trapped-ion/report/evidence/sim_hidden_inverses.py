#!/usr/bin/env python3
"""
Independent replication (numpy statevector/density-matrix) of
Majumder et al., arXiv:2205.14225, "Characterizing and mitigating coherent errors
in a trapped ion quantum processor using hidden inverses" (Quantum, 2023).

We reproduce the CORE analytical claim of the paper: the Hidden-Inverses (HI)
protocol cancels coherent over-rotation errors by structural symmetry, not by
adding gates. We check:

  (R1) Hadamard HI: standard decomposition H = Y(-pi/2) . X(pi) vs Hermitian-
       conjugate H^dagger = X(-pi) . Y(pi/2). Under the paper's Eq. (1) noise
       model with over-rotation epsilon, we form the identity operation
       H . X(Theta) . Z(Phi) . H^dagger and check that swapping the second
       H for H^dagger (i.e. the "hidden inverse" trick) reduces the leading
       coherent-error term in fidelity.

  (R2) Repeated block: [H . X(Theta) . Z(Phi) . H^dagger]^N with N=100 (paper's
       Fig 5 characterization circuit). We show the population phase space
       depends on {Theta, Phi, epsilon, phi, delta} exactly as Eq. (1)
       predicts and that a curve-fit recovers epsilon, phi, delta with
       variance ~10^-4 (paper's stated fit variance).

  (R3) Order-of-suppression comparison. For a bare pi-rotation with over-
       rotation epsilon vs the HI-equivalent (X(pi) followed by X(-pi))
       we scan epsilon in [-0.1, 0.1] and compute 1-F. HI structurally
       cancels the coherent piece and 1-F drops from O(epsilon^2) to
       O(epsilon^4) or better (the paper argues an analogous cancellation
       for H and CNOT).

  (R4) MS-gate simulation: 2-qubit MS(pi/2) with static over-rotation
       eps=0.09 rad + depolarizing p2q=0.02 -> reproduce ~97.5% MS fidelity
       claimed in the paper. Then eps=0.12, p2q=0.06 -> ~89%.

Author: replication run 2026-07-05
"""
import numpy as np
from scipy.optimize import curve_fit
import json, sys, time

RNG = np.random.default_rng(20260705)

# --------------------------------------------------------------------------
# Single-qubit operators
# --------------------------------------------------------------------------
I2 = np.eye(2, dtype=complex)
X  = np.array([[0,1],[1,0]], dtype=complex)
Y  = np.array([[0,-1j],[1j,0]], dtype=complex)
Z  = np.array([[1,0],[0,-1]], dtype=complex)

def expm_2x2(A):
    """Matrix exp for a 2x2 hermitian-times-i argument (small; use eig)."""
    w, V = np.linalg.eigh(1j*(A - A.conj().T)*(-0.5j))  # unused fallback
    # Just use scipy-free Pade approx via eig on -iA if A is skew-hermitian.
    # Simpler: use general series for our small case.
    return _expm_generic(A)

def _expm_generic(A, order=30):
    """Scaling-and-squaring style expm for small 2x2 matrices."""
    # Simple Taylor with scaling
    norm = np.linalg.norm(A, 2)
    s = max(0, int(np.ceil(np.log2(max(norm, 1.0)))))
    A_scaled = A / (2**s)
    result = np.eye(A.shape[0], dtype=complex)
    term = np.eye(A.shape[0], dtype=complex)
    for k in range(1, order+1):
        term = term @ A_scaled / k
        result = result + term
    for _ in range(s):
        result = result @ result
    return result

def X_noisy(theta, eps=0.0, phi=0.0, delta=0.0):
    """
    Eq. (1) noisy X(theta) rotation:
      X = exp[-i * (theta*(1+eps)/2) * (cos(phi)X + sin(phi)Y) - i*(delta*t/2)*Z]
    We treat delta*t = delta_arg (same units as theta) for simulation.
    """
    ang = 0.5 * theta * (1.0 + eps)
    H_gen = -1j * (ang * (np.cos(phi)*X + np.sin(phi)*Y) + 0.5*delta*Z)
    return _expm_generic(H_gen)

def Y_noisy(theta, eps=0.0, phi=0.0, delta=0.0):
    """
    Eq. (1) noisy Y(theta):
      Y = exp[-i * (theta*(1+eps)/2) * (cos(phi)Y + sin(phi)X) - i*(delta*t/2)*Z]
    """
    ang = 0.5 * theta * (1.0 + eps)
    H_gen = -1j * (ang * (np.cos(phi)*Y + np.sin(phi)*X) + 0.5*delta*Z)
    return _expm_generic(H_gen)

def Z_ideal(phi):
    return np.array([[np.exp(-1j*phi/2), 0],
                     [0,                  np.exp( 1j*phi/2)]], dtype=complex)

# --------------------------------------------------------------------------
# Hadamard decompositions (paper Fig 1)
# --------------------------------------------------------------------------
def H_standard(eps=0.0, phi=0.0, delta=0.0):
    """H = Y(-pi/2) * X(pi)    (native trapped-ion decomposition)."""
    return Y_noisy(-np.pi/2, eps, phi, delta) @ X_noisy(np.pi, eps, phi, delta)

def H_hidden(eps=0.0, phi=0.0, delta=0.0):
    """H_dagger = X(-pi) * Y(pi/2)  -- the 'hidden inverse' of H."""
    return X_noisy(-np.pi, eps, phi, delta) @ Y_noisy(np.pi/2, eps, phi, delta)

def fidelity_states(psi, phi):
    return float(np.abs(np.vdot(psi, phi))**2)

def fidelity_unitary(U, V, d=2):
    """Average gate fidelity between U and V."""
    tr = np.trace(U.conj().T @ V)
    return float((np.abs(tr)**2 + d) / (d*(d+1)))

# --------------------------------------------------------------------------
# (R1)+(R3) Over-rotation suppression: standard vs hidden inverse
# --------------------------------------------------------------------------
def suppression_scan(eps_list):
    """
    Compare bare vs hidden-inverse over-rotation suppression.
    Circuit: H . X(Theta) . Z(Phi) . H'   where H' is either H (bare, reuses
    same-direction rotation, so coherent errors ADD) or H^dagger (HI, errors
    partially CANCEL).
    Fix Theta=pi/4, Phi=0 for the scan (nontrivial rotation content).
    """
    Theta, Phi = np.pi/4, 0.0
    out = []
    for eps in eps_list:
        # Ideal target: H . X(Theta) . Z(Phi) . H  (with no noise)
        H_id = H_standard(0,0,0)
        U_ideal = H_id @ X_noisy(Theta,0,0,0) @ Z_ideal(Phi) @ H_id

        # Bare (no HI): both wrappers are H_standard with noise
        H_n = H_standard(eps,0,0)
        U_bare = H_n @ X_noisy(Theta,eps,0,0) @ Z_ideal(Phi) @ H_n

        # Hidden Inverse: second wrapper is H_hidden (H^dagger form)
        H_hi = H_hidden(eps,0,0)
        U_hi = H_hi @ X_noisy(Theta,eps,0,0) @ Z_ideal(Phi) @ H_standard(eps,0,0)

        F_bare = fidelity_unitary(U_bare, U_ideal)
        F_hi   = fidelity_unitary(U_hi,   U_ideal)
        out.append({"eps": float(eps),
                    "infid_bare": float(1-F_bare),
                    "infid_hi":   float(1-F_hi)})
    return out

# --------------------------------------------------------------------------
# (R2) Full 100-repetition characterization circuit + fit
# --------------------------------------------------------------------------
def pop0_after_repeated_block(Theta, Phi, eps, phi, delta, N=100):
    """
    Population of |0> after [H . X(Theta) . Z(Phi) . H^dagger]^N on |0>.
    """
    block = H_hidden(eps, phi, delta) @ X_noisy(Theta, eps, phi, delta) @ \
            Z_ideal(Phi) @ H_standard(eps, phi, delta)
    # Fast: eig-diagonalize block once and raise to N
    w, V = np.linalg.eig(block)
    block_N = V @ np.diag(w**N) @ np.linalg.inv(V)
    psi = block_N @ np.array([1.0+0j, 0.0+0j])
    return float(np.abs(psi[0])**2)

def build_phase_space(Theta_grid, Phi_grid, eps, phi, delta, N=100):
    P = np.zeros((len(Theta_grid), len(Phi_grid)))
    for i, T in enumerate(Theta_grid):
        for j, F in enumerate(Phi_grid):
            P[i,j] = pop0_after_repeated_block(T, F, eps, phi, delta, N)
    return P

def fit_noise_params(Theta_grid, Phi_grid, P_meas, N=100):
    """
    Fit (eps, phi, delta) to observed P_meas over the (Theta, Phi) grid.
    Uses SciPy's non-linear least squares (curve_fit), exactly the tool
    named in the paper.
    """
    T_mesh, F_mesh = np.meshgrid(Theta_grid, Phi_grid, indexing='ij')
    xdata = np.vstack([T_mesh.ravel(), F_mesh.ravel()])
    ydata = P_meas.ravel()

    def model(xy, eps_p, phi_p, delta_p):
        T = xy[0]; F = xy[1]
        out = np.zeros_like(T)
        for k, (Tv, Fv) in enumerate(zip(T, F)):
            out[k] = pop0_after_repeated_block(Tv, Fv, eps_p, phi_p, delta_p, N)
        return out

    p0 = [0.001, 0.001, 0.001]
    popt, pcov = curve_fit(model, xdata, ydata, p0=p0,
                           bounds=([-0.5,-0.5,-0.5],[0.5,0.5,0.5]),
                           maxfev=2000)
    perr = np.sqrt(np.diag(pcov))
    return popt, perr

# --------------------------------------------------------------------------
# (R4) MS gate with over-rotation + depolarizing noise (density matrix)
# --------------------------------------------------------------------------
def MS_noisy(theta, eps=0.0):
    """
    Molmer-Sorensen MS(theta) two-qubit gate = exp(-i * theta*(1+eps)/2 * XX)
    """
    XX = np.kron(X, X)
    ang = 0.5 * theta * (1.0 + eps)
    return _expm_generic(-1j * ang * XX)

def two_qubit_depol_channel(rho, p):
    """
    Two-qubit depolarizing channel with total error prob p:
       rho -> (1-p)*rho + p * I/4
    """
    d = 4
    return (1.0 - p)*rho + (p/d)*np.eye(d, dtype=complex)

def apply_unitary(rho, U):
    return U @ rho @ U.conj().T

def ms_fidelity(theta_ideal=np.pi/2, eps=0.09, p2q=0.02):
    """Average gate fidelity of noisy MS relative to ideal MS."""
    U_ideal = MS_noisy(theta_ideal, 0.0)
    U_noisy = MS_noisy(theta_ideal, eps)

    # average fidelity via Haar-average formula for a channel E:
    #   F_avg = (d*F_ent + 1) / (d+1),
    # where F_ent is entanglement fidelity between the ideal U and the channel.
    # For E(rho) = (1-p) U rho U^dag + p * I/4,
    #   F_ent = (1-p) |Tr(U_ideal^dag U_noisy)/d|^2 + p*(1/d^2)
    d = 4
    tr = np.trace(U_ideal.conj().T @ U_noisy) / d
    F_ent = (1.0 - p2q) * (np.abs(tr)**2) + p2q * (1.0 / (d*d))
    F_avg = (d*F_ent + 1.0) / (d + 1.0)
    return float(F_avg), float(F_ent)

# --------------------------------------------------------------------------
# MAIN
# --------------------------------------------------------------------------
def main():
    results = {}
    t0 = time.time()

    # ----- (R1)+(R3) over-rotation suppression -----
    eps_list = np.linspace(-0.1, 0.1, 21)
    scan = suppression_scan(eps_list)
    results["suppression_scan"] = scan
    # fit orders: log(1-F) vs log|eps|
    eps_pos = [s for s in scan if abs(s["eps"]) > 1e-3]
    def _order(key):
        xs = np.array([np.log(abs(s["eps"])) for s in eps_pos])
        ys = np.array([np.log(max(s[key], 1e-18)) for s in eps_pos])
        # linear fit slope = order
        slope, intercept = np.polyfit(xs, ys, 1)
        return float(slope)
    results["order_bare"] = _order("infid_bare")
    results["order_hi"]   = _order("infid_hi")
    print(f"[R1/R3] Over-rotation suppression order:")
    print(f"        bare  1-F ~ |eps|^{results['order_bare']:.2f}")
    print(f"        HI    1-F ~ |eps|^{results['order_hi']:.2f}")

    # ----- (R2) 100-block circuit + noise-model fit -----
    print(f"\n[R2] Building phase-space grid (11x11 * N=100 blocks)...")
    Tgrid = np.linspace(-0.08, 0.08, 11)   # matches Fig 5 axis scale
    Fgrid = np.linspace(-0.08, 0.08, 11)
    true_eps, true_phi, true_delta = 0.03, -0.02, 0.015
    P_meas = build_phase_space(Tgrid, Fgrid, true_eps, true_phi, true_delta, N=100)
    # add gentle shot-noise to mimic the experimental data quality
    P_meas_noisy = np.clip(P_meas + RNG.normal(0, 0.005, P_meas.shape), 0, 1)
    popt, perr = fit_noise_params(Tgrid, Fgrid, P_meas_noisy, N=100)
    print(f"      True (eps, phi, delta) = ({true_eps}, {true_phi}, {true_delta})")
    print(f"      Fit  (eps, phi, delta) = ({popt[0]:+.4f}, {popt[1]:+.4f}, {popt[2]:+.4f})")
    print(f"      Errs (1-sigma)         = ({perr[0]:.2e}, {perr[1]:.2e}, {perr[2]:.2e})")
    results["fit"] = {
        "true":   [true_eps, true_phi, true_delta],
        "fit":    [float(p) for p in popt],
        "sigma":  [float(e) for e in perr],
    }
    # paper claims variance ~1e-4; we compare
    max_sigma = float(max(perr))
    results["fit_max_sigma"] = max_sigma
    results["fit_paper_stated_sigma_order"] = 1e-4

    # ----- (R4) MS gate fidelity reproduction -----
    print(f"\n[R4] MS-gate fidelities (paper Sec 5.3):")
    for label, eps, p2q, tgt in [
        ("noiseless-best-fit (paper claims 97.5%)", 0.09, 0.02, 0.975),
        ("under-rotation 0.45 rad case  (paper claims ~91%)", 0.45, 0.02, 0.91),
        ("reduced cooling (paper claims ~89%)", 0.12, 0.06, 0.89),
    ]:
        F_avg, F_ent = ms_fidelity(np.pi/2, eps, p2q)
        # Paper's "MS gate fidelity" isn't unambiguously average vs entanglement;
        # report both so the reader can compare.
        print(f"      {label}: F_avg={F_avg:.3f}, F_ent={F_ent:.3f}  (target ~{tgt})")
        results.setdefault("MS", []).append(
            {"case": label, "eps": eps, "p2q": p2q, "target": tgt,
             "F_avg": F_avg, "F_ent": F_ent})

    t1 = time.time()
    results["runtime_seconds"] = round(t1-t0, 2)
    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nDone in {t1-t0:.1f}s.  Wrote results.json")

if __name__ == "__main__":
    main()
