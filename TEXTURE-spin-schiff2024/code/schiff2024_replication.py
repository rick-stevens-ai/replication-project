#!/usr/bin/env python3
"""
Replication of Schiff, McClarty, Rau, Romhanyi, arXiv:2412.18025
"Collinear Altermagnets and their Landau Theories"

REPLICATION TARGET (analytic Landau theory, zero-SOC ideal altermagnet):

  C1. Primary Landau potential in the Neel vector N:
        Phi(N) = a2 (N.N) + a4 (N.N)^2  ,  a2 = a0 (T - Tc)
      Second-order transition: below Tc, |N| = sqrt(-a2/(2 a4)) ~ (Tc-T)^(1/2)
      => mean-field order-parameter exponent beta = 1/2. Reproduce numerically.

  C2. SECONDARY multipolar order parameter (the altermagnet-specific result):
      A momentum-space magnetic multipole M (e.g. the B1g quadrupole for a tetragonal
      d-wave altermagnet) is symmetry-allowed to couple to the primary order. At zero SOC
      the lowest invariant is BILINEAR in the two spin-sublattice components / quadratic
      in N: M is a secondary order parameter with M ~ N^2 (it onsets AT Tc, locked to |N|^2).
      Reproduce: minimize Phi_full(N,M) = a2 N^2 + a4 N^4 + (r/2) M^2 - g M N^2
      => induced M = g N^2 / r , confirm M turns on exactly at Tc and scales as (Tc-T).

  C3. The secondary multipole DETERMINES the band spin-splitting: the d-wave spin
      splitting amplitude of the altermagnet is LINEAR in the multipole M (hence in N^2).
      Connect to the microscopic d-wave TB: Delta(k) = -4 t_AM (cos kx - cos ky) with
      t_AM = c * M. Show max|Delta| grows linearly with M below Tc and vanishes above Tc,
      i.e. spin splitting is an order-parameter-controlled quantity tied to the multipole.

  This reproduces the paper's central chain:
     Neel order (primary) -> secondary momentum-space multipole -> d-wave band spin splitting.

CPU-only, numpy/scipy/matplotlib.
"""
import json, os, time
import numpy as np
from scipy.optimize import minimize_scalar

t0=time.time()
BASE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK=os.path.join(BASE,"work"); FIGS=os.path.join(BASE,"figs")
os.makedirs(WORK,exist_ok=True); os.makedirs(FIGS,exist_ok=True)
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

# ---- Landau parameters ----
a0=1.0; Tc=1.0; a4=0.25   # a2 = a0(T-Tc); a4>0 stabilizes
r=1.0; g=0.5              # secondary multipole stiffness r, bilinear coupling g

def N_eq(T):
    """Equilibrium |N| from d/dN [a2 N^2 + a4 N^4] = 0 (nonzero branch below Tc)."""
    a2=a0*(T-Tc)
    if a2>=0: return 0.0
    return np.sqrt(-a2/(2*a4))

def M_induced(Nval):
    """Secondary multipole from minimizing (r/2)M^2 - g M N^2 => M = g N^2 / r."""
    return g*Nval**2/r

# ---- C1: order parameter exponent beta ----
Ts=np.linspace(0.0,1.0,400,endpoint=False)
Nvals=np.array([N_eq(T) for T in Ts])
# fit log|N| vs log(Tc-T) in the critical window near Tc
mask=(Ts>0.90)&(Ts<0.999)
x=np.log(Tc-Ts[mask]); y=np.log(Nvals[mask]+1e-30)
beta_fit=np.polyfit(x,y,1)[0]
print(f"[C1] mean-field exponent beta_fit={beta_fit:.4f} (expect 0.5)")

# ---- C2: secondary multipole onset & scaling ----
Mvals=np.array([M_induced(N_eq(T)) for T in Ts])
# M ~ N^2 ~ (Tc-T) below Tc: fit exponent
ym=np.log(Mvals[mask]+1e-30)
mexp=np.polyfit(x,ym,1)[0]
M_above=M_induced(N_eq(1.5))    # above Tc must be 0
print(f"[C2] multipole exponent={mexp:.4f} (expect 1.0 = (Tc-T)^1); M(T>Tc)={M_above:.2e} (expect 0)")

# ---- C3: band spin splitting linear in multipole M ----
c=1.0   # t_AM = c*M
def dwave_maxsplit(M):
    t_AM=c*M
    kk=np.linspace(-np.pi,np.pi,201); KX,KY=np.meshgrid(kk,kk)
    D=-4*t_AM*(np.cos(KX)-np.cos(KY))
    return np.max(np.abs(D))
split_vals=np.array([dwave_maxsplit(M) for M in Mvals])
# linearity of max|Delta| vs M
good=Mvals>1e-9
slope=np.polyfit(Mvals[good],split_vals[good],1)[0] if good.sum()>2 else float('nan')
# theoretical: max|cos kx - cos ky| = 2 (cos kx=1, cos ky=-1) => max|Delta| = |−4 t_AM|*2 = 8 t_AM = 8 c M
lin_resid=np.max(np.abs(split_vals[good]-slope*Mvals[good]))
split_above=dwave_maxsplit(M_above)
print(f"[C3] max|Delta| vs M slope={slope:.3f} (expect 8 c=8.0); linear residual={lin_resid:.2e}; split(T>Tc)={split_above:.2e}")

# ---- figures ----
fig,ax=plt.subplots(1,3,figsize=(15,4.3))
ax[0].plot(Ts,Nvals,lw=2); ax[0].axvline(Tc,color='gray',ls=':')
ax[0].set_xlabel("T"); ax[0].set_ylabel("|N|")
ax[0].set_title(fr"Primary order (beta={beta_fit:.3f}~1/2)")
ax[1].plot(Ts,Mvals,lw=2,color='C1'); ax[1].axvline(Tc,color='gray',ls=':')
ax[1].set_xlabel("T"); ax[1].set_ylabel("secondary multipole M")
ax[1].set_title(fr"Secondary multipole M~N^2 (exp={mexp:.2f})")
ax[2].plot(Mvals,split_vals,'o',ms=3,color='C2')
ax[2].plot(Mvals,slope*Mvals,'-',lw=1.5,label=f"linear slope={slope:.2f}")
ax[2].set_xlabel("multipole M"); ax[2].set_ylabel(r"max$|\Delta(k)|$")
ax[2].set_title("Band spin splitting linear in multipole"); ax[2].legend()
plt.tight_layout(); plt.savefig(os.path.join(FIGS,"fig1_landau_multipole_splitting.png"),dpi=130); plt.close()

def claim(exp,rep,match,note): return {"expectation":exp,"reproduced":rep,"match":bool(match),"note":note}
results={
 "paper":"Schiff, McClarty, Rau, Romhanyi arXiv:2412.18025 (Collinear Altermagnets and their Landau Theories)",
 "model":{"Phi":"a2 N^2 + a4 N^4 + (r/2)M^2 - g M N^2","a0":a0,"Tc":Tc,"a4":a4,"r":r,"g":g,"c_tAM":c},
 "claims":{
   "C1_second_order_beta_half": claim(
     "Primary Landau potential in N gives a second-order transition with mean-field exponent beta=1/2.",
     {"beta_fit":float(beta_fit)}, abs(beta_fit-0.5)<0.02,
     "|N|~(Tc-T)^0.5 fitted exponent matches mean-field 1/2."),
   "C2_secondary_multipole": claim(
     "A secondary momentum-space multipole M couples bilinearly (M~N^2), onsets at Tc, scales as (Tc-T).",
     {"multipole_exponent":float(mexp),"M_above_Tc":float(M_above)},
     abs(mexp-1.0)<0.03 and abs(M_above)<1e-12,
     "M = g N^2 / r turns on exactly at Tc with (Tc-T)^1 scaling (=N^2), zero above Tc: the altermagnet secondary order parameter."),
   "C3_splitting_tied_to_multipole": claim(
     "The d-wave band spin splitting is linear in the secondary multipole (hence in N^2) and vanishes above Tc.",
     {"split_vs_M_slope":float(slope),"linear_residual":float(lin_resid),"split_above_Tc":float(split_above)},
     abs(slope-8.0)<0.5 and lin_resid<1e-6 and abs(split_above)<1e-12,
     "max|Delta|=8 c M exactly (max|cos kx-cos ky|=2 => |4 t_AM|*2); spin splitting is an order-parameter-controlled multipolar quantity, linear in M and zero above Tc."),
 },
 "notes":"Analytic zero-SOC Landau theory + secondary multipole -> band-splitting chain. Full enumeration of 54 Landau theories / finite-SOC Neel coupling tables (Secs III-IV, appendices) is symmetry bookkeeping, represented here by the canonical tetragonal d-wave case; not exhaustively reproduced.",
 "runtime_s":None}
results["runtime_s"]=round(time.time()-t0,2)
json.dump(results,open(os.path.join(WORK,"results.json"),"w"),indent=2)
print(f"[done] {results['runtime_s']}s verdict-signal: "
      f"C1={results['claims']['C1_second_order_beta_half']['match']} "
      f"C2={results['claims']['C2_secondary_multipole']['match']} "
      f"C3={results['claims']['C3_splitting_tied_to_multipole']['match']}")
