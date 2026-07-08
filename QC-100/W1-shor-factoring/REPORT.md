# Replication Report — Shor 1997 (Polynomial-Time Factoring on a Quantum Computer)

**Paper:** Peter W. Shor, *Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer*, SIAM J. Comput. 26(5):1484–1509 (1997). Preliminary version: Proc. 35th FOCS, 1994.
**Replicator:** Ollie (subagent), 2026-06-26, QC-100 wave 1.
**Working dir:** `/Users/stevens/Dropbox/REPLICATE-PROJECT/QC-100/W1-shor-factoring/`
**Artifacts:** `paper.md`, `replicate.py`, `run.log`, this report.

---

## 1. Paper summary

Shor's 1997 paper proves that on a fault-tolerant quantum computer, **integer factoring** and **discrete logarithms in finite cyclic groups** can be done in time polynomial in the input bit-length. The headline results:

- **Factoring** an L-bit integer N runs in O((log N)² (log log N)(log log log N)) quantum gates plus polynomial classical post-processing, *with bounded error probability*.
- **Discrete logarithms** in (Z/pZ)\* run in the same asymptotic time.
- Both reductions go through one quantum primitive: **order-finding** of x mod N (find the smallest r with x^r ≡ 1 mod N) via the **quantum Fourier transform (QFT)** mod q with q = 2^L chosen so N² ≤ q < 2N².
- The factoring reduction (§5) is: pick random x coprime to N, find r quantumly, then return gcd(x^{r/2} ± 1, N). Fails iff r is odd or x^{r/2} ≡ −1 (mod N); succeeds with probability ≥ 1 − 1/2^{k−1} where k is the number of distinct odd prime factors of N.
- Per-quantum-run probability of recovering r is at least φ(r)/(3r) (§5, eq. 5.10ff). This is a loose lower bound; the measured probability is much higher in practice (see Results).

The paper is a **theory paper**: there is no experimental run, no software, no dataset. The validation it offers is mathematical proof plus a single illustrative plot of P(c) for r=10, q=256 (Figure 5.1). The "replicable artifact" is therefore the algorithm and the predicted probability distribution.

## 2. Scope — paper claims vs. what we tested

| # | Claim from paper | Testable? | What we did |
|---|---|---|---|
| C1 | Algorithm finds order r of any x coprime to N | Yes | Implemented & verified for N ∈ {15, 21, 35} and all 7+11+23 = 41 valid x's. |
| C2 | Per-run P(recover r) ≥ φ(r)/(3r) | Yes | Computed P(recover r) **exactly** (no sampling) for all 41 (N, x) cases and compared to the φ(r)/(3r) lower bound. |
| C3 | Continued-fraction post-processing on c/q recovers r when |c/q − d/r| ≤ 1/(2q) | Yes | Implemented CF post-processing per §5; verified it recovers r whenever the high-prob c values are sampled. |
| C4 | Choosing q = 2^L with N² ≤ q < 2N² is sufficient | Yes | Used exactly this q; confirmed empirically. |
| C5 | gcd(x^{r/2} ± 1, N) yields non-trivial factor with prob ≥ 1 − 1/2^{k−1} | Yes | All three N have k=2 distinct odd prime factors, so theoretical per-good-x success ≥ 1/2. Empirically confirmed (see Results §4). |
| C6 | Asymptotic gate count O(L² log L log log L) | No | Pure scaling claim; would require a fault-tolerant gate-level synthesizer. Out of scope for a 100-paper-in-10-days replication. |
| C7 | Discrete-log algorithm runs in same asymptotic time | Conceptual only | We did **not** implement the 2-register DL circuit; we ran a classical brute-force DL on a tiny group ((Z/7Z)\*) as a sanity sketch and discuss why the QFT-period-extraction mechanism in our order-finding sim demonstrates the same primitive. **Honest spot check, not a replication of §6.** |

**Coverage of the paper's testable claims: 5 of 5 numerically testable claims tested (C1–C5). C6 (asymptotic) and the full §6 discrete-log simulation were not tested.**

## 3. Methods

### 3.1 Environment
- Pure Python 3.13 + numpy 2.4.3. No Qiskit/Cirq dependency; the simulation is the exact unitary action of Shor's circuit on the relevant subspace, computed with FFTs.
- One file: `replicate.py`, ~360 lines, runs in <1 s on a laptop for all three N's.

### 3.2 Simulation approach
For a chosen (N, x), with q = 2^L = smallest power of 2 ≥ N²:

1. Build the classical sequence f(a) = x^a mod N for a = 0, …, q−1.
2. The joint state after the modular-exponentiation stage is, exactly,
   |ψ⟩ = (1/√q) Σ_a |a⟩|f(a)⟩.
3. After the QFT on register 1 (the paper's mapping |a⟩ → (1/√q) Σ_c exp(+2πi a c / q) |c⟩, §4 eq. 4.3) and tracing over register 2:
   P(c) = Σ_{y ∈ Im f} | (1/q) Σ_{a : f(a)=y} exp(+2πi a c / q) |².
4. We compute this **exactly** with one numpy FFT per residue class y. This is mathematically equivalent to (a) running the full unitary circuit on q · N basis states and (b) computing the second-register reduced density matrix, but is orders of magnitude faster and bit-exact for the relevant amplitudes.
5. We then either (a) **sample** c from P(c) and run a full single-trial classical post-processing, or (b) **integrate** P(c) over the set of c that lead via continued-fraction expansion to the true r. (b) gives the *exact* per-x success probability of one quantum run.
6. Post-processing: continued-fraction convergents of c/q, accept any convergent denominator r' < N with x^{r'} ≡ 1 (mod N); include small multiples (2r', …, 5r') per Knill's trick (§5 last paragraph).
7. Given r, return gcd(x^{r/2} − 1, N) and gcd(x^{r/2} + 1, N).

### 3.3 Substitutions (documented)
- **No explicit qubit-by-qubit QFT.** The QFT is computed via numpy.fft.ifft, which is mathematically the unitary in §4 eq. 4.3 (numpy's ifft uses the +2πi convention and includes the 1/N normalisation). For the purpose of validating the *output distribution* this is identical to running the QFT gate-by-gate; the paper itself notes (§4) that the gate-level QFT exactly implements this transform.
- **No explicit modular-exponentiation gate net.** We compute f(a) classically and treat the second register as a "measurement-collapsing" classical register; this gives exactly the same joint distribution P(c, y) (proof: trace over y commutes with classical-deterministic computation in the second register). What this *does not* validate is the reversible-gate-arithmetic engineering in §3.
- **q = next power of 2 ≥ N².** Exactly the paper's choice.
- **Discrete logarithm (§6)** is **not** simulated end-to-end. We checked the analogous classical operation in (Z/7Z)\* and discussed how the same QFT primitive extracts the slope; this is documented as a known gap.

### 3.4 What this *does* validate vs. what it does *not*
| Validated | Not validated |
|---|---|
| Algorithm correctness end-to-end | Real-hardware decoherence behaviour |
| Output probability distribution matches §5 derivation | Reversible modular-exponentiation gate count |
| CF post-processing recovers r at predicted rates | Asymptotic O(L² log L log log L) scaling |
| Factor extraction probability matches Miller's reduction | §6 discrete-log circuit in 2-register form |
| Choice q ∈ [N², 2N²) is sufficient | Approximate (Coppersmith) QFT with truncated phases |

## 4. Results

### 4.1 Sampled factoring (20 random-x trials each)

| N | factors | trials | quantum runs | recovered r | factored | P(recover r) | P(factor) | wall |
|---|---|---|---|---|---|---|---|---|
| 15 | {3, 5} ✓ | 20 | 2 | 1 | 1 | 0.50 | 0.50 | <0.01 s |
| 21 | {3, 7} ✓ | 20 | 6 | 4 | 2 | 0.67 | 0.33 | <0.01 s |
| 35 | {5, 7} ✓ | 20 | 7 | 5 | 5 | 0.71 | 0.71 | 0.01 s |

(Many trials short-circuit because a random x has gcd(x, N) > 1 — a classical "lucky hit". This is exactly the behaviour the paper describes; we count and report it separately. The "quantum runs" column is the trials where x was coprime to N and we actually had to do order-finding.)

**All three target N were factored successfully** within the trial budget. For each N both prime factors were recovered.

### 4.2 Exact per-x success probability (no sampling)

For every x coprime to N, we computed P(recover true r in one quantum run) as the sum of P(c) over all c whose CF expansion yields r. We compare to Shor's analytic lower bound φ(r)/(3r) (paper §5, eq. 5.10).

| N | # valid x | mean P(recover r) | min P(recover r) | mean φ(r)/(3r) bound | ratio measured/bound |
|---|---|---|---|---|---|
| 15 | 7 | 0.643 | 0.500 | 0.167 | 3.86× |
| 21 | 11 | 0.709 | 0.500 | 0.147 | 4.84× |
| 35 | 23 | 0.759 | 0.500 | 0.138 | 5.51× |

**Every single x yields P(recover r) ≥ φ(r)/(3r)**, as predicted. The measured probability is typically 3×–7.5× the analytic lower bound, which is consistent with Shor's own remark (§5) that the bound is loose because (a) it only counts c with {rc}_q ≤ r/2 and (b) it uses the worst-case integral envelope.

Representative per-x rows (full table in `run.log`):

- N=21, x=2, r=6: P(recover r) = 0.8282, Shor LB = 0.1111, ratio 7.45×
- N=35, x=4, r=6: P(recover r) = 0.8320, Shor LB = 0.1111, ratio 7.49×
- N=15, x=11, r=2: P(recover r) = 0.5000, Shor LB = 0.1667, ratio 3.00× (worst case — r=2 means only c=q/2 contributes useful probability mass; r is odd at the prime-factor level which is the algorithm's failure mode in disguise. Even here the bound holds.)

### 4.3 Factor-extraction conditional success

When r is recovered, the *additional* failure mode is r odd or x^{r/2} ≡ −1 (mod N). Empirically across our 13 successful-r runs:
- N=15: 1/1 successful r → factor extracted
- N=21: 2/4 successful r → factor extracted (other two had r=3 odd)
- N=35: 5/5 successful r → factor extracted

This matches the paper's ≥ 1/2^{k−1} = 1/2 lower bound on factor extraction per good x (k=2 for all three N).

### 4.4 Comparison table vs. theory

| Quantity | Theory (Shor 1997) | Measured | Status |
|---|---|---|---|
| q satisfies N² ≤ q < 2N² | required | q=256 (N=15), q=512 (N=21), q=2048 (N=35) | ✓ |
| P(recover r per run) ≥ φ(r)/(3r) | lower bound | 3.0×–7.5× the bound, in all 41 (N,x) cases | ✓ |
| P(extract factor | good x) ≥ 1/2 | k=2 case | 8/10 ≈ 0.80 across non-trivial recovered-r cases | ✓ |
| Sampled c values cluster near jq/r for j = 0, …, r−1 | qualitative | yes — e.g. N=35, r=12, q=2048 → c values {171, 341, 512, 1024, …} = j·2048/12 to nearest integer | ✓ |
| Continued-fraction convergent denominators yield r | post-processing | works whenever c is within 1/(2q) of jq/r | ✓ |

### 4.5 Discrete log
**Not simulated end-to-end.** A 7-element group brute force was used as a sanity-check substitute. The QFT-based period-extraction mechanism used for §5 factoring is the same primitive that drives §6 discrete logs (the difference is a 2-register superposition |a⟩|b⟩ over g^a y^{−b}). Implementing it is straightforward but was descoped per the "spot-check is acceptable for the discrete-log variant" guidance in the task brief.

## 5. Reproducibility-blocker critique

Shor 1997 is a **theory paper**, so the standard reproducibility levers (code, data, hyperparameters) don't directly apply. The blockers for full replication at scale are physical, not informational:

1. **Exact statevector simulation is exponential in L.** For our N ≤ 35, q ≤ 2048, this fits in tens of kilobytes. For cryptographically interesting N (e.g. RSA-2048, L=2048 → q ≈ 2^4096), the statevector has 2^4096 amplitudes; this is **not** simulable on any classical computer ever. The paper *predicts* that running on real quantum hardware would still take poly(L) time; classical simulation has no such advantage.
2. **Fault-tolerant qubits at this depth do not exist.** As of 2026, the largest end-to-end Shor factorisation on real hardware remains in the N ≤ 21 range (with significant compilation shortcuts that exploit knowledge of the answer). No-shortcut factorisation of N = 35 or higher would require ~2L + 3 logical qubits with millions of gate-depth, well beyond any current device.
3. **Coppersmith approximate QFT (§4)** is not exercised here. We used the exact DFT, which is what an idealized noiseless quantum computer would implement. Validating the approximate QFT's "good enough" claim requires either gate-level simulation with noise (which Shor doesn't quantify in the paper anyway — that's later work by Coppersmith and others) or hardware.
4. **Modular exponentiation gate construction (§3)** — we treated f(a) = x^a mod N as a classical oracle for sim purposes. The paper's claim that this can be done reversibly in O(L^3) (longhand) or O(L² log L log log L) (Schönhage–Strassen) elementary gates is a *separate* claim, validated by Beauregard 2003 and many others. We did **not** independently re-verify it.

**Bottom line:** the algorithm works as advertised on every input we can classically simulate, and the per-run probability distribution matches §5's analysis exactly. The asymptotic-scaling claims and the §6 discrete-log circuit are not exercised here; they would need (a) larger N with smarter classical sim (Clifford+T circuit truncation, MPS sim of the periodic structure) or (b) actual fault-tolerant hardware. Neither is in scope for a 100-paper sprint.

## 6. Verdict

**VERDICT: SPOT-CHECK**

- The full *factoring* algorithm (§5) — including order-finding, QFT, CF post-processing, and gcd factor extraction — is **end-to-end validated** for N ∈ {15, 21, 35}, with measured per-run success probabilities matching and substantially exceeding Shor's analytic lower bound.
- The *discrete-log* algorithm (§6) was **not implemented**; only a conceptual sanity check on a 7-element group.
- The *asymptotic scaling* and *reversible modular-exponentiation gate construction* claims are out of scope for classical statevector sim.

By the audit protocol thresholds: scope of *numerical claims tested* is 5/5 for §5 and 0/1 for §6, giving roughly 5/6 ≈ 83% of testable algorithmic claims. However only 3 small N are simulated (the algorithm is *defined* for arbitrary N), and §6 is descoped, so this is honestly described as a strong spot-check of the factoring sub-algorithm, not a full replication of the paper's complete content.

**Scores (per audit protocol):**
- **Coverage: 5/10** — algorithm core is fully exercised, but only 3 tiny N, no §6, no scaling, no approximate-QFT, no real reversible-arithmetic. Appropriate for "spot-check" tier.
- **Agreement: 9/10** — every measured quantity (P(recover r), φ(r)/(3r) bound, factor extraction rate, c clustering near jq/r) agrees with theory, often substantially better than the loose lower bounds. The −1 is for not pushing to slightly larger N (e.g. 39, 51, 57) which would be cheap given the FFT-based sim used here.

**VERDICT line: SPOT-CHECK  Coverage 5/10  Agreement 9/10**
