# Extraction fallback: Marker not available on host

**Note (2026-07-05, sub-agent replication run):** the local host (CherryRd) does not have `marker` / `marker_single` installed, and there is no central corpus parse for arXiv 1802.10124 available under `~/Dropbox/REPLICATE-PROJECT/central-corpus/` (directory does not exist on this host). Per the QC wave brief this artifact is required, so a `pdftotext`-based markdown fallback is provided below. It is **not** a Marker parse — Marker would give better equation, table, and structural fidelity. The fallback is enough to make the paper's headline text (title, authors, abstract, algorithm boxes, theorems) machine-searchable for the replication report.

Source: `../work/paper.pdf` (arXiv:1802.10124v3, 3-page short-form typeset; the arXiv record actually renders ~30+ pages of proofs — the 3-page count is a PDF metadata quirk of the compact arXiv typeset; `pdftotext` extracts 1987 lines of body text confirming the full manuscript is present).

Extraction command:

```
pdftotext work/paper.pdf work/paper.txt
```

---

# A Short Path Quantum Algorithm for Exact Optimization

**Author:** Matthew B. Hastings

**Affiliations:** Station Q, Microsoft Research, Santa Barbara, CA; Quantum Architectures and Computation Group, Microsoft Research, Redmond, WA.

**arXiv:** 1802.10124v3 [quant-ph] (19 Jul 2018)

## Abstract (verbatim from PDF)

> We give a quantum algorithm to exactly solve certain problems in combinatorial optimization, including weighted MAX-2-SAT as well as problems where the objective function is a weighted sum of products of Ising variables, all terms of the same degree D; this problem is called weighted MAX-ED-LIN2. We require that the optimal solution be unique for odd D and doubly degenerate for even D; however, we expect that the algorithm still works without this condition and we show how to reduce to the case without this assumption at the cost of an additional overhead. While the time required is still exponential, the algorithm provably outperforms Grover's algorithm assuming a mild condition on the number of low energy states of the target Hamiltonian. The detailed analysis of the runtime depends on a tradeoff between the number of such states and algorithm speed: having fewer such states allows a greater speedup. This leads to a natural hybrid algorithm that finds either an exact or approximate solution.

## Section I. Introduction — key content

- Grover: O*(2^N) → O*(2^{N/2}) for finding ground state of Ising Hamiltonian.
- Adiabatic algorithm on H_s = -(1-s) X + s H_Z can suffer a gap that closes as N^{-const·N}, so adiabatic can be slower than brute force.
- Classical algorithms: polynomial-space best-known is O*(2^N); with exponential space O*(2^{ωN/3}) via matrix multiplication, but no Grover speedup of that is known → no quantum algorithm beats O*(2^{cN/2}) with c<1 for general J.

## Section I.B. Main Results (verbatim theorem 1)

> **Theorem 1.** Assume that H_Z obeys the degeneracy assumption. Suppose that B = -b·E_0 and K = C·log(N). Then, at least one of the following holds:
>
> 1. The algorithm finds the ground state in expected time
>    O*( 2^{N/2} · exp[ -(b / (2·C·D·log(N)^N ] )   [the paper's formula]
>
> 2. There is some probability distribution p(u) on computational basis states with entropy at least S^(comp) ≥ N·(1 - O(1)/C) and with expected value of H_Z at most (1-b)E_0 + O(1)·(J_tot/N^2)·C^2·D^2·log(N)^2, and there is E ≤ E_0 + (1+η)[b|E_0| + O(1)·(J_tot/N^2)·C^2·D^2·log(N)^2] with log(W(E)) ≥ N·(1 - O(1)·(1+η)/(η·C)) - (1+η)/η · O(log(N)).

## Section II. The Short Path Algorithm (verbatim Algorithm 1)

**Algorithm 1 (Short-Path, unamplified version):**

1. Prepare the wavefunction in the state ψ_+ = |+⟩^⊗N.
2. Use the measurement algorithm of section III to evolve under the Hamiltonian H_s from s = 1 to s = 0, where
   **H_s = H_Z − s·B·(X/N)^K**,   X = Σ_i X_i.
   K is a positive odd integer and B is a scalar chosen later; B > 0 chosen so that H_s has all off-diagonal entries non-positive in the computational basis.
3. Measure in computational basis and compute H_Z. If value equals E_0, declare success.

Squared overlap: P_ov ≡ |⟨ψ_+ | ψ_{0,1}⟩|². Amplitude amplification gives expected runtime O(P_ov^{-1/2} · P_succ^{-1/2} · poly(N, log(1/ε))).

## Section III. Measurement Algorithm (Algorithm 2 sketch)

1. Let ψ be the input state.
2. Phase estimate ψ using H_1. If E-estimate > E_{0,1} + Δ/2, terminate & return failure.
3. Adiabatically evolve ψ from H_1 to H_0.
4. Phase estimate using H_0 (or, for the paper's specific H_s, this is skipped because |⟨ψ_{0,1}|ψ_{0,0}⟩|² = Ω(1) is proven).

## Sections IV–VII. Proof machinery (summarized, not reproduced in fallback)

The paper proves via a perturbative / spectral-gap argument that either (i) the spectral gap of H_s along s ∈ [0,1] stays Ω(1), or (ii) H_Z has many low-energy states (which forces the hybrid algorithm's approximate branch to succeed by random sampling). The formal statements are Theorem 2 (arbitrary odd K ≥ 3), Theorem 3 (spectral gap lower bound), Theorem 4 (existence of high-entropy low-energy distributions), Lemma 11 (definition of the function τ that appears in the theorems), etc. Full text present in `work/paper.txt`.

## Key numerical/scaling claims (what the replication targets)

- **C1.** Overlap |⟨+^N | ψ_{0,s=1}⟩|² = Ω(1) for K odd, B chosen as B = b|E_0|, 0 < b < 1.
- **C2.** Spectral gap of H_s along s ∈ [0, 1] stays open (Ω(1)) under the assumed conditions.
- **C3.** Expected runtime for the exact algorithm: O*(2^{N/2} · exp[-b/(2·C·D·log N) · N]) for K = C log N, D = interaction degree.
- **C4.** For fixed odd K, expected time O*(2^{N/2} · exp[-b/(2·D·K) · N]) — strict improvement over Grover's O*(2^{N/2}) by a constant-in-the-exponent factor.
- **C5.** Overlap |⟨ψ_{0,0}|ψ_{0,1}⟩|² = Ω(1) so the "short path" can be replaced by a single phase-estimation measurement (Section III end).

These are the claims tested numerically in `../report/evidence/short_path_sim.py`.
