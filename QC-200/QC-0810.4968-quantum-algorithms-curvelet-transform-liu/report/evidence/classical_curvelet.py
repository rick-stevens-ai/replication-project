"""Classical discrete curvelet transform (Liu 2008 eq. 14), 1D and 2D variants.

Liu's curvelet transform (arXiv:0810.4968 eq. 14) is:

    Gamma f(a, b, theta) = (sigma/(2L))^(n/2) * sum_k fhat(k) * chi_{a,theta}(k) * exp(2*pi*i*k.b)

with the KEY partition-of-unity constraint on the window family {chi_{a,theta}}:

    sum_{a,theta} |chi_{a,theta}(k)|^2 = 1  for all k in the frequency grid

(this is exactly what makes the curvelet transform a UNITARY on the joint
|k, a, theta> space, and hence quantum-realisable.)

Since the paper's continuous windows involve non-trivial cutoffs on the sphere,
we implement a *faithful discretisation* that satisfies the partition-of-unity
identity by construction. Specifically, we build windows chi_j on N frequency
bins (indexed j = 0..N-1) by:

    1. Assigning each bin k to a (scale, direction) sector (a hard tile of
       frequency space, as in Fig. 1 of Liu 2008; this is the "case (1)"
       instance the paper's Sec 6.2 explicitly calls out — indicator functions
       on disjoint sets — for which the quantum implementation is efficient).
    2. Setting chi_{a,theta}(k) = 1 if k lies in sector S_{a,theta}, else 0.

This is Liu Section 6.2, Case (1): "the window functions are indicator
functions supported on disjoint sets" — exactly the case where efficient
quantum implementation is straightforward.

We then verify:
  (P1) partition of unity: sum_{a,theta} chi^2 == 1 on every frequency bin
  (P2) unitarity of the joint curvelet map (norm preservation)
  (P3) inversion identity: applying Gamma then Gamma^dagger returns the input
"""
from __future__ import annotations

import numpy as np


# ---------------------------------------------------------------------------
# 1-D discrete curvelet: dyadic tiling of frequency ring
# ---------------------------------------------------------------------------

def dyadic_windows_1d(N: int) -> np.ndarray:
    """Return chi[j, k] with shape (num_windows, N) satisfying sum_j chi[j]^2 = 1.

    We split the N frequency bins (indexed by DC-centered frequency k) into:
      * DC bin (k=0):              window 0
      * positive dyadic annuli:    [1,1], [2,3], [4,7], [8,15], ... up to N/2-1
      * Nyquist bin (k=N/2):       last positive window
      * negative dyadic annuli:    mirror of positives
    Each bin gets assigned to exactly ONE window -> hard partition,
    chi in {0,1}, so sum chi^2 = 1 trivially.
    """
    # Centered frequencies: -N/2..N/2-1, but numpy FFT uses 0..N-1 order.
    freqs = np.fft.fftfreq(N, d=1.0) * N   # integer freqs -N/2..N/2-1
    freqs = freqs.astype(int)
    sectors: list[np.ndarray] = []
    # DC
    sectors.append((freqs == 0).astype(float))
    # Positive dyadic annuli
    k = 1
    while k < N // 2:
        lo, hi = k, min(2 * k, N // 2)
        mask = (freqs >= lo) & (freqs < hi)
        sectors.append(mask.astype(float))
        k = hi
    # Nyquist
    sectors.append((freqs == -N // 2).astype(float))
    # Negative dyadic annuli
    k = 1
    while k < N // 2:
        lo, hi = k, min(2 * k, N // 2)
        mask = (freqs <= -lo) & (freqs > -hi)
        sectors.append(mask.astype(float))
        k = hi
    chi = np.stack(sectors, axis=0)  # (S, N)
    return chi


def curvelet_1d(f: np.ndarray, chi: np.ndarray) -> np.ndarray:
    """Return Gamma f[j, b], with j ranging over windows, b over positions.

    Gamma f(j, b) = (1/sqrt(N)) * sum_k fhat(k) * chi[j,k] * exp(2 pi i k b / N)

    We use unitary FFT conventions throughout: fhat = FFT(f)/sqrt(N),
    inverse = sqrt(N)*IFFT(...).
    """
    N = f.shape[0]
    fhat = np.fft.fft(f) / np.sqrt(N)          # (N,)
    windowed = chi * fhat[None, :]              # (S, N)
    # inverse FFT along the frequency axis => location b
    gamma = np.fft.ifft(windowed, axis=1) * np.sqrt(N)   # (S, N)
    return gamma


def inv_curvelet_1d(gamma: np.ndarray, chi: np.ndarray) -> np.ndarray:
    """Adjoint of curvelet_1d; also the inverse when chi is a partition of unity."""
    N = gamma.shape[1]
    # forward FFT along location axis => frequency
    g_freq = np.fft.fft(gamma, axis=1) / np.sqrt(N)     # (S, N)
    # multiply by chi (conjugate; chi is real here so it's the same)
    accum = np.sum(chi * g_freq, axis=0)                # (N,)
    # inverse FFT to spatial domain
    f = np.fft.ifft(accum) * np.sqrt(N)
    return f


# ---------------------------------------------------------------------------
# 2-D discrete curvelet: dyadic angular tiling (Liu Fig. 1)
# ---------------------------------------------------------------------------

def dyadic_wedge_windows_2d(N: int, num_scales: int = 3, num_angles_at_finest: int = 8) -> np.ndarray:
    """Build a 2-D partition-of-unity of frequency bins in wedge-shaped sectors.

    Frequency plane is split into:
      * A central disk (low freq)
      * ``num_scales`` dyadic radial annuli
      * Each annulus at scale s is further sliced into ``num_angles_at_finest / 2^{num_scales-1-s}``
        angular wedges  -- matches Liu's rule "angular width sqrt(a)" (halving of angular count
        as scale coarsens).
      * A high-freq corner catches everything outside the last annulus.
    Every frequency bin is assigned to exactly ONE wedge.
    Returns chi[j, kx, ky] with sum_j chi = 1 (hard partition).
    """
    kx = np.fft.fftfreq(N, d=1.0) * N
    ky = np.fft.fftfreq(N, d=1.0) * N
    KX, KY = np.meshgrid(kx, ky, indexing="ij")
    R = np.sqrt(KX**2 + KY**2)
    THETA = np.arctan2(KY, KX)          # -pi..pi
    THETA_pos = np.mod(THETA, 2 * np.pi)

    # Radial bin edges: 0, 1, 2, 4, 8, ..., R_max -- always ensure we have
    # (num_scales + 2) edges so indices [0..num_scales+1] are all valid.
    r_edges = [0.0, 1.0]
    while len(r_edges) < num_scales + 2 or r_edges[-1] < N / 2:
        r_edges.append(r_edges[-1] * 2 if r_edges[-1] >= 1 else 2.0)
    # Truncate to exactly num_scales+2 edges and stretch the last one to catch
    # the whole grid corner.
    r_edges = r_edges[: num_scales + 2]
    r_edges[-1] = float(N)

    # Assign each bin to a wedge index
    assign = np.full(R.shape, -1, dtype=int)
    windows: list[np.ndarray] = []
    # DC / low disk
    inner = R < r_edges[1]
    windows.append(inner.astype(float))
    assign[inner] = 0
    wid = 1
    for s in range(num_scales):
        r_lo, r_hi = r_edges[s + 1], r_edges[s + 2]
        # number of angular wedges at this scale: halve as scale index grows
        n_ang = max(4, num_angles_at_finest // (2 ** s))
        for a in range(n_ang):
            t_lo = 2 * np.pi * a / n_ang
            t_hi = 2 * np.pi * (a + 1) / n_ang
            mask = (R >= r_lo) & (R < r_hi) & (THETA_pos >= t_lo) & (THETA_pos < t_hi)
            if not np.any(mask):
                continue
            windows.append(mask.astype(float))
            assign[mask] = wid
            wid += 1
    # High freq catch-all (anything not yet assigned)
    hi = assign < 0
    if np.any(hi):
        windows.append(hi.astype(float))
        assign[hi] = wid
    chi = np.stack(windows, axis=0)  # (S, N, N)
    return chi


def curvelet_2d(f: np.ndarray, chi: np.ndarray) -> np.ndarray:
    """2-D discrete curvelet transform, unitary FFT."""
    N = f.shape[0]
    fhat = np.fft.fft2(f) / N
    windowed = chi * fhat[None, :, :]                 # (S, N, N)
    gamma = np.fft.ifft2(windowed, axes=(1, 2)) * N   # (S, N, N)
    return gamma


def inv_curvelet_2d(gamma: np.ndarray, chi: np.ndarray) -> np.ndarray:
    N = gamma.shape[1]
    g_freq = np.fft.fft2(gamma, axes=(1, 2)) / N
    accum = np.sum(chi * g_freq, axis=0)
    return np.fft.ifft2(accum) * N


# ---------------------------------------------------------------------------
# Self-tests / demo
# ---------------------------------------------------------------------------

def check_partition_of_unity(chi: np.ndarray) -> float:
    """Return max |sum_j chi^2 - 1| over all frequency bins."""
    s = np.sum(chi.astype(float) ** 2, axis=0)
    return float(np.max(np.abs(s - 1.0)))


def check_isometry(chi: np.ndarray, fwd, inv, seed: int = 0, n_trials: int = 5) -> tuple[float, float]:
    """Check ||Gamma f||^2 == ||f||^2 (isometry) and inv(fwd(f)) == f."""
    rng = np.random.default_rng(seed)
    max_norm_err = 0.0
    max_inv_err = 0.0
    for _ in range(n_trials):
        shape = chi.shape[1:]
        f = rng.standard_normal(shape) + 1j * rng.standard_normal(shape)
        g = fwd(f, chi)
        n1 = float(np.sum(np.abs(f) ** 2))
        n2 = float(np.sum(np.abs(g) ** 2))
        max_norm_err = max(max_norm_err, abs(n1 - n2))
        f_rec = inv(g, chi)
        max_inv_err = max(max_inv_err, float(np.max(np.abs(f - f_rec))))
    return max_norm_err, max_inv_err


if __name__ == "__main__":
    import json
    results = {}

    # -------- 1D --------
    for N in (16, 32, 64, 128):
        chi = dyadic_windows_1d(N)
        pu = check_partition_of_unity(chi)
        norm_err, inv_err = check_isometry(chi, curvelet_1d, inv_curvelet_1d)
        results[f"1d_N{N}"] = {
            "N": N,
            "num_windows": int(chi.shape[0]),
            "partition_of_unity_error": pu,
            "norm_preservation_error": norm_err,
            "inversion_max_abs_error": inv_err,
        }

    # -------- 2D --------
    for N in (8, 16, 32):
        chi = dyadic_wedge_windows_2d(N, num_scales=3, num_angles_at_finest=8)
        pu = check_partition_of_unity(chi)
        norm_err, inv_err = check_isometry(chi, curvelet_2d, inv_curvelet_2d)
        results[f"2d_N{N}"] = {
            "N": N,
            "num_windows": int(chi.shape[0]),
            "partition_of_unity_error": pu,
            "norm_preservation_error": norm_err,
            "inversion_max_abs_error": inv_err,
        }

    print(json.dumps(results, indent=2))
