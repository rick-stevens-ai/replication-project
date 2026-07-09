"""
Pure-Python re-implementation of the Lightning Laplace solver
(Gopal & Trefethen 2019, "New Laplace and Helmholtz solvers", arXiv:1902.00374).

Scope: enough to re-verify the paper's NUMERIC claims independently of MATLAB.
- Polygonal domains specified as a list of complex corners (counterclockwise).
- Pole basis: a_k / (z - z_k) with z_k clustered exponentially OUTSIDE each
  reentrant corner of the polygon (Newman / lightning configuration).
- Polynomial basis: b_j * z^j (centered at domain centroid for conditioning).
- Real harmonic representation: u(z) = Re( sum a_k/(z-z_k) + sum b_j z^j ).
- Boundary sampling: clustered toward each corner (tanh-style) with sample
  count per side scaled to N.
- Solve real least-squares (boundary residual) with numpy.linalg.lstsq.

This is intentionally a clean re-implementation rather than a 1:1 port of
laplace.m, so any agreement with the pass-1 MATLAB run is independent
evidence rather than re-running the same code.

Author: Ollie (subagent re-pass), 2026-06-23
"""

from __future__ import annotations

import math
import time
from dataclasses import dataclass

import numpy as np


# ---------------------------------------------------------------------------
# Polygon helpers
# ---------------------------------------------------------------------------

def lshape_corners() -> np.ndarray:
    """Standard L-shape used in Gopal & Trefethen 2019, Fig. 1.

    Vertices (counterclockwise), reentrant corner at z=1+1i:
        2, 2+1i, 1+1i, 1+2i, 2i, 0
    """
    return np.array(
        [2 + 0j, 2 + 1j, 1 + 1j, 1 + 2j, 0 + 2j, 0 + 0j],
        dtype=complex,
    )


def interior_angle(v_prev: complex, v: complex, v_next: complex) -> float:
    """Interior angle at vertex v of a CCW polygon, in radians."""
    a = v_prev - v
    b = v_next - v
    # CCW interior angle from edge (v->v_prev) sweeping to edge (v->v_next).
    ang = math.atan2((a.conjugate() * b).imag, (a.conjugate() * b).real)
    if ang <= 0:
        ang += 2 * math.pi
    return ang


def outward_normal_direction(v_prev: complex, v: complex, v_next: complex) -> complex:
    """Unit complex number pointing outward from the polygon at vertex v.

    For a CCW polygon, the exterior bisector at v is the inward bisector of
    the two outgoing edges (v->v_prev) and (v->v_next) reflected. We use the
    average of the two edge outward normals at v.
    """
    # Edge v -> v_next: tangent (v_next - v); outward normal = -i * tangent / |...|
    t1 = v_next - v
    n1 = -1j * t1 / abs(t1)
    # Edge v_prev -> v: tangent (v - v_prev); outward normal = -i * tangent / |...|
    t2 = v - v_prev
    n2 = -1j * t2 / abs(t2)
    n = n1 + n2
    if abs(n) < 1e-14:
        # straight angle; pick perpendicular to t1
        n = -1j * t1 / abs(t1)
    return n / abs(n)


def in_polygon(z: np.ndarray, corners: np.ndarray) -> np.ndarray:
    """Boolean mask: True if z lies strictly inside the CCW polygon."""
    from matplotlib.path import Path
    pts = np.stack([z.real, z.imag], axis=-1).reshape(-1, 2)
    poly = np.stack([corners.real, corners.imag], axis=-1)
    inside = Path(poly).contains_points(pts).reshape(z.shape)
    return inside


# ---------------------------------------------------------------------------
# Pole and boundary-sample placement
# ---------------------------------------------------------------------------

@dataclass
class PolePlacement:
    poles: np.ndarray            # complex pole locations (outside polygon)
    per_corner: list[int]        # number of poles at each corner index
    sigma: float                 # clustering parameter
    scale: float                 # geometric scale used for pole spacing
    corners: np.ndarray
    poly_degree: int             # N2 in eq (1)


def place_poles(
    corners: np.ndarray,
    n_per_corner: int,
    sigma: float = 4.0,
    scale: float | None = None,
    poly_degree: int = 20,
) -> PolePlacement:
    """Place exponentially-clustered poles outside each corner.

    Following Gopal-Trefethen, distances from corner are
        d_k = exp(-sigma * (sqrt(k) - sqrt(n_per_corner))) * scale,
    so the closest pole is roughly `scale` away and they cluster geometrically
    toward the corner with rate `sigma`.
    Pole is placed along the OUTWARD bisector of the corner.
    """
    nw = len(corners)
    if scale is None:
        # characteristic scale: typical edge length
        scale = float(np.mean(np.abs(np.diff(np.append(corners, corners[0])))))

    poles_all: list[complex] = []
    per_corner: list[int] = []
    for i in range(nw):
        v_prev = corners[(i - 1) % nw]
        v = corners[i]
        v_next = corners[(i + 1) % nw]
        n_out = outward_normal_direction(v_prev, v, v_next)
        # exponential clustering: k = 1..n_per_corner
        k = np.arange(1, n_per_corner + 1)
        # Distances from corner, monotonically decreasing toward the corner.
        d = np.exp(-sigma * (np.sqrt(n_per_corner) - np.sqrt(k))) * scale
        # Place at v + d * n_out
        pj = v + d * n_out
        poles_all.extend(pj.tolist())
        per_corner.append(n_per_corner)

    return PolePlacement(
        poles=np.array(poles_all, dtype=complex),
        per_corner=per_corner,
        sigma=sigma,
        scale=scale,
        corners=corners,
        poly_degree=poly_degree,
    )


def sample_boundary(
    corners: np.ndarray,
    samples_per_side: int,
    cluster: bool = True,
    cluster_distances: np.ndarray | None = None,
) -> np.ndarray:
    """Sample points on each polygon side; cluster toward endpoints if requested.

    If `cluster_distances` is provided (shape (K,)) we ALSO add sample points
    at distances matching the pole-clustering pattern from each endpoint of
    each side (mimicking the laplace.m pattern). This is critical when poles
    are placed very close (~1e-6) to the corner: linearly-spaced boundary
    samples cannot resolve a pole that close, so the LS fit degenerates.
    """
    nw = len(corners)
    pts = []
    for i in range(nw):
        a = corners[i]
        b = corners[(i + 1) % nw]
        side_len = abs(b - a)
        if cluster:
            s = np.arange(1, samples_per_side + 1) / (samples_per_side + 1)
            t = 0.5 * (1 - np.cos(np.pi * s))
        else:
            t = np.arange(1, samples_per_side + 1) / (samples_per_side + 1)
        side_pts = a + t * (b - a)
        pts.append(side_pts)
        if cluster_distances is not None:
            # Add extra clustered samples near BOTH endpoints (at distances
            # 1/3 d, 2/3 d, d for each pole spacing d).
            d = np.concatenate(
                [cluster_distances / 3, 2 * cluster_distances / 3,
                 cluster_distances]
            )
            d = d[(d > 0) & (d < side_len)]
            if d.size:
                tan_ab = (b - a) / side_len
                near_a = a + d * tan_ab
                near_b = b - d * tan_ab
                pts.append(near_a)
                pts.append(near_b)
    return np.concatenate(pts)


# ---------------------------------------------------------------------------
# Build & solve real least-squares system
# ---------------------------------------------------------------------------

def _arnoldi_basis(dz: np.ndarray, n: int) -> tuple[np.ndarray, np.ndarray]:
    """Arnoldi-orthogonalize the Krylov basis {1, dz, dz^2, ..., dz^n}.

    Returns (Q, H) where Q is M x (n+1) with complex orthonormal columns
    spanning the same space as Vandermonde columns of dz, and H is the
    Hessenberg matrix from the recurrence (used in evaluation).

    Cf. Brubeck-Nakatsukasa-Trefethen 'Vandermonde with Arnoldi' (SIAM Rev.
    2021), as used in laplace.m.
    """
    m = dz.shape[0]
    Q = np.zeros((m, n + 1), dtype=complex)
    H = np.zeros((n + 1, n), dtype=complex)
    Q[:, 0] = 1.0 / math.sqrt(m)
    for k in range(n):
        v = dz * Q[:, k]
        for j in range(k + 1):
            H[j, k] = np.vdot(Q[:, j], v)
            v = v - H[j, k] * Q[:, j]
        H[k + 1, k] = np.linalg.norm(v)
        if H[k + 1, k] < 1e-300:
            break
        Q[:, k + 1] = v / H[k + 1, k]
    return Q, H


def _arnoldi_eval(dz: np.ndarray, H: np.ndarray, m_train: int) -> np.ndarray:
    """Reproduce the Arnoldi Q on new points dz, given H and the training
    sample count m_train (so we can initialize Q[:,0] = 1/sqrt(m_train))."""
    n = H.shape[1]
    m = dz.shape[0]
    Q = np.zeros((m, n + 1), dtype=complex)
    Q[:, 0] = 1.0 / math.sqrt(m_train)
    for k in range(n):
        v = dz * Q[:, k]
        for j in range(k + 1):
            v = v - H[j, k] * Q[:, j]
        if H[k + 1, k] > 1e-300:
            Q[:, k + 1] = v / H[k + 1, k]
    return Q


def build_basis_matrix(
    z: np.ndarray,
    placement: PolePlacement,
    centroid: complex,
    arnoldi_H: np.ndarray | None = None,
    m_train: int | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """Real-valued boundary basis matrix.

    For each complex basis function f(z), unknowns are (Re c, Im c) and
    contributions to u = Re(c f(z)) are (Re f) and (-Im f).

    Polynomial part is constructed via Arnoldi orthogonalization of the
    scaled monomials in (z - centroid). If `arnoldi_H` is None, we build
    H from these training points and return it; else we re-apply it.
    """
    z = np.asarray(z, dtype=complex)
    cols: list[np.ndarray] = []

    # Rational (pole) part: a_k / (z - z_k)
    for zk in placement.poles:
        f = 1.0 / (z - zk)
        cols.append(f.real)
        cols.append(-f.imag)

    # Polynomial part via Arnoldi
    n = placement.poly_degree
    dz = z - centroid
    if arnoldi_H is None:
        Q, H = _arnoldi_basis(dz, n)
        m_train_out = z.shape[0]
    else:
        assert m_train is not None
        Q = _arnoldi_eval(dz, arnoldi_H, m_train)
        H = arnoldi_H
        m_train_out = m_train

    # First column (k=0) corresponds to the constant; take its real part only
    # (b_0 real per paper).
    cols.append(Q[:, 0].real)
    for k in range(1, n + 1):
        cols.append(Q[:, k].real)
        cols.append(-Q[:, k].imag)

    A = np.stack(cols, axis=1)
    return A, H


def evaluate_solution(
    z: np.ndarray,
    coeffs: np.ndarray,
    placement: PolePlacement,
    centroid: complex,
    arnoldi_H: np.ndarray,
    m_train: int,
) -> np.ndarray:
    """Evaluate u(z) = Re( ... ) at points z using coefficients from solve()."""
    A, _ = build_basis_matrix(z, placement, centroid,
                               arnoldi_H=arnoldi_H, m_train=m_train)
    return A @ coeffs


@dataclass
class SolveResult:
    coeffs: np.ndarray
    placement: PolePlacement
    centroid: complex
    samples: np.ndarray
    bnd_resid: np.ndarray
    max_bnd_err: float
    n_dof: int
    n_samples: int
    cond_estimate: float
    solve_time_s: float
    build_time_s: float
    arnoldi_H: np.ndarray = None
    m_train: int = 0


def solve_laplace(
    corners: np.ndarray,
    g,                          # callable: complex -> real, Dirichlet data
    n_per_corner: int = 12,
    samples_per_side: int = 80,
    poly_degree: int = 20,
    sigma: float = 4.0,
    centroid: complex | None = None,
) -> SolveResult:
    placement = place_poles(corners, n_per_corner, sigma=sigma,
                             poly_degree=poly_degree)
    # Cluster boundary samples at the same scales as the poles.
    # Distances per corner are exp(-sigma*(sqrt(n)-sqrt(k))) * scale.
    k_arr = np.arange(1, n_per_corner + 1)
    cluster_d = np.exp(-sigma * (math.sqrt(n_per_corner) - np.sqrt(k_arr))) * placement.scale
    Z = sample_boundary(corners, samples_per_side, cluster=True,
                         cluster_distances=cluster_d)
    if centroid is None:
        # Use centroid of bounding box, then nudge AWAY from any reentrant
        # corner so the polynomial expansion point is well inside.
        cx = 0.5 * (corners.real.min() + corners.real.max())
        cy = 0.5 * (corners.imag.min() + corners.imag.max())
        centroid = complex(cx, cy)
        # If centroid happens to coincide (within scale*0.05) with a corner,
        # shift it toward the interior centroid instead.
        dists = np.abs(centroid - corners)
        if dists.min() < 0.05 * placement.scale:
            interior_centroid = complex(corners.real.mean(), corners.imag.mean())
            centroid = 0.5 * (centroid + interior_centroid) + 1e-3 * placement.scale
            # final safety: if still at a corner, just use interior_centroid + 1e-2
            if np.min(np.abs(centroid - corners)) < 0.05 * placement.scale:
                centroid = interior_centroid + 0.1 * placement.scale

    t0 = time.perf_counter()
    A, H = build_basis_matrix(Z, placement, centroid)
    b = np.array([g(zi) for zi in Z], dtype=float)
    t1 = time.perf_counter()

    coeffs, residuals, rank, sv = np.linalg.lstsq(A, b, rcond=None)
    t2 = time.perf_counter()

    bnd_pred = A @ coeffs
    bnd_resid = bnd_pred - b
    max_bnd_err = float(np.max(np.abs(bnd_resid)))
    cond = float(sv[0] / sv[-1]) if sv[-1] > 0 else float('inf')

    return SolveResult(
        coeffs=coeffs,
        placement=placement,
        centroid=centroid,
        samples=Z,
        bnd_resid=bnd_resid,
        max_bnd_err=max_bnd_err,
        n_dof=A.shape[1],
        n_samples=A.shape[0],
        cond_estimate=cond,
        solve_time_s=t2 - t1,
        build_time_s=t1 - t0,
        arnoldi_H=H,
        m_train=Z.shape[0],
    )


# ---------------------------------------------------------------------------
# Convenience: evaluate at points (timed)
# ---------------------------------------------------------------------------

def evaluate_many(
    sol: SolveResult,
    points: np.ndarray,
) -> tuple[np.ndarray, float]:
    """Evaluate u at many points, return (values, wallclock_seconds)."""
    t0 = time.perf_counter()
    vals = evaluate_solution(points, sol.coeffs, sol.placement, sol.centroid,
                              sol.arnoldi_H, sol.m_train)
    t1 = time.perf_counter()
    return vals, t1 - t0


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    corners = lshape_corners()
    g = lambda z: z.real ** 2   # paper's default test BC
    sol = solve_laplace(corners, g, n_per_corner=18, samples_per_side=80,
                         poly_degree=24, sigma=4.0)
    print(f"DoFs={sol.n_dof}  samples={sol.n_samples}  "
          f"max_bnd_err={sol.max_bnd_err:.3e}  cond~{sol.cond_estimate:.2e}  "
          f"solve_s={sol.solve_time_s:.3f}")
    probe = np.array([0.99 + 0.99j])
    vals, t = evaluate_many(sol, probe)
    print(f"u(0.99,0.99) = {vals[0]:.13f}   (paper: 1.02679192610...)  "
          f"|err|={abs(vals[0]-1.02679192610731):.2e}   evalt={t:.4e}s")
