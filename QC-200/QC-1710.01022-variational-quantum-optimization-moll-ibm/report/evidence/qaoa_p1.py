"""
QAOA p=1 on random 3-regular graphs (n=6,8,10).
Real numpy statevector simulation.

Farhi-Goldstone-Gutmann 2014 baseline: QAOA p=1 achieves >= 0.6924 * MaxCut(G)
on 3-regular graphs (worst-case guarantee).

Method:
  - build random 3-regular graph G
  - classical brute-force MaxCut(G) over 2^n bit assignments
  - build cost Hamiltonian C_MaxCut (diagonal in Z basis)
  - build mixer B = sum_i X_i
  - trial state |psi(beta,gamma)> = e^{-i beta B} e^{-i gamma C} |+>^n
  - <psi|C|psi> minimized (i.e. -<C> maximized) via COBYLA
  - report r = <C>_opt / MaxCut

Independent replication for arXiv:1710.01022 (Moll et al., IBM 2017).
"""
import numpy as np
from scipy.optimize import minimize
import itertools, json, time, os, sys

rng = np.random.default_rng(20260705)

def random_3regular_graph(n, tries=200):
    """Build a random 3-regular graph on n vertices via the pairing (configuration) model."""
    assert n * 3 % 2 == 0, "n*3 must be even (i.e. n even) for a 3-regular graph"
    for _ in range(tries):
        stubs = list(range(n)) * 3
        rng.shuffle(stubs)
        edges = set()
        ok = True
        for i in range(0, len(stubs), 2):
            a, b = stubs[i], stubs[i+1]
            if a == b: ok = False; break                # self-loop
            e = (min(a,b), max(a,b))
            if e in edges: ok = False; break            # multi-edge
            edges.add(e)
        if ok:
            deg = [0]*n
            for u,v in edges: deg[u]+=1; deg[v]+=1
            if all(d == 3 for d in deg):
                return sorted(edges)
    raise RuntimeError("failed to sample 3-regular graph")

def brute_maxcut(n, edges):
    best = 0
    best_x = None
    for x in range(1 << n):
        cut = 0
        for u,v in edges:
            if ((x>>u)&1) != ((x>>v)&1): cut += 1
        if cut > best: best = cut; best_x = x
    return best, best_x

def cost_diag(n, edges):
    """Diagonal entries of C = sum_{(u,v)} (1 - Z_u Z_v)/2 in computational basis."""
    C = np.zeros(1 << n, dtype=np.float64)
    for x in range(1 << n):
        cut = 0
        for u,v in edges:
            if ((x>>u)&1) != ((x>>v)&1): cut += 1
        C[x] = cut
    return C

def apply_mixer(state, n, beta):
    """Apply e^{-i beta sum_i X_i}. Since X's commute, = prod_i e^{-i beta X_i}.
    Each single-qubit e^{-i beta X} = cos(beta) I - i sin(beta) X.
    We apply it per qubit by reshaping."""
    psi = state.copy()
    c, s = np.cos(beta), np.sin(beta)
    for q in range(n):
        # bring qubit q to first axis via reshape [(2^q), 2, (2^(n-q-1))]
        psi = psi.reshape(2**q, 2, 2**(n-q-1))
        a, b = psi[:,0,:].copy(), psi[:,1,:].copy()
        psi[:,0,:] = c*a - 1j*s*b
        psi[:,1,:] = c*b - 1j*s*a
        psi = psi.reshape(-1)
    return psi

def qaoa_expect(n, edges, C, beta, gamma):
    # start in |+>^n
    psi = np.ones(1 << n, dtype=np.complex128) / np.sqrt(1 << n)
    # apply e^{-i gamma C} (diagonal)
    psi = np.exp(-1j * gamma * C) * psi
    # apply e^{-i beta B}
    psi = apply_mixer(psi, n, beta)
    # <psi|C|psi> = sum_x C[x] |psi[x]|^2
    return float(np.sum(C * (psi.conj() * psi).real))

def qaoa_optimize(n, edges, C, restarts=40):
    def negC(theta):
        return -qaoa_expect(n, edges, C, theta[0], theta[1])
    best = None
    for k in range(restarts):
        # good starting range for QAOA: beta in (0, pi/2), gamma in (0, 2*pi) for MaxCut
        x0 = np.array([rng.uniform(0.05, np.pi/2 - 0.05),
                       rng.uniform(0.05, 2*np.pi - 0.05)])
        res = minimize(negC, x0, method="COBYLA", options={"maxiter": 300, "rhobeg": 0.2})
        val = -res.fun
        if (best is None) or (val > best["expC"]):
            best = {"expC": float(val), "beta": float(res.x[0]), "gamma": float(res.x[1])}
    return best

def main():
    out = {"paper": "arXiv:1710.01022", "sim": "numpy statevector",
           "baseline_ratio_FGG2014": 0.6924, "graphs": []}
    for n in [6, 8, 10]:
        t0 = time.time()
        edges = random_3regular_graph(n)
        maxcut, xstar = brute_maxcut(n, edges)
        C = cost_diag(n, edges)
        best = qaoa_optimize(n, edges, C, restarts=60)
        r = best["expC"] / maxcut
        entry = {
            "n": n,
            "edges": edges,
            "num_edges": len(edges),
            "maxcut_classical": maxcut,
            "best_bitstring": format(xstar, f"0{n}b"),
            "qaoa_p1": best,
            "approximation_ratio": r,
            "meets_FGG2014_bound": bool(r >= 0.6924),
            "elapsed_sec": round(time.time() - t0, 3),
        }
        out["graphs"].append(entry)
        print(f"n={n:2d}  |E|={len(edges):2d}  MaxCut={maxcut}  <C>_QAOA={best['expC']:.4f}  r={r:.4f}  meets_0.6924={r>=0.6924}")
    out["all_meet_bound"] = all(g["meets_FGG2014_bound"] for g in out["graphs"])
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "qaoa_p1_results.json"), "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nAll graphs meet FGG2014 bound (>=0.6924)? {out['all_meet_bound']}")

if __name__ == "__main__":
    main()
