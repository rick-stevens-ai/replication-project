#!/usr/bin/env python3
"""
Independent replication of BOUT++ MMS advection verification (Sec 4.2, Fig 3).

Equation (12):  df/dt = -[phi, f] - H*dx^4 * grad_perp^4 f
Poisson bracket [phi,f] = dphi/dx df/dz - dphi/dz df/dx.

Manufactured solutions (eqs 13-14), 0<=x<=1, 0<=z<=2pi:
    f = cos(4x^2 + z) + sin(t) sin(3x + 2z)
    phi = sin(6x^2 - z)

We add a source S(x,z,t) so that f_M is an exact solution:
    S = df_M/dt + [phi, f_M] + H*dx^4 * grad_perp^4 f_M
Then the numerical scheme should reproduce f_M; the residual measures scheme error.

Paper claim (Fig 3), resolutions 16x16 -> 1024x1024, H=20:
    Arakawa            1.998
    1st-order upwind   0.993
    2nd-order central  2.005
    3rd-order WENO     2.019
All limited to ~2nd order because phi advection velocity and BCs are 2nd order.

We do NOT use BOUT++. We build the brackets from scratch with:
 - z periodic (FFT-free, use np.roll), x is bounded [0,1] with Dirichlet BCs from f_M.
Following the paper's setup: the schemes for the bracket differ; the x-derivatives of phi
are 2nd-order central (that's why WENO is capped at 2). We evaluate the *spatial residual*
convergence directly (semi-discrete) which is the cleanest MMS order-of-accuracy measure:
compute the discrete bracket B_h[phi,f_M] and compare to the exact bracket, refining dx.
This isolates the spatial truncation order of each advection stencil exactly as the paper's
order-of-accuracy test does.
"""
import numpy as np

TWOPI = 2*np.pi

def fM(x, z, t):
    return np.cos(4*x**2 + z) + np.sin(t)*np.sin(3*x + 2*z)

def phiM(x, z):
    return np.sin(6*x**2 - z)

# analytic derivatives for exact bracket
def dfdx(x, z, t):
    return -8*x*np.sin(4*x**2+z) + 3*np.sin(t)*np.cos(3*x+2*z)
def dfdz(x, z, t):
    return -np.sin(4*x**2+z) + 2*np.sin(t)*np.cos(3*x+2*z)
def dphidx(x, z):
    return 12*x*np.cos(6*x**2 - z)
def dphidz(x, z):
    return -np.cos(6*x**2 - z)

def exact_bracket(x, z, t):
    # [phi,f] = dphi/dx df/dz - dphi/dz df/dx
    return dphidx(x,z)*dfdz(x,z,t) - dphidz(x,z)*dfdx(x,z,t)

# ---- discrete derivative helpers ----
# z: periodic (uniform, spacing dz), use np.roll along axis=1
# x: bounded, uniform spacing dx, use one-sided/ghost from analytic at boundaries
def ddz_c2(A, dz):
    return (np.roll(A,-1,axis=1) - np.roll(A,1,axis=1))/(2*dz)
def ddx_c2(A, dx):
    d = np.zeros_like(A)
    d[1:-1,:] = (A[2:,:]-A[:-2,:])/(2*dx)
    # one-sided 2nd order at x boundaries
    d[0,:]  = (-3*A[0,:]+4*A[1,:]-A[2,:])/(2*dx)
    d[-1,:] = ( 3*A[-1,:]-4*A[-2,:]+A[-3,:])/(2*dx)
    return d

# ---- advection schemes for the Poisson bracket [phi,f] ----
# The advection velocity components from phi (via 2nd-order central):
#   vx = -dphi/dz  (advects in x),  vz = dphi/dx  (advects in z)
# so [phi,f] = dphi/dx * df/dz - dphi/dz * df/dx = vz*df/dz + vx*df/dx  ... equivalently
#   [phi,f] = -( vx*df/dx + vz*df/dz )? Careful: define transport form
#   [phi,f] = dphi/dx df/dz - dphi/dz df/dx
# Treat as advection of f by velocity u=(ux,uz) where the flux form is u.grad f with
#   ux = -dphi/dz, uz = dphi/dx  ->  u.grad f = ux df/dx + uz df/dz
#                                            = -dphi/dz df/dx + dphi/dx df/dz = [phi,f]. Good.

def velocities(X, Z, dx, dz):
    P = phiM(X, Z)
    ux = -ddz_c2(P, dz)   # -dphi/dz
    uz =  ddx_c2(P, dx)   #  dphi/dx
    return ux, uz

def bracket_central2(F, ux, uz, dx, dz):
    return ux*ddx_c2(F,dx) + uz*ddz_c2(F,dz)

def bracket_upwind1(F, ux, uz, dx, dz):
    # 1st-order upwind in each direction
    # x-direction (bounded): backward/forward diff based on sign of ux
    dFdx = np.zeros_like(F)
    fwd = (np.zeros_like(F)); 
    # interior
    Fxp = np.empty_like(F); Fxm = np.empty_like(F)
    Fxp[:-1,:] = (F[1:,:]-F[:-1,:])/dx   # forward
    Fxp[-1,:]  = (F[-1,:]-F[-2,:])/dx
    Fxm[1:,:]  = (F[1:,:]-F[:-1,:])/dx   # backward
    Fxm[0,:]   = (F[1,:]-F[0,:])/dx
    dFdx = np.where(ux>0, Fxm, Fxp)
    # z-direction (periodic)
    Fzp = (np.roll(F,-1,axis=1)-F)/dz
    Fzm = (F-np.roll(F,1,axis=1))/dz
    dFdz = np.where(uz>0, Fzm, Fzp)
    return ux*dFdx + uz*dFdz

def bracket_arakawa(F, P, dx, dz):
    # Arakawa (1966) 2nd-order energy/enstrophy-conserving Jacobian J(P,F)=[phi,f]
    # = P_x F_z - P_z F_x. Verified 2nd order on doubly-periodic domain
    # (arakawa_check.py). z periodic; x bounded -> x boundary rows (0,1,-2,-1)
    # replaced by 2nd-order central bracket (roll wraps x nonphysically otherwise).
    a = P; b = F
    ip = lambda A: np.roll(A, -1, axis=0)
    im = lambda A: np.roll(A,  1, axis=0)
    jp = lambda A: np.roll(A, -1, axis=1)
    jm = lambda A: np.roll(A,  1, axis=1)
    Jpp = ( (ip(a)-im(a))*(jp(b)-jm(b)) - (jp(a)-jm(a))*(ip(b)-im(b)) )
    Jpx = ( ip(a)*(jp(ip(b))-jm(ip(b))) - im(a)*(jp(im(b))-jm(im(b)))
          - jp(a)*(ip(jp(b))-im(jp(b))) + jm(a)*(ip(jm(b))-im(jm(b))) )
    Jxp = ( ip(jp(a))*(jp(b)-ip(b)) - im(jm(a))*(im(b)-jm(b))
          - im(jp(a))*(jp(b)-im(b)) + ip(jm(a))*(ip(b)-jm(b)) )
    J = (Jpp + Jpx + Jxp) / (12.0*dx*dz)
    Jarak = J.copy()
    ux = -ddz_c2(P, dz); uz = ddx_c2(P, dx)
    cen = ux*ddx_c2(F, dx) + uz*ddz_c2(F, dz)
    for r in (0, 1, -1, -2):
        Jarak[r, :] = cen[r, :]
    return Jarak

def weno3_flux_deriv(F, u, dx, axis, periodic):
    # 3rd-order WENO (Jiang-Shu) reconstruction of df/d(axis), upwinded by sign(u).
    # Two candidate 2nd-order derivatives blended by nonlinear smoothness weights;
    # reduces to 3rd order in smooth regions.
    def sh(A, s):
        return np.roll(A, -s, axis=axis)   # element i -> A[i+s]
    Fm2 = sh(F, -2); Fm1 = sh(F, -1); F0 = F; Fp1 = sh(F, 1); Fp2 = sh(F, 2)
    eps = 1e-6
    g0, g1 = 2.0/3.0, 1.0/3.0
    # positive wind (u>0): backward/left-biased
    d0p = (Fp1 - Fm1) / (2*dx)            # centered candidate
    d1p = (3*F0 - 4*Fm1 + Fm2) / (2*dx)   # backward-biased candidate
    b0p = (Fp1 - F0)**2
    b1p = (F0 - Fm1)**2
    a0p = g0/(eps+b0p)**2; a1p = g1/(eps+b1p)**2
    w0p = a0p/(a0p+a1p); w1p = a1p/(a0p+a1p)
    dpos = w0p*d0p + w1p*d1p
    # negative wind (u<0): forward/right-biased mirror
    d0n = (Fp1 - Fm1) / (2*dx)
    d1n = (-3*F0 + 4*Fp1 - Fp2) / (2*dx)
    b0n = (F0 - Fm1)**2
    b1n = (Fp1 - F0)**2
    a0n = g0/(eps+b0n)**2; a1n = g1/(eps+b1n)**2
    w0n = a0n/(a0n+a1n); w1n = a1n/(a0n+a1n)
    dneg = w0n*d0n + w1n*d1n
    d = np.where(u > 0, dpos, dneg)
    return d

def bracket_weno3(F, ux, uz, dx, dz):
    dFdx = weno3_flux_deriv(F, ux, dx, axis=0, periodic=False)
    dFdz = weno3_flux_deriv(F, uz, dz, axis=1, periodic=True)
    # fix x boundaries with one-sided 2nd order
    dFdx[0,:]  = (-3*F[0,:]+4*F[1,:]-F[2,:])/(2*dx)
    dFdx[-1,:] = ( 3*F[-1,:]-4*F[-2,:]+F[-3,:])/(2*dx)
    return ux*dFdx + uz*dFdz

def run_scheme(scheme, N, t=0.3):
    # grid: x in [0,1] with N points (Dirichlet), z in [0,2pi) periodic with N points
    x = np.linspace(0,1,N)
    dx = x[1]-x[0]
    z = np.linspace(0,TWOPI,N,endpoint=False)
    dz = z[1]-z[0]
    X, Z = np.meshgrid(x, z, indexing='ij')
    F = fM(X, Z, t)
    P = phiM(X, Z)
    ux, uz = velocities(X, Z, dx, dz)
    if scheme=='central2':
        B = bracket_central2(F, ux, uz, dx, dz)
    elif scheme=='upwind1':
        B = bracket_upwind1(F, ux, uz, dx, dz)
    elif scheme=='arakawa':
        B = bracket_arakawa(F, P, dx, dz)
    elif scheme=='weno3':
        B = bracket_weno3(F, ux, uz, dx, dz)
    else:
        raise ValueError(scheme)
    Bexact = exact_bracket(X, Z, t)
    err = B - Bexact
    # interior only (exclude x boundary rows where all schemes drop to 2nd/BC-limited)
    interior = err[2:-2, :]
    l2 = np.sqrt(np.mean(interior**2))
    linf = np.max(np.abs(interior))
    return dx, l2, linf

def convergence(scheme, paper_rate):
    Ns = [16,32,64,128,256,512,1024]
    dxs=[]; l2s=[]; linfs=[]
    for N in Ns:
        dx,l2,linf = run_scheme(scheme,N)
        dxs.append(dx); l2s.append(l2); linfs.append(linf)
    print(f"\n== {scheme} (paper l2 rate {paper_rate}) ==")
    print(f"{'N':>6}{'dx':>12}{'l2':>14}{'rate':>8}{'linf':>14}{'rate':>8}")
    l2rates=[]; linfrates=[]
    for i,N in enumerate(Ns):
        if i==0:
            print(f"{N:6d}{dxs[i]:12.4e}{l2s[i]:14.4e}{'--':>8}{linfs[i]:14.4e}{'--':>8}")
        else:
            r=np.log(l2s[i-1]/l2s[i])/np.log(dxs[i-1]/dxs[i])
            ri=np.log(linfs[i-1]/linfs[i])/np.log(dxs[i-1]/dxs[i])
            l2rates.append(r); linfrates.append(ri)
            print(f"{N:6d}{dxs[i]:12.4e}{l2s[i]:14.4e}{r:8.3f}{linfs[i]:14.4e}{ri:8.3f}")
    return l2rates[-1]

if __name__=="__main__":
    paper={'arakawa':1.998,'upwind1':0.993,'central2':2.005,'weno3':2.019}
    mine={}
    for s in ['arakawa','upwind1','central2','weno3']:
        mine[s]=convergence(s,paper[s])
    print("\n=== SUMMARY (finest-pair l2 rate: mine vs paper) ===")
    for s in ['arakawa','upwind1','central2','weno3']:
        print(f"  {s:10s}: mine={mine[s]:.3f}  paper={paper[s]:.3f}  diff={abs(mine[s]-paper[s]):.3f}")
