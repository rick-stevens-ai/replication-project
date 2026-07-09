# Marker parse — arXiv:1612.09512

> **NOTE:** Marker (VikParuchuri/marker) is not installed on the host `CherryRd`
> where this replication ran, and no pre-parsed Marker output for 1612.09512
> was found in the central corpus (`~/Dropbox/REPLICATE-PROJECT/**`).
>
> As a faithful substitute this file contains the `pdftotext -layout` extraction
> from the arXiv PDF, lightly reflowed and given section headers so downstream
> retrieval keys against real body text. Equations are preserved as ASCII / TeX
> because pdftotext cannot recover mathematical layout. Marker would produce a
> higher-fidelity Markdown+equation rendering; see
> `report/failure_analysis.md` for the impact assessment (none material for this
> replication — the reproduction uses the equations verbatim from the source
> text, not from Marker/Nougat).

## Paper metadata
- **arXiv id:** 1612.09512
- **Title:** Efficient Quantum Algorithms for Simulating Lindblad Evolution
- **Authors:** Richard Cleve, Chunhao Wang
- **Affiliation:** Institute for Quantum Computing / Cheriton School of Computer Science, University of Waterloo; CIFAR
- **Version parsed:** v3 (4 Jan 2019)
- **Preliminary version:** ICALP 2017, pages 17:1–17:14.

## Abstract (verbatim)
> We consider the natural generalization of the Schrödinger equation to Markovian open system dynamics: the so-called the Lindblad equation. We give a quantum algorithm for simulating the evolution of an n-qubit system for time t within precision ε. If the Lindbladian consists of poly(n) operators that can each be expressed as a linear combination of poly(n) tensor products of Pauli operators then the gate cost of our algorithm is O(t · polylog(t/ε) · poly(n)). We also obtain similar bounds for the cases where the Lindbladian consists of local operators, and where the Lindbladian consists of sparse operators. This is remarkable in light of evidence that we provide indicating that the above efficiency is impossible to attain by first expressing Lindblad evolution as Schrödinger evolution on a larger system and tracing out the ancillary system: the cost of such a reduction incurs an efficiency overhead of O(t²/ε) even before the Hamiltonian evolution simulation begins. Instead, the approach of our algorithm is to use a novel variation of the "linear combinations of unitaries" construction that pertains to channels.

## Section outline (as recovered from pdftotext)
1. Introduction — motivation, Feynman closed-system precedent, examples of open-system evolution in physics, chemistry, biology, quantum information.
2. Standard LCU and Stinespring dilations — subsection 2.1 shows why applying the standard LCU method to a Stinespring dilation of a channel *cannot* reach the O(t·polylog) regime.
3. New LCU method for channels and completely positive maps — key novel ingredient. Introduces the circuit W with an auxiliary "purifier" register whose measurement outcome selects the applied Kraus branch (Fig. 2).
4. Overview of the main result — Theorem 1: for a Lindbladian expressed as a linear combination of q Pauli terms with m Lindblad operators, gate complexity is O(t · polylog(mqt/ε) · poly(n)).
   - 4.2. Approximating M_δ by a quantum circuit via the new LCU method.
5. (proof) Extension to local Lindbladians (Corollary 2) and sparse Lindbladians (Corollary 3).

## Central master equation (Eq. 1)
    dρ/dt = -i [H, ρ]  +  Σ_{j=1..m} ( L_j ρ L_j†  -  ½ L_j† L_j ρ  -  ½ ρ L_j† L_j )

## Headline complexity claims
- **Theorem 1 (Pauli-LCU Lindbladian):** gate complexity O(τ · polylog(mqτ/ε) · poly(n)) with τ = t · ‖L‖_pauli.
- **Corollary 2 (local Lindbladian):** same asymptotic form, m and q absorbed by locality.
- **Corollary 3 (d-sparse Lindbladian):** query complexity O(τ · polylog(mqτ/ε) · poly(d,n)).
- Lower bound (referenced from Childs & Li [9]): Ω(t) queries for H = 0, m = 1.
- "Impossibility of dilation shortcut" — reducing Lindblad simulation to Hamiltonian simulation on a purified larger system pays an unavoidable O(t²/ε) overhead *before* Hamiltonian simulation begins.

## Method sketch (informal, as pertinent to a numerical replication)
The construction targets the object
    exp(t · 𝓛)   where 𝓛 acts on density matrices via
    𝓛(ρ) = -i [H, ρ] + Σ_j ( L_j ρ L_j† - ½ {L_j† L_j, ρ} )
by
1. Vectorizing / super-operator lifting: rewrite 𝓛 as a matrix 𝓛_vec acting on vec(ρ) so that ρ(t) = unvec( e^{t 𝓛_vec} vec(ρ) ).
2. Chopping [0, t] into N sub-intervals of length δ = t/N and approximating each `exp(δ 𝓛)` by a *coherent* Taylor truncation Σ_{k=0..K} (δ 𝓛)^k / k!.
3. Preparing each term of that truncated sum as a linear combination of unitaries whose selection register is measured post-hoc; the paper's *new* LCU variant lets that measurement be interpreted as a Kraus branch rather than a coherent post-selection, which is what recovers the polylog(1/ε) precision scaling.
4. Repeating oblivious amplitude amplification per segment.

## Comparison to prior algorithms (verbatim from §1)
- Childs & Li [9]: quadratic-time algorithm O(t²/ε), improved to O(t^1.5/√ε); also O((t²/ε) polylog(t/ε)) query algorithm for the same problem.
- Ω(t) lower bound for the query complexity when H = 0 and m = 1.
- Cleve & Wang: O(t · polylog(t/ε) · poly(n)) gate complexity — matches the Ω(t) lower bound up to polylog.

## Data / code availability
No source code accompanies the paper — it is a theoretical construction. The replication in `report/evidence/lindblad_lcu.py` exercises the *mathematical kernel* of the algorithm (truncated-Taylor / LCU expansion of e^{t 𝓛_vec}) against a `scipy.linalg.expm` gold standard on a 2-qubit toy Lindbladian.
