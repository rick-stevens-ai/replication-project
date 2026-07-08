"""Run the core replication experiment.

For each benchmark circuit (Qiskit QASM in a CNOT/U3 basis):
  A. Baseline: Qiskit transpile(optimization_level=3, basis={cx, u3})
  B. BQSKit: bqskit.compile(circuit, optimization_level=3) with CNOT gate model
  C. Composed: run BQSKit optimizer AFTER Qiskit level-3 (paper's "+Qiskit" mode)

Report CNOT counts and single-qubit gate counts for each.
Verify functional equivalence by comparing unitary matrices (Frobenius distance)
for small circuits (<=5 qubits).

Headline claim tested: BQSKit reduces CNOT count vs Qiskit baseline (13% avg for
optimizer standalone; 5% additional avg when composed).
"""
import os, json, time, sys
import numpy as np
from qiskit import QuantumCircuit, qasm2, transpile
from qiskit.quantum_info import Operator

from bqskit import Circuit as BqCircuit, compile as bq_compile
from bqskit.ir.gates import CNOTGate

HERE = os.path.dirname(os.path.abspath(__file__))
BENCH = os.path.join(HERE, 'benchmarks')
EVIDENCE = os.path.abspath(os.path.join(HERE, '..', 'report', 'evidence'))
os.makedirs(EVIDENCE, exist_ok=True)


def qiskit_qasm_path(name):
    return os.path.join(BENCH, f'{name}.qasm')


def qiskit_from_file(name):
    return qasm2.load(qiskit_qasm_path(name),
                       include_path=qasm2.LEGACY_INCLUDE_PATH,
                       custom_instructions=qasm2.LEGACY_CUSTOM_INSTRUCTIONS,
                       custom_classical=qasm2.LEGACY_CUSTOM_CLASSICAL,
                       strict=False)


def bqskit_from_file(name):
    return BqCircuit.from_file(qiskit_qasm_path(name))


def gate_counts_qiskit(qc: QuantumCircuit):
    """Convert to {u3, cx} basis then count."""
    qc2 = transpile(qc, basis_gates=['u3', 'cx'], optimization_level=0)
    ops = dict(qc2.count_ops())
    return {'cx': ops.get('cx', 0), 'sq': ops.get('u3', 0), 'depth': qc2.depth()}


def gate_counts_bqskit(bc: BqCircuit):
    """Convert BQSKit -> QASM -> Qiskit and count in same basis."""
    qasm_str = bc.to('qasm')
    from qiskit import qasm2
    qc = qasm2.loads(qasm_str,
                      include_path=qasm2.LEGACY_INCLUDE_PATH,
                      custom_instructions=qasm2.LEGACY_CUSTOM_INSTRUCTIONS,
                      custom_classical=qasm2.LEGACY_CUSTOM_CLASSICAL,
                      strict=False)
    return gate_counts_qiskit(qc)


def unitary_close(qc_a: QuantumCircuit, qc_b: QuantumCircuit, tol=1e-6):
    if qc_a.num_qubits > 5 or qc_b.num_qubits > 5:
        return None, None  # too big to check exactly
    try:
        Ua = Operator(qc_a).data
        Ub = Operator(qc_b).data
        # Up to global phase: use |Tr(Ua^dag Ub)| / dim
        d = Ua.shape[0]
        overlap = abs(np.trace(Ua.conj().T @ Ub)) / d
        return float(overlap), bool(overlap > 1 - tol)
    except Exception as e:
        return None, str(e)


def bqskit_to_qiskit(bc: BqCircuit) -> QuantumCircuit:
    from qiskit import qasm2
    qasm_str = bc.to('qasm')
    return qasm2.loads(qasm_str,
                        include_path=qasm2.LEGACY_INCLUDE_PATH,
                        custom_instructions=qasm2.LEGACY_CUSTOM_INSTRUCTIONS,
                        custom_classical=qasm2.LEGACY_CUSTOM_CLASSICAL,
                        strict=False)


def run_one(name):
    print(f'\n=== {name} ===', flush=True)
    result = {'name': name}

    # Original (as-built)
    qc_orig = qiskit_from_file(name)
    orig = gate_counts_qiskit(qc_orig)
    result['original'] = orig
    print(f'  original      : cx={orig["cx"]:4d}  sq={orig["sq"]:4d}  depth={orig["depth"]}', flush=True)

    # A. Qiskit level-3 baseline
    t0 = time.time()
    qc_qk3 = transpile(qc_orig, basis_gates=['u3', 'cx'], optimization_level=3, seed_transpiler=0)
    t_qk3 = time.time() - t0
    qk3 = gate_counts_qiskit(qc_qk3)
    qk3['time_s'] = round(t_qk3, 3)
    result['qiskit_l3'] = qk3
    print(f'  qiskit L3     : cx={qk3["cx"]:4d}  sq={qk3["sq"]:4d}  depth={qk3["depth"]}  t={t_qk3:.2f}s', flush=True)

    # B. BQSKit standalone at optimization_level=3
    bc = bqskit_from_file(name)
    t0 = time.time()
    try:
        bc_opt = bq_compile(bc, optimization_level=3)
        t_bq = time.time() - t0
        bq = gate_counts_bqskit(bc_opt)
        bq['time_s'] = round(t_bq, 3)
        bq['status'] = 'ok'
    except Exception as e:
        t_bq = time.time() - t0
        bq = {'error': str(e), 'time_s': round(t_bq, 3), 'status': 'error'}
        bc_opt = None
    result['bqskit_l3'] = bq
    if bc_opt is not None:
        print(f'  bqskit L3     : cx={bq["cx"]:4d}  sq={bq["sq"]:4d}  depth={bq["depth"]}  t={t_bq:.2f}s', flush=True)
    else:
        print(f'  bqskit L3     : ERROR t={t_bq:.2f}s : {bq["error"][:120]}', flush=True)

    # C. Composed: BQSKit AFTER Qiskit level-3
    try:
        # Write intermediate QASM
        interm_path = os.path.join(EVIDENCE, f'{name}_qiskit_l3.qasm')
        with open(interm_path, 'w') as f:
            f.write(qasm2.dumps(qc_qk3))
        bc_from_qk3 = BqCircuit.from_file(interm_path)
        t0 = time.time()
        bc_comp = bq_compile(bc_from_qk3, optimization_level=3)
        t_comp = time.time() - t0
        comp = gate_counts_bqskit(bc_comp)
        comp['time_s'] = round(t_comp, 3)
        comp['status'] = 'ok'
    except Exception as e:
        t_comp = time.time() - t0 if 't0' in dir() else 0
        comp = {'error': str(e), 'time_s': 0, 'status': 'error'}
        bc_comp = None
    result['qiskit_l3_then_bqskit'] = comp
    if bc_comp is not None:
        print(f'  qk3+bqskit    : cx={comp["cx"]:4d}  sq={comp["sq"]:4d}  depth={comp["depth"]}  t={comp["time_s"]:.2f}s', flush=True)
    else:
        print(f'  qk3+bqskit    : ERROR : {comp["error"][:120]}', flush=True)

    # Equivalence check (small circuits only)
    if qc_orig.num_qubits <= 5:
        ov, ok = unitary_close(qc_orig, qc_qk3)
        result['equiv_qiskit_l3'] = {'overlap': ov, 'match': ok}
        print(f'  equiv qk3     : overlap={ov}  match={ok}', flush=True)
        if bc_opt is not None:
            qc_bq = bqskit_to_qiskit(bc_opt)
            ov2, ok2 = unitary_close(qc_orig, qc_bq)
            result['equiv_bqskit_l3'] = {'overlap': ov2, 'match': ok2}
            print(f'  equiv bqskit  : overlap={ov2}  match={ok2}', flush=True)
        if bc_comp is not None:
            qc_c = bqskit_to_qiskit(bc_comp)
            ov3, ok3 = unitary_close(qc_orig, qc_c)
            result['equiv_composed'] = {'overlap': ov3, 'match': ok3}
            print(f'  equiv qk3+bq  : overlap={ov3}  match={ok3}', flush=True)

    # Save optimized circuits as evidence
    if bc_opt is not None:
        with open(os.path.join(EVIDENCE, f'{name}_bqskit_l3.qasm'), 'w') as f:
            f.write(bc_opt.to('qasm'))
    if bc_comp is not None:
        with open(os.path.join(EVIDENCE, f'{name}_qk3_then_bqskit.qasm'), 'w') as f:
            f.write(bc_comp.to('qasm'))

    return result


def main():
    names = ['qaoa5', 'qaoa10', 'grover3', 'adder4', 'hub4']
    if len(sys.argv) > 1:
        names = sys.argv[1:]

    results = []
    for name in names:
        try:
            r = run_one(name)
            results.append(r)
        except Exception as e:
            import traceback
            traceback.print_exc()
            results.append({'name': name, 'error': str(e)})

    def _default(o):
        import numpy as _np
        if isinstance(o, (_np.bool_,)):
            return bool(o)
        if isinstance(o, (_np.integer,)):
            return int(o)
        if isinstance(o, (_np.floating,)):
            return float(o)
        return str(o)
    out = os.path.join(EVIDENCE, 'comparison_results.json')
    with open(out, 'w') as f:
        json.dump(results, f, indent=2, default=_default)
    print(f'\nWrote {out}')

    # Summary
    print('\n=== SUMMARY ===')
    print(f'{"name":<10} {"orig_cx":>8} {"qk3_cx":>8} {"bq_cx":>8} {"qk3+bq_cx":>10} {"bq vs qk3":>10} {"qk3+bq vs qk3":>15}')
    reds_b = []
    reds_c = []
    for r in results:
        if 'error' in r:
            continue
        o = r['original']['cx']
        q = r['qiskit_l3']['cx']
        b = r['bqskit_l3'].get('cx', -1)
        c = r['qiskit_l3_then_bqskit'].get('cx', -1)
        if q > 0 and b >= 0:
            db = (q - b) / q * 100
            reds_b.append(db)
        else:
            db = None
        if q > 0 and c >= 0:
            dc = (q - c) / q * 100
            reds_c.append(dc)
        else:
            dc = None
        print(f'{r["name"]:<10} {o:>8} {q:>8} {b:>8} {c:>10} {("+" if db and db<0 else "") + (f"{db:+.1f}%" if db is not None else "?"):>10} {("+" if dc and dc<0 else "") + (f"{dc:+.1f}%" if dc is not None else "?"):>15}')

    if reds_b:
        print(f'\nAvg BQSKit vs Qiskit L3 CNOT reduction: {np.mean(reds_b):+.1f}% (paper claim: standalone 8% of inputs improved on 2Q; +Qiskit avg -5%)')
    if reds_c:
        print(f'Avg (Qiskit L3 + BQSKit) vs Qiskit L3 CNOT reduction: {np.mean(reds_c):+.1f}% (paper claim: additional 5%)')


if __name__ == '__main__':
    main()
