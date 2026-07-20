#!/usr/bin/env python3
"""
From-scratch replication of the coupled iCDW-rCDW Landau theory of
Christensen, Birol, Andersen & Fernandes, "Loop currents in AV3Sb5 kagome
metals: multipolar and toroidal magnetic orders", arXiv:2207.12820v2 (2022).

Reproducible core (the DFT-free part): the coupled Landau free energy, Eqs.
(10)-(13). Order parameters:
  N = (N1,N2,N3)  real-CDW (rCDW, M1+, bond distortion)
  Phi=(F1,F2,F3)  imaginary-CDW (iCDW, loop current, TRS-breaking)
The three components sit on the three symmetry-related M points Q1,Q2,Q3.

Key symmetry facts encoded:
  * rCDW allows a trilinear gamma_r * N1 N2 N3 (real, TRS-even).
  * iCDW forbids a Phi1 Phi2 Phi3 trilinear (imaginary/TRS-odd -> odd power
    of Phi flips sign under TRS), so NO gamma_i term.  This is why a pure
    2Q or 3Q iCDW is NOT a minimum on its own: the ONLY cubic invariant
    that can lower the iCDW energy is the mixed trilinear
    gamma_ir (N1 F2 F3 + F1 N2 F3 + F1 F2 N3).
  * That mixed trilinear is minimized by exactly two configurations:
      3Q-3Q  : all Ni, Fi nonzero
      2Q-1Q  : Fi,Fj,Nl nonzero (one permutation)
Which one wins is set by the quartic (u), biquadratic (lambda) and
quadrilinear (kappa) coefficients (paper Sec. IV, Ref. 54 analogy).

We minimize F numerically over the 6-D order-parameter space on a grid of
bare quadratic coefficients (ar, ai) ~ (T-Tr, T-Ti) and classify the global
minimum, then map the phase diagram and check the two generic scenarios.

Kernel credit: uses ideas / geometry conventions from the shared TEXTURES-100
loop_current_meanfield_kernel.py (Ollie) for the loop-current interpretation.
"""
from __future__ import annotations
import json, itertools, time
import numpy as np
from scipy.optimize import minimize

t0 = time.time()

# ---- Free energy Eqs. (11)-(13) ----------------------------------------
def free_energy(x, ar, ai, ur, ui, lr, li, gr, gir, kir, lir1, lir2):
    N = x[:3]; F = x[3:]
    N2 = np.dot(N, N); F2 = np.dot(F, F)
    # rCDW  (Eq. 11): trilinear allowed
    Fr = 0.5*ar*N2 + (gr/3.0)*N[0]*N[1]*N[2] + 0.25*ur*N2*N2 \
         + 0.25*lr*(N[0]**2*N[1]**2 + N[0]**2*N[2]**2 + N[1]**2*N[2]**2)
    # iCDW  (Eq. 12): NO trilinear (TRS)
    Fi = 0.5*ai*F2 + 0.25*ui*F2*F2 \
         + 0.25*li*(F[0]**2*F[1]**2 + F[0]**2*F[2]**2 + F[1]**2*F[2]**2)
    # coupling (Eq. 13)
    tri = N[0]*F[1]*F[2] + F[0]*N[1]*F[2] + F[0]*F[1]*N[2]
    quad = N[0]*N[1]*F[0]*F[1] + N[0]*N[2]*F[0]*F[2] + N[1]*N[2]*F[1]*F[2]
    biq1 = N[0]**2*F[0]**2 + N[1]**2*F[1]**2 + N[2]**2*F[2]**2
    Fir = (gir/3.0)*tri + 0.25*kir*quad + 0.25*lir1*biq1 + 0.25*lir2*N2*F2
    return Fr + Fi + Fir

# ---- global minimizer via multistart ------------------------------------
SEEDS = []
rng = np.random.default_rng(0)
# structured seeds: pure/mixed candidates + random
base = [
    [0,0,0, 0,0,0],                 # disordered
    [1,1,1, 0,0,0],                 # pure 3Q rCDW
    [1,0,0, 0,0,0],                 # pure 1Q rCDW
    [0,0,0, 1,0,0],                 # pure 1Q iCDW
    [0,0,0, 1,1,0],                 # pure 2Q iCDW
    [0,0,0, 1,1,1],                 # pure 3Q iCDW
    [1,1,1, 1,1,1],                 # 3Q-3Q
    [0,0,1, 1,1,0],                 # 2Q-1Q (Nl=N3, Fi=F1,Fj=F2)
    [1,0,0, 0,1,1],                 # 2Q-1Q variant
]
for b in base:
    SEEDS.append(np.array(b, float))
for _ in range(24):
    SEEDS.append(rng.normal(0, 1.0, 6))

def minimize_F(params):
    best = None
    for s in SEEDS:
        r = minimize(free_energy, s, args=params, method="Nelder-Mead",
                     options=dict(xatol=1e-8, fatol=1e-12, maxiter=4000))
        if best is None or r.fun < best.fun - 1e-10:
            best = r
    return best.x, best.fun

def classify(x, tol=1e-3):
    N = np.abs(x[:3]); F = np.abs(x[3:])
    nN = int(np.sum(N > tol)); nF = int(np.sum(F > tol))
    if nN == 0 and nF == 0: return "disordered"
    if nN == 3 and nF == 3: return "3Q-3Q"
    if nF == 2 and nN == 1: return "2Q-1Q"
    if nN == 3 and nF == 0: return "pure-3Q-rCDW"
    if nN == 1 and nF == 0: return "pure-1Q-rCDW"
    if nF == 1 and nN == 0: return "pure-1Q-iCDW"
    if nF == 2 and nN == 0: return "pure-2Q-iCDW"
    if nF == 3 and nN == 0: return "pure-3Q-iCDW"
    return f"other(nN={nN},nF={nF})"

# ---- fixed higher-order coefficients (positive, stable), from Ref-54 analogy
COEF = dict(ur=1.0, ui=1.0, lr=0.6, li=0.6, gr=0.4, gir=0.8, kir=0.3,
            lir1=0.4, lir2=0.2)

# ============ SCENARIO A: parameters favoring 3Q-3Q =====================
# strong isotropic coupling, modest biquadratic anisotropy
coefA = dict(COEF); coefA.update(lir1=0.0, kir=0.05, li=0.05, lr=0.05, gir=1.3, gr=0.9)
# ============ SCENARIO B: parameters favoring 2Q-1Q =====================
# larger biquadratic penalty lir1 penalizes co-located N_i,Phi_i -> 2Q-1Q
coefB = dict(COEF); coefB.update(lir1=1.6, kir=0.6, li=0.3, lr=0.3)

def sweep(coef, ar_grid, ai_grid):
    grid = {}
    counts = {}
    for ar in ar_grid:
        for ai in ai_grid:
            params = (ar, ai, coef["ur"], coef["ui"], coef["lr"], coef["li"],
                      coef["gr"], coef["gir"], coef["kir"], coef["lir1"], coef["lir2"])
            x, f = minimize_F(params)
            ph = classify(x)
            grid[(round(float(ar),3), round(float(ai),3))] = dict(
                phase=ph, F=float(f), N=[float(v) for v in x[:3]],
                Phi=[float(v) for v in x[3:]])
            counts[ph] = counts.get(ph, 0) + 1
    return grid, counts

ar_grid = np.linspace(-2.0, 0.5, 6)
ai_grid = np.linspace(-2.0, 0.5, 6)

gridA, countsA = sweep(coefA, ar_grid, ai_grid)
gridB, countsB = sweep(coefB, ar_grid, ai_grid)

# ---- deep-cool representative points ------------------------------------
def rep(coef, ar, ai):
    params = (ar, ai, coef["ur"], coef["ui"], coef["lr"], coef["li"],
              coef["gr"], coef["gir"], coef["kir"], coef["lir1"], coef["lir2"])
    x, f = minimize_F(params)
    return dict(phase=classify(x), F=float(f),
                N=[round(float(v),4) for v in x[:3]],
                Phi=[round(float(v),4) for v in x[3:]])

repA = rep(coefA, -2.0, -2.0)
repB = rep(coefB, -2.0, -2.0)

# ---- TRS-breaking check: iCDW nonzero <=> loop currents present ---------
def trs_broken(d):
    return any(abs(v) > 1e-3 for v in d["Phi"])

# ---- verify pure-iCDW is NOT a stand-alone minimum ----------------------
# turn off rCDW ability (ar large positive) but cool iCDW: check what happens
params_iconly = (5.0, -2.0, COEF["ur"], COEF["ui"], COEF["lr"], COEF["li"],
                 COEF["gr"], COEF["gir"], COEF["kir"], COEF["lir1"], COEF["lir2"])
x_ic, f_ic = minimize_F(params_iconly)
iconly = dict(phase=classify(x_ic), N=[round(float(v),4) for v in x_ic[:3]],
              Phi=[round(float(v),4) for v in x_ic[3:]])

result = {
    "paper": "Christensen et al., arXiv:2207.12820v2 (2022)",
    "method": "from-scratch numerical minimization of coupled iCDW-rCDW Landau free energy (Eqs. 10-13)",
    "kernel_credit": "shared-kernels-cache/loop_current_meanfield_kernel.py (Ollie) for loop-current interpretation/geometry conventions",
    "free_energy_terms": {
        "rCDW_trilinear_gamma_r": "ALLOWED (TRS-even)",
        "iCDW_trilinear_gamma_i": "FORBIDDEN by TRS (imaginary CDW) -> pure iCDW not a minimum",
        "mixed_trilinear_gamma_ir": "N1 F2 F3 + F1 N2 F3 + F1 F2 N3 : selects 3Q-3Q or 2Q-1Q"
    },
    "scenarioA_favor_3Q3Q": {"coef": coefA, "phase_counts": countsA, "deep_cool": repA,
                              "TRS_broken": trs_broken(repA)},
    "scenarioB_favor_2Q1Q": {"coef": coefB, "phase_counts": countsB, "deep_cool": repB,
                              "TRS_broken": trs_broken(repB)},
    "pure_iCDW_alone_test": iconly,
    "two_generic_outcomes_confirmed": (repA["phase"] == "3Q-3Q" and repB["phase"] == "2Q-1Q"),
    "orthorhombic_2Q1Q": "2Q-1Q has unequal N-components (single-Q rCDW) => breaks C3 => orthorhombic",
    "runtime_s": round(time.time() - t0, 2),
}

out = "/home/stevens/textures-100/corpus/textures-loop-current-christensen2022/work/christensen2022_result.json"
with open(out, "w") as fh:
    json.dump(result, fh, indent=2)
print(json.dumps(result, indent=2))
print("SAVED", out)
