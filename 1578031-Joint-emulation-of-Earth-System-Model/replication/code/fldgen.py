"""
fldgen v2.0 — Python Replication
==================================
Reimplementation of the fldgen v2.0 algorithm for joint emulation of 
Earth System Model temperature-precipitation realizations.

Reference:
  Link et al. (2019). "Joint emulation of Earth System Model temperature-
  precipitation realizations with fldgen v2.0." Geoscientific Model Development.
  OSTI ID: 1578031. GitHub: https://github.com/JGCRI/fldgen

Algorithm:
  1. Pattern scaling: regress gridded T and log(P) against global-mean T
  2. Compute residuals
  3. Empirical CDF: characterize per-grid-cell residual distributions
  4. Normalize residuals to N(0,1) via probability integral transform
  5. Joint EOF (PCA) of concatenated [T_resid | P_resid] state vector
  6. Fourier phase randomization of EOF projection coefficients
  7. Inverse quantile transform back to native distributions
  8. Add mean field to recover full T and P fields

Author: Ollie (OpenClaw replication agent)
Date: 2026-04-30
"""

import numpy as np
from scipy import stats
from scipy.interpolate import interp1d
from dataclasses import dataclass, field
from typing import Optional, List, Tuple


@dataclass
class MeanField:
    """Pattern scaling result: T_i(t) = w_i * T_gav(t) + b_i + r_i(t)"""
    w: np.ndarray          # slope per grid cell [ngrid]
    b: np.ndarray          # intercept per grid cell [ngrid]
    r: np.ndarray          # residuals [ntime x ngrid]


@dataclass
class EmpiricalDistribution:
    """Per-grid-cell empirical CDF and quantile functions."""
    cdfs: list             # list of interpolating CDF functions
    quantiles: list        # list of interpolating quantile functions


@dataclass
class EOFResult:
    """EOF decomposition result."""
    rotation: np.ndarray   # basis vectors [2*ngrid x neof]
    x: np.ndarray          # projection coefficients [ntime x neof]
    sdev: np.ndarray       # standard deviations of each component


@dataclass
class FldgenEmulator:
    """Trained fldgen v2.0 emulator."""
    # Grid metadata
    lat: np.ndarray
    lon: np.ndarray
    ngrid: int
    
    # Input data (transformed)
    tdata: np.ndarray      # temperature data [ntime x ngrid]
    pdata: np.ndarray      # log(precipitation) data [ntime x ngrid]
    
    # Global mean temperature
    tgav: np.ndarray       # [ntime]
    
    # Pattern scaling results
    meanfld_t: MeanField
    meanfld_p: MeanField
    
    # Empirical distribution characterization
    tfuns: EmpiricalDistribution
    pfuns: EmpiricalDistribution
    
    # EOF decomposition
    reof: EOFResult
    
    # Fourier transform info
    fx_mag: np.ndarray     # magnitude [ntime x neof]
    fx_phases: list        # list of phase matrices [ntime x neof]


# ============================================================================
# Pattern Scaling
# ============================================================================

def pscl_analyze(field_data: np.ndarray, tgav: np.ndarray) -> MeanField:
    """
    Linear pattern scaling: regress each grid cell against global mean T.
    
    T_i(t) = w_i * T_gav(t) + b_i + residual_i(t)
    
    Parameters
    ----------
    field_data : array [ntime x ngrid]
    tgav : array [ntime]
    
    Returns
    -------
    MeanField with w, b, r
    """
    ntime, ngrid = field_data.shape
    tg = tgav.reshape(-1, 1)  # [ntime x 1]
    
    # Design matrix [ntime x 2]: [tgav, ones]
    X = np.column_stack([tg, np.ones(ntime)])
    
    # Solve least squares for all grid cells simultaneously
    # field_data = X @ [w; b] + residuals
    coeffs, _, _, _ = np.linalg.lstsq(X, field_data, rcond=None)
    
    w = coeffs[0, :]   # slopes [ngrid]
    b = coeffs[1, :]   # intercepts [ngrid]
    
    # Compute residuals
    predicted = tg @ w.reshape(1, -1) + b.reshape(1, -1)
    r = field_data - predicted
    
    return MeanField(w=w, b=b, r=r)


def pscl_apply(meanfld: MeanField, tgav: np.ndarray) -> np.ndarray:
    """
    Apply pattern scaling to generate mean field.
    
    Parameters
    ----------
    meanfld : MeanField
    tgav : array [ntime]
    
    Returns
    -------
    array [ntime x ngrid]
    """
    tg = tgav.reshape(-1, 1)
    return tg @ meanfld.w.reshape(1, -1) + meanfld.b.reshape(1, -1)


# ============================================================================
# Empirical Distribution Characterization
# ============================================================================

def characterize_emp_dist(residuals: np.ndarray) -> EmpiricalDistribution:
    """
    Build empirical CDF and quantile functions for each grid cell.
    
    Following fldgen's approach:
    - Sort residuals for each grid cell
    - Assign probabilities using (rank-1)/(N+1) formula
    - Add extrapolated tail points at p=0 and p=1
    - Build interpolating functions
    
    Parameters
    ----------
    residuals : array [ntime x ngrid]
    
    Returns
    -------
    EmpiricalDistribution
    """
    ntime, ngrid = residuals.shape
    offset = 1.0 / (ntime + 1)
    
    cdfs = []
    quantiles = []
    
    for j in range(ngrid):
        col = residuals[:, j].copy()
        
        # Add extrapolated tail points (following fldgen's newmin/newmax logic)
        sorted_vals = np.sort(col)
        
        # Max extrapolation (for p=1 point)
        x_max1 = sorted_vals[-1]
        x_max2 = sorted_vals[-2] if len(sorted_vals) > 1 else x_max1
        p_max1 = (ntime) * offset       # ~ 1 - offset
        p_max2 = (ntime - 1) * offset   # ~ 1 - 2*offset
        if x_max1 != x_max2:
            slope1 = (p_max1 - p_max2) / (x_max1 - x_max2)
            k = 100.0
            slope0 = k * slope1
            x_max0 = (1.0 / slope0) * (1.0 - p_max1) + x_max1
        else:
            x_max0 = x_max1 * 1.01 + 0.01
        
        # Min extrapolation (for p=0 point)
        x_min1 = sorted_vals[0]
        x_min2 = sorted_vals[1] if len(sorted_vals) > 1 else x_min1
        p_min1 = 1 * offset
        p_min2 = 2 * offset
        if x_min1 != x_min2:
            slope1 = (p_min1 - p_min2) / (x_min1 - x_min2)
            k = 100.0
            slope0 = k * slope1
            x_min0 = (1.0 / slope0) * (0.0 - p_min1) + x_min1
        else:
            x_min0 = x_min1 * 0.99 - 0.01
        
        # Also add a slightly-above-max point (fldgen adds 1.0001 * max)
        x_padmax = (1.0 + 0.0001) * x_max1 if x_max1 > 0 else x_max1 - 0.0001 * abs(x_max1)
        
        # Build augmented residual vector
        augmented = np.concatenate([col, [x_padmax, x_min0]])
        
        # Rank and compute probabilities
        ranks = stats.rankdata(augmented, method='ordinal')
        probs = (ranks - 1) * offset
        
        # Sort by value for interpolation
        sort_idx = np.argsort(augmented)
        x_sorted = augmented[sort_idx]
        p_sorted = probs[sort_idx]
        
        # Ensure monotonicity (add tiny perturbation to duplicates)
        for i in range(1, len(x_sorted)):
            if x_sorted[i] <= x_sorted[i-1]:
                x_sorted[i] = x_sorted[i-1] + 1e-12
        
        # Build interpolating CDF: x -> p
        cdf_func = interp1d(x_sorted, p_sorted, 
                           kind='linear', bounds_error=False,
                           fill_value=(0.0, 1.0))
        
        # Build interpolating quantile function: p -> x
        # Ensure p_sorted is strictly increasing
        unique_mask = np.concatenate([[True], np.diff(p_sorted) > 0])
        quant_func = interp1d(p_sorted[unique_mask], x_sorted[unique_mask],
                             kind='linear', bounds_error=False,
                             fill_value=(x_sorted[0], x_sorted[-1]))
        
        cdfs.append(cdf_func)
        quantiles.append(quant_func)
    
    return EmpiricalDistribution(cdfs=cdfs, quantiles=quantiles)


def normalize_resids(residuals: np.ndarray, 
                     emp_dist: EmpiricalDistribution) -> np.ndarray:
    """
    Normalize residuals to N(0,1) via probability integral transform.
    
    z = Phi^{-1}(F_emp(r))
    
    Parameters
    ----------
    residuals : array [ntime x ngrid]
    emp_dist : EmpiricalDistribution
    
    Returns
    -------
    array [ntime x ngrid] of normalized residuals
    """
    ntime, ngrid = residuals.shape
    normalized = np.zeros_like(residuals)
    
    for j in range(ngrid):
        # Apply empirical CDF to get quantiles
        p = emp_dist.cdfs[j](residuals[:, j])
        
        # Clip to avoid infinities from qnorm at 0 or 1
        p = np.clip(p, 1e-10, 1.0 - 1e-10)
        
        # Apply inverse normal CDF
        normalized[:, j] = stats.norm.ppf(p)
    
    return normalized


def unnormalize_resids(norm_resids: np.ndarray,
                       emp_dist: EmpiricalDistribution) -> np.ndarray:
    """
    Reverse the normalization: map N(0,1) values back to native distribution.
    
    r = F_emp^{-1}(Phi(z))
    
    Parameters
    ----------
    norm_resids : array [ntime x ngrid]
    emp_dist : EmpiricalDistribution
    
    Returns
    -------
    array [ntime x ngrid] in native distribution
    """
    ntime, ngrid = norm_resids.shape
    native = np.zeros_like(norm_resids)
    
    for j in range(ngrid):
        # Convert normal values to probabilities
        p = stats.norm.cdf(norm_resids[:, j])
        
        # Apply empirical quantile function
        native[:, j] = emp_dist.quantiles[j](p)
    
    return native


# ============================================================================
# EOF Analysis
# ============================================================================

def eof_analyze(joint_resids: np.ndarray, ngrid: int,
                globop: np.ndarray) -> EOFResult:
    """
    EOF (PCA) analysis of the joint normalized residuals.
    
    Following fldgen:
    1. Construct zeroth basis vector from global mean operator
    2. Project residuals onto it and subtract
    3. PCA on the remainder
    4. Graft zeroth component back
    
    Parameters
    ----------
    joint_resids : array [ntime x 2*ngrid] 
        Concatenated [T_norm_resid | P_norm_resid]
    ngrid : int
        Number of grid cells per variable
    globop : array [ngrid]
        Global mean operator (area weights, normalized)
    
    Returns
    -------
    EOFResult
    """
    nvars = joint_resids.shape[1] // ngrid
    
    # Build zeroth basis vector: repeat globop for each variable
    xh0 = np.tile(globop, nvars)
    xh0 = xh0 / np.sqrt(np.sum(xh0**2))
    
    # Project onto zeroth basis
    proj0 = joint_resids @ xh0  # [ntime]
    
    # Subtract projection
    resids_sub = joint_resids - np.outer(proj0, xh0)
    
    # PCA on the remainder (no centering/scaling — data is already N(0,1))
    U, S, Vt = np.linalg.svd(resids_sub, full_matrices=False)
    
    # Discard near-zero components
    sdmin = 1e-8 * S[0]
    keep = S > sdmin
    
    rotation_pca = Vt[keep, :].T    # [2*ngrid x nkeep]
    x_pca = U[:, keep] * S[keep]    # [ntime x nkeep] = scores
    sdev_pca = S[keep] / np.sqrt(joint_resids.shape[0] - 1)
    
    # Graft zeroth component
    rotation = np.column_stack([xh0, rotation_pca])
    x = np.column_stack([proj0, x_pca])
    sdev = np.concatenate([[np.std(proj0, ddof=1)], sdev_pca])
    
    return EOFResult(rotation=rotation, x=x, sdev=sdev)


# ============================================================================
# Power Spectral Density Estimation
# ============================================================================

def psdest(eof_x: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Estimate PSD from EOF projection coefficients.
    
    Parameters
    ----------
    eof_x : array [ntime x neof]
    
    Returns
    -------
    (psd, phases) where:
        psd : array [ntime x neof] — power spectral density
        phases : array [ntime x neof] — phases from DFT
    """
    fx = np.fft.fft(eof_x, axis=0)
    psd = np.abs(fx)**2
    phases = np.angle(fx)
    return psd, phases


# ============================================================================
# Field Generation (Fourier Phase Randomization)
# ============================================================================

def nphase(N: int) -> int:
    """Number of independent phases for FFT of length N."""
    if N % 2 == 0:
        return N // 2 + 1
    else:
        return (N - 1) // 2 + 1


def find_minusf_coord(i: np.ndarray, N: int) -> np.ndarray:
    """
    For 0-indexed FFT coordinates, find the index of -f.
    Note: using 0-indexed unlike the R version (1-indexed).
    """
    return np.where(i == 0, 0, N - i)


def phsym(phase: float) -> float:
    """Force phase to nearest self-symmetric value (0 or pi)."""
    if abs(phase - np.pi) < np.pi / 2:
        return np.pi
    return 0.0


def mkcorrts(fx_mag: np.ndarray, fx_phases: list,
             method: int = 1) -> np.ndarray:
    """
    Generate new time series with specified autocorrelation via
    Fourier phase randomization.
    
    Parameters
    ----------
    fx_mag : array [ntime x neof] — sqrt(PSD)
    fx_phases : list of phase matrices from training data
    method : 1 (fully random phases) or 2 (phase-shift from template)
    
    Returns
    -------
    array [ntime x neof] of new projection coefficients
    """
    Nt, M = fx_mag.shape
    Nf = nphase(Nt)
    
    # 0-indexed plus rows: 0, 1, ..., Nf-1
    plusrows = np.arange(Nf)
    minusrows = find_minusf_coord(plusrows, Nt)
    
    if method == 2:
        # Phase-shift method: pick a template and add random shift
        dtheta = np.random.uniform(0, 2*np.pi, size=Nf)
        dtheta[0] = phsym(dtheta[0])
        if Nt % 2 == 0:
            dtheta[Nf-1] = phsym(dtheta[Nf-1])
        
        template_idx = np.random.randint(len(fx_phases))
        phase = fx_phases[template_idx][plusrows, :].copy()
        phase = phase + dtheta[:, np.newaxis]
    else:
        # Method 1: fully random phases
        phase = np.random.uniform(0, 2*np.pi, size=(Nf, M))
        phase[0, :] = [phsym(p) for p in phase[0, :]]
        if Nt % 2 == 0:
            phase[Nf-1, :] = [phsym(p) for p in phase[Nf-1, :]]
    
    # Build complex Fourier coefficients
    Fxout = np.zeros((Nt, M), dtype=complex)
    
    # Plus frequencies: magnitude * e^{i*phase}
    Fxout[plusrows, :] = fx_mag[plusrows, :] * (np.cos(phase) + 1j * np.sin(phase))
    
    # Minus frequencies: conjugate of plus frequencies
    # (but skip f=0 which maps to itself)
    for k in range(len(plusrows)):
        if minusrows[k] != plusrows[k]:  # skip DC (and Nyquist for even N)
            Fxout[minusrows[k], :] = np.conj(Fxout[plusrows[k], :])
    
    # Inverse FFT
    xout = np.fft.ifft(Fxout, axis=0)
    return np.real(xout)


# ============================================================================
# Training and Generation
# ============================================================================

def train_tp(tdata: np.ndarray, pdata: np.ndarray,
             lat: np.ndarray, lon: np.ndarray,
             tgav: Optional[np.ndarray] = None,
             p_transform=np.log,
             p_floor: float = 1e-9) -> FldgenEmulator:
    """
    Train the fldgen v2.0 emulator on temperature and precipitation data.
    
    Parameters
    ----------
    tdata : array [ntime x ngrid] — temperature (tas)
    pdata : array [ntime x ngrid] — precipitation (pr, in native units)
    lat : array [nlat] — latitudes
    lon : array [nlon] — longitudes
    tgav : array [ntime], optional — global mean temperature
    p_transform : callable — transform for precipitation (default: log)
    p_floor : float — floor for precipitation before log transform
    
    Returns
    -------
    FldgenEmulator
    """
    ntime, ngrid = tdata.shape
    
    # 1. Transform precipitation
    pdata_raw = pdata.copy()
    pdata_t = p_transform(np.maximum(pdata, p_floor))
    
    # 2. Compute area weights for global mean
    # Approximate: cos(lat) weighting
    lat_rad = np.deg2rad(lat)
    cos_lat = np.cos(lat_rad)
    
    # Build global operator: area-weighted average
    nlat = len(lat)
    nlon = len(lon)
    
    # Each grid cell's weight = cos(lat) 
    # Expand to full grid
    weights = np.repeat(cos_lat, nlon)
    globop = weights / np.sum(weights)
    
    # 3. Compute or use provided global mean T
    if tgav is None:
        tgav = tdata @ globop
    
    # 4. Pattern scaling for T and log(P)
    meanfld_t = pscl_analyze(tdata, tgav)
    meanfld_p = pscl_analyze(pdata_t, tgav)
    
    # 5. Characterize empirical distributions of residuals
    tfuns = characterize_emp_dist(meanfld_t.r)
    pfuns = characterize_emp_dist(meanfld_p.r)
    
    # 6. Normalize residuals to N(0,1)
    norm_t = normalize_resids(meanfld_t.r, tfuns)
    norm_p = normalize_resids(meanfld_p.r, pfuns)
    
    # 7. Joint state vector
    joint = np.hstack([norm_t, norm_p])
    
    # 8. EOF decomposition
    reof = eof_analyze(joint, ngrid, globop)
    
    # 9. PSD estimation
    psd, phases = psdest(reof.x)
    fx_mag = np.sqrt(psd)
    
    return FldgenEmulator(
        lat=lat, lon=lon, ngrid=ngrid,
        tdata=tdata, pdata=pdata_t,
        tgav=tgav,
        meanfld_t=meanfld_t, meanfld_p=meanfld_p,
        tfuns=tfuns, pfuns=pfuns,
        reof=reof,
        fx_mag=fx_mag, fx_phases=[phases]
    )


def generate_resids(emulator: FldgenEmulator, ngen: int = 1,
                    method: int = 1) -> List[np.ndarray]:
    """
    Generate new residual fields using Fourier phase randomization.
    
    Parameters
    ----------
    emulator : FldgenEmulator
    ngen : int — number of realizations
    method : int — phase randomization method (1 or 2)
    
    Returns
    -------
    List of arrays [ntime x 2*ngrid], each a new realization.
    First ngrid columns = T residuals, next ngrid = log(P) residuals.
    """
    results = []
    ngrid = emulator.ngrid
    
    for _ in range(ngen):
        # Generate new EOF projection coefficients
        bcoord = mkcorrts(emulator.fx_mag, emulator.fx_phases, method=method)
        
        # Reconstruct normalized residual fields
        norm_fields = bcoord @ emulator.reof.rotation.T  # [ntime x 2*ngrid]
        
        # Un-normalize: T
        t_resids = unnormalize_resids(norm_fields[:, :ngrid], emulator.tfuns)
        
        # Un-normalize: P
        p_resids = unnormalize_resids(norm_fields[:, ngrid:], emulator.pfuns)
        
        results.append(np.hstack([t_resids, p_resids]))
    
    return results


def generate_fullgrids(emulator: FldgenEmulator, 
                       residgrids: List[np.ndarray],
                       tgav: np.ndarray,
                       p_inverse=np.exp) -> List[dict]:
    """
    Generate full T and P fields by adding mean field to residuals.
    
    Parameters
    ----------
    emulator : FldgenEmulator
    residgrids : list of [ntime x 2*ngrid] residual arrays
    tgav : array [ntime] — global mean temperature trajectory
    p_inverse : callable — inverse of P transform (default: exp)
    
    Returns
    -------
    List of dicts with 'tas' and 'pr' arrays [ntime x ngrid]
    """
    ngrid = emulator.ngrid
    
    # Reconstruct mean fields
    meanfield_t = pscl_apply(emulator.meanfld_t, tgav)
    meanfield_p = pscl_apply(emulator.meanfld_p, tgav)
    
    results = []
    for resid in residgrids:
        t_field = resid[:, :ngrid] + meanfield_t      # temperature
        p_field = resid[:, ngrid:] + meanfield_p       # log(precipitation)
        p_field = p_inverse(p_field)                    # precipitation
        
        results.append({'tas': t_field, 'pr': p_field})
    
    return results, meanfield_t, meanfield_p
