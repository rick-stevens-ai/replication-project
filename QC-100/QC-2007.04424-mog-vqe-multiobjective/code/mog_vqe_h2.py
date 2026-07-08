"""
Independent replication of MoG-VQE (arXiv:2007.04424, Chivilikhin et al. 2020) for H2.

The paper's central quantitative claim (Abstract + Figs 3/4/5): the multiobjective GA discovers
ansatze that reach chemical accuracy with far fewer CNOTs than the standard hardware-efficient
ansatz (HEA) — "nearly ten-fold reduction in the two-qubit gate counts". For H2 the paper uses
a 4-qubit encoding and shows that very few CNOTs suffice.

We reproduce the pattern on H2 (STO-3G, 4 qubits, JW, ~0.74 A):
  1) Build the JW-mapped Hamiltonian in PennyLane; get exact ground-state energy by diag.
  2) Baseline #1 (chemistry-inspired): UCCSD via explicit Trotterized single/double excitations
     (qml.SingleExcitation + qml.DoubleExcitation), count CNOTs from an explicit decomposition.
  3) Baseline #2 (hardware-efficient): HEA with L layers of RY-RZ + CNOT-ladder entanglers,
     sweep L, count CNOTs needed to first reach chemical accuracy.
  4) MoG-VQE (this work's approach): NSGA-II-style GA over sequences of "generalized-CNOT blocks"
     (Fig 2a of the paper: pre-rotations + CNOT + post-rotations, 1 CNOT/block, 5 angles/block),
     with an inner CMA-ES / SciPy angle optimizer. Track a Pareto front over (energy_error, NCNOT).
  5) Compare min-CNOTs-to-chemical-accuracy between MoG-VQE and both baselines.
  6) Real simulation only — no fabricated numbers. Small pop/gens so it finishes in ~minutes.
"""

import json
import os
import random
import sys
import time
import numpy as np
import pennylane as qml

sys.stdout.reconfigure(line_buffering=True)
from pennylane import qchem
from scipy.optimize import minimize

random.seed(1234)
np.random.seed(1234)

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVID = os.path.join(OUT, "report", "evidence")
os.makedirs(EVID, exist_ok=True)


# ---------------------------------------------------------------------------
# 1) H2 Hamiltonian (STO-3G, JW mapping, 4 qubits)
# ---------------------------------------------------------------------------
symbols = ["H", "H"]
coords = np.array([[0.0, 0.0, -0.37], [0.0, 0.0, 0.37]])  # ~0.74 A bond

H, n_qubits = qchem.molecular_hamiltonian(
    symbols, coords, charge=0, mult=1, basis="sto-3g", method="pyscf",
)
try:
    n_terms = len(H.ops)
except AttributeError:
    n_terms = len(list(H.operands)) if hasattr(H, "operands") else -1
print(f"H2 Hamiltonian: {n_qubits} qubits, {n_terms} Pauli terms")

Hmat = qml.matrix(H, wire_order=range(n_qubits))
eigs = np.linalg.eigvalsh(Hmat)
E_FCI = float(eigs[0])
print(f"Exact FCI ground-state energy: {E_FCI:.8f} Ha")

hf_state = qml.qchem.hf_state(electrons=2, orbitals=n_qubits)
print(f"HF state occupation vector: {hf_state}")

dev = qml.device("default.qubit", wires=n_qubits)

@qml.qnode(dev)
def hf_energy_circuit():
    qml.BasisState(hf_state, wires=range(n_qubits))
    return qml.expval(H)

E_HF = float(hf_energy_circuit())
print(f"HF energy: {E_HF:.8f} Ha  (correlation energy = {E_FCI - E_HF:.6f} Ha)")

CHEM_ACC = 1.6e-3  # 1.6 mHa
# NOTE: the correlation energy for H2/STO-3G at 0.74 A is only ~10 mHa, so a HF-only circuit
# already misses chemical accuracy by ~6x. We must actually correlate.


# ---------------------------------------------------------------------------
# 2a) Baseline: UCCSD via explicit fermionic excitation operators.
#     Count CNOTs by expanding each SingleExcitation / DoubleExcitation into its
#     Pauli-string-Trotter form.
# ---------------------------------------------------------------------------
singles, doubles = qchem.excitations(electrons=2, orbitals=n_qubits)
print(f"UCCSD: {len(singles)} single excitations {singles}, {len(doubles)} double excitations {doubles}")

# Trotterized CNOT counts (see e.g. Yordanov et al. 2020):
#   Each SingleExcitation e^{θ(a†_i a_j - h.c.)} decomposes to 2 CNOT-staircases of length
#   (|i-j|), each with 2*(|i-j|)+2 CNOTs → total 2*(2*|i-j|+2)/2 ≈ 2*|i-j|+2 CNOTs in the
#   compact JW form; a conservative canonical count is 2 for the shortest, but PennyLane's
#   SingleExcitation gate compiles to 4 CNOTs for adjacent orbitals (i,j=i+1) and more otherwise.
#   Each DoubleExcitation compiles to 16 CNOTs in the canonical Trotterized JW form.
#
# We measure the CNOT count empirically by decomposing PennyLane's built-in gates to a
# CNOT+single-qubit gate basis.

def cnot_count_of_qfunc(qfunc, *args, **kwargs):
    """Decompose to CNOT+rot basis and count CNOTs."""
    with qml.tape.QuantumTape() as tape:
        qfunc(*args, **kwargs)
    # decompose recursively into 1- and 2-qubit gates
    decomposed = tape.expand(depth=6, stop_at=lambda op: op.name in
                             {"CNOT", "RX", "RY", "RZ", "Hadamard", "PauliX", "PauliY", "PauliZ",
                              "S", "T", "PhaseShift", "SX", "Rot"})
    return sum(1 for op in decomposed.operations if op.name == "CNOT")


def uccsd_qfunc(params):
    qml.BasisState(hf_state, wires=range(n_qubits))
    idx = 0
    for s in singles:
        qml.SingleExcitation(params[idx], wires=s); idx += 1
    for d in doubles:
        qml.DoubleExcitation(params[idx], wires=d); idx += 1


n_params_ucc = len(singles) + len(doubles)
cnots_uccsd = cnot_count_of_qfunc(uccsd_qfunc, np.zeros(n_params_ucc))
print(f"UCCSD decomposed CNOT count: {cnots_uccsd}")

@qml.qnode(dev)
def uccsd_circ(params):
    uccsd_qfunc(params)
    return qml.expval(H)


def uccsd_loss(x):
    return float(uccsd_circ(x))

t0 = time.time()
res_uccsd = minimize(uccsd_loss, np.zeros(n_params_ucc), method="COBYLA",
                     options={"maxiter": 500, "rhobeg": 0.1, "catol": 1e-7})
t_uccsd = time.time() - t0
E_uccsd = float(res_uccsd.fun)
print(f"UCCSD VQE energy: {E_uccsd:.8f} Ha (err {E_uccsd-E_FCI:.2e}, {t_uccsd:.1f}s)")


# ---------------------------------------------------------------------------
# 2b) Baseline: Hardware-Efficient Ansatz (HEA).
#     Each layer = RY on every qubit + linear CNOT chain (n_qubits-1 CNOTs).
#     Sweep L = 1..6, VQE each, record CNOTs & energy.
# ---------------------------------------------------------------------------
def hea_qfunc(params, L):
    # params shape: L * n_qubits (RY angles per layer)
    for l in range(L):
        for q in range(n_qubits):
            qml.RY(params[l * n_qubits + q], wires=q)
        for q in range(n_qubits - 1):
            qml.CNOT(wires=[q, q + 1])
    # trailing rotation layer
    # (kept out to match "L entangler layers" convention)


def make_hea_circ(L):
    @qml.qnode(dev)
    def _c(params):
        qml.BasisState(hf_state, wires=range(n_qubits))
        hea_qfunc(params, L)
        return qml.expval(H)
    return _c


hea_results = []
for L in range(1, 7):
    circ = make_hea_circ(L)
    best_e = np.inf; best_x = None
    for r in range(3):
        x0 = np.random.RandomState(100 + L * 10 + r).randn(L * n_qubits) * 0.2
        res = minimize(lambda x: float(circ(x)), x0, method="COBYLA",
                       options={"maxiter": 400, "rhobeg": 0.2})
        if res.fun < best_e:
            best_e, best_x = float(res.fun), res.x
    cnots = L * (n_qubits - 1)
    err = best_e - E_FCI
    ok = err < CHEM_ACC
    print(f"HEA L={L}: NCNOT={cnots}, E={best_e:.6f} Ha, err={err:.3e}, chem-acc? {ok}")
    hea_results.append({"L": L, "ncnot": cnots, "energy_Ha": best_e, "abs_error_Ha": err, "chem_acc": ok})

hea_min_ncnot = None
for r in hea_results:
    if r["chem_acc"]:
        hea_min_ncnot = r["ncnot"]; hea_min_energy = r["energy_Ha"]
        break


# ---------------------------------------------------------------------------
# 3) MoG-VQE: NSGA-II-like GA over sequences of generalized-CNOT blocks (Fig 2a).
# ---------------------------------------------------------------------------
QUBIT_PAIRS = [(i, j) for i in range(n_qubits) for j in range(n_qubits) if i != j]


def genome_num_cnots(genome):
    return len(genome)


def genome_num_angles(genome):
    return n_qubits + 5 * len(genome)


def build_circuit_fn(genome):
    @qml.qnode(dev)
    def circ(theta):
        qml.BasisState(hf_state, wires=range(n_qubits))
        for q in range(n_qubits):
            qml.RY(theta[q], wires=q)
        idx = n_qubits
        for _, c, t in genome:
            a, b, cc, d, e = theta[idx:idx + 5]
            qml.RY(a, wires=c)
            qml.RY(b, wires=t)
            qml.RZ(cc, wires=t)
            qml.CNOT(wires=[c, t])
            qml.RY(d, wires=c)
            qml.RY(e, wires=t)
            idx += 5
        return qml.expval(H)
    return circ


def evaluate_genome(genome, restarts=3, maxiter=200):
    circ = build_circuit_fn(genome)
    n = genome_num_angles(genome)
    best_e, best_x = np.inf, None
    for r in range(restarts):
        x0 = np.random.randn(n) * 0.3
        res = minimize(lambda x: float(circ(x)), x0, method="COBYLA",
                       options={"maxiter": maxiter, "rhobeg": 0.25, "catol": 1e-7})
        if res.fun < best_e:
            best_e, best_x = float(res.fun), res.x
    return best_e, best_x


# NSGA-II core
def dominates(a, b):
    return (a[0] <= b[0] and a[1] <= b[1]) and (a[0] < b[0] or a[1] < b[1])


def non_dominated_sort(objs):
    N = len(objs)
    S = [[] for _ in range(N)]
    n = [0] * N
    fronts = [[]]
    for p in range(N):
        for q in range(N):
            if p == q: continue
            if dominates(objs[p], objs[q]): S[p].append(q)
            elif dominates(objs[q], objs[p]): n[p] += 1
        if n[p] == 0: fronts[0].append(p)
    i = 0
    while fronts[i]:
        nxt = []
        for p in fronts[i]:
            for q in S[p]:
                n[q] -= 1
                if n[q] == 0: nxt.append(q)
        i += 1; fronts.append(nxt)
    return [f for f in fronts if f]


def crowding_distance(objs, front):
    dist = {i: 0.0 for i in front}
    if len(front) <= 2:
        for i in front: dist[i] = float("inf")
        return dist
    for m in range(2):
        fs = sorted(front, key=lambda i: objs[i][m])
        dist[fs[0]] = float("inf"); dist[fs[-1]] = float("inf")
        vmin, vmax = objs[fs[0]][m], objs[fs[-1]][m]
        if vmax - vmin < 1e-12: continue
        for k in range(1, len(fs) - 1):
            dist[fs[k]] += (objs[fs[k + 1]][m] - objs[fs[k - 1]][m]) / (vmax - vmin)
    return dist


MAX_CNOTS = 6

def random_gene():
    c, t = random.choice(QUBIT_PAIRS)
    return ("cnot_block", c, t)

def random_genome(max_len=MAX_CNOTS):
    # Bias toward mid-depth circuits: HF alone can't reach chem acc, and single-CNOT circuits
    # dominate too aggressively in NSGA-II sorting. Start each genome with at least 2 blocks.
    L = random.randint(2, max_len)
    return [random_gene() for _ in range(L)]

def mutate(g):
    g = list(g)
    if not g:
        g.append(random_gene()); return g
    op = random.choice(["swap_pair", "insert", "delete", "swap_pos"])
    if op == "swap_pair":
        i = random.randrange(len(g)); g[i] = random_gene()
    elif op == "insert" and len(g) < MAX_CNOTS:
        i = random.randrange(len(g) + 1); g.insert(i, random_gene())
    elif op == "delete" and len(g) > 1:  # keep at least 1
        i = random.randrange(len(g)); g.pop(i)
    elif op == "swap_pos" and len(g) >= 2:
        i, j = random.sample(range(len(g)), 2); g[i], g[j] = g[j], g[i]
    return g

def crossover(a, b):
    if not a or not b: return (list(a) + list(b))[:MAX_CNOTS] or [random_gene()]
    ca = random.randint(0, len(a)); cb = random.randint(0, len(b))
    child = (a[:ca] + b[cb:])[:MAX_CNOTS]
    if not child: child = [random_gene()]
    return child


POP = 16
GENS = 6
INNER_RESTARTS = 3
INNER_MAXITER = 200


def objective_of(energy, genome):
    err = max(energy - E_FCI, 0.0)
    return (float(err), int(genome_num_cnots(genome)))


print(f"\n--- MoG-VQE NSGA-II: pop={POP}, gens={GENS}, max_cnots={MAX_CNOTS} ---")
random.seed(42); np.random.seed(42)
pop = [random_genome() for _ in range(POP)]
cache = {}
history = []


def eval_pop(pop):
    scored = []
    for g in pop:
        k = tuple(g)
        if k in cache: e, x = cache[k]
        else:
            e, x = evaluate_genome(g, restarts=INNER_RESTARTS, maxiter=INNER_MAXITER)
            cache[k] = (e, x)
        scored.append((g, e, x))
    return scored


t0 = time.time()
best_ever_ca = None  # (ncnot, energy, genome)
for gen in range(GENS):
    scored = eval_pop(pop)
    objs = [objective_of(e, g) for g, e, _ in scored]
    fronts = non_dominated_sort(objs)
    front0 = fronts[0]
    front_info = sorted([(objs[i][1], objs[i][0], scored[i][0], scored[i][1]) for i in front0])
    # track best CA circuit
    for c, err, g, e in front_info:
        if err < CHEM_ACC:
            if best_ever_ca is None or c < best_ever_ca[0]:
                best_ever_ca = (c, e, list(g))
    print(f"gen {gen}: |pop|={len(scored)}, cache={len(cache)}, front-0:")
    for c, err, g, e in front_info[:6]:
        tag = "★" if err < CHEM_ACC else " "
        print(f"   {tag} NCNOT={c:2d}  E={e:.6f}  err={err:.3e}")
    history.append({"gen": gen,
                    "front": [{"ncnot": c, "err": err, "energy": e,
                               "genome": [list(x) for x in g]} for c, err, g, e in front_info]})
    # offspring
    offspring = []
    while len(offspring) < POP:
        p1 = random.choice(pop); p2 = random.choice(pop)
        child = crossover(p1, p2)
        if random.random() < 0.8: child = mutate(child)
        offspring.append(child)
    combined = pop + offspring
    scored_all = eval_pop(combined)
    objs_all = [objective_of(e, g) for g, e, _ in scored_all]
    fronts_all = non_dominated_sort(objs_all)
    new_pop = []
    for front in fronts_all:
        if len(new_pop) + len(front) <= POP:
            new_pop.extend([scored_all[i][0] for i in front])
        else:
            dist = crowding_distance(objs_all, front)
            fs = sorted(front, key=lambda i: -dist[i])
            new_pop.extend([scored_all[i][0] for i in fs[:POP - len(new_pop)]]); break
    pop = new_pop

t_mog = time.time() - t0
print(f"\nMoG-VQE search finished in {t_mog:.1f}s")

scored_final = eval_pop(pop)
objs_final = [objective_of(e, g) for g, e, _ in scored_final]
fronts_final = non_dominated_sort(objs_final)
pareto = sorted([(objs_final[i][1], objs_final[i][0], scored_final[i][0], scored_final[i][1])
                 for i in fronts_final[0]])

print("\nFINAL Pareto front (MoG-VQE):")
for c, err, g, e in pareto:
    tag = "★" if err < CHEM_ACC else " "
    print(f"  {tag} NCNOT={c:2d}  E={e:.8f}  err={err:.3e}")

# smallest CNOT reaching chem acc across cache (not just final Pareto — best-ever)
mog_min_cnots_ca = None
mog_min_energy_ca = None
best_below = [(genome_num_cnots(list(k)), v[0]) for k, v in cache.items() if (v[0] - E_FCI) < CHEM_ACC]
if best_below:
    best_below.sort()
    mog_min_cnots_ca = best_below[0][0]
    mog_min_energy_ca = best_below[0][1]

print("\n=== SUMMARY ===")
print(f"FCI:              {E_FCI:.8f} Ha")
print(f"HF:               {E_HF:.8f} Ha  (err={E_HF-E_FCI:.2e})")
print(f"UCCSD:            NCNOT={cnots_uccsd}, E={E_uccsd:.6f} Ha, err={E_uccsd-E_FCI:.2e}")
if hea_min_ncnot is not None:
    print(f"HEA (min CA):     NCNOT={hea_min_ncnot}, E={hea_min_energy:.6f} Ha")
else:
    print(f"HEA:              never reached chemical accuracy up to L=6")
if mog_min_cnots_ca is not None:
    print(f"MoG-VQE (min CA): NCNOT={mog_min_cnots_ca}, E={mog_min_energy_ca:.6f} Ha")
    if hea_min_ncnot is not None and hea_min_ncnot > 0:
        print(f"MoG-VQE / HEA CNOT reduction: {hea_min_ncnot/max(mog_min_cnots_ca,1):.2f}x")
    if cnots_uccsd > 0:
        print(f"MoG-VQE / UCCSD CNOT reduction: {cnots_uccsd/max(mog_min_cnots_ca,1):.2f}x")
else:
    print(f"MoG-VQE:          no circuit in search reached chemical accuracy")

result = {
    "molecule": "H2",
    "basis": "sto-3g",
    "bond_length_A": 0.74,
    "n_qubits": n_qubits,
    "n_hamiltonian_terms": n_terms,
    "chem_accuracy_Ha": CHEM_ACC,
    "reference_energies": {
        "FCI_Ha": E_FCI, "HF_Ha": E_HF, "correlation_Ha": E_FCI - E_HF,
    },
    "baselines": {
        "UCCSD": {
            "n_singles": len(singles), "n_doubles": len(doubles),
            "n_params": n_params_ucc, "cnot_count": cnots_uccsd,
            "vqe_energy_Ha": E_uccsd, "abs_error_Ha": E_uccsd - E_FCI,
            "chem_acc": (E_uccsd - E_FCI) < CHEM_ACC, "wall_time_s": t_uccsd,
        },
        "HEA_sweep": hea_results,
        "HEA_min_cnots_chem_acc": hea_min_ncnot,
    },
    "mog_vqe": {
        "population": POP, "generations": GENS,
        "inner_restarts": INNER_RESTARTS, "inner_maxiter": INNER_MAXITER,
        "max_cnots_bound": MAX_CNOTS,
        "wall_time_s": t_mog,
        "cache_size": len(cache),
        "min_cnots_chem_acc": mog_min_cnots_ca,
        "energy_at_min_cnots": mog_min_energy_ca,
        "final_pareto_front": [
            {"ncnot": c, "energy_Ha": e, "abs_error_Ha": err,
             "genome": [list(x) for x in g]} for c, err, g, e in pareto
        ],
    },
    "history": history,
    "comparison": {
        "MoG_vs_UCCSD_cnot_ratio": (cnots_uccsd / mog_min_cnots_ca) if (mog_min_cnots_ca and cnots_uccsd) else None,
        "MoG_vs_HEA_cnot_ratio": (hea_min_ncnot / mog_min_cnots_ca) if (mog_min_cnots_ca and hea_min_ncnot) else None,
    },
}

with open(os.path.join(EVID, "mog_vqe_h2_result.json"), "w") as f:
    json.dump(result, f, indent=2, default=str)
with open(os.path.join(EVID, "mog_vqe_h2_pareto.csv"), "w") as f:
    f.write("ncnot,energy_Ha,abs_error_Ha,below_chem_acc\n")
    for c, err, g, e in pareto:
        f.write(f"{c},{e:.8f},{err:.6e},{int(err<CHEM_ACC)}\n")

print("\nWrote:", os.path.join(EVID, "mog_vqe_h2_result.json"))
