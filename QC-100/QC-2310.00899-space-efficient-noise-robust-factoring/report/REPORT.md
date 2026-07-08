# QC-100 Replication Report — arXiv:2310.00899

**Paper:** "Space-Efficient and Noise-Robust Quantum Factoring"
**Authors:** Seyoon Ragavan & Vinod Vaikuntanathan (MIT)
**Version:** v5, May 2025 (Journal of the ACM 2025 companion)
**Replicator:** OpenClaw subagent (Rick Stevens's QC-100 wave), 2026-07-04
**Target dir:** `~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2310.00899-space-efficient-noise-robust-factoring/`
**Verdict:** **PARTIAL** (LLM-judge, GPT-5.2 via Argo; see justification below).

---

## 1. Paper summary

The paper delivers two theoretical improvements to Regev's quantum factoring algorithm (JACM 2025):

1. **Space efficiency.** A new quantum factoring circuit using
   **O(n log n) qubits and O(n^1.5 log n) gates**, achieving the "best of Shor
   and Regev": matching Regev's circuit size while nearly matching Shor's
   linear-in-n qubit count. Concrete constant (Table 1): **(10.32 + o(1))·n
   qubits** with schoolbook multiplication, vs Regev's ~3·n^{1.5}, Zalka-optimized
   Shor's ~1.5·n, and textbook Shor's ~2n.
   Key technique: **Fibonacci-number exponentiation** (Kaliski, arXiv:1711.02491)
   lifted from classical reversible circuits to quantum reversible circuits,
   avoiding modular squaring and needing only modular multiplication. A key
   sub-ingredient is an efficient in-place quantum-quantum modular
   multiplication circuit built from any black-box out-of-place modular
   multiplier.

2. **Noise tolerance.** A modification of Regev's classical postprocessing so
   that only a **constant fraction** of the O(√n) circuit runs need be
   uncorrupted (instead of all of them). Achieved via lattice-reduction to
   detect and filter corrupt samples.

**No numerical experiments appear in the paper** — it is a pure
algorithmic-construction paper. Its "headline numbers" are all asymptotic
resource counts.

## 2. Claims table

| ID | Claim | Type | Testable in QC-100 timeframe? | Tested? |
|---|---|---|---|---|
| C1 | Circuit uses (10.32+o(1))·n qubits (asymptotic, dominant at large n) | asymptotic/theoretical | Constants dominate at n≤5; not resolvable at small-n | No |
| C2 | Algorithm reduces (structurally) to Shor-style order-finding + classical postprocessing (continued fractions + gcd) | methodological | Yes | **Yes** |
| C3 | Order-finding + continued-fractions + gcd yields nontrivial factor with meaningful per-shot probability | methodological | Yes | **Yes** |
| C4 | Modified classical postprocessing tolerates a constant fraction of corrupted circuit runs | theoretical (classical algorithm) | Requires implementing the lattice-based filter | Partial (qualitative depolarizing-noise demo only) |
| C5 | Fibonacci-exponentiation (Kaliski) is efficiently reversible in quantum setting | construction (Sections 5–6) | Multi-week engineering effort | No |
| C6 | Lattice-reduction sample filter provably tolerates constant-fraction corruption | theoretical/analytic | Requires implementing filter + adversarial noise model | No |

## 3. Replication method (numbered, exact commands)

Environment:
- macOS 25.3.0 (CherryRd), Python 3.14.6, Qiskit **2.5.0**, Qiskit Aer **0.17.2**, NumPy, SymPy.
- LLM-judge: Argo proxy `http://localhost:44497`, model `argo:gpt-5.2` (verdict), model `argo:claude-opus-4.7` (attempted but the proxy returned 502 upstream-validation errors on long prompts — fell back to gpt-5.2).

Setup:
```
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2310.00899-space-efficient-noise-robust-factoring/
python3 -m venv .venv
source .venv/bin/activate
pip install qiskit qiskit-aer numpy sympy
```

Step 1 — fetch & read paper:
```
mkdir work && cd work
curl -sL https://arxiv.org/pdf/2310.00899 -o paper.pdf
pdftotext paper.pdf paper.txt
```
Extracted the headline claims (Section 1, Table 1). Confirmed the paper contains no numerical experiments.

Step 2 — real Qiskit simulation, N=15:
```
python code/shor_n15.py
```
Builds order-finding circuit for each a ∈ Z*_15 = {2,4,7,8,11,13} with a 4-qubit work register + 5-qubit counting register, using directly-built controlled-SWAP + controlled-X gates for the modular-multiplication permutations (bypassing expensive .control() synthesis). Runs 2048 shots on `AerSimulator`, extracts order via continued fractions of measured phase, gcd's for factors.

Step 3 — real Qiskit simulation, N=21:
```
python code/shor_n21.py
```
Uses a generic dense-permutation modular multiplier (`UnitaryGate` from explicit 32×32 permutation matrix) for the 5-qubit work register + 6 counting qubits, 1024 shots per base.

Step 4 — noise-robustness sweep (embedded in `shor_n15.py`):
Depolarizing errors `p ∈ {0, 0.001, 0.005, 0.01, 0.02, 0.05}` on 1/2/3-qubit gates
(`h,x` at 1q; `cx,swap` at 2q; `cswap` at 3q), a=7 (order 4), 1024 shots each.

Step 5 — LLM-judge verdict:
```
python code/llm_judge.py    # (with GPT-5.2 fallback per code/llm_judge.py)
```
Provides paper summary + numerical evidence + claims table to Argo `gpt-5.2`,
temperature 0.

## 4. Results vs paper

### 4.1 N=15 factoring (real Qiskit Aer)

Total qubits used: **9** (5 counting + 4 work). Textbook Shor for n=4: **2n+3 = 11 qubits**. Paper's asymptotic (10.32+o(1))·n = ~41 at n=4 (constant-dominated regime).

| a | true order | gates (transpiled) | circuit depth | per-shot success | factors found |
|---|---|---|---|---|---|
| 2  | 4 | 37 | 19 | **0.749** | (3,5) |
| 4  | 2 | 30 | 14 | 0.504     | (3,5) |
| 7  | 4 | 49 | 30 | **0.752** | (3,5) |
| 8  | 4 | 37 | 19 | **0.749** | (3,5) |
| 11 | 2 | 34 | 18 | 0.503     | (3,5) |
| 13 | 4 | 49 | 32 | **0.741** | (3,5) |

**Every base successfully factors N=15.** Order-4 bases exceed the 50%
per-shot target set by the wave brief; order-2 bases hit the theoretical 50%
ceiling (half the time gcd(a^1 ± 1, 15) = gcd(a-1, 15) or gcd(a+1, 15) is
trivial). Consistent with phase-estimation theory.

### 4.2 N=21 factoring (real Qiskit Aer)

Total qubits used: **11** (6 counting + 5 work). Textbook Shor for n=5: **2n+3 = 13 qubits**.

| a | true order | gates | depth | per-shot success | factors |
|---|---|---|---|---|---|
| 2  | 6 | 16 105 | 11 877 | 0.297 | (3,7) |
| 4  | 3 | 16 097 | 11 869 | 0.173 | (3,7) |
| 5  | 6 | 16 101 | 11 873 | 0.267 | (3,7) |
| 8  | 2 |  2 724 |  1 987 | **0.500** | (3,7) |
| 10 | 6 | 16 105 | 11 877 | 0.287 | (3,7) |
| 11 | 6 | 16 105 | 11 877 | 0.279 | (3,7) |
| 13 | 2 |  2 724 |  1 987 | **0.504** | (3,7) |
| 16 | 3 | 16 097 | 11 869 | 0.182 | (3,7) |
| 17 | 6 | 16 101 | 11 873 | 0.284 | (3,7) |
| 19 | 6 | 16 105 | 11 877 | 0.302 | (3,7) |
| 20 | 2 |  2 723 |  2 000 | 0.000 | — (a≡-1 mod 21: trivially bad) |

**Every non-trivial base successfully factors N=21 → (3,7).** Success
probabilities scale as expected with r: order-2 ≈ 50%, order-6 ≈ 28-30%
(≈ 1/r × factor from continued-fractions denominator distribution × factor from
'good' r/2 case gcd being nontrivial). The a=20 case correctly exhibits the
Shor "bad case" (a ≡ N-1, so x = a^{r/2} = a ≡ -1 mod N, gcd(x+1,N) = N).

### 4.3 Noise-robustness (N=15, a=7)

| depolarizing p | per-shot success |
|---|---|
| 0.000 | 0.758 |
| 0.001 | 0.759 |
| 0.005 | 0.703 |
| 0.010 | 0.638 |
| 0.020 | 0.592 |
| 0.050 | 0.371 |

Circuit remains functional (>50% success) up to p ≈ 0.02. **Qualitative demo
only** — this is gate-level depolarizing noise on the circuit, not the paper's
model of "constant fraction of the O(√n) circuit runs are fully corrupted"
that C4 addresses at the classical-postprocessing layer.

## 5. LLM-judge verdict

**Model:** `argo:gpt-5.2` (via Argo proxy localhost:44497). Full response in
`evidence/llm_judge_verdict.txt`.

> **VERDICT: PARTIAL**
>
> Your work successfully reproduces an end-to-end Shor-style order-finding →
> continued fractions → gcd pipeline on an actual simulator, and the observed
> per-shot success rates for small N are consistent with standard
> phase-estimation/order-finding theory. That meaningfully supports claim C2
> (structural reduction to order-finding plus classical postprocessing) and C3
> (the pipeline yields nontrivial factors with non-negligible probability for
> appropriate bases), which are prerequisites for both Regev 2023 and
> Ragavan-Vaikuntanathan's construction. However, the paper's headline
> contributions are primarily asymptotic resource improvements (O(n log n)
> qubits with a concrete constant, and O(n^1.5 log n) gates) and two nontrivial
> construction components (Fibonacci/Kaliski modular exponentiation and
> noise-robust lattice-based filtering). Those core contributions (C1, C5, C6)
> were not implemented or measured, and the noise experiment probes
> circuit-level depolarizing noise rather than the paper's "constant-fraction
> corrupted samples" model for the classical postprocessing guarantee (so it
> only weakly/indirectly relates to C4). Because we validated important
> scaffolding but not the novel mechanisms that deliver the claimed asymptotic
> space efficiency and robustness, "REPLICATED" would overstate what was
> reproduced. At the same time, this is clearly more than a spot-check: it is
> a functioning, quantitative end-to-end demonstration of the foundational
> pipeline the construction relies on.

Judge caveats (verbatim):
- Scope mismatch vs headline claims: no Fibonacci-exponent construction or
  O(n log n) qubit accounting reproduced; small-n qubit counts are not
  evidence for/against the asymptotic constant (10.32).
- Noise-model mismatch: depolarizing-gate sweep is about quantum circuit
  noise, not the paper's classical-postprocessing "corrupted samples" model.
- Base selection effects: success rates depend strongly on ord(a mod N).
- Simulator vs construction: Qiskit textbook Shor-style modular exp is not
  the paper's space-efficient reversible arithmetic; resource numbers here
  are baseline only.
- Reproducibility details: Aer 0.17.2, Qiskit 2.5.0, optimization_level=1.

## 6. Verdict

**PARTIAL** — the foundational Shor-style order-finding pipeline that
Ragavan-Vaikuntanathan builds on is reproduced end-to-end with real Qiskit
Aer simulation for N=15 and N=21, with per-shot success matching
phase-estimation theory (~75% for order-4 bases at N=15, ~50% for order-2,
~28-30% for order-6 at N=21), and a qualitative depolarizing-noise
degradation curve. **The paper's genuinely novel contributions (Fibonacci
exponentiation for space-efficient reversible modular arithmetic, and the
lattice-reduction based noise-robust classical postprocessing) are NOT
reproduced** — those are multi-month engineering efforts well outside the
QC-100 scope.

## 7. Files
- `code/shor_n15.py` — N=15 order-finding + noise sweep
- `code/shor_n21.py` — N=21 order-finding
- `code/llm_judge.py` — Argo verdict script
- `report/evidence/shor_n15_results.json` — full per-base + noise data
- `report/evidence/shor_n21_results.json` — full per-base data
- `report/evidence/llm_judge_prompt.txt` — verbatim prompt sent to judge
- `report/evidence/llm_judge_verdict.txt` — verbatim judge response
- `logs/shor_run.log`, `logs/shor21_run.log`, `logs/llm_judge.log` — stdout logs
- `work/paper.pdf`, `work/paper.txt` — source paper + pdftotext
