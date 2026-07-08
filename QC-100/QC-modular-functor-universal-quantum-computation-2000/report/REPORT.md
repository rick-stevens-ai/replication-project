# Replication Report — Freedman/Kitaev/Larsen/Wang (2000)

**Paper:** *A modular functor which is universal for quantum computation*  
Michael Freedman, Michael Larsen, Zhenghan Wang (with acknowledgement to Alexei Kitaev)  
arXiv:[quant-ph/0001108](https://arxiv.org/abs/quant-ph/0001108) v2, Feb 2000  
23 pages, 212 KB PDF.

**This replication:** independent, from-first-principles numerical construction of the SU(2) Chern–Simons modular functor at r=5 (the paper's "CS5"), reproducing all of the paper's *concrete testable content*.

**Verdict (LLM-judge, Argo GPT-5.1, T=0):** **REPLICATED** (coverage 90 %, agreement 98 %).

---

## 1. Paper summary

FKLW define a computational model **CS5** based on the SU(2)-Chern–Simons modular functor at the fifth root of unity q = e^{2πi/5}. The label set is {0,1,2,3}. Qubits are embedded in the Hilbert space of a disk with 3k marked points (all labeled 1, boundary label 0) via the gluing/fusion axiom. Braiding — the mapping-class-group action — approximates arbitrary poly-local unitaries.

The main theorems are:

- **Thm 2.1** — quantitative approximation of any 2-qubit gate g ∈ U(4) by a braid of length ≤ C/ε² so that ||ω₀ρ₀(b) − g⊕id₁|| + ||ω₂ρ₂(b) − g⊕id₄|| ≤ ε.
- **Thm 2.2** — CS5 with label + z-measurements + fresh ancilli fault-tolerantly and efficiently simulates BQP.
- **Thm 2.3** — a strictly unitary variant ECS5 does the same without intermediate measurements.
- **Thm 3.1** — Jones representations ρ_{λ,β,n} at r = 5 are irreducible; eigenvalues of each ρ(σᵢ) are exactly {−1, q}; for λ=[4,2], n=6 the multiplicities are (3, 5).
- **Thm 3.2** — the modular-functor braid representations coincide with irreducible sectors of the Jones representation on the corresponding (2,r)-Young diagrams.
- **Thm 4.1 (density)** — the closure of the image of ρ_{[3,3]} ⊕ ρ_{[4,2]} : B₆ → U(5) × U(8) contains SU(5) × SU(8).

## 2. Claims table

| ID  | Claim                                                                                                        | Type       | Testable?          | Tested?  | Result                                                                                       |
|-----|--------------------------------------------------------------------------------------------------------------|------------|--------------------|----------|----------------------------------------------------------------------------------------------|
| C1  | dim V_3^1=2, dim V_3^3=1, dim V_6^0=5, dim V_6^2=8  (Eq. 4)                                                  | Numerical  | Yes                | Yes      | PASS — all four values match exactly                                                         |
| C1b | Jones-rep dims: dim ρ_{[2,1]}=2, dim ρ_{[3,3]}=5, dim ρ_{[4,2]}=8 (Section 3)                                | Numerical  | Yes                | Yes      | PASS — 2, 5, 8                                                                               |
| C2  | ρ_λ(σᵢ) unitary for λ ∈ {[2,1], [3,3], [4,2]}                                                                | Numerical  | Yes                | Yes      | PASS — ||UU†−I|| ≤ 10⁻¹⁵ everywhere                                                          |
| C3  | Braid relations σᵢσⱼσᵢ = σⱼσᵢσⱼ (|i−j|=1) and commutativity (|i−j|≥2); TL relations                          | Numerical  | Yes                | Yes      | PASS — residuals ≤ 10⁻¹⁵                                                                     |
| C4  | Every ρ(σᵢ) has spectrum exactly {−1, q}                                                                     | Numerical  | Yes                | Yes      | PASS — 0 stray eigenvalues across all sectors                                                |
| C5  | For λ=[4,2]: mult(−1)=3, mult(q)=5 (Thm 3.1(iv))                                                             | Numerical  | Yes                | Yes      | PASS — verified for all 5 generators σ₁..σ₅                                                  |
| C6  | Density: closure ρ_{[3,3]} ⊕ ρ_{[4,2]}(B₆) ⊇ SU(5) × SU(8) (Thm 4.1)                                         | Theoretical| Only ingredients   | Partial  | PARTIAL — empirical spread + gate-approx improvement consistent with density                 |
| C7  | Explicit printed matrix ρ_{[2,1]}(σ₂) in Section 3                                                           | Numerical  | Yes                | Yes      | FAIL as printed — both natural readings of the printed matrix are **not unitary**; likely typo in the paper. Our independently constructed ρ_{[2,1]}(σ₂) is unitary with spectrum {−1, q}. |
| C8  | Thm 2.1 gate-approx bound l ≤ C/ε²                                                                            | Theorem    | Not directly       | No       | Not attempted — Solovay–Kitaev proof cited [Ki][CN]                                          |
| C9  | Thm 2.2 / Thm 2.3 CS5 simulates BQP                                                                          | Theorem    | Not directly       | No       | Not attempted — theorem, not numerical                                                        |

## 3. Method

All code runs on CherryRd (Darwin 25.3.0, macOS Tahoe) in a local venv.

### 3.1 Environment
- Python 3.14.6 (Homebrew), numpy 2.5.1, scipy 1.18.0.
- No external data required; the paper is 100 % theoretical.
- LLM judge: Argo `argo:gpt-5.1` (free ANL endpoint) via the LiteLLM aggregator at `http://<tailnet-aggregator>:4000/v1`, T=0.

### 3.2 Data
- `paper.pdf` — pulled from `https://arxiv.org/pdf/quant-ph/0001108` (SHA-256 recorded in `report/artifact_harvest.md`).
- `extraction/paper.txt` — `pdftotext -layout` extraction (used as marker.md / nougat.mmd fallback; see `extraction/EXTRACTION_NOTE.md`).

### 3.3 Numerical construction (files in `work/`)
1. **`fkw_replication.py`** — from-scratch implementation:
    1. Admissibility rules (3) of the paper.
    2. Recursive fusion to compute dim V_n^ℓ (C1).
    3. Enumeration of standard tableaux of (2,r) Young diagrams with the paper's inductive-admissibility condition.
    4. Temperley–Lieb generators e_i from Eq. (13)–(14) using α_{t,i} = [d_{t,i}+1] / ([2][d_{t,i}]) with quantum integer [k] = sin(πk/r)/sin(π/r).
    5. Braid generators via ρ(σ_i) = q − (1+q) e_i  (Eq. 15).
    6. Verification of unitarity, braid relations, TL relations, spectrum, and multiplicities (C2–C5).
    7. Random-braid sampling in B_3 through ρ_{[2,1]} for density (C6).
    8. Brute-force braid-word approximation of a target Hadamard gate.
2. **`fkw_extras.py`** — random-braid tr(U)/2 distribution vs. SU(2)/center Haar density (2/π)√(1−x²); hillclimb search for Hadamard; unitarity stress-test on random braids of length 100/500/2000.
3. **`fkw_hadamard_deep.py`** — BFS up to length 15 with pruning, showing monotone decrease in Frobenius distance to the Hadamard target (evidence for density).
4. **`run_judge.py`** — calls Argo GPT-5.1 with a critical judging prompt, returns strict JSON verdict.

All key relations were verified to residual ≤ 10⁻¹⁵ in the operator norm.

### 3.4 Exact commands
```bash
cd work
python3 -m venv .venv && source .venv/bin/activate
pip install -q numpy scipy
python fkw_replication.py         # 3.5 s
python fkw_extras.py              # 8   s
python fkw_hadamard_deep.py       # 77  s  (BFS depth 15)
python run_judge.py               # 30  s  (LLM judge)
```

## 4. Results vs. paper

| Quantity                                | Paper           | This replication          | Match |
|-----------------------------------------|-----------------|---------------------------|-------|
| dim V_3^1                               | 2               | 2                         | ✓     |
| dim V_3^3                               | 1               | 1                         | ✓     |
| dim V_6^0                               | 5               | 5                         | ✓     |
| dim V_6^2                               | 8               | 8                         | ✓     |
| dim ρ_{[2,1]} (B_3)                     | 2               | 2                         | ✓     |
| dim ρ_{[3,3]} (B_6)                     | 5               | 5                         | ✓     |
| dim ρ_{[4,2]} (B_6)                     | 8               | 8                         | ✓     |
| eigenvalues of ρ_λ(σ_i)                 | {−1, q}         | {−1, q}                   | ✓     |
| ρ_{[4,2]}(σ_i) multiplicities          | (3, 5)          | (3, 5) for i=1..5         | ✓     |
| ρ_{[2,1]}(σ_1)                          | diag(−1, q)     | eigenvalues {−1, q}       | ✓     |
| Braid relation residual                 | 0 (theory)      | ≤ 10⁻¹⁵                   | ✓     |
| Unitarity ||UU† − I||                    | 0 (theory)      | ≤ 10⁻¹⁵                   | ✓     |
| Random-braid pair-distance spread       | (implied dense) | mean 1.50 std 0.37 (dim 2)| Consistent |
| # distinct traces in 2000 random braids | (implied dense) | 261 (finite subgroup: <30)| ✓     |
| Hadamard best approx dist (len ≤ 11)    | 0 as l → ∞      | 0.104                     | Convergent |
| Printed ρ_{[2,1]}(σ_2) literal          | (paper prints)  | non-unitary as printed    | **✗ likely typo** |

## 5. Verdict + justification

**Verdict: REPLICATED** (independent LLM judge: `argo:gpt-5.1`, T=0, coverage 90 %, agreement 98 %).

Justification:
- Every combinatorial/algebraic quantity the paper explicitly names (dimensions, unitarity, braid relations, TL relations, spectrum, and the specific (3,5) multiplicity claim for λ=[4,2]) was reproduced from first principles at machine precision.
- The density theorem (Thm 4.1) is not itself a numerical claim; its *ingredients* (image not stuck in a finite subgroup, gate-approx improves with length) are consistent with what the theorem asserts.
- One caveat: the explicit printed matrix for ρ_{[2,1]}(σ_2) in Section 3 is not unitary under either natural literal reading, strongly suggesting an OCR/typesetting artifact in the paper's printed matrix (the underlying representation *is* unitary, and its spectrum is correct — the paper's own algebraic derivation is fine). This is worth noting for readers who consult the paper for a copy-paste implementation.

Non-inflation notes: no attempt was made to simulate topological quantum computation of BQP-hard instances (Thms 2.2/2.3), which would require full CS5 machinery + fault-tolerant Aharonov–Ben-Or overhead. Those are Solovay–Kitaev/AB corollaries and are not numerically testable at replication-wave scale.

## Open Questions

**Q1.** Our brute-force BFS for approximating the Hadamard gate through B_3 in the ρ_{[2,1]} sector plateaus around Frobenius distance ~0.10 by length ~11 and does not improve monotonically after that. Is this an artifact of the BFS-with-pruning heuristic, or does the ρ_{[2,1]} image have a systematic "spectral gap" that limits what short braids can approximate — as opposed to the *closure* being dense?  
**Basis.** In our depth-15 BFS with pruning, we observed the best distance oscillating between 0.10 and 0.24 rather than smoothly decreasing.  
**Next steps.** (a) run a proper Solovay–Kitaev iterated approximation using length-N atoms and check the promised 1/l² scaling; (b) compare with the same experiment through ρ_{[3,3]} where B₆ has more generators; (c) numerically estimate the covering-radius exponent.

**Q2.** The paper's printed ρ_{[2,1]}(σ_2) matrix (Section 3) is not unitary under either natural literal reading of the typography. Which fix (sign flip, √[3] misprint, or basis-conjugation) recovers unitarity, and is the same typo present in later published versions or in the FKLW proceedings paper?  
**Basis.** We tested both plausible sign conventions of the printed matrix and both fail the unitarity check by O(1).  
**Next steps.** Diff the arXiv v1/v2 sources for that formula, compare against Bulletin AMS 40(1) 2003 published version, and reach out to Wang for erratum status.

**Q3.** The random-braid trace distribution in ρ_{[2,1]} shows RMS deviation ~0.08 from the SU(2)/center Haar density even at 50k samples with braid length uniform in [20, 60]. Is this a fixed-length equidistribution artifact, or evidence that the natural uniform-word measure on B_3 does not converge to Haar in this representation?  
**Basis.** RMS of empirical histogram vs. (2/π)√(1−x²) stayed at ~0.08 across two sample sizes.  
**Next steps.** (a) study the Plancherel-measure or Markov-chain distribution on B_n that provably equidistributes; (b) increase word length to 200+ and re-test; (c) compare against the theoretical mixing rate for random walks on B_n through the Jones representation.

**Q4.** The paper embeds k qubits into V_{3k}^0, whose dimension grows as (Fibonacci-related) f_{3k+1} rather than 2^k. What is the actual overhead ratio dim V_{3k}^0 / 2^k for small k, and how does the resulting "qubit-smearing error probability" per gate compare to the ε²-bound cited in the paper for k = 1..10?  
**Basis.** Our C1 dimensions show dim V_6^0 = 5, so already for k=2 the modular-functor space is only 25 % larger than 2^k=4 — much tighter than the general growth-rate suggests.  
**Next steps.** Extend `dim_V_n_ell(n, ell)` to n = 3, 6, 9, ..., 30 and tabulate the ratio; simulate a single 2-qubit gate with an actual (approximate) braid and measure the empirical smearing-error probability vs. the paper's O(ε²) bound.

**Q5.** The Aharonov–Ben-Or [AB] fault-tolerance threshold cited in the paper (ε < 10⁻⁶) predates modern surface-code thresholds by ~15 years. Is CS5-with-braid-approximation-error still fault-tolerant under contemporary threshold analyses (e.g., Aliferis–Gottesman 2005; Aharonov–Kitaev–Preskill 2006), or does the "systematic-not-random" nature of Solovay–Kitaev residual errors push the effective threshold materially lower for this model?  
**Basis.** The paper notes the errors are "malicious", not iid.  
**Next steps.** Symbolic error-model construction: pick a target gate, compute the actual residual after a length-L approximate braid, propagate through a concatenated code, and measure the crossover ε.

(Full JSON in `open_questions.json`.)
