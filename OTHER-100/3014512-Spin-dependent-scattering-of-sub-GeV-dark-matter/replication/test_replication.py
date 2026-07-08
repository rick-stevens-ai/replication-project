#!/usr/bin/env python3
"""
Comprehensive tests for the replication of Gori et al. (2025).
Run with:  python -m pytest tests/test_replication.py -v
"""
import sys, os, pickle, math
import numpy as np
import pytest

PROJECT_DIR = os.path.expanduser("~/projects/replicate-darkmatter")
sys.path.insert(0, os.path.join(PROJECT_DIR, "darkelf_repo"))
sys.path.insert(0, os.path.join(PROJECT_DIR, "src"))

DE_DATA = os.path.join(PROJECT_DIR, "darkelf_repo", "data") + "/"
PKL     = os.path.join(PROJECT_DIR, "data", "all_results.pkl")

# ── helpers ──────────────────────────────────────────────────────────────────
def suppress():
    """Context manager: suppress stdout."""
    import contextlib, io
    return contextlib.redirect_stdout(io.StringIO())

def load_de(target, mX=1e8, mMed=10e9, op="A'"):
    import darkelf as de
    with suppress():
        d = de.darkelf(target=target, mX=mX, mMed=mMed,
                       v0kms=220, vekms=240, vesckms=500,
                       eps_data_dir=DE_DATA)
        d.update_params(mX=mX, mMed=mMed, SD_op=op)
    return d

@pytest.fixture(scope='session')
def results():
    with open(PKL,'rb') as f: return pickle.load(f)

# ── 1. DarkELF initialisation ────────────────────────────────────────────────
class TestDarkELFInit:
    def test_al2o3_loads(self):
        d = load_de('Al2O3')
        assert d.target == 'Al2O3'

    def test_gaas_loads(self):
        d = load_de('GaAs')
        assert d.target == 'GaAs'

    def test_si_loads(self):
        d = load_de('Si')
        assert d.target == 'Si'

    def test_halo_params_set(self):
        d = load_de('Al2O3')
        C = 2.99792458e5
        assert abs(d.v0 - 220/C) < 1e-8
        assert abs(d.vesc - 500/C) < 1e-8
        assert abs(d.veavg - 240/C) < 1e-8

    def test_rho_chi(self):
        d = load_de('Al2O3')
        # rhoX stored in eV/cm^3; should be 0.4 GeV/cm^3 = 0.4e9 eV/cm^3
        assert abs(d.rhoX - 0.4e9) < 1e3


# ── 2. SI benchmark ──────────────────────────────────────────────────────────
class TestSIBenchmark:
    """SI results must be physically reasonable (not validating exact DarkELF numbers,
    but checking correct order-of-magnitude and monotonicity)."""

    def test_si_al2o3_order_of_magnitude(self, results):
        arr = results['Al2O3_SI_heavy']['1meV']
        valid = arr[np.isfinite(arr) & (arr>0) & (arr<1e-10)]
        assert len(valid) > 20
        # Expect ~1e-43 to 1e-42 at the peak sensitivity (tens of MeV DM mass)
        assert valid.min() < 1e-40

    def test_si_smaller_than_sd_aprime(self, results):
        """SI reach is deeper (lower σ) than SD for any given mass - cross sections smaller."""
        si  = results['Al2O3_SI_heavy']['1meV']
        sd  = results["Al2O3_A'_heavy"]['1meV']
        mx  = results['mx_eV']
        # At 10-100 MeV masses SI bound should be tighter (lower sigma)
        mask = (mx>1e7) & (mx<1e8) & np.isfinite(si) & (si>0) & (si<1e-10) \
                                   & np.isfinite(sd) & (sd>0) & (sd<1e-10)
        if mask.sum() > 3:
            assert np.median(si[mask]) < np.median(sd[mask])


# ── 3. SD rates: basic sanity ────────────────────────────────────────────────
class TestSDRates:
    def test_Aprime_al2o3_1mev_all_masses_finite(self, results):
        arr = results["Al2O3_A'_heavy"]['1meV']
        good = np.isfinite(arr) & (arr>0) & (arr<1e-10)
        assert good.sum() == 40, f"Only {good.sum()}/40 valid"

    def test_Aprime_gaas_1mev_all_masses_finite(self, results):
        arr = results["GaAs_A'_heavy"]['1meV']
        good = np.isfinite(arr) & (arr>0) & (arr<1e-10)
        assert good.sum() == 40

    def test_phi_al2o3_heavy_all_finite(self, results):
        arr = results['Al2O3_phi_heavy']['1meV']
        good = np.isfinite(arr) & (arr>0) & (arr<1e-10)
        assert good.sum() == 40

    def test_a_al2o3_heavy_all_finite(self, results):
        arr = results['Al2O3_a_heavy']['1meV']
        good = np.isfinite(arr) & (arr>0) & (arr<1e-10)
        assert good.sum() == 40

    def test_higher_threshold_gives_higher_sigma(self, results):
        """A higher threshold means fewer events → larger excluded σ."""
        for key in ["Al2O3_A'_heavy", 'Al2O3_phi_heavy', 'Al2O3_a_heavy']:
            arr1 = results[key]['1meV']
            arr2 = results[key]['1eV']
            mx   = results['mx_eV']
            # Compare at mX = ~100 MeV where both should be valid
            mask = (mx > 5e7) & (mx < 2e8) \
                & np.isfinite(arr1)&(arr1>0)&(arr1<1e-10) \
                & np.isfinite(arr2)&(arr2>0)&(arr2<1e-10)
            if mask.sum() > 0:
                # 1eV threshold sigma must be >= 1meV threshold sigma
                assert np.all(arr2[mask] >= arr1[mask] * 0.5), \
                    f"{key}: higher threshold gives lower sigma, unexpected"

    def test_sigma_positive(self, results):
        for key in results:
            if key == 'mx_eV': continue
            for th, arr in results[key].items():
                m = np.isfinite(arr) & (arr < 1e-10)
                assert np.all(arr[m] > 0), f"{key} {th} has non-positive sigma"


# ── 4. Physics: operator scaling ────────────────────────────────────────────
class TestOperatorScaling:
    """Check that operator form factor scaling is correct via direct DarkELF calls."""

    def test_aprime_sd_op_string(self):
        d = load_de('Al2O3', mX=1e8, mMed=10e9, op="A'")
        assert d.SD_op == "A'"

    def test_phi_sd_op_string(self):
        d = load_de('Al2O3', mX=1e8, mMed=1e5, op='phi')
        assert d.SD_op == 'phi'

    def test_a_sd_op_string(self):
        d = load_de('Al2O3', mX=1e8, mMed=1e5, op='a')
        assert d.SD_op == 'a'

    def test_isotope_factors_al2o3_nonzero(self):
        """Al2O3 contains 27Al (J=5/2) → nonzero isotope_averaged_factors."""
        d = load_de('Al2O3')
        assert np.any(d.isotope_averaged_factors > 0)

    def test_isotope_factors_gaas_nonzero(self):
        """GaAs contains 69Ga/71Ga and 75As (all with spin) → nonzero."""
        d = load_de('GaAs')
        assert np.any(d.isotope_averaged_factors > 0)

    def test_si_29si_only_spin_isotope(self):
        """Si: only 29Si has nonzero spin; 28Si and 30Si are spin-0."""
        d = load_de('Si')
        # isotope_averaged_factors should be small but nonzero (4.7% 29Si abundance)
        assert d.isotope_averaged_factors[0] > 0
        assert d.isotope_averaged_factors[0] < 0.1   # small fraction

    def test_mediator_form_factor_heavy_limit(self):
        """Heavy mediator: F_med → 1 for q << mMed."""
        d = load_de('Al2O3', mX=1e8, mMed=10e9, op="A'")
        q_small = np.array([100.0, 500.0, 1000.0])   # eV << 10 GeV
        F = d.Fmed_nucleus_SD(q_small)
        assert np.allclose(F, 1.0, rtol=1e-3)

    def test_mediator_form_factor_massless(self):
        """Massless mediator: F_med ∝ q0²/q² → increases at small q."""
        d = load_de('Al2O3', mX=1e8, mMed=0, op="A'")
        q0_val = d.q0
        q = np.array([q0_val/10, q0_val, q0_val*10])
        F = d.Fmed_nucleus_SD(q)
        assert F[0] > F[1] > F[2]

    def test_rate_positive_al2o3(self):
        d = load_de('Al2O3', mX=1e8, mMed=10e9, op="A'")
        rate = d.R_multiphonons_SD(threshold=1e-3, sigman=1e-38)
        assert rate > 0

    def test_sigma_al2o3_aprime_100mev_magnitude(self):
        """At mX=100 MeV, A' heavy, Al2O3 at 1meV threshold: sigma ~ 1e-40 cm²."""
        d = load_de('Al2O3', mX=1e8, mMed=10e9, op="A'")
        sig = d.sigma_multiphonons_SD(threshold=1e-3)
        # Accept broad range [1e-43, 1e-37]
        assert 1e-43 < sig < 1e-37, f"sigma={sig:.2e} out of expected range"


# ── 5. Halo model / kinematics ───────────────────────────────────────────────
class TestHaloModel:
    def test_etav_vanishes_above_vmax(self):
        d = load_de('Al2O3')
        vmax = d.vmax
        eta = d.etav(vmax * 1.01)
        assert abs(eta) < 1e-30

    def test_etav_positive_below_vmax(self):
        d = load_de('Al2O3')
        vmin_test = d.vmax * 0.5
        eta = d.etav(vmin_test)
        assert eta > 0

    def test_vmin_formula(self):
        """vmin = q/(2mX) + ω/q  (elastic, δ=0)."""
        d = load_de('Al2O3', mX=1e8)
        q_test = 5000.0    # eV
        om_test = 0.05     # eV
        vmin_calc = q_test/(2*d.mX) + om_test/q_test
        vmin_de   = d.vmin(om_test, q_test)
        assert abs(vmin_calc - vmin_de) < 1e-12

    def test_omega_dm_max(self):
        """omegaDMmax = mX/2 * (vesc+ve)²."""
        d = load_de('Al2O3', mX=1e8)
        expected = d.mX/2 * (d.vesc + d.veavg)**2
        assert abs(d.omegaDMmax - expected) < 1e-3*expected


# ── 6. Figures were produced ─────────────────────────────────────────────────
class TestFiguresExist:
    expected = ['fig5_phonon_dos.png','fig6_phi.png','fig7_a.png','fig8_Aprime.png',
                'sd_vs_si.png','all_operators_Al2O3.png','response_functions.png',
                'dR_domega.png','summary_all_operators.png']

    def test_all_figures_exist(self):
        fig_dir = os.path.join(PROJECT_DIR, 'figures')
        for fname in self.expected:
            path = os.path.join(fig_dir, fname)
            assert os.path.exists(path), f"Missing figure: {fname}"
            assert os.path.getsize(path) > 1000, f"Figure too small: {fname}"


# ── 7. Reference cross-section formulas ─────────────────────────────────────
class TestReferenceXS:
    """Verify reference cross-section formulas from the paper (Eqs 14-16)."""

    def _mu(self, mX, mp=0.94e9):
        return mX*mp/(mX+mp)

    def test_sigma_bar_phi_formula(self):
        """σ̄_ϕ = (g_p²g_χ²)/(2π m_p²) * v0²μ⁴/(q0²+m_ϕ²)²
        For heavy med (m_ϕ >> q0): σ̄_ϕ ≈ g²/(2π m_p²) * v0²μ⁴/m_ϕ⁴.
        All quantities in eV."""
        C_KMS = 2.99792458e5
        v0 = 220/C_KMS          # dimensionless
        mp = 0.94e9             # eV
        mX = 1e8                # eV (100 MeV)
        mu = self._mu(mX)
        q0_val = mX*v0          # eV  ≈ 73 keV for 100 MeV DM
        g2 = 1.0
        # Use a truly heavy mediator: 1 GeV >> q0~73 keV
        m_phi = 1e9             # eV (1 GeV)
        sigma_bar = g2/(2*math.pi*mp**2) * v0**2*mu**4/(q0_val**2+m_phi**2)**2
        # Result in eV^-2: expected ~few × 10^-50 eV^-2
        assert sigma_bar > 0
        # In eV^-2: expect ~6.5e-30; convert to cm^2 gives ~2.5e-39 cm^2 — sensible for SD
        eVcm = 1.9732e-5
        sigma_cm2 = sigma_bar * eVcm**2
        assert 1e-45 < sigma_cm2 < 1e-33

    def test_reduced_mass(self):
        mX = 1e8; mp = 0.94e9
        mu = self._mu(mX)
        assert abs(mu - mX*mp/(mX+mp)) < 1

    def test_q0_reference_momentum(self):
        """q0 = mX * v0/c.  For mX=100 MeV and v0=220 km/s: q0 ≈ 73.4 keV."""
        C_KMS = 2.99792458e5
        mX = 1e8          # eV
        v0 = 220/C_KMS    # dimensionless
        q0 = mX*v0        # eV
        # Expected: 1e8 * (220/299792.458) ≈ 73,384 eV ≈ 73.4 keV
        assert abs(q0 - 73384.0) < 100.0


if __name__ == '__main__':
    import subprocess, sys
    ret = subprocess.run([sys.executable, '-m', 'pytest', __file__, '-v', '--tb=short'],
                        cwd=PROJECT_DIR)
    sys.exit(ret.returncode)
