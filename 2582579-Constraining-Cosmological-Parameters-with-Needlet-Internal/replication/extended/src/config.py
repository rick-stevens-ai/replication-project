"""Configuration for NILC replication (OSTI 2582579)."""
import numpy as np

# Resolution / band-limits
NSIDE = 128
LMAX = 3 * NSIDE - 1  # 383
NPIX = 12 * NSIDE * NSIDE

# Planck-like frequencies (GHz) - 5-channel subset (drop 30/44 GHz whose big
# beams + deep galactic synchrotron power make deconvolution unstable at our
# chosen common beam).
FREQS = np.array([70.0, 100.0, 143.0, 217.0, 353.0])

# Beam FWHM in arcmin (approximate Planck values)
FWHM_ARCMIN = np.array([14.0, 10.0, 7.1, 5.5, 5.0])

# White-noise level in uK_CMB * arcmin (approximate Planck-like)
NOISE_UKARCMIN = np.array([150., 65., 43., 67., 200.])

# Fiducial LCDM (Planck 2018 TT,TE,EE+lowE+lensing best-fit-ish)
FID = dict(
    H0=67.36,
    ombh2=0.02237,
    omch2=0.12,
    tau=0.0544,
    As=2.1e-9,
    ns=0.9649,
)

# Needlet: cosine-squared bank; 6 scales covering [0, LMAX]
N_NEEDLETS = 6

# Random seed
SEED = 20260424
