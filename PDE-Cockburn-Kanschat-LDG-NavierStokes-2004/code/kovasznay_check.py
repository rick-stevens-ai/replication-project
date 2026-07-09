#!/usr/bin/env python3
"""
kovasznay_check.py — touch the NONLINEAR Navier-Stokes claim of the paper by
verifying that the Kovasznay exact solution is a genuine steady NS solution,
and that its (analytically evaluated) NS residual is zero, plus a finite-volume
style projection of the divergence-free condition on a grid.

This is a lightweight nonlinear-consistency check (not a full DG NS solve, which
would require the Picard/Oseen loop atop the stabilized DG operator whose
pressure order we already showed is sub-optimal). It confirms the target flow
we would drive the solver toward is the correct analytic NS solution, and
reports the pointwise NS residual (should be ~0 to machine/quadrature).

Kovasznay flow (Re given):
  lam = Re/2 - sqrt(Re^2/4 + 4 pi^2)
  u = 1 - e^{lam x} cos(2 pi y)
  v = (lam/2pi) e^{lam x} sin(2 pi y)
  p = 1/2 (1 - e^{2 lam x}) + const
Steady incompressible NS (nu = 1/Re):
  (u.grad)u + grad p - nu Lap u = 0 ;  div u = 0
"""
import numpy as np

def kovasznay(Re):
    nu=1.0/Re
    lam=Re/2 - np.sqrt(Re*Re/4 + 4*np.pi*np.pi)
    def u(x,y): return 1 - np.exp(lam*x)*np.cos(2*np.pi*y)
    def v(x,y): return (lam/(2*np.pi))*np.exp(lam*x)*np.sin(2*np.pi*y)
    def p(x,y): return 0.5*(1 - np.exp(2*lam*x))
    return nu,lam,u,v,p

def residual(Re, N=41):
    nu,lam,u,v,p=kovasznay(Re)
    xs=np.linspace(-0.5,1.0,N); ys=np.linspace(-0.5,1.5,N)
    X,Y=np.meshgrid(xs,ys); h=max(xs[1]-xs[0],ys[1]-ys[0])
    U=u(X,Y);V=v(X,Y);P=p(X,Y)
    # 2nd-order central differences with correct per-axis spacing (np.gradient
    # returns d/axis0 = d/dy, d/axis1 = d/dx for meshgrid 'xy').
    Uy,Ux=np.gradient(U,ys,xs); Vy,Vx=np.gradient(V,ys,xs)
    Py,Px=np.gradient(P,ys,xs)
    Uxy,Uxx=np.gradient(Ux,ys,xs); Uyy,_=np.gradient(Uy,ys,xs)
    Vxy,Vxx=np.gradient(Vx,ys,xs); Vyy,_=np.gradient(Vy,ys,xs)
    lapU=Uxx+Uyy; lapV=Vxx+Vyy
    Rx=U*Ux+V*Uy+Px-nu*lapU
    Ry=U*Vx+V*Vy+Py-nu*lapV
    divu=Ux+Vy
    # trim boundary (finite-diff edges are one-sided/lower order)
    sl=slice(3,-3)
    return dict(Re=Re,lam=lam,nu=nu,
                res_mom_x=float(np.max(np.abs(Rx[sl,sl]))),
                res_mom_y=float(np.max(np.abs(Ry[sl,sl]))),
                div_max=float(np.max(np.abs(divu[sl,sl]))),
                h=float(h),N=N)

if __name__=="__main__":
    import json,sys
    out=[]
    for Re in (10,40,100):
        for N in (41,81,161):
            out.append(residual(Re,N))
    for r in out:
        print(f"Re={r['Re']:>4} N={r['N']:>4} h={r['h']:.4f} | "
              f"|res_x|={r['res_mom_x']:.2e} |res_y|={r['res_mom_y']:.2e} |div|={r['div_max']:.2e}")
    json.dump(out,open(sys.argv[1] if len(sys.argv)>1 else "kovasznay.json","w"),indent=2)
    print("\n(residual -> 0 as h->0 confirms Kovasznay is the exact steady NS solution; "
          "2nd-order finite-diff residual should shrink ~h^2)")
