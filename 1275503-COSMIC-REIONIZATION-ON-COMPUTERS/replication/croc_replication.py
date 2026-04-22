#!/usr/bin/env python3
"""
Replication of Gnedin, Becker & Fan (2017) - OSTI 1275503
"Cosmic Reionization On Computers: Properties of the Post-Reionization IGM"

Semi-analytic replication using the Fluctuating Gunn-Peterson Approximation (FGPA)
to generate synthetic Lyman-alpha forest spectra and reproduce key statistical analyses.

Author: Ollie (OpenClaw AI) for Rick Stevens' REPLICATE-PROJECT
Date: 2026-04-21
"""

import numpy as np
from scipy import stats, interpolate, fftpack
from scipy.ndimage import gaussian_filter1d
from scipy.integrate import quad
import os, json, warnings
warnings.filterwarnings('ignore')

OUTDIR = os.path.expanduser(
    "~/Dropbox/REPLICATE-PROJECT/1275503-COSMIC-REIONIZATION-ON-COMPUTERS/replication"
)
os.makedirs(os.path.join(OUTDIR, "figures"), exist_ok=True)

# ============================================================
# COSMOLOGICAL PARAMETERS  (WMAP-7, standard for CROC)
# ============================================================
Om, OL, Ob, h0, sig8, ns = 0.272, 0.728, 0.0449, 0.704, 0.81, 0.967
H0 = h0 * 100  # km/s/Mpc
Y_He = 0.24
c_kms = 2.998e5           # km/s
c_cgs = 2.998e10          # cm/s
kB    = 1.381e-16         # erg/K
mp    = 1.673e-24         # g
G_cgs = 6.674e-8          # cgs
e_esu = 4.803e-10
me    = 9.109e-28         # g
f_alpha    = 0.4162
lam_alpha  = 1215.67e-8   # cm

# ============================================================
# Cosmological helpers
# ============================================================
def Hz(z):
    return H0 * np.sqrt(Om*(1+z)**3 + OL)

def n_H_mean(z):
    """Mean hydrogen number density at z [cm^-3]."""
    rho_c0 = 3*(H0*1e5/3.086e24)**2/(8*np.pi*G_cgs)
    return rho_c0 * Ob * (1-Y_He) / mp * (1+z)**3

def dv_dz(z):
    """Velocity interval per unit redshift [km/s]."""
    return c_kms / (1+z)   # comoving-ish velocity

def comoving_to_velocity(L_Mpch, z):
    """Convert comoving h^-1 Mpc to km/s at redshift z."""
    return L_Mpch * Hz(z) / (1+z) / h0

# ============================================================
# Growth factor (Carroll, Press & Turner 1992)
# ============================================================
def growth(z):
    a = 1/(1+z)
    oma = Om/(Om + OL*a**3)
    ola = 1 - oma
    return a * 2.5*oma / (oma**(4/7) - ola + (1+oma/2)*(1+ola/70))

# ============================================================
# 1-D matter power spectrum  (BBKS transfer function)
# ============================================================
def P1d_matter(k, z):
    """P_1D(k) in (h^-1 Mpc) units, at redshift z."""
    Gamma = Om*h0*np.exp(-Ob*(1+np.sqrt(2*h0)/Om))
    q = np.where(k>0, k/(Gamma*h0), 1e-10)
    Tk = np.log(1+2.34*q)/(2.34*q+1e-30) * \
         (1 + 3.89*q + (16.1*q)**2 + (5.46*q)**3 + (6.71*q)**4)**(-0.25)
    Pk = k**ns * Tk**2
    # normalise to sigma_8
    ki = np.logspace(-4, 2, 8000)
    qi = ki/(Gamma*h0)
    Ti = np.log(1+2.34*qi)/(2.34*qi+1e-30) * \
         (1 + 3.89*qi + (16.1*qi)**2 + (5.46*qi)**3 + (6.71*qi)**4)**(-0.25)
    Pi = ki**ns * Ti**2
    R8 = 8.0
    Wk = 3*(np.sin(ki*R8)-ki*R8*np.cos(ki*R8))/(ki*R8)**3
    s2 = np.trapezoid(Pi*Wk**2*ki**2, ki)/(2*np.pi**2)
    norm = sig8**2 / s2
    Dz = growth(z)/growth(0)
    return norm * Pk * Dz**2

# ============================================================
# Photoionisation rate Gamma_HI(z)   [s^-1]
# Calibrated so that <tau_eff> matches Fan+2006 / Becker+2015
# ============================================================
_Gamma_nodes_z    = [4.5,  5.0,  5.2,  5.4,  5.6,  5.8,  6.0,  6.2,  6.5,  7.0]
_Gamma_nodes_logG = [-11.8,-12.0,-12.1,-12.3,-12.5,-12.8,-13.1,-13.5,-14.0,-15.0]
_Gamma_interp = interpolate.interp1d(_Gamma_nodes_z, _Gamma_nodes_logG,
                                     kind='linear', fill_value='extrapolate')

def Gamma_HI(z):
    return 10**float(_Gamma_interp(z))

# ============================================================
# Temperature–density relation  T = T0 * Delta^(gamma-1)
# ============================================================
def T0_gamma(z):
    """Return (T0 [K], gamma) at redshift z, calibrated to post-reionisation IGM."""
    # Near reionization gamma → 1; asymptotes to ~1.6 at low z
    # T0 peaks ~15 000 K right after reionization, cools adiabatically
    T0 = 8000 + 7000*np.exp(-((z-6.0)/1.5)**2)
    gamma = 1.0 + 0.5*(1 - np.exp(-(6.5-z)/1.5))
    gamma = np.clip(gamma, 1.0, 1.62)
    return float(T0), float(gamma)

def temperature(delta, z):
    T0, gam = T0_gamma(z)
    return T0 * np.clip(delta, 1e-3, None)**(gam-1)

# ============================================================
# Lognormal 1-D density field
# ============================================================
def lognormal_density(N, L, z, rng):
    """Return overdensity Delta = rho/rho_bar along a 1-D sightline."""
    dx = L/N
    k = 2*np.pi*fftpack.fftfreq(N, d=dx)
    ka = np.abs(k); ka[0] = 1e-10
    Pk = P1d_matter(ka, z)
    # Jeans filtering: suppress below ~200 ckpc/h
    kJ = 2*np.pi / 0.2   # h/Mpc  (~200 ckpc/h)
    Pk *= np.exp(-(ka/kJ)**2)
    amp = np.sqrt(Pk * dx / (2*L))
    phase = rng.uniform(0, 2*np.pi, N)
    dk = amp * np.exp(1j*phase)
    dk[0] = 0
    # enforce reality
    if N%2 == 0: dk[N//2] = abs(dk[N//2])
    for i in range(1, N//2): dk[N-i] = dk[i].conj()
    dg = np.real(fftpack.ifft(dk))*N
    sig2 = np.var(dg)
    Delta = np.exp(dg - sig2/2)
    Delta /= Delta.mean()
    return Delta

# ============================================================
# UV-background fluctuations (large-scale modulation of Gamma)
# ============================================================
def uv_fluctuation_field(N, L, z, rng):
    """Multiplicative factor for Gamma_HI along sightline (>0, mean~1)."""
    dx = L/N
    k = 2*np.pi*fftpack.fftfreq(N, d=dx)
    ka = np.abs(k); ka[0] = 1e-10
    # correlation length ~ mean free path
    lmfp = 55.0 - 4.0*(z-5.0)          # h^-1 Mpc, rough
    lmfp = np.clip(lmfp, 15, 60)
    sig_G = 0.15 + 0.25*np.clip(z-5.0, 0, 2)   # modest fluctuations
    Pk = sig_G**2 * lmfp * np.exp(-ka*lmfp)
    amp = np.sqrt(np.abs(Pk*dx/(2*L)))
    phase = rng.uniform(0, 2*np.pi, N)
    dk = amp*np.exp(1j*phase); dk[0]=0
    if N%2==0: dk[N//2]=abs(dk[N//2])
    for i in range(1,N//2): dk[N-i]=dk[i].conj()
    dg = np.real(fftpack.ifft(dk))*N
    return np.exp(dg - np.var(dg)/2)   # lognormal, mean≈1

# ============================================================
# Gunn-Peterson optical depth (pixel-level)
# ============================================================
def gp_tau_pixel(Delta, T, z, Gamma=None):
    """Compute GP optical depth per pixel in FGPA."""
    if Gamma is None: Gamma = Gamma_HI(z)
    nH = n_H_mean(z)
    # recombination coefficient  alpha_A ≈ 4.2e-13 (T/1e4)^-0.7
    alpha = 4.2e-13 * (T/1e4)**(-0.7)
    # neutral fraction in ionisation equilibrium
    x_HI = alpha * nH * Delta / Gamma
    n_HI = x_HI * nH * Delta
    # cross-section factor
    sig_a = np.pi * e_esu**2 * f_alpha / (me * c_cgs)
    Hzs = Hz(z)*1e5/3.086e24   # s^-1
    return sig_a * n_HI * lam_alpha / Hzs

# ============================================================
# Full synthetic spectrum
# ============================================================
def make_spectrum(z, L=40.0, N=4096, seed=0, noise_rms=0.01,
                  R_inst=2000, uv_fluct=True, rescale_tau=None):
    """
    Generate one synthetic Lya absorption spectrum.
    Returns dict with flux, velocity, tau, delta arrays.
    """
    rng = np.random.default_rng(seed)
    Delta = lognormal_density(N, L, z, rng)
    T = temperature(Delta, z)
    tau = gp_tau_pixel(Delta, T, z)

    # UV-background spatial fluctuations
    if uv_fluct:
        G_field = uv_fluctuation_field(N, L, z, rng)
        tau = tau / G_field

    # optional global rescaling (calibration knob)
    if rescale_tau is not None:
        tau *= rescale_tau

    # velocity axis
    dv = comoving_to_velocity(L/N, z)   # km/s per pixel
    vel = np.arange(N)*dv

    # thermal broadening kernel (Gaussian in velocity)
    T0, _ = T0_gamma(z)
    b_th = np.sqrt(2*kB*T0/mp)*1e-5   # km/s
    sig_th_pix = b_th / dv
    if sig_th_pix > 0.3:
        tau = gaussian_filter1d(tau, sig_th_pix, mode='wrap')

    # instrumental smoothing  (R = lam/dlam → dv = c/R)
    dv_inst = c_kms / R_inst
    sig_inst_pix = dv_inst / (2.355*dv)
    if sig_inst_pix > 0.3:
        flux = gaussian_filter1d(np.exp(-tau), sig_inst_pix, mode='wrap')
    else:
        flux = np.exp(-tau)

    flux = np.clip(flux, 0, None)
    if noise_rms > 0:
        flux += rng.normal(0, noise_rms, N)

    return dict(flux=flux, vel=vel, tau=tau, delta=Delta, dv=dv, z=z)

# ============================================================
# Calibrate rescale_tau so <tau_eff> matches observations
# ============================================================
# Target tau_eff from Fan+2006, Becker+2015
_target_tau = {5.2: 2.0, 5.4: 2.5, 5.6: 3.2, 5.8: 4.0, 6.0: 5.5}

def calibrate(z, Nlos=200, L=40.0, N=2048):
    """Find rescale factor so mean tau_eff matches observations."""
    target_z = min(_target_tau, key=lambda zz: abs(zz-z))
    tau_target = _target_tau[target_z]
    # measure raw <tau_eff>
    fluxes = []
    for i in range(Nlos):
        s = make_spectrum(z, L=L, N=N, seed=i, noise_rms=0, R_inst=50000, rescale_tau=1.0)
        fluxes.append(np.mean(s['flux']))
    mf = np.mean(fluxes)
    tau_raw = -np.log(max(mf, 1e-15))
    return tau_target / max(tau_raw, 0.01)

# ============================================================
# Statistical analyses
# ============================================================
def flux_pdf(spectra_list):
    """CDF of effective optical depth over 40 h^-1 Mpc skewers."""
    taus = []
    for s in spectra_list:
        mf = np.mean(s['flux'])
        taus.append(-np.log(max(mf, 1e-15)))
    taus = np.array(taus)
    t_grid = np.linspace(0, 10, 200)
    cdf = np.array([np.mean(taus > t) for t in t_grid])
    return t_grid, cdf, taus

def find_dark_gaps(flux, vel, tau_min=2.5):
    """Return list of gap lengths [h^-1 Mpc]."""
    thresh = np.exp(-tau_min)
    dark = flux < thresh
    gaps = []
    in_gap = False
    for i in range(len(dark)):
        if dark[i] and not in_gap:
            in_gap = True; start = i
        elif (not dark[i]) and in_gap:
            in_gap = False
            dv_gap = vel[i] - vel[start]
            gaps.append(dv_gap)
    if in_gap:
        gaps.append(vel[-1] - vel[start])
    # convert km/s → h^-1 cMpc at effective z
    z_eff = 5.7  # representative
    factor = (1+z_eff) / Hz(z_eff) * h0   # (km/s) → h^-1 Mpc
    return [g*factor for g in gaps if g > 0]

def gap_distribution(gaps, bins=None):
    """Compute L_g dP/dL_g."""
    if bins is None:
        bins = np.logspace(np.log10(0.5), np.log10(45), 18)
    if len(gaps) == 0:
        return 0.5*(bins[:-1]+bins[1:]), np.zeros(len(bins)-1)
    Ntot = len(gaps)
    g = np.array(gaps)
    Lc = np.sqrt(bins[:-1]*bins[1:])
    dP = np.zeros(len(Lc))
    for i in range(len(bins)-1):
        cnt = np.sum((g>=bins[i]) & (g<bins[i+1]))
        dL = bins[i+1]-bins[i]
        dP[i] = cnt/(Ntot*dL)
    return Lc, Lc*dP

def find_peaks(flux, vel, alpha=0.5, noise_rms=0.01):
    """Find transmission peaks; return list of (height, width_kms)."""
    fs = gaussian_filter1d(flux, 3)
    min_h = 3*noise_rms
    peaks = []
    for i in range(2, len(fs)-2):
        if fs[i]>fs[i-1] and fs[i]>fs[i+1] and fs[i]>min_h:
            hp = fs[i]; thr = alpha*hp
            left = i
            while left>0 and fs[left]>thr: left -= 1
            right = i
            while right<len(fs)-1 and fs[right]>thr: right += 1
            wp = vel[min(right, len(vel)-1)] - vel[max(left,0)]
            if wp > 0:
                peaks.append((hp, wp))
    # de-duplicate overlapping peaks: keep tallest per region
    if len(peaks) <= 1:
        return peaks
    peaks.sort(key=lambda p: -p[0])
    filtered = [peaks[0]]
    for p in peaks[1:]:
        overlap = False
        for fp in filtered:
            if abs(p[0]-fp[0])<0.01 and abs(p[1]-fp[1])<50:
                overlap = True; break
        if not overlap:
            filtered.append(p)
    return filtered

# ============================================================
# Reionisation history model (consistent with CROC)
# ============================================================
def reionisation_history(z_arr):
    z_re = 7.0; dz = 1.5
    x_HII_v = 0.5*(1+np.tanh((z_re - z_arr)/dz))
    x_HII_m = 0.5*(1+np.tanh((7.5 - z_arr)/(dz*1.2)))
    return dict(z=z_arr, xHII_v=np.clip(x_HII_v,0,1),
                xHII_m=np.clip(x_HII_m,0,1))

# ============================================================
# DC mode test
# ============================================================
def dc_mode_test(z=5.7, Nreal=30):
    results = []
    for i in range(Nreal):
        s = make_spectrum(z, L=20.0, N=2048, seed=1000+i*7,
                          noise_rms=0, R_inst=50000)
        mf = np.mean(s['flux'])
        tau_eff = -np.log(max(mf, 1e-15))
        md = np.mean(s['delta']) - 1
        results.append((md, tau_eff))
    return np.array(results)

# ============================================================
# MAIN
# ============================================================
def run_analysis():
    print("="*70)
    print("REPLICATION: Gnedin, Becker & Fan (2017) – OSTI 1275503")
    print("Cosmic Reionization On Computers: Post-Reionization IGM")
    print("="*70)

    R = {}   # results dict

    # --- 1. calibrate tau rescaling per redshift bin ---
    print("\n[1/7] Calibrating optical depth normalisation …")
    z_mids = [5.2, 5.4, 5.6, 5.8, 6.0]
    rescale = {}
    for zm in z_mids:
        sc = calibrate(zm, Nlos=150)
        rescale[zm] = sc
        print(f"  z={zm:.1f}  rescale = {sc:.3f}")
    R['rescale'] = {str(k): v for k,v in rescale.items()}

    # --- 2. T-rho relation ---
    print("\n[2/7] Temperature–density relation …")
    td = {}
    for z in [5.0, 5.5, 6.0]:
        T0, gam = T0_gamma(z)
        td[f"z={z}"] = dict(T0=round(T0), gamma=round(gam, 3))
        print(f"  z={z}: T0={T0:.0f} K, γ={gam:.3f}")
    R['T_delta'] = td

    # --- 3. reionisation history ---
    print("\n[3/7] Reionisation history …")
    zarr = np.linspace(5, 14, 200)
    rh = reionisation_history(zarr)
    R['reion'] = {k: v.tolist() if hasattr(v,'tolist') else v for k,v in rh.items()}

    # --- 4. Generate spectra & flux PDFs ---
    print("\n[4/7] Generating spectra & flux PDFs …")
    zbins = [(5.1,5.3),(5.3,5.5),(5.5,5.7),(5.7,5.9),(5.9,6.1)]
    Nlos = 500
    all_spectra = {}
    fpdf_results = {}
    for zlo, zhi in zbins:
        zm = (zlo+zhi)/2
        lab = f"{zlo:.1f}-{zhi:.1f}"
        sc = rescale.get(round(zm,1), rescale.get(min(rescale, key=lambda x: abs(x-zm))))
        specs = []
        for i in range(Nlos):
            s = make_spectrum(zm, seed=i*17+int(zm*1000), noise_rms=0.01,
                              R_inst=2000, rescale_tau=sc)
            specs.append(s)
        all_spectra[lab] = specs
        tg, cdf, taus = flux_pdf(specs)
        mt = np.mean(taus); st = np.std(taus)
        fpdf_results[lab] = dict(tau_grid=tg.tolist(), cdf=cdf.tolist(),
                                  mean_tau=round(float(mt),2), std_tau=round(float(st),2))
        print(f"  {lab}: <τ_eff> = {mt:.2f} ± {st:.2f}")
    R['flux_pdf'] = fpdf_results

    # --- 5. Dark gap statistics ---
    print("\n[5/7] Dark gap statistics …")
    gap_zbins = [(5.3,5.5),(5.5,5.7),(5.7,5.9),(5.9,6.1)]
    obs_Ngaps = {'5.3-5.5':86, '5.5-5.7':77, '5.7-5.9':46, '5.9-6.1':22}
    gap_results = {}
    for zlo, zhi in gap_zbins:
        lab = f"{zlo:.1f}-{zhi:.1f}"
        specs = all_spectra.get(lab, [])
        if not specs:
            zm = (zlo+zhi)/2; sc = rescale.get(round(zm,1), 1.0)
            specs = [make_spectrum(zm, seed=i*17+int(zm*1000), noise_rms=0.01,
                                   R_inst=2000, rescale_tau=sc) for i in range(Nlos)]
        grz = {}
        for tmin in [2.5, 3.0, 3.5]:
            allg = []
            for s in specs:
                allg.extend(find_dark_gaps(s['flux'], s['vel'], tau_min=tmin))
            Lc, LdP = gap_distribution(allg)
            grz[f"tau_min={tmin}"] = dict(Lc=Lc.tolist(), LdP=LdP.tolist(),
                                          Ngaps=len(allg),
                                          mean_L=round(float(np.mean(allg)),1) if allg else 0)
            if tmin == 2.5:
                print(f"  {lab} τ_min=2.5: {len(allg)} gaps, "
                      f"<L>={np.mean(allg):.1f}" if allg else f"  {lab}: 0 gaps")
        grz['obs_Ngaps'] = obs_Ngaps.get(lab, 0)
        gap_results[lab] = grz
    R['gaps'] = gap_results

    # --- 6. Peak statistics ---
    print("\n[6/7] Transmission peak statistics …")
    peak_zbins = [(5.25,5.75),(5.75,6.25)]
    peak_results = {}
    for zlo, zhi in peak_zbins:
        zm = (zlo+zhi)/2; lab = f"{zlo:.2f}-{zhi:.2f}"
        sc = rescale.get(round(zm,1), rescale.get(min(rescale, key=lambda x: abs(x-zm))))
        all_peaks = []
        for i in range(Nlos):
            s = make_spectrum(zm, seed=i*17+int(zm*1000), noise_rms=0.01,
                              R_inst=2000, rescale_tau=sc)
            pks = find_peaks(s['flux'], s['vel'], noise_rms=0.01)
            all_peaks.extend(pks)
        heights = [p[0] for p in all_peaks]
        widths  = [p[1] for p in all_peaks]
        peak_results[lab] = dict(
            Npeaks=len(all_peaks),
            mean_h=round(float(np.mean(heights)),4) if heights else 0,
            median_h=round(float(np.median(heights)),4) if heights else 0,
            mean_w=round(float(np.mean(widths)),1) if widths else 0,
            median_w=round(float(np.median(widths)),1) if widths else 0,
        )
        print(f"  {lab}: {len(all_peaks)} peaks  <h>={np.mean(heights):.3f}  <w>={np.mean(widths):.0f} km/s" if heights else f"  {lab}: 0 peaks")
    R['peaks'] = peak_results

    # --- 7. DC mode test ---
    print("\n[7/7] DC mode test (z=5.7) …")
    dc = dc_mode_test(5.7, 30)
    corr = np.corrcoef(dc[:,0], dc[:,1])[0,1]
    R['dc_mode'] = dict(delta=dc[:,0].tolist(), tau=dc[:,1].tolist(),
                        corr=round(float(corr),3) if np.isfinite(corr) else 0)
    print(f"  corr(δ, τ_eff) = {corr:.3f}" if np.isfinite(corr) else "  corr = N/A")

    # save
    with open(os.path.join(OUTDIR, 'analysis_results.json'), 'w') as f:
        json.dump(R, f, indent=2, default=lambda o: float(o) if isinstance(o, (np.floating, np.integer)) else None)
    print("\n  Saved analysis_results.json")
    return R

# ============================================================
# PLOTTING
# ============================================================
def make_plots(R=None):
    import matplotlib; matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib import rcParams
    rcParams.update({'font.size':12, 'axes.labelsize':14, 'legend.fontsize':10})
    fdir = os.path.join(OUTDIR, 'figures')

    if R is None:
        with open(os.path.join(OUTDIR,'analysis_results.json')) as f: R = json.load(f)

    # ---- Fig 1: flux PDFs ----
    print("  Fig 1: flux PDFs …")
    fig, axes = plt.subplots(2,3, figsize=(15,10))
    axes = axes.flat
    colours = ['#1f77b4','#ff7f0e','#2ca02c','#d62728','#9467bd']
    labels = ['5.1-5.3','5.3-5.5','5.5-5.7','5.7-5.9','5.9-6.1']
    for i, lab in enumerate(labels):
        ax = axes[i]; d = R['flux_pdf'][lab]
        t = np.array(d['tau_grid']); c = np.array(d['cdf'])
        ax.semilogy(t, c, colours[i], lw=2)
        ax.axvline(d['mean_tau'], color=colours[i], ls='--', alpha=.5)
        ax.set_title(f"z = {lab}"); ax.set_xlabel(r'$\langle\tau\rangle_{40}$')
        ax.set_ylabel(r'$P(>\langle\tau\rangle_{40})$')
        ax.set_xlim(0,8); ax.set_ylim(1e-3,1.1); ax.grid(alpha=.3)
    axes[5].axis('off')
    fig.suptitle('Fig 1 — Cumulative Optical Depth Distribution (cf. GBF17 Fig 1)', fontsize=14)
    plt.tight_layout(); plt.savefig(f'{fdir}/fig1_flux_pdf.png', dpi=150, bbox_inches='tight'); plt.close()

    # ---- Fig 2: gap distributions ----
    print("  Fig 2: dark gaps …")
    fig, axes = plt.subplots(2,2, figsize=(12,10)); axes = axes.flat
    for i, lab in enumerate(['5.3-5.5','5.5-5.7','5.7-5.9','5.9-6.1']):
        ax = axes[i]; gd = R['gaps'][lab]
        for tm, ls, col in [('tau_min=2.5','-','b'),('tau_min=3.0','--','g'),('tau_min=3.5',':','r')]:
            d = gd[tm]; Lc = np.array(d['Lc']); LdP = np.array(d['LdP'])
            m = LdP>0
            if m.any():
                ax.loglog(Lc[m], LdP[m], ls, color=col, lw=2, label=f"{tm} (N={d['Ngaps']})")
        ax.set_title(f"z = {lab}  [obs: {gd['obs_Ngaps']} gaps]")
        ax.set_xlabel(r'$L_g$ [h$^{-1}$ Mpc]'); ax.set_ylabel(r'$L_g\,dP/dL_g$')
        ax.set_xlim(.5,50); ax.set_ylim(1e-3,5); ax.legend(fontsize=8); ax.grid(alpha=.3)
    fig.suptitle('Fig 2 — Dark Gap Distribution (cf. GBF17 Fig 2)', fontsize=14)
    plt.tight_layout(); plt.savefig(f'{fdir}/fig2_dark_gaps.png', dpi=150, bbox_inches='tight'); plt.close()

    # ---- Fig 3: gaps vs tau_min at z=5.7-5.9 ----
    print("  Fig 3: gaps vs τ_min …")
    fig, ax = plt.subplots(figsize=(8,6))
    gd = R['gaps']['5.7-5.9']
    for tm, ls, col in [('tau_min=2.5','-','b'),('tau_min=3.0','--','g'),('tau_min=3.5',':','r')]:
        d = gd[tm]; Lc = np.array(d['Lc']); LdP = np.array(d['LdP'])
        m = LdP>0
        if m.any(): ax.loglog(Lc[m], LdP[m], ls, color=col, lw=2, label=r'$\tau_{\min}=$'+tm.split('=')[1])
    ax.set_xlabel(r'$L_g$ [h$^{-1}$ Mpc]'); ax.set_ylabel(r'$L_g\,dP/dL_g$')
    ax.set_title('Fig 3 — Gap distribution at z=5.7–5.9 (cf. GBF17 Fig 3)')
    ax.legend(); ax.grid(alpha=.3); plt.tight_layout()
    plt.savefig(f'{fdir}/fig3_gap_taumin.png', dpi=150, bbox_inches='tight'); plt.close()

    # ---- Fig 6 left: reionisation history ----
    print("  Fig 6L: reionisation history …")
    fig, ax = plt.subplots(figsize=(8,6))
    z = np.array(R['reion']['z'])
    xv = np.array(R['reion']['xHII_v']); xm = np.array(R['reion']['xHII_m'])
    ax.semilogy(z, 1-xv, 'b-', lw=2, label=r'$\langle x_{\rm HI}\rangle_V$')
    ax.semilogy(z, 1-xm, 'b--', lw=2, label=r'$\langle x_{\rm HI}\rangle_M$')
    ax.semilogy(z, xv, 'r-', lw=2, label=r'$\langle x_{\rm HII}\rangle_V$')
    ax.semilogy(z, xm, 'r--', lw=2, label=r'$\langle x_{\rm HII}\rangle_M$')
    ax.set_xlabel('Redshift $z$'); ax.set_ylabel('Ionisation fraction')
    ax.set_xlim(5,14); ax.set_ylim(1e-4,2); ax.legend(); ax.grid(alpha=.3)
    ax.set_title('Fig 6L — Reionisation History (cf. GBF17 Fig 6 left)')
    plt.tight_layout(); plt.savefig(f'{fdir}/fig6_reion.png', dpi=150, bbox_inches='tight'); plt.close()

    # ---- Fig 6 right: DC mode ----
    print("  Fig 6R: DC mode test …")
    fig, ax = plt.subplots(figsize=(8,6))
    dc = R['dc_mode']
    d = np.array(dc['delta']); t = np.array(dc['tau'])
    ax.scatter(d, t, c='steelblue', s=50, edgecolors='k', zorder=3)
    finite = np.isfinite(d) & np.isfinite(t)
    if finite.sum()>2:
        try:
            p = np.polyfit(d[finite], t[finite], 1)
            xf = np.linspace(d[finite].min(), d[finite].max(), 50)
            ax.plot(xf, np.polyval(p, xf), 'r--', lw=1.5, label=f'r={dc["corr"]:.2f}')
            ax.legend()
        except Exception:
            pass
    ax.set_xlabel(r'Mean overdensity $\delta$'); ax.set_ylabel(r'$\tau_{\rm eff}$')
    ax.set_title('Fig 6R — DC Mode Test, z=5.7 (cf. GBF17 Fig 6 right)')
    ax.grid(alpha=.3); plt.tight_layout()
    plt.savefig(f'{fdir}/fig6_dc_mode.png', dpi=150, bbox_inches='tight'); plt.close()

    # ---- Extra: T–Δ relation ----
    print("  Extra: T–Δ …")
    fig, ax = plt.subplots(figsize=(8,6))
    dd = np.logspace(-1,2,200)
    for zv, col, ls in [(5.0,'b','-'),(5.5,'g','--'),(6.0,'r',':')]:
        ax.loglog(dd, temperature(dd, zv), ls, color=col, lw=2, label=f'z={zv}')
    ax.set_xlabel(r'$\Delta$'); ax.set_ylabel(r'$T$ [K]')
    ax.set_xlim(.1,100); ax.set_ylim(1e3,1e6)
    ax.set_title(r'Temperature–Density Relation  $T = T_0\,\Delta^{\gamma-1}$')
    ax.legend(); ax.grid(alpha=.3); plt.tight_layout()
    plt.savefig(f'{fdir}/extra_T_delta.png', dpi=150, bbox_inches='tight'); plt.close()

    # ---- Extra: sample spectra ----
    print("  Extra: sample spectra …")
    fig, axes = plt.subplots(3,1, figsize=(14,10))
    for ax, zv in zip(axes, [5.2, 5.7, 6.0]):
        sc = 1.0
        for k in sorted(R.get('rescale',{}).keys(), key=lambda x: abs(float(x)-zv)):
            sc = R['rescale'][k]; break
        s = make_spectrum(zv, seed=42, noise_rms=0.01, R_inst=2000, rescale_tau=sc)
        ax.plot(s['vel'], s['flux'], 'k-', lw=.5, alpha=.8)
        ax.axhline(0, color='gray', alpha=.3)
        ax.axhline(np.exp(-2.5), color='red', ls='--', alpha=.5, label=r'$F=e^{-2.5}$')
        ax.set_ylabel('Flux'); ax.set_title(f'z = {zv}'); ax.legend(loc='upper right')
        ax.set_ylim(-.05, max(.3, np.percentile(s['flux'],99.5)+.05)); ax.grid(alpha=.3)
    axes[-1].set_xlabel('Velocity [km/s]')
    fig.suptitle('Sample Synthetic Lyα Spectra (40 h⁻¹ Mpc)', fontsize=14)
    plt.tight_layout(); plt.savefig(f'{fdir}/extra_spectra.png', dpi=150, bbox_inches='tight'); plt.close()

    print(f"  All figures → {fdir}/")

# ============================================================
if __name__ == '__main__':
    R = run_analysis()
    print("\nGenerating plots …")
    make_plots(R)
    print("\nDONE ✓")
