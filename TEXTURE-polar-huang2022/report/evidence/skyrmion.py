"""
Independent reimplementation of core physics of Huang 2022 (arXiv:2202.11348):
Ferroelectric control of skyrmions via DMI in Fe3GeTe2/In2Se3.

Discrete micromagnetic square lattice, energy terms: exchange + interfacial
(Neel) DMI + uniaxial anisotropy (+optional field). Overdamped LLG / projected
gradient descent relaxation of an initial circular domain.

We test the paper's central claim: switching DMI (proxy for FE polarization)
between D_up=0.28 mJ/m^2 and D_down=0.06 mJ/m^2 creates vs annihilates a
skyrmion, and measure the resulting skyrmion diameter (paper: ~12 nm bilayer).
"""
import numpy as np

# ---- micromagnetic parameters (SI) ----
A   = 1.0e-12      # exchange stiffness J/m (typical Fe3GeTe2 ~1 pJ/m)
K   = 0.04e6       # anisotropy J/m^3  (paper modeling value 0.04 MJ/m^3)
dx  = 1.0e-9       # cell size m (1 nm)
N   = 60           # 60 nm supercell -> 60 cells

def analytic_Dc():
    # spiral/skyrmion instability threshold (thin film): Dc = 4/pi sqrt(A K)
    return 4.0/np.pi*np.sqrt(A*K)

def init_domain(N, r0, chir=-1.0):
    """circular domain: -z inside radius r0 (core), +z outside; smooth wall.
    chir sets Neel handedness (radially out vs in) to match sign of D."""
    x = (np.arange(N)-N/2+0.5)
    X,Y = np.meshgrid(x,x,indexing='ij')
    R = np.sqrt(X**2+Y**2)*dx
    theta = np.pi*np.clip(1-(R/(r0)),0,1)  # theta=pi at center(-z), 0 far(+z)
    phi = np.arctan2(Y,X) + (0.0 if chir<0 else np.pi)  # Neel handedness
    m = np.zeros((N,N,3))
    m[...,0]=np.sin(theta)*np.cos(phi)
    m[...,1]=np.sin(theta)*np.sin(phi)
    m[...,2]=np.cos(theta)
    return m

def roll(m,ax,sh):
    return np.roll(m,sh,axis=ax)

def eff_field(m,D):
    """H_eff = -dE/dm  (up to common thickness factor; units arbitrary-consistent)."""
    # exchange: 2A/dx^2 * sum neighbors (Laplacian form)
    lap = (roll(m,0,1)+roll(m,0,-1)+roll(m,1,1)+roll(m,1,-1)-4*m)
    H = 2*A/dx**2 * lap  # exchange effective field density
    # anisotropy easy-axis z
    Ha = np.zeros_like(m); Ha[...,2]=2*K*m[...,2]
    H += Ha
    # interfacial Neel DMI, atomistic bond form E=sum D_ij.(mi x mj),
    # D_ij = d*(zhat x u_ij), d = D*dx.  Effective field density -> /dx^2 scaling.
    d = D*dx
    # neighbor spins
    mxp=roll(m,0,-1); mxm=roll(m,0,1); myp=roll(m,1,-1); mym=roll(m,1,1)
    # For +x bond D=+d*yhat; -x bond D=-d*yhat; +y bond D=-d*xhat; -y bond D=+d*xhat
    yhat=np.array([0,1.,0]); xhat=np.array([1.,0,0])
    Hd = ( np.cross(mxp, d*yhat) + np.cross(mxm,-d*yhat)
         + np.cross(myp,-d*xhat) + np.cross(mym, d*xhat) )
    H += Hd/dx**2
    return H

def energy(m,D):
    e_ex = A/dx**2*np.sum((roll(m,0,-1)-m)**2 + (roll(m,1,-1)-m)**2)
    e_an = -K*np.sum(m[...,2]**2)
    d=D*dx
    yhat=np.array([0,1.,0]); xhat=np.array([1.,0,0])
    e_d = np.sum(d*yhat*np.cross(m,roll(m,0,-1)) + (-d*xhat)*np.cross(m,roll(m,1,-1)))
    e_d = e_d/dx**2
    return (e_ex+e_an+e_d)*dx**3  # times volume element (thickness ~dx)

def relax(m,D,steps=4000,alpha=0.2):
    for it in range(steps):
        H=eff_field(m,D)
        # overdamped LLG: dm = -m x (m x H) = H - (m.H)m  (projected gradient)
        mdotH=np.sum(m*H,axis=-1,keepdims=True)
        dm = H - mdotH*m
        # normalize step size by field scale
        scale=alpha/(np.max(np.abs(H))+1e-30)
        m = m + scale*dm
        m /= np.linalg.norm(m,axis=-1,keepdims=True)+1e-30
    return m

def topo_charge(m):
    # Berg-Luscher-ish lattice topological charge (approx via solid angle sum)
    mxp=roll(m,0,-1); myp=roll(m,1,-1)
    q = np.sum(m*np.cross(mxp,myp))
    return q/(4*np.pi)

def sky_diameter(m):
    """diameter where m_z crosses 0 (domain wall), measured across center."""
    mz=m[...,2]
    if mz.min()>-0.3:   # no reversed core -> no skyrmion
        return 0.0
    # count cells with mz<0 -> area -> equivalent diameter
    area=np.sum(mz<0)*dx**2
    return 2*np.sqrt(area/np.pi)/1e-9  # nm

if __name__=="__main__":
    import json
    Dc=analytic_Dc()
    print(f"A={A*1e12:.2f} pJ/m  K={K/1e6:.3f} MJ/m^3  analytic Dc={Dc*1e3:.3f} mJ/m^2")
    cases={"D_up":0.28e-3,"D_down":0.06e-3,"D_upup":0.22e-3,"D_downdown":-0.24e-3}
    results={}
    for name,D in cases.items():
        m=init_domain(N,r0=8e-9,chir=np.sign(D) if D!=0 else -1.0)
        m=relax(m,D,steps=5000,alpha=0.3)
        diam=sky_diameter(m); Q=topo_charge(m)
        has=abs(Q)>0.5 and diam>1.0
        results[name]={"D_mJm2":D*1e3,"diameter_nm":round(diam,2),
                       "Q":round(Q,3),"skyrmion":bool(has)}
        print(f"{name:11s} D={D*1e3:+.2f} mJ/m^2  diam={diam:6.2f} nm  Q={Q:+.3f}  sky={has}")
    print("analytic Dc =",round(Dc*1e3,3),"mJ/m^2")
    json.dump({"Dc_mJm2":Dc*1e3,"cases":results},open("/home/stevens/work/_sim_out.json","w"),indent=2)
