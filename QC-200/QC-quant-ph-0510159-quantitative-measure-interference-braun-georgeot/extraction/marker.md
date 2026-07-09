# A Quantitative Measure of Interference

**Authors:** Daniel Braun and Bertrand Georgeot
**Affiliation:** Laboratoire de Physique Théorique, UMR 5152 du CNRS, Université Paul Sabatier, 118, route de Narbonne, 31062 Toulouse, FRANCE
**arXiv:** quant-ph/0510159 v1 (20 Oct 2005)
**PACS:** 03.67.-a, 03.67.Lx

## Extraction note

`marker` was not installed on the replication host and the central pre-parsed corpus
did not contain a Marker parse for this paper. This file is a `pdftotext -layout`
fallback (777 lines) that preserves the two-column layout well enough for text
mining. See `extraction/pdftotext_layout.txt` for the raw dump and
`extraction/nougat.mmd` for a math-oriented parse (also fallback). The paper is
short (10 pages) and the equations we needed (Eq. 6, Eq. 7, Eq. 8) were extracted
by hand from the PDF; verbatim renderings are in the report.

---

## Abstract

We introduce an interference measure which allows to quantify the amount of
interference present in any physical process that maps an initial density matrix
to a final density matrix. In particular, the interference measure enables one
to monitor the amount of interference generated in each step of a quantum
algorithm. We show that a Hadamard gate acting on a single qubit is a basic
building block for interference generation and realizes one bit of interference,
an "i-bit". We use the interference measure to quantify interference for various
examples, including Grover's search algorithm and Shor's factorization algorithm.
We distinguish between "potentially available" and "actually used" interference,
and show that for both algorithms the potentially available interference is
exponentially large. However, the amount of interference actually used in
Grover's algorithm is only about 3 i-bits and asymptotically independent of the
number of qubits, while Shor's algorithm indeed uses an exponential amount of
interference.

## Key formulas

**Definition (Eq. 6) — general propagator P:**

$$
I(P) \;=\; \sum_{i,k,l} |P_{ii,kl}|^2 \;-\; \sum_{i,k} |P_{ii,kk}|^2
$$

**Unitary case (Eq. 8), P_{ii,kl} = U_{ik} U_{il}^*:**

$$
I(P(U)) \;=\; N \;-\; \sum_{i,k} |U_{ik}|^4
$$

with $0 \le I(P(U)) \le N-1$, saturated by unitaries whose column-IPRs are all
$1/\sqrt N$ (Cauchy-Schwarz bound).

**i-bit unit:** the interference bits are $n_I = \log_2(I+1)$ so that a single
Hadamard (I = 1) gives 1 i-bit and the Walsh-Hadamard $W_n$ (I = 2^n - 1) gives
n i-bits.

(See `work/paper.txt` lines 130-210 for the full derivation in the paper.)

## Sections

- I.  Introduction
- II. The essence of interference
- III. Definition — general propagator (Eq. 6, Eq. 7)
- IV.A. Unitary case (Eq. 8)
- IV.B. Properties: invariances, factorization
- IV.A.4. The i-bit and the Hadamard gate
- IV.C. Beam splitter and Mach-Zehnder
- IV.D. Decoherence / bit-flip / phase errors and teleportation
- IV.E. Shor's algorithm
- IV.F. Grover's algorithm
- V.  Discussion

## Numeric claims tested in this replication

| Object                 | Paper claim                | Notes                              |
|------------------------|----------------------------|------------------------------------|
| Identity, X, Y, Z, CNOT, SWAP, CCX | I = 0            | permutation / diagonal → 0         |
| Hadamard (1 qubit)     | I = 1 (1 i-bit)            | Sec. IV.A.4                        |
| Walsh-Hadamard W_n     | I = 2^n - 1 (n i-bits)     | tensor of H's                      |
| QFT_n                  | I = N - 1 = 2^n - 1        | maximal (all |U_ik|² = 1/N)        |
| Beam splitter U_BS(θ)  | I = 2(1 - cos⁴θ - sin⁴θ)   | Sec. IV.C                          |
| Teleportation encoder  | I = 6                      | Sec. IV.D                          |
| Grover, n=8, full      | I ≈ 2^n - 2 = 254          | Sec. IV.F Fig. 6                   |
| Grover "actually used" | asymp. → 8 (~3 i-bits)     | 24/N + O(1/N²), Sec. IV.F Fig. 7   |
| Tensor factor rule     | (N_AB - I(A⊗B)) = (N_A-I(A))·(N_B-I(B)) | derived from Eq. 8 |
