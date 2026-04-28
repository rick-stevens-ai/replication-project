"""Needlet Internal Linear Combination (NILC).

Standard ILC solves minimum-variance linear combination of frequency maps with
unit response to CMB:
    w = R^-1 a / (a^T R^-1 a),  R = frequency-frequency covariance.
For CMB separation in thermodynamic units, a = (1, 1, ..., 1).

NILC: do this per needlet scale, with R estimated locally (smoothed spatial
covariance). We implement per-scale spatially-smoothed covariance: at each
needlet scale k, filter each frequency map with h_k(ell), then estimate
R(p) = <T_i T_j> smoothed over neighbouring pixels, invert, combine, then
project back with h_k and sum over k.

We pre-deconvolve to a common beam before NILC so the response vector is unity.
"""
import numpy as np
import healpy as hp


def needlet_filter_map(m, hk, lmax):
    alm = hp.map2alm(m, lmax=lmax)
    alm = hp.almxfl(alm, hk)
    return hp.alm2map(alm, nside=hp.npix2nside(len(m)), verbose=False)


def smooth_map(m, fwhm_deg):
    return hp.smoothing(m, fwhm=np.deg2rad(fwhm_deg), verbose=False)


def ilc_weights_global(cov):
    """Given (nfreq, nfreq) covariance, return length-nfreq ILC weights with unit response."""
    nfreq = cov.shape[0]
    a = np.ones(nfreq)
    # Regularize
    cov = cov + 1e-20 * np.eye(nfreq) * np.trace(cov) / nfreq
    Rinv = np.linalg.inv(cov)
    num = Rinv @ a
    den = a @ num
    return num / den


def nilc_separate(maps_common_beam, needlet_bank, lmax, smooth_fwhm_deg=None):
    """Run NILC on beam-matched frequency maps.

    Parameters
    ----------
    maps_common_beam : (nfreq, npix) array in uK_CMB, already deconvolved to a common beam.
    needlet_bank : (nscales, lmax+1) array, cosine-squared partition of unity.
    lmax : int
    smooth_fwhm_deg : list of nscales fwhm (deg) for local covariance estimation.
                      If None, use reasonable default scaling with needlet scale.

    Returns
    -------
    cmb_nilc : (npix,) cleaned CMB map
    weights_by_scale : list of (nfreq, npix) weight maps
    filtered_by_scale : list of list of (npix,) per-freq needlet-filtered maps
    """
    nfreq, npix = maps_common_beam.shape
    nscales = needlet_bank.shape[0]
    nside = hp.npix2nside(npix)

    if smooth_fwhm_deg is None:
        # Larger smoothing at large scales (low ell), small at small scales
        # Rough rule: fwhm ~ 3 * pi / ell_peak, clipped
        peaks = []
        for k in range(nscales):
            ells = np.arange(lmax + 1)
            # peak = ell at max filter value
            peaks.append(ells[np.argmax(needlet_bank[k])])
        peaks = np.array(peaks, dtype=float)
        peaks[peaks < 2] = 2.0
        # Larger smoothing domains -> more independent modes per domain ->
        # smaller ILC bias. Use ~5*pi/ell_peak.
        smooth_fwhm_deg = np.rad2deg(5.0 * np.pi / peaks)
        # Cap
        smooth_fwhm_deg = np.clip(smooth_fwhm_deg, 3.0, 60.0)

    # Step 1: needlet-filter each frequency map
    filt = np.zeros((nscales, nfreq, npix))
    for k in range(nscales):
        hk = needlet_bank[k]
        for i in range(nfreq):
            filt[k, i] = needlet_filter_map(maps_common_beam[i], hk, lmax)

    # Step 2: local covariance per scale, invert, compute weights, apply
    cmb_nilc = np.zeros(npix)
    weights_by_scale = []
    for k in range(nscales):
        fwhm_deg = smooth_fwhm_deg[k]
        # Local covariance: smooth T_i * T_j
        cov_maps = np.zeros((nfreq, nfreq, npix))
        for i in range(nfreq):
            for j in range(i, nfreq):
                prod = filt[k, i] * filt[k, j]
                smoothed = smooth_map(prod, fwhm_deg)
                cov_maps[i, j] = smoothed
                cov_maps[j, i] = smoothed
        # Per-pixel weights
        a = np.ones(nfreq)
        w_map = np.zeros((nfreq, npix))
        cleaned_k = np.zeros(npix)
        # Vectorize inversion over pixels
        # cov_maps shape (nfreq, nfreq, npix) -> transpose to (npix, nfreq, nfreq)
        cov_pix = np.moveaxis(cov_maps, -1, 0)  # (npix, nfreq, nfreq)
        reg = 1e-20 * np.trace(cov_pix, axis1=1, axis2=2).mean() * np.eye(nfreq)
        cov_pix = cov_pix + reg
        try:
            Rinv = np.linalg.inv(cov_pix)  # (npix, nfreq, nfreq)
        except np.linalg.LinAlgError:
            Rinv = np.linalg.pinv(cov_pix)
        Rinv_a = Rinv @ a  # (npix, nfreq)
        den = (a[None, :] * Rinv_a).sum(axis=1)  # (npix,)
        den[np.abs(den) < 1e-30] = 1e-30
        w_pix = Rinv_a / den[:, None]  # (npix, nfreq)
        # Weighted combination of filtered maps
        filt_k = filt[k]  # (nfreq, npix)
        cleaned_k = (w_pix.T * filt_k).sum(axis=0)
        # Needlet synthesis: multiply by hk in harmonic space and add
        alm = hp.map2alm(cleaned_k, lmax=lmax)
        alm = hp.almxfl(alm, needlet_bank[k])
        cmb_nilc += hp.alm2map(alm, nside=nside, verbose=False)
        weights_by_scale.append(w_pix.T)  # store as (nfreq, npix)

    return cmb_nilc, weights_by_scale, filt
