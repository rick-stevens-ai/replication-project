"""
Final verification: run both encoders, save all evidence to report/evidence/.
"""
import stim
import json
import sys
sys.path.insert(0, '.')

from scaling_study import build_planar_surface_code, canonical_encoder_circuit, circuit_depth, count_two_qubit_gates, verify_encoder_circuit
from optimized_scaling import build_optimized_zero_L_circuit, verify_zero_L


def run_d3_comparison():
    L = 3
    code = build_planar_surface_code(L)

    # Canonical (Cleve-Gottesman / Dennis-style) encoder
    canonical_circ = canonical_encoder_circuit(code)
    can_depth = circuit_depth(canonical_circ)
    can_2q = count_two_qubit_gates(canonical_circ)
    can_valid, can_msg = verify_encoder_circuit(canonical_circ, code)

    # Optimized parallel-scheduled encoder for |0_L>
    opt_circ, opt_depth, opt_cnots, opt_cnot_steps = build_optimized_zero_L_circuit(code)
    opt_valid, opt_msg = verify_zero_L(opt_circ, code)

    return {
        'L': L,
        'n_qubits': code['n'],
        'canonical': {
            'depth': can_depth,
            'two_qubit_gates': can_2q,
            'valid_code_state': can_valid,
            'circuit_str': str(canonical_circ),
        },
        'optimized_zero_L': {
            'depth': opt_depth,
            'two_qubit_gates': opt_cnots,
            'valid_code_state': opt_valid,
            'circuit_str': str(opt_circ),
        },
        'paper_2L_bound_unknown_state': 2 * L,
    }


def run_scaling():
    results = []
    for L in [3, 5, 7]:
        code = build_planar_surface_code(L)
        canonical_circ = canonical_encoder_circuit(code)
        can_depth = circuit_depth(canonical_circ)
        can_2q = count_two_qubit_gates(canonical_circ)
        can_valid, _ = verify_encoder_circuit(canonical_circ, code)
        results.append({
            'L': L,
            'n_qubits': code['n'],
            'canonical_depth': can_depth,
            'canonical_two_qubit_gates': can_2q,
            'canonical_valid': can_valid,
            'paper_2L_bound': 2 * L,
        })
    return results


if __name__ == "__main__":
    print("=" * 70)
    print("D=3 CORE REPLICATION")
    print("=" * 70)
    d3 = run_d3_comparison()
    print(f"L = {d3['L']}, n = {d3['n_qubits']} qubits")
    print()
    print("Canonical (Cleve-Gottesman, generic stabilizer encoder):")
    print(f"  Depth:              {d3['canonical']['depth']} time steps")
    print(f"  Two-qubit gates:    {d3['canonical']['two_qubit_gates']}")
    print(f"  Valid |0_L>:        {d3['canonical']['valid_code_state']}")
    print()
    print("Optimized (parallel-scheduled unique-seed CSS encoder for |0_L>):")
    print(f"  Depth:              {d3['optimized_zero_L']['depth']} time steps")
    print(f"  Two-qubit gates:    {d3['optimized_zero_L']['two_qubit_gates']}")
    print(f"  Valid |0_L>:        {d3['optimized_zero_L']['valid_code_state']}")
    print()
    print(f"Paper's 2L bound (arbitrary state): {d3['paper_2L_bound_unknown_state']}")
    print()
    print(f"Depth reduction (canonical -> optimized): {d3['canonical']['depth'] / d3['optimized_zero_L']['depth']:.2f}x")
    print(f"Depth reduction (canonical -> paper 2L):  {d3['canonical']['depth'] / d3['paper_2L_bound_unknown_state']:.2f}x")

    print()
    print("=" * 70)
    print("SCALING STUDY (canonical encoder vs paper's 2L)")
    print("=" * 70)
    scaling = run_scaling()
    print(f"{'L':<4} {'n':<6} {'2L(paper)':<12} {'canonical_depth':<18} {'canonical_2Q':<14} {'valid':<8}")
    print("-" * 70)
    for row in scaling:
        print(f"{row['L']:<4} {row['n_qubits']:<6} {row['paper_2L_bound']:<12} {row['canonical_depth']:<18} {row['canonical_two_qubit_gates']:<14} {'YES' if row['canonical_valid'] else 'NO':<8}")
    # Ratio
    print()
    print("Depth ratio (canonical / 2L):")
    for row in scaling:
        r = row['canonical_depth'] / row['paper_2L_bound']
        print(f"  L={row['L']}: {row['canonical_depth']}/{row['paper_2L_bound']} = {r:.2f}x")

    # Save JSON evidence
    all_evidence = {
        'paper': 'arXiv:2002.00362 (Higgott et al., Optimal local unitary encoding circuits for the surface code)',
        'tool': f'Stim {stim.__version__}',
        'd3_comparison': d3,
        'scaling_study': scaling,
    }
    with open('../report/evidence/full_results.json', 'w') as f:
        json.dump(all_evidence, f, indent=2, default=str)
    print("\nSaved: report/evidence/full_results.json")

    # Save d=3 circuits explicitly for inspection
    with open('../report/evidence/d3_canonical_encoder.stim', 'w') as f:
        f.write(d3['canonical']['circuit_str'])
    with open('../report/evidence/d3_optimized_encoder.stim', 'w') as f:
        f.write(d3['optimized_zero_L']['circuit_str'])
    print("Saved: report/evidence/d3_canonical_encoder.stim")
    print("Saved: report/evidence/d3_optimized_encoder.stim")
