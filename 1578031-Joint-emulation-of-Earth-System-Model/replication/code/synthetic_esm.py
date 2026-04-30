"""
Synthetic ESM Data Generator
=============================
Generates realistic synthetic Earth System Model output for testing fldgen.

Creates temperature and precipitation fields with:
- A forced trend (pattern scaling with global mean T)
- Spatially correlated internal variability
- Cross-variable (T-P) correlation
- Realistic climatological patterns

This serves as training data when the real ESM NetCDF files (42 MB each)
are impractical to download.
"""

import numpy as np
from scipy.ndimage import gaussian_filter


def generate_synthetic_esm(nlat: int = 24, nlon: int = 48, 
                           nyears: int = 95,
                           scenario: str = 'rcp85',
                           seed: int = 42) -> dict:
    """
    Generate synthetic ESM-like output.
    
    Parameters
    ----------
    nlat : int — number of latitude points
    nlon : int — number of longitude points  
    nyears : int — number of years (default 95 = 2006-2100)
    scenario : str — warming scenario identifier
    seed : int — random seed
    
    Returns
    -------
    dict with keys:
        'tas' : array [nyears x nlat*nlon] — surface air temperature (K)
        'pr'  : array [nyears x nlat*nlon] — precipitation (kg/m²/s)
        'tgav': array [nyears] — global mean temperature (K)
        'lat' : array [nlat] — latitudes
        'lon' : array [nlon] — longitudes
        'years': array [nyears] — year values
    """
    rng = np.random.default_rng(seed)
    
    # Create coordinate grid
    lat = np.linspace(-87.5, 87.5, nlat)
    lon = np.linspace(0, 360 - 360/nlon, nlon)
    lon_grid, lat_grid = np.meshgrid(lon, lat)
    lat_rad = np.deg2rad(lat_grid)
    lon_rad = np.deg2rad(lon_grid)
    
    ngrid = nlat * nlon
    years = np.arange(2006, 2006 + nyears)
    
    # ---- Global mean temperature trajectory ----
    # RCP8.5-like: ~4.5°C warming by 2100
    # Quadratic + some interannual variability
    t_frac = (years - 2006) / (2100 - 2006)
    if scenario == 'rcp85':
        tgav_trend = 287.0 + 4.5 * (0.3 * t_frac + 0.7 * t_frac**2)
    elif scenario == 'rcp45':
        tgav_trend = 287.0 + 2.0 * (0.4 * t_frac + 0.6 * t_frac**2)
    else:
        tgav_trend = 287.0 + 3.0 * t_frac
    
    # Add interannual variability (~0.15 K std)
    tgav_noise = rng.normal(0, 0.15, nyears)
    # Smooth slightly for realistic autocorrelation
    tgav_noise = np.convolve(tgav_noise, [0.25, 0.5, 0.25], mode='same')
    tgav = tgav_trend + tgav_noise
    
    # ---- Temperature pattern scaling field ----
    # Polar amplification: stronger warming at high latitudes
    polar_amp = 1.0 + 1.5 * (np.abs(lat_rad) / (np.pi/2))**2
    
    # Land/ocean contrast (crude): more warming over "continents"
    land_mask = (np.sin(2*lon_rad) * np.cos(lat_rad) > 0.2).astype(float)
    land_enhance = 1.0 + 0.5 * land_mask
    
    # Pattern scaling coefficients (w): warming per unit global warming
    w_pattern = polar_amp * land_enhance
    w_flat = w_pattern.flatten()
    
    # Baseline T field: realistic climatology
    # Warm tropics, cold poles
    t_clim = 288 + 30 * np.cos(lat_rad) - 20 * (np.abs(lat_rad) / (np.pi/2))**2
    b_flat = t_clim.flatten()
    
    # ---- Temperature variability (internal) ----
    # Generate spatially correlated noise using Gaussian filter
    tas = np.zeros((nyears, ngrid))
    for t in range(nyears):
        # Uncorrelated noise
        noise = rng.normal(0, 1, (nlat, nlon))
        # Apply spatial correlation via Gaussian smoothing
        noise_smooth = gaussian_filter(noise, sigma=2.0)
        # Scale to ~1-3 K variability (larger at high latitudes)
        var_scale = 1.0 + 1.5 * (np.abs(lat_rad) / (np.pi/2))
        noise_scaled = noise_smooth * var_scale
        
        # Combine mean field + variability
        dt = tgav[t] - 287.0  # warming relative to baseline
        tas[t, :] = b_flat + w_flat * dt + noise_scaled.flatten()
    
    # Add some temporal autocorrelation to variability
    # Simple AR(1) smoothing
    alpha = 0.3
    for t in range(1, nyears):
        resid = tas[t, :] - (b_flat + w_flat * (tgav[t] - 287.0))
        resid_prev = tas[t-1, :] - (b_flat + w_flat * (tgav[t-1] - 287.0))
        tas[t, :] = b_flat + w_flat * (tgav[t] - 287.0) + alpha * resid_prev + np.sqrt(1-alpha**2) * resid
    
    # ---- Precipitation ----
    # Climatological precipitation pattern
    # ITCZ (tropical max), midlat storm tracks, dry subtropics/poles
    pr_clim = (3.0 * np.exp(-((lat_rad)**2) / (0.15)) +  # ITCZ
               1.5 * np.exp(-((np.abs(lat_rad) - 0.8)**2) / (0.2)) +  # storm tracks
               0.3) * 1e-5   # kg/m²/s (typical precip rate)
    
    # Reduce over "land"
    pr_clim = pr_clim * (1 - 0.3 * land_mask)
    
    # Precipitation response to warming: ~2%/K increase in tropics, drying in subtropics
    pr_response = (0.02 * np.exp(-((lat_rad)**2) / (0.2)) - 
                   0.01 * np.exp(-((np.abs(lat_rad) - 0.5)**2) / (0.1)))
    
    pr = np.zeros((nyears, ngrid))
    for t in range(nyears):
        dt = tgav[t] - 287.0
        noise = rng.normal(0, 1, (nlat, nlon))
        noise_smooth = gaussian_filter(noise, sigma=2.5)
        
        # Precipitation variability is proportional to mean (multiplicative)
        pr_mean = pr_clim * (1 + pr_response * dt)
        pr_var = 0.15 * pr_mean  # ~15% CV
        pr_field = pr_mean + pr_var * noise_smooth
        
        # Ensure non-negative
        pr_field = np.maximum(pr_field, 1e-9)
        pr[t, :] = pr_field.flatten()
    
    # Add some T-P correlation: warmer years slightly wetter in tropics
    # This creates cross-variable correlation
    for t in range(nyears):
        t_anom = tas[t, :] - np.mean(tas, axis=0)
        # Moderate positive T-P correlation in tropics
        tropical = np.abs(lat_grid.flatten()) < 30
        pr[t, tropical] += 0.3e-5 * t_anom[tropical] / np.std(t_anom[tropical]) * pr[t, tropical]
        pr[t, :] = np.maximum(pr[t, :], 1e-9)
    
    # Add temporal autocorrelation for precip
    alpha_p = 0.2
    for t in range(1, nyears):
        resid_t = pr[t, :] - np.mean(pr, axis=0)
        resid_prev = pr[t-1, :] - np.mean(pr, axis=0)
        pr[t, :] = np.mean(pr, axis=0) + alpha_p * resid_prev + np.sqrt(1-alpha_p**2) * resid_t
        pr[t, :] = np.maximum(pr[t, :], 1e-9)
    
    return {
        'tas': tas,
        'pr': pr,
        'tgav': tgav,
        'lat': lat,
        'lon': lon,
        'years': years,
        'nlat': nlat,
        'nlon': nlon,
        'ngrid': ngrid,
    }


if __name__ == '__main__':
    data = generate_synthetic_esm()
    print(f"Generated synthetic ESM data:")
    print(f"  Grid: {data['nlat']} lat x {data['nlon']} lon = {data['ngrid']} cells")
    print(f"  Time: {data['years'][0]} - {data['years'][-1]} ({len(data['years'])} years)")
    print(f"  T range: {data['tas'].min():.1f} - {data['tas'].max():.1f} K")
    print(f"  P range: {data['pr'].min():.2e} - {data['pr'].max():.2e} kg/m²/s")
    print(f"  Tgav trend: {data['tgav'][0]:.1f} - {data['tgav'][-1]:.1f} K")
