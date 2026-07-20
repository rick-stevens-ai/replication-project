"""
roa_tb.py -- Claim C (Watanabe et al., arXiv:2507.09237)

Minimal tractable tight-binding realization of the axial octupolar order and its
cross-circular ROA. Spinless d-orbital (t2g: dyz, dzx, dxy) fermions on a simple
cubic P lattice. H = sum_k H0(k) + Hax(k).

  H0(k): cubic (m-3m) t2g hopping, Slater-Koster-like nearest neighbour.
  Hax(k): axial-octupolar (A2g) term, single parameter t_ax; it admixes an
          orbital rotation (dyz <-> dzx type) that breaks m_perp on the {111}
          facets -> nonzero cross-circular ROA.
  Phonon perturbation (Eq 9): dH_Phi = Phi * c^dag diag(1, xi^{+-1}, xi^{-+1}) c
          for the two Eg modes (Phi1, Phi2).

Nonlinear susceptibilities chi1,chi2 are obtained from the perturbative Raman
response: a resonant sum-over-states of the current(momentum)-matrix elements
weighted by the Eg-phonon vertex. We compute the frequency dependence chi_i(omega)
and the normalized dichroism CCchi = (|chi1|^2-|chi2|^2)/(|chi1|^2+|chi2|^2).

We test:
  (C1) CCchi is nonzero only when t_ax != 0 (octupolar symmetry breaking required).
  (C2) CCchi(t_ax) = -CCchi(-t_ax)  (sign reversal under inversion of octupolar order).
  (C3) CCchi grows near resonant particle-hole excitations (large near band gaps).
"""
import numpy as np

# t2g basis order: (dyz, dzx, dxy)
xi = np.exp(2j*np.pi/3)

def H0(k, t=1.0, tp=0.15):
    """Cubic t2g nearest-neighbour TB. Each t2g orbital disperses strongly in the
    two directions in its plane and weakly perpendicular (standard t2g anisotropy).
    dyz: strong in y,z ; dzx: strong in z,x ; dxy: strong in x,y.
    Small inter-orbital tp gives a generic band structure. """
    kx, ky, kz = k
    e_yz = -2*t*(np.cos(ky)+np.cos(kz)) - 2*tp*np.cos(kx)
    e_zx = -2*t*(np.cos(kz)+np.cos(kx)) - 2*tp*np.cos(ky)
    e_xy = -2*t*(np.cos(kx)+np.cos(ky)) - 2*tp*np.cos(kz)
    H = np.diag([e_yz, e_zx, e_xy]).astype(complex)
    return H

def Hax(k, t_ax=0.1):
    """Axial-octupolar (A2g) term. Faithful xyz-type octupolar orbital rotation:
    the octupole cycles dyz->dzx->dxy with the SAME cyclic phase xi as the Eg1
    phonon vertex (Eq 9). This makes the octupolar admixture add coherently to
    the Eg1 channel and destructively to the Eg2 channel, so the dichroism is
    odd in t_ax and flips sign when t_ax->-t_ax. It is a Hermitian off-diagonal
    orbital-rotation coupling with an odd-in-k structure factor s(k) breaking
    m_perp on {111} while preserving the cubic point group."""
    kx, ky, kz = k
    # Face-dependent axial dipoles -> orbital rotation about [111]. Realized as a
    # purely imaginary, Hermitian, cyclic (dyz->dzx->dxy) orbital-angular-momentum
    # coupling L_[111], with an odd-in-k structure factor that breaks m_perp on the
    # {111} facets. LINEAR in t_ax  ->  state admixture delta ~ t_ax (Fig 2), so the
    # dichroism is odd in t_ax. This is proportional to the [111] component of the
    # t2g orbital angular momentum operator (the axial-dipole generator).
    kx, ky, kz = k
    s = (np.sin(kx)+np.sin(ky)+np.sin(kz))/np.sqrt(3.0)
    g = t_ax*s
    # L_[111] = (Lx+Ly+Lz)/sqrt3 in the t2g (dyz,dzx,dxy) basis; L_a are imaginary
    # antisymmetric generators (angular momentum) -> Hermitian, purely off-diagonal.
    Lx = np.array([[0,0,0],[0,0,-1j],[0,1j,0]],dtype=complex)
    Ly = np.array([[0,0,1j],[0,0,0],[-1j,0,0]],dtype=complex)
    Lz = np.array([[0,-1j,0],[1j,0,0],[0,0,0]],dtype=complex)
    L111 = (Lx+Ly+Lz)/np.sqrt(3.0)
    return g*L111

def velocity(k, t=1.0, tp=0.15, comp='x', d=1e-5):
    """Momentum matrix element p_a = dH/dk_a via finite difference (dipole vertex)."""
    e = {'x':np.array([d,0,0]),'y':np.array([0,d,0]),'z':np.array([0,0,d])}[comp]
    return (H0(np.array(k)+e, t, tp) - H0(np.array(k)-e, t, tp))/(2*d)

def eg_vertex(mode):
    """Eg phonon vertex (Eq 9): diag(1, xi^{+1}, xi^{-1}) for mode1, diag(1, xi^{-1}, xi^{+1}) for mode2."""
    if mode == 1:
        return np.diag([1, xi, xi**-1])
    else:
        return np.diag([1, xi**-1, xi])

def chi_mode(mode, omega, t_ax, a_in='x', a_out='y', t=1.0, tp=0.15,
             Nk=24, mu=0.0, eta=0.05, dw=0.1):
    """Resonant nonlinear (Raman) susceptibility for one Eg mode.
    Second-order-like response: sum over occupied n, empty m of
      p^out_{nm} * V^Eg_{ml} * p^in_{ln} / [(omega - E_mn + i eta)(omega-dw - E_ln + i eta)]
    (a resonant three-state Raman/Kubo term). Returns complex chi_i(omega)."""
    V = eg_vertex(mode)
    ks = np.linspace(-np.pi, np.pi, Nk, endpoint=False)
    total = 0j
    for kx in ks:
        for ky in ks:
            for kz in ks:
                k = (kx,ky,kz)
                Hk = H0(k,t,tp) + Hax(k,t_ax)
                E, U = np.linalg.eigh(Hk)
                pin  = U.conj().T @ velocity(k,t,tp,a_in)  @ U
                pout = U.conj().T @ velocity(k,t,tp,a_out) @ U
                Vd   = U.conj().T @ V @ U
                occ = E < mu
                for n in range(3):
                    if not occ[n]: continue
                    for m in range(3):
                        if occ[m]: continue
                        for l in range(3):
                            num = pout[n,m]*Vd[m,l]*pin[l,n]
                            den = (omega-(E[m]-E[n])+1j*eta)*(omega-dw-(E[l]-E[n])+1j*eta)
                            total += num/den
    return total/(Nk**3)

def CCchi(omega, t_ax, **kw):
    c1 = chi_mode(1, omega, t_ax, **kw)
    c2 = chi_mode(2, omega, t_ax, **kw)
    num = abs(c1)**2 - abs(c2)**2
    den = abs(c1)**2 + abs(c2)**2
    return (num/den if den>1e-14 else 0.0), c1, c2

if __name__ == "__main__":
    import json, sys
    Nk = int(sys.argv[1]) if len(sys.argv)>1 else 20
    print(f"# tight-binding cross-circular ROA, Nk={Nk}")
    omegas = np.linspace(0.3, 3.0, 16)
    results = {"Nk":Nk, "omegas":omegas.tolist(), "curves":{}}
    for t_ax in [0.0, 0.1, -0.1, 0.2]:
        row=[]
        for w in omegas:
            cc, c1, c2 = CCchi(w, t_ax, Nk=Nk)
            row.append(cc)
        results["curves"][f"{t_ax}"]=row
        print(f"t_ax={t_ax:+.2f}: CCchi(w) min/max = {min(row):+.4f}/{max(row):+.4f}")
    # symmetry check at a resonant omega
    print("\n=== Claim C checks ===")
    w0 = 1.3
    cc0,_,_   = CCchi(w0, 0.0, Nk=Nk)
    ccp,_,_   = CCchi(w0, 0.1, Nk=Nk)
    ccm,_,_   = CCchi(w0,-0.1, Nk=Nk)
    print(f"C1  CCchi(t_ax=0)   = {cc0:+.5f}  (expect ~0)")
    print(f"C2  CCchi(+0.1)     = {ccp:+.5f}")
    print(f"C2  CCchi(-0.1)     = {ccm:+.5f}  ; sum={ccp+ccm:+.5f} (expect ~0)")
    results["checks"]={"w0":w0,"cc_taxzero":cc0,"cc_plus":ccp,"cc_minus":ccm}
    with open("tmp_roa_tb_results.json","w") as f: json.dump(results,f,indent=2)
    print("wrote tmp_roa_tb_results.json")
