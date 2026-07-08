"""
step5_response_diagram.py — Section 3.1 / Fig 12.

Build the response diagram z_inf vs wf for (alpha=0.05, gamma=-0.1).
The paper constructs this via the DETUNED slow-amplitude system: for each wf,
nu = wf - beta, integrate the slow (A,B) system to steady state and read off
the steady amplitude of the reconstructed solution
    z(t) ~ A(tau) C(that) + B(tau) S(that),
whose envelope magnitude scales with sqrt(A^2+B^2) * (peak of basis).

For each wf we run TWO initial conditions:
  - near origin (0.01,0.01)  -> finds the trivial (decay) branch
  - large       (0.3,0.3)    -> finds the large-amplitude branch if it exists
This reveals the bistable region and the bifurcation edges where the large
branch appears/disappears (paper: ~0.6375 and ~0.6405).

We use the same numerically-derived coefficient structure as step3/step4, but
recompute the resonant linear-coupling block as a function of wf via detuning
nu = wf - beta entering the slow system. To keep the construction faithful and
wf-dependent, we recompute the secondary-forcing projection at each wf.
"""
import sys, json
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, str(__file__.rsplit('/',1)[0]))
from mathieu_beta import solve_beta, compute_D_coeffs
from step3_slow_amplitudes import make_basis, proj

ROOT = __file__.rsplit('/',2)[0]

def derive_coeffs_wf(alpha, gamma, mu, delta, chi, wf, basis, N=2):
    """Derive slow coeffs with secondary forcing at frequency 2 wf (so the
    detuning nu = wf-beta is built in through the forcing projection)."""
    beta, D, that, C, S, dC, dS = basis
    cc_c, cc_s = proj(dC, that, beta); ds_c, ds_s = proj(dS, that, beta)
    Lmat = -2.0*np.array([[cc_c, ds_c],[cc_s, ds_s]])
    pref = -4.0*chi*(gamma + alpha*np.cos(2*that))
    f2w  = 4.0*delta*np.cos(2*wf*that)
    def P(f): return proj(f, that, beta)
    dampC=P(-mu*dC); dampS=P(-mu*dS); forcC=P(f2w*C); forcS=P(f2w*S)
    C3=P(pref*C**3); C2S=P(pref*3*C**2*S); CS2=P(pref*3*C*S**2); S3=P(pref*S**3)
    cos=dict(A=dampC[0]+forcC[0],B=dampS[0]+forcS[0],A3=C3[0],A2B=C2S[0],AB2=CS2[0],B3=S3[0])
    sin=dict(A=dampC[1]+forcC[1],B=dampS[1]+forcS[1],A3=C3[1],A2B=C2S[1],AB2=CS2[1],B3=S3[1])
    Linv=np.linalg.inv(Lmat); co={}
    for k in ['A','B','A3','A2B','AB2','B3']:
        co[k]=Linv@(-np.array([cos[k],sin[k]]))
    return dict(beta=beta,
        g_A=co['A'][0],g_B=co['B'][0],g_A3=co['A3'][0],g_A2B=co['A2B'][0],g_AB2=co['AB2'][0],g_B3=co['B3'][0],
        h_A=co['A'][1],h_B=co['B'][1],h_A3=co['A3'][1],h_A2B=co['A2B'][1],h_AB2=co['AB2'][1],h_B3=co['B3'][1])

def slow(tau,y,c):
    A,B=y
    dA=c['g_A3']*A**3+c['g_A2B']*A**2*B+c['g_AB2']*A*B**2+c['g_B3']*B**3+c['g_A']*A+c['g_B']*B
    dB=c['h_A3']*A**3+c['h_A2B']*A**2*B+c['h_AB2']*A*B**2+c['h_B3']*B**3+c['h_A']*A+c['h_B']*B
    return [dA,dB]

def steady_amp(c, ic, T=400):
    sol=solve_ivp(slow,(0,T),ic,args=(c,),rtol=1e-9,atol=1e-11,max_step=0.1)
    A,B=sol.y[:,-1]
    return np.hypot(A,B)

if __name__=="__main__":
    alpha,gamma=0.05,-0.1; mu=delta=chi=1.0
    beta=solve_beta(alpha,gamma)
    print(f"beta={beta:.6f}; sweeping wf around it")
    basis=make_basis(alpha,gamma,N=2)
    wfs=np.linspace(beta-0.08, beta+0.08, 81)
    low=[]; high=[]
    for wf in wfs:
        c=derive_coeffs_wf(alpha,gamma,mu,delta,chi,wf,basis)
        low.append(steady_amp(c,(0.01,0.01)))
        high.append(steady_amp(c,(0.5,0.5)))
    low=np.array(low); high=np.array(high)

    # bifurcation edges: where high-branch amplitude crosses a threshold
    thr=0.1*high.max() if high.max()>0 else 0.1
    big=high>thr
    edges=wfs[np.where(np.diff(big.astype(int))!=0)[0]]
    print("large-amplitude branch present for wf in:",
          f"[{wfs[big].min():.4f}, {wfs[big].max():.4f}]" if big.any() else "none")
    print("approx bifurcation edges (wf):", np.round(edges,4),
          " | paper quotes ~0.6375 and ~0.6405")

    fig,ax=plt.subplots(figsize=(7,5))
    ax.plot(wfs,high,'b-',lw=1.5,label='large-amp branch (IC large)')
    ax.plot(wfs,low,'g--',lw=1.2,label='trivial branch (IC ~0)')
    ax.axvline(beta,color='k',ls=':',alpha=0.5,label=f'wf=beta={beta:.4f}')
    for e in [0.6375,0.6405]: ax.axvline(e,color='r',ls='-.',alpha=0.4)
    ax.set_xlabel(r'$\omega_f$'); ax.set_ylabel(r'$z_\infty \sim \sqrt{A^2+B^2}$')
    ax.set_title('Fig 12 analog: response diagram (alpha=0.05, gamma=-0.1)')
    ax.legend(); ax.grid(alpha=0.3)
    fig.savefig(f"{ROOT}/figures/fig12_response_diagram.png",dpi=130,bbox_inches='tight')
    print("wrote figures/fig12_response_diagram.png")
    np.savetxt(f"{ROOT}/evidence/response_sweep.csv",
               np.column_stack([wfs,low,high]),delimiter=',',
               header='wf,trivial_branch,large_branch',comments='')
    json.dump({'beta':beta,'bifurcation_edges':list(map(float,edges)),
               'paper_edges':[0.6375,0.6405],
               'branch_range':[float(wfs[big].min()),float(wfs[big].max())] if big.any() else None},
              open(f"{ROOT}/evidence/response_diagram.json","w"),indent=2)
