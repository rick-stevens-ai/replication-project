#!/usr/bin/env python3
"""Standalone Arakawa Jacobian, carefully implemented and verified for 2nd order.
Convention: J(a,b) = a_x b_z - a_z b_x  (matches [phi,f]=phi_x f_z - phi_z f_x).
Arakawa (1966) J = (J++ + Jx+ + J+x)/3, each on a 12*dx*dz normalization.
Grid: x index i (axis 0), z index j (axis 1). We test on a doubly-periodic
manufactured field to isolate the stencil order (no boundary contamination).
"""
import numpy as np

def arakawa(a, b, dx, dz):
    # all shifts periodic (np.roll). axis0=x(i), axis1=z(j)
    ip = lambda A: np.roll(A,-1,axis=0)  # i+1
    im = lambda A: np.roll(A, 1,axis=0)  # i-1
    jp = lambda A: np.roll(A,-1,axis=1)  # j+1
    jm = lambda A: np.roll(A, 1,axis=1)  # j-1
    # Arakawa 1966, standard form (e.g. from many CFD texts)
    Jpp = ( (ip(a)-im(a))*(jp(b)-jm(b)) - (jp(a)-jm(a))*(ip(b)-im(b)) )
    Jpx = ( ip(a)*(jp(ip(b))-jm(ip(b))) - im(a)*(jp(im(b))-jm(im(b)))
          - jp(a)*(ip(jp(b))-im(jp(b))) + jm(a)*(ip(jm(b))-im(jm(b))) )
    Jxp = ( ip(jp(a))*(jp(b)-ip(b)) - im(jm(a))*(im(b)-jm(b))
          - im(jp(a))*(jp(b)-im(b)) + ip(jm(a))*(ip(b)-jm(b)) )
    return (Jpp + Jpx + Jxp) / (12.0*dx*dz)

# doubly periodic manufactured test: a=sin(x+2z), b=cos(2x - z) on [0,2pi]^2
def a_f(X,Z): return np.sin(X+2*Z)
def b_f(X,Z): return np.cos(2*X-Z)
def a_x(X,Z): return np.cos(X+2*Z)
def a_z(X,Z): return 2*np.cos(X+2*Z)
def b_x(X,Z): return -2*np.sin(2*X-Z)
def b_z(X,Z): return  np.sin(2*X-Z)
def J_exact(X,Z): return a_x(X,Z)*b_z(X,Z) - a_z(X,Z)*b_x(X,Z)

for N in [16,32,64,128,256]:
    x=np.linspace(0,2*np.pi,N,endpoint=False); dx=x[1]-x[0]
    z=np.linspace(0,2*np.pi,N,endpoint=False); dz=z[1]-z[0]
    X,Z=np.meshgrid(x,z,indexing='ij')
    Jn=arakawa(a_f(X,Z),b_f(X,Z),dx,dz)
    Je=J_exact(X,Z)
    l2=np.sqrt(np.mean((Jn-Je)**2))
    if N==16:
        print(f"N={N:4d} dx={dx:.4e} l2={l2:.4e}   rate=  --"); prev=(dx,l2)
    else:
        r=np.log(prev[1]/l2)/np.log(prev[0]/dx)
        print(f"N={N:4d} dx={dx:.4e} l2={l2:.4e}   rate={r:6.3f}"); prev=(dx,l2)
