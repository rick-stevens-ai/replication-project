<!--
extraction/marker.md
Source: arXiv:quant-ph/0208135 v1 (2002)
Provenance: this file is a Markdown-cleaned rendering of poppler's `pdftotext`
output, produced because neither `marker_single` nor `nougat` is installed on
this machine (CherryRd, 2026-07-05). The paper is a clean text-based PDF from
2002 (Word/LaTeX source), so pdftotext gives near-perfect extraction; equations
are re-rendered here in Markdown/LaTeX for readability. This is the same source
text used by the replication script `report/evidence/adiabatic_paths.py`.
See `report/artifacts_summary.md` for the full provenance chain.
-->

# Quantum Adiabatic Evolution Algorithms with Different Paths

**Authors**: Edward Farhi, Jeffrey Goldstone (MIT CTP), Sam Gutmann (Northeastern Math)
**arXiv**: quant-ph/0208135v1, 21 Aug 2002
**Report**: MIT-CTP #3297

## Abstract

In quantum adiabatic evolution algorithms, the quantum computer follows the ground state of a slowly varying Hamiltonian. The ground state of the initial Hamiltonian is easy to construct; the ground state of the final Hamiltonian encodes the solution of the computational problem. These algorithms have generally been studied in the case where the "straight line" path from initial to final Hamiltonian is taken. But there is no reason not to try paths involving terms that are not linear combinations of the initial and final Hamiltonians. We give several proposals for randomly generating new paths. Using one of these proposals, we convert an algorithmic failure into a success.

## 1  Introduction

Quantum adiabatic evolution algorithms [1] are designed to keep the quantum computer in the ground state of a slowly varying Hamiltonian H(t). The initial Hamiltonian $H_B = H(0)$ is chosen so that its ground state is easy to construct. The ground state of the final Hamiltonian $H_P = H(T)$, where $T$ is the running time of the algorithm, encodes the solution to the computational problem at hand. The simplest interpolation is

$$
H(t) = \tilde H(t/T), \qquad \tilde H(s) = (1-s) H_B + s H_P, \quad 0 \le s \le 1. \tag{1,2}
$$

The adiabatic algorithm succeeds as long as $T \gg 1 / \mathrm{gap}^2$, where the gap is the minimum energy difference between the ground and first excited states of $\tilde H(s)$ as $s$ varies in $[0,1]$. In this paper we consider paths of the form

$$
\tilde H(s) = (1-s) H_B + s H_P + s(1-s) H_E, \tag{3}
$$

with $H_E$ an "extra" piece turned off at the boundaries.

## 2  Examples of different paths

For a local classical cost function $h(z_1,\dots,z_n) = \sum_C h_C$, each $h_C$ acting on a few bits, one defines the problem Hamiltonian $H_P = \sum_C H_{P,C}$ diagonal in the computational basis, and

$$
H_{B,C} = \tfrac12 \sum_{q \in C}\bigl(1 - \sigma_x^{(q)}\bigr), \qquad H_B = \sum_C H_{B,C}. \tag{7,8}
$$

Then (2) reads $\tilde H(s) = \sum_C \bigl[(1-s) H_{B,C} + s H_{P,C}\bigr]$ (eq 9). Introducing per-clause $H_{E,C}$ preserving the same decomposition,

$$
\tilde H(s) = \sum_C \bigl[(1-s) H_{B,C} + s H_{P,C} + s(1-s) H_{E,C}\bigr]. \tag{11}
$$

Three proposals for $H_E$:

- **P1**: For each clause on $b_C$ bits, take an independent random Hermitian $A_C$ of size $2^{b_C} \times 2^{b_C}$ (off-diagonal $\mathrm{Unif}[-3,3]$-ish, diagonal = 0). Different $A_C$ per clause; breaks permutation symmetry.
- **P2**: Applies when every clause has the same $h_3$. Pick **one** $8\times 8$ Hermitian $A$ (diagonal = 0) and use it for every triple. Preserves permutation symmetry.
- **P3**: 3-SAT specific. Start with $A$ for the "reference" clause with (0,0,0) as the false assignment; generate seven other $8\times 8$ matrices by bit-negation conjugation via $\sigma_x$.

## 3  A different path can turn failure into success

The authors reexamine the example of [5]. The cost function is

$$
h_3(z,z',z'') = \begin{cases} 0 & z+z'+z''=0 \\ 3 & z+z'+z''=1 \\ 1 & z+z'+z''=2 \\ 1 & z+z'+z''=3 \end{cases}, \qquad h = \sum_{i<j<k} h_3(z_i,z_j,z_k). \tag{13,14}
$$

The global minimum is at $z_1=\dots=z_n=0$. In the symmetric subspace, using $S_z = \tfrac12 \sum_i \sigma_z^{(i)}$,

$$
H_P = \frac{3n}{2}(n/2 - S_z)(n/2 + S_z)(n/2 + S_z - 1) + \tfrac12(n/2 + S_z)(n/2 - S_z)(n/2 - S_z - 1) + \tfrac16(n/2 - S_z)(n/2 - S_z - 1)(n/2 - S_z - 2), \tag{15}
$$

$$
H_B = \binom{n-1}{2} \bigl(n/2 - S_x\bigr). \tag{17}
$$

**Failure without $H_E$**: The effective potential (large-$n$ ansatz $|\theta,\varphi\rangle$)

$$
V_0(\theta,\varphi,s) = 2(1-s)(1 - \sin\theta \cos\varphi) + \tfrac16 s\bigl(13 + 3\cos\theta - 9\cos^2\theta - 7\cos^3\theta\bigr) \tag{27}
$$

has a local minimum that a polynomial-time adiabatic run continuously tracks. That minimum starts at $\theta=\pi/2$ ($s=0$) and moves *rightward* to $\theta=\pi$ ($s=1$), i.e. $|z_1=\dots=z_n=1\rangle$, which is **not** the global minimum $|z=00\dots0\rangle$. Hence the algorithm fails at polynomial time.

**Success with a specific $H_E$**: Choose

$$
A = \begin{pmatrix}
0 & -2 & -2 & 0 & -2 & 0 & 0 & 0 \\
-2 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
-2 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 0 & 0 & 0 & 2 \\
-2 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 0 & 0 & 0 & 2 \\
0 & 0 & 0 & 0 & 0 & 0 & 0 & 2 \\
0 & 0 & 0 & 2 & 0 & 2 & 2 & 0 \\
\end{pmatrix}. \tag{28}
$$

By P2, this gives (leading order in $n$)

$$
H_E = -2n(S_x S_z + S_z S_x) + O(n^2), \qquad V_E(\theta,\varphi,s) = -8 s(1-s) \cos\theta \sin\theta \cos\varphi. \tag{29,30}
$$

Now the continuously tracked local minimum of $V = V_0 + V_E$ starting at $\theta=\pi/2$ ends at $\theta=0$, i.e., $|z=00\dots0\rangle$ — success in polynomial time.

**Random-$A$ experiment**: Draw $A$ real symmetric $8\times 8$, off-diagonal $\mathrm{Unif}[-3,3]$, diagonal $=0$. Track the local minimum of $V(\theta,\varphi,s)$ continuously in $s$ starting at $(\pi/2, 0)$. Result: **351 out of 1000 tries** end at $(0,0)$ — i.e. a large fraction of random $A$'s convert the algorithm from failure to success.

## 4  Conclusion

The straight-line path is arbitrary. Adding a path term $s(1-s) H_E$ can move the trajectory out of small-gap regions and turn an exponential-time failure into polynomial time. Suggest running adiabatic evolution repeatedly with random paths.

## Acknowledgments

Thanks to Michael Sipser and Wim van Dam. Support: DOE DE-FC02-94ER40818, NSA/ARDA/ARO DAAD19-01-1-0656.

## References

1. E. Farhi, J. Goldstone, S. Gutmann, M. Sipser, "Quantum Computation by Adiabatic Evolution", quant-ph/0001106.
2. E. Farhi et al., "A Quantum Adiabatic Evolution Algorithm Applied to Random Instances of an NP-Complete Problem", quant-ph/0104129.
3. A. M. Childs, E. Farhi, J. Preskill, "Robustness of Adiabatic Quantum Computation", quant-ph/0108048; Phys. Rev. A **65**, 012322 (2002).
4. D. Preda, "Quantum Adiabatic Evolution with a Different Path", MIT Senior Thesis, June 2002.
5. E. Farhi, J. Goldstone, S. Gutmann, "Quantum Adiabatic Evolution Algorithms versus Simulated Annealing", quant-ph/0201031.
