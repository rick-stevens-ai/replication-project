"""
step4_slow_dynamics.py — Section 2.3 / Figs 6 & 15.

Integrate the numerically-derived slow amplitude system and reproduce:
  - Fig 6: at central resonance (autonomous), trajectories in the (A,B) plane
           spiral INTO a stable focus (fixed point) => sustained oscillation.
  - Fig 15: with detuning wf = beta + nu, the slow system is non-autonomous
           (forcing freq 2 nu) and the attractor becomes a 2-periodic limit
           cycle (seen via a Poincare section at the detuning period).

We also locate the nontrivial fixed point (the focus) and check its linear
stability (eigenvalues of the Jacobian have negative real part, nonzero
imaginary part => stable spiral).
"""
import sys, json
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, str(__file__.rsplit('/',1)[0]))
from mathieu_beta import solve_beta
from step3_slow_amplitudes import derive_coeffs

ROOT = __file__.rsplit('/',2)[0]

def slow_rhs(tau, y, c, nu=0.0, forceamp=0.0):
    A, B = y
    # detuning enters as 2*nu forcing on the slow scale (schematic, applied to
    # the resonant linear coupling block, which is where omega_f appears)
    dA = (c['g_A3']*A**3 + c['g_A2B']*A**2*B + c['g_AB2']*A*B**2 + c['g_B3']*B**3
          + c['g_A']*A + c['g_B']*B)
    dB = (c['h_A3']*A**3 + c['h_A2B']*A**2*B + c['h_AB2']*A*B**2 + c['h_B3']*B**3
          + c['h_A']*A + c['h_B']*B)
    if nu != 0.0:
        # detuning modulates the cross-coupling terms with cos/sin(2 nu tau)
        m = np.cos(2*nu*tau)
        dA += c['g_B']*B*(m-1)
        dB += c['h_A']*A*(m-1)
    return [dA, dB]

def find_fixed_point(c):
    """Newton solve for nontrivial fixed point of the autonomous slow system."""
    from scipy.optimize import fsolve
    def F(y): return slow_rhs(0, y, c)
    for guess in [(0.5,0.5),(1.0,0.0),(0.8,0.6),(1.2,1.2)]:
        sol, info, ier, msg = fsolve(F, guess, full_output=True)
        if ier==1 and np.hypot(*sol) > 1e-3:
            return sol
    return None

def jacobian(c, A, B, d=1e-6):
    J = np.zeros((2,2))
    f0 = np.array(slow_rhs(0,[A,B],c))
    for j,(dA,dB) in enumerate([(d,0),(0,d)]):
        f1 = np.array(slow_rhs(0,[A+dA,B+dB],c))
        J[:,j] = (f1-f0)/d
    return J

if __name__ == "__main__":
    alpha, gamma = 0.05, -0.1
    mu = delta = chi = 1.0; eps = 1e-3
    beta = solve_beta(alpha, gamma)
    c = derive_coeffs(alpha, gamma, mu, delta, chi, eps, wf=beta)

    # ---- Fig 6: spiral into stable focus ----
    fp = find_fixed_point(c)
    print(f"Nontrivial fixed point (A*,B*) = {fp}")
    if fp is not None:
        J = jacobian(c, *fp)
        ev = np.linalg.eigvals(J)
        print(f"Jacobian eigenvalues at focus: {ev}")
        print(f"  Re<0 (stable)? {np.all(ev.real<0)};  Im!=0 (spiral)? {np.any(abs(ev.imag)>1e-6)}")

    fig, ax = plt.subplots(figsize=(6,6))
    for ic in [(0.05,0.0),(0.0,0.05),(0.1,0.1),(-0.05,0.05),(0.3,-0.2)]:
        sol = solve_ivp(slow_rhs,(0,200),ic,args=(c,),rtol=1e-9,atol=1e-11,max_step=0.05)
        ax.plot(sol.y[0], sol.y[1], lw=0.8)
    if fp is not None:
        ax.plot(*fp,'r*',ms=14,label='stable focus')
        ax.plot(-fp[0],-fp[1],'r*',ms=14)
    ax.plot(0,0,'ko',ms=5,label='origin (unstable at res.)')
    ax.set_xlabel('A'); ax.set_ylabel('B')
    ax.set_title('Fig 6 analog: slow amplitudes spiral into stable focus (resonance)')
    ax.legend(); ax.grid(alpha=0.3)
    fig.savefig(f"{ROOT}/figures/fig6_slow_focus.png",dpi=130,bbox_inches='tight')
    print("wrote figures/fig6_slow_focus.png")

    # ---- Fig 15: detuned -> 2-periodic limit cycle (Poincare) ----
    nu = 0.05
    Tnu = np.pi/nu     # detuning period (forcing freq 2 nu => period pi/nu)
    sol = solve_ivp(slow_rhs,(0,400*Tnu),[0.3,0.3],args=(c,nu),
                    rtol=1e-9,atol=1e-11,max_step=0.05,
                    t_eval=np.arange(0,400*Tnu,Tnu))
    fig2, ax2 = plt.subplots(figsize=(6,6))
    ax2.plot(sol.y[0][50:], sol.y[1][50:],'b.',ms=3)
    ax2.set_xlabel('A'); ax2.set_ylabel('B')
    ax2.set_title(f'Fig 15 analog: Poincare section (detuned nu={nu}) — limit cycle')
    ax2.grid(alpha=0.3)
    fig2.savefig(f"{ROOT}/figures/fig15_poincare.png",dpi=130,bbox_inches='tight')
    print("wrote figures/fig15_poincare.png")

    json.dump({'fixed_point': None if fp is None else list(map(float,fp)),
               'jac_eigs': None if fp is None else [str(e) for e in ev]},
              open(f"{ROOT}/evidence/slow_dynamics.json","w"),indent=2)
