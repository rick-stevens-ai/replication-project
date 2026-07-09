"""
Independent 2D SWE solver + MMS convergence study to reproduce paper's Fig 5.

Paper: Bisht et al. 2026 (OSTI 3013688) "Development of a River Dynamical Core..."
Section 3.2 (MMS) + Appendix F (source terms).

Manufactured solutions on domain (0, Lx) x (0, Ly), Lx=Ly=5 m:
  h(x,y,t) = H (1 + sin(pi*x/Lx) * sin(pi*y/Ly)) * exp(t/T)
  u(x,y,t) = U cos(pi*x/Lx) * sin(pi*y/Ly) * exp(t/T)
  v(x,y,t) = V sin(pi*x/Lx) * cos(pi*y/Ly) * exp(t/T)
  z(x,y)   = Z sin(pi*x/Lx) * sin(pi*y/Ly)
  n(x,y)   = N (1 + sin(pi*x/Lx) * sin(pi*y/Ly))

with H=0.005 m, U=V=0.025 m/s, T=20 s, Z=0.0025 m, N=0.01 (Manning), Lx=Ly=5 m.
Bottom drag C_D = 0 in paper (Manning-only friction; see Eq. F.13-F.14 the
    C_D u sqrt(...) term coexists WITH the Manning g*n^2/h^(1/3) term. We
    assume paper's default is CD=0, only Manning turned on — matches
    Appendix E convention for the verification tests.)

Numerics (matching paper Sec. 2 declared method):
  - First-order finite-volume, cell-centered, uniform Cartesian.
  - Roe approximate Riemann solver at each face (x and y faces).
  - Bed-slope source via well-balanced quiescent-flow style: -g*h*grad(z)
    evaluated with cell-centered values (paper uses PETSc/DMPlex quiescent-
    balancing; for a spot-check we use the standard cell-centered
    approximation, which is asymptotically first-order).
  - Manning friction: semi-implicit on momentum (paper's convention).
  - Explicit forward Euler in time with CFL = 0.3.
  - MMS source terms S_h, S_hu, S_hv from Appendix F added to RHS every step.
  - Dirichlet boundary conditions from manufactured solution at all edges
    (paper's MMS driver uses spatiotemporally varying BCs).

Runs to t_final = 1.0 s (short enough for tractable CPU time yet many
Euler steps to expose the discretization error; the paper does not state
its t_final for MMS but the exp(t/T) factor with T=20 s makes the solution
evolve smoothly and non-trivially over any O(1 s) window).

Reports L1, L2, Linf error norms for h, hu, hv at four grids and fits
the L1 slope by least-squares regression on log(dx).
"""

import numpy as np
import json
import sys
import time as _time

# ------------------------------ constants ---------------------------------
G   = 9.81
H0  = 0.005
U0  = 0.025
V0  = 0.025
T0  = 20.0
Z0  = 0.0025
N0  = 0.01
LX  = 5.0
LY  = 5.0
CD  = 0.0     # Manning-only (per paper; Chezy CD term left off)
PI  = np.pi

# ------------------------- manufactured solution --------------------------
def mms_h(x, y, t):
    return H0 * (1.0 + np.sin(PI*x/LX) * np.sin(PI*y/LY)) * np.exp(t/T0)

def mms_u(x, y, t):
    return U0 * np.cos(PI*x/LX) * np.sin(PI*y/LY) * np.exp(t/T0)

def mms_v(x, y, t):
    return V0 * np.sin(PI*x/LX) * np.cos(PI*y/LY) * np.exp(t/T0)

def mms_z(x, y):
    return Z0 * np.sin(PI*x/LX) * np.sin(PI*y/LY)

def mms_n(x, y):
    return N0 * (1.0 + np.sin(PI*x/LX) * np.sin(PI*y/LY))

# ---------- analytic derivatives (Appendix F) -----------------------------
def dh_dx(x, y, t):
    return (PI * H0 / LX) * np.cos(PI*x/LX) * np.sin(PI*y/LY) * np.exp(t/T0)

def dh_dy(x, y, t):
    return (PI * H0 / LY) * np.sin(PI*x/LX) * np.cos(PI*y/LY) * np.exp(t/T0)

def dh_dt(x, y, t):
    return mms_h(x, y, t) / T0

def du_dx(x, y, t):
    return -(PI * U0 / LX) * np.sin(PI*x/LX) * np.sin(PI*y/LY) * np.exp(t/T0)

def du_dy(x, y, t):
    return (PI * U0 / LY) * np.cos(PI*x/LX) * np.cos(PI*y/LY) * np.exp(t/T0)

def du_dt(x, y, t):
    return mms_u(x, y, t) / T0

def dv_dx(x, y, t):
    return (PI * V0 / LX) * np.cos(PI*x/LX) * np.cos(PI*y/LY) * np.exp(t/T0)

def dv_dy(x, y, t):
    return -(PI * V0 / LY) * np.sin(PI*x/LX) * np.sin(PI*y/LY) * np.exp(t/T0)

def dv_dt(x, y, t):
    return mms_v(x, y, t) / T0

def dz_dx(x, y):
    return (Z0 * PI / LX) * np.cos(PI*x/LX) * np.sin(PI*y/LY)

def dz_dy(x, y):
    return (Z0 * PI / LY) * np.sin(PI*x/LX) * np.cos(PI*y/LY)

# ---------- MMS source terms (Appendix F.12-F.14) -------------------------
def source_h(x, y, t):
    h  = mms_h(x, y, t)
    u  = mms_u(x, y, t)
    v  = mms_v(x, y, t)
    return (h / T0) + u * dh_dx(x,y,t) + h * du_dx(x,y,t) \
                    + v * dh_dy(x,y,t) + h * dv_dy(x,y,t)

def source_hu(x, y, t):
    """Appendix F.13 (x-momentum source).

    S_hu = u*dh/dt + h*du/dt
         + u^2*dh/dx + 2hu*du/dx + gh*dh/dx
         + uv*dh/dy + hv*du/dy + hu*dv/dy
         + gh*dz/dx + g*n^2/h^(1/3) * u * sqrt(u^2+v^2)
    """
    h  = mms_h(x, y, t)
    u  = mms_u(x, y, t)
    v  = mms_v(x, y, t)
    n  = mms_n(x, y)
    term_t = u * dh_dt(x,y,t) + h * du_dt(x,y,t)
    term_x = (u*u) * dh_dx(x,y,t) + 2.0*h*u * du_dx(x,y,t) + G * h * dh_dx(x,y,t)
    term_y = (u*v) * dh_dy(x,y,t) + h*v * du_dy(x,y,t) + h*u * dv_dy(x,y,t)
    bed    = G * h * dz_dx(x, y)
    fric   = G * n*n / (h**(1.0/3.0)) * u * np.sqrt(u*u + v*v + 1e-30)
    return term_t + term_x + term_y + bed + fric

def source_hv(x, y, t):
    """Appendix F.14 (y-momentum source).

    S_hv = v*dh/dt + h*dv/dt
         + vu*dh/dx + hu*dv/dx + hv*du/dx
         + v^2*dh/dy + 2hv*dv/dy + gh*dh/dy
         + gh*dz/dy + g*n^2/h^(1/3) * v * sqrt(u^2+v^2)
    """
    h  = mms_h(x, y, t)
    u  = mms_u(x, y, t)
    v  = mms_v(x, y, t)
    n  = mms_n(x, y)
    term_t = v * dh_dt(x,y,t) + h * dv_dt(x,y,t)
    term_x = (v*u) * dh_dx(x,y,t) + h*u * dv_dx(x,y,t) + h*v * du_dx(x,y,t)
    term_y = (v*v) * dh_dy(x,y,t) + 2.0*h*v * dv_dy(x,y,t) + G * h * dh_dy(x,y,t)
    bed    = G * h * dz_dy(x, y)
    fric   = G * n*n / (h**(1.0/3.0)) * v * np.sqrt(u*u + v*v + 1e-30)
    return term_t + term_x + term_y + bed + fric

# ------------------------------ Roe flux ---------------------------------
def roe_flux_1d(hL, huL, hR, huR):
    """1D SWE Roe flux F = (hu, hu^2 + 1/2 g h^2). Also returns |A|."""
    # Positivity guard
    hL = max(hL, 1e-12); hR = max(hR, 1e-12)
    uL = huL / hL; uR = huR / hR
    # Roe averages
    sqhL = np.sqrt(hL); sqhR = np.sqrt(hR)
    hRoe = 0.5 * (hL + hR)
    uRoe = (sqhL*uL + sqhR*uR) / (sqhL + sqhR)
    cRoe = np.sqrt(G * hRoe)
    # Wave speeds
    lam1 = uRoe - cRoe
    lam2 = uRoe + cRoe
    # Physical fluxes
    FL = np.array([huL, huL*uL + 0.5*G*hL*hL])
    FR = np.array([huR, huR*uR + 0.5*G*hR*hR])
    # Delta U
    dU = np.array([hR - hL, huR - huL])
    # Wave strengths
    alpha1 = ((uRoe + cRoe) * dU[0] - dU[1]) / (2.0 * cRoe)
    alpha2 = (-(uRoe - cRoe) * dU[0] + dU[1]) / (2.0 * cRoe)
    # Eigenvectors
    r1 = np.array([1.0, lam1])
    r2 = np.array([1.0, lam2])
    # Roe flux
    return 0.5 * (FL + FR) - 0.5 * (abs(lam1) * alpha1 * r1 + abs(lam2) * alpha2 * r2)

def roe_flux_x_vec(hL, huL, hvL, hR, huR, hvR):
    """Vectorized Roe flux across x-faces (2D SWE). All inputs are ndarrays.
    Returns (Fh, Fhu, Fhv) each same shape as inputs."""
    hL = np.maximum(hL, 1e-12); hR = np.maximum(hR, 1e-12)
    uL = huL / hL; vL = hvL / hL
    uR = huR / hR; vR = hvR / hR
    sqhL = np.sqrt(hL); sqhR = np.sqrt(hR)
    hRoe = 0.5 * (hL + hR)
    uRoe = (sqhL*uL + sqhR*uR) / (sqhL + sqhR)
    vRoe = (sqhL*vL + sqhR*vR) / (sqhL + sqhR)
    cRoe = np.sqrt(G * hRoe)
    lam1 = uRoe - cRoe
    lam3 = uRoe + cRoe
    # Physical fluxes across x-face
    Fh_L  = huL;                       Fh_R  = huR
    Fhu_L = huL*uL + 0.5*G*hL*hL;      Fhu_R = huR*uR + 0.5*G*hR*hR
    Fhv_L = huL*vL;                    Fhv_R = huR*vR
    dh    = hR - hL
    dhu   = huR - huL
    dhv   = hvR - hvL
    alpha1 = 0.5 * (dh - (dhu - uRoe*dh) / cRoe)
    alpha2 = dhv - vRoe * dh
    alpha3 = 0.5 * (dh + (dhu - uRoe*dh) / cRoe)
    # eigenvectors (only nonzero components needed)
    # r1 = (1, uRoe-c, vRoe), r2 = (0,0,1), r3 = (1, uRoe+c, vRoe)
    diss_h  = np.abs(lam1)*alpha1*1.0    + 0.0                    + np.abs(lam3)*alpha3*1.0
    diss_hu = np.abs(lam1)*alpha1*lam1   + 0.0                    + np.abs(lam3)*alpha3*lam3
    diss_hv = np.abs(lam1)*alpha1*vRoe   + np.abs(uRoe)*alpha2*1.0 + np.abs(lam3)*alpha3*vRoe
    Fh  = 0.5*(Fh_L + Fh_R)   - 0.5*diss_h
    Fhu = 0.5*(Fhu_L + Fhu_R) - 0.5*diss_hu
    Fhv = 0.5*(Fhv_L + Fhv_R) - 0.5*diss_hv
    return Fh, Fhu, Fhv


def roe_flux_y_vec(hL, huL, hvL, hR, huR, hvR):
    """Vectorized Roe flux across y-faces. Analog of the x-face version."""
    hL = np.maximum(hL, 1e-12); hR = np.maximum(hR, 1e-12)
    uL = huL / hL; vL = hvL / hL
    uR = huR / hR; vR = hvR / hR
    sqhL = np.sqrt(hL); sqhR = np.sqrt(hR)
    hRoe = 0.5 * (hL + hR)
    uRoe = (sqhL*uL + sqhR*uR) / (sqhL + sqhR)
    vRoe = (sqhL*vL + sqhR*vR) / (sqhL + sqhR)
    cRoe = np.sqrt(G * hRoe)
    lam1 = vRoe - cRoe
    lam3 = vRoe + cRoe
    Gh_L  = hvL;                       Gh_R  = hvR
    Ghu_L = hvL*uL;                    Ghu_R = hvR*uR
    Ghv_L = hvL*vL + 0.5*G*hL*hL;      Ghv_R = hvR*vR + 0.5*G*hR*hR
    dh    = hR - hL
    dhu   = huR - huL
    dhv   = hvR - hvL
    alpha1 = 0.5 * (dh - (dhv - vRoe*dh) / cRoe)
    alpha2 = dhu - uRoe * dh
    alpha3 = 0.5 * (dh + (dhv - vRoe*dh) / cRoe)
    # r1 = (1, uRoe, vRoe-c), r2 = (0,1,0), r3 = (1, uRoe, vRoe+c)
    diss_h  = np.abs(lam1)*alpha1*1.0     + 0.0                    + np.abs(lam3)*alpha3*1.0
    diss_hu = np.abs(lam1)*alpha1*uRoe    + np.abs(vRoe)*alpha2*1.0 + np.abs(lam3)*alpha3*uRoe
    diss_hv = np.abs(lam1)*alpha1*lam1    + 0.0                    + np.abs(lam3)*alpha3*lam3
    Gh  = 0.5*(Gh_L + Gh_R)   - 0.5*diss_h
    Ghu = 0.5*(Ghu_L + Ghu_R) - 0.5*diss_hu
    Ghv = 0.5*(Ghv_L + Ghv_R) - 0.5*diss_hv
    return Gh, Ghu, Ghv

# ------------------------------ solver -----------------------------------
def run_mms(dx, t_final=1.0, cfl=0.25, verbose=False):
    """Vectorized 2D SWE + MMS run at grid spacing dx. Returns error norms."""
    nx = int(round(LX / dx)); ny = int(round(LY / dx))
    xc = (np.arange(nx) + 0.5) * dx
    yc = (np.arange(ny) + 0.5) * dx
    X, Y = np.meshgrid(xc, yc, indexing='ij')  # shape (nx, ny)
    Z   = mms_z(X, Y)
    Nm  = mms_n(X, Y)
    # Initial condition = manufactured solution at t=0
    h  = mms_h(X, Y, 0.0)
    hu = h * mms_u(X, Y, 0.0)
    hv = h * mms_v(X, Y, 0.0)

    t  = 0.0
    step = 0
    while t < t_final - 1e-14:
        # CFL
        u = hu / h; v = hv / h
        c = np.sqrt(G * np.maximum(h, 1e-12))
        dt = cfl * dx / (np.max(np.abs(u) + c) + np.max(np.abs(v) + c) + 1e-12)
        if t + dt > t_final:
            dt = t_final - t

        # Ghost cells filled from MMS Dirichlet BCs at faces at time t (upwind BC data)
        hg  = np.pad(h,  1, mode='edge')
        hug = np.pad(hu, 1, mode='edge')
        hvg = np.pad(hv, 1, mode='edge')
        # Overwrite ghost row/col edges with manufactured solution at t
        # Left/right ghost columns (x boundaries)
        y_all = (np.arange(ny) + 0.5) * dx
        # left ghost x = -dx/2
        xg_left = -0.5 * dx
        h_l  = mms_h(xg_left, y_all, t)
        u_l  = mms_u(xg_left, y_all, t)
        v_l  = mms_v(xg_left, y_all, t)
        hg[0, 1:-1]  = h_l
        hug[0, 1:-1] = h_l * u_l
        hvg[0, 1:-1] = h_l * v_l
        # right ghost x = Lx + dx/2
        xg_right = LX + 0.5 * dx
        h_r  = mms_h(xg_right, y_all, t)
        u_r  = mms_u(xg_right, y_all, t)
        v_r  = mms_v(xg_right, y_all, t)
        hg[-1, 1:-1]  = h_r
        hug[-1, 1:-1] = h_r * u_r
        hvg[-1, 1:-1] = h_r * v_r
        # bottom/top ghost rows (y boundaries)
        x_all = (np.arange(nx) + 0.5) * dx
        yg_bot = -0.5 * dx
        h_b = mms_h(x_all, yg_bot, t)
        u_b = mms_u(x_all, yg_bot, t)
        v_b = mms_v(x_all, yg_bot, t)
        hg[1:-1, 0]  = h_b
        hug[1:-1, 0] = h_b * u_b
        hvg[1:-1, 0] = h_b * v_b
        yg_top = LY + 0.5 * dx
        h_t = mms_h(x_all, yg_top, t)
        u_t = mms_u(x_all, yg_top, t)
        v_t = mms_v(x_all, yg_top, t)
        hg[1:-1, -1]  = h_t
        hug[1:-1, -1] = h_t * u_t
        hvg[1:-1, -1] = h_t * v_t

        # ------------- x-face fluxes (nx+1 by ny) -----------------
        # x-face i (i=0..nx): left = hg[i,   1:-1], right = hg[i+1, 1:-1]
        hL  = hg[:-1, 1:-1];  huL = hug[:-1, 1:-1];  hvL = hvg[:-1, 1:-1]
        hR  = hg[1:,  1:-1];  huR = hug[1:,  1:-1];  hvR = hvg[1:,  1:-1]
        Fx_h, Fx_hu, Fx_hv = roe_flux_x_vec(hL, huL, hvL, hR, huR, hvR)

        # ------------- y-face fluxes (nx by ny+1) -----------------
        # y-face j (j=0..ny): left = hg[1:-1, j], right = hg[1:-1, j+1]
        hL  = hg[1:-1, :-1];  huL = hug[1:-1, :-1];  hvL = hvg[1:-1, :-1]
        hR  = hg[1:-1, 1:];   huR = hug[1:-1, 1:];   hvR = hvg[1:-1, 1:]
        Fy_h, Fy_hu, Fy_hv = roe_flux_y_vec(hL, huL, hvL, hR, huR, hvR)

        # ------------- update (forward Euler with MMS source) -------
        # RHS = -(F_{i+1/2} - F_{i-1/2})/dx - (G_{j+1/2} - G_{j-1/2})/dy - bed + fric + MMS
        rhs_h  = -(Fx_h[1:] - Fx_h[:-1]) / dx - (Fy_h[:, 1:] - Fy_h[:, :-1]) / dx
        rhs_hu = -(Fx_hu[1:] - Fx_hu[:-1]) / dx - (Fy_hu[:, 1:] - Fy_hu[:, :-1]) / dx
        rhs_hv = -(Fx_hv[1:] - Fx_hv[:-1]) / dx - (Fy_hv[:, 1:] - Fy_hv[:, :-1]) / dx

        # Bed slope source (paper: -g*h*grad(z), cell-centered)
        # dz/dx cell-centered from analytic z (this is the paper's convention
        # since MMS uses the exact source terms)
        rhs_hu = rhs_hu - G * h * dz_dx(X, Y)
        rhs_hv = rhs_hv - G * h * dz_dy(X, Y)

        # MMS source terms (subtract to make manufactured soln exact)
        rhs_h  = rhs_h  + source_h(X, Y, t)
        rhs_hu = rhs_hu + source_hu(X, Y, t)
        rhs_hv = rhs_hv + source_hv(X, Y, t)

        # Explicit update on h
        h_new  = h + dt * rhs_h
        # Semi-implicit Manning friction on momentum:
        #   (hu)^{n+1} = (hu)* / (1 + dt * g * n^2 / h^(4/3) * |vel|)
        hu_star = hu + dt * rhs_hu
        hv_star = hv + dt * rhs_hv
        h_safe  = np.maximum(h_new, 1e-12)
        u_curr  = hu / np.maximum(h, 1e-12)
        v_curr  = hv / np.maximum(h, 1e-12)
        speed   = np.sqrt(u_curr*u_curr + v_curr*v_curr) + 1e-30
        fric_coef = G * Nm*Nm / (h_safe**(4.0/3.0)) * speed
        hu = hu_star / (1.0 + dt * fric_coef)
        hv = hv_star / (1.0 + dt * fric_coef)
        h  = h_new

        t += dt
        step += 1
        if verbose and step % 50 == 0:
            print(f"  step {step:5d} t={t:.4f} dt={dt:.5f} minh={h.min():.3e}")

    # Compare against manufactured solution at t_final
    h_exact  = mms_h(X, Y, t_final)
    u_exact  = mms_u(X, Y, t_final)
    v_exact  = mms_v(X, Y, t_final)
    hu_exact = h_exact * u_exact
    hv_exact = h_exact * v_exact

    area = dx * dx
    total_area = LX * LY

    def norms(sim, ex):
        d = np.abs(sim - ex)
        L1  = np.sum(d) * area / total_area
        L2  = np.sqrt(np.sum(d*d) * area / total_area)
        Li  = np.max(d)
        return L1, L2, Li

    L1h, L2h, Lih    = norms(h,  h_exact)
    L1hu, L2hu, Lihu = norms(hu, hu_exact)
    L1hv, L2hv, Lihv = norms(hv, hv_exact)

    return dict(dx=dx, nx=nx, ny=ny, t=t_final, steps=step,
                L1_h=L1h, L2_h=L2h, Linf_h=Lih,
                L1_hu=L1hu, L2_hu=L2hu, Linf_hu=Lihu,
                L1_hv=L1hv, L2_hv=L2hv, Linf_hv=Lihv)


def fit_slope(dx_list, err_list):
    """Least-squares slope of log(err) vs log(dx)."""
    x = np.log(np.array(dx_list))
    y = np.log(np.array(err_list))
    A = np.vstack([x, np.ones_like(x)]).T
    m, b = np.linalg.lstsq(A, y, rcond=None)[0]
    return m


if __name__ == "__main__":
    # Grid list (paper uses 0.5, 0.25, 0.125, 0.0625)
    # For runtime tractability with un-vectorized flux loop, we do 3 grids:
    #   dx = 0.5, 0.25, 0.125  (already fits a clean line)
    # 0.0625 optional if time permits.
    dx_list = [0.5, 0.25, 0.125]
    if "--fine" in sys.argv:
        dx_list = [0.5, 0.25, 0.125, 0.0625]

    t_final = 0.5
    if "--t" in sys.argv:
        idx = sys.argv.index("--t")
        t_final = float(sys.argv[idx + 1])

    results = []
    t0 = _time.time()
    for dx in dx_list:
        print(f"[run] dx = {dx} m ... ", flush=True)
        rt0 = _time.time()
        r = run_mms(dx, t_final=t_final, cfl=0.25)
        rt1 = _time.time()
        r["wall_seconds"] = rt1 - rt0
        print(f"  N={r['nx']}x{r['ny']} steps={r['steps']} wall={r['wall_seconds']:.1f}s "
              f"L1_h={r['L1_h']:.3e} L1_hu={r['L1_hu']:.3e} L1_hv={r['L1_hv']:.3e}",
              flush=True)
        results.append(r)

    # Fit slopes
    slope_L1_h  = fit_slope([r["dx"] for r in results], [r["L1_h"]  for r in results])
    slope_L1_hu = fit_slope([r["dx"] for r in results], [r["L1_hu"] for r in results])
    slope_L1_hv = fit_slope([r["dx"] for r in results], [r["L1_hv"] for r in results])
    slope_L2_h  = fit_slope([r["dx"] for r in results], [r["L2_h"]  for r in results])
    slope_L2_hu = fit_slope([r["dx"] for r in results], [r["L2_hu"] for r in results])
    slope_L2_hv = fit_slope([r["dx"] for r in results], [r["L2_hv"] for r in results])
    slope_Li_h  = fit_slope([r["dx"] for r in results], [r["Linf_h"]  for r in results])
    slope_Li_hu = fit_slope([r["dx"] for r in results], [r["Linf_hu"] for r in results])
    slope_Li_hv = fit_slope([r["dx"] for r in results], [r["Linf_hv"] for r in results])

    print()
    print("=== MMS convergence rates (fitted slope of log(err) vs log(dx)) ===")
    print(f" h  : L1 slope = {slope_L1_h:.3f}  L2 slope = {slope_L2_h:.3f}  Linf = {slope_Li_h:.3f}")
    print(f" hu : L1 slope = {slope_L1_hu:.3f}  L2 slope = {slope_L2_hu:.3f}  Linf = {slope_Li_hu:.3f}")
    print(f" hv : L1 slope = {slope_L1_hv:.3f}  L2 slope = {slope_L2_hv:.3f}  Linf = {slope_Li_hv:.3f}")

    print(f"\nPaper Fig 5 reported slopes: h L1=0.95 L2=0.96 Linf=0.94")
    print(f"                              hu L1=0.92 L2=0.93 Linf=0.78")
    print(f"                              hv L1=0.92 L2=0.93 Linf=0.78")
    print(f"\ntotal wall time: {_time.time()-t0:.1f} s")

    out = dict(t_final=t_final, cfl=0.25, runs=results,
               slopes=dict(L1_h=slope_L1_h, L1_hu=slope_L1_hu, L1_hv=slope_L1_hv,
                           L2_h=slope_L2_h, L2_hu=slope_L2_hu, L2_hv=slope_L2_hv,
                           Linf_h=slope_Li_h, Linf_hu=slope_Li_hu, Linf_hv=slope_Li_hv),
               paper_slopes=dict(L1_h=0.95, L1_hu=0.92, L1_hv=0.92,
                                 L2_h=0.96, L2_hu=0.93, L2_hv=0.93,
                                 Linf_h=0.94, Linf_hu=0.78, Linf_hv=0.78))
    with open("mms_results.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nwrote mms_results.json")
