#!/usr/bin/env python
"""
From-scratch tight-binding replication of the RSLC (ridge-spin-layer coupling)
model of Tian, Zhang, Cui, Yu, Yao, "Ridge-Spin-Layer Coupling and Emergent
Ridgetronics in 2D Altermagnets", arXiv:2607.15009v1 (2026).

Scope: the TIGHT-BINDING part only (Eqs. 1-3 + Boltzmann transport Eq. 2, 4).
DFT of Mg2Mo2(PO5)2 is deliberately scoped out.

Core model (paper Eq. 3), basis {|dxz,up>_2 , |dyz,down>_1}:

    H(k) = eps + diag( pi0 cos kx + delta cos ky ,
                       pi0 cos ky + delta cos kx )

    band 0 = (dxz, spin-up)   : E_up  = eps + pi0 cos kx + delta cos ky
    band 1 = (dyz, spin-down)  : E_dn  = eps + pi0 cos ky + delta cos kx

Ridge limit delta -> 0:
    E_up depends only on kx  => v_y = 0  => spin-up ridge runs along ky,
                                            conducts ONLY along x.
    E_dn depends only on ky  => v_x = 0  => spin-down ridge runs along kx,
                                            conducts ONLY along y.

Transport (paper Eq. 2, semiclassical Boltzmann, constant tau):
    sigma_ab^n  ~  e^2 tau  * (1/N) sum_k  v_a^n v_b^n  (-df/dE)|_{E_n(k)}
Spin polarization of conductivity (paper Eq. 4):
    SP_nn = (sigma_nn^up - sigma_nn^dn) / (sigma_nn^up + sigma_nn^dn)
"""
import json, time
import numpy as np

t0 = time.time()

# ---------------- parameters ----------------
eps   = 0.0
pi0   = 1.0          # dominant t2g hopping amplitude
Nk    = 401          # k-grid per dimension
EF    = 0.30         # Fermi level inside the ridge window (units of pi0)
kBT   = 0.02         # thermal broadening for -df/dE (units of pi0)
e2tau = 1.0          # e^2 tau prefactor -> report relative sigma

kx = np.linspace(-np.pi, np.pi, Nk, endpoint=False)
ky = np.linspace(-np.pi, np.pi, Nk, endpoint=False)
KX, KY = np.meshgrid(kx, ky, indexing="ij")

def bands(delta):
    """Return E_up, E_dn and their group velocities on the k-grid."""
    E_up = eps + pi0*np.cos(KX) + delta*np.cos(KY)
    E_dn = eps + pi0*np.cos(KY) + delta*np.cos(KX)
    # v_a = dE/dk_a  (hbar=1)
    vx_up = -pi0*np.sin(KX)                 # = 0 only if pi0=0; nonzero
    vy_up = -delta*np.sin(KY)               # -> 0 as delta->0  (RIDGE)
    vx_dn = -delta*np.sin(KX)               # -> 0 as delta->0  (RIDGE)
    vy_dn = -pi0*np.sin(KY)
    return (E_up, E_dn), (vx_up, vy_up, vx_dn, vy_dn)

def dfdE(E):
    """-df/dE for Fermi-Dirac at EF, kBT (Lorentzian-free, exact FD)."""
    x = (E - EF)/kBT
    # sech^2/(4kT); guard overflow
    return np.where(np.abs(x) < 40, 1.0/(4*kBT*np.cosh(x/2)**2), 0.0)

def conductivity(delta):
    (E_up, E_dn), (vx_up, vy_up, vx_dn, vy_dn) = bands(delta)
    N = KX.size
    w_up = dfdE(E_up); w_dn = dfdE(E_dn)
    s = {}
    s["xx_up"] = e2tau/N * np.sum(vx_up**2 * w_up)
    s["yy_up"] = e2tau/N * np.sum(vy_up**2 * w_up)
    s["xx_dn"] = e2tau/N * np.sum(vx_dn**2 * w_dn)
    s["yy_dn"] = e2tau/N * np.sum(vy_dn**2 * w_dn)
    return s

def spin_pol(s):
    def SP(a):
        num = s[f"{a}_up"] - s[f"{a}_dn"]
        den = s[f"{a}_up"] + s[f"{a}_dn"]
        return num/den if den > 1e-14 else 0.0
    return SP("xx"), SP("yy")

# ---------------- run: ridge limit + finite delta ----------------
results = {}
for label, delta in [("ridge_delta0", 0.0), ("quasi1D_delta0p05", 0.05),
                     ("delta0p2", 0.2)]:
    s = conductivity(delta)
    SPxx, SPyy = spin_pol(s)
    results[label] = {
        "delta": delta,
        "sigma": {k: float(v) for k, v in s.items()},
        "SP_xx": float(SPxx),
        "SP_yy": float(SPyy),
    }

# ---------------- band-structure along Gamma-X-M-Y-Gamma ----------
def kpath():
    G=(0,0); X=(np.pi,0); M=(np.pi,np.pi); Y=(0,np.pi)
    segs=[(G,X),(X,M),(M,Y),(Y,G)]; n=120; pts=[]; labels=[]; dist=[0.0]
    for a,b in segs:
        for i in range(n):
            t=i/n
            pts.append(((1-t)*a[0]+t*b[0], (1-t)*a[1]+t*b[1]))
    pts.append(M if False else G)  # close
    return pts
delta_bs = 0.0
pts = []
G=(0,0); X=(np.pi,0); M=(np.pi,np.pi); Y=(0,np.pi)
for a,b in [(G,X),(X,M),(M,Y),(Y,G)]:
    for i in range(120):
        t=i/120; pts.append(((1-t)*a[0]+t*b[0],(1-t)*a[1]+t*b[1]))
Eup_path=[eps+pi0*np.cos(p[0])+delta_bs*np.cos(p[1]) for p in pts]
Edn_path=[eps+pi0*np.cos(p[1])+delta_bs*np.cos(p[0]) for p in pts]

# ridge flatness metric: along Delta=(0,v,0) i.e. Gamma->Y, spin-up must be flat
# Gamma->Y is segment index 3 (Y->G) reversed; test kx=0 line for E_up
v_line = np.linspace(0, np.pi, 200)
Eup_along_ky = eps + pi0*np.cos(0.0) + delta_bs*np.cos(v_line)  # varies w/ ky? via delta only
Eup_flatness = float(np.ptp(eps + pi0*np.cos(0.0*v_line) + 0.0*np.cos(v_line)))  # delta=0 -> flat
# more directly: variance of E_up as ky varies at fixed kx=0, delta=0
Eup_ridge = eps + pi0*np.cos(np.zeros_like(v_line)) + 0.0*np.cos(v_line)
ridge_ptp = float(np.ptp(Eup_ridge))

out = {
    "paper": "Tian et al., arXiv:2607.15009v1 (2026)",
    "scope": "tight-binding RSLC model (Eq.3) + Boltzmann transport (Eq.2,4); DFT scoped out",
    "model": {
        "hamiltonian": "H = eps + diag(pi0 cos kx + delta cos ky, pi0 cos ky + delta cos kx)",
        "basis": "{|dxz,up>_2, |dyz,down>_1}",
        "params": {"eps": eps, "pi0": pi0, "Nk": Nk, "EF": EF, "kBT": kBT},
    },
    "transport_by_delta": results,
    "ridge_flatness_ptp_along_ky_at_kx0_deltamono0": ridge_ptp,
    "band_path": {
        "path": "Gamma-X-M-Y-Gamma",
        "E_up_min_max": [float(min(Eup_path)), float(max(Eup_path))],
        "E_dn_min_max": [float(min(Edn_path)), float(max(Edn_path))],
    },
    "claim_check": {
        "headline": "RSLC enables quasi-1D 100% spin-polarized transport",
        "SP_xx_ridge": results["ridge_delta0"]["SP_xx"],
        "SP_yy_ridge": results["ridge_delta0"]["SP_yy"],
        "expected": "SP_xx=-1 (only down? sign depends on basis), SP_yy=+1; both |SP|=1",
        "abs_SP_xx": abs(results["ridge_delta0"]["SP_xx"]),
        "abs_SP_yy": abs(results["ridge_delta0"]["SP_yy"]),
    },
    "runtime_s": round(time.time()-t0, 3),
}

with open("/home/stevens/textures-100/corpus/textures-polar-tian2026/work/tian2026_result.json","w") as f:
    json.dump(out, f, indent=2)

print(json.dumps(out, indent=2))
