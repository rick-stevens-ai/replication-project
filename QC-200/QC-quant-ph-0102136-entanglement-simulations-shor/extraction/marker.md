# Surrogate Marker extraction — arXiv:quant-ph/0102136v2

**Note:** The Marker CLI (`marker_single`) is not installed on this host
(CherryRd, 2026-07-05). Neither is Nougat (`nougat`). This file is a
best-effort surrogate extraction produced by `pdftotext -layout` and
lightly cleaned. The layout-preserved raw form is in
`../work/paper.txt`.

---

# Entanglement Simulations of Shor's Algorithm

S. Parker and M. B. Plenio
Optics Section, The Blackett Laboratory, Imperial College, London SW7 2BW, England
(arXiv:quant-ph/0102136v2, 12 Sep 2001)

## Abstract

We demonstrate that, in the case of Shor's algorithm for factoring,
highly mixed states will allow efficient quantum computation, indeed
factorization can be achieved efficiently with just one initial pure
qubit and a supply of initially maximally mixed qubits (S. Parker and
M. B. Plenio, Phys. Rev. Lett., 85, 3049 (2000)). This leads us to ask
how this affects the entanglement in the algorithm. We thus investigate
the behavior of entanglement in Shor's algorithm for small numbers of
qubits by classical computer simulation of the quantum computer at
different stages of the algorithm. We find that entanglement is an
intrinsic part of the algorithm and that the entanglement through the
algorithm appears to be closely related to the amount of mixing.
Furthermore, if the computer is in a highly mixed state any attempt to
remove entanglement by further mixing of the algorithm results in a
significant decrease in its efficiency.

PACS: 03.67.-a, 03.67.Lk

## Section headings (as detected)

- I. Outline of Shor's algorithm
  - A. The algorithm
  - B. Decomposition into basic gates
- II. Simulating quantum algorithms
- III. Entanglement measures and mixed states
  - A. Entanglement measures for pure states
  - B. (Numbered entanglement measure axioms)
  - C. A measure of entanglement for mixed states  — introduces
    log-negativity `Eneg = log Tr|rho^{T_1}| = log Tr|rho^{T_2}|` (Eq. 18)
- IV. Multipartite entanglement
- V. Simulations
  - A. Simulations
  - B. Noise
  - C. Mixing of the control qubit
  - D. (details)
- VI. Results — focused on N = 15, a = 2 (period r = 4) and
  N = 21, a = 2 (period r = 6). Figures 7-10 plot noise robustness;
  Figures 11-14 plot average bipartite log-negativity vs mixing
  parameter epsilon; Figures 15-16 collapse the results to prob-of-
  finding-r vs avg entanglement.
- VII. Conclusions — entanglement is intrinsic to Shor even in
  highly mixed regime; forcibly removing entanglement (further mixing)
  reduces efficiency.

## Central quantitative claims (extracted from body + figs)

1. **Entanglement measure**: log-negativity Eneg = log Tr|rho^{T_A}|
   (Eq. 18), applied to every bipartite partitioning of the register.
2. **Average bipartite entanglement across all 2^{n-1}-1 partitions**
   is the main summary quantity plotted.
3. For N=15, a=2, r=4, pure state at epsilon=0:
   - After controlled-U_a stages: nonzero
   - After (non-selective) measurements: much smaller / near zero
   (see Figs. 11, 15).
4. For the mixed-state algorithm, avg entanglement reaches 0 at
   epsilon ~ 0.396 (before max-mixed epsilon = 0.5).
5. Classical randomness (fully-mixed algorithm) reduces the algorithm
   to random guessing.

## Notes on the surrogate

- Reference numbers ([1]--[41]) preserved by pdftotext with mangled
  spacing.
- All figures appear as text captions (Fig. 1 through Fig. 16) plus
  raster axes; numerical values were read from figure ranges by human
  inspection, not extracted programmatically.
