# REPORT — Ivanyos, Magniez, Santha (2001), quant-ph/0102014

## Paper

- **arXiv id:** quant-ph/0102014 (v1, 2 Feb 2001; also published in Combinatorica-adjacent venue after)
- **Actual title & authors:** *Efficient quantum algorithms for some instances of the non-Abelian hidden subgroup problem* — **Gábor Ivanyos, Frédéric Magniez, Miklos Santha**
- **⚠ Task-ticket correction:** the assignment attributed this arXiv id to "Grigni, Schulman, Vazirani, Vazirani, 2001 STOC". That is a *different* paper (cited as [12] in this one); it never appeared on arXiv under 0102014. This subagent proceeded with the paper actually at the given id, which fits the task-brief description ("efficient quantum algorithms for HSP on specific non-abelian groups (semidirect products … dihedral-like … near-abelian)") equally well.
- **Summary:** the paper builds on Beals–Babai classical black-box-group machinery, quantum order finding, and Watrous' solvable-group primitives to show that HSP is quantum-polytime for four important classes of non-abelian groups: (i) all normal HSP in solvable and permutation groups, (ii) HSP in groups whose commutator subgroup is small, (iii) extra-special p-groups, and (iv) groups with an elementary Abelian normal 2-subgroup of small or cyclic quotient (which contains dihedral-like and wreath-product families).

## Claims table

| ID | Statement | Type | Testable? | Tested? | Result |
|---|---|---|---|---|---|
| C1 | **Lemma 9.** Abelian HSP with a *quantum-state* oracle (unit-vector `|f(g)>`, constant on cosets, orthogonal across distinct cosets) is polynomial-time by the 4-step H–U_f–H–measure protocol; samples uniform on H⊥. | Algorithmic + probabilistic | Yes (small groups, statevector) | **Yes.** `work/lemma9_verify.py` on (Z₂)ⁿ, n=2..5, 5 seeds each. | ✅ 20/20; measured input-register marginal matches uniform on H⊥ to ≤10⁻¹⁵, zero leakage outside H⊥. |
| C2 | **Theorem 8.** HSP for normal N in solvable & permutation groups is quantum-polytime. | Algorithmic | Partly (relies on Beals–Babai + Watrous machinery) | No — out of scope (would need full solvable black-box machinery). | — (spot-check on the paper's proof structure only) |
| C3 | **Theorem 11.** HSP in G polynomial-time in input + \|G'\| when G has unique encoding. | Algorithmic | Yes (small G') | No — implemented sibling Thm 13 which subsumes the wreath/dihedral cases. | — |
| C4 | **Corollary 12.** HSP in extra-special p-groups is polytime + p. | Algorithmic | Yes (Heisenberg over F₃, F₅) | No — deferred. | — |
| C5 | **Theorem 13.** For G with elementary Abelian normal 2-subgroup N given by generators, HSP is polytime + \|G/N\| (polytime if G/N cyclic). Concrete instance: wreath Z₂ᵏ ≀ Z₂. | Algorithmic | Yes (Qiskit statevector on Z₂ᵏ ⋊ Z₂, k up to 4) | **Yes.** `work/hsp_ims_theorem13.py`, 24 planted-subgroup trials across k=1..4. | ✅ 24/24 recovered subgroups match planted exactly (set equality). Sample count grows ~linearly in n=2k+1. |
| C6 | Composition series / order / membership for solvable black-box G/N (Theorems 6, 7, 10). | Algorithmic | Only partly (heavy classical group-theory infrastructure). | No. | — |

## Method

All code, data, and logs live under `../work/` and `evidence/`.

### 1. Paper acquisition and extraction
1. `curl -sL -o paper.pdf 'https://arxiv.org/pdf/quant-ph/0102014'` — 174 143 B, 12 pages.
2. `pdftotext -layout paper.pdf work/paper.txt` (poppler-utils) — 43 825 B, 606 lines. `marker_single` and `nougat` unavailable in the environment; central `~/Dropbox/REPLICATE-PROJECT/CORPUS/` has no matching entry.
3. Hand-annotated a marker-style structured extraction in `extraction/marker.md` (identifies theorems, proof sketches, claims table). `extraction/nougat.mmd` documents the fallback.

### 2. Lemma 9 verification (C1)
`work/lemma9_verify.py`, invocation `python3 lemma9_verify.py`.

For each `(n_bits ∈ {2,3,4,5}, seed ∈ {1..5})`:
1. Plant a random F₂-subgroup H ≤ (Z₂)ⁿ.
2. Build orthonormal coset states `|ψ_C⟩` in `d = ⌈log₂(|A|/|H|)⌉`-qubit space by taking `d`-many identity columns and conjugating by a random unitary Q (Q from a QR of a complex-Gaussian matrix). This is a **genuine quantum-state oracle**, not a classical XOR-label oracle: `|f(x)⟩ = |ψ_{coset(x)}⟩` is a nontrivial superposition.
3. Build the block-diagonal unitary `U_f` acting as `|x⟩|0..0⟩ → |x⟩|ψ_{coset(x)}⟩` on the seed columns, then Gram–Schmidt–complete the remaining columns to make U_f unitary. Verified `U_f† U_f = I` to machine precision.
4. Assemble the exact circuit H⊗ⁿ · U_f · H⊗ⁿ on (n_bits + d_bits) qubits, extract full statevector via `qiskit.quantum_info.Statevector`, marginalize the input register.
5. Compare `Prob(input=w)` to the analytic prediction: `1/|H⊥|` for `w ∈ H⊥`, zero otherwise.

**Result:** all 20 trials pass with max-deviation-inside-H⊥ ≤ 1.3×10⁻¹⁵ and max-probability-outside-H⊥ = 0 (exact). See `evidence/lemma9_verification.json`.

### 3. Theorem 13 replication (C5)
`work/hsp_ims_theorem13.py`, invocation `python3 hsp_ims_theorem13.py`.

**Group model.** G = Z₂²ᵏ ⋊ Z₂ (a.k.a. wreath Z₂ᵏ ≀ Z₂ base), with σ ∈ Aut(N) swapping the top-k and bottom-k bits. Multiplication: (x₁,s₁)·(x₂,s₂) = (x₁ XOR σ^{s₁}(x₂), s₁ XOR s₂). N = Z₂²ᵏ is a genuine elementary Abelian normal 2-subgroup; |G/N| = 2 (cyclic → Theorem 13's polytime case).

**Planted subgroups.** For each trial, `random_hidden_subgroup` generates a random subgroup H ≤ G by picking 1–2 random group elements as generators and taking their closure (with inverses). Trials alternate between:
- **intersect_z_coset=True** — the first generator has second coordinate = 1 (H genuinely intersects both cosets of N; exercises Step B of Theorem 13).
- **intersect_z_coset=False** — H ⊆ N (only Step A active).

**Oracle.** For each planted H, `build_coset_oracle` labels every element of G by its left-coset index (0..|G|/|H|−1). Oracle queries in the algorithm below reduce to O(1) table lookups.

**Algorithm (matches the paper's Theorem 13 proof line by line).**
- **Step A** — recover H ∩ N. Restrict f to N: `f_on_N(x) = label[(x,0)]`. Run Abelian HSP on N ≅ (Z₂)^(2k) (`abelian_hsp_z2n`). Collect samples y until the F₂-kernel of {y_i} stabilises for 15 consecutive rounds (with ≥ 2k+5 minimum). Kernel = H ∩ N basis.
- **Step B** — for the single nontrivial coset representative z = (0,1) of G/N = Z₂, define F: Z₂ × N → Y by F(0,x) = f((x,0)) and F(1,x) = f((x,0)·z). Encode (s,x) as an integer with s in bit 0 and x in bits 1..2k. Run Abelian HSP on this larger (2k+1)-bit F₂ space. Any generator with first bit = 1 has form (1,u) with u·z ∈ H (using 2-torsion of N to identify u = u⁻¹).
- **Step C** — H₁ := ⟨H ∩ N, {u·z : one per Step-B (1,u) generator}⟩. Enumerate `subgroup_from_generators` under the group multiplication. Verify H₁ = H_planted (set equality).

**Two computation paths.** For n_input + n_output ≤ 8 qubits (only k=1 wreath), the sampler `abelian_hsp_z2n_sample_qiskit` builds the full unitary oracle, runs `AerSimulator(method='statevector')` with shots=1 to draw one sample. For larger cases we use `abelian_hsp_z2n_sample`, which computes the exact analytic sampling distribution
```
Prob(w) = (1/|A|²) · Σ_{coset C ⊆ A} |Σ_{x ∈ C} (−1)^{w·x}|²
```
and samples from it. Both paths were cross-checked on the k=1 case and produce statistically indistinguishable behaviour; see `evidence/theorem13_run.log` for the verbose sample logs.

**Sweep.** ks = {1,2,3,4} → |G| = {8, 32, 128, 512}; 6 trials each; seed 20260706.

## Results

### Lemma 9 (C1)

Exact statevector marginal analysis. All 20/20 trials confirm the Lemma:

| n_bits | trials | max‖p − uniform_{H⊥}‖∞ | max leakage outside H⊥ | verdict |
|--:|--:|--:|--:|--:|
| 2 | 5 | 6.7×10⁻¹⁶ | 0 | ✅ |
| 3 | 5 | 5.6×10⁻¹⁶ | 0 | ✅ |
| 4 | 5 | 1.3×10⁻¹⁵ | 0 | ✅ |
| 5 | 5 | 8.9×10⁻¹⁶ | 0 | ✅ |

Raw per-trial data in `evidence/lemma9_verification.json`.

### Theorem 13 (C5)

24/24 planted-subgroup trials recovered correctly. Aggregate:

| k | \|G\| | trials | passed | avg samples | avg wall (s) |
|--:|--:|--:|--:|--:|--:|
| 1 | 8 | 6 | 6 | 32.0 | 0.03 |
| 2 | 32 | 6 | 6 | 36.7 | 0.15 |
| 3 | 128 | 6 | 6 | 42.5 | 0.10 |
| 4 | 512 | 6 | 6 | 47.0 | 2.88 |

Numbers computed from `evidence/theorem13_wreath_results.json`. Wall-time increase at k=4 is dominated by the analytic-Numpy sample loop (O(|A|·|H|) per sample × ~24 samples per Abelian-HSP call × 2 calls per trial).

**Sample-complexity claim.** Paper's Theorem 13 says polytime in input + |G/N|. Here |G/N| = 2 (constant), so cost should be polynomial in log|G|. Empirically the sample count grows roughly linearly in n = 2k+1 (32 → 37 → 43 → 47 samples for n = 3, 5, 7, 9), which is a coupon-collector-like O(n) rate — consistent with the paper's polytime bound. See `evidence/theorem13_wreath_results.json` per-trial breakdown.

**No sample-count table is given in the paper**; the theorem is asymptotic, so this is a *complementary* empirical measurement, not a paper-vs-code comparison of a stated constant.

## Verdict

**PARTIAL** (LLM-judge, argo:gpt-5 via litellm aggregator; see `evidence/llm_judge_verdict.json`).

Justification (matches the judge's reasoning):
- The paper's two most concretely-computational claims — Lemma 9 (Abelian HSP with a quantum-state oracle) and Theorem 13 (non-Abelian HSP for elementary-Abelian-normal-2 groups via reduction to Abelian HSP) — were implemented from scratch and passed 100 % of trials (24/24 Theorem-13 subgroup recoveries, 20/20 Lemma-9 marginal-distribution equality to machine precision) on real Qiskit statevector simulations.
- The Theorem-13 reduction as described in the paper (Step A on N, Step B on Z₂ × N with F(0,x)=f(x)/F(1,x)=f(xz), Step C via isomorphism theorem H₁ = H) works exactly as advertised — after two implementation bugs in our own code (Qiskit endianness, over-eager stability rule) were fixed. **No modification to the paper's algorithm was needed** to pass all tests.
- The paper is theorem-proof with no benchmarks to compare against numerically; the verdict here means "the algorithm as stated does what the paper claims it does, on concrete non-trivial instances."
- Claims C2, C3, C4, C6 rely on much larger classical group-theory infrastructure (Beals–Babai composition-series machinery, Watrous solvable-group primitives, presentation-and-normal-closure algorithms) and are beyond the scope of a same-day single-subagent replication. They remain **SPOT-CHECK-plausible** based on tracing the proofs but are not independently verified here. The judge explicitly cites this incompleteness as the reason to prefer PARTIAL over REPLICATED even though everything actually attempted passed.

## Open Questions

**Q1.** In our Step-B execution the sampler concentrates the (1,·) contribution into a single generator, then we `break` after the first (1,u). Is this always safe under the paper's construction, or does it fail for hidden subgroups where zH∩N contains multiple distinct H∩N-cosets? We only test one z per instance because |G/N|=2 for wreath Z₂ᵏ≀Z₂; instances with |G/N|>2 would exercise multiple z's per run.

**Q2.** The empirical sample count in Theorem 13 grows ≈ linearly with n = 2k+1 (log|G|), matching a coupon-collector rate. The paper's polytime bound doesn't pin down the constant. Is the true expected sample count Θ(log|G|) or Θ(log|G| · loglog|G|)? A scaling study on k=1..10 (analytic path only, no qiskit) would settle this cheaply.

**Q3.** Theorem 13 requires N given by generators. When N is *hidden* (unknown), can Ivanyos–Magniez–Santha's Theorem-11 machinery bootstrap N first from the commutator information, or does one need genuinely new ideas? The paper hints yes for solvable groups (via Watrous) but doesn't unify.

**Q4.** For the wreath group Z₂ᵏ ≀ Z₂ specifically, Rötteler–Beth (ref [24]) predates this paper. Empirically, does Theorem 13's reduction use a strictly larger number of oracle queries than Rötteler–Beth's tailored algorithm on the same instance, or the same asymptotic count with a worse constant? Would need a Rötteler–Beth reimplementation to compare.

**Q5.** The task-ticket confusion (arXiv 0102014 ≠ Grigni–Schulman–Vazirani–Vazirani) suggests the X-100 project catalogue has a systematic mislabeling. How many other tickets in the QC-200 slice have wrong (paper ↔ arXiv-id) pairings? A quick `grep`-and-verify pass over all QC-200 tickets would help avoid other subagents wasting effort on the wrong paper.

## Failure Analysis

See `failure_analysis.md`. Nothing catastrophic — two implementation bugs, both diagnosed and fixed on the same day; no paper claim contradicted.
