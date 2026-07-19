"""
Independent replication of Zhang, Liu & Zhang (2012), arXiv:1211.0762,
"Spin-orbital Texture in Topological Insulators".

Core physics: TI surface Dirac Hamiltonian H = hbar vf (sx ky - sy kx) [Eq.1].
The eigenstates |Phi+/-> are expanded in p-orbitals (px,py,pz) x real-spin
(up,down) up to first order in k [Eqs. 4,5]. We build these 6-dim wavefunctions
from the equations (NOT author code), then compute the spin-orbital projection
D^+/-_{i,eta} = <Phi|(|pi><pi| (x) s_eta)|Phi>  [Eq.6]
around the Fermi contour and compare to the paper's analytic predictions
(Eqs. 7,8 for px/py spin textures; pz texture; Eq.10 for Ppx polarization).

We use a single effective orbital-parameter set (drop the atom-sum over alpha,
which only rescales overall magnitudes). Parameters u0,v0,u1,v1,w1 taken real
(as the paper states from ab-initio fit). hbar*vf = 1 (units of energy/k).
"""
import numpy as np
import json, os

# ---- basis: orbital {px,py,pz} (index 0,1,2) (x) spin {up,down} (index 0,1) ----
# 6-vector index = 2*orb + spin
def orb_vec(name, theta):
    px = np.array([1,0,0.], complex)
    py = np.array([0,1,0.], complex)
    pz = np.array([0,0,1.], complex)
    if name == 'pz': return pz
    if name == 'pr': return np.cos(theta)*px + np.sin(theta)*py     # radial
    if name == 'pt': return -np.sin(theta)*px + np.cos(theta)*py    # tangential

def spin_vec(name, theta):
    up = np.array([1,0.], complex); dn = np.array([0,1.], complex)
    if name == 'up_t':  return (1/np.sqrt(2))*(+1j*np.exp(-1j*theta)*up + dn)  # |up_theta> left-handed
    if name == 'dn_t':  return (1/np.sqrt(2))*(-1j*np.exp(-1j*theta)*up + dn)  # |dn_theta> right-handed

def kron(orb, spin):
    return np.kron(orb, spin)  # length 6

def Phi(cone, k, theta, p):
    """cone = +1 (upper) or -1 (lower). p = (u0,v0,u1,v1,w1). Eqs.4,5."""
    u0,v0,u1,v1,w1 = p
    s = cone  # +/- sign
    up_t = spin_vec('up_t', theta); dn_t = spin_vec('dn_t', theta)
    if cone == +1:  # Eq.4
        c_pz =  (u0 - v1*k)
        c_pr = -(1j/np.sqrt(2))*(v0 - u1*k - w1*k)
        c_pt =  (1/np.sqrt(2))*(v0 - u1*k + w1*k)
        v = ( c_pz*kron(orb_vec('pz',theta), up_t)
            + c_pr*kron(orb_vec('pr',theta), up_t)
            + c_pt*kron(orb_vec('pt',theta), dn_t) )
    else:           # Eq.5
        c_pz =  (u0 + v1*k)
        c_pr =  (1j/np.sqrt(2))*(v0 + u1*k + w1*k)
        c_pt = -(1/np.sqrt(2))*(v0 + u1*k - w1*k)
        v = ( c_pz*kron(orb_vec('pz',theta), dn_t)
            + c_pr*kron(orb_vec('pr',theta), dn_t)
            + c_pt*kron(orb_vec('pt',theta), up_t) )
    return v

# ---- Pauli/orbital projectors in the 6-dim space ----
I2 = np.eye(2, dtype=complex)
sx = np.array([[0,1],[1,0]], complex)
sy = np.array([[0,-1j],[1j,0]], complex)
sz = np.array([[1,0],[0,-1]], complex)
S = {'0':I2,'x':sx,'y':sy,'z':sz}
def orb_proj(i):
    P = np.zeros((3,3), complex); P[i,i]=1; return P   # |pi><pi| in px,py,pz basis
ORB = {'px':orb_proj(0),'py':orb_proj(1),'pz':orb_proj(2)}

def D(cone,k,theta,p,orb,eta):
    v = Phi(cone,k,theta,p)
    M = np.kron(ORB[orb], S[eta])
    return np.real(np.vdot(v, M@v))

# ---- effective parameters (real, arbitrary but generic) ----
p = (1.0, 0.6, 0.4, 0.3, 0.25)   # u0,v0,u1,v1,w1
u0,v0,u1,v1,w1 = p
k = 0.3
thetas = np.linspace(0, 2*np.pi, 24, endpoint=False)

report = {}

# ---- TEST 1: pz spin texture  [Dpz,x,Dpz,y,Dpz,z] = +/- (u0 -/+ v1 k)^2 [sin,-cos,0] ----
err_pz = 0
for cone in (+1,-1):
    for th in thetas:
        amp = (u0 - cone*v1*k)**2
        pred = cone*amp*np.array([np.sin(th), -np.cos(th), 0.0])
        got = np.array([D(cone,k,th,p,'pz',e) for e in ('x','y','z')])
        err_pz = max(err_pz, np.max(np.abs(got-pred)))
report['pz_texture_maxabs_err'] = float(err_pz)

# ---- TEST 2: px spin texture Eq.7  = -/+ (v0^2/2)[sin,cos,0] (small k) ----
# The paper's Eqs 7,8 are the small-k limit; check at small k.
ksmall = 1e-4
err_px = err_py = 0
for cone in (+1,-1):
    for th in thetas:
        pred_px = -cone*(v0**2/2)*np.array([np.sin(th), np.cos(th), 0.0])
        pred_py = +cone*(v0**2/2)*np.array([np.sin(th), np.cos(th), 0.0])
        got_px = np.array([D(cone,ksmall,th,p,'px',e) for e in ('x','y','z')])
        got_py = np.array([D(cone,ksmall,th,p,'py',e) for e in ('x','y','z')])
        err_px = max(err_px, np.max(np.abs(got_px-pred_px)))
        err_py = max(err_py, np.max(np.abs(got_py-pred_py)))
report['px_texture_smallk_maxabs_err'] = float(err_px)
report['py_texture_smallk_maxabs_err'] = float(err_py)

# ---- TEST 3: orbital-character difference Dpx0 - Dpy0 = -/+ 2 cos(2th) (v0 -/+ k u1) k w1 ----
err_diff = 0
for cone in (+1,-1):
    for th in thetas:
        pred = -cone*2*np.cos(2*th)*(v0 - cone*k*u1)*k*w1
        got = D(cone,k,th,p,'px','0') - D(cone,k,th,p,'py','0')
        err_diff = max(err_diff, abs(got-pred))
report['orbital_char_diff_2theta_maxabs_err'] = float(err_diff)

# ---- TEST 4: total in-plane spin [Dx,Dy] = 4[-sin,cos](v0 -/+ k u1) k w1 (right-handed) ----
err_tot = 0; handed = []
for cone in (+1,-1):
    coef = (v0 - cone*k*u1)*k*w1
    for th in thetas:
        pred = 4*np.array([-np.sin(th), np.cos(th)])*coef
        Dx = D(cone,k,th,p,'px','x')+D(cone,k,th,p,'py','x')
        Dy = D(cone,k,th,p,'px','y')+D(cone,k,th,p,'py','y')
        err_tot = max(err_tot, np.max(np.abs(np.array([Dx,Dy])-pred)))
    handed.append(coef>0)  # right-handed when coef>0
report['total_inplane_spin_maxabs_err'] = float(err_tot)
report['total_inplane_right_handed_both_cones'] = bool(handed[0] and handed[1])

# ---- TEST 5: Ppx polarization Eq.10  ----
# Ppx(cone) = [Dpx0(th=0) - Dpx0(th=90)]/[sum]  (Eq.9), analytic Eq.10:
# Ppx = -/+ 2(v0 -/+ E u1)(E w1) / [ (v0 -/+ E u1)^2 + E^2 w1^2 ]  (hbar vf =1, E = k here mapping)
err_pp = 0; pp_signs=[]
for cone in (+1,-1):
    E = k  # hbar vf =1 so E ~ k
    d0  = D(cone,k,0.0,p,'px','0')
    d90 = D(cone,k,np.pi/2,p,'px','0')
    got = (d0-d90)/(d0+d90)
    num = 2*(v0 - cone*E*u1)*(E*w1)
    den = (v0 - cone*E*u1)**2 + E**2*w1**2
    pred = -cone*num/den
    err_pp = max(err_pp, abs(got-pred))
    pp_signs.append(np.sign(got))
report['Ppx_Eq10_maxabs_err'] = float(err_pp)
# upper (cone+): tangential -> Ppx(+)<0 ; lower (cone-): radial -> Ppx(-)>0
report['Ppx_upper_tangential(neg)'] = bool(pp_signs[0] < 0)
report['Ppx_lower_radial(pos)']     = bool(pp_signs[1] > 0)

# ---- normalization sanity ----
report['norm_Phi_upper'] = float(np.real(np.vdot(Phi(+1,k,0.3,p),Phi(+1,k,0.3,p))))

for kk,vv in report.items():
    print(f"{kk:45s}: {vv}")

os.makedirs(os.path.dirname(os.path.abspath(__file__)), exist_ok=True)
out = os.path.join(os.path.dirname(os.path.abspath(__file__)),'zhang2012_checks.json')
json.dump(report, open(out,'w'), indent=2)
print("\nwrote", out)
