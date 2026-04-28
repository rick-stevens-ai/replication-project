"""Preprocess WebSky inputs:
  - lensed_alm.fits (uK alms)  -> cmb_lensed_nsideX_K.fits (Kelvin map at nside)
  - tsz_2048.fits (dimensionless y) -> tsz_nsideX.fits (y map at nside)
Target nside default 32 (paper), but we keep at 1024 (matches authors' example yaml)
so that the NILC-PS-Model degrades it internally.
"""
import os, sys
import numpy as np
import healpy as hp

INDIR = 'inputs'
NSIDE_OUT = int(sys.argv[1]) if len(sys.argv) > 1 else 128
# Authors' yaml had cmb at nside=1024. We use 128 for speed; pipeline degrades
# to nside=32 internally.

# 1) CMB: lensed_alm is uK. Load alms (may be complex); take TT only (index 0)
print(f'Loading lensed_alm.fits ...', flush=True)
alm_all = hp.read_alm(os.path.join(INDIR, 'lensed_alm.fits'), hdu=(1, 2, 3))
# Some files have a single HDU; try-except
if hasattr(alm_all, 'shape') and alm_all.ndim == 2:
    alm_T = alm_all[0]
else:
    alm_T = alm_all
print(f'  alm_T size: {len(alm_T)}  lmax inferred: {hp.Alm.getlmax(len(alm_T))}')
# Band-limit to 3*NSIDE_OUT-1 for speed
lmax_in = hp.Alm.getlmax(len(alm_T))
lmax_cut = min(lmax_in, 3 * NSIDE_OUT - 1)
if lmax_cut < lmax_in:
    # Make truncated alm array
    new_alm = np.zeros(hp.Alm.getsize(lmax_cut), dtype=alm_T.dtype)
    for l in range(lmax_cut + 1):
        for m in range(l + 1):
            new_alm[hp.Alm.getidx(lmax_cut, l, m)] = alm_T[hp.Alm.getidx(lmax_in, l, m)]
    alm_T = new_alm
print(f'  synthesizing at nside={NSIDE_OUT}, lmax={lmax_cut}', flush=True)
cmb_uK = hp.alm2map(alm_T, nside=NSIDE_OUT, lmax=lmax_cut)
cmb_K = 1e-6 * cmb_uK
out_cmb = os.path.join(INDIR, f'cmb_lensed_nside{NSIDE_OUT}_K.fits')
hp.write_map(out_cmb, cmb_K, overwrite=True, dtype=np.float32)
print(f'  wrote {out_cmb}  rms={cmb_K.std():.3e} K')

# 2) tSZ: y-map, degrade
print(f'Loading tsz_2048.fits ...', flush=True)
y = hp.read_map(os.path.join(INDIR, 'tsz_2048.fits'))
print(f'  input nside={hp.get_nside(y)}, mean y={y.mean():.3e}, max={y.max():.3e}')
y_out = hp.ud_grade(y, NSIDE_OUT)
out_tsz = os.path.join(INDIR, f'tsz_nside{NSIDE_OUT}.fits')
hp.write_map(out_tsz, y_out, overwrite=True, dtype=np.float32)
print(f'  wrote {out_tsz}')
print('Done.')
