# Marker-style extraction (via pdftotext fallback)

**Note:** `marker_single` unavailable in this environment. Extraction done via `pdftotext -layout` (poppler) which produces high-fidelity plain text for this LaTeX-typeset paper. Full raw text preserved in `../work/paper.txt` (43 KB, 606 lines).

## Paper identification (IMPORTANT — task-assignment correction)

- **arXiv id:** quant-ph/0102014
- **Actual title:** *Efficient quantum algorithms for some instances of the non-Abelian hidden subgroup problem*
- **Actual authors:** **Gábor Ivanyos, Frédéric Magniez, Miklos Santha** (Hungarian Academy of Sciences + CNRS-LRI, Orsay)
- **Date on arXiv:** 2 Feb 2001
- **Task assignment said:** "Grigni, Schulman, Vazirani, Vazirani, 2001 STOC" — that is a *different* paper, cited as **[12]** in this one. The GSV V STOC 2001 paper ("Quantum mechanical algorithms for the nonabelian hidden subgroup problem") was never posted to arXiv under 0102014. This subagent proceeded with the actual paper at the given arXiv id.

## Abstract (verbatim)

> In this paper we show that certain special cases of the hidden subgroup problem can be solved
> in polynomial time by a quantum algorithm. These special cases involve finding hidden normal
> subgroups of solvable groups and permutation groups, finding hidden subgroups of groups with
> small commutator subgroup and of groups admitting an elementary Abelian normal 2-subgroup
> of small index or with cyclic factor group.

## Section-by-section content

### 1. Introduction
Motivates non-Abelian HSP (contains graph isomorphism), reviews prior work: Rötteler-Beth (Z_2^k ≀ Z_2), Ettinger-Høyer (dihedral, only O(log|G|) queries but exponential classical post-processing), Ettinger-Høyer-Knill (query-lower-bound style), Hallgren-Russell-Ta-Shma (normal subgroups when Fourier transform is efficient), Grigni-Schulman-Vazirani-Vazirani (large normalizer-intersection), Watrous (solvable black-box groups). Uses Beals–Babai [5] as classical backbone.

### 2. Preliminaries — black-box groups
- G encoded by binary strings length n; oracle U_G |g⟩|h⟩ = |g⟩|gh⟩ and inverse.
- Encoding need not be unique; then identity-test oracle is needed.
- **Theorem 1 (Cheung-Mosca):** Abelian black-box group with unique encoding → decomposition into cyclic prime-power summands in polytime by quantum.
- **Theorem 2 (Watrous):** Solvable black-box group with unique encoding → order + membership in polytime by quantum; also produce |N⟩ = |N|^{-1/2} Σ_{x∈N} |x⟩ efficiently.
- **Theorem 3 (Mosca):** Abelian HSP solvable in polytime by quantum.

### 3. Group algorithms (Beals–Babai)
- Parameter ν(G) = smallest ν such that every non-Abelian composition factor of G has a faithful permutation representation of degree ≤ ν. ν(solvable)=1.
- **Theorem 4 (Beals-Babai):** Given (a) superset of primes dividing |G|, (b) discrete-log oracle in fields ≤|G|, (c) constructive-membership-test oracle in elementary Abelian subgroups → Las Vegas polytime algorithms for: membership test, order+presentation, center generators, composition series, Sylow subgroups.
- **Corollary 5:** Replace (a)+(b) by order-of-element oracle; task list extended to constructive membership in G.

### 4. Quantum implementations
- **Theorem 6 (unique encoding):** All Corollary 5 tasks solvable in quantum polytime + ν(G). Proof reduces constructive Abelian membership to Abelian HSP via homomorphism φ(α_1,…,α_r,α) = h_1^{α_1}⋯h_r^{α_r} g^{-α}.
- **Theorem 7 (hidden normal N):** Corollary 5 tasks for G/N by same reduction with φ(α)=f(h_1^{α_1}⋯g^{-α}).
- **Theorem 8:** For normal hidden N, generators of N recoverable in polytime + ν(G/N). In particular solvable and permutation groups → normal HSP polytime.

- **Lemma 9 (Abelian HSP with quantum-state oracle):** Let A Abelian, X finite set, H ≤ A, f: A → C^X (unit vectors, constant on left cosets of H, orthogonal across distinct cosets). Then H is found by polytime quantum. Proof = standard Abelian HSP algorithm:
    1. Prepare |1_G⟩|0^m⟩
    2. QFT on first register: Σ_{g∈A} |g⟩|0^m⟩
    3. Call f: Σ_{g∈A} |g⟩|f(g)⟩
    4. QFT again: Σ_{g∈A/H, h∈H^⊥} χ_h(g) |h⟩|f(g)⟩
    5. Measure first register → uniform distribution on H^⊥.

- **Theorem 10 (unique encoding + solvable normal N given by generators):** Corollary 5 tasks for G/N in polytime + ν(G/N). Uses Lemma 9 with quantum function f(k)=|g^k N⟩ (Watrous' |N⟩ state).

### 5. Groups with small commutator subgroup G'
- **Theorem 11:** HSP in G in time polynomial in input + |G'|. Idea: F(x) = {f(xg) | g∈G'} hides HG' (which is normal since G/G' Abelian) → Theorem 8; then enumerate cosets of G' inside each generator of HG' to find members of H.
- **Corollary 12:** Extra-special p-groups → HSP in polytime + p.

### 6. Groups with a large elementary Abelian normal 2-subgroup N
- **Theorem 13:** For N normal elementary Abelian 2-subgroup given by generators, HSP in G solvable in polytime + |G/N|. If G/N cyclic → polytime.
- Proof construction: for each z in a coset-representative set V of G/N, define F: Z_2 × N → Y by F(0,x)=f(x), F(1,x)=f(xz). Then F hides either {0}×(H∩N) or ({0}×(H∩N)) ∪ ({1}×u(H∩N)) for some u ∈ zH ∩ N. Since Z_2 × N is elementary Abelian 2-group, Abelian HSP recovers this in polytime → gives u^{-1}z ∈ H. Union with H∩N (Abelian HSP inside N) generates a subgroup H_1 with H_1 ∩ N = H ∩ N and H_1 N = HN → H_1 = H by isomorphism theorem.
- Includes wreath products Z_2^k ≀ Z_2 (Rötteler-Beth [24]) and dihedral D_{2^k} as special cases.

## Claims table

| ID | Statement | Type | Testable? |
|---|---|---|---|
| C1 | Abelian HSP with unit-vector coset-orthogonal quantum oracle → polytime quantum recovery of H (Lemma 9). | Algorithmic | Yes, small groups |
| C2 | HSP for normal N in solvable & permutation groups → polytime quantum (Theorem 8). | Algorithmic | Yes, small groups |
| C3 | HSP in G polytime + |G'| when unique encoding (Theorem 11). | Algorithmic | Yes, small G' |
| C4 | HSP in extra-special p-groups → polytime + p (Corollary 12). | Algorithmic | Yes, Heisenberg over F_p |
| C5 | HSP in G with elem-Abelian normal 2-subgroup N → polytime + |G/N|; polytime if G/N cyclic (Theorem 13). | Algorithmic | Yes, D_{2^k}, Z_2^k ⋊ Z_2 |
| C6 | Composition-series/order/membership for solvable black-box G/N (Theorems 6,7,10). | Algorithmic | Only partly (heavy) |
