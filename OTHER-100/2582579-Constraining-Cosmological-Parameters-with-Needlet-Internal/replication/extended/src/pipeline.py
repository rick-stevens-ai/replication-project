"""End-to-end NILC pipeline: sim -> common beam -> NILC -> Cl -> diagnostics."""
import os
import numpy as np
import healpy as hp
from . import config as cfg
from . import simulate as sim
from . import needlets as ndl
from . import nilc as nilc_mod


def deconvolve_to_common_beam(maps, beam_bls, target_bl, lmax):
    nfreq = maps.shape[0]
    nside = hp.npix2nside(maps.shape[1])
    out = np.zeros_like(maps)
    for i in range(nfreq):
        alm = hp.map2alm(maps[i], lmax=lmax)
        ratio = np.zeros(lmax + 1)
        mask = beam_bls[i] > 1e-5
        ratio[mask] = target_bl[mask] / beam_bls[i][mask]
        alm = hp.almxfl(alm, ratio)
        out[i] = hp.alm2map(alm, nside=nside, verbose=False)
    return out


def run_pipeline(outdir):
    os.makedirs(outdir, exist_ok=True)
    print('[1/5] Simulating sky...')
    sim.simulate_sky(outdir)
    d = np.load(os.path.join(outdir, 'sim.npz'))
    maps = d['maps']
    beam_bls = d['beam_bls']

    print('[2/5] Deconvolving to common beam (worst beam = 14 arcmin)...')
    target_fwhm = float(np.max(cfg.FWHM_ARCMIN))  # arcmin
    target_bl = hp.gauss_beam(np.deg2rad(target_fwhm / 60.0), lmax=cfg.LMAX)
    maps_cb = deconvolve_to_common_beam(maps, beam_bls, target_bl, cfg.LMAX)

    print('[3/5] Building cosine needlet bank...')
    bank, peaks = ndl.cosine_needlet_bank(cfg.LMAX, cfg.N_NEEDLETS)

    print('[4/5] Running NILC...')
    cmb_nilc, weights, filt = nilc_mod.nilc_separate(maps_cb, bank, cfg.LMAX)

    print('[5/5] Computing power spectra...')
    # Deconvolve target beam from recovered CMB to get unbiased Cl
    alm = hp.map2alm(cmb_nilc, lmax=cfg.LMAX)
    ratio = np.zeros_like(target_bl)
    mask = target_bl > 1e-5
    ratio[mask] = 1.0 / target_bl[mask]
    alm = hp.almxfl(alm, ratio)
    cl_nilc = hp.alm2cl(alm)

    # True CMB Cl from input realization (no noise, no beam)
    cl_cmb_real = hp.anafast(d['cmb_map'], lmax=cfg.LMAX)
    # Theory Cl
    cl_theory = d['cl_tt']

    np.savez(os.path.join(outdir, 'nilc_result.npz'),
             cmb_nilc=cmb_nilc, cl_nilc=cl_nilc,
             cl_cmb_real=cl_cmb_real, cl_theory=cl_theory,
             bank=bank, peaks=peaks, target_bl=target_bl)
    print('Done. Results in', outdir)
    return cmb_nilc, cl_nilc, cl_cmb_real, cl_theory
