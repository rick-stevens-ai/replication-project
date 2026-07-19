#!/usr/bin/env python
"""
Independent real-space finite-difference BdG replication of:
  Dar, Scheurer, Schrade, "Altermagnetic spin textures coupled to superconductors:
  Domain wall spin-triplet superconductivity and supercurrent-induced torques"
  (arXiv:2607.15249v1, textures-orbital-dar2026).

Implements the PROJECTED low-energy effective Hamiltonian for a planar radial
Neel domain wall (paper Eq. 8) with the geometric/emergent fields (Eq. 4, and the
radial-wall forms in Sec. IV):

  h_proj(r,p) = xi(r,p) sigma0 + bz(r,p) sigma_z + (1/2){p, alpha(r)} sigma_x

  xi(r,p) = rho0 p^2 + rho0 V0(r) - mu ,     V0(r) = (1/4) phi'(r)^2
  bz(r,p) = rho_z (px^2 - py^2) + rho_z Vz(r,chi),  Vz = (1/4) phi'(r)^2 cos(2chi)
  alpha(r)= rho3 phi'(r) rhat   (radial),   phi(r) = (pi/2) tanh((r-R0)/w)

BdG (Eq. 7), fixed uniform proximity singlet Delta0 (semiclassical, non-self-consistent):
  H = [[ h_proj ,  Delta0(-i sigma_y) ],
       [ Delta0(-i sigma_y)^dag , -h_proj*        ]]

Convention: hbar = 1, energies in eV, lengths in nm (rho's in eV nm^2, so p is a
wavevector [1/nm] and rho*p^2 is an energy -- consistent with the paper's dispersion).

We extract:
  * on-site singlet amplitude  psi_s(r) = <c_up c_dn> - <c_dn c_up>  (s-wave)
  * equal-spin triplet p-wave bond intensity It(r) = sum_{sigma,delta} |<c_{r,sigma} c_{r+delta,sigma}>|^2
  * spin-resolved It_up, It_dn and spin selectivity
and test the headline: triplet hotspots localized at the wall, with fourfold
angular modulation in the AM case (rho_z != 0) that vanishes in the AFM limit.
"""
import json, time
import numpy as np
import scipy.sparse as sp
from scipy.linalg import eigh

# ----------------------------- parameters -----------------------------
# eV / nm units (recipe values, geometry shrunk to keep dense diag light but wall well inside box)
rho0 = 1.0      # eV nm^2
rho_z = 0.1     # eV nm^2 (altermagnetic d-wave splitting); set 0 for AFM limit
rho3 = 0.05     # eV nm^2 (controls emergent SOC)
mu   = 0.010    # eV  (10 meV)
Delta0 = 0.0005 # eV  (0.5 meV)
R0 = 20.0       # nm  domain-wall radius
w  = 4.0        # nm  wall width
N  = 44         # grid points per side
a  = 1.6        # nm  spacing -> box ~70 nm, wall (R0=20) well inside
T  = 0.0        # zero temperature

sx = np.array([[0,1],[1,0]], dtype=complex)
sz = np.array([[1,0],[0,-1]], dtype=complex)
s0 = np.eye(2, dtype=complex)
misy = np.array([[0,-1],[1,0]], dtype=complex)  # -i sigma_y

def build_fields():
    coords = (np.arange(N) - (N-1)/2.0) * a
    X, Y = np.meshgrid(coords, coords, indexing='xy')  # shape (N,N), index [iy,ix]
    r = np.sqrt(X**2 + Y**2)
    chi = np.arctan2(Y, X)
    sech2 = 1.0/np.cosh((r-R0)/w)**2
    phip = (np.pi/2.0)*(1.0/w)*sech2          # phi'(r)  [1/nm]
    V0 = 0.25*phip**2                          # [1/nm^2]
    Vz = 0.25*phip**2*np.cos(2*chi)
    ax = rho3*phip*np.cos(chi)                 # alpha_x [eV nm]
    ay = rho3*phip*np.sin(chi)
    return X, Y, r, chi, phip, V0, Vz, ax, ay

def idx(iy, ix):
    return iy*N + ix

def build_site_operators(V0, Vz, ax, ay):
    Ns = N*N
    inva2 = 1.0/a**2
    # K0 = rho0 * (-lap) ; Kz = rho_z*(-d2x + d2y) ; onsite scalars
    K0 = sp.lil_matrix((Ns, Ns), dtype=complex)
    Kz = sp.lil_matrix((Ns, Ns), dtype=complex)
    O  = sp.lil_matrix((Ns, Ns), dtype=complex)   # SOC scalar operator (mult sigma_x)
    d0 = np.zeros(Ns, dtype=complex)              # onsite sigma0
    dz = np.zeros(Ns, dtype=complex)              # onsite sigma_z
    # divergence of alpha via central differences
    divA = np.zeros((N, N), dtype=complex)
    for iy in range(N):
        for ix in range(N):
            k = idx(iy, ix)
            # ---- kinetic diagonals ----
            K0[k, k] += rho0*4.0*inva2
            # x neighbors
            if ix+1 < N:
                K0[k, idx(iy,ix+1)] += -rho0*inva2
                Kz[k, idx(iy,ix+1)] += -rho_z*inva2     # from -d2x
            if ix-1 >= 0:
                K0[k, idx(iy,ix-1)] += -rho0*inva2
                Kz[k, idx(iy,ix-1)] += -rho_z*inva2
            # y neighbors
            if iy+1 < N:
                K0[k, idx(iy+1,ix)] += -rho0*inva2
                Kz[k, idx(iy+1,ix)] += +rho_z*inva2     # from +d2y
            if iy-1 >= 0:
                K0[k, idx(iy-1,ix)] += -rho0*inva2
                Kz[k, idx(iy-1,ix)] += +rho_z*inva2
            # ---- onsite scalars ----
            d0[k] = rho0*V0[iy,ix] - mu
            dz[k] = rho_z*Vz[iy,ix]
            # ---- div alpha ----
            axp = ax[iy,ix+1] if ix+1<N else 0.0
            axm = ax[iy,ix-1] if ix-1>=0 else 0.0
            ayp = ay[iy+1,ix] if iy+1<N else 0.0
            aym = ay[iy-1,ix] if iy-1>=0 else 0.0
            divA[iy,ix] = (axp-axm)/(2*a) + (ayp-aym)/(2*a)
    # SOC operator O = (-i/2) divA  - i (ax d_x + ay d_y),  d central
    for iy in range(N):
        for ix in range(N):
            k = idx(iy, ix)
            O[k, k] += (-1j/2.0)*divA[iy,ix]
            if ix+1 < N:
                O[k, idx(iy,ix+1)] += -1j*ax[iy,ix]/(2*a)
            if ix-1 >= 0:
                O[k, idx(iy,ix-1)] += +1j*ax[iy,ix]/(2*a)
            if iy+1 < N:
                O[k, idx(iy+1,ix)] += -1j*ay[iy,ix]/(2*a)
            if iy-1 >= 0:
                O[k, idx(iy-1,ix)] += +1j*ay[iy,ix]/(2*a)
    K0 = K0.tocsr(); Kz = Kz.tocsr(); O = O.tocsr()
    O = 0.5*(O + O.getH())   # enforce hermiticity (symmetric FD ordering)
    return K0, Kz, O, d0, dz

def build_He(K0, Kz, O, d0, dz):
    Ns = N*N
    He = sp.kron(K0, s0) + sp.kron(Kz, sz) + sp.kron(O, sx) \
         + sp.kron(sp.diags(d0), s0) + sp.kron(sp.diags(dz), sz)
    return He.tocsr()

def build_bdg(He):
    Ns2 = He.shape[0]  # 2*N*N
    D = sp.kron(sp.identity(N*N), Delta0*misy).tocsr()
    top = sp.hstack([He, D])
    bot = sp.hstack([D.getH(), -He.conj()])
    H = sp.vstack([top, bot]).tocsr()
    return H

def anomalous(evecs, evals):
    """F_full(a,b)=<c_a c_b> = sum_{E>0} u[a,n] conj(v[b,n]). a,b run over (site,spin)."""
    Ns2 = evecs.shape[0]//2
    pos = evals > 1e-12
    U = evecs[:Ns2, pos]        # particle amplitudes
    Vv = evecs[Ns2:, pos]       # hole amplitudes
    F = U @ Vv.conj().T         # (2Ns x 2Ns)
    return F

def orb(k, sigma):  # sigma: 0=up,1=dn ; spin fastest
    return 2*k + sigma

def extract(F):
    Ns = N*N
    psi_s = np.zeros((N,N))
    It_up = np.zeros((N,N)); It_dn = np.zeros((N,N))
    for iy in range(N):
        for ix in range(N):
            k = idx(iy,ix)
            uu = F[orb(k,0), orb(k,1)]  # <c_up c_dn>
            du = F[orb(k,1), orb(k,0)]  # <c_dn c_up>
            psi_s[iy,ix] = abs(0.5*(uu-du))
            # equal-spin p-wave bond amplitudes (+x, +y)
            acc_up = 0.0; acc_dn = 0.0
            for (jy,jx) in [(iy,ix+1),(iy+1,ix)]:
                if 0<=jx<N and 0<=jy<N:
                    kk = idx(jy,jx)
                    acc_up += abs(F[orb(k,0), orb(kk,0)])**2
                    acc_dn += abs(F[orb(k,1), orb(kk,1)])**2
            It_up[iy,ix] = acc_up
            It_dn[iy,ix] = acc_dn
    It = It_up + It_dn
    return psi_s, It, It_up, It_dn

def ring_profile(field, r, nb=40):
    rmax = (N-1)/2.0*a
    edges = np.linspace(0, rmax, nb+1)
    prof = []
    for i in range(nb):
        m = (r>=edges[i]) & (r<edges[i+1])
        prof.append(float(field[m].mean()) if m.any() else 0.0)
    centers = 0.5*(edges[:-1]+edges[1:])
    return centers, np.array(prof)

def angular_on_wall(field, r, chi, dr=4.0):
    """average field in annulus |r-R0|<dr as function of chi, in 16 bins."""
    m = np.abs(r-R0) < dr
    ch = chi[m]; fv = field[m]
    nb = 16
    edges = np.linspace(-np.pi, np.pi, nb+1)
    prof = []
    for i in range(nb):
        mm = (ch>=edges[i]) & (ch<edges[i+1])
        prof.append(float(fv[mm].mean()) if mm.any() else 0.0)
    centers = 0.5*(edges[:-1]+edges[1:])
    return centers, np.array(prof)

def run(rz):
    global rho_z
    rho_z = rz
    X,Y,r,chi,phip,V0,Vz,ax,ay = build_fields()
    K0,Kz,O,d0,dz = build_site_operators(V0,Vz,ax,ay)
    He = build_He(K0,Kz,O,d0,dz)
    H = build_bdg(He).toarray()
    # hermiticity check
    herm = np.max(np.abs(H - H.conj().T))
    evals, evecs = eigh(H)
    F = anomalous(evecs, evals)
    psi_s, It, It_up, It_dn = extract(F)
    return dict(r=r, chi=chi, psi_s=psi_s, It=It, It_up=It_up, It_dn=It_dn,
                herm=float(herm), emin=float(np.min(np.abs(evals))))

if __name__ == "__main__":
    t0=time.time()
    print(f"Grid {N}x{N} (box {(N-1)*a:.0f} nm), dim BdG = {4*N*N}")
    res_am  = run(0.1)   # altermagnet
    print(f"AM done  t={time.time()-t0:.1f}s herm={res_am['herm']:.1e}")
    res_afm = run(0.0)   # antiferromagnet limit
    print(f"AFM done t={time.time()-t0:.1f}s")

    r = res_am['r']; chi = res_am['chi']
    # radial localization of triplet
    rc, prof_am  = ring_profile(res_am['It'], r)
    _,  prof_afm = ring_profile(res_afm['It'], r)
    # angular modulation on the wall
    ac, ang_am_tot = angular_on_wall(res_am['It'],  r, chi)
    _,  ang_afm_tot= angular_on_wall(res_afm['It'], r, chi)
    _,  ang_up     = angular_on_wall(res_am['It_up'], r, chi)
    _,  ang_dn     = angular_on_wall(res_am['It_dn'], r, chi)

    # metrics
    # triplet localization: fraction of total It within +/- 2w of wall
    wall_mask = np.abs(r-R0) < 2*w
    loc_am  = float(res_am['It'][wall_mask].sum()/res_am['It'].sum())
    loc_afm = float(res_afm['It'][wall_mask].sum()/res_afm['It'].sum())
    # fourfold modulation strength: (max-min)/(max+min) of angular profile on wall
    def mod(a): 
        a=np.array(a); return float((a.max()-a.min())/(a.max()+a.min()+1e-30))
    mod_am  = mod(ang_am_tot)
    mod_afm = mod(ang_afm_tot)
    # count angular maxima (fourfold?) via fft component m=4
    def fft_power(a):
        a=np.array(a)-np.mean(a); F=np.abs(np.fft.rfft(a))
        return {str(m): float(F[m]) for m in range(1,7)}
    fftp_am = fft_power(ang_am_tot); fftp_afm = fft_power(ang_afm_tot)

    out = dict(
        params=dict(rho0=rho0, rho_z_AM=0.1, rho3=rho3, mu=mu, Delta0=Delta0,
                    R0=R0, w=w, N=N, a=a, box_nm=(N-1)*a),
        hermiticity_residual=res_am['herm'],
        min_abs_bdg_eigenvalue=res_am['emin'],
        triplet_max_over_singlet_max_AM=float(np.sqrt(res_am['It'].max())/(res_am['psi_s'].max()+1e-30)),
        singlet_max_AM=float(res_am['psi_s'].max()),
        singlet_at_center_AM=float(res_am['psi_s'][N//2,N//2]),
        triplet_It_max_AM=float(res_am['It'].max()),
        triplet_It_max_AFM=float(res_afm['It'].max()),
        triplet_localization_frac_AM=loc_am,
        triplet_localization_frac_AFM=loc_afm,
        angular_modulation_AM=mod_am,
        angular_modulation_AFM=mod_afm,
        fft_angular_power_AM=fftp_am,
        fft_angular_power_AFM=fftp_afm,
        radial_centers_nm=rc.tolist(),
        radial_It_AM=prof_am.tolist(),
        radial_It_AFM=prof_afm.tolist(),
        angular_centers_rad=ac.tolist(),
        angular_It_AM=ang_am_tot.tolist(),
        angular_It_AFM=ang_afm_tot.tolist(),
        angular_It_up_AM=ang_up.tolist(),
        angular_It_dn_AM=ang_dn.tolist(),
    )
    with open("dar2026_result.json","w") as f:
        json.dump(out, f, indent=2)
    print("\n=== SUMMARY ===")
    print(f"Hermiticity residual: {out['hermiticity_residual']:.2e}")
    print(f"Singlet max (AM): {out['singlet_max_AM']:.3e}  center: {out['singlet_at_center_AM']:.3e}")
    print(f"Triplet It max AM/AFM: {out['triplet_It_max_AM']:.3e} / {out['triplet_It_max_AFM']:.3e}")
    print(f"Triplet localization frac (|r-R0|<2w) AM/AFM: {loc_am:.3f} / {loc_afm:.3f}")
    print(f"Angular modulation on wall AM/AFM: {mod_am:.3f} / {mod_afm:.3f}")
    print(f"FFT angular power AM: {fftp_am}")
    print(f"FFT angular power AFM: {fftp_afm}")
    print("Wrote dar2026_result.json")
