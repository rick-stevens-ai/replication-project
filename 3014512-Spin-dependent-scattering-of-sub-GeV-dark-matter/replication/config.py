"""
Configuration and physical constants for the replication of
Gori, Knapen, Lin, Munbodh, Suter (PRD 112, 075019, 2025)
"Spin-Dependent Scattering of Sub-GeV Dark Matter"
"""
import numpy as np
import os

# ===== Paths =====
PROJECT_DIR = os.path.expanduser("~/projects/replicate-darkmatter")
DARKELF_REPO = os.path.join(PROJECT_DIR, "darkelf_repo")
DATA_DIR = os.path.join(DARKELF_REPO, "data")
FIGURES_DIR = os.path.join(PROJECT_DIR, "figures")
REPORT_DIR = os.path.join(PROJECT_DIR, "report")

# ===== Standard Halo Model parameters =====
V0_KMS = 220.0      # v0 in km/s
VE_KMS = 240.0      # Earth velocity in km/s
VESC_KMS = 500.0     # Escape velocity in km/s (paper uses 500)
RHO_CHI = 0.4e9     # DM density in eV/cm^3 (0.4 GeV/cm^3)

# ===== Physical constants =====
MP_EV = 0.94e9       # Proton mass in eV
ME_EV = 511e3        # Electron mass in eV
C_KMS = 2.99792458e5 # Speed of light in km/s
ALPHA_EM = 1.0/137.0

# ===== DM mass range =====
MX_MIN = 1e3   # 1 MeV in eV  
MX_MAX = 1e9   # 1 GeV in eV
N_MX = 60      # Number of mass points

# ===== Mediator models =====
# Benchmark mediator masses relative to q0 = mX * v0
LIGHT_FACTOR = 0.3   # m_med = 0.3 * q0
HEAVY_FACTOR = 3.0   # m_med = 3.0 * q0
MA_PRIME = 10e9       # A' mediator mass = 10 GeV in eV

# ===== Threshold energies (eV) =====
THRESHOLDS = {
    '1meV': 1e-3,
    '20meV': 20e-3,
    '100meV': 100e-3,
    '1eV': 1.0,
}

# ===== Target materials =====
TARGETS = ['Al2O3', 'GaAs', 'Si', 'Ge']

# ===== Operators =====
SD_OPERATORS = ['phi', 'a', "A'"]

# ===== UV completion parameters (Eq. 20-29) =====
FA = 1e3  # fa = 1 TeV in GeV
GP_CGG = 8.11e-4   # gp ≈ 8.11e-4 * c_GG (Eq. 22)
GN_CGG = -3.50e-5  # gn ≈ -3.50e-5 * c_GG (Eq. 24)
GA = 1.2754         # axial coupling from beta decay
G0 = 0.440          # singlet coupling from lattice QCD

# ===== KSVZ bounds =====
CGG_MAX = 20.0      # c_GG <= 20 (Eq. 29)
GP_MAX = 2e-2       # |gp| <= 2e-2
GN_MAX = 7e-4       # |gn| <= 7e-4

# ===== SIDM bound =====
SIGMA_OVER_MX_BOUND = 1.1  # cm^2/g
V_SIDM = 0.005             # v/c ~ 0.005 (1430 km/s)

# ===== Supernova constraints =====
# Trapping window for gp: ~2e-6 to 7e-6
GP_SN_LOW = 2e-6
GP_SN_HIGH = 7e-6

def mx_range_eV(n=N_MX):
    """DM mass range in eV, logarithmically spaced."""
    return np.logspace(np.log10(MX_MIN), np.log10(MX_MAX), n)

def q0(mX_eV):
    """Reference momentum q0 = mX * v0 in eV."""
    return mX_eV * V0_KMS / C_KMS

def mediator_mass_light(mX_eV):
    """Light mediator benchmark: m_med = 0.3 * q0."""
    return LIGHT_FACTOR * q0(mX_eV)

def mediator_mass_heavy(mX_eV):
    """Heavy mediator benchmark: m_med = 3 * q0."""
    return HEAVY_FACTOR * q0(mX_eV)
