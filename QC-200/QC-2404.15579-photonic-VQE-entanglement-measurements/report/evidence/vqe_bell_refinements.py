#!/usr/bin/env python3
"""Refinements to the main replication (arXiv:2404.15579):
  R1. HeH+ with the PAPER'S EXACT hand-picked GC grouping:
        {XX, ZZ, II}  {XI, XZ, IZ}  {IX, ZI, ZX}    (3 bases, per Appendix A).
      Verify (a) the grouping is arithmetically valid (all triples mutually commute),
      (b) VQE with 3 measurement bases matches the QWC-4 estimator on the same shot budget.
  R2. Heisenberg VQE-E with SPSA-flavoured longer run + shot averaging showing that
      the large variance in the fast COBYLA run is a stochastic-optimizer effect,
      not a Bell-measurement effect.  Reference: paper reports both VQE-P and VQE-E
      converge to E ~= -3 (Fig 2 in main text).
"""
import numpy as np, json, itertools, time
from pathlib import Path
from scipy.optimize import minimize

import sys
sys.path.insert(0, str(Path(__file__).parent))
from vqe_bell_replication import (
    HAM_HEIS, HAM_HEHp_09, hamiltonian_matrix, ground_energy,
    ansatz_2q, exp_val, pauli_string, commute, qwc,
    sample_bell, bell_estimate_XYZ, pauli_measure,
    single_qubit_gate, cnot, I2
)

# ---------------------------------------------------------------------------
# R1: Paper's exact HeH+ GC grouping
# ---------------------------------------------------------------------------
print("="*70)
print("R1: HeH+ with the paper's EXACT GC grouping")
print("="*70)

paper_groups = [
    ['XX', 'ZZ', 'II'],          # measured with Bell basis (GC, not QWC)
    ['XI', 'XZ', 'IZ'],          # QWC
    ['IX', 'ZI', 'ZX'],          # QWC
]

# Sanity: every pair in every group must commute (GC)
for gi, g in enumerate(paper_groups):
    for a, b in itertools.combinations(g, 2):
        c = commute(a, b)
        print(f"  Group {gi+1} pair ({a},{b}): commute? {c}")

# Do all 9 strings appear exactly once?
allP = sum(paper_groups, [])
Hstrs = [s for _, s in HAM_HEHp_09]
print(f"\nAll 9 paper strings covered by 3 groups? {sorted(allP)==sorted(Hstrs)}")

# ---- Measurement functions ------------------------------------------------
def rotate_and_sample(psi, basis, nshots, rng):
    """Rotate each qubit into its measurement basis (X->H, Y->HS^dag, Z->I),
    sample counts. Basis is a length-n string of {X,Y,Z} (I is treated as Z)."""
    n = len(basis)
    U = np.eye(2**n, dtype=complex)
    for q, ch in enumerate(basis):
        if ch == 'X':
            H1 = (1/np.sqrt(2))*np.array([[1,1],[1,-1]], dtype=complex)
            U = single_qubit_gate(n,q,H1) @ U
        elif ch == 'Y':
            Sd = np.array([[1,0],[0,-1j]], dtype=complex)
            H1 = (1/np.sqrt(2))*np.array([[1,1],[1,-1]], dtype=complex)
            U = single_qubit_gate(n,q,H1 @ Sd) @ U
    psi_rot = U @ psi
    probs = np.abs(psi_rot)**2; probs = probs/probs.sum()
    return rng.multinomial(nshots, probs)

def qwc_group_estimates(psi, group, nshots, rng):
    """Estimate every Pauli in a QWC group from a single tensor-product basis."""
    n = len(group[0])
    per_q = ['I']*n
    for s in group:
        for q, ch in enumerate(s):
            if ch != 'I':
                if per_q[q] == 'I': per_q[q] = ch
    basis = ''.join(ch if ch != 'I' else 'Z' for ch in per_q)
    counts = rotate_and_sample(psi, basis, nshots, rng)
    ests = {s: 0.0 for s in group}
    for i, c in enumerate(counts):
        if c == 0: continue
        bits = [(i>>k)&1 for k in range(n)][::-1]
        for s in group:
            parity = 0
            for q, ch in enumerate(s):
                if ch != 'I': parity ^= bits[q]
            ests[s] += ((-1)**parity)*c
    return {k: v/nshots for k,v in ests.items()}

def bell_group_estimates(psi, group, nshots, rng):
    """Estimate XX, YY, ZZ, II from one Bell-basis measurement (paper eq (4))."""
    counts = sample_bell(psi, nshots, rng)
    xx, yy, zz = bell_estimate_XYZ(counts, nshots)
    table = {'XX': xx, 'YY': yy, 'ZZ': zz, 'II': 1.0}
    return {s: table[s] for s in group if s in table}

def cost_heh_paper_groups(theta, nshots_per_basis, rng):
    psi = ansatz_2q(theta)
    w_of = {s: w for w, s in HAM_HEHp_09}
    E = 0.0
    # Group 1: Bell basis measures {XX, ZZ, II}
    ests1 = bell_group_estimates(psi, paper_groups[0], nshots_per_basis, rng)
    for s in paper_groups[0]:
        E += w_of[s] * ests1[s]
    # Groups 2 & 3: QWC
    for g in paper_groups[1:]:
        ests = qwc_group_estimates(psi, g, nshots_per_basis, rng)
        for s in g:
            E += w_of[s] * ests[s]
    return E

def cost_heh_qwc4(theta, nshots_per_basis, rng):
    """Same shot budget per basis, but 4 QWC groups."""
    psi = ansatz_2q(theta)
    w_of = {s: w for w, s in HAM_HEHp_09}
    qwc_groups = [
        ['II','IZ','ZI','ZZ'],   # commuting Z's
        ['IX','ZX'],
        ['XI','XZ'],
        ['XX'],
    ]
    E = 0.0
    for g in qwc_groups:
        ests = qwc_group_estimates(psi, g, nshots_per_basis, rng)
        for s in g:
            E += w_of[s]*ests[s]
    return E

# Reference exact energy
gs_heh, _ = ground_energy(HAM_HEHp_09)
print(f"\nExact HeH+ ground energy (numpy):         {gs_heh:+.4f} MJ/mol")

# Equal shot budgets:  12000 total shots
NSHOTS_TOTAL = 12000
n_paper = 3
n_qwc4  = 4
shots_paper = NSHOTS_TOTAL // n_paper   # 4000
shots_qwc4  = NSHOTS_TOTAL // n_qwc4    # 3000

# 3 independent VQE runs each
def run_vqe(cost_fn, n_params, n_runs, seed_base, extra_args=(), maxiter=300, tol=0.005):
    out = []
    for r in range(n_runs):
        rng = np.random.default_rng(seed_base + 3000*r)
        x0 = rng.uniform(-np.pi, np.pi, size=n_params)
        res = minimize(cost_fn, x0, args=extra_args,
                       method='COBYLA', tol=tol,
                       options={'maxiter':maxiter, 'rhobeg':0.4})
        out.append({'run':r,'E':float(res.fun),'nfev':int(res.nfev)})
    return out

print(f"\nBudget = {NSHOTS_TOTAL} total shots")
print(f"Paper-3-bases: {shots_paper} shots/basis; QWC-4-bases: {shots_qwc4} shots/basis\n")

runs_paper3 = run_vqe(cost_heh_paper_groups, 8, 3, seed_base=1001,
                      extra_args=(shots_paper, np.random.default_rng(51)))
runs_qwc4   = run_vqe(cost_heh_qwc4,         8, 3, seed_base=2001,
                      extra_args=(shots_qwc4,  np.random.default_rng(61)))

print("Paper 3-basis grouping (Bell + 2xQWC):")
for r in runs_paper3: print(f"  run{r['run']}: E={r['E']:+.4f} MJ/mol  (nfev={r['nfev']})")
print("QWC 4-basis grouping:")
for r in runs_qwc4:   print(f"  run{r['run']}: E={r['E']:+.4f} MJ/mol  (nfev={r['nfev']})")

best_paper = min(r['E'] for r in runs_paper3)
best_qwc4  = min(r['E'] for r in runs_qwc4)
print(f"\nBest paper-3-basis VQE:  {best_paper:+.4f} MJ/mol")
print(f"Best QWC-4-basis VQE:    {best_qwc4:+.4f} MJ/mol")
print(f"Exact:                   {gs_heh:+.4f} MJ/mol")
print(f"Basis reduction:         {(1-3/4)*100:.1f}% (4 -> 3, matches paper Appendix A)")

# ---------------------------------------------------------------------------
# R2: Heisenberg VQE-E with tighter optimizer  --------------------------------
# ---------------------------------------------------------------------------
print()
print("="*70)
print("R2: Heisenberg VQE-E (Bell) with tighter COBYLA settings")
print("     (main run had large variance from too-loose tol=0.01)")
print("="*70)

def cost_heis_bell(theta, nshots, rng):
    psi = ansatz_2q(theta)
    counts = sample_bell(psi, nshots, rng)
    xx, yy, zz = bell_estimate_XYZ(counts, nshots)
    return xx+yy+zz

def cost_heis_pauli(theta, nshots_each, rng):
    psi = ansatz_2q(theta)
    return (pauli_measure(psi,'XX',nshots_each,rng)
          + pauli_measure(psi,'YY',nshots_each,rng)
          + pauli_measure(psi,'ZZ',nshots_each,rng))

# Same total shots = 9000; VQE-E gets 9000 in one basis, VQE-P gets 3000 each.
N = 9000
runs_p = run_vqe(cost_heis_pauli, 8, 5, seed_base=3001,
                 extra_args=(N//3, np.random.default_rng(71)),
                 maxiter=400, tol=0.001)
runs_e = run_vqe(cost_heis_bell,  8, 5, seed_base=4001,
                 extra_args=(N,    np.random.default_rng(72)),
                 maxiter=400, tol=0.001)
Ep = [r['E'] for r in runs_p]; Ee = [r['E'] for r in runs_e]
print(f"VQE-P (Pauli, 3 bases, {N//3} shots each): mean={np.mean(Ep):+.4f} std={np.std(Ep):.4f}  best={min(Ep):+.4f}")
print(f"VQE-E (Bell,  1 basis, {N}   shots     ): mean={np.mean(Ee):+.4f} std={np.std(Ee):.4f}  best={min(Ee):+.4f}")
print(f"Exact: {-3.0}")

# Save
out = {
    'R1_heh_paper_groups': {
        'paper_groups': paper_groups,
        'exact': gs_heh,
        'budget_total_shots': NSHOTS_TOTAL,
        'runs_paper3': runs_paper3,
        'runs_qwc4':  runs_qwc4,
        'best_paper3': float(best_paper),
        'best_qwc4':   float(best_qwc4),
        'basis_reduction_qwc4_to_paper3': (1-3/4),
    },
    'R2_heisenberg_tight': {
        'shots_total': N,
        'runs_P': runs_p,
        'runs_E': runs_e,
        'mean_P': float(np.mean(Ep)), 'std_P': float(np.std(Ep)), 'best_P': float(min(Ep)),
        'mean_E': float(np.mean(Ee)), 'std_E': float(np.std(Ee)), 'best_E': float(min(Ee)),
    },
}
Path(__file__).parent.joinpath('refinements.json').write_text(json.dumps(out, indent=2))
print("\nSaved refinements.json")
