# Brief — quant-ph/0012055

Wang, Sørensen and Mølmer (2000) propose a multi-bit gate scheme for ion-trap quantum
computers where all qubits couple to a shared vibrational bus mode via a Sørensen–Mølmer
geometric-phase loop, allowing $C^n$-NOT and Grover's search to be built out of a small
number of parallelogram-shaped pulse sequences.  In an independent QuTiP statevector
simulation I verify the Fourier decomposition (Eq. 6, error $<10^{-15}$), the Grover
diffusion identity (Eq. 10, error $<10^{-15}$), the full Grover algorithm for $n=3..6$
(agreement with theory to machine precision), the $C^{n_c}$-NOT permutation fidelity
$F_{\rm perm}=1.0000$ up to $n_c=6$ (7-qubit gate), and the oscillator-state-insensitivity
claim (reduced qubit unitarity error $<10^{-6}$ across ground, Fock and coherent oscillator
states).  The one substantive discrepancy is that the printed Eq. (5) three-qubit Toffoli
Hamiltonian generates $\exp(-i\pi(\sigma_z^1+\sigma_z^2+1)^2\sigma_x^3/16)$, which differs
from the exact Toffoli by a single-qubit $\exp(-i\pi\sigma_x^3/16)$ rotation
($F_{\rm avg}=0.9662$ vs 1.0000).  A plausible typo correction ($+1/(32K)\to-\sigma_x^3/(32K)$
in the constant term) yields exact Toffoli.  **Verdict: PARTIAL** — architecture and
downstream constructions replicate; one printed Hamiltonian has a small notational issue.
