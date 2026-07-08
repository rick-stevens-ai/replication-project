#!/usr/bin/env python3
"""Full replication driver for arXiv:1907.02359. Emits results.json + console log."""
import numpy as np, json, time
from scipy.optimize import minimize
from qaoa_core import (TWO_SAT_8A, MAXCUT_16, build_HC_diag, qaoa_state,
                       metrics, analytic_E_p1, is_triangle_free, apply_UB, apply_UC)

np.random.seed(20260702)
RESULTS = {"paper":"arXiv:1907.02359 Willsch et al. QIP 19,197(2020)","tests":{}}

def prep(inst):
    diag = build_HC_diag(inst)
    Emin = float(diag.min()); Emax = float(diag.max())
    gs_mask = np.isclose(diag, Emin)
    return diag, Emin, Emax, gs_mask

# ---------------------------------------------------------------------------
# TEST 1: analytic p=1 energy (Eq.19) vs exact statevector energy
# ---------------------------------------------------------------------------
def test_analytic(name, inst):
    diag, Emin, Emax, gs = prep(inst)
    N = inst["N"]
    maxerr = 0.0; samples=[]
    rng = np.random.default_rng(1)
    for _ in range(200):
        g = rng.uniform(0, 2*np.pi); b = rng.uniform(0, np.pi)
        st = qaoa_state(diag, N, [g], [b])
        E_num = float(np.sum(np.abs(st)**2 * diag))
        E_ana = float(analytic_E_p1(inst, g, b))
        err = abs(E_num - E_ana); maxerr = max(maxerr, err)
        if len(samples)<3: samples.append({"gamma":g,"beta":b,"E_num":E_num,"E_ana":E_ana})
    print(f"[T1 {name}] analytic Eq.19 vs statevector: max|dE|={maxerr:.3e} over 200 pts")
    RESULTS["tests"].setdefault("T1_analytic_p1",{})[name]={"max_abs_err":maxerr,"samples":samples}
    return maxerr

# ---------------------------------------------------------------------------
# TEST 2: QAOA optimization p=1..5, minimize energy E_p (practical setting,
#         as in Table 1); report success prob & ratio r. Layerwise INTERP init:
#         optimal (gamma,beta) from p-1 + append gamma_p=beta_p=0 (paper's recipe).
# ---------------------------------------------------------------------------
def cost_energy(params, diag, N, p):
    g = params[:p]; b = params[p:]
    st = qaoa_state(diag, N, g, b)
    return float(np.sum(np.abs(st)**2 * diag))

def cost_neg_succ(params, diag, N, p, gs):
    g = params[:p]; b = params[p:]
    st = qaoa_state(diag, N, g, b)
    return -float(np.sum(np.abs(st)[gs]**2))

def optimize_pchain(name, inst, pmax=5, restarts=20):
    diag, Emin, Emax, gs = prep(inst)
    N = inst["N"]
    rng = np.random.default_rng(7)
    prev = None
    rows = []
    for p in range(1, pmax+1):
        best = None
        # seed 1: interpolate from p-1
        seeds = []
        if prev is not None:
            g0 = np.concatenate([prev[0], [0.0]]); b0 = np.concatenate([prev[1], [0.0]])
            seeds.append(np.concatenate([g0, b0]))
        # random restarts
        for _ in range(restarts):
            g0 = rng.uniform(0, np.pi, p); b0 = rng.uniform(0, np.pi/2, p)
            seeds.append(np.concatenate([g0, b0]))
        for s in seeds:
            res = minimize(cost_energy, s, args=(diag,N,p), method="Nelder-Mead",
                           options={"maxiter":4000,"xatol":1e-6,"fatol":1e-8})
            if best is None or res.fun < best.fun:
                best = res
        g = best.x[:p]; b = best.x[p:]
        st = qaoa_state(diag, N, g, b)
        succ, E, r = metrics(st, diag, gs, Emin, Emax)
        rows.append({"p":p,"succ_pct":100*succ,"E":E,"r":r})
        prev = (g, b)
        print(f"[T2 {name}] p={p}: succ={100*succ:6.2f}%  E={E:8.4f}  r={r:.4f}")
    RESULTS["tests"].setdefault("T2_qaoa_energy_min",{})[name]=rows
    return rows

# ---------------------------------------------------------------------------
# TEST 3: linear annealing-schedule initialization at large p -> high success.
#   gamma_n = tau*(n-1/2)/p ; beta_n = -tau*(1-n/p) ; beta_p = -tau/(4p)  (Eqs.29-31)
#   Then Nelder-Mead refine minimizing energy. Reproduce "close to 1" claim.
# ---------------------------------------------------------------------------
def linear_anneal_params(p, tau):
    n = np.arange(1, p+1)
    gam = tau*(n-0.5)/p
    beta = -tau*(1 - n/p)
    beta[-1] = -tau/(4*p)
    return gam, beta

def test_linear_anneal(name, inst, p, tau):
    diag, Emin, Emax, gs = prep(inst)
    N = inst["N"]
    gam, beta = linear_anneal_params(p, tau)
    st = qaoa_state(diag, N, gam, beta)
    s0, E0, r0 = metrics(st, diag, gs, Emin, Emax)
    x0 = np.concatenate([gam, beta])
    res = minimize(cost_energy, x0, args=(diag,N,p), method="Nelder-Mead",
                   options={"maxiter":8000,"xatol":1e-7,"fatol":1e-9})
    g = res.x[:p]; b = res.x[p:]
    st2 = qaoa_state(diag, N, g, b)
    s1, E1, r1 = metrics(st2, diag, gs, Emin, Emax)
    print(f"[T3 {name}] p={p} tau={tau}: init succ={100*s0:.2f}% (E={E0:.3f}) "
          f"-> refined succ={100*s1:.2f}% (E={E1:.3f}, r={r1:.3f})")
    RESULTS["tests"].setdefault("T3_linear_anneal",{})[name]={
        "p":p,"tau":tau,"init":{"succ_pct":100*s0,"E":E0,"r":r0},
        "refined":{"succ_pct":100*s1,"E":E1,"r":r1}}
    return s1

# ---------------------------------------------------------------------------
if __name__ == "__main__":
    t0=time.time()
    print("="*70)
    print("TEST 1 — p=1 analytic energy (Eq.19) vs exact statevector")
    print("="*70)
    for nm,ins in [("2SAT-8A",TWO_SAT_8A),("MaxCut-16",MAXCUT_16)]:
        test_analytic(nm, ins)

    print("\n"+"="*70)
    print("TEST 2 — QAOA p=1..5, minimize E_p (Table 1 practical setting)")
    print("Paper Table 1: 2SAT-8(A) p1 succ=8.84% r=0.71 ; p5 succ=42.39% r=0.84")
    print("="*70)
    optimize_pchain("2SAT-8A", TWO_SAT_8A, pmax=5, restarts=30)
    print("Paper Fig.7: MaxCut-16 p=1 success prob < 2%")
    optimize_pchain("MaxCut-16", MAXCUT_16, pmax=5, restarts=20)

    print("\n"+"="*70)
    print("TEST 3 — linear-annealing init at large p -> near-unit success")
    print("Paper Fig.11: 2SAT-8(A) p=50 tau param -> succ ~82.7% -> ~1 after refine")
    print("Paper Fig.10: MaxCut-16 p=10 tau=1 -> succ ~85.6%")
    print("="*70)
    test_linear_anneal("2SAT-8A", TWO_SAT_8A, p=50, tau=8.0)
    test_linear_anneal("MaxCut-16", MAXCUT_16, p=10, tau=1.0)

    RESULTS["runtime_sec"]=time.time()-t0
    with open("results.json","w") as f: json.dump(RESULTS,f,indent=2)
    print(f"\nDONE in {RESULTS['runtime_sec']:.1f}s -> results.json")
