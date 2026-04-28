"""Cosine-squared needlet bank.

Construction: partition [0, lmax] with peaks at ell_peak_k. Each filter h_k(ell)
is a cosine half-cycle between neighboring peaks, such that sum_k h_k(ell)^2 = 1.
"""
import numpy as np


def cosine_needlet_bank(lmax, n_scales):
    """Return (n_scales, lmax+1) array of filter values h_k(ell).
    Peaks logarithmically spaced (but lowest at 0).
    Property: sum_k h_k(ell)^2 = 1 for ell in [0, lmax].
    """
    # Peaks: 0, then log-spaced between ~5 and lmax
    peaks = np.zeros(n_scales)
    peaks[0] = 0.0
    peaks[-1] = lmax
    if n_scales > 2:
        log_peaks = np.linspace(np.log(5.0), np.log(lmax), n_scales - 1)
        peaks[1:] = np.exp(log_peaks)
    peaks = np.sort(peaks)

    ells = np.arange(lmax + 1, dtype=float)
    bank = np.zeros((n_scales, lmax + 1))
    for k in range(n_scales):
        lp = peaks[k - 1] if k > 0 else None
        lc = peaks[k]
        ln = peaks[k + 1] if k < n_scales - 1 else None
        # Left side of peak (rising): cos^2 from pi/2 (at lp) to 0 (at lc)
        if lp is not None:
            mask = (ells >= lp) & (ells <= lc)
            x = (ells[mask] - lp) / (lc - lp + 1e-30)  # 0..1
            bank[k, mask] = np.cos(0.5 * np.pi * (1.0 - x))  # 0 at lp, 1 at lc
        else:
            # First filter: full amplitude at ell=0
            mask = ells <= lc
            bank[k, mask] = 1.0
        # Right side: cos^2 from 0 (at lc) to pi/2 (at ln), amplitude 1->0
        if ln is not None:
            mask = (ells > lc) & (ells <= ln)
            x = (ells[mask] - lc) / (ln - lc + 1e-30)  # 0..1
            bank[k, mask] = np.cos(0.5 * np.pi * x)  # 1 at lc, 0 at ln
        else:
            # Last filter: full amplitude beyond peak
            mask = ells >= lc
            bank[k, mask] = 1.0
    # Now normalize so sum h^2 = 1 exactly
    norm = np.sqrt(np.sum(bank**2, axis=0))
    norm[norm == 0] = 1.0
    bank = bank / norm[None, :]
    return bank, peaks
