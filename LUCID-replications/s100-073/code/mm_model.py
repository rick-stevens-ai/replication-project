"""
Manchester Mechanistic (MM) model RBE equations from
Smith et al. 2019, Sci Rep 9:19870 (doi:10.1038/s41598-019-56258-5).

Implements Eqs. 4, 5, 6, 7, 8 with Table 1 parameter values.

All RBE_x values are dimensionless. Inputs:
  D       - proton absorbed dose, Gy
  LET_d   - dose-averaged LET, keV/um
  LET_t   - track-averaged LET, keV/um
  alpha_beta_x - tissue alpha/beta ratio for the *photon* reference, Gy
"""

from math import sqrt

# ----------------------------------------------------------------------
# Table 1 parameters (Smith et al. 2019)
# ----------------------------------------------------------------------
# McNamara (2015) phenomenological model:
Z1 = 0.99064
Z2 = 0.35605
Z3 = 1.1012
Z4 = 0.00387

# LET_d-weighted dose (McMahon 2018). NOTE: Table 1 lists 0.0055 but the
# paper text + Fig. 2 caption + cited source all use 0.055. We follow the
# corrected (text/source) value here.
KAPPA = 0.055  # um/keV  -- corrected from Table 1's likely typo of 0.0055
KAPPA_TABLE1 = 0.0055  # value as printed in Table 1 (likely typo)

# MM correlations (Henthorn 2018, repeated in Smith 2019 Table 1):
a = 0.1966
b = 0.008
c = 0.0736
d = 1.149      # um keV^-1 Gy^-1
e = 24.1       # Gy^-1
f = 4.879e-4   # um^2 keV^-2
g = 2.84e-3    # um keV^-1
h = 5.13e-2

# Photon (Co-60) reference yields per Gy:
GAMMA_R = 1.726   # residual DSB / Gy
GAMMA_M = 0.0427  # misrepaired DSB / Gy

# ----------------------------------------------------------------------
# Eq. 4: LET_d-weighted dose
# ----------------------------------------------------------------------
def dose_letd_weighted(D, LET_d, kappa=KAPPA):
    """Eq. 4: Dose_w = D * (1 + kappa * LET_d)"""
    return D * (1.0 + kappa * LET_d)

def rbe_letd_weighted(LET_d, kappa=KAPPA):
    return 1.0 + kappa * LET_d

# ----------------------------------------------------------------------
# Eq. 5: McNamara phenomenological RBE
# ----------------------------------------------------------------------
def rbe_mcnamara(D, LET_d, alpha_beta_x):
    """
    McNamara 2015 RBE model. Returns RBE such that Dose_McN = D * RBE.

    RBE = (1/(2D)) * sqrt( (alpha/beta_x)^2
                          + 4 D (alpha/beta_x) (Z1 + Z2/(alpha/beta_x) * LET_d)
                          + 4 D^2 (Z3 - Z4 * sqrt(alpha/beta_x))^2 )
          - (alpha/beta_x)/(2D)
    """
    ab = alpha_beta_x
    inside = (ab * ab
              + 4.0 * D * ab * (Z1 + (Z2 / ab) * LET_d)
              + 4.0 * D * D * (Z3 - Z4 * sqrt(ab)) ** 2)
    return (1.0 / (2.0 * D)) * sqrt(inside) - ab / (2.0 * D)

def dose_mcnamara(D, LET_d, alpha_beta_x):
    return D * rbe_mcnamara(D, LET_d, alpha_beta_x)

# ----------------------------------------------------------------------
# MM correlations (Eqs. 6, 7, 8)
# ----------------------------------------------------------------------
def yield_residual_proton(D, LET_t):
    """Numerator of Eq. 6: predicted residual DSB yield per cell (proton)."""
    return (d * LET_t + e) * c * D

def yield_misrepair_proton(D, LET_t):
    """Numerator of Eq. 7: predicted misrepaired DSB yield per cell (proton)."""
    return (d * LET_t + e) * (a * (f * LET_t * LET_t + g * LET_t + h) + b) * (1.0 - c) * D

def yield_residual_photon(D):
    """Photon reference residual DSB yield = gamma_r * D."""
    return GAMMA_R * D

def yield_misrepair_photon(D):
    """Photon reference misrepair DSB yield = gamma_m * D."""
    return GAMMA_M * D

def rbe_residual(LET_t):
    """Eq. 6: RBE_r = [(d*LET_t + e) * c] / gamma_r  (D cancels)."""
    return (d * LET_t + e) * c / GAMMA_R

def rbe_misrepair(LET_t):
    """Eq. 7: RBE_m = [(d*LET_t + e) * (a*(f*LET_t^2 + g*LET_t + h) + b) * (1-c)] / gamma_m."""
    return (d * LET_t + e) * (a * (f * LET_t * LET_t + g * LET_t + h) + b) * (1.0 - c) / GAMMA_M

def rbe_residual_and_misrepair(LET_t):
    """Eq. 8: combined RBE = (residual + misrepair numerators) / (gamma_r + gamma_m)."""
    num = ((d * LET_t + e) * c
           + (d * LET_t + e) * (a * (f * LET_t * LET_t + g * LET_t + h) + b) * (1.0 - c))
    return num / (GAMMA_R + GAMMA_M)

def dose_residual(D, LET_t):
    return D * rbe_residual(LET_t)

def dose_misrepair(D, LET_t):
    return D * rbe_misrepair(LET_t)

def dose_residual_and_misrepair(D, LET_t):
    return D * rbe_residual_and_misrepair(LET_t)


if __name__ == "__main__":
    # quick self-test
    print("Sanity at LET_t = 0:")
    print(f"  RBE_r    = {rbe_residual(0):.6f}")
    print(f"  RBE_m    = {rbe_misrepair(0):.6f}")
    print(f"  RBE_r&m  = {rbe_residual_and_misrepair(0):.6f}")
    # All three should be exactly 1.0 because at LET_t = 0 the proton equation
    # reduces algebraically to the photon reference.
