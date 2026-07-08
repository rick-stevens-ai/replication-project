#!/usr/bin/env python3
"""Debug: apply single ZZ block-encoding gadget to |+>|+> in Qiskit, compare to
analytic exp(-gamma*dtau*ZZ)|+>|+>."""
import numpy as np
from qiskit_full_ite import apply_pite_gadget_via_qiskit, pauli_op

plus = np.array([1,1], dtype=complex)/np.sqrt(2)
pp = np.kron(plus, plus)
gamma = -0.5; dtau = 0.1
sites = {0:'Z', 1:'Z'}

new_qis, ps = apply_pite_gadget_via_qiskit(pp, 2, gamma, sites, dtau)
print("Qiskit output state:", np.round(new_qis, 6))
print("Success prob:", ps)

ZZ = pauli_op(2, sites)
ref = np.cosh(gamma*dtau)*pp - np.sinh(gamma*dtau)*(ZZ @ pp)
ref_norm = ref / np.linalg.norm(ref)
print("Analytic output state (renormalized):", np.round(ref_norm, 6))
print("|<qis|ref>| =", abs(np.vdot(new_qis, ref_norm)))
