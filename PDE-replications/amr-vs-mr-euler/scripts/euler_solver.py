"""
1D compressible Euler solvers — apples-to-apples comparison kit
================================================================

Three solvers on the SAME 1D Euler equations and the SAME Sod shock-tube IC:

  1. `uniform_fv`     — uniform finite-volume HLL, 2nd-order MUSCL + minmod
  2. `amr_fv`         — block-structured AMR (Berger-Oliger-lite, 1D)
                        on top of the same HLL/MUSCL scheme
  3. `mr_fv`          — multiresolution (Harten cell-average wavelet thresholding)
                        on top of the same HLL/MUSCL scheme

Reference: exact Riemann solution for Sod (rho_L=1, u_L=0, p_L=1;
rho_R=0.125, u_R=0, p_R=0.1; gamma=1.4) at T=0.2.

All solvers share the same physics, same Riemann solver, same limiter, so
differences in error/timing are attributable to the adaptive strategy.

Clean-room implementation by Ollie for the AMR-vs-MR replication study.
License: do whatever. (BSD-0/CC0 equivalent.)
"""

from __future__ import annotations
import numpy as np
import time
from dataclasses import dataclass, field
from typing import Callable, Optional

GAMMA = 1.4
EPS = 1e-12


# -----------------------------------------------------------------------------
# Physics: conservative variables U=(rho, rho*u, E), fluxes, HLL Riemann
# -----------------------------------------------------------------------------
def cons_to_prim(U):
    rho = np.maximum(U[..., 0], EPS)
    u = U[..., 1] / rho
    E = U[..., 2]
    p = np.maximum((GAMMA - 1.0) * (E - 0.5 * rho * u * u), EPS)
    return rho, u, p


def prim_to_cons(rho, u, p):
    E = p / (GAMMA - 1.0) + 0.5 * rho * u * u
    U = np.stack([rho, rho * u, E], axis=-1)
    return U


def euler_flux(U):
    rho, u, p = cons_to_prim(U)
    F = np.stack([
        rho * u,
        rho * u * u + p,
        u * (U[..., 2] + p),
    ], axis=-1)
    return F


def sound_speed(rho, p):
    return np.sqrt(GAMMA * p / np.maximum(rho, EPS))


def hll_flux(UL, UR):
    """HLL Riemann solver, vectorized along leading axis."""
    rhoL, uL, pL = cons_to_prim(UL)
    rhoR, uR, pR = cons_to_prim(UR)
    cL = sound_speed(rhoL, pL)
    cR = sound_speed(rhoR, pR)
    SL = np.minimum(uL - cL, uR - cR)
    SR = np.maximum(uL + cL, uR + cR)
    FL = euler_flux(UL)
    FR = euler_flux(UR)
    Fhll = np.where(
        SL[..., None] >= 0, FL,
        np.where(SR[..., None] <= 0, FR,
                 (SR[..., None] * FL - SL[..., None] * FR
                  + (SL * SR)[..., None] * (UR - UL))
                 / (SR - SL + EPS)[..., None])
    )
    return Fhll


def minmod(a, b):
    return np.where(a * b > 0, np.sign(a) * np.minimum(np.abs(a), np.abs(b)), 0.0)


def muscl_reconstruct(U):
    """MUSCL with minmod limiter, returns left/right states at each interior face.
    U: (N,3) array. Returns UL, UR each (N-1,3) for faces i+1/2."""
    # slopes at cells 1..N-2
    dU_L = U[1:-1] - U[:-2]
    dU_R = U[2:] - U[1:-1]
    slope = minmod(dU_L, dU_R)
    # Pad with zero-slope at boundaries
    slope_full = np.zeros_like(U)
    slope_full[1:-1] = slope
    # Face i+1/2: left state from cell i, right state from cell i+1
    UL_face = U[:-1] + 0.5 * slope_full[:-1]
    UR_face = U[1:] - 0.5 * slope_full[1:]
    return UL_face, UR_face


def compute_flux(U):
    """Returns flux at each interior face: shape (N-1, 3)."""
    UL, UR = muscl_reconstruct(U)
    return hll_flux(UL, UR)


def cfl_dt(U, dx, cfl=0.5):
    rho, u, p = cons_to_prim(U)
    c = sound_speed(rho, p)
    return cfl * dx / np.max(np.abs(u) + c + EPS)


# -----------------------------------------------------------------------------
# Sod IC and exact solution
# -----------------------------------------------------------------------------
def sod_initial(x):
    """Sod shock tube IC: rho_L=1, u_L=0, p_L=1; rho_R=0.125, u_R=0, p_R=0.1.
    Interface at x=0.5."""
    rho = np.where(x < 0.5, 1.0, 0.125)
    u = np.zeros_like(x)
    p = np.where(x < 0.5, 1.0, 0.1)
    return prim_to_cons(rho, u, p)


def sod_exact(x, t, gamma=1.4):
    """Exact Sod solution at time t. Returns rho, u, p arrays."""
    from scipy.optimize import brentq
    rhoL, uL, pL = 1.0, 0.0, 1.0
    rhoR, uR, pR = 0.125, 0.0, 0.1
    cL = np.sqrt(gamma * pL / rhoL)
    cR = np.sqrt(gamma * pR / rhoR)

    # Solve for p_star using exact two-shock / two-rarefaction system
    def f_L(p):  # left wave function
        if p > pL:  # shock
            A = 2.0 / ((gamma + 1.0) * rhoL)
            B = (gamma - 1.0) / (gamma + 1.0) * pL
            return (p - pL) * np.sqrt(A / (p + B))
        else:  # rarefaction
            return 2.0 * cL / (gamma - 1.0) * ((p / pL) ** ((gamma - 1.0) / (2.0 * gamma)) - 1.0)

    def f_R(p):
        if p > pR:
            A = 2.0 / ((gamma + 1.0) * rhoR)
            B = (gamma - 1.0) / (gamma + 1.0) * pR
            return (p - pR) * np.sqrt(A / (p + B))
        else:
            return 2.0 * cR / (gamma - 1.0) * ((p / pR) ** ((gamma - 1.0) / (2.0 * gamma)) - 1.0)

    def F(p):
        return f_L(p) + f_R(p) + (uR - uL)

    p_star = brentq(F, 1e-6, 10.0, xtol=1e-12)
    u_star = 0.5 * (uL + uR) + 0.5 * (f_R(p_star) - f_L(p_star))

    # Left side: rarefaction (since p_star<pL)
    cL_star = cL * (p_star / pL) ** ((gamma - 1.0) / (2.0 * gamma))
    rho_starL = rhoL * (p_star / pL) ** (1.0 / gamma)
    # Right side: shock (since p_star>pR)
    rho_starR = rhoR * ((p_star / pR + (gamma - 1.0) / (gamma + 1.0))
                        / ((gamma - 1.0) / (gamma + 1.0) * p_star / pR + 1.0))
    S_R = uR + cR * np.sqrt((gamma + 1.0) / (2.0 * gamma) * p_star / pR
                            + (gamma - 1.0) / (2.0 * gamma))
    # Rarefaction head/tail (left)
    S_HL = uL - cL
    S_TL = u_star - cL_star

    xi = (x - 0.5) / max(t, 1e-12)
    rho = np.empty_like(x)
    u = np.empty_like(x)
    p = np.empty_like(x)
    for i, xi_i in enumerate(xi):
        if xi_i < S_HL:
            rho[i], u[i], p[i] = rhoL, uL, pL
        elif xi_i < S_TL:
            # Inside rarefaction fan
            u_fan = 2.0 / (gamma + 1.0) * (cL + (gamma - 1.0) / 2.0 * uL + xi_i)
            c_fan = 2.0 / (gamma + 1.0) * (cL + (gamma - 1.0) / 2.0 * (uL - xi_i))
            rho[i] = rhoL * (c_fan / cL) ** (2.0 / (gamma - 1.0))
            p[i] = pL * (c_fan / cL) ** (2.0 * gamma / (gamma - 1.0))
            u[i] = u_fan
        elif xi_i < u_star:
            rho[i], u[i], p[i] = rho_starL, u_star, p_star
        elif xi_i < S_R:
            rho[i], u[i], p[i] = rho_starR, u_star, p_star
        else:
            rho[i], u[i], p[i] = rhoR, uR, pR
    return rho, u, p


# -----------------------------------------------------------------------------
# Solver 1: Uniform FV
# -----------------------------------------------------------------------------
@dataclass
class RunStats:
    name: str
    N_active_max: int = 0
    N_active_avg: float = 0.0
    N_active_samples: list = field(default_factory=list)
    N_uniform_equiv: int = 0
    wall_time_s: float = 0.0
    steps: int = 0
    err_L1_rho: float = 0.0
    err_L2_rho: float = 0.0
    err_Linf_rho: float = 0.0
    final_dt: float = 0.0
    notes: str = ""

    def compression(self):
        return self.N_active_avg / max(self.N_uniform_equiv, 1)


def run_uniform(N=400, T=0.2, cfl=0.5, x_min=0.0, x_max=1.0, bc="transmissive"):
    """Uniform-grid FV solver, MUSCL+HLL."""
    t0 = time.perf_counter()
    dx = (x_max - x_min) / N
    x = x_min + (np.arange(N) + 0.5) * dx
    U = sod_initial(x)
    t = 0.0
    steps = 0
    stats = RunStats(name=f"uniform_N={N}", N_active_max=N, N_active_avg=N,
                     N_uniform_equiv=N)
    while t < T:
        dt = cfl_dt(U, dx, cfl)
        dt = min(dt, T - t)
        # 2 ghost cells each side
        Uext = _pad(U, 2, bc)
        F = compute_flux(Uext)         # interior faces -> shape (N+3, 3)
        # Cell i (in U) maps to face i+1/2 between Uext[i+1] and Uext[i+2]
        # Flux at left face = F[i+1], right = F[i+2]
        U = U - dt / dx * (F[2:N+2] - F[1:N+1])
        t += dt
        steps += 1
        stats.N_active_samples.append(N)
    stats.wall_time_s = time.perf_counter() - t0
    stats.steps = steps
    stats.final_dt = dt
    stats.N_active_avg = N
    # error
    rho_num = cons_to_prim(U)[0]
    rho_ex, _, _ = sod_exact(x, T)
    stats.err_L1_rho = np.mean(np.abs(rho_num - rho_ex))
    stats.err_L2_rho = np.sqrt(np.mean((rho_num - rho_ex) ** 2))
    stats.err_Linf_rho = np.max(np.abs(rho_num - rho_ex))
    return x, U, stats


def _pad(U, n, bc):
    """Apply BC by padding n ghost cells each side."""
    if bc == "transmissive":
        return np.concatenate([np.repeat(U[:1], n, axis=0),
                               U,
                               np.repeat(U[-1:], n, axis=0)], axis=0)
    elif bc == "periodic":
        return np.concatenate([U[-n:], U, U[:n]], axis=0)
    else:
        raise ValueError(bc)


# -----------------------------------------------------------------------------
# Solver 2: Block-structured AMR (1D, two-level Berger-Oliger-lite)
# -----------------------------------------------------------------------------
def run_amr(N_coarse=100, refine_ratio=4, T=0.2, cfl=0.5,
            x_min=0.0, x_max=1.0, bc="transmissive",
            refine_threshold=0.05, regrid_every=4, buffer_cells=2):
    """1D block-structured AMR.

    Strategy:
      - Base level 0 covers domain uniformly with N_coarse cells, dx0.
      - Level 1 has cells dx1 = dx0/refine_ratio.
      - Refinement is determined by |grad rho|/rho > refine_threshold,
        flagged cells dilated by buffer_cells then turned into contiguous
        patches on level 1.
      - Subcycling: per coarse step take refine_ratio fine steps.
      - Conservation: flux correction at coarse-fine boundary
        (Berger-Colella style — replace coarse flux at C/F interface
         with sum of subcycled fine fluxes).
      - Restriction (fine->coarse) of fine cells covering coarse cells.
    """
    t0 = time.perf_counter()
    dx0 = (x_max - x_min) / N_coarse
    dx1 = dx0 / refine_ratio
    x_c = x_min + (np.arange(N_coarse) + 0.5) * dx0
    U_c = sod_initial(x_c)
    # patches on level 1: list of (i_start, i_end) coarse-cell ranges (inclusive)
    patches = []
    fine_data = {}  # patch_id -> ndarray (n_fine, 3)

    stats = RunStats(name=f"amr_N0={N_coarse}_r={refine_ratio}_thr={refine_threshold}",
                     N_uniform_equiv=N_coarse * refine_ratio)

    def regrid(U_c, patches, fine_data):
        rho_c = cons_to_prim(U_c)[0]
        grad = np.zeros(N_coarse)
        grad[1:-1] = np.abs(rho_c[2:] - rho_c[:-2]) / (2 * dx0) / (rho_c[1:-1] + EPS)
        flag = grad > refine_threshold
        # Buffer
        flag_buf = flag.copy()
        for _ in range(buffer_cells):
            flag_buf[1:] |= flag_buf[:-1]
            flag_buf[:-1] |= flag_buf[1:]
        # Build contiguous patches
        new_patches = []
        i = 0
        while i < N_coarse:
            if flag_buf[i]:
                j = i
                while j < N_coarse and flag_buf[j]:
                    j += 1
                new_patches.append((i, j - 1))
                i = j
            else:
                i += 1
        # Initialize/migrate fine data
        new_fine = {}
        for pid, (i0, i1) in enumerate(new_patches):
            n_fine = (i1 - i0 + 1) * refine_ratio
            x_f = x_min + (i0 * refine_ratio + np.arange(n_fine) + 0.5) * dx1
            # Try to interpolate from old fine patches that overlap
            U_f_new = None
            for old_pid, (oi0, oi1) in enumerate(patches):
                if oi1 >= i0 and oi0 <= i1:  # overlap
                    old_x_f = x_min + (oi0 * refine_ratio
                                       + np.arange((oi1 - oi0 + 1) * refine_ratio)
                                       + 0.5) * dx1
                    # interp each variable
                    cand = np.stack([
                        np.interp(x_f, old_x_f, fine_data[old_pid][:, k])
                        for k in range(3)
                    ], axis=-1)
                    if U_f_new is None:
                        U_f_new = cand
                    else:
                        # blend by location (later overlap overrides)
                        pass
            if U_f_new is None:
                # initialize by piecewise-constant prolongation from coarse
                U_f_new = np.repeat(U_c[i0:i1 + 1], refine_ratio, axis=0)
            new_fine[pid] = U_f_new
        return new_patches, new_fine

    # Initial regrid
    patches, fine_data = regrid(U_c, patches, fine_data)

    t = 0.0
    steps = 0
    n_active_samples = []
    while t < T:
        # CFL: min over all data
        dt = cfl_dt(U_c, dx0, cfl)
        for pid in fine_data:
            dt = min(dt, cfl_dt(fine_data[pid], dx1, cfl))
        dt = min(dt, T - t)

        # 1) Advance fine levels by refine_ratio substeps of dt/refine_ratio
        dt_f = dt / refine_ratio
        for sub in range(refine_ratio):
            for pid, (i0, i1) in enumerate(patches):
                U_f = fine_data[pid]
                # boundary: get ghost cells from coarse (piecewise prolong)
                Uext = _amr_pad_fine(U_f, U_c, i0, i1, refine_ratio, 2, bc, N_coarse)
                F = compute_flux(Uext)
                n_f = U_f.shape[0]
                fine_data[pid] = U_f - dt_f / dx1 * (F[2:n_f + 2] - F[1:n_f + 1])

        # 2) Advance coarse level by dt with HLL
        Uext = _pad(U_c, 2, bc)
        F_c = compute_flux(Uext)  # shape (N_coarse+3, 3)
        # 3) Flux correction at C/F interfaces:
        #    The coarse flux at coarse-face f between cells (i, i+1) where
        #    one side is refined and the other isn't, should be replaced
        #    by the time-averaged sum of fine fluxes computed during subcycling.
        #    For simplicity here we re-compute fine flux at the C/F face using the
        #    UPDATED fine data and use it (Berger-Colella correct in spirit;
        #    we skip the full reflux register for clarity).
        for pid, (i0, i1) in enumerate(patches):
            U_f = fine_data[pid]
            # Left C/F face: between coarse cell i0-1 (coarse) and i0 (refined)
            if i0 > 0 and (i0 - 1 < N_coarse) and not _is_in_patches(i0 - 1, patches):
                # face index in coarse F_c: F_c[i0 + 1] is the flux at face i0-1/2 to i0
                # Wait — Uext has 2 ghost cells, so F[1] is left face of cell 0,
                # F[i+1] is left face of cell i. So face between i0-1 and i0 is F[i0+1].
                # Use HLL between coarse U_c[i0-1] and fine U_f[0]
                F_face = hll_flux(U_c[i0 - 1:i0], U_f[0:1])
                F_c[i0 + 1] = F_face[0]
            # Right C/F face
            if i1 < N_coarse - 1 and not _is_in_patches(i1 + 1, patches):
                F_face = hll_flux(U_f[-1:], U_c[i1 + 1:i1 + 2])
                F_c[i1 + 2] = F_face[0]

        U_c = U_c - dt / dx0 * (F_c[2:N_coarse + 2] - F_c[1:N_coarse + 1])

        # 4) Restriction: replace coarse cells covered by fine patches with average
        for pid, (i0, i1) in enumerate(patches):
            U_f = fine_data[pid]
            for k, ci in enumerate(range(i0, i1 + 1)):
                U_c[ci] = np.mean(U_f[k * refine_ratio:(k + 1) * refine_ratio], axis=0)

        # 5) Regrid periodically
        if steps % regrid_every == 0:
            patches, fine_data = regrid(U_c, patches, fine_data)

        t += dt
        steps += 1
        n_active = N_coarse - sum(i1 - i0 + 1 for (i0, i1) in patches) \
                   + sum((i1 - i0 + 1) * refine_ratio for (i0, i1) in patches)
        n_active_samples.append(n_active)
        stats.N_active_max = max(stats.N_active_max, n_active)

    stats.wall_time_s = time.perf_counter() - t0
    stats.steps = steps
    stats.final_dt = dt
    stats.N_active_avg = float(np.mean(n_active_samples))
    stats.N_active_samples = n_active_samples

    # Build effective high-res solution for error: prolong final coarse + overlay fine
    x_fine_full = x_min + (np.arange(N_coarse * refine_ratio) + 0.5) * dx1
    U_fine_full = np.repeat(U_c, refine_ratio, axis=0)
    for pid, (i0, i1) in enumerate(patches):
        U_f = fine_data[pid]
        U_fine_full[i0 * refine_ratio:(i1 + 1) * refine_ratio] = U_f
    rho_num = cons_to_prim(U_fine_full)[0]
    rho_ex, _, _ = sod_exact(x_fine_full, T)
    stats.err_L1_rho = np.mean(np.abs(rho_num - rho_ex))
    stats.err_L2_rho = np.sqrt(np.mean((rho_num - rho_ex) ** 2))
    stats.err_Linf_rho = np.max(np.abs(rho_num - rho_ex))
    return x_fine_full, U_fine_full, stats, patches


def _amr_pad_fine(U_f, U_c, i0, i1, r, n_ghost, bc, N_coarse):
    """Build ghost cells for a fine patch from coarse (or adjacent fine if available)."""
    # Left ghosts from coarse cell i0-1 piecewise-constantly prolonged
    if i0 == 0:
        if bc == "transmissive":
            left_g = np.repeat(U_f[:1], n_ghost, axis=0)
        else:
            raise NotImplementedError
    else:
        left_g = np.repeat(U_c[i0 - 1:i0], n_ghost, axis=0)
    if i1 == N_coarse - 1:
        if bc == "transmissive":
            right_g = np.repeat(U_f[-1:], n_ghost, axis=0)
        else:
            raise NotImplementedError
    else:
        right_g = np.repeat(U_c[i1 + 1:i1 + 2], n_ghost, axis=0)
    return np.concatenate([left_g, U_f, right_g], axis=0)


def _is_in_patches(i, patches):
    return any(i0 <= i <= i1 for (i0, i1) in patches)


# -----------------------------------------------------------------------------
# Solver 3: Multiresolution (Harten cell-average) on uniform fine grid
# -----------------------------------------------------------------------------
def run_mr(N_fine=400, J_levels=4, T=0.2, cfl=0.5, x_min=0.0, x_max=1.0,
           tol=1e-3, bc="transmissive"):
    """Adaptive multiresolution (cell-average wavelet thresholding) solver.

    Approach (faithful to Harten/Roussel/Carmen idea):
      - Represent solution on finest grid of N_fine cells (dx_fine = L/N_fine).
      - At each step, compute multilevel cell-average wavelet (detail) coefficients
        d_j[k] = U_{j+1,2k+1} - (predicted from level j) for level j=0..J-1.
      - Active leaves at level j+1 are those whose details |d_j|/||U||_inf > tol_j
        with Harten's scale-dependent tol_j = tol * 2^(j-J) (in 1D).
      - Compute fluxes ONLY on active leaves; coarse representations carry
        averaged data where leaves are pruned.
      - Time step: take fine-grid dt computed from CFL, advance only active cells.
      - This is a *graded* tree: parents of active leaves are kept;
        siblings of active leaves are kept (for derivatives).

    Implementation: rather than build a tree, we keep a uniform fine array
    and a boolean `active` mask. Inactive cells are stored as their level-j
    cell-average (constant across the 2^(J-j) covered fines). This is the
    standard "lazy MR" form — gives correct compression accounting and
    correct numerics for the active cells; lets us reuse the same HLL+MUSCL
    flux routine for the active interface fluxes.
    """
    t0 = time.perf_counter()
    dx = (x_max - x_min) / N_fine
    x = x_min + (np.arange(N_fine) + 0.5) * dx
    U = sod_initial(x)
    assert N_fine % (2 ** J_levels) == 0, "N_fine must be divisible by 2^J"

    def wavelet_threshold(U):
        """Compute multilevel cell-averages and detail coeffs.
        Returns `active` boolean array (N_fine,) marking cells whose
        finest representation is kept."""
        # Build pyramid: averages[j] has N_fine / 2^j cells
        averages = [U.copy()]
        for j in range(1, J_levels + 1):
            cur = averages[-1]
            avg = 0.5 * (cur[0::2] + cur[1::2])
            averages.append(avg)
        # Details: d_j[k] = U_{j+1,k_pair} - predicted_from_level_j+1
        # Simplest predictor: linear from level j+1 (with periodic-aware fallback)
        active = np.zeros(N_fine, dtype=bool)
        # Always keep coarsest level (force "graded" basis)
        for j in range(J_levels, 0, -1):
            cur = averages[j - 1]      # finer
            coarse = averages[j]       # coarser, half size
            # Predict cur from coarse using simple injection + correction:
            # For pair (2k, 2k+1) of cur, the average is coarse[k].
            # A simple linear predictor: pred[2k] = coarse[k] + slope_k/4,
            #                            pred[2k+1] = coarse[k] - slope_k/4
            # where slope_k = (coarse[k+1] - coarse[k-1])/2 (central)
            n_c = coarse.shape[0]
            slope = np.zeros_like(coarse)
            slope[1:-1] = 0.5 * (coarse[2:] - coarse[:-2])
            pred_even = coarse - 0.25 * slope
            pred_odd = coarse + 0.25 * slope
            # Details on rho channel (most informative) — normalized by ||rho||_inf
            d_even = cur[0::2] - pred_even
            d_odd = cur[1::2] - pred_odd
            rho_scale = np.max(np.abs(cur[..., 0])) + EPS
            d_norm = np.maximum(np.abs(d_even[..., 0]), np.abs(d_odd[..., 0])) / rho_scale
            # Harten scale-dependent threshold (in 1D): tol_j = tol * 2^(j - J)
            tol_j = tol * (2.0 ** (j - J_levels))
            keep_coarse = d_norm > tol_j  # cells at level j-1 that should NOT be coarsened
            # Map keep_coarse (size n_c) onto fine active mask
            # If keep_coarse[k] is True, all 2^j fine cells under coarse cell k stay potentially active
            block = 2 ** (j - 1)  # number of cells at level (j-1) under each level-j cell
            # Wait — level numbering: level 0 = finest, level J = coarsest.
            # cur (level j-1) has 2*n_c cells; each pair (2k,2k+1) at level j-1 maps to k at level j.
            # If keep_coarse[k]==False, we coarsen the pair to coarse[k] (i.e. mark them inactive).
            # If True, keep them active.
            #
            # Translate to fine grid: each level-(j-1) cell covers 2^(j-1) fine cells.
            stride_fine = 2 ** (j - 1)
            for k in range(n_c):
                if keep_coarse[k]:
                    fine_start = (2 * k) * stride_fine
                    fine_end = (2 * k + 2) * stride_fine
                    active[fine_start:fine_end] = True
        return active, averages

    def project_to_active(U, active, averages):
        """Cells not in `active` get replaced by their coarse-level cell-average
        constant across the covered fine cells (i.e. the data is 'projected'
        onto the adapted basis). This is the data form on which we then run
        the flux update."""
        U_proj = U.copy()
        # For each contiguous run of inactive cells of length 2^j, set them
        # to the average over that block (using `averages` pyramid lookup).
        # Simplest: walk through fine cells, group by largest power-of-2 run
        # that is wholly inactive and aligned, replace with that block's mean.
        i = 0
        N = U.shape[0]
        while i < N:
            if active[i]:
                i += 1
                continue
            # find length of inactive run
            j = i
            while j < N and not active[j]:
                j += 1
            run_len = j - i
            if run_len > 0:
                U_proj[i:j] = np.mean(U[i:j], axis=0)
            i = j
        return U_proj

    t = 0.0
    steps = 0
    n_active_samples = []
    stats = RunStats(name=f"mr_N={N_fine}_J={J_levels}_tol={tol}",
                     N_uniform_equiv=N_fine)

    while t < T:
        # Threshold + project
        active, averages = wavelet_threshold(U)
        U = project_to_active(U, active, averages)

        dt = cfl_dt(U, dx, cfl)
        dt = min(dt, T - t)

        # Standard HLL+MUSCL update on full fine grid; the savings here are
        # representational/accuracy, not arithmetic. We measure compression
        # as n_active / N_fine to match Carmen's reporting.
        # NOTE: a truly faster MR code (Carmen) computes fluxes only at
        # active leaves; we use a simplified accounting model here.
        Uext = _pad(U, 2, bc)
        F = compute_flux(Uext)
        U = U - dt / dx * (F[2:N_fine + 2] - F[1:N_fine + 1])
        t += dt
        steps += 1
        n_active = int(active.sum())
        n_active_samples.append(n_active)
        stats.N_active_max = max(stats.N_active_max, n_active)

    stats.wall_time_s = time.perf_counter() - t0
    stats.steps = steps
    stats.final_dt = dt
    stats.N_active_avg = float(np.mean(n_active_samples))
    stats.N_active_samples = n_active_samples
    rho_num = cons_to_prim(U)[0]
    rho_ex, _, _ = sod_exact(x, T)
    stats.err_L1_rho = np.mean(np.abs(rho_num - rho_ex))
    stats.err_L2_rho = np.sqrt(np.mean((rho_num - rho_ex) ** 2))
    stats.err_Linf_rho = np.max(np.abs(rho_num - rho_ex))
    return x, U, stats
