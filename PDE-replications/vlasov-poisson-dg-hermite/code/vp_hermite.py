"""
1D1V Vlasov-Poisson solver using a symmetrically-weighted Hermite
spectral expansion in velocity and a Fourier pseudospectral
discretization in space.

Reduced/independent reimplementation in the spirit of
Bessemoulin-Chatard & Filbet (DG/Hermite for VP) and the broader
SW-Hermite Vlasov literature (Schumer-Holloway, Filbet, Camporeale,
Delzanno, Cai-Wang).

Expansion:
    f(x, v, t) = sum_{n=0}^{N-1} C_n(x, t) * psi_n(v)
    psi_n(v) = (1/sqrt(2^n n! sqrt(pi))) * H_n(v/v_t) * exp(-v^2/(2 v_t^2)) / sqrt(v_t)

With the SW basis, the velocity-derivative operator and v* multiplication act
as the same symmetric tridiagonal:

    v psi_n = v_t * ( sqrt(n/2) psi_{n-1} + sqrt((n+1)/2) psi_{n+1} )
    d/dv psi_n = -(1/v_t) * ( sqrt(n/2) psi_{n-1} - sqrt((n+1)/2) psi_{n+1} )

Then Vlasov  ∂_t f + v ∂_x f - E ∂_v f = 0  becomes, for each Fourier mode k:

    ∂_t C_n + v_t * (sqrt(n/2) ∂_x C_{n-1} + sqrt((n+1)/2) ∂_x C_{n+1})
            + (E/v_t) * (sqrt(n/2) C_{n-1} - sqrt((n+1)/2) C_{n+1}) = 0

Poisson: ∂_x E = ρ - 1, where ρ(x,t) = ∫ f dv = C_0(x,t) * (sqrt(v_t) * pi^{1/4})
  because ∫ psi_0 dv = (1/sqrt(sqrt(pi))) * sqrt(v_t) * sqrt(pi) / sqrt(v_t) ...
  We compute the normalization constant explicitly below.
"""

import numpy as np


# ---- Normalization helpers ---------------------------------------------------

def psi_integral_const(v_t):
    """∫ psi_0(v) dv. psi_0 = (1/sqrt(sqrt(pi))) * exp(-v^2/(2 v_t^2)) / sqrt(v_t).

    ∫ exp(-v^2/(2 v_t^2)) dv = sqrt(2 pi) v_t.
    => ∫ psi_0 dv = (1/pi^{1/4}) * sqrt(2 pi) * v_t / sqrt(v_t)
                  = (1/pi^{1/4}) * sqrt(2 pi) * sqrt(v_t)
                  = sqrt(2) * pi^{1/4} * sqrt(v_t).
    """
    return np.sqrt(2.0) * (np.pi ** 0.25) * np.sqrt(v_t)


def psi_v2_integral_const(v_t):
    """∫ v^2 psi_0(v) dv  (for kinetic energy from C_0,C_2 modes).

    Using v psi_0 = v_t * sqrt(1/2) * psi_1,
    so v^2 psi_0 = v_t^2 * sqrt(1/2) * (sqrt(1/2) psi_0 + sqrt(2/2) psi_2)
                 = v_t^2 * (1/2 psi_0 + (1/sqrt(2)) psi_2)... wait, redo:
    v psi_1 = v_t (sqrt(1/2) psi_0 + sqrt(2/2) psi_2) = v_t(sqrt(1/2) psi_0 + psi_2)
    v^2 psi_0 = v_t * sqrt(1/2) * v psi_1
              = v_t^2 * sqrt(1/2) * (sqrt(1/2) psi_0 + psi_2)
              = v_t^2 * (1/2 psi_0 + (1/sqrt(2)) psi_2).
    Then ∫ v^2 psi_0 dv = v_t^2 * (1/2 * I0 + (1/sqrt(2)) * I2),
    where I_n = ∫ psi_n dv. For SW basis, ∫ psi_n dv = 0 for n>=1 odd is wrong;
    in general, ∫ H_n(x) e^{-x^2/2} dx is nonzero only for even n.

    For even n=2: ∫ psi_2 dv. psi_2 = (1/sqrt(2^2 * 2!) sqrt(sqrt(pi))) H_2(v/v_t)
    exp(-v^2/(2 v_t^2)) / sqrt(v_t).
    H_2(x) = 4x^2 - 2 (physicists' Hermite).
    ∫ (4 v^2/v_t^2 - 2) exp(-v^2/(2 v_t^2)) dv
      = 4/v_t^2 * v_t^2 * sqrt(2 pi) v_t  -  2 * sqrt(2 pi) v_t
      = 4 sqrt(2 pi) v_t - 2 sqrt(2 pi) v_t = 2 sqrt(2 pi) v_t.
    Norm: 1/sqrt(8 * sqrt(pi)) / sqrt(v_t).
    I_2 = 2 sqrt(2 pi) v_t / sqrt(8 sqrt(pi)) / sqrt(v_t)
        = 2 sqrt(2 pi) * sqrt(v_t) / sqrt(8) / pi^{1/4}
        = sqrt(2 pi) / sqrt(2) * sqrt(v_t) / pi^{1/4}
        = sqrt(pi) * sqrt(v_t) / pi^{1/4}
        = pi^{1/4} * sqrt(v_t).

    For higher even moments we'd extend, but we use a different route below.
    """
    raise NotImplementedError("Use moment helpers directly.")


# Precompute coefficients for moments of psi_n(v):  M_k^n = ∫ v^k psi_n dv.
# Only need k=0,1,2 for mass, momentum, kinetic energy.
# Derived from recursions: v psi_n = v_t (a_n psi_{n-1} + a_{n+1} psi_{n+1}),
# with a_n = sqrt(n/2). Then v^k psi_0 is a linear combination of psi_j for
# j <= k; we compute the coefficients by repeated matrix-vector application.

def hermite_v_matrix(N, v_t):
    """Matrix V s.t. v*psi = V @ psi (vector of psi_n)."""
    V = np.zeros((N, N))
    for n in range(N):
        a_n = np.sqrt(n / 2.0)
        a_np1 = np.sqrt((n + 1) / 2.0)
        if n - 1 >= 0:
            V[n, n - 1] = v_t * a_n
        if n + 1 < N:
            V[n, n + 1] = v_t * a_np1
    return V


def moments_of_basis(N, v_t):
    """Return (I0, I1, I2) arrays of length N giving ∫ v^k psi_n(v) dv."""
    # Base case: I0[n] = ∫ psi_n dv.
    # From orthonormality of SW basis under weight 1 (not e^{-v^2}!),
    # the basis psi_n is orthonormal in L^2(R, dv): ∫ psi_n psi_m dv = δ_{nm}.
    # So I0[n] = ∫ psi_n * 1 dv = <psi_n, 1>_{L^2}.
    # The constant function 1 in the SW basis: 1 = sum_n c_n psi_n, with
    # c_n = ∫ 1 * psi_n dv = I0[n]. We can compute by direct integration with
    # Gauss-Hermite quadrature.
    Nq = max(4 * N, 200)
    nodes, weights = np.polynomial.hermite_e.hermegauss(Nq)
    # HermiteE: weight exp(-x^2/2), so v = v_t * x then dv = v_t dx
    v_nodes = v_t * nodes
    # psi_n(v) values
    # Use 3-term recurrence for the SW Hermite functions directly to avoid overflow.
    # phi_n(x) := (1/sqrt(2^n n! sqrt(pi))) H_n(x) exp(-x^2/2)/sqrt(v_t? )
    # Recurrence for physicists' Hermite functions (orthonormal in L^2(R,dx)):
    #   h_0(x) = pi^{-1/4} exp(-x^2/2)
    #   h_1(x) = sqrt(2) x h_0(x)
    #   h_{n+1}(x) = sqrt(2/(n+1)) x h_n(x) - sqrt(n/(n+1)) h_{n-1}(x)
    # Then psi_n(v) = (1/sqrt(v_t)) h_n(v/v_t).
    x = nodes  # quadrature in x (HermiteE means weight exp(-x^2/2))
    # But we want v = v_t * x_phys with weight 1.
    # Use physicists' Hermite quadrature instead:
    x_phys, w_phys = np.polynomial.hermite.hermgauss(Nq)
    # weight exp(-x^2), integrate g(x) -> sum w_i g(x_i) approximates ∫ g(x) e^{-x^2} dx
    # We want ∫ psi_n(v) v^k dv = ∫ psi_n(v_t * y) (v_t y)^k v_t dy
    y = x_phys  # in v / v_t units? careful — we don't use the e^{-x^2} weight directly.
    # Simpler: build a uniform fine grid in v and integrate numerically.
    Lv = 8.0 * v_t
    Nv = 4000
    v = np.linspace(-Lv, Lv, Nv)
    dv = v[1] - v[0]
    # Hermite functions h_n(v/v_t) by stable recurrence
    z = v / v_t
    h = np.zeros((N, Nv))
    h[0] = (np.pi ** -0.25) * np.exp(-0.5 * z * z)
    if N > 1:
        h[1] = np.sqrt(2.0) * z * h[0]
    for n in range(1, N - 1):
        h[n + 1] = np.sqrt(2.0 / (n + 1)) * z * h[n] - np.sqrt(n / (n + 1.0)) * h[n - 1]
    psi = h / np.sqrt(v_t)  # psi_n(v)
    I0 = np.sum(psi, axis=1) * dv
    I1 = np.sum(psi * v[None, :], axis=1) * dv
    I2 = np.sum(psi * (v[None, :] ** 2), axis=1) * dv
    return I0, I1, I2, psi, v


# ---- Initial conditions in Hermite coefficient space ------------------------

def project_initial(fxv_func, x, v, psi):
    """Given f(x,v) as a function, project onto SW Hermite basis in v at each x.

    Returns C of shape (N, Nx).
    """
    Nv = v.size
    dv = v[1] - v[0]
    Nx = x.size
    f = fxv_func(x[None, :], v[:, None])  # shape (Nv, Nx)
    # C_n(x) = ∫ f(x,v) psi_n(v) dv
    C = (psi * dv) @ f  # (N, Nx)
    return C


# ---- Solver -----------------------------------------------------------------

class VPHermite:
    def __init__(self, Nx, N, L, v_t, nu=0.0, nu_power=6):
        """nu: hyper-collisional damping coefficient on Hermite mode n,
        applied as  dC_n/dt -= nu * (n/(N-1))^nu_power * C_n.
        Standard closure trick (Camporeale-Delzanno; Cai 2018) to suppress
        spurious recurrence/filamentation at the highest modes without
        affecting low-mode dynamics."""
        self.Nx = Nx
        self.N = N
        self.L = L
        self.v_t = v_t
        self.nu = nu
        self.nu_power = nu_power
        self.x = np.linspace(0, L, Nx, endpoint=False)
        self.dx = L / Nx
        self.k = 2 * np.pi * np.fft.fftfreq(Nx, d=self.dx)
        # k for Poisson (avoid k=0)
        self.k_pois = np.where(self.k == 0, 1.0, self.k)

        # SW Hermite coupling coefficients a_n = sqrt(n/2)
        self.a = np.sqrt(np.arange(N + 1) / 2.0)

        # Build moments arrays (for diagnostics)
        I0, I1, I2, psi, v = moments_of_basis(N, v_t)
        self.I0 = I0
        self.I1 = I1
        self.I2 = I2
        self.psi = psi
        self.v_grid = v

    def density(self, C):
        """ρ(x) = ∫ f dv = sum_n I0[n] C_n(x)."""
        return self.I0 @ C

    def momentum(self, C):
        return self.I1 @ C

    def kinetic_energy(self, C):
        # ∫∫ 0.5 v^2 f dv dx
        ekin_x = 0.5 * (self.I2 @ C)
        return np.sum(ekin_x) * self.dx

    def total_mass(self, C):
        return np.sum(self.density(C)) * self.dx

    def l2_norm(self, C):
        # ‖f‖^2 = ∫∫ f^2 dv dx = ∫ Σ_n C_n^2 dx (orthonormality)
        return np.sum(C * C) * self.dx

    def poisson(self, rho):
        """Solve ∂_x E = ρ - <ρ>; periodic. Returns E(x)."""
        rho_mean = np.mean(rho)
        rhs = rho - rho_mean
        rhs_hat = np.fft.fft(rhs)
        E_hat = rhs_hat / (1j * self.k_pois)
        E_hat[self.k == 0] = 0.0
        E = np.real(np.fft.ifft(E_hat))
        return E

    def field_energy(self, E):
        return 0.5 * np.sum(E * E) * self.dx

    def rhs(self, C):
        """Vlasov RHS in Hermite-Fourier space:
        dC_n/dt = - v_t (a_n ∂_x C_{n-1} + a_{n+1} ∂_x C_{n+1})
                  + (E/v_t)(a_n C_{n-1} - a_{n+1} C_{n+1}).

        Indices: C_{-1} = 0, C_{N} = 0 (closure by truncation).
        """
        N, Nx = C.shape
        # ∂_x C_n via FFT
        C_hat = np.fft.fft(C, axis=1)
        dxC = np.real(np.fft.ifft(1j * self.k[None, :] * C_hat, axis=1))

        rho = self.density(C)
        E = self.poisson(rho)

        dC = np.zeros_like(C)
        for n in range(N):
            a_n = self.a[n]
            a_np1 = self.a[n + 1]
            term_adv = 0.0
            term_acc = 0.0
            if n - 1 >= 0:
                term_adv = term_adv + a_n * dxC[n - 1]
                term_acc = term_acc + a_n * C[n - 1]
            if n + 1 < N:
                term_adv = term_adv + a_np1 * dxC[n + 1]
                term_acc = term_acc - a_np1 * C[n + 1]
            dC[n] = -self.v_t * term_adv + (E / self.v_t) * term_acc
        if self.nu > 0:
            n_idx = np.arange(N)
            damp = self.nu * (n_idx / max(N - 1, 1)) ** self.nu_power
            dC = dC - damp[:, None] * C
        return dC, E

    def step_rk4(self, C, dt):
        k1, E1 = self.rhs(C)
        k2, _ = self.rhs(C + 0.5 * dt * k1)
        k3, _ = self.rhs(C + 0.5 * dt * k2)
        k4, _ = self.rhs(C + dt * k3)
        C_new = C + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        return C_new, E1

    def run(self, C0, T, dt, diag_every=1):
        nsteps = int(np.round(T / dt))
        diag = {
            "t": [], "mass": [], "momentum": [], "ekin": [],
            "efield": [], "l2": [], "total_energy": [],
            "E_max": [], "E_l2": [],
        }
        C = C0.copy()
        for step in range(nsteps + 1):
            t = step * dt
            if step % diag_every == 0 or step == nsteps:
                rho = self.density(C)
                E = self.poisson(rho)
                ekin = self.kinetic_energy(C)
                ef = self.field_energy(E)
                mom = np.sum(self.momentum(C)) * self.dx
                mass = self.total_mass(C)
                l2 = self.l2_norm(C)
                diag["t"].append(t)
                diag["mass"].append(mass)
                diag["momentum"].append(mom)
                diag["ekin"].append(ekin)
                diag["efield"].append(ef)
                diag["l2"].append(l2)
                diag["total_energy"].append(ekin + ef)
                diag["E_max"].append(np.max(np.abs(E)))
                diag["E_l2"].append(np.sqrt(2.0 * ef))
            if step == nsteps:
                break
            C, _ = self.step_rk4(C, dt)
        for k in diag:
            diag[k] = np.array(diag[k])
        return C, diag


# ---- Standard initial conditions --------------------------------------------

def landau_ic(alpha=0.01, k=0.5, v_t=1.0):
    """f0(x,v) = (1 + α cos(k x)) * (1/√(2π v_t^2)) exp(-v^2/(2 v_t^2)).
    Domain in x: [0, 2π/k]."""
    def f(x, v):
        return (1.0 + alpha * np.cos(k * x)) * (1.0 / np.sqrt(2 * np.pi * v_t ** 2)) \
            * np.exp(-v ** 2 / (2 * v_t ** 2))
    L = 2 * np.pi / k
    return f, L


def two_stream_ic(alpha=0.05, k=0.5, v_t=1.0, v_b=2.0):
    """Symmetric two-stream:
    f0 = (1 + α cos(k x)) * 0.5 [g(v - v_b) + g(v + v_b)] with g a Maxwellian."""
    def f(x, v):
        g_plus = (1.0 / np.sqrt(2 * np.pi * v_t ** 2)) * np.exp(-(v - v_b) ** 2 / (2 * v_t ** 2))
        g_minus = (1.0 / np.sqrt(2 * np.pi * v_t ** 2)) * np.exp(-(v + v_b) ** 2 / (2 * v_t ** 2))
        return (1.0 + alpha * np.cos(k * x)) * 0.5 * (g_plus + g_minus)
    L = 2 * np.pi / k
    return f, L


def two_stream_classical_ic(alpha=0.05, k=0.5, v0=2.4):
    """Classical two-stream of Filbet & Sonnendrücker (J. Comput. Phys.):
    f0(x,v) = (2/sqrt(2π)) v^2 exp(-v^2/2) (1 + α cos(k x))
    Linear growth rate γ ≈ 0.2845 for k=0.5 (well documented).
    """
    def f(x, v):
        return (2.0 / np.sqrt(2 * np.pi)) * v ** 2 * np.exp(-v ** 2 / 2.0) * (1.0 + alpha * np.cos(k * x))
    L = 2 * np.pi / k
    return f, L
