"""
GSM² stochastic model + system-size expansion implementation.

Replicates: Cordoni F.G., "On the Emergence of the Deviation from a Poisson Law
in Stochastic Mathematical Models for Radiation-Induced DNA Damage: A System
Size Expansion", Entropy 25 (2023) 1322. DOI 10.3390/e25091322.

Three layers, all driven by the same (r, a, b_tilde, x0, y0) parameters:

1. `gillespie_ssa`  — exact stochastic-simulation algorithm for the GSM² CTMC
   with reactions
        X -> ∅          rate r * X
        X -> Y          rate a * X
        2X -> Y         rate b_tilde * X * (X - 1)
   where b_tilde = b/K (the K-rescaled clustering rate of Eq. 6).

2. `macro_ode`     — deterministic macroscopic limit (Eq. 11 of the paper):
        dx/dt = -(a+r) x - 2 b x^2
        dy/dt =  a x   +     b x^2
   (we use b == b_tilde here, since x is the *actual* lesion count and the
   simulation lives at one fixed K so the K-rescaling is absorbed).

3. `moment_ode`    — linear-noise covariance ODEs (Eq. 16 of the paper):
        d c_vv  /dt =  2 (2 b x + a) c_xi_v + a x + b x^2
        d c_xi_v/dt = (2 b x + a) c_xi_xi - (4 b x + a + r) c_xi_v
                      - (2 b x^2 + a x)
        d c_xi_xi/dt = -2 (4 b x + a + r) c_xi_xi + (a + r) x + 4 b x^2

4. `time_dep_ou`   — sample paths of the Ornstein–Uhlenbeck process of
   Remark 3, equations (22), using Euler–Maruyama.

Author: Ollie (subagent), 2026-05-29.
"""

from __future__ import annotations

import numpy as np
from scipy.integrate import solve_ivp


# ---------------------------------------------------------------------------
# 1.  Exact Gillespie SSA for the GSM² CTMC
# ---------------------------------------------------------------------------

def gillespie_ssa(
    *,
    x0: int,
    y0: int,
    r: float,
    a: float,
    b_tilde: float,
    t_max: float,
    rng: np.random.Generator | None = None,
    record_times: np.ndarray | None = None,
):
    """Run one realization of the GSM² CTMC to t_max.

    Returns (times_recorded, X_recorded, Y_recorded) sampled on
    `record_times` if provided, otherwise the full jump trajectory.
    """
    if rng is None:
        rng = np.random.default_rng()

    t = 0.0
    X = int(x0)
    Y = int(y0)

    if record_times is not None:
        record_times = np.asarray(record_times)
        Xrec = np.empty_like(record_times, dtype=np.int64)
        Yrec = np.empty_like(record_times, dtype=np.int64)
        next_idx = 0
        n_rec = record_times.size

        # If t = 0 is in record_times, emit it
        while next_idx < n_rec and record_times[next_idx] <= t:
            Xrec[next_idx] = X
            Yrec[next_idx] = Y
            next_idx += 1

        while next_idx < n_rec:
            if X == 0:
                # nothing more can happen; freeze remaining records
                while next_idx < n_rec:
                    Xrec[next_idx] = X
                    Yrec[next_idx] = Y
                    next_idx += 1
                break

            a1 = r * X                       # X -> 0
            a2 = a * X                       # X -> Y
            a3 = b_tilde * X * (X - 1)       # 2X -> Y
            a_tot = a1 + a2 + a3
            if a_tot <= 0.0:
                while next_idx < n_rec:
                    Xrec[next_idx] = X
                    Yrec[next_idx] = Y
                    next_idx += 1
                break

            dt = rng.exponential(1.0 / a_tot)
            t_new = t + dt

            # Emit all record times in [t, t_new) at the *old* state
            while next_idx < n_rec and record_times[next_idx] < t_new:
                Xrec[next_idx] = X
                Yrec[next_idx] = Y
                next_idx += 1

            if next_idx >= n_rec:
                break

            t = t_new
            u = rng.uniform() * a_tot
            if u < a1:
                X -= 1
            elif u < a1 + a2:
                X -= 1
                Y += 1
            else:
                # 2X -> Y :  two sub-lethal lesions cluster into one lethal
                X -= 2
                Y += 1

        return record_times, Xrec, Yrec

    # full trajectory
    ts, Xs, Ys = [t], [X], [Y]
    while t < t_max and X > 0:
        a1 = r * X
        a2 = a * X
        a3 = b_tilde * X * (X - 1)
        a_tot = a1 + a2 + a3
        if a_tot <= 0.0:
            break
        dt = rng.exponential(1.0 / a_tot)
        t += dt
        if t > t_max:
            ts.append(t_max)
            Xs.append(X)
            Ys.append(Y)
            break
        u = rng.uniform() * a_tot
        if u < a1:
            X -= 1
        elif u < a1 + a2:
            X -= 1
            Y += 1
        else:
            X -= 2
            Y += 1
        ts.append(t)
        Xs.append(X)
        Ys.append(Y)
    return np.asarray(ts), np.asarray(Xs), np.asarray(Ys)


# ---------------------------------------------------------------------------
# 2.  Deterministic macroscopic ODE (Eq. 11)
# ---------------------------------------------------------------------------

def macro_ode(*, x0: float, y0: float, r: float, a: float, b: float,
              t_eval: np.ndarray):
    """Integrate the macroscopic limit of GSM² (Eq. 11).

    dx/dt = -(a + r) x - 2 b x^2
    dy/dt = a x + b x^2
    """
    def rhs(t, z):
        x, y = z
        dx = -(a + r) * x - 2.0 * b * x * x
        dy = a * x + b * x * x
        return [dx, dy]

    sol = solve_ivp(rhs, (t_eval[0], t_eval[-1]), [x0, y0],
                    t_eval=t_eval, rtol=1e-10, atol=1e-12,
                    method="LSODA")
    return sol.t, sol.y[0], sol.y[1]


# ---------------------------------------------------------------------------
# 3.  Moment ODEs (Eq. 16) — sub-lethal-driven fluctuations
# ---------------------------------------------------------------------------

def moment_ode(*, x0: float, y0: float, r: float, a: float, b: float,
               t_eval: np.ndarray,
               c_init: tuple[float, float, float] = (0.0, 0.0, 0.0)):
    """Integrate (x, y, c_vv, c_xi_v, c_xi_xi) jointly.

    The mean fields (x, y) are propagated alongside so the time-dependent
    drift terms 2bx+a, 4bx+a+r are evaluated consistently.

    c_init : initial (c_vv, c_xi_v, c_xi_xi); paper uses (0,0,0) for the
             deterministic-initial-condition case (Sec. 3.2) and (y0, 0, x0)
             for the Gaussian-initial-condition case (Eq. 21).
    """
    cvv0, cxv0, cxx0 = c_init

    def rhs(t, z):
        x, y, cvv, cxv, cxx = z
        dx = -(a + r) * x - 2.0 * b * x * x
        dy = a * x + b * x * x
        dcvv = 2.0 * (2.0 * b * x + a) * cxv + a * x + b * x * x
        dcxv = ((2.0 * b * x + a) * cxx
                - (4.0 * b * x + a + r) * cxv
                - (2.0 * b * x * x + a * x))
        dcxx = (-2.0 * (4.0 * b * x + a + r) * cxx
                + (a + r) * x + 4.0 * b * x * x)
        return [dx, dy, dcvv, dcxv, dcxx]

    sol = solve_ivp(rhs, (t_eval[0], t_eval[-1]),
                    [x0, y0, cvv0, cxv0, cxx0],
                    t_eval=t_eval, rtol=1e-10, atol=1e-12,
                    method="LSODA")
    return {
        "t": sol.t,
        "x": sol.y[0],
        "y": sol.y[1],
        "c_vv": sol.y[2],
        "c_xi_v": sol.y[3],
        "c_xi_xi": sol.y[4],
    }


# ---------------------------------------------------------------------------
# 4.  Time-dependent OU process for sample paths (Remark 3 / Eq. 22)
# ---------------------------------------------------------------------------

def time_dep_ou_paths(
    *,
    x0: float,
    y0: float,
    r: float,
    a: float,
    b: float,
    t_eval: np.ndarray,
    n_paths: int,
    rng: np.random.Generator | None = None,
):
    """Simulate n_paths sample paths of (Y(t), X(t)) from the linear-noise OU
    process (Eq. 22) using Euler–Maruyama on a fine grid.

    Returns dict with arrays of shape (n_paths, len(t_eval)) for X and Y.
    Mean field is pre-computed once.
    """
    if rng is None:
        rng = np.random.default_rng()

    t = np.asarray(t_eval)
    n = t.size

    # Mean field on a fine sub-grid for accuracy
    n_sub = max(20, n)
    t_fine = np.linspace(t[0], t[-1], n_sub * 10)
    _, xbar, ybar = macro_ode(x0=x0, y0=y0, r=r, a=a, b=b, t_eval=t_fine)

    # Pre-interpolated for the Euler steps
    def xbar_at(tt):
        return np.interp(tt, t_fine, xbar)
    def ybar_at(tt):
        return np.interp(tt, t_fine, ybar)

    # SDE drift matrix A(t) and diffusion Q(t) per Remark 3
    # state Z = (v, xi).
    # A = [[0, -(2 b x + a)], [0, 4 b x + a + r]]
    # Q is given in the paper; we use the full diffusion matrix
    # built from the FPE coefficients:
    #     D_xx = (a + r) x + 4 b x^2
    #     D_vv = a x + b x^2
    #     D_xv = -(2 b x^2 + a x)
    # and Q = chol(D).  Note this matches the form in the paper after
    # symmetric square-rooting of D.
    paths_v = np.zeros((n_paths, n))
    paths_xi = np.zeros((n_paths, n))

    # Initial fluctuations: deterministic-initial-condition case → zero.
    v = np.zeros(n_paths)
    xi = np.zeros(n_paths)
    paths_v[:, 0] = v
    paths_xi[:, 0] = xi

    dt = t_fine[1] - t_fine[0]
    # For each fine step, advance the SDE; sample on t_eval indices
    idx_map = np.searchsorted(t_fine, t)

    for k in range(1, t_fine.size):
        tk = t_fine[k - 1]
        x_t = xbar_at(tk)

        # Build diffusion (positive-semi-definite)
        D_xx = max((a + r) * x_t + 4.0 * b * x_t * x_t, 0.0)
        D_vv = max(a * x_t + b * x_t * x_t, 0.0)
        D_xv = -(2.0 * b * x_t * x_t + a * x_t)

        # 2x2 PSD lower-triangular Cholesky
        L00 = np.sqrt(D_vv) if D_vv > 0 else 0.0
        if L00 > 0:
            L10 = D_xv / L00
        else:
            L10 = 0.0
        L11_sq = D_xx - L10 * L10
        L11 = np.sqrt(max(L11_sq, 0.0))

        # drift
        # dv = (2 b x + a) xi dt
        # dxi = -(4 b x + a + r) xi dt
        drift_v = (2.0 * b * x_t + a) * xi
        drift_xi = -(4.0 * b * x_t + a + r) * xi

        z1 = rng.standard_normal(n_paths)
        z2 = rng.standard_normal(n_paths)
        dW_v = z1 * np.sqrt(dt)
        dW_xi = z2 * np.sqrt(dt)

        v = v + drift_v * dt + L00 * dW_v
        xi = xi + drift_xi * dt + L10 * dW_v + L11 * dW_xi

        # If this fine step lands at one of our recorded times, store
        # We just snap after the whole loop; for efficiency, find indices that
        # equal k.
        mask = (idx_map == k)
        if np.any(mask):
            for j in np.where(mask)[0]:
                paths_v[:, j] = v
                paths_xi[:, j] = xi

    # Convert fluctuations back to (X, Y) using K=1 convention
    # (so that the OU process is in the same units as the SSA counts).
    # Per Eq. 7,  X = K xbar + sqrt(K) xi.  With K=1, X = xbar + xi.
    X_paths = xbar_at(t) + paths_xi
    Y_paths = ybar_at(t) + paths_v

    return {
        "t": t,
        "X": X_paths,
        "Y": Y_paths,
        "v": paths_v,
        "xi": paths_xi,
        "xbar": xbar_at(t),
        "ybar": ybar_at(t),
    }


# ---------------------------------------------------------------------------
# 5.  Convenience: ensemble of SSA realizations recorded on a fixed grid
# ---------------------------------------------------------------------------

def ssa_ensemble(
    *,
    x0: int,
    y0: int,
    r: float,
    a: float,
    b_tilde: float,
    t_eval: np.ndarray,
    n_paths: int,
    seed: int = 1,
):
    """Run n_paths Gillespie realizations, recorded on t_eval.

    Returns dict with arrays X (n_paths, n_t) and Y (n_paths, n_t) of ints.
    """
    rng = np.random.default_rng(seed)
    n_t = t_eval.size
    X = np.empty((n_paths, n_t), dtype=np.int64)
    Y = np.empty((n_paths, n_t), dtype=np.int64)
    for p in range(n_paths):
        # independent stream per path
        sub_rng = np.random.default_rng(rng.integers(0, 2**63 - 1))
        _, Xp, Yp = gillespie_ssa(
            x0=x0, y0=y0, r=r, a=a, b_tilde=b_tilde,
            t_max=t_eval[-1] + 1e-9,
            rng=sub_rng,
            record_times=t_eval,
        )
        X[p] = Xp
        Y[p] = Yp
    return {"t": t_eval, "X": X, "Y": Y}


# Default parameter set used in the paper's Fig. 1–3
PAPER_PARAMS = dict(
    x0=100,
    y0=0,
    r=4.0,
    a=0.1,
    b_tilde=0.01,
)
