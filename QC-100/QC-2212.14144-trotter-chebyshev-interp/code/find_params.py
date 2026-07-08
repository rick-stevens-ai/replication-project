"""Find g such that |E0| of H = -J(ZZ + g(XI+IX)) matches paper's ~1.117.
Also print exact ground state energy for reference."""
import numpy as np
from numpy.linalg import eigh

I2 = np.eye(2)
X = np.array([[0,1],[1,0]], dtype=complex)
Z = np.array([[1,0],[0,-1]], dtype=complex)

def H_tfim(J=1.0, g=0.5):
    ZZ = np.kron(Z, Z)
    XI = np.kron(X, I2)
    IX = np.kron(I2, X)
    return -J * (ZZ + g*(XI + IX))

for g in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1.0]:
    H = H_tfim(J=1.0, g=g)
    w = eigh(H)[0]
    print(f"g={g:.2f}  E0={w[0]:+.6f}  |E0|={abs(w[0]):.6f}  spectrum={w.round(4)}")
