"""
Lightning-style Helmholtz solver (Python).

Core idea (Gopal-Trefethen 2019, PNAS 116:10223): the same pole-clustering trick
that gives root-exponential convergence for Laplace extends to Helmholtz.  The
Laplace basis

   u(z) = Re  sum_j a_j / (z - p_j)     with p_j exponentially clustered
          near each corner,

becomes for the Helmholtz equation (Delta + k^2) u = 0 :

   u(z) = sum_j  a_j * Y0( k |z - p_j| )         (real-valued near-field basis)
        + poly,   with Y0 = Bessel function of the second kind (singular at p_j).

Equivalently in free-space fundamental solutions language, we place exponentially
clustered sources outside the domain near each corner and use the Method of
Fundamental Solutions (MFS).  Here we use the real fundamental solution Y0(k r)
so that linear combinations are real-valued when boundary data is real.
We add a polynomial (Vekua-style Fourier-Bessel) basis
  { J_n(k r) cos(n theta), J_n(k r) sin(n theta) }  n=0..N
as the "smooth" part, analogous to the Arnoldi-polynomial term for Laplace.

Tested on: L-shape with manufactured solution
   u_exact(x,y) = J0(k*r1) + J0(k*r2)          (satisfies Helmholtz)
with r1, r2 measured from two source points *outside* the domain.
"""
from __future__ import annotations
import numpy as np
from scipy.special import j0, jn, y0
from pathlib import Path
import time

# -------------------------------------------------------------------
# Geometry: L-shape (complex corners, same as laplace.m's 'L')
#    vertices 2, 2+i, 1+i, 1+2i, 2i, 0  (counterclockwise)
# The reentrant corner is at 1+i with interior angle 3pi/2.
# -------------------------------------------------------------------
L_CORNERS = np.array([2, 2+1j, 1+1j, 1+2j, 2j, 0], dtype=complex)


def outward_normals(corners):
    n = len(corners)
    out = np.zeros(n, dtype=complex)
    for k in range(n):
        fwd = corners[(k+1) % n] - corners[k]
        bwd = corners[(k-1) % n] - corners[k]
        # bisector pointing *outward* of convex hull: -(fwd_u + bwd_u)
        fu = fwd/abs(fwd); bu = bwd/abs(bwd)
        tmp = 1j * bu * np.sqrt(-fu/bu)
        out[k] = tmp/abs(tmp)
    return out


def sample_boundary(corners, pts_per_side=120):
    """Sample points along polygon boundary, clustered near corners (sqrt spacing)."""
    Zs, sides = [], []
    n = len(corners)
    # Chebyshev-cluster to resolve near-corner behaviour
    s = (1 - np.cos(np.linspace(1e-10, 1-1e-10, pts_per_side)))/2
    for k in range(n):
        a = corners[k]; b = corners[(k+1) % n]
        Zk = a + s*(b-a)
        Zs.append(Zk); sides.append(np.full_like(Zk, k, dtype=int))
    return np.concatenate(Zs), np.concatenate(sides)


def cluster_poles(corners, n_per_corner=50, sigma=4.0, scale=None):
    """Exponentially clustered source points outside domain, near each corner.

    Follows laplace.m:  d_k = scale * exp( sigma*(sqrt(j) - sqrt(N)) ),  j=1..N
    """
    if scale is None:
        wr = corners.real; wi = corners.imag
        scale = max(wr.max()-wr.min(), wi.max()-wi.min())
    out = outward_normals(corners)
    poles = []
    for k, v in enumerate(corners):
        j = np.arange(1, n_per_corner+1)
        dk = scale * np.exp(sigma*(np.sqrt(j) - np.sqrt(n_per_corner)))
        poles.append(v + out[k]*dk)
    return np.concatenate(poles)


# ---- Helmholtz basis evaluation -----------------------------------

def helmholtz_basis(Z, poles, k, poly_deg=8, wc=None):
    """Build least-squares matrix A and bookkeeping for Helmholtz basis.

    Parameters
    ----------
    Z       : (M,) complex sample points
    poles   : (P,) complex source points outside domain
    k       : wavenumber
    poly_deg: Fourier-Bessel degree N (uses modes n=0..N)
    wc      : complex center (for polar coords of smooth part)

    Basis (all real-valued on Z):
      - poles:  Y0(k |Z - p_j|)                          P columns
      - Fourier-Bessel smooth part about wc:
          J0(k*r),  Jn(k*r) cos(n*theta), Jn(k*r) sin(n*theta), n=1..N
                                                        (2N+1) columns
    """
    if wc is None:
        wc = Z.mean()
    # Pole columns: real fundamental solutions, singular *at* the outside poles
    # (so they look like r^0-log near each pole; for Helmholtz, Y0 ~ (2/pi)log).
    # Displacement
    d = Z[:, None] - poles[None, :]            # (M, P)
    r = np.abs(d)
    # Avoid r=0 (poles are outside boundary so should be strictly >0)
    Apole = y0(k*r)                            # (M, P)

    # Smooth part: Fourier-Bessel
    Zc = Z - wc
    rc = np.abs(Zc)
    th = np.angle(Zc)
    cols = [j0(k*rc)]
    for n in range(1, poly_deg+1):
        Jn = jn(n, k*rc)
        cols.append(Jn*np.cos(n*th))
        cols.append(Jn*np.sin(n*th))
    Asmooth = np.column_stack(cols)            # (M, 2N+1)

    A = np.hstack([Asmooth, Apole])
    return A, wc


def solve_helmholtz(corners, g_func, k, n_per_corner=40, poly_deg=8,
                    sigma=4.0, pts_per_side=120):
    Z, sides = sample_boundary(corners, pts_per_side=pts_per_side)
    poles = cluster_poles(corners, n_per_corner=n_per_corner, sigma=sigma)
    # Drop poles that happen to land inside polygon (shouldn't for L-shape if sigma ok)
    from matplotlib.path import Path as MplPath
    poly = MplPath(np.column_stack([corners.real, corners.imag]))
    inside = poly.contains_points(np.column_stack([poles.real, poles.imag]))
    poles = poles[~inside]

    # Weight points near corners (relative error weighting)
    # Identify nearest corner for each Z
    dd = np.abs(Z[:,None] - corners[None,:])
    nearest = dd.min(axis=1)
    scale = max(np.ptp(corners.real), np.ptp(corners.imag))
    wt = nearest/scale
    # Floor to avoid zero weight
    wt = np.maximum(wt, 1e-4)

    A, wc = helmholtz_basis(Z, poles, k, poly_deg=poly_deg)
    G = g_func(Z)

    W = wt[:, None]
    coef, *_ = np.linalg.lstsq(W*A, wt*G, rcond=None)
    u_approx = A @ coef

    # Boundary errors
    err_raw  = np.max(np.abs(u_approx - G))
    err_wtd  = np.max(wt*np.abs(u_approx - G))

    def u(zz):
        zz = np.atleast_1d(zz)
        AA, _ = helmholtz_basis(zz, poles, k, poly_deg=poly_deg, wc=wc)
        return AA @ coef

    return dict(u=u, coef=coef, poles=poles, A=A, Z=Z, G=G,
                err_raw=err_raw, err_wtd=err_wtd, N=A.shape[1], M=A.shape[0])


# -------------------------------------------------------------------
# Manufactured solution and experiment
# -------------------------------------------------------------------
def make_exact(k, sources):
    """u_exact = sum J0(k |z - s|) for sources outside domain.  Satisfies
       (Delta+k^2) u = 0 inside the domain."""
    def u(z):
        z = np.asarray(z, dtype=complex)
        out = np.zeros(z.shape, dtype=float)
        for s in sources:
            out = out + j0(k*np.abs(z - s))
        return out
    return u


def run_convergence_sweep():
    # Manufactured Helmholtz solution on L-shape.
    # Put sources well outside the domain.
    sources = np.array([5+5j, -3-3j, 6-2j], dtype=complex)
    print('=== Lightning-Helmholtz on L-shape (Python MFS port) ===')
    rows = []
    for k in [1.0, 3.0, 10.0]:
        u_exact = make_exact(k, sources)
        print(f'\n-- wavenumber k = {k} --')
        for n_per_corner in [5, 10, 20, 40, 60, 80, 120]:
            poly_deg = max(8, int(2*k)+4)
            t0 = time.time()
            res = solve_helmholtz(L_CORNERS, u_exact, k,
                                  n_per_corner=n_per_corner,
                                  poly_deg=poly_deg,
                                  sigma=4.0,
                                  pts_per_side=max(80, 4*n_per_corner))
            t = time.time() - t0
            # Check at an interior test point
            zt = np.array([1.3 + 1.3j, 0.5+0.5j, 1.8+1.7j])
            u_num = res['u'](zt)
            u_ref = u_exact(zt)
            err_int = np.max(np.abs(u_num - u_ref))
            row = dict(k=k, n_per_corner=n_per_corner, N=res['N'], M=res['M'],
                       bnd_err=res['err_raw'], bnd_err_wtd=res['err_wtd'],
                       int_err=err_int, walltime=t, n_poles=len(res['poles']))
            rows.append(row)
            print(f'  Npc={n_per_corner:3d}  N={res["N"]:4d}  poles={len(res["poles"]):3d}'
                  f'  bnd_err={res["err_raw"]:.2e}  bnd_wtd={res["err_wtd"]:.2e}'
                  f'  int_err={err_int:.2e}  t={t:.2f}s')
    import csv
    with open(Path(__file__).parent/'exp4_helmholtz.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)


if __name__ == '__main__':
    run_convergence_sweep()
