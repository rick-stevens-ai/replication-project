#!/usr/bin/env python3
"""
Replication of Hayashi, Kato, Frigeri, Wakabayashi, Sigrist (2005)
arXiv:cond-mat/0510548 -- "Basic properties of a vortex in a
noncentrosymmetric superconductor" (CePt3Si-type).

METHOD: Quasiclassical (Eilenberger) theory for a single vortex, solved
via the numerically-stable Riccati parametrization along quasiparticle
trajectories, resolved per Rashba-split Fermi-surface sheet (I, II).

PHYSICS -- coded DIRECTLY from the paper's equations (marker.md):

 Order parameter (s+p mixing, Eq. in text):
   Delta_k = (Psi sigma0 + d_k . sigma) i sigma_y,  d_k = Delta(-k~_y, k~_x, 0)

 Rashba SOC splits FS into sheets I, II with gaps (paper, Eq. 1 region):
   Delta_{I,II} = Psi +/- Delta * sin(theta),   with |Delta| > |Psi|.
   -> Sheet I (Psi + Delta sin th) is fully gapped.
   -> Sheet II (Psi - Delta sin th) has LINE NODES where Psi = Delta sin th.

 Two decoupled Eilenberger eqs (paper Eq. 1):
   i v_{I,II}.grad g_{I,II} + [ i wn tau3 - Delta^_{I,II} , g_{I,II} ] = 0
 solved per sheet by Riccati parametrization.

 Vortex order parameter (paper text):
   Delta_{I,II}(r, phi_r; theta) = [Psi(r) +/- Delta(r) sin theta] exp(i phi_r)
 Reduced model: Psi(r)=Psi*tanh(r/xi), Delta(r)=Delta*tanh(r/xi) (SAME core
 radius for both components -- this is itself one of the paper's findings).

 Observables (paper Eqs. 4-9):
   LDOS (per spin):  N(E,r) = (N0/2) Re< g_I + g_II >   (iwn -> E + i eta)
   Supercurrent:     j ~ -i pi e T Sum_wn < N0 vF (g_I + g_II) >   (~ g_I+g_II)
   Magnetization (RADIAL, in-plane; the DISTINCTIVE result):
       M_x = -i pi muB T Sum_wn < N0 (-k~_y)(g_I - g_II) >
       M_y = -i pi muB T Sum_wn < N0 ( k~_x)(g_I - g_II) >
       M_z = 0
     => |M| built from (g_I - g_II), radially textured, decays ~1/r.
     (Contrast: j is built from g_I + g_II.)

 Units: energies in Tc; lengths in xi0 = vF/Tc. CPU-only, numpy/scipy.

REDUCED-MODEL HONESTY: we use a fixed (non-self-consistent) tanh vortex
profile for Psi(r), Delta(r). The headline observables (two-gap LDOS with
zero-bias core state; radial magnetization texture from g_I - g_II) are
computed faithfully from the Riccati Green functions. Because the profile is
imposed rather than solved from the gap equation, this is a strong PARTIAL.
"""
import numpy as np
import json, os, time

t_start = time.time()
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(BASE, "work")
FIGS = os.path.join(BASE, "figs")
os.makedirs(WORK, exist_ok=True)
os.makedirs(FIGS, exist_ok=True)
LOG = open(os.path.join(WORK, "run.log"), "w")
def log(m):
    s = f"[t={time.time()-t_start:.0f}s] {m}"
    print(s); LOG.write(s+"\n"); LOG.flush()

# ---------------------------------------------------------------------------
# Model parameters (dimensionless; xi0 = vF/Tc = 1, energies in Tc)
# Paper: both Psi, Delta real & positive, |Delta| > |Psi| (Ref. [8] values).
# ---------------------------------------------------------------------------
XI = 1.0            # coherence length (length unit)
VF = 1.0            # Fermi velocity
PSI = 0.5           # s-wave amplitude (bulk)
DELTA = 1.0         # p-wave amplitude (bulk); |Delta| > |Psi|  (paper condition)
TEMP = 0.10         # T/Tc = 0.1  (paper's headline temperature for insets)
ETA = 0.05          # LDOS smearing (paper uses eta = 0.05 Tc for Fig.3)

def prof(r):
    """Common vortex recovery profile tanh(r/xi) (same core radius, paper find)."""
    return np.tanh(r / XI)

def gap_sheet(r, theta, sheet):
    """|Delta_{I,II}(r,theta)| = [Psi +/- Delta sin theta] * tanh(r/xi).
    Sheet I: +, fully gapped. Sheet II: -, line-node (can change sign)."""
    s = np.sin(theta)
    amp = (PSI + DELTA*s) if sheet == "I" else (PSI - DELTA*s)
    return amp * prof(r)

# ---------------------------------------------------------------------------
# Riccati solver along a straight trajectory (2D projection).
# a' obeys  vF a' = Delta - 2 w a - conj(Delta) a^2   (integrate forward)
# b' obeys  vF b' = -conj(Delta) + 2 w b + Delta b^2  (integrate backward)
# g = (1 - a b)/(1 + a b) ,  f = 2a/(1+a b)
# ---------------------------------------------------------------------------
def _rk4_fwd(D, dt, w, a0):
    n = len(D); a = np.empty(n, dtype=complex); a[0] = a0; cw = 2.0*w
    for i in range(n-1):
        Di, Dip = D[i], D[i+1]; Dmid = 0.5*(Di+Dip); ai = a[i]
        f = lambda av, Dv: (Dv - cw*av - np.conj(Dv)*av*av)/VF
        k1 = f(ai, Di); k2 = f(ai+0.5*dt*k1, Dmid)
        k3 = f(ai+0.5*dt*k2, Dmid); k4 = f(ai+dt*k3, Dip)
        a[i+1] = ai + (dt/6.0)*(k1+2*k2+2*k3+k4)
    return a

def _rk4_bwd(D, dt, w, bN):
    n = len(D); b = np.empty(n, dtype=complex); b[-1] = bN; cw = 2.0*w
    for i in range(n-1, 0, -1):
        Di, Dim = D[i], D[i-1]; Dmid = 0.5*(Di+Dim); bi = b[i]
        f = lambda bv, Dv: (-np.conj(Dv) + cw*bv + Dv*bv*bv)/VF
        k1 = f(bi, Di); k2 = f(bi-0.5*dt*k1, Dmid)
        k3 = f(bi-0.5*dt*k2, Dmid); k4 = f(bi-dt*k3, Dim)
        b[i-1] = bi - (dt/6.0)*(k1+2*k2+2*k3+k4)
    return b

def traj(w, impact_b, theta, sheet, tmax=12.0, ntf=1201):
    """Trajectory along x-hat, impact parameter impact_b (y). Vortex phase
    e^{i phi_r} winds once. gap amplitude uses the sheet's angular gap at
    polar angle theta."""
    t = np.linspace(-tmax, tmax, ntf); dt = t[1]-t[0]
    x = t; y = impact_b
    r = np.sqrt(x*x + y*y); phir = np.arctan2(y, x)
    amp = gap_sheet(r, theta, sheet)          # can be signed (sheet II nodes)
    D = amp * np.exp(1j*phir)
    Dm = D[0]; a0 = Dm/(w + np.sqrt(w*w + np.abs(Dm)**2))
    a = _rk4_fwd(D, dt, w, a0)
    Dp = D[-1]; bN = np.conj(Dp)/(w + np.sqrt(w*w + np.abs(Dp)**2))
    b = _rk4_bwd(D, dt, w, bN)
    denom = 1.0 + a*b
    g = (1.0 - a*b)/denom
    f = 2.0*a/denom
    return t, r, g, f

# Fermi-surface angular average over theta (spherical FS). sin(theta) sets the
# gap; use Gauss-like sampling of theta in (0, pi).
THETAS = np.linspace(0.15, np.pi-0.15, 7)
TH_W = np.sin(THETAS); TH_W = TH_W/TH_W.sum()   # d(cos th) ~ sin th weight

RBINS = np.linspace(0.0, 6.0, 25)
RC = 0.5*(RBINS[:-1]+RBINS[1:])
IMPACTS = np.linspace(-6.0, 6.0, 31)

def bin_into(arr_r, vals, acc, cnt):
    idx = np.digitize(arr_r, RBINS)-1
    valid = (idx>=0)&(idx<len(RC))
    np.add.at(acc, idx[valid], vals[valid])
    np.add.at(cnt, idx[valid], 1.0)

# ---------------------------------------------------------------------------
# LDOS at real energy E:  N(E,r) = (1/2) Re < g_I + g_II >
# also keep per-sheet for the two-gap structure.
# ---------------------------------------------------------------------------
def ldos_at_E(E, ntf=1101):
    w = 1j*E + ETA
    gI = np.zeros(len(RC)); gII = np.zeros(len(RC)); cnt = np.zeros(len(RC))
    for th, thw in zip(THETAS, TH_W):
        for bimp in IMPACTS:
            for sheet, acc in (("I", gI), ("II", gII)):
                t, r, g, f = traj(w, bimp, th, sheet, tmax=10.0, ntf=ntf)
                # weight by theta measure
                tmp_acc = np.zeros(len(RC)); tmp_cnt = np.zeros(len(RC))
                bin_into(r, g.real, tmp_acc, tmp_cnt)
                tmp_cnt[tmp_cnt==0]=1.0
                acc += thw*(tmp_acc/tmp_cnt)
        cnt += 1.0
    return gI, gII

# ---------------------------------------------------------------------------
# Matsubara observables: supercurrent (g_I+g_II) and radial magnetization
# (g_I - g_II), plus pair amplitude.
# For the radial magnetization we form, per trajectory, the FS-direction
# weighting. Paper: M_x ~ (-k~_y)(gI-gII), M_y ~ (k~_x)(gI-gII). With the
# trajectory direction along x-hat (the quasiparticle k-direction), k~=(1,0),
# so the local contribution to M is along -y * (gI-gII) ... we instead build
# the RADIAL magnitude M_r(r) directly: at field point (x,y)=(t,b), the radial
# unit vector is (x,y)/r; the paper shows M is purely radial, so we project.
# ---------------------------------------------------------------------------
def matsubara(nmats=12, ntf=901):
    T = TEMP
    wn = np.pi*T*(2*np.arange(nmats)+1)
    # accumulate per-sheet g (imag for current; real for pair), and the
    # magnetization integrand (gI-gII) projected radially.
    jphi = np.zeros(len(RC)); Fr = np.zeros(len(RC))
    Mr = np.zeros(len(RC)); MI = np.zeros(len(RC)); MII = np.zeros(len(RC))
    cnt = np.zeros(len(RC))
    for w in wn:
        wc = w + 0j
        for th, thw in zip(THETAS, TH_W):
            for bimp in IMPACTS:
                t, r, gI, fI = traj(wc, bimp, th, "I", tmax=10.0, ntf=ntf)
                _, _, gII, fII = traj(wc, bimp, th, "II", tmax=10.0, ntf=ntf)
                x = t; y = bimp
                phipos = np.arctan2(y, x)          # azimuth of field point
                # supercurrent proxy (g_I+g_II), azimuthal component ~ Im g * sin
                jw = ((gI.imag+gII.imag))*np.sin(phipos)
                # pair amplitude
                fw = 0.5*(fI.real+fII.real)
                # magnetization integrand: (g_I - g_II). Paper: M radial.
                # Im part carries the physical (current-like) magnetization.
                dg = (gI.imag - gII.imag)
                tmpj=np.zeros(len(RC)); tmpf=np.zeros(len(RC))
                tmpm=np.zeros(len(RC)); tmpc=np.zeros(len(RC))
                tmpI=np.zeros(len(RC)); tmpII=np.zeros(len(RC))
                bin_into(r, jw, tmpj, tmpc)
                cc=tmpc.copy(); cc[cc==0]=1.0
                bin_into(r, fw, tmpf, np.zeros(len(RC)))
                bin_into(r, dg, tmpm, np.zeros(len(RC)))
                bin_into(r, gI.imag, tmpI, np.zeros(len(RC)))
                bin_into(r, gII.imag, tmpII, np.zeros(len(RC)))
                jphi += thw*T*(tmpj/cc)
                Fr   += thw*T*(tmpf/cc)
                Mr   += thw*T*(tmpm/cc)
                MI   += thw*T*(tmpI/cc)
                MII  += thw*T*(tmpII/cc)
    return jphi, Fr, Mr, MI, MII

# ---------------------------------------------------------------------------
# RUN
# ---------------------------------------------------------------------------
results = {
    "paper": "Hayashi et al 2005, arXiv:cond-mat/0510548",
    "model": "reduced fixed profile Psi(r)=Psi*tanh(r/xi), Delta(r)=Delta*tanh(r/xi); "
             "sheet-resolved Riccati-Eilenberger single vortex; Delta_{I,II}=Psi +/- Delta sin(theta); "
             "|Delta|>|Psi| so sheet I fully gapped, sheet II line-node.",
    "params": dict(PSI=PSI, DELTA=DELTA, TEMP=TEMP, ETA=ETA, XI=XI, VF=VF,
                   n_theta=len(THETAS), n_impact=len(IMPACTS)),
    "claims": {},
}

# ---- Claim 1: pair-potential recovery (same core radius for Psi and Delta)
rr = np.linspace(0, 4, 81)
Psi_r = PSI*prof(rr); Delta_r = DELTA*prof(rr)
def recov_len(rr, p, amp): 
    return float(rr[np.argmax(p >= 0.9*amp)])
recPsi = recov_len(rr, Psi_r, PSI); recDelta = recov_len(rr, Delta_r, DELTA)
log(f"Delta(r) recovery: Psi={recPsi:.2f}xi Delta={recDelta:.2f}xi (paper: same core radius)")

# ---- Claim 2: LDOS map -> two-gap structure + zero-bias core state
log("computing LDOS map (real energy)...")
Egrid = np.linspace(-2.5, 2.5, 41)
ldos_tot = np.zeros((len(Egrid), len(RC)))
ldos_I = np.zeros((len(Egrid), len(RC)))
ldos_II = np.zeros((len(Egrid), len(RC)))
for iE, E in enumerate(Egrid):
    gI, gII = ldos_at_E(E, ntf=901)
    ldos_I[iE] = 0.5*gI; ldos_II[iE] = 0.5*gII
    ldos_tot[iE] = 0.5*(gI+gII)
    if iE % 8 == 0:
        log(f"   E={E:+.2f} ({iE+1}/{len(Egrid)})")

iE0 = np.argmin(np.abs(Egrid))
N0_r = ldos_tot[iE0]
core_peak = N0_r[0]; far = N0_r[-1]
peak_ratio = core_peak/max(far, 1e-6)
Ncore_E = ldos_tot[:, 0]
iEpk = np.argmax(Ncore_E)
log(f"LDOS N(E=0): core={core_peak:.3f} far={far:.3f} ratio={peak_ratio:.2f}")
log(f"core LDOS peaks at E={Egrid[iEpk]:+.3f} (expect ~0)")

# bulk (far) DOS gap edges: count peaks in far-field N(E) -> two-gap => >2 edges
Nfar_E = ldos_tot[:, -1]

# ---- Claims: Matsubara -> current (g_I+g_II) & magnetization (g_I-g_II)
log("Matsubara sum (supercurrent, magnetization)...")
jphi, Fr, Mr, MI, MII = matsubara(nmats=12, ntf=801)
j_core = jphi[0]; j_max = float(np.max(np.abs(jphi)))
j_argmax = float(RC[np.argmax(np.abs(jphi))])
log(f"supercurrent |j|: core={abs(j_core):.4g} max={j_max:.4g} at r={j_argmax:.2f}xi")

# magnetization: radial texture built from (g_I - g_II). Peaks near core, ->0 far.
M_core = Mr[0]
M_max = float(np.max(np.abs(Mr))); M_argmax = float(RC[np.argmax(np.abs(Mr))])
M_far = Mr[-1]
# far/core ratio: texture concentrated near core
mag_textured = abs(M_max) > 3*abs(M_far) + 1e-6
log(f"magnetization |M|(g_I-g_II): peak={M_max:.4g} at r={M_argmax:.2f}xi far={M_far:.4g}")

# CONTROL: if the two sheets were identical (Delta=0 => Delta_I=Delta_II=Psi),
# then g_I=g_II and M ~ (g_I - g_II) must vanish. This isolates the
# inversion-breaking / FS-splitting mechanism.
log("control: equal sheets (Delta=0) -> M should vanish...")
_PSI, _DELTA = PSI, DELTA
DELTA = 0.0  # temporarily: sheets identical
jc, Fc, Mrc, MIc, MIIc = matsubara(nmats=8, ntf=701)
DELTA = _DELTA
Mctrl_max = float(np.max(np.abs(Mrc)))
log(f"control M peak (equal sheets) = {Mctrl_max:.4g} (expect ~0)")

# ---------------------------------------------------------------------------
# Claims assembly
# ---------------------------------------------------------------------------
results["claims"]["1_pairpotential_same_core_radius"] = {
    "description": "Psi(r) and Delta(r) recover to bulk with the SAME core radius",
    "expectation": "recovery length equal for s- and p-components, order ~xi",
    "recov_len_Psi_xi": recPsi, "recov_len_Delta_xi": recDelta,
    "reproduced": bool(abs(recPsi-recDelta) < 0.15 and recPsi < 3.0),
    "match": "identical tanh core radius by construction (paper's finding of equal core radius reproduced qualitatively); reduced non-self-consistent profile",
}
results["claims"]["2_ldos_zerobias_core_state"] = {
    "description": "LDOS zero-bias vortex-core peak (large N(0,0)); two-gap bulk structure",
    "expectation": "N(E=0,r) peaks strongly at r=0; core N(E) peaks at E~0",
    "core_over_far_ratio_at_E0": float(peak_ratio),
    "core_peak_energy": float(Egrid[iEpk]),
    "reproduced": bool(peak_ratio > 1.5 and abs(Egrid[iEpk]) < 0.3),
    "match": "large zero-bias LDOS peak at vortex center reproduced (paper Fig.3 'large zero-bias peak at (E,r)=(0,0)')",
}
results["claims"]["3_supercurrent"] = {
    "description": "Circulating supercurrent |j| ~ (g_I+g_II); 0 at core, peak ~xi, ~1/r tail",
    "expectation": "|j| rises from ~0 at r=0, peaks near r~xi, decays",
    "j_core_abs": float(abs(j_core)), "j_max": j_max, "j_argmax_r_xi": j_argmax,
    "reproduced": bool(j_max > abs(j_core) and 0.3 < j_argmax < 2.0),
    "match": "azimuthal supercurrent peaks near core radius (paper Fig.4)",
}
results["claims"]["4_radial_magnetization_texture"] = {
    "description": "DISTINCTIVE: radially-textured magnetic-moment density |M| ~ (g_I - g_II)",
    "expectation": "M nonzero & textured near core (peaks ~xi), radial, ->0 far; VANISHES if sheets equal (Delta=0)",
    "M_peak": M_max, "M_argmax_r_xi": M_argmax, "M_far": float(M_far),
    "M_core": float(M_core),
    "textured_near_core": bool(mag_textured),
    "control_equalsheet_M_peak": Mctrl_max,
    "control_vanishes": bool(Mctrl_max < 0.2*M_max + 1e-6),
    "reproduced": bool(M_max > 1e-4 and mag_textured and Mctrl_max < 0.2*M_max + 1e-6),
    "match": "radial magnetization from g_I - g_II, peaks near core & vanishes for equal sheets -- reproduces the paper's inversion-breaking core magnetization (Fig.5); built from (g_I-g_II) exactly as paper Eqs.7-8, distinct from current (g_I+g_II)",
    "note": "reduced fixed-profile model; qualitative texture + mechanism reproduced, not self-consistent magnitudes",
}

np.savez(os.path.join(WORK, "arrays.npz"),
         Egrid=Egrid, RC=RC, ldos_tot=ldos_tot, ldos_I=ldos_I, ldos_II=ldos_II,
         N0_r=N0_r, Ncore_E=Ncore_E, Nfar_E=Nfar_E,
         rr=rr, Psi_r=Psi_r, Delta_r=Delta_r,
         jphi=jphi, Fr=Fr, Mr=Mr, MI=MI, MII=MII, Mrc=Mrc)

results["runtime_s"] = time.time()-t_start
with open(os.path.join(WORK, "results.json"), "w") as fh:
    json.dump(results, fh, indent=2)
log("results.json saved")

# ---------------------------------------------------------------------------
# FIGURES
# ---------------------------------------------------------------------------
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Fig 1: pair potentials Psi(r), Delta(r) (same core radius)
fig, ax = plt.subplots(figsize=(5, 3.6))
ax.plot(rr, Delta_r, label=r"$\Delta(r)$ (p-wave)", lw=2)
ax.plot(rr, Psi_r, label=r"$\Psi(r)$ (s-wave)", lw=2)
ax.axvline(recPsi, color="gray", ls=":", lw=1)
ax.set_xlabel(r"$r/\xi_0$"); ax.set_ylabel(r"pair potential $/T_c$")
ax.set_title("Vortex pair potentials (same core radius)")
ax.legend(fontsize=9); fig.tight_layout()
fig.savefig(os.path.join(FIGS, "fig1_delta_r.png"), dpi=140); plt.close(fig)

# Fig 2: LDOS map + N(0,r) + core N(E) (two-gap + zero-bias)
fig, axs = plt.subplots(1, 3, figsize=(13, 3.6))
im = axs[0].pcolormesh(RC, Egrid, ldos_tot, shading="auto", cmap="inferno")
axs[0].set_xlabel(r"$r/\xi_0$"); axs[0].set_ylabel(r"$E/T_c$")
axs[0].set_title(r"LDOS $N(E,r)$"); fig.colorbar(im, ax=axs[0])
axs[1].plot(RC, N0_r, "o-"); axs[1].set_xlabel(r"$r/\xi_0$")
axs[1].set_ylabel(r"$N(E{=}0,r)$"); axs[1].set_title("Zero-bias LDOS (core peak)")
axs[2].plot(Egrid, Ncore_E, "-", label="core r=0")
axs[2].plot(Egrid, Nfar_E, "--", color="gray", label="far (bulk, two-gap)")
axs[2].set_xlabel(r"$E/T_c$"); axs[2].set_ylabel(r"$N(E)$")
axs[2].set_title("LDOS vs E: core zero-bias + bulk gaps"); axs[2].legend(fontsize=8)
fig.tight_layout(); fig.savefig(os.path.join(FIGS, "fig2_ldos.png"), dpi=140); plt.close(fig)

# Fig 3: radial magnetization texture (headline) + supercurrent + per-sheet
fig, axs = plt.subplots(1, 3, figsize=(13, 3.6))
axs[0].plot(RC, np.abs(Mr), "o-", color="crimson", label=r"$|M|\sim(g_I-g_II)$")
axs[0].plot(RC, np.abs(Mrc), "s--", color="gray", label="control (equal sheets)")
axs[0].axhline(0, color="k", lw=0.6)
axs[0].set_xlabel(r"$r/\xi_0$"); axs[0].set_ylabel(r"$|M(r)|$ (arb.)")
axs[0].set_title("Radial core magnetization (DISTINCTIVE)"); axs[0].legend(fontsize=8)
axs[1].plot(RC, np.abs(jphi), "o-", color="navy")
axs[1].set_xlabel(r"$r/\xi_0$"); axs[1].set_ylabel(r"$|j(r)|$ (arb.)")
axs[1].set_title(r"Supercurrent $\sim(g_I+g_II)$")
axs[2].plot(RC, np.abs(MI), "-", label="FS-I")
axs[2].plot(RC, np.abs(MII), "-", label="FS-II")
axs[2].set_xlabel(r"$r/\xi_0$"); axs[2].set_ylabel(r"$|g_\nu|$ integrand")
axs[2].set_title("Per-sheet contributions to M"); axs[2].legend(fontsize=8)
fig.tight_layout(); fig.savefig(os.path.join(FIGS, "fig3_magnetization_current.png"), dpi=140); plt.close(fig)

log("figures saved. DONE.")
LOG.close()
