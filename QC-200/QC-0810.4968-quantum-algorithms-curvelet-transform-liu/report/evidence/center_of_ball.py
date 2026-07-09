"""Liu (2008) Algorithm 1 - center of a ball via quantum curvelet transform.

Setup: dimension n=2 (below Liu's n>=4 requirement for the heavy-tail asymptotics,
but the QUALITATIVE prediction -- that the curvelet basis identifies the wavefront
set of the ball, i.e. the normal direction to the sphere surface -- still applies
and is directly verifiable.).

Concretely: on an N x N grid (N=16, 32) build the indicator function f of a ball
of radius beta centered at c, prepare the quantum-sample state
     |psi> = (1/sqrt|B|) sum_{x in B} |x>,
apply the 2D discrete curvelet transform (which decomposes freq. plane into wedge
sectors labelled by (a, theta)), and check the marginal probability distribution
Pr[theta | measurement] concentrates on the ANGLES normal to the ball's surface --
which for a disk centered at the origin is UNIFORM over all directions (by rotational
symmetry). When the ball is off-center, curvelet-basis measurements should still yield
a b-value near the sphere surface and a theta-value pointing radially through c.

We measure two headline numbers:

    (A) Marginal norm captured by the DIRECTIONAL wedge sectors (the whole plane
        excluding the low-freq disk).  Liu's Sec 4 predicts that for a ball the
        overwhelming majority of the curvelet probability mass sits in these
        wedges (fhat of an indicator ball decays as J_1/r, mostly outside the
        low-freq disk once beta >> 1/lambda).  The rigorous claim (Theorem 3):
            integral over |k|<1/lambda of |fhat|^2 dk  <  pi^n / (n-1)  * eps^{n-1}
        We report the numerical value P_low = || fhat |_{|k|<1/lambda} ||^2
        / ||fhat||^2.

    (B) Line-through-center test. From a curvelet measurement (a, b, theta) with a in
        the finest scale, form the line L = { b + t * theta : t in R } and measure the
        distance dist(c, L) from the true center c.  Compare against random sampling
        (guessing a random point in the ball).  Averaging over many measurements from
        the curvelet distribution, is the mean distance smaller than random sampling
        would give?

We DO NOT claim to reproduce Liu's Omega(nu^3) constant -- that requires n>=4 and the
exact continuous window functions (Liu Sec 6.2 Case 2, which we did not implement).
This is a SPOT-CHECK in 2D of the mechanism.
"""
from __future__ import annotations
import json
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from classical_curvelet import dyadic_wedge_windows_2d, curvelet_2d


def indicator_ball_2d(N: int, center: tuple[float, float], radius: float) -> np.ndarray:
    xs = np.arange(N) - N / 2
    ys = np.arange(N) - N / 2
    X, Y = np.meshgrid(xs, ys, indexing="ij")
    mask = ((X - center[0]) ** 2 + (Y - center[1]) ** 2) <= radius ** 2
    f = mask.astype(complex)
    f /= np.linalg.norm(f)   # unit-norm quantum sample
    return f


def line_point_distance(b: np.ndarray, theta: np.ndarray, c: np.ndarray) -> float:
    """Perpendicular distance from point c to line {b + t theta}."""
    d = c - b
    # subtract component parallel to theta
    t_norm = theta / (np.linalg.norm(theta) + 1e-30)
    perp = d - np.dot(d, t_norm) * t_norm
    return float(np.linalg.norm(perp))


def sector_center_direction(chi_j: np.ndarray) -> np.ndarray:
    """Return unit vector at the centroid of frequency bins with chi_j > 0.
    This is the 'nominal direction theta' for that wedge sector.
    """
    N = chi_j.shape[0]
    kx = np.fft.fftfreq(N, d=1.0) * N
    ky = np.fft.fftfreq(N, d=1.0) * N
    KX, KY = np.meshgrid(kx, ky, indexing="ij")
    weight = chi_j
    total = weight.sum()
    if total == 0:
        return np.array([0.0, 0.0])
    cx = float((KX * weight).sum() / total)
    cy = float((KY * weight).sum() / total)
    norm = np.sqrt(cx**2 + cy**2)
    if norm < 1e-9:
        return np.array([0.0, 0.0])
    return np.array([cx / norm, cy / norm])


def run(N: int, center: tuple[float, float], radius: float, seed: int = 0, n_samples: int = 2000):
    rng = np.random.default_rng(seed)
    f = indicator_ball_2d(N, center, radius)
    chi = dyadic_wedge_windows_2d(N, num_scales=3, num_angles_at_finest=16)
    gamma = curvelet_2d(f, chi)  # shape (S, N, N)
    S = gamma.shape[0]

    # Probability distribution over (sector j, location b)
    probs = np.abs(gamma) ** 2  # (S, N, N)
    total = probs.sum()
    assert abs(total - 1.0) < 1e-10, f"probs don't sum to 1: {total}"

    # Marginal over sector
    marg_sector = probs.sum(axis=(1, 2))  # (S,)
    # sector 0 = low-freq disk
    p_low = float(marg_sector[0])
    p_directional = float(1.0 - p_low)

    # For each sector, the nominal direction
    directions = np.stack([sector_center_direction(chi[j]) for j in range(S)])  # (S, 2)

    # Sample (j, bx, by) according to probs and compute line-through-center metric
    flat = probs.flatten()
    idx = rng.choice(len(flat), size=n_samples, p=flat)
    js, bxs, bys = np.unravel_index(idx, probs.shape)
    # positions bx, by are integers in [0, N); relate to grid coordinates centered at 0:
    # remember our ball is centered at 'center' (in coord system where 0 is grid center)
    # and quantum output "b" indexes the DFT position, which is also 0..N-1 with fft ordering.
    # For visualization purposes we shift so that bx=N/2 corresponds to origin:
    b_coord = np.stack([bxs - N/2, bys - N/2], axis=1).astype(float)  # (n_samples, 2)
    c_arr = np.array(center)

    distances_curvelet = []
    for i in range(n_samples):
        j = js[i]
        if j == 0:  # low-freq: no direction, treat as random point
            distances_curvelet.append(np.linalg.norm(b_coord[i] - c_arr))
            continue
        theta = directions[j]
        if np.linalg.norm(theta) < 1e-9:
            distances_curvelet.append(np.linalg.norm(b_coord[i] - c_arr))
            continue
        distances_curvelet.append(line_point_distance(b_coord[i], theta, c_arr))

    # baseline: random point uniformly in the ball; distance is expected R/sqrt(3) or so
    rand_pts_in_ball = []
    while len(rand_pts_in_ball) < n_samples:
        candidate = rng.uniform(-radius, radius, size=2) + c_arr
        if np.linalg.norm(candidate - c_arr) <= radius:
            rand_pts_in_ball.append(np.linalg.norm(candidate - c_arr))
    distances_random_point = np.array(rand_pts_in_ball[:n_samples])

    return {
        "N": N,
        "num_sectors": int(S),
        "center": list(center),
        "radius": radius,
        "p_probability_low_freq_sector": p_low,
        "p_probability_directional_sectors": p_directional,
        "curvelet_line_distance_mean": float(np.mean(distances_curvelet)),
        "curvelet_line_distance_median": float(np.median(distances_curvelet)),
        "curvelet_line_distance_stddev": float(np.std(distances_curvelet)),
        "random_point_distance_mean": float(np.mean(distances_random_point)),
        "random_point_distance_median": float(np.median(distances_random_point)),
        "n_samples": n_samples,
        # success = fraction of measurements yielding a line within 1 grid unit of center
        "curvelet_success_prob_within_1_unit": float(np.mean(np.array(distances_curvelet) <= 1.0)),
        "random_success_prob_within_1_unit": float(np.mean(distances_random_point <= 1.0)),
        # success within radius (obvious - random should be 100% inside the ball)
        "curvelet_success_prob_within_half_radius": float(np.mean(np.array(distances_curvelet) <= radius/2)),
        "random_success_prob_within_half_radius": float(np.mean(distances_random_point <= radius/2)),
    }


if __name__ == "__main__":
    results = {}
    # Ball centered on grid center (0,0)
    for N, rad in [(16, 4.0), (32, 8.0)]:
        results[f"origin_N{N}_r{rad}"] = run(N, (0.0, 0.0), rad)
    # Ball off-center
    results["offcenter_N32_r6_at(3,-2)"] = run(32, (3.0, -2.0), 6.0)
    print(json.dumps(results, indent=2))
