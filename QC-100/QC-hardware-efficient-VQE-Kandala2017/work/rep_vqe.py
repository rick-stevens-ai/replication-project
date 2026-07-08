#!/usr/bin/env python
"""
Independent replication of Kandala et al. 2017 (arXiv:1704.05018),
"Hardware-efficient VQE for small molecules and quantum magnets", Nature 549:242.

Reproducible core (noiseless statevector simulation):
 - Hardware-efficient ansatz: initial single-qubit Euler layer (Rz-Rx-Rz) then
   `depth` blocks of [entangler] + [single-qubit Euler layer]. Entangler = CNOT
   network (linear chain, or all-to-all for the paper's "all-to-all connectivity"
   critical-depth claim). This is the noiseless analog of the paper's
   cross-resonance U_ENT; on a noiseless simulator the entangling structure is
   exactly what the paper's own numerical simulations use.
 - Qubit encoding matches the paper: parity/spin-parity Z2 reduction removing
   exactly 2 qubits ("remove two qubits associated with the spin-parities"),
   giving H2->2q, LiH->4q, BeH2->6q, matching the paper's stated qubit counts.
 - Exact reference = min eigenvalue of the SAME (tapered) qubit Hamiltonian =
   the FCI energy in the chosen active space (the "exact curve" the paper plots).

Claims tested:
 C2: VQE converges to chemical accuracy (~0.0016 Ha) vs exact along dissoc curve.
 C3: critical depth to reach chem acc at the bond distance (paper: d=1,8,28 for
     H2,LiH,BeH2 on all-to-all connectivity) -- we probe depth dependence.
"""
import json, time, argparse
import numpy as np
import pennylane as qml
from pennylane import numpy as pnp

CHEM_ACC = 0.0016  # Hartree

MOL = {
    "H2":  dict(symbols=["H","H"], ae=None, ao=None, nelec=2,
                geom=lambda l: [[0,0,0],[0,0,l]], eq=0.735,
                curve=[0.4,0.5,0.6,0.735,0.9,1.1,1.3,1.6,2.0,2.5]),
    "LiH": dict(symbols=["Li","H"], ae=2, ao=3, nelec=2,
                geom=lambda l: [[0,0,0],[0,0,l]], eq=1.545,
                curve=[1.0,1.2,1.4,1.545,1.8,2.2,2.7,3.2]),
    "BeH2":dict(symbols=["Be","H","H"], ae=4, ao=4, nelec=4,
                geom=lambda l: [[0,0,-l],[0,0,0],[0,0,l]], eq=1.3,
                curve=[0.9,1.1,1.3,1.6,2.0,2.5]),
}

def build_H(mol, l):
    m = MOL[mol]
    H, nq = qml.qchem.molecular_hamiltonian(
        m["symbols"], np.array(m["geom"](l), float), basis="sto-3g",
        mapping="jordan_wigner", method="pyscf",
        active_electrons=m["ae"], active_orbitals=m["ao"])
    gens = qml.symmetry_generators(H)
    g2 = gens[:2]                       # remove exactly 2 qubits (spin parities)
    px = qml.paulix_ops(g2, nq)
    sec = qml.qchem.optimal_sector(H, g2, m["nelec"])
    Ht = qml.simplify(qml.taper(H, g2, px, sec))
    wires = sorted(set(Ht.wires))
    # remap wires to 0..k-1
    wmap = {w: i for i, w in enumerate(wires)}
    Ht = qml.map_wires(Ht, wmap)
    nqt = len(wires)
    return Ht, nqt, sec

def exact_gs(H, nq):
    Hmat = qml.matrix(H, wire_order=list(range(nq)))
    return float(np.min(np.linalg.eigvalsh(Hmat).real))

def hea(params, nq, depth, entangler="linear"):
    def euler(slot):
        for q in range(nq):
            qml.RZ(params[slot, q, 0], wires=q)
            qml.RX(params[slot, q, 1], wires=q)
            qml.RZ(params[slot, q, 2], wires=q)
    euler(0)
    for d in range(depth):
        if entangler == "all2all":
            for a in range(nq):
                for b in range(a+1, nq):
                    qml.CNOT(wires=[a, b])
        else:
            for q in range(nq-1):
                qml.CNOT(wires=[q, q+1])
        euler(d+1)

def run_vqe(H, nq, depth, entangler="linear", maxiter=500, restarts=4,
            stepsize=0.1, tol=1e-9):
    dev = qml.device("default.qubit", wires=nq)
    @qml.qnode(dev, diff_method="backprop")
    def cost(p):
        hea(p, nq, depth, entangler)
        return qml.expval(H)
    best_E, best_hist = np.inf, None
    for r in range(restarts):
        rng = np.random.default_rng(100+r)
        p = pnp.array(rng.normal(0, 0.1, size=(depth+1, nq, 3)), requires_grad=True)
        opt = qml.AdamOptimizer(stepsize=stepsize)
        prev, hist = None, []
        for it in range(maxiter):
            p, E = opt.step_and_cost(cost, p); E = float(E); hist.append(E)
            if prev is not None and abs(prev-E) < tol: break
            prev = E
        Ef = float(cost(p))
        if Ef < best_E: best_E, best_hist = Ef, hist
    return best_E, best_hist

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mol", required=True, choices=list(MOL))
    ap.add_argument("--depths", default=None)
    ap.add_argument("--curve", action="store_true")
    ap.add_argument("--depth", type=int, default=1)
    ap.add_argument("--entangler", default="linear", choices=["linear","all2all"])
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    m = MOL[args.mol]
    result = {"mol": args.mol, "chem_acc": CHEM_ACC, "entangler": args.entangler}

    if args.depths:
        depths = [int(x) for x in args.depths.split(",")]
        H, nq, sec = build_H(args.mol, m["eq"])
        Eex = exact_gs(H, nq)
        result.update(nqubits=nq, bond_A=m["eq"], E_exact_bond=Eex, depth_scan=[])
        for d in depths:
            t0=time.time(); Ev,hist=run_vqe(H,nq,d,args.entangler); err=Ev-Eex
            row=dict(depth=d,E_vqe=Ev,E_exact=Eex,err_Ha=err,
                     chem_acc=bool(abs(err)<CHEM_ACC),iters=len(hist),sec=round(time.time()-t0,1))
            result["depth_scan"].append(row)
            print(f"[{args.mol} depth {args.entangler}] d={d} nq={nq} E_vqe={Ev:.6f} exact={Eex:.6f} err={err:.2e} chemacc={row['chem_acc']} ({row['sec']}s)",flush=True)

    if args.curve:
        result.update(curve_depth=args.depth, curve=[])
        for l in m["curve"]:
            H,nq,sec=build_H(args.mol,l); Eex=exact_gs(H,nq)
            t0=time.time(); Ev,hist=run_vqe(H,nq,args.depth,args.entangler); err=Ev-Eex
            row=dict(bond_A=l,nqubits=nq,E_vqe=Ev,E_exact=Eex,err_Ha=err,
                     chem_acc=bool(abs(err)<CHEM_ACC),sec=round(time.time()-t0,1))
            result["curve"].append(row)
            print(f"[{args.mol} curve d={args.depth} {args.entangler}] l={l} nq={nq} E_vqe={Ev:.6f} exact={Eex:.6f} err={err:.2e} chemacc={row['chem_acc']} ({row['sec']}s)",flush=True)

    json.dump(result, open(args.out,"w"), indent=2)
    print("WROTE", args.out, flush=True)

if __name__ == "__main__":
    main()
