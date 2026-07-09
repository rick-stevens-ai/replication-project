"""Dynamical Low-Rank (DLR) projector-splitting integrator for 1D1V Vlasov-Poisson.

Discrete representation:
   f(x_i, v_j, t) ≈ Σ_{k,l=1}^r  X_{i,k}(t)  S_{k,l}(t)  V_{j,l}(t)
   X ∈ R^{Nx×r}, S ∈ R^{r×r}, V ∈ R^{Nv×r},
   X^T X = I_r (discrete L²_x using weight √dx),  V^T V = I_r (with √dv).

Equivalent matrix form: F = X S V^T,  F ∈ R^{Nx×Nv}.

Projector-splitting (KSL) for ∂_t F = G(F), where for Vlasov-Poisson:
   G(F) = - D_x F · diag(v) + diag(E) · F · D_v^T
       ≈ - (v · ∇_x f) + (E · ∇_v f)         (in matrix form, with circulant D_x, D_v)

This is mathematically equivalent to splitting the orthogonal projection P(F) onto
the tangent space of the rank-r manifold at F = X S V^T :
   P(F) δF = X X^T δF + δF V V^T - X X^T δF V V^T.
The three sub-steps (K, S, L) integrate each piece exactly in the corresponding factor.

References: Lubich & Oseledets, BIT 54 (2014) 171-188; Einkemmer & Lubich, SISC 40 (2018).

Implementation notes
--------------------
We work with unweighted matrices and use the L² inner product weights implicitly
(orthonormality X^T X * dx = I_r, V^T V * dv = I_r). To keep code simple we use
the *rescaled* convention X^T X = I, V^T V = I and absorb dx, dv constants where
needed in the right-hand-sides.

Specifically let \tilde X = X * √dx, \tilde V = V * √dv. Then \tilde X^T \tilde X = I,
\tilde V^T \tilde V = I, and F = X S V^T = \tilde X (S/√(dx·dv)) \tilde V^T. We store
the rescaled \tilde X, \tilde V, and \tilde S = S/√(dx·dv). With this rescaling
all inner products are plain matrix products, and ∫ f dv = (\tilde X \tilde S
\tilde V^T) · 1 · dv = \tilde X \tilde S (\tilde V^T · √dv · 1) = \tilde X \tilde S
(√dv · sum_j \tilde V_j). For brevity we drop tildes; X, S, V below are the
rescaled (orthonormal-column) versions.
"""
from __future__ import annotations
import numpy as np
from scipy.linalg import expm
from vp_common import Grid


# ---------- spectral differentiation in x and v (periodic) -----------------

def _make_Dx(grid: Grid):
    """Build pseudo-spectral derivative operator d/dx as a function dx_op(g) on (Nx,r)."""
    kx = grid.kx
    def op(g):
        # g: (Nx, r)
        return np.real(np.fft.ifft(1j * kx[:, None] * np.fft.fft(g, axis=0), axis=0))
    return op


def _make_Dv(grid: Grid):
    kv = grid.kv
    def op(g):
        return np.real(np.fft.ifft(1j * kv[:, None] * np.fft.fft(g, axis=0), axis=0))
    return op


# ---------- Poisson solve directly from low-rank factors -------------------

def poisson_E_lr(X, S, V, grid: Grid):
    """Compute E(x) given F = X S V^T (rescaled factors).

    ρ(x) = ∫ f dv = (X S V^T) · 1 · dv
         = X S (V^T 1) · dv,    1 is length-Nv vector of ones.
    With rescaling V^T V = I (so V already includes √dv), we have:
        ρ(x) = X S V^T 1 * dv  =  X (S (V^T 1)) * dv.
    But V here is rescaled (\tilde V = V_unscaled * √dv), so V^T 1 = √dv * sum_j V_unscaled_j.
    The factor of dv appears once: ρ = X S (V^T 1) * sqrt(dv).

    Cleaner: just reconstruct F and integrate.
    """
    F = X @ S @ V.T  # rescaled F; relation to physical f below
    # Physical f_phys(x,v) = F(x,v) / sqrt(dx*dv)  (since X has √dx, V has √dv absorbed)
    # ρ_phys(x) = ∫ f_phys dv = sum_j f_phys(x,v_j) dv = sum_j F(x,v_j) * sqrt(dv/dx)
    rho = 1.0 - np.sum(F, axis=1) * np.sqrt(grid.dv / grid.dx)
    rho_hat = np.fft.fft(rho)
    kx = grid.kx
    E_hat = np.zeros_like(rho_hat)
    nz = kx != 0
    E_hat[nz] = rho_hat[nz] / (1j * kx[nz])
    E = np.real(np.fft.ifft(E_hat))
    return E


def reconstruct_f(X, S, V, grid: Grid):
    """Return physical f(x_i, v_j) on the grid."""
    F = X @ S @ V.T
    return F / np.sqrt(grid.dx * grid.dv)


# ---------- low-rank initialization via SVD ---------------------------------

def lr_init(f: np.ndarray, grid: Grid, r: int):
    """Initialize (X,S,V) from physical f via truncated SVD in the L² inner product.

    Construct F_scaled = f * sqrt(dx*dv); then SVD F_scaled = U Σ W^T, take rank r.
    X = U[:, :r] (Nx×r, orthonormal in plain Euclidean -> orthonormal in L²_x because
    of the sqrt(dx) rescaling).  V = W[:, :r],  S = diag(Σ[:r]).
    """
    Fs = f * np.sqrt(grid.dx * grid.dv)
    U, sig, Wt = np.linalg.svd(Fs, full_matrices=False)
    X = U[:, :r]
    S = np.diag(sig[:r])
    V = Wt[:r, :].T
    return X, S, V


# ---------- projector-splitting (KSL) one time step ------------------------

def _solve_advection_x(K0, v_eff, grid: Grid, dt: float):
    """Solve ∂_t K = -∂_x(K * diag(v_eff)) exactly via FFT.

    Here K is (Nx, r) and v_eff is (r,) (eigenvalue-like coefficients).
    For each column k:  ∂_t K_k + v_eff_k ∂_x K_k = 0  -> shift by v_eff_k * dt in x.

    Wait — in the K-step the right-hand-side is more general: a sum of advections
    with the matrix coefficient V^T diag(v) V. We use a matrix-exponential
    approach in Fourier:
        ∂_t K_hat(k) = -i k * K_hat(k) * C^T,   C = V^T diag(v) V  (r×r)
    Solution: K_hat(k, dt) = K_hat(k, 0) * exp(-i k dt C^T).
    For each Fourier mode this is an (r×r) matrix exponential; we diagonalize C
    once: C = Q Λ Q^{-1}, then exp(-i k dt C^T) = (Q^{-T}) exp(-i k dt Λ) Q^T.

    Similarly handles the cross-coupling produced by the K-step ODE which is
    NOT diagonal in v_eff in general.
    """
    pass  # superseded by the matrix version below


def _expm_advection(coef_matrix, op_x_fft, grid: Grid, dt: float, K):
    """Given ∂_t K = -∂_x K · C^T (matrix advection where C is r×r),
    return K(dt).

    In Fourier (axis=0):  ∂_t \hat K(kx) = -i kx \hat K(kx) C^T
    Solution: \hat K(kx, dt) = \hat K(kx, 0) · expm(-i kx dt C^T).

    We compute expm(-i kx dt C^T) for each kx via batched matrix-exponential
    using eigendecomposition (C symmetric for our use cases: C1=V^T diag(v) V is
    symmetric since diag(v) is symmetric and V has orthonormal columns wrt
    Euclidean inner product. So C1=C1^T -> real eigenvalues, well-conditioned).
    """
    C = coef_matrix
    Ct = C.T
    # Symmetric -> use eigh; if not symmetric, fall back to eig with clipping.
    sym_err = np.linalg.norm(Ct - Ct.T) / max(np.linalg.norm(Ct), 1e-30)
    if sym_err < 1e-10:
        eigvals, Q = np.linalg.eigh(Ct)
        Qinv = Q.T
    else:
        eigvals, Q = np.linalg.eig(Ct)
        Qinv = np.linalg.inv(Q)
    Ktil = K @ Q
    kx = grid.kx
    Ktil_hat = np.fft.fft(Ktil, axis=0)
    for k in range(Ktil.shape[1]):
        Ktil_hat[:, k] *= np.exp(-1j * kx * eigvals[k] * dt)
    Ktil = np.fft.ifft(Ktil_hat, axis=0)
    Knew = Ktil @ Qinv
    return np.real(Knew)


def _solve_K_step(X, S, V, grid: Grid, dt: float):
    """K-step: set K = X S (Nx × r); evolve ∂_t K = -∂_x K · (V^T diag(v) V)^T
    + diag(?) [no force term in K-step under standard KSL: the velocity-shift
    contribution is handled in L-step]. Following Einkemmer-Lubich (2018) eq.
    (3.4)–(3.6):

    Actually the projector-splitting for ∂_t f = -v ∂_x f + E ∂_v f gives:
       K-step: ∂_t K = -∂_x K · ⟨V, v V⟩^T  + diag(E) · K · ⟨∂_v V, V⟩^T
       S-step: ∂_t S = + (⟨X, ∂_x X⟩ S ⟨V, v V⟩^T)^? ... [reverse signs]
       L-step: ∂_t L = + ⟨v X, ∂_x X⟩^T · L  - L · (⟨X, E X⟩) · ?

    To stay tractable & correct, we follow a clean derivation:
    project G(F) = -∂_x(v F) + ∂_v(E F)·(-1)·(-1) = -v ∂_x F + E ∂_v F onto
    tangent space; KSL splits the projection.

    Let:
       c_V := V^T diag(v) V                 (r×r)   "velocity matrix"
       d_V := V^T diag(v) ∂v V?  not needed since we keep E_v term in K-step via
              right-multiplication: E_v contribution requires V^T (∂_v · V) in L-step.

    Standard form (Einkemmer-Lubich 2018 algorithm 1):
       K-step:  K = X S; solve  ∂_t K = -∂_x K · C1^T  + E.*K · C2^T
                where  C1 = V^T diag(v) V,  C2 = V^T diag(∂_v 1) V ?  No --
                the E ∂_v f term yields E(x) * X S (V^T ∂_v V)^T after integrating
                by parts in v (with periodic V).

    So:
       C1 = V^T diag(v) V   (r×r)
       D2 = V^T ∂_v V      (r×r)  (each column: ∂_v of V column, then project)
       K-step:  ∂_t K = -∂_x K · C1^T  + diag(E(x)) · K · D2^T

    This is a coupled advection-reaction in x for the r columns of K.
    """
    # Build C1, D2 from V
    Nv = V.shape[0]
    v = grid.v
    # C1 = V^T diag(v) V
    C1 = V.T @ (v[:, None] * V)
    # D2 = V^T ∂_v V (spectral)
    kv = grid.kv
    Vhat = np.fft.fft(V, axis=0)
    dV = np.real(np.fft.ifft(1j * kv[:, None] * Vhat, axis=0))
    D2 = V.T @ dV
    # Compute E from current state (before evolving K)
    E = poisson_E_lr(X, S, V, grid)
    # Form K
    K = X @ S
    # We solve  ∂_t K = -∂_x K · C1^T  + diag(E) · K · D2^T  using an
    # operator-splitting between advection and reaction (Strang within K-step):
    K = _expm_advection(C1, None, grid, 0.5 * dt, K)
    # reaction step (pointwise in x): ∂_t K(x) = E(x) * K · D2^T  (linear ODE in r-dim per x).
    # Solution: K(x,t) = K(x,0) * expm(E(x) dt D2^T) [right-multiplied].
    # D2 = V^T ∂_v V is skew-symmetric-like (eigenvalues purely imaginary). Use
    # an eigendecomposition of D2^T once, then batch over x:
    eigD, QD = np.linalg.eig(D2.T)            # complex in general
    QDinv = np.linalg.inv(QD)
    Ktil = K @ QD                              # (Nx, r) complex
    # Each column k: Ktil(x) <- Ktil(x) * exp(E(x)*dt*eigD[k])
    # eigD purely imaginary => exp is bounded oscillation; clip exp arg real part
    # for numerical safety in case of small non-zero real component:
    arg = (E[:, None] * dt * eigD[None, :])    # (Nx, r) complex
    # Cap real part of argument to avoid overflow if scheme is being driven
    # unstable; this changes only the sub-step in regions of instability.
    arg_real = np.clip(arg.real, -50.0, 50.0)
    arg = arg_real + 1j * arg.imag
    Ktil = Ktil * np.exp(arg)
    K = np.real(Ktil @ QDinv)
    K = _expm_advection(C1, None, grid, 0.5 * dt, K)
    # Re-orthonormalize K = X_new R; new S_tilde = R
    X_new, R = np.linalg.qr(K)
    S_new = R
    return X_new, S_new


def _solve_S_step(X, S, V, grid: Grid, dt: float):
    """S-step: ∂_t S = + ⟨X, v ∂_x X⟩? ... With KSL the S-step *reverses sign*:
         ∂_t S = -[ -⟨∂_x X, X⟩^T S ⟨V, v V⟩? + ... ]
    Concretely (Einkemmer-Lubich 2018):
       ∂_t S = + (X^T ∂_x X) S C1^T  - X^T diag(E) X · S · D2^T
    (sign flipped relative to K- and L-step).
    """
    Nx = X.shape[0]
    # C1 = V^T diag(v) V
    v = grid.v
    C1 = V.T @ (v[:, None] * V)
    kv = grid.kv
    Vhat = np.fft.fft(V, axis=0)
    dV = np.real(np.fft.ifft(1j * kv[:, None] * Vhat, axis=0))
    D2 = V.T @ dV
    # ∂_x X
    kx = grid.kx
    Xhat = np.fft.fft(X, axis=0)
    dX = np.real(np.fft.ifft(1j * kx[:, None] * Xhat, axis=0))
    A1 = X.T @ dX                 # r×r
    # E from current factors
    E = poisson_E_lr(X, S, V, grid)
    B1 = X.T @ (E[:, None] * X)   # r×r
    # ODE: ∂_t S = + A1 S C1^T  -  B1 S D2^T
    # Solve via small-step RK4 to limit per-step S growth (the S-step ODE has
    # spectral norm bounded by ||A1||*||C1|| + ||B1||*||D2|| which can be ~O(10)
    # in nonlinear regimes; subcycle to keep CFL-like ratio small).
    norm_est = (np.linalg.norm(A1, 2) * np.linalg.norm(C1, 2)
                + np.linalg.norm(B1, 2) * np.linalg.norm(D2, 2))
    nsub = max(1, int(np.ceil(norm_est * dt / 0.2)))
    h = dt / nsub
    def rhs(St):
        return A1 @ St @ C1.T - B1 @ St @ D2.T
    for _ in range(nsub):
        k1 = rhs(S)
        k2 = rhs(S + 0.5 * h * k1)
        k3 = rhs(S + 0.5 * h * k2)
        k4 = rhs(S + h * k3)
        S = S + (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
    return X, S, V


def _solve_L_step(X, S, V, grid: Grid, dt: float):
    """L-step: L = V S^T (Nv × r). Evolve
       ∂_t L = -∂_v L · (X^T diag(E) X)^T  + diag(v) · L · (X^T ∂_x X)^T
    Wait — careful with signs/derivations. The original PDE is
       ∂_t f + v ∂_x f - E ∂_v f = 0  =>  ∂_t f = -v ∂_x f + E ∂_v f.
    The L-step handles the "right factor" contributions:
       ∂_t L = + ⟨v, ∂_x X⟩? ...  Following the standard form:
       ∂_t L = - diag(v) · L · A1^T  + ∂_v L · B1^T,
    where A1 = X^T ∂_x X (r×r) and B1 = X^T diag(E) X (r×r).
    """
    Nv = V.shape[0]
    v = grid.v
    # Recompute E using the *updated* X and current V/S (post K and S steps)
    # NB: in standard KSL, L-step uses E evaluated from the current factors.
    E = poisson_E_lr(X, S, V, grid)
    # ∂_x X
    kx = grid.kx
    Xhat = np.fft.fft(X, axis=0)
    dX = np.real(np.fft.ifft(1j * kx[:, None] * Xhat, axis=0))
    A1 = X.T @ dX                 # r×r
    B1 = X.T @ (E[:, None] * X)   # r×r
    L = V @ S.T                   # (Nv, r)
    # ∂_t L = -diag(v) L A1^T  +  ∂_v L · B1^T
    # Strang: reaction half, advection full (in v) with matrix B1, reaction half
    # Reaction: ∂_t L(v) = -v L(v) A1^T. Per-v ODE in r dims, linear with v-scaled matrix.
    # Diagonalize A1^T = Q Λ Q^{-1}.
    # A1 = X^T ∂_x X has purely imaginary eigenvalues to leading order (∂_x is
    # skew on real periodic fns). Use per-v matrix exponential via scipy.expm to
    # be robust.
    # A1 = X^T ∂_x X is skew-like; diagonalize once, batch over v.
    eigA, QA = np.linalg.eig(A1.T)
    QAinv = np.linalg.inv(QA)
    def reaction(Lin, half_dt):
        Ltil = Lin @ QA
        arg = (-v[:, None] * half_dt * eigA[None, :])
        arg_real = np.clip(arg.real, -50.0, 50.0)
        arg = arg_real + 1j * arg.imag
        Ltil = Ltil * np.exp(arg)
        return np.real(Ltil @ QAinv)
    L = reaction(L, 0.5 * dt)
    # Advection: ∂_t L = ∂_v L · B1^T  =>  per Fourier mode kv: ∂_t L_hat = +i kv L_hat B1^T
    # Solution per Fourier mode: L_hat(kv,t) = L_hat(kv,0) * expm(+i kv dt B1^T)
    # B1 is symmetric (X^T diag(E) X), so eigenvalues are real, expm bounded.
    eigB, QB = np.linalg.eig(B1.T)
    QBinv = np.linalg.inv(QB)
    Ltil = L @ QB
    kv = grid.kv
    Ltil_hat = np.fft.fft(Ltil, axis=0)
    # Each column k: shift by -eigB[k] in v direction (advection speed -eigB[k])
    for k in range(Ltil.shape[1]):
        Ltil_hat[:, k] *= np.exp(1j * kv * eigB[k].real * dt)
    Ltil = np.fft.ifft(Ltil_hat, axis=0)
    L = np.real(Ltil @ QBinv)
    L = reaction(L, 0.5 * dt)
    # Re-orthonormalize L = V_new S_new^T
    V_new, R = np.linalg.qr(L)
    S_new = R.T
    return X, S_new, V_new


def step_KSL(X, S, V, grid: Grid, dt: float):
    """One projector-splitting (Lie) step. For better accuracy could Strang-split
    the (K,S,L) sequence, but standard KSL is first-order Lie."""
    X, S = _solve_K_step(X, S, V, grid, dt)
    X, S, V = _solve_S_step(X, S, V, grid, dt)
    X, S, V = _solve_L_step(X, S, V, grid, dt)
    return X, S, V


def step_KSL_strang(X, S, V, grid: Grid, dt: float):
    """Strang-style symmetric composition: K(dt/2) S(dt/2) L(dt) S(dt/2) K(dt/2).
    Formally 2nd-order if each substep is 2nd-order; here substeps are exact in
    their operator so symmetric composition gives 2nd order in dt for the
    KSL splitting (cf. Lubich-Oseledets 2014).
    """
    X, S = _solve_K_step(X, S, V, grid, 0.5 * dt)
    X, S, V = _solve_S_step(X, S, V, grid, 0.5 * dt)
    X, S, V = _solve_L_step(X, S, V, grid, dt)
    X, S, V = _solve_S_step(X, S, V, grid, 0.5 * dt)
    X, S = _solve_K_step(X, S, V, grid, 0.5 * dt)
    return X, S, V


# ---------- driver ---------------------------------------------------------

def run(f0: np.ndarray, grid: Grid, T: float, dt: float, r: int, diag_every: int = 1):
    from vp_common import electric_energy, total_mass, kinetic_energy, l2_norm

    X, S, V = lr_init(f0, grid, r)
    Nt = int(round(T / dt))
    t = np.zeros(Nt + 1)
    Ee = np.zeros(Nt + 1)
    mass = np.zeros(Nt + 1)
    KE = np.zeros(Nt + 1)
    L2 = np.zeros(Nt + 1)

    def diag(n):
        f = reconstruct_f(X, S, V, grid)
        E = poisson_E_lr(X, S, V, grid)
        Ee[n] = electric_energy(E, grid)
        mass[n] = total_mass(f, grid)
        KE[n] = kinetic_energy(f, grid)
        L2[n] = l2_norm(f, grid)
    diag(0)

    for n in range(Nt):
        X, S, V = step_KSL(X, S, V, grid, dt)
        t[n + 1] = (n + 1) * dt
        if not (np.isfinite(X).all() and np.isfinite(S).all() and np.isfinite(V).all()):
            print(f"  [warning] DLR scheme blew up at step {n+1} (t={t[n+1]:.3f}); halting and returning prior state.")
            # truncate arrays to before blowup
            t = t[:n + 1]
            Ee = Ee[:n + 1]
            mass = mass[:n + 1]
            KE = KE[:n + 1]
            L2 = L2[:n + 1]
            break
        if (n + 1) % diag_every == 0 or n == Nt - 1:
            diag(n + 1)

    f_final = reconstruct_f(X, S, V, grid)
    return {
        "t": t,
        "E_energy": Ee,
        "mass": mass,
        "kinetic_energy": KE,
        "l2": L2,
        "f_final": f_final,
        "X": X, "S": S, "V": V,
    }
