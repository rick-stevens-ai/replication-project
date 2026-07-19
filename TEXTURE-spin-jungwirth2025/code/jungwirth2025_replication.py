#!/usr/bin/env python3
"""
Replication of Jungwirth et al., arXiv:2508.09748 "Altermagnetic spintronics" (review)

REPLICATION TARGET: the review's Fig. 1 MODEL d-wave altermagnet spin-dependent currents.
We compute the linear-response (Drude/Boltzmann constant-tau) charge and spin currents on the
d-wave spin-split Fermi surfaces and reproduce the three signature spintronic claims:

  C1. Bias along x -> current spin-up polarized; bias along y -> current spin-DOWN polarized
      (the spin polarization of the electrical current REVERSES with bias direction, d-wave).
  C2. Bias along the in-plane DIAGONAL -> longitudinal current is spin-UNPOLARIZED, but the
      spin-up and spin-down currents are DEFLECTED by opposite transverse angles => a transverse
      PURE SPIN CURRENT (the non-relativistic spin-splitter effect, SSE).
  C3. Contrast controls: a ferromagnet current is spin-up polarized for ALL bias directions;
      a conventional AFM current is UNPOLARIZED for all bias directions.

Method: sigma^s_{ab} = (e^2 tau / V) sum_k v_a^s(k) v_b^s(k) (-df/dE) per spin s, evaluated on a
k-grid at fixed EF (constant-tau Boltzmann). Charge sigma = sigma^up+sigma^dn; spin conductivity
sigma^spin = sigma^up - sigma^dn. Current polarization P = j^spin / j^charge; transverse spin
current from the off-diagonal spin conductivity for a diagonal bias.

CPU-only, numpy.
"""
import json, os, time
import numpy as np

t0=time.time()
BASE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK=os.path.join(BASE,"work"); FIGS=os.path.join(BASE,"figs")
os.makedirs(WORK,exist_ok=True); os.makedirs(FIGS,exist_ok=True)
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

t=1.0; t_AM=0.6; EF=-1.0; kT=0.05
Nk=400; kk=np.linspace(-np.pi,np.pi,Nk,endpoint=False); KX,KY=np.meshgrid(kk,kk)

def E(kx,ky,s,tAM):   return -2*t*(np.cos(kx)+np.cos(ky)) - 2*s*tAM*(np.cos(kx)-np.cos(ky))
def vx(kx,ky,s,tAM):  return  2*t*np.sin(kx) + 2*s*tAM*np.sin(kx)   # dE/dkx
def vy(kx,ky,s,tAM):  return  2*t*np.sin(ky) - 2*s*tAM*np.sin(ky)   # dE/dky
def dfdE(en):         # -df/dE ~ delta(E-EF), thermal broadened
    x=(en-EF)/kT; return np.exp(x)/(kT*(1+np.exp(x))**2)

def sigma_tensor(s, tAM):
    """2x2 conductivity tensor for spin s (constant-tau=1, e=1, V=1)."""
    en=E(KX,KY,s,tAM); w=dfdE(en)
    Vx=vx(KX,KY,s,tAM); Vy=vy(KX,KY,s,tAM)
    sxx=np.sum(w*Vx*Vx); syy=np.sum(w*Vy*Vy); sxy=np.sum(w*Vx*Vy)
    return np.array([[sxx,sxy],[sxy,syy]])

def currents_for_bias(Edir, tAM):
    """Given unit bias direction Edir, return (j_up, j_dn) 2-vectors."""
    Eh=np.array(Edir,float); Eh/=np.linalg.norm(Eh)
    s_up=sigma_tensor(+1,tAM); s_dn=sigma_tensor(-1,tAM)
    return s_up@Eh, s_dn@Eh

def polarization_and_transverse(Edir, tAM):
    ju,jd=currents_for_bias(Edir,tAM)
    Eh=np.array(Edir,float); Eh/=np.linalg.norm(Eh)
    That=np.array([-Eh[1],Eh[0]])          # transverse unit vector
    jc=ju+jd; js=ju-jd                       # charge & spin current vectors
    jc_long=jc@Eh; js_long=js@Eh
    P_long = js_long/jc_long if abs(jc_long)>1e-12 else 0.0   # longitudinal current spin polarization
    js_trans = js@That                       # transverse spin current (SSE)
    jc_trans = jc@That
    return P_long, js_trans, jc_trans, jc_long

# ---- C1: bias along x vs y ----
Px,_,_,_ = polarization_and_transverse([1,0], t_AM)
Py,_,_,_ = polarization_and_transverse([0,1], t_AM)
print(f"[C1] P(bias||x)={Px:+.3f}  P(bias||y)={Py:+.3f}  (expect opposite signs => reverses)")

# ---- C2: diagonal bias => unpolarized longitudinal + transverse pure spin current ----
Pd, js_t, jc_t, jc_l = polarization_and_transverse([1,1], t_AM)
print(f"[C2] diagonal: P_long={Pd:+.3e} (expect ~0 unpolarized); transverse spin current js_T={js_t:+.3f} (expect !=0 SSE); transverse charge jc_T={jc_t:+.3e} (expect ~0)")

# ---- C3: FM (single spin) and AFM (t_AM=0) controls ----
# ferromagnet: exchange split rigidly (both directions spin-up dominated) -> model as global spin
def fm_polarization(Edir):
    # FM: up and down bands rigidly split by a k-independent exchange h => up FS larger for all dirs
    h=0.6
    def Efm(kx,ky,s): return -2*t*(np.cos(kx)+np.cos(ky)) - s*h
    def st(s):
        en=Efm(KX,KY,s); w=dfdE(en)
        Vx=2*t*np.sin(KX); Vy=2*t*np.sin(KY)
        return np.array([[np.sum(w*Vx*Vx),np.sum(w*Vx*Vy)],[np.sum(w*Vx*Vy),np.sum(w*Vy*Vy)]])
    Eh=np.array(Edir,float); Eh/=np.linalg.norm(Eh)
    ju=st(+1)@Eh; jd=st(-1)@Eh
    return ((ju-jd)@Eh)/((ju+jd)@Eh)
Pfm_x=fm_polarization([1,0]); Pfm_y=fm_polarization([0,1]); Pfm_d=fm_polarization([1,1])
# AFM: t_AM=0 => bands spin-degenerate => unpolarized all dirs
Pafm_x,_,_,_=polarization_and_transverse([1,0],0.0)
Pafm_d,_,_,_=polarization_and_transverse([1,1],0.0)
print(f"[C3] FM P: x={Pfm_x:+.3f} y={Pfm_y:+.3f} diag={Pfm_d:+.3f} (expect same sign all dirs)")
print(f"     AFM P: x={Pafm_x:+.3e} diag={Pafm_d:+.3e} (expect ~0 all dirs)")

# ---- figures ----
fig,ax=plt.subplots(1,2,figsize=(11,5))
# spin-split Fermi surfaces
ax[0].contour(KX,KY,E(KX,KY,+1,t_AM),levels=[EF],colors='red')
ax[0].contour(KX,KY,E(KX,KY,-1,t_AM),levels=[EF],colors='blue')
ax[0].set_title("d-wave altermagnet spin-split FS\nred=up blue=down"); ax[0].set_aspect('equal')
ax[0].set_xlabel("kx"); ax[0].set_ylabel("ky")
# polarization vs bias angle
angs=np.linspace(0,np.pi,91); Pang=[]
for a in angs:
    P,_,_,_=polarization_and_transverse([np.cos(a),np.sin(a)],t_AM); Pang.append(P)
ax[1].plot(np.degrees(angs),Pang,lw=2)
ax[1].axhline(0,color='gray',ls=':'); ax[1].axvline(45,color='green',ls=':',label='diagonal (unpol)')
ax[1].set_xlabel("bias angle from x (deg)"); ax[1].set_ylabel("current spin polarization P")
ax[1].set_title("Current polarization reverses x->y, zero at 45 deg (d-wave)"); ax[1].legend()
plt.tight_layout(); plt.savefig(os.path.join(FIGS,"fig1_spin_splitter_currents.png"),dpi=130); plt.close()

def claim(exp,rep,match,note): return {"expectation":exp,"reproduced":rep,"match":bool(match),"note":note}
results={
 "paper":"Jungwirth et al arXiv:2508.09748 (Altermagnetic spintronics)",
 "model":{"t":t,"t_AM":t_AM,"EF":EF,"method":"constant-tau Boltzmann sigma^s_ab on d-wave spin-split FS"},
 "claims":{
   "C1_polarization_reverses": claim(
     "Current spin polarization is spin-up for bias||x and reverses to spin-down for bias||y (d-wave).",
     {"P_bias_x":float(Px),"P_bias_y":float(Py)},
     Px>0.05 and Py<-0.05 and np.sign(Px)!=np.sign(Py),
     "P(x) and P(y) have opposite signs => the electrical-current spin polarization reverses with bias direction, following d-wave altermagnet symmetry."),
   "C2_spin_splitter_effect": claim(
     "Diagonal bias: longitudinal current spin-unpolarized, but a transverse PURE spin current appears (SSE).",
     {"P_long_diag":float(Pd),"transverse_spin_current":float(js_t),"transverse_charge_current":float(jc_t)},
     abs(Pd)<1e-3 and abs(js_t)>0.05 and abs(jc_t)<1e-3,
     "Diagonal bias gives ~0 longitudinal polarization but nonzero transverse spin current and ~0 transverse charge current => non-relativistic spin-splitter effect (transverse pure spin current)."),
   "C3_controls_FM_AFM": claim(
     "Ferromagnet: same-sign polarization for all bias directions; conventional AFM: unpolarized for all.",
     {"FM_Px":float(Pfm_x),"FM_Py":float(Pfm_y),"FM_diag":float(Pfm_d),"AFM_Px":float(Pafm_x),"AFM_diag":float(Pafm_d)},
     (np.sign(Pfm_x)==np.sign(Pfm_y)==np.sign(Pfm_d)) and abs(Pafm_x)<1e-3 and abs(Pafm_d)<1e-3,
     "FM keeps one polarization sign for every bias direction; AFM (t_AM=0) is spin-unpolarized for all directions — the two contrasts in the paper's Fig. 1."),
 },
 "notes":"Reproduces the review's Fig. 1 model d-wave altermagnet spintronic signatures (polarization reversal, spin-splitter effect, FM/AFM contrasts) via constant-tau Boltzmann transport. Material-specific TMR/AHE magnitudes + THz dynamics are review-level surveys, out of scope.",
 "runtime_s":None}
results["runtime_s"]=round(time.time()-t0,2)
json.dump(results,open(os.path.join(WORK,"results.json"),"w"),indent=2)
print(f"[done] {results['runtime_s']}s verdict-signal: "
      f"C1={results['claims']['C1_polarization_reverses']['match']} "
      f"C2={results['claims']['C2_spin_splitter_effect']['match']} "
      f"C3={results['claims']['C3_controls_FM_AFM']['match']}")
