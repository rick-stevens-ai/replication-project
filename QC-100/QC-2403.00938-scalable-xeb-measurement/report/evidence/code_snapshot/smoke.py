"""Quick correctness sanity checks for xeb_mipt.py."""
import sys
sys.path.insert(0, '.')
import numpy as np
from xeb_mipt import (
    sample_mipt_circuit, linear_xeb_for_circuit, linear_xeb_same_input,
    measurement_record_probs, _initial_state_in_axis_convention,
)

print('--- initial state sanity ---')
z4 = _initial_state_in_axis_convention(4, 'zero')
print('|zero>^4  norm^2 =', float(np.vdot(z4, z4).real))
zt4 = _initial_state_in_axis_convention(4, 'zeroT')
print('|0T0T> norm^2 =', float(np.vdot(zt4, zt4).real))
# Overlap between |0>^4 and |0T0T>: only nonzero on qubits 1 and 3 being |0>.
ov = np.vdot(z4, zt4)
# Expected: qubits 1,3 in state |T> = (|0>+e^{ipi/4}|1>)/sqrt2, projecting to |0> gives 1/sqrt2 each.
expected = (1.0 / np.sqrt(2.0)) ** 2  # for two |T> qubits
print(f'<0000|0T0T> = {ov} (expected magnitude {expected})')
assert abs(abs(ov) - expected) < 1e-10, 'initial state overlap wrong'
print('  OK')

print()
print('--- chi same-input == 1 exactly ---')
for L in (4, 6):
    for p in (0.0, 0.2, 0.5):
        circ = sample_mipt_circuit(L, p, seed=42)
        chi, diag = linear_xeb_same_input(circ, 'zero')
        print(f'  L={L} p={p}: chi_same = {chi:.10f}  (n_records={diag["n_records"]}, n_meas={sum(len(l) for l in circ.layers_meas)})')
        assert abs(chi - 1.0) < 1e-9, f'same-input chi should be 1, got {chi}'
print('  OK')

print()
print('--- chi diff-input at p=0 (no measurements) ---')
# With p=0 there are no measurement records; sum is over the empty tuple only.
# p^rho_() = p^sigma_() = 1, so chi = 1*1 / 1 = 1.
for L in (4, 6, 8):
    circ = sample_mipt_circuit(L, 0.0, seed=7)
    chi, diag = linear_xeb_for_circuit(circ)
    print(f'  L={L} p=0: chi_diff = {chi:.10f}  (n_meas={diag["n_meas_total"]})')
    assert abs(chi - 1.0) < 1e-9, f'p=0 chi should be 1, got {chi}'
print('  OK')

print()
print('--- chi diff-input at moderate p: sample a few circuits ---')
for L in (4, 6):
    chis = []
    for s in range(6):
        circ = sample_mipt_circuit(L, 0.3, seed=100 + s)
        chi, diag = linear_xeb_for_circuit(circ)
        chis.append(chi)
    print(f'  L={L} p=0.3: mean chi_diff = {np.mean(chis):.4f} +/- {np.std(chis):.4f}  '
          f'(range [{min(chis):.4f}, {max(chis):.4f}])')

print()
print('SMOKE PASSED')
