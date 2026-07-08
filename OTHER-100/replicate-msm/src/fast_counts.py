"""
Fast count matrix computation using NumPy vectorization.
Replaces the triple-nested loop with histogram-based counting.
"""

import numpy as np


def count_stats_fast(trajs, assign, n_states, lag):
    """
    Compute s, S_tau, S2_tau using vectorized operations.
    
    Parameters
    ----------
    trajs : (n_traj, L) int array — microstate trajectories
    assign : (n_micro,) int array — microstate → MSM state mapping
    n_states : int
    lag : int
    
    Returns
    -------
    s, S_tau, S2 : count vector, count matrix, two-step count tensor
    """
    coarse = assign[trajs]  # (n_traj, L)
    n_traj, L = coarse.shape
    max_k = L - 2 * lag
    
    if max_k <= 0:
        raise ValueError(f"Trajectories too short for lag={lag}")
    
    s = np.zeros(n_states)
    S_tau = np.zeros((n_states, n_states))
    S2 = np.zeros((n_states, n_states, n_states))
    
    # Process in time-step chunks to avoid huge memory
    for k in range(max_k):
        i_col = coarse[:, k]          # (n_traj,)
        r_col = coarse[:, k + lag]    # (n_traj,)
        j_col = coarse[:, k + 2*lag]  # (n_traj,)
        
        # Count vector: histogram of i
        np.add.at(s, i_col, 1)
        
        # One-step count matrix: 2D histogram of (i, r)
        flat_ir = i_col * n_states + r_col
        counts_ir = np.bincount(flat_ir, minlength=n_states * n_states)
        S_tau += counts_ir.reshape(n_states, n_states)
        
        # Two-step count tensor: 3D histogram of (r, i, j)
        flat_rij = r_col * (n_states * n_states) + i_col * n_states + j_col
        counts_rij = np.bincount(flat_rij, minlength=n_states**3)
        S2 += counts_rij.reshape(n_states, n_states, n_states)
    
    return s, S_tau, S2


def direct_msm(S_tau, n_states, lag):
    """Estimate direct (uncorrected) MSM transition matrix and implied timescales."""
    from scipy import linalg
    
    T = np.zeros((n_states, n_states))
    for i in range(n_states):
        rs = S_tau[i].sum()
        if rs > 0:
            T[i] = S_tau[i] / rs
        else:
            T[i, i] = 1.0
    
    ev = np.sort(np.real(linalg.eigvals(T)))[::-1]
    timescales = []
    for k in range(1, min(4, len(ev))):
        if 0 < ev[k] < 1:
            timescales.append(-lag / np.log(ev[k]))
        else:
            timescales.append(np.inf)
    
    return T, ev, np.array(timescales)


def _oom_compute_at_M(s, S_tau, S2, U, sigma, Vt, n_states, lag, M):
    """
    Internal: compute OOM MSM at a fixed rank M.
    Returns T_corr, pi_corr, ev_oom, timescales.
    """
    from scipy import linalg

    M = min(M, len(sigma), n_states - 1)
    M = max(M, 2)

    sigma_inv_sqrt = np.diag(1.0 / np.sqrt(np.maximum(sigma[:M], 1e-10)))
    F1 = U[:, :M] @ sigma_inv_sqrt
    F2 = Vt[:M, :].T @ sigma_inv_sqrt

    Xi_hat = np.zeros((n_states, M, M))
    for r in range(n_states):
        Xi_hat[r] = F1.T @ S2[r] @ F2

    sigma_hat = F1.T @ s
    Xi_Omega = np.sum(Xi_hat, axis=0)

    eigenvalues_xi, eigvecs_xi = linalg.eig(Xi_Omega.T)
    idx_ev1 = np.argmin(np.abs(eigenvalues_xi - 1.0))
    omega_hat = np.real(eigvecs_xi[:, idx_ev1])
    denom = omega_hat @ sigma_hat
    if abs(denom) < 1e-12:
        raise ValueError("OOM: omega^T sigma ~ 0")
    omega_hat /= denom

    # Corrected correlations and stationary distribution
    C_eq = np.zeros((n_states, n_states))
    pi_corr = np.zeros(n_states)
    for i in range(n_states):
        pi_corr[i] = omega_hat @ Xi_hat[i] @ sigma_hat
        for j in range(n_states):
            C_eq[i, j] = omega_hat @ Xi_hat[i] @ Xi_hat[j] @ sigma_hat

    pi_corr = np.maximum(pi_corr, 0)
    if pi_corr.sum() > 0:
        pi_corr /= pi_corr.sum()

    T_corr = np.zeros((n_states, n_states))
    for i in range(n_states):
        rs = C_eq[i].sum()
        if rs > 0:
            T_corr[i] = np.maximum(C_eq[i], 0) / rs
        else:
            T_corr[i, i] = 1.0

    ev_oom = np.sort(np.real(linalg.eigvals(Xi_Omega)))[::-1]
    timescales = []
    for k in range(1, min(4, len(ev_oom))):
        if 0 < ev_oom[k] < 1:
            timescales.append(-lag / np.log(ev_oom[k]))
        else:
            timescales.append(np.inf)

    return T_corr, pi_corr, ev_oom, np.array(timescales)


def oom_msm(s, S_tau, S2, n_states, lag, M=None, M_max=38, snr_threshold=0.001,
            adaptive_search=True):
    """
    OOM-corrected MSM estimator (Nüske et al. 2017, Eqs. 44–55).

    Parameters
    ----------
    s       : (n_states,) initial-state count vector
    S_tau   : (n_states, n_states) one-step count matrix
    S2      : (n_states, n_states, n_states) two-step count tensor
    n_states: number of MSM states
    lag     : lag time in frames
    M       : fixed rank (if None, adaptive selection is used)
    M_max   : maximum rank to consider (default 38, per paper)
    snr_threshold : singular value threshold for initial rank estimate
                    (sigma_i / sigma_1 > threshold)
    adaptive_search : if True and M is None, search M values to maximise t2

    Returns
    -------
    T_corr, pi_corr, ev_oom, timescales, M_used
    """
    from scipy import linalg

    U, sigma, Vt = np.linalg.svd(S_tau, full_matrices=False)

    # ── Rank selection ──────────────────────────────────────────────────────
    if M is not None:
        # Fixed rank supplied by caller
        M_use = min(M, len(sigma), n_states - 1)
        T_c, pi_c, ev, ts = _oom_compute_at_M(s, S_tau, S2, U, sigma, Vt,
                                               n_states, lag, M_use)
        return T_c, pi_c, ev, ts, M_use

    # Determine initial M from singular-value threshold
    M_svd = int(np.sum(sigma > sigma[0] * snr_threshold))
    M_svd = max(2, min(M_svd, M_max, n_states - 1, len(sigma)))

    if not adaptive_search:
        T_c, pi_c, ev, ts = _oom_compute_at_M(s, S_tau, S2, U, sigma, Vt,
                                               n_states, lag, M_svd)
        return T_c, pi_c, ev, ts, M_svd

    # ── Adaptive search: try M in [M_lo, M_hi] and pick best t2 ────────────
    # Search from M_svd down to 5 and up to min(M_max, n_states-1)
    # ── Adaptive search: largest stable M ────────────────────────────────────
    # "Stable" means no second eigenvalue of Xi_Omega is spuriously near 1.0.
    # We scan M upward and stop when ev2 first reaches the instability ceiling.
    # This conservatively mirrors the bootstrap SNR criterion in the paper.
    ev_ceiling = 1.0 - 1e-3  # eigenvalue must be strictly below this

    M_lo = 5
    M_hi = min(M_max, n_states - 1, len(sigma))
    candidates = list(range(M_lo, M_hi + 1))

    best_result = None
    best_M = M_lo

    for m in candidates:
        try:
            T_c, pi_c, ev, ts = _oom_compute_at_M(s, S_tau, S2, U, sigma, Vt,
                                                    n_states, lag, m)
            # Check stability: second-largest eigenvalue must be real and < ceiling
            if len(ev) < 2:
                break
            ev2_r = float(np.real(ev[1]))
            if ev2_r >= ev_ceiling:
                # Numerical instability — stop here (don't accept this M)
                break
            if len(ts) > 0 and np.isfinite(ts[0]):
                best_result = (T_c, pi_c, ev, ts)
                best_M = m
        except Exception:
            pass

    if best_result is None:
        # Fallback: SVD-threshold M without adaptive search
        T_c, pi_c, ev, ts = _oom_compute_at_M(s, S_tau, S2, U, sigma, Vt,
                                               n_states, lag, M_svd)
        return T_c, pi_c, ev, ts, M_svd

    T_c, pi_c, ev, ts = best_result
    return T_c, pi_c, ev, ts, best_M
