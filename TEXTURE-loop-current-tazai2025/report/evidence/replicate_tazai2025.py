#!/usr/bin/env python3
"""
From-scratch replication of Tazai et al. (2025):
Chiral d-wave superconductivity under a pure loop-current (LC) phase on the
12-site (2x2) kagome supercell model for AV3Sb5.

Headline claim replicated:
  Under pure LC order eta = 0.014 (phi = 0), the chiral d-wave pairing
  eigenvalue lambda_d rises sharply below ~5 meV and takes over the s-wave
  state, giving a chiral d-wave gap Delta_mu ~ (1, w^2, w) (w = e^{i2pi/3}),
  i.e. chi_d = -1, with Tc << 4 meV.

Method (paper Eqs. 1-2):
  lambda Delta_m = g sum_l Gamma_ml Delta_l
  Gamma_ml = (T/N) sum_{k,n} G_k^{ml}(e_n) G_{-k}^{ml}(-e_n) Theta(e_n;Omega)
  Theta(e_n;Omega) = Omega^2 / ((|e_n| - pi T)^2 + Omega^2)

Built from scratch here; the reusable kagome tight-binding geometry conventions
are informed by shared-kernels-cache/loop_current_kagome_kernel.py
(KagomeModel, Peierls-flux LC order). Credit: that kernel.
"""
from __future__ import annotations
import json, sys, time
import numpy as np

SQ3 = np.sqrt(3.0)
a1 = np.array([1.0, 0.0])
a2 = np.array([0.5, SQ3/2.0])
# kagome sublattice offsets (mid-bond convention)
sub = np.array([0.5*a1, 0.5*a2, 0.5*(a1+a2)])   # A,B,C

# ---- Build 2x2 supercell (12 sites) -------------------------------------
# supercell lattice vectors
A1 = 2*a1
A2 = 2*a2
sites = []      # (pos, sublattice_letter 0/1/2, n1, n2)
for n1 in (0,1):
    for n2 in (0,1):
        for s in range(3):
            pos = n1*a1 + n2*a2 + sub[s]
            sites.append((pos, s, n1, n2))
NS = len(sites)   # 12
positions = np.array([p for p,_,_,_ in sites])

# neighbor search over supercell periodic images
def min_image(dr):
    # reduce dr by supercell vectors A1,A2 to nearest image
    Mmat = np.array([A1, A2]).T
    frac = np.linalg.solve(Mmat, dr)
    frac -= np.round(frac)
    return Mmat @ frac

# classify bonds by distance
NN = 0.5     # nearest-neighbour kagome distance (|a1|/2)
NNN = None
# compute all pair distances to find NN, NNN shells
dists = []
for i in range(NS):
    for j in range(NS):
        if i==j: continue
        d = np.linalg.norm(min_image(positions[j]-positions[i]))
        dists.append(d)
dists = np.array(sorted(set(np.round(dists,4))))
d_nn = dists[0]
d_nnn = dists[1]

# ---- LC form factor f_ij (staggered, circulating around center O_eta) ----
# We orient NN bonds so each triangular plaquette carries a net circulating
# current: f_ij = -f_ji = +1 following CCW orientation about each up-triangle,
# with a 2x2 staggered sign so the LC center O_eta pattern breaks C6 (paper
# Fig 1c). This reproduces iCDW / loop-current order delta t^c_ij = i eta f_ij.
def lc_sign(i, j):
    pi_pos, si, n1i, n2i = sites[i]
    pj_pos, sj, n1j, n2j = sites[j]
    # orientation within a triangle: A->B->C->A is +. Use sublattice order.
    order = {(0,1):+1,(1,2):+1,(2,0):+1,(1,0):-1,(2,1):-1,(0,2):-1}
    base = order.get((si,sj),0)
    # 2x2 stagger: flip sign on odd cells (breaks translation to 2x2, C6)
    stag = 1 if ((n1i+n2i) % 2 == 0) else -1
    return base*stag

def build_Hk(k, eta=0.0, phi=0.0, t=-0.5, tp_ratio=0.08):
    """12x12 Bloch Hamiltonian at folded-BZ momentum k."""
    tp = tp_ratio*t
    H = np.zeros((NS,NS), complex)
    Mmat = np.array([A1,A2]).T
    for i in range(NS):
        for j in range(NS):
            if i==j: continue
            dr0 = positions[j]-positions[i]
            dr = min_image(dr0)
            d = np.linalg.norm(dr)
            if abs(d-d_nn) < 1e-3:
                hop = t
                # BO order phi (real, staggered) - zero for pure-LC run
                if phi != 0.0:
                    hop += phi*lc_sign(i,j)  # bond-order form factor g_ij
                # LC order: imaginary i*eta*f_ij
                lc = 1j*eta*lc_sign(i,j)
                amp = hop + lc
            elif abs(d-d_nnn) < 1e-3:
                amp = tp
            else:
                continue
            # Bloch phase over the min-image displacement
            phase = np.exp(1j*np.dot(k, dr))
            H[i,j] += amp*phase
    # Hermitize (numerical safety)
    H = 0.5*(H + H.conj().T)
    return H

# ---- Fermi level for filling n=11 (of 12 bands per cell => actually band
#      filling; paper n=11 electrons per 12-site cell region). We fix mu by
#      target average occupation.
def find_mu(kgrid, eta, filling_frac):
    allE = []
    for k in kgrid:
        allE.append(np.linalg.eigvalsh(build_Hk(k, eta=eta)))
    allE = np.sort(np.concatenate(allE))
    idx = int(round(filling_frac*len(allE)))
    idx = min(max(idx,1), len(allE)-1)
    return 0.5*(allE[idx-1]+allE[idx])

def kmesh(nk):
    fs = (np.arange(nk)+0.5)/nk
    # reciprocal of supercell
    Mmat = np.array([A1,A2]).T
    B = 2*np.pi*np.linalg.inv(Mmat).T
    b1, b2 = B[0], B[1]
    ks = [u*b1+v*b2 for u in fs for v in fs]
    return ks

# ---- Pair kernel Gamma_ml (Eqs. 1-2) ------------------------------------
def pair_kernel(nk, T, eta, mu, Omega=0.01, nmats=64):
    ks = kmesh(nk)
    N = len(ks)
    n_arr = np.arange(-nmats, nmats)
    eps = np.pi*T*(2*n_arr+1)
    Theta = Omega**2/((np.abs(eps)-np.pi*T)**2 + Omega**2)
    Gamma = np.zeros((NS,NS), complex)
    I = np.eye(NS)
    # precompute H(k) and H(-k)
    for k in ks:
        Hk = build_Hk(k, eta=eta) - mu*I
        Hmk = build_Hk(-np.array(k), eta=eta) - mu*I
        for e, th in zip(eps, Theta):
            Gk = np.linalg.inv(1j*e*I - Hk)
            Gmk = np.linalg.inv(-1j*e*I - Hmk)
            # element-wise G_k^{ml} G_{-k}^{ml}
            Gamma += (Gk*Gmk)*th
    Gamma *= T/N
    return Gamma

def solve_gap(Gamma, g):
    M = g*Gamma
    # symmetric-ish; use general eigensolver
    w, V = np.linalg.eig(M)
    order = np.argsort(-w.real)
    return w[order], V[:,order]

# ---- Chiral d-wave detection --------------------------------------------
def chiral_overlap(vec):
    """Project 12-vector onto chiral d-wave pattern Delta_mu ~ (1,w^2,w)
    across sublattices A,B,C (w=e^{i2pi/3}), uniform across mu."""
    w = np.exp(2j*np.pi/3)
    patt = np.zeros(NS, complex)
    for idx,(pos,s,n1,n2) in enumerate(sites):
        patt[idx] = [1.0, w**2, w][s]
    patt /= np.linalg.norm(patt)
    v = vec/np.linalg.norm(vec)
    return abs(np.vdot(patt, v))

def swave_overlap(vec):
    patt = np.ones(NS, complex); patt/=np.linalg.norm(patt)
    v = vec/np.linalg.norm(vec)
    return abs(np.vdot(patt, v))

# ---- Main sweep ----------------------------------------------------------
def run():
    t0 = time.time()
    g = 0.4          # < 0.5 per paper
    Omega = 0.01
    nk = 8
    eta0 = 0.014
    T_meV = [0.1, 0.5, 1.0, 2.0, 3.0, 5.0, 8.0]
    filling = 11.0/12.0

    # mu at eta0 (meV-scale T doesn't move mu much; use T-independent grid)
    ks = kmesh(nk)
    mu = find_mu(ks, eta0, filling)

    # (A) lambda vs T at eta=0.014 : expect lambda_d rise for T<5meV
    lamT = []
    for Tm in T_meV:
        T = Tm/1000.0   # eV
        Gam = pair_kernel(nk, T, eta0, mu, Omega=Omega)
        w, V = solve_gap(Gam, g)
        # identify s-wave and chiral-d among top few eigvecs
        top = []
        for i in range(min(6,NS)):
            top.append(dict(lam=float(w[i].real),
                            chiral_d=float(chiral_overlap(V[:,i])),
                            swave=float(swave_overlap(V[:,i]))))
        # pick best chiral-d and best s-wave
        d_lam = max(top, key=lambda x: x['chiral_d'])
        s_lam = max(top, key=lambda x: x['swave'])
        lamT.append(dict(T_meV=Tm, lam_d=d_lam['lam'], lam_s=s_lam['lam'],
                         chiral_d_overlap=d_lam['chiral_d'],
                         swave_overlap=s_lam['swave'],
                         lam_max=float(w[0].real)))
        print(f"  T={Tm:5.2f} meV  lam_d={d_lam['lam']:.4f} (chi-overlap {d_lam['chiral_d']:.2f})  lam_s={s_lam['lam']:.4f}")

    # (B) lambda_d vs eta at T=0.5 meV: expect chiral d rises 0.01-0.016
    T = 0.5/1000.0
    lamEta = []
    for eta in [0.0, 0.005, 0.01, 0.014, 0.016, 0.02]:
        muE = find_mu(ks, eta, filling)
        Gam = pair_kernel(nk, T, eta, muE, Omega=Omega)
        w, V = solve_gap(Gam, g)
        top = [(float(w[i].real), chiral_overlap(V[:,i]), swave_overlap(V[:,i])) for i in range(min(6,NS))]
        d = max(top, key=lambda x:x[1]); s = max(top, key=lambda x:x[2])
        lamEta.append(dict(eta=eta, lam_d=d[0], lam_s=s[0], chiral_d_overlap=float(d[1])))
        print(f"  eta={eta:.3f}  lam_d={d[0]:.4f}  lam_s={s[0]:.4f}  chi-overlap={d[1]:.2f}")

    # (C) eigenvector structure at eta0, low T
    Gam = pair_kernel(nk, 0.1/1000.0, eta0, mu, Omega=Omega)
    w, V = solve_gap(Gam, g)
    # find chiral-d eigenvector
    ov = [chiral_overlap(V[:,i]) for i in range(NS)]
    id_d = int(np.argmax(ov))
    vd = V[:,id_d]/np.linalg.norm(V[:,id_d])
    # average phase per sublattice A,B,C
    sub_phase = {}
    for s,let in zip(range(3),'ABC'):
        comps = [vd[i] for i in range(NS) if sites[i][1]==s]
        m = np.mean(comps)
        sub_phase[let] = dict(mag=float(abs(m)), phase_deg=float(np.degrees(np.angle(m))))

    result = dict(
        paper="tazai2025 - chiral d-wave under pure loop-current order (kagome AV3Sb5)",
        method="12-site (2x2) kagome mean-field SC gap equation, Eqs.1-2; on-site attractive g",
        kernel_credit="loop_current_kagome_kernel.py (KagomeModel Peierls-flux LC conventions)",
        params=dict(t=-0.5, tp_over_t=0.08, filling_n_over_12=filling, g=g, Omega=Omega,
                    eta_claim=eta0, nk=nk, nmats=64, mu=float(mu)),
        A_lambda_vs_T=lamT,
        B_lambda_vs_eta=lamEta,
        C_chiral_d_eigenvector=dict(
            chiral_d_overlap=float(ov[id_d]),
            sublattice_ABC_phases=sub_phase,
            expected_pattern="(1, w^2, w), w=exp(i2pi/3): phases 0, -120, +120 deg",
        ),
        runtime_s=round(time.time()-t0,1),
    )
    return result

if __name__ == "__main__":
    print("Running from-scratch Tazai2025 replication...")
    res = run()
    out = "/home/stevens/textures-100/corpus/textures-loop-current-tazai2025/work/tazai2025_result.json"
    with open(out,"w") as f:
        json.dump(res, f, indent=2)
    print("SAVED ->", out)
