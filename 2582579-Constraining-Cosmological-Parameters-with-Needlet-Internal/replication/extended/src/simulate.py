"""Generate synthetic multi-frequency sky maps for NILC test.

Components:
  - CMB (from CAMB fiducial LCDM) - Gaussian realization
  - Galactic dust (MBB, single template with amplitude Cl_dust)
  - Galactic synchrotron (power-law, single template)
  - White noise per frequency

Each freq channel = sum_c SED_c(nu) * T_c(p), convolved with a Gaussian beam,
plus white noise.
"""
import os
import numpy as np
import healpy as hp
import camb
from . import config as cfg
from . import foregrounds as fg


def fiducial_cmb_cls(As=cfg.FID['As'], ns=cfg.FID['ns'], H0=cfg.FID['H0'],
                     ombh2=cfg.FID['ombh2'], omch2=cfg.FID['omch2'],
                     tau=cfg.FID['tau'], lmax=cfg.LMAX):
    pars = camb.CAMBparams()
    pars.set_cosmology(H0=H0, ombh2=ombh2, omch2=omch2, tau=tau)
    pars.InitPower.set_params(As=As, ns=ns)
    pars.set_for_lmax(lmax, lens_potential_accuracy=1)
    res = camb.get_results(pars)
    # totCL returns ell(ell+1)Cl/2pi in uK^2 for TT, EE, BB, TE (if cp units = muK)
    powers = res.get_cmb_power_spectra(pars, CMB_unit='muK', raw_cl=True)
    totCL = powers['total']  # shape (lmax+1, 4): TT, EE, BB, TE (raw Cl in uK^2)
    ell = np.arange(totCL.shape[0])
    cl_tt = totCL[:, 0]
    return ell, cl_tt


def foreground_cl_templates(lmax=cfg.LMAX):
    """Simple power-law Cl templates (uK_CMB^2) for dust at 353 GHz and sync at 30 GHz."""
    ell = np.arange(lmax + 1, dtype=float)
    ell_safe = np.where(ell < 2, 2, ell)
    # Dust: D_ell (= ell(ell+1)Cl/2pi) approx ~ ell^-0.4, amplitude ~ 1e3 uK^2 at ell=80, 353 GHz
    Dl_dust_80 = 1.0e3  # uK_CMB^2 at 353 GHz
    Dl_dust = Dl_dust_80 * (ell_safe / 80.0)**(-0.4)
    cl_dust = 2.0 * np.pi * Dl_dust / (ell_safe * (ell_safe + 1.0))
    cl_dust[:2] = 0.0
    # Sync: amplitude ~ 200 uK^2 at ell=80, 30 GHz, Dl ~ ell^-0.6
    Dl_sync_80 = 200.0
    Dl_sync = Dl_sync_80 * (ell_safe / 80.0)**(-0.6)
    cl_sync = 2.0 * np.pi * Dl_sync / (ell_safe * (ell_safe + 1.0))
    cl_sync[:2] = 0.0
    return cl_dust, cl_sync


def gaussian_beam_bl(fwhm_arcmin, lmax):
    fwhm_rad = np.deg2rad(fwhm_arcmin / 60.0)
    return hp.gauss_beam(fwhm_rad, lmax=lmax)


def noise_cl(noise_ukarcmin, lmax):
    sigma_rad = np.deg2rad(noise_ukarcmin / 60.0)  # uK * rad
    return np.full(lmax + 1, sigma_rad**2)


def simulate_sky(outdir, seed=cfg.SEED):
    os.makedirs(outdir, exist_ok=True)
    rng = np.random.default_rng(seed)
    lmax = cfg.LMAX

    # 1) CMB realization (single sky)
    ell, cl_tt = fiducial_cmb_cls(lmax=lmax)
    # healpy synfast: needs Cl
    cmb_map = hp.synfast(cl_tt, nside=cfg.NSIDE, new=True, verbose=False)

    # 2) Foreground templates (single realization each)
    cl_dust, cl_sync = foreground_cl_templates(lmax=lmax)
    dust_template = hp.synfast(cl_dust, nside=cfg.NSIDE, new=True, verbose=False)
    sync_template = hp.synfast(cl_sync, nside=cfg.NSIDE, new=True, verbose=False)

    # 3) Build per-frequency maps
    freqs = cfg.FREQS
    nfreq = len(freqs)
    maps = np.zeros((nfreq, cfg.NPIX))
    beam_bls = np.zeros((nfreq, lmax + 1))

    for i, nu in enumerate(freqs):
        # Components in uK_CMB
        cmb_c = cmb_map * fg.cmb_sed(nu)[0]
        dust_c = dust_template * fg.dust_sed_cmb(nu, nu0=353.0)
        sync_c = sync_template * fg.sync_sed_cmb(nu, nu0=30.0)
        total = cmb_c + dust_c + sync_c
        # Beam-convolve
        fwhm = cfg.FWHM_ARCMIN[i]
        bl = gaussian_beam_bl(fwhm, lmax)
        alm = hp.map2alm(total, lmax=lmax)
        alm = hp.almxfl(alm, bl)
        smooth = hp.alm2map(alm, nside=cfg.NSIDE, verbose=False)
        # Add white noise (uK_CMB) in pixel space
        pix_area_arcmin2 = hp.nside2pixarea(cfg.NSIDE, degrees=True) * 60.0**2
        sigma_pix = cfg.NOISE_UKARCMIN[i] / np.sqrt(pix_area_arcmin2)
        noise = rng.normal(0.0, sigma_pix, cfg.NPIX)
        maps[i] = smooth + noise
        beam_bls[i] = bl

    # Save
    np.savez(os.path.join(outdir, 'sim.npz'),
             maps=maps, beam_bls=beam_bls,
             cmb_map=cmb_map, dust_template=dust_template, sync_template=sync_template,
             cl_tt=cl_tt, cl_dust=cl_dust, cl_sync=cl_sync,
             freqs=freqs, fwhm_arcmin=cfg.FWHM_ARCMIN,
             noise_ukarcmin=cfg.NOISE_UKARCMIN)
    return maps, beam_bls, cmb_map


if __name__ == '__main__':
    import sys
    outdir = sys.argv[1] if len(sys.argv) > 1 else 'data'
    simulate_sky(outdir)
    print(f'Sim written to {outdir}/sim.npz')
