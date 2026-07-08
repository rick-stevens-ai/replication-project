#!/usr/bin/env python3
"""
Analytic reconstruction of Roetteler et al. 2017 (arXiv:1706.06752)
Table 2 headline resource counts for Shor's algorithm on ECDLP.

Two independent cost formulas from the paper are used:

  (A) Closed-form asymptotic (abstract / Section 5.2):
        Qubits:  9n + 2*ceil(log2 n) + 10
        Toffoli: (448 * log2(n) + 4090) * n^3        [Shor over ECDLP]

  (B) Per-point-addition formula (Section 5.2, Figure 11 fit):
        Toffoli per controlled point-addition: 224*n^2*log2(n) + 2045*n^2
        Full Shor = 2n * (per point-addition)
        =>  Toffoli = (448*log2(n) + 4090)*n^3         (same as A, by construction)

These are the AUTHORS' OWN interpolation formulas, derived from their simulated
Toffoli counts at n in {110, 160, 192, 224, 256, 384, 521}. Reproducing Table 2
from these formulas therefore tests: (1) that we have transcribed the formulas
faithfully, (2) that the closed-form is internally consistent with Table 2 to
the ~few-percent tolerance authors themselves note ("up to lower order terms").

Table 1 also gives per-primitive breakdown, which we cross-check as a bonus:
  ctrl_add_modp:      2n+1 qubits (n ancilla)     16*n*log2(n) - 26.9*n     Toffolis
  ctrl_sub_modp:      2n+4 qubits                 16*n*log2(n) - 23.8*n
  ctrl_neg_modp:      n+3                          8*n*log2(n) - 14.5*n
  mul_modp (dbl/add): 3n+2                        32*n^2*log2(n) - 59.4*n^2
  mul_modp (Mont):    5n+4 qubits, 2n+4 ancilla  16*n^2*log2(n) - 26.3*n^2
  squ_modp (dbl/add): 2n+3                        32*n^2*log2(n) - 59.4*n^2
  squ_modp (Mont):    4n+5 qubits, 2n+5 ancilla  16*n^2*log2(n) - 26.3*n^2
  inv_modp:           7n + 2*ceil(log2 n) + 9    32*n^2*log2(n)

Per-point-addition leading-coeff derivation (Section 5.2):
  4 inversions * 32  + 2 squarings * 16 + 4 multiplications * 16 = 224   ✓
  => leading term: 224 * n^2 * log2(n)
  => next term (regression fit):  +2045 * n^2

Shor requires 2n controlled point-additions, so:
  Shor Toffoli = 2n * (224*n^2*log2(n) + 2045*n^2)
               = 448*n^3*log2(n) + 4090*n^3.

Reported Table 2 values (ground truth from paper):
  n=110:  1014 qubits,  9.44e9  Toffoli
  n=160:  1466,         2.97e10
  n=192:  1754,         5.30e10
  n=224:  2042,         8.43e10
  n=256:  2330,         1.26e11
  n=384:  3484,         4.52e11
  n=521:  4719,         1.14e12
"""
from math import log2, ceil
import json
import os

TABLE2_REPORTED = {
    110: (1014, 9.44e9),
    160: (1466, 2.97e10),
    192: (1754, 5.30e10),
    224: (2042, 8.43e10),
    256: (2330, 1.26e11),
    384: (3484, 4.52e11),
    521: (4719, 1.14e12),
}

def qubits(n: int) -> int:
    # Section 5.2 (right after Table 1):
    #   inversion uses 7n + 2*ceil(log2 n) + 9
    #   +1 control qubit + 2n scratch during inversion
    #   = 9n + 2*ceil(log2 n) + 10
    return 9*n + 2*ceil(log2(n)) + 10

def toffoli_shor(n: int) -> float:
    # Closed-form from abstract + Section 5.2:
    return (448.0 * log2(n) + 4090.0) * n**3

def toffoli_per_point_add(n: int) -> float:
    # Section 5.2 / Figure 11 fit:
    return 224.0 * n**2 * log2(n) + 2045.0 * n**2

def per_primitive(n: int):
    """Table 1 breakdown (used to cross-check the '224' leading coefficient)."""
    log2n = log2(n)
    prims = {
        'ctrl_add_modp': (2*n + 1,           16*n*log2n - 26.9*n),
        'ctrl_sub_modp': (2*n + 4,           16*n*log2n - 23.8*n),
        'ctrl_neg_modp': (n + 3,             8*n*log2n - 14.5*n),
        'mul_dbladd':    (3*n + 2,           32*n**2*log2n - 59.4*n**2),
        'mul_mont':      (5*n + 4,           16*n**2*log2n - 26.3*n**2),
        'squ_dbladd':    (2*n + 3,           32*n**2*log2n - 59.4*n**2),
        'squ_mont':      (4*n + 5,           16*n**2*log2n - 26.3*n**2),
        'inv_modp':      (7*n + 2*ceil(log2n) + 9,   32*n**2*log2n),
    }
    return prims

def point_add_from_primitives(n: int) -> float:
    """Cross-check: build point-add Toffoli count from Table 1 primitives.

    Section 5.2: 'a total of 4 inverters, 2 squarers, and 4 multipliers'
    Uses Montgomery multiplication + squaring (per paper's stated choice).
    """
    prims = per_primitive(n)
    return 4*prims['inv_modp'][1] + 2*prims['squ_mont'][1] + 4*prims['mul_mont'][1]

def shor_from_primitives(n: int) -> float:
    return 2*n * point_add_from_primitives(n)

def rel_err(a: float, b: float) -> float:
    return abs(a - b) / b

def main():
    rows = []
    print(f"{'n':>4}  {'qub_calc':>8}  {'qub_rep':>7}  {'q_match':>7}  "
          f"{'toff_closed':>13}  {'toff_prims':>13}  {'toff_reported':>13}  "
          f"{'closed_err':>10}  {'prims_err':>9}")
    print('-'*130)
    for n, (q_rep, toff_rep) in sorted(TABLE2_REPORTED.items()):
        q_calc = qubits(n)
        t_closed = toffoli_shor(n)
        t_prims  = shor_from_primitives(n)
        q_ok = (q_calc == q_rep)
        row = {
            'n': n,
            'qubits_calc': q_calc,
            'qubits_reported': q_rep,
            'qubits_match': q_ok,
            'toffoli_closed_form': t_closed,
            'toffoli_from_primitives': t_prims,
            'toffoli_reported': toff_rep,
            'closed_rel_err': rel_err(t_closed, toff_rep),
            'primitives_rel_err': rel_err(t_prims, toff_rep),
        }
        rows.append(row)
        print(f"{n:>4}  {q_calc:>8}  {q_rep:>7}  {'YES' if q_ok else 'NO':>7}  "
              f"{t_closed:>13.3e}  {t_prims:>13.3e}  {toff_rep:>13.3e}  "
              f"{row['closed_rel_err']*100:>9.2f}%  {row['primitives_rel_err']*100:>8.2f}%")

    # Aggregate
    q_all_match = all(r['qubits_match'] for r in rows)
    max_closed_err = max(r['closed_rel_err'] for r in rows)
    max_prims_err = max(r['primitives_rel_err'] for r in rows)
    mean_closed_err = sum(r['closed_rel_err'] for r in rows)/len(rows)
    mean_prims_err = sum(r['primitives_rel_err'] for r in rows)/len(rows)

    print()
    print(f"Qubit formula matches Table 2 for ALL n:  {q_all_match}")
    print(f"Toffoli closed-form:  max rel err = {max_closed_err*100:.2f}%   "
          f"mean = {mean_closed_err*100:.2f}%")
    print(f"Toffoli via primitives: max rel err = {max_prims_err*100:.2f}%   "
          f"mean = {mean_prims_err*100:.2f}%")

    outdir = os.path.expanduser(
        '~/Dropbox/REPLICATE-PROJECT/QC-100/'
        'QC-1706.06752-shor-elliptic-curve-resources/report/evidence')
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, 'analytic_reconstruction.json'), 'w') as f:
        json.dump({
            'formulas': {
                'qubits':              '9n + 2*ceil(log2 n) + 10',
                'toffoli_shor_closed': '(448*log2(n) + 4090)*n^3',
                'toffoli_point_add':   '224*n^2*log2(n) + 2045*n^2',
                'toffoli_shor_full':   '2n * (point-add Toffoli)',
            },
            'reported_ground_truth_source':
                'Roetteler et al. 2017 (arXiv:1706.06752v3), Table 2',
            'rows': rows,
            'summary': {
                'qubits_all_match': q_all_match,
                'toffoli_closed_max_rel_err': max_closed_err,
                'toffoli_closed_mean_rel_err': mean_closed_err,
                'toffoli_from_primitives_max_rel_err': max_prims_err,
                'toffoli_from_primitives_mean_rel_err': mean_prims_err,
            },
        }, f, indent=2)
    print(f"\nWrote: {outdir}/analytic_reconstruction.json")

if __name__ == '__main__':
    main()
