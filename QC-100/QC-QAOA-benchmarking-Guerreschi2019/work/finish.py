#!/usr/bin/env python3
"""Fast finisher: MaxCut p=5 (interp+few restarts) + T3 linear-annealing tests.
Also assembles the full results.json from all completed numbers."""
import numpy as np, json, time
from scipy.optimize import minimize
from qaoa_core import TWO_SAT_8A, MAXCUT_16, build_HC_diag, qaoa_state, metrics

def prep(inst):
    diag=build_HC_diag(inst); Emin=float(diag.min()); Emax=float(diag.max())
    gs=np.isclose(diag,Emin); return diag,Emin,Emax,gs

def cost_energy(params,diag,N,p):
    g=params[:p]; b=params[p:]; st=qaoa_state(diag,N,g,b)
    return float(np.sum(np.abs(st)**2*diag))

def linparams(p,tau):
    n=np.arange(1,p+1); gam=tau*(n-0.5)/p; beta=-tau*(1-n/p); beta[-1]=-tau/(4*p)
    return gam,beta

# ---- MaxCut p=5 continuation from p=4 optimum (rebuild p=4 fast, then extend) ----
def maxcut_p5():
    inst=MAXCUT_16; diag,Emin,Emax,gs=prep(inst); N=inst["N"]
    rng=np.random.default_rng(11)
    # quick p-chain 1..5 with interp + 3 restarts (enough for monotone)
    prev=None; row=None
    for p in range(1,6):
        best=None; seeds=[]
        if prev is not None:
            seeds.append(np.concatenate([np.append(prev[0],0.0),np.append(prev[1],0.0)]))
        for _ in range(3):
            seeds.append(np.concatenate([rng.uniform(0,np.pi,p),rng.uniform(0,np.pi/2,p)]))
        for s in seeds:
            r=minimize(cost_energy,s,args=(diag,N,p),method="Nelder-Mead",
                       options={"maxiter":3000,"xatol":1e-6,"fatol":1e-8})
            if best is None or r.fun<best.fun: best=r
        g=best.x[:p]; b=best.x[p:]; st=qaoa_state(diag,N,g,b)
        succ,E,r=metrics(st,diag,gs,Emin,Emax); prev=(g,b)
        row={"p":p,"succ_pct":100*succ,"E":E,"r":r}
        print(f"[MaxCut-16 fast] p={p}: succ={100*succ:6.2f}% E={E:8.4f} r={r:.4f}")
    return row

def t3(name,inst,p,tau,maxiter):
    diag,Emin,Emax,gs=prep(inst); N=inst["N"]
    gam,beta=linparams(p,tau); st=qaoa_state(diag,N,gam,beta)
    s0,E0,r0=metrics(st,diag,gs,Emin,Emax)
    x0=np.concatenate([gam,beta])
    res=minimize(cost_energy,x0,args=(diag,N,p),method="Nelder-Mead",
                 options={"maxiter":maxiter,"xatol":1e-6,"fatol":1e-8})
    g=res.x[:p]; b=res.x[p:]; st2=qaoa_state(diag,N,g,b)
    s1,E1,r1=metrics(st2,diag,gs,Emin,Emax)
    print(f"[T3 {name}] p={p} tau={tau}: init succ={100*s0:.2f}%(E={E0:.3f}) "
          f"-> refined succ={100*s1:.2f}%(E={E1:.3f},r={r1:.3f})")
    return {"p":p,"tau":tau,"init":{"succ_pct":100*s0,"E":E0,"r":r0},
            "refined":{"succ_pct":100*s1,"E":E1,"r":r1}}

if __name__=="__main__":
    t0=time.time()
    print("=== MaxCut p=5 fast finisher ===")
    mc5=maxcut_p5()
    print("\n=== T3 linear-annealing init at large p ===")
    # 8-qubit p=50: scan a couple of tau, keep best refined
    best8=None
    for tau in [6.0,8.0,10.0,12.0]:
        rr=t3("2SAT-8A",TWO_SAT_8A,50,tau,6000)
        if best8 is None or rr["refined"]["succ_pct"]>best8["refined"]["succ_pct"]: best8=rr
    mc10=t3("MaxCut-16",MAXCUT_16,10,1.0,3000)

    out={
      "T1_analytic_p1":{"2SAT-8A":4.441e-15,"MaxCut-16":6.217e-15,"note":"max|dE| Eq.19 vs statevector, 200 random (gamma,beta)"},
      "T2_qaoa_energy_min":{
        "2SAT-8A":[
          {"p":1,"succ_pct":8.84,"E":-4.3101,"r":0.7069},
          {"p":2,"succ_pct":17.39,"E":-5.3298,"r":0.7706},
          {"p":3,"succ_pct":28.49,"E":-5.9383,"r":0.8086},
          {"p":4,"succ_pct":37.73,"E":-6.2694,"r":0.8293},
          {"p":5,"succ_pct":41.03,"E":-6.4967,"r":0.8435}],
        "MaxCut-16":[
          {"p":1,"succ_pct":1.45,"E":-6.0564,"r":0.6711},
          {"p":2,"succ_pct":13.19,"E":-10.4481,"r":0.7951},
          {"p":3,"succ_pct":30.36,"E":-13.3183,"r":0.8762},
          {"p":4,"succ_pct":39.69,"E":-14.5044,"r":0.9097},
          mc5]},
      "T3_linear_anneal":{"2SAT-8A":best8,"MaxCut-16":mc10},
      "paper_targets":{
        "T2_2SAT8A":"Table1: p1 succ=8.84% r=0.71; p5 succ=42.39% r=0.84",
        "T2_MaxCut16":"Fig.7: p1 succ<2%",
        "T3_2SAT8A":"Fig.11: p=50 linear-anneal -> succ ~82.7% -> ~1 after refine",
        "T3_MaxCut16":"Fig.10: p=10 tau=1 -> succ ~85.6%",
        "instances":"E_C0(2SAT8A)=-9 (Fig.11), E_C0(MaxCut16)=-17.7 (Fig.10) -- both matched exactly"},
      "runtime_finisher_sec":time.time()-t0}
    json.dump(out,open("results.json","w"),indent=2)
    print(f"\nWROTE results.json in {time.time()-t0:.1f}s")
