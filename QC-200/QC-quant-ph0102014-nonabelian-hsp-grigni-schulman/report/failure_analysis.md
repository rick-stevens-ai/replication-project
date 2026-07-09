# Failure Analysis

The replication went end-to-end without any paper-claim contradiction, but the local implementation hit two bugs worth documenting.

## Bug 1 — Qiskit endianness in the truth-table oracle unitary

**Symptom.** First working sweep of Theorem 13 at k=1 (|G|=8) had 4/12 trials passing, but the failing trials showed a very characteristic pattern in the verbose log: the Abelian-HSP subroutine returned `y=0` (all-zero measurement) for *every* sample, then the coupon-collector stability rule confidently concluded H_perp = {0}, i.e. H = full group (Z_2)^n. Yet the analytic-numpy sampler (used for k=2, k=3) gave the correct distribution on the same inputs.

**Isolation.** Ran a 3-line direct comparison of the two samplers on a trivial-H oracle (`f(x) = x`, so H = {0} and H_perp = full group):

```python
def f(x): return x
rng = random.Random(42)
ys_np = [abelian_hsp_z2n_sample(4, f, 4, rng) for _ in range(200)]
ys_qk = [abelian_hsp_z2n_sample_qiskit(4, f, 4, rng) for _ in range(200)]
# numpy: distinct = 16 of 16; y=0 count 12/200          (correct)
# qiskit: distinct =  1 of 16; y=0 count 200/200        (broken)
```

**Root cause.** The oracle unitary was built as `U[dst, src] = 1` with `src = x * dim_out + y` and `dst = x * dim_out + (y ^ f(x))`. But Qiskit uses **little-endian qubit ordering with qubit 0 as the least-significant bit** of the basis-state index. For a `(n_bits + n_out)`-qubit circuit with input on qubits 0..n_bits-1 and output on qubits n_bits..n_bits+n_out-1, the basis index for input `x` (bits at qubit indices 0..n_bits-1) and output `y` (bits at qubit indices n_bits..) is `(y << n_bits) | x`, **not** `x * dim_out + y`. The wrong layout meant U was still unitary (a permutation of columns), but its action was equivalent to XOR-ing `y` into a *different* register, producing spurious statistics.

**Fix.** Replaced the two lines with:

```python
src = (y << n_bits) | x
dst = ((y ^ fx) << n_bits) | x
```

After this fix all Qiskit-path samples agreed with the numpy analytic path to within Monte-Carlo noise. This is a classic pitfall for anyone new to Qiskit's Little-Endian: **the qiskit-tutorial index convention is opposite of how the circuit diagram reads left-to-right.**

**Prevention.** Whenever building a `UnitaryGate` from a numpy matrix in Qiskit for a multi-register circuit, cross-check against `sim.run(...).get_counts()` with a *known* trivial output first (e.g. `f = identity` on Abelian HSP -> must be uniform), before wiring into a larger pipeline.

## Bug 2 — Over-eager Abelian HSP stopping rule

**Symptom.** Even after fixing Bug 1, Step A of Theorem 13 in the k=2 trial 1 (planted H = {(0,0),(15,1)}, so H∩N = {(0,0)}, order 1) stopped after collecting only samples of `y=0000` and concluded H_N = full N (size 16). That's because when H_N = {0}, all 2^n samples y ∈ (Z_2)^n are equally likely; the sampler happened to draw y=0 twelve times in a row (probability 1/16^12 = 2^-48 in the worst case, but actually happens more often due to a subtle interaction with the stopping rule).

**Root cause.** The original stopping rule required only 5 consecutive samples that didn't change the running F_2-kernel of collected y's. If the very first 6 samples all happen to be y=0, kernel stays at "everything" and the rule triggers immediately, missing all the nonzero y's that would restrict H down to {0}. In particular for small n and small H_N, this is a real risk.

**Fix.** Two-part safeguard:
- Require at least `n_bits + 5` samples before any early-stop can trigger.
- Require a longer stability streak (15 rather than 5).

**Prevention.** For quantum-sampling HSP subroutines, the "n_bits + a few" minimum is the standard coupon-collector cushion. Bake it in whenever the calling code doesn't know the true |H| in advance.

## What did NOT go wrong

- **The paper's algorithm** worked exactly as stated. No claim in Ivanyos–Magniez–Santha's Theorem 13 or Lemma 9 was contradicted or required amendment.
- **The wreath-group multiplication** was checked by hand on |G|=8 (D_4) and matches standard references.
- **The Statevector-vs-Analytic dual-path** was itself a bug-catcher: without it, Bug 1 would have quietly held for all k, and the paper would appear to "fail" — a false negative worse than a bug.
- **Compute-quota.** Wall clock stayed well under 1 minute for the full sweep at k ≤ 4; no need to escalate to uicgpu. If we wanted k ≥ 8 we would.

## Lessons for the X-100 project

1. **Author-id checks are cheap and worth doing up front.** Ten minutes at the start of this task saved the risk of running down a wrong path (the ticket said Grigni–Schulman–Vazirani–Vazirani but the arXiv id is Ivanyos–Magniez–Santha). Recommendation: a linter over the QC-200 ticket file.
2. **Two independent code paths (analytic + statevector) beats one twice.** The disagreement between them was what surfaced Bug 1 in three minutes.
3. **`marker` and `nougat` are not universally installed.** For pure-math papers a `pdftotext -layout` fallback + hand-annotated marker.md is honest and fast.
