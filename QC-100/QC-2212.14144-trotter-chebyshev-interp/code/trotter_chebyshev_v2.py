"""
Replication v2 of arXiv:2212.14144: use reflection symmetry (Ũ_s even in s)
per paper Sec 5 -- interpolate in u=s^2 with n Chebyshev-of-1st-kind nodes
on (0, s_max^2), giving a well-conditioned even interpolant to s=0.
Also produces the head-to-head cost plot analogous to paper Fig 5.
"""
from __future__ import annotations
import json, os
import numpy as np
from numpy.linalg import eigh
from scipy.linalg import expm, logm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

I2 = np.eye(2, dtype=complex)
X = np.array([[0,1],[1,0]], dtype=complex)
Z = np.array([[1,0],[0,-1]], dtype=complex)

def build_H(J=1.0, g=0.3):
    ZZ = np.kron(Z, Z); XI = np.kron(X, I2); IX = np.kron(I2, X)
    H1 = -J*ZZ; H2 = -J*g*(XI + IX); return H1+H2, H1, H2

def S2(H1,H2,t):
    A = expm(-1j*H1*t/2.0); B = expm(-1j*H2*t); return A@B@A

def S2k(H1,H2,t,k):
    if k==1: return S2(H1,H2,t)
    u = 1.0/(4.0 - 4.0**(1.0/(2*k-1)))
    inner1 = S2k(H1,H2,u*t,k-1)
    inner2 = S2k(H1,H2,(1-4*u)*t,k-1)
    return inner1@inner1@inner2@inner1@inner1

def U_tilde_frac(H1,H2,t,s,order=2):
    step = S2(H1,H2,s*t) if order==2 else S2k(H1,H2,s*t,2)
    return expm((1.0/s)*logm(step))

def E0_frac(H1,H2,t,s,order=2):
    U = U_tilde_frac(H1,H2,t,s,order=order)
    L = logm(U); Hs = 0.5*((1j*L/t)+(1j*L/t).conj().T)
    return float(eigh(Hs)[0][0])

def cheb_interp_at(x_nodes, y_nodes, x_query):
    """Barycentric Lagrange at Chebyshev-1st-kind nodes.
       Weights w_j = (-1)^j sin((2j+1) pi / (2n))  (Salzer's formula)."""
    n = len(x_nodes)
    j = np.arange(n)
    w = ((-1.0)**j) * np.sin((2*j+1)*np.pi/(2*n))
    for i in range(n):
        if np.isclose(x_query, x_nodes[i]):
            return y_nodes[i]
    d = w/(x_query - np.asarray(x_nodes))
    return float(np.sum(d*np.asarray(y_nodes))/np.sum(d))

def run():
    outdir = '/Users/stevens/Dropbox/REPLICATE-PROJECT/QC-100/QC-2212.14144-trotter-chebyshev-interp/report/evidence'
    os.makedirs(outdir, exist_ok=True)
    J,g,t = 1.0, 0.3, 1.0
    H,H1,H2 = build_H(J,g)
    E0_true = float(eigh(H)[0][0])
    print(f"E0_exact = {E0_true:.10f}")

    # -- Single S_2 and S_4 vs r
    rs = [1,2,3,4,6,8,12,16,24,32,48,64,96,128,192,256]
    single = []
    for r in rs:
        s = 1.0/r
        e2 = E0_frac(H1,H2,t,s,order=2)
        e4 = E0_frac(H1,H2,t,s,order=4)
        # cost: 3r S_2 exponentials; ~15r S_4 exponentials (5*3 per S_4 step)
        single.append(dict(r=r, s=s, err_S2=abs(e2-E0_true), err_S4=abs(e4-E0_true),
                           cost_S2=3*r, cost_S4=15*r))
        print(f"  r={r:4d}  err S_2={abs(e2-E0_true):.3e}  err S_4={abs(e4-E0_true):.3e}")

    # -- Chebyshev in u = s^2 (uses U_tilde is EVEN in s, per paper Sec 5)
    s_min, s_max = 1e-3, 1.0/3.0
    u_min, u_max = s_min**2, s_max**2
    cheb = []
    n_list = [2,3,4,5,6,7,8,9,10,12,14,16]
    print("\n-- Chebyshev in u=s^2, S_2 data --")
    for n in n_list:
        k = np.arange(n)
        # Chebyshev 1st-kind nodes on (-1,1)
        xk = np.cos(np.pi*(2*k+1)/(2*n))
        # map to (u_min, u_max)
        uk = 0.5*(u_max-u_min)*xk + 0.5*(u_max+u_min)
        sk = np.sqrt(uk)
        e2_nodes = np.array([E0_frac(H1,H2,t,s,order=2) for s in sk])
        e4_nodes = np.array([E0_frac(H1,H2,t,s,order=4) for s in sk])
        # Barycentric interp on the u-axis to u=0
        e2_at_0 = cheb_interp_at(uk, e2_nodes, 0.0)
        e4_at_0 = cheb_interp_at(uk, e4_nodes, 0.0)
        err2 = abs(e2_at_0 - E0_true)
        err4 = abs(e4_at_0 - E0_true)
        # cost: sum over nodes of r_k = 1/s_k, times 3 (S_2) or 15 (S_4) expms
        cost2 = float(3.0 * np.sum(1.0/sk))
        cost4 = float(15.0 * np.sum(1.0/sk))
        cheb.append(dict(n=n, sk=sk.tolist(), uk=uk.tolist(),
                         E2_at_0=e2_at_0, E4_at_0=e4_at_0,
                         err_S2=err2, err_S4=err4,
                         cost_S2=cost2, cost_S4=cost4))
        print(f"  n={n:2d}  err interp(S_2)={err2:.3e}  err interp(S_4)={err4:.3e}  "
              f"cost(S_2)={cost2:.1f}")

    # -- Save --
    with open(os.path.join(outdir,'results_v2.json'),'w') as f:
        json.dump(dict(paper='arXiv:2212.14144', E0_true=E0_true,
                       model=dict(J=J,g=g,t=t,H='-J(Z@Z + g(X@I+I@X))'),
                       single_trotter=single, cheb_interp=cheb), f, indent=2)

    # -- Plots (paper Fig 4/5 analogs) --
    fig, axes = plt.subplots(1, 2, figsize=(12,5))
    ax = axes[0]
    ax.loglog([row['r'] for row in single], [row['err_S2'] for row in single],
              'o-', label='Single Trotter S_2 (err vs 1/s)')
    ax.loglog([row['r'] for row in single], [row['err_S4'] for row in single],
              's-', label='Single Trotter S_4 (err vs 1/s)')
    # Chebyshev: plot err vs n on same axis using n on top? Use twiny.
    ax2 = ax.twiny()
    ax2.loglog([row['n'] for row in cheb], [row['err_S2'] for row in cheb],
               '^-', color='C2', label='Chebyshev on S_2 data (err vs n nodes)')
    ax2.set_xlabel('# Chebyshev interpolation nodes n')
    ax.set_xlabel('Trotter steps r = 1/s')
    ax.set_ylabel('|E0 estimate error|')
    ax.set_title('Paper Fig 4 analog: exact systematic error')
    ax.grid(True, which='both', alpha=0.3)
    ax.legend(loc='lower left'); ax2.legend(loc='upper right')

    ax = axes[1]
    ax.loglog([row['cost_S2'] for row in single], [row['err_S2'] for row in single],
              'o-', label='Single S_2 (cost = 3r)')
    ax.loglog([row['cost_S4'] for row in single], [row['err_S4'] for row in single],
              's-', label='Single S_4 (cost ~15r)')
    ax.loglog([row['cost_S2'] for row in cheb], [row['err_S2'] for row in cheb],
              '^-', label='Cheb+S_2 (cost = sum 3/s_k)')
    ax.set_xlabel('Cost (# Trotter exponentials)')
    ax.set_ylabel('|E0 estimate error|')
    ax.set_title('Paper Fig 5 analog: err vs cost')
    ax.grid(True, which='both', alpha=0.3)
    ax.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(outdir,'fig_scaling.png'), dpi=130)
    print(f"\nSaved: {outdir}/fig_scaling.png")
    print(f"Saved: {outdir}/results_v2.json")

    # -- Summary numbers for verdict --
    best_single_S2 = min(row['err_S2'] for row in single if row['cost_S2'] <= 100)
    best_cheb_S2   = min(row['err_S2'] for row in cheb if row['cost_S2'] <= 100)
    print(f"\nBest err S_2 alone at cost<=100: {best_single_S2:.3e}")
    print(f"Best err Cheb+S_2 at cost<=100: {best_cheb_S2:.3e}")
    print(f"Cheb advantage factor: {best_single_S2/best_cheb_S2:.1f}x")

if __name__=='__main__':
    run()
