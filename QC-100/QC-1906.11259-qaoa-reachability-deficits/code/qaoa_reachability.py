"""
QAOA reachability deficit replication for Akshay et al. 1906.11259.

Statevector simulation. For n=6 variables we work with 2^6=64 dimensional states.
We reproduce Figure 1 (top): random 3-SAT instances, MAX-3-SAT via QAOA with
standard X driver, sweeping clause density alpha = m/n, at fixed p depths.

The paper claim: f = E_QAOA - min(H_SAT) is ~0 for small alpha and rises
sharply once alpha crosses ~1, plateauing/growing at high alpha; higher p reduces f
but the growth pattern persists.

We use small p (much smaller than the paper's p=15,25,35 which the paper's own
Fig 1 uses) to keep CPU time bounded. That means our absolute f values will be
LARGER than the paper's for the same alpha; the qualitative TREND (monotonically
non-decreasing with alpha, deficit persists) is the falsifiable claim we test.
"""
from __future__ import annotations
import json
import time
import os
import random
from dataclasses import dataclass, asdict
from typing import List, Tuple
import numpy as np
from scipy.optimize import minimize

# --------------------------------------------------------------------------- #
# Basic n-qubit statevector helpers                                            #
# --------------------------------------------------------------------------- #

def basis_bits(n: int) -> np.ndarray:
    """Return (2**n, n) uint8 array, row x = bits of x (MSB is qubit 0)."""
    x = np.arange(2**n, dtype=np.uint32)
    bits = np.zeros((2**n, n), dtype=np.uint8)
    for i in range(n):
        # qubit i (i=0 = leftmost) -> bit position (n-1-i)
        bits[:, i] = (x >> (n - 1 - i)) & 1
    return bits

def plus_state(n: int) -> np.ndarray:
    N = 2**n
    return np.ones(N, dtype=np.complex128) / np.sqrt(N)

# --------------------------------------------------------------------------- #
# 3-SAT clause -> diagonal Hamiltonian                                         #
# --------------------------------------------------------------------------- #
# 3-SAT clause = 3 (variable index, negated?) tuples. Clause is UNSAT for the
# single assignment where each literal is False, i.e. variable=0 for a positive
# literal and variable=1 for a negative literal. Following the paper: each
# clause contributes a rank-1 projector penalizing exactly that unsat pattern
# with +1 energy. So H_SAT is diagonal with entry[x] = number of unsat clauses
# for assignment x. min(H_SAT) = 0 if satisfiable, >0 otherwise = min # unsat.

@dataclass
class Clause:
    vars: Tuple[int, int, int]
    negs: Tuple[bool, bool, bool]  # True = variable appears negated

def random_3sat_instance(n: int, m: int, rng: random.Random) -> List[Clause]:
    """m uniformly random 3-SAT clauses over n variables. Each clause samples
    3 distinct variables uniformly, then a uniform sign per literal."""
    out: List[Clause] = []
    for _ in range(m):
        vs = tuple(rng.sample(range(n), 3))
        ns = tuple(rng.random() < 0.5 for _ in range(3))
        out.append(Clause(vs, ns))  # type: ignore[arg-type]
    return out

def hsat_diagonal(instance: List[Clause], n: int, bits: np.ndarray) -> np.ndarray:
    """Return real diagonal H_SAT[x] = # unsatisfied clauses at assignment x."""
    N = 2**n
    diag = np.zeros(N, dtype=np.float64)
    for c in instance:
        v0, v1, v2 = c.vars
        n0, n1, n2 = c.negs
        b0 = bits[:, v0]; b1 = bits[:, v1]; b2 = bits[:, v2]
        # literal is False when: (positive literal AND bit=0) OR (negative AND bit=1)
        # i.e. lit_true = bit XOR negated? Actually:
        #   pos literal (neg=False), true iff bit=1 -> false iff bit=0
        #   neg literal (neg=True),  true iff bit=0 -> false iff bit=1
        # -> literal_false = (bit == 0) if not neg else (bit == 1)  == (bit != int(not neg))  == (bit XOR (1 - int(neg))) simpler: lit_false = (bit == int(not neg))
        # positive literal (neg=False): false when bit=0  -> bit == 0 == int(neg)
        # negative literal (neg=True):  false when bit=1  -> bit == 1 == int(neg)
        f0 = (b0 == int(n0))
        f1 = (b1 == int(n1))
        f2 = (b2 == int(n2))
        unsat = f0 & f1 & f2  # clause unsat iff all three literals false
        diag += unsat.astype(np.float64)
    return diag

# --------------------------------------------------------------------------- #
# QAOA with standard X-mixer driver                                            #
# --------------------------------------------------------------------------- #
# exp(-i * gamma * H_SAT) is diagonal -> just multiply
# exp(-i * beta * sum_i X_i) = product_i exp(-i beta X_i)
#   exp(-i beta X) = cos(beta) I - i sin(beta) X
# Apply single-qubit X-rotation to statevector in-place.

def apply_x_rotation_all(state: np.ndarray, beta: float, n: int) -> np.ndarray:
    """Apply exp(-i*beta*sum_j X_j) to state, in shape (2^n,) complex vector."""
    c = np.cos(beta)
    s = -1j * np.sin(beta)
    # reshape to (2, 2, ..., 2) with n axes
    st = state.reshape([2] * n)
    for j in range(n):
        # move axis j to front, apply 2x2 mixing, move back
        st = np.moveaxis(st, j, 0)
        new0 = c * st[0] + s * st[1]
        new1 = s * st[0] + c * st[1]
        st = np.stack([new0, new1], axis=0)
        st = np.moveaxis(st, 0, j)
    return st.reshape(-1)

def qaoa_energy(params: np.ndarray, diag: np.ndarray, n: int, p: int) -> float:
    """Compute <psi(gamma,beta)| H_SAT |psi(gamma,beta)>."""
    gammas = params[:p]
    betas = params[p:]
    psi = plus_state(n)
    for k in range(p):
        # apply exp(-i*gamma*H) (diagonal)
        psi = np.exp(-1j * gammas[k] * diag) * psi
        # apply mixer
        psi = apply_x_rotation_all(psi, betas[k], n)
    # expectation of diagonal Hamiltonian
    probs = np.abs(psi) ** 2
    return float(np.sum(probs * diag))

def optimize_qaoa(diag: np.ndarray, n: int, p: int, n_restarts: int = 5,
                  seed: int = 0) -> Tuple[float, np.ndarray]:
    """Optimize the QAOA energy over (gamma, beta) with n_restarts random starts."""
    rng = np.random.default_rng(seed)
    best_e = np.inf
    best_x = None
    for r in range(n_restarts):
        # gamma in [0, 2 pi) since H is integer-valued -> period 2 pi
        # beta in [0, pi) since X mixer has period pi
        g0 = rng.uniform(0.0, 2 * np.pi, size=p)
        b0 = rng.uniform(0.0, np.pi, size=p)
        x0 = np.concatenate([g0, b0])
        try:
            res = minimize(
                qaoa_energy,
                x0,
                args=(diag, n, p),
                method="COBYLA",
                options={"maxiter": 300, "rhobeg": 0.3},
            )
        except Exception:
            continue
        if res.fun < best_e:
            best_e = float(res.fun)
            best_x = res.x
    return best_e, best_x if best_x is not None else np.zeros(2 * p)

# --------------------------------------------------------------------------- #
# Sweep                                                                        #
# --------------------------------------------------------------------------- #

def run_sweep(
    n: int,
    alphas: List[float],
    ps: List[int],
    n_instances: int,
    n_restarts: int,
    seed: int,
    outfile: str,
) -> dict:
    """For each (p, alpha), run n_instances random 3-SAT instances, record
    f = E_QAOA - min(H_SAT) (mean, std) and average min(H_SAT)."""
    bits = basis_bits(n)
    rng = random.Random(seed)
    results = []
    t0 = time.time()
    for alpha in alphas:
        m = max(1, int(round(alpha * n)))
        # generate the same instances for all p (paired), for a fair alpha->p comparison
        instances = [random_3sat_instance(n, m, rng) for _ in range(n_instances)]
        diags = [hsat_diagonal(inst, n, bits) for inst in instances]
        min_es = [float(d.min()) for d in diags]
        for p in ps:
            fs = []
            eqs = []
            for i, d in enumerate(diags):
                e, _ = optimize_qaoa(
                    d, n, p, n_restarts=n_restarts, seed=seed + 1000 * p + i,
                )
                fs.append(e - min_es[i])
                eqs.append(e)
            row = dict(
                n=n,
                alpha=alpha,
                m=m,
                p=p,
                n_instances=n_instances,
                f_mean=float(np.mean(fs)),
                f_sem=float(np.std(fs, ddof=1) / np.sqrt(len(fs))) if len(fs) > 1 else 0.0,
                f_std=float(np.std(fs, ddof=1)) if len(fs) > 1 else 0.0,
                min_e_mean=float(np.mean(min_es)),
                e_qaoa_mean=float(np.mean(eqs)),
                fs=fs,
                min_es=min_es,
                elapsed_s=time.time() - t0,
            )
            results.append(row)
            print(f"[{time.time()-t0:6.1f}s] n={n} alpha={alpha:>4.2f} m={m:>2d} "
                  f"p={p:>2d} f_mean={row['f_mean']:.3f} f_sem={row['f_sem']:.3f} "
                  f"min_e_mean={row['min_e_mean']:.2f}")
    out = dict(
        paper="arXiv:1906.11259",
        figure="1 (top) analog: 3-SAT reachability deficit vs clause density",
        n=n,
        alphas=alphas,
        ps=ps,
        n_instances=n_instances,
        n_restarts=n_restarts,
        seed=seed,
        elapsed_s=time.time() - t0,
        results=results,
    )
    with open(outfile, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nWrote {outfile}   total {time.time()-t0:.1f}s")
    return out


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out_json = os.path.join(here, "..", "data", "qaoa_3sat_sweep.json")
    run_sweep(
        n=6,
        alphas=[0.5, 1.0, 2.0, 3.0, 5.0, 7.0, 10.0],
        ps=[1, 2, 4],
        n_instances=15,     # paper uses 100; we use 15 for CPU budget
        n_restarts=4,       # random restarts for COBYLA
        seed=20260703,
        outfile=out_json,
    )
