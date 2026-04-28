"""Simple analytic foreground SEDs in thermodynamic CMB units (uK_CMB).

We model:
  - Galactic thermal dust as modified blackbody (Bd, Td)
  - Galactic synchrotron as power law in antenna temperature
Both converted to CMB (thermodynamic) units.
"""
import numpy as np

T_CMB = 2.7255  # K
h_planck = 6.62607015e-34
k_B = 1.380649e-23
c_light = 2.99792458e8


def planck_bnu(nu_hz, T):
    x = h_planck * nu_hz / (k_B * T)
    return (2.0 * h_planck * nu_hz**3 / c_light**2) / (np.exp(x) - 1.0)


def dBdT_cmb(nu_hz):
    """Derivative of Planck function wrt T at T_CMB (for conversion)."""
    x = h_planck * nu_hz / (k_B * T_CMB)
    return (2.0 * h_planck**2 * nu_hz**4 / (c_light**2 * k_B * T_CMB**2)) \
        * np.exp(x) / (np.exp(x) - 1.0)**2


def rj_to_cmb(nu_ghz):
    """Convert Rayleigh-Jeans (antenna) temperature to thermodynamic CMB temperature.
    T_RJ = (2 nu^2 kB / c^2) -> uK_RJ to uK_CMB factor: dB/dT_RJ over dB/dT_CMB.
    Actually: I_nu_RJ = 2 nu^2 kB T_RJ / c^2. For small fluctuations:
    T_CMB = T_RJ * (dB/dT_RJ) / (dB/dT_CMB) where dB/dT_RJ = 2 nu^2 kB / c^2.
    """
    nu = nu_ghz * 1e9
    dBdT_rj = 2.0 * nu**2 * k_B / c_light**2
    return dBdT_rj / dBdT_cmb(nu)


def dust_sed_cmb(nu_ghz, nu0=353.0, beta=1.54, T_d=20.0):
    """Modified blackbody dust SED, returned as factor in thermodynamic CMB units,
    normalized so dust_sed_cmb(nu0) = 1 (amplitude specified at nu0 in uK_CMB)."""
    nu = nu_ghz * 1e9
    nu0h = nu0 * 1e9
    # MBB in intensity
    num = (nu / nu0h)**(beta + 3.0) * (np.exp(h_planck * nu0h / (k_B * T_d)) - 1.0) \
        / (np.exp(h_planck * nu / (k_B * T_d)) - 1.0)
    # Convert from intensity ratio to CMB thermodynamic ratio
    # I_nu = A * MBB(nu). dT_CMB = dI / (dB/dT_CMB)
    factor = num * dBdT_cmb(nu0h) / dBdT_cmb(nu)
    return factor


def sync_sed_cmb(nu_ghz, nu0=30.0, beta_s=-3.1):
    """Power-law synchrotron in antenna (RJ) units, converted to CMB thermo.
    Normalized to unity at nu0 in CMB units."""
    nu = nu_ghz * 1e9
    nu0h = nu0 * 1e9
    # Ratio in RJ
    rj_ratio = (nu / nu0h)**beta_s
    # Convert RJ -> CMB for both: T_CMB(nu) / T_CMB(nu0) = rj_ratio * (rj_to_cmb(nu) / rj_to_cmb(nu0))
    return rj_ratio * (rj_to_cmb(nu_ghz) / rj_to_cmb(nu0))


def cmb_sed(nu_ghz):
    return np.ones_like(np.atleast_1d(nu_ghz).astype(float))
