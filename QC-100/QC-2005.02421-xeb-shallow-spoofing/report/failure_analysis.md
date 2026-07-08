# Failure analysis — QC-2005.02421 (shallow-XEB spoofing)

Honest critique of this replication. Written to Rick's 2026-07-05
hard-requirement standard: flag what was reimplemented independently,
what was reproduced numerically vs quoted, and what was skipped.

## TL;DR

- **Spoofing algorithm reimplemented independently?** Partially yes.
  The $L{=}2$ depth-1 spoofer is a full, honest reimplementation of
  Theorem 1.1's mechanism. The $L{=}4$ block spoofer at depth 2 is our
  own brute-force marginal computation, not the tensor-network
  reduction the paper introduces in §3.
- **XEB score reproduced vs quoted?** Reproduced. Every numerical
  $F_{\mathrm{XEB}}$ in the report is Monte-Carlo estimated from
  freshly generated Haar-random circuits under a fixed seed; nothing
  is taken from the paper (which reports no numerical
  $F_{\mathrm{XEB}}$ anyway — it's an analytic paper).
- **Shallow-depth threshold quantitatively verified?** Only
  qualitatively. We see the spoofer's advantage decay smoothly with
  depth, consistent with the $1/15^d$ factor of Theorem 1.1, but did
  NOT fit the numerical decay to $15^{-d}$ or sweep $(L/n)$ to test
  the prefactor.
- **Comparison against genuine quantum sampling?** Not attempted. The
  paper's numerical anchor is Google's Sycamore $F=2.24\cdot 10^{-3}$;
  matching that requires a 53-qubit noisy device or HPC-scale
  simulation. The paper itself does not attempt this.

## Where independence was strong

1. **Circuit generator.** 1D brick-wall Haar-random 2-qubit circuits
   built from scratch using QR-of-Gaussian (Mezzadri 2007). No code
   from Cirq's built-in random-circuit helpers relied upon for the
   circuit ensemble itself; Cirq only used as the statevector engine.
2. **Baselines (C1, C2).** Uniform and exact samplers wired directly to
   the amplitude vector; the $F_{\mathrm{XEB}}$ estimator is a
   one-liner. Nothing from the paper reused.
3. **Depth-1 spoofer (C3, $L{=}2$).** Full reimplementation of the
   paper's mechanism at its simplest instance: compute per-block
   marginals ($4$ numbers each), take the argmax, concatenate. No
   inputs from the paper.
4. **Collision-probability trajectory (C4).** Direct evaluation of
   $\mathrm{CP}(q_C) = \sum_x q_C(x)^2$ on the exact statevector.

## Where the replication is deliberately weaker

1. **The full paper algorithm is NOT reimplemented.** The paper's §3
   builds a tensor-network approximation of the light-cone marginal that
   is asymptotically more efficient than brute-force. Our $L{=}4$
   block spoofer computes the marginal by summing $2^{n-L}$ amplitudes
   -- correct but $O(2^n)$ per block, which is fine for our $n\le 8$
   but does not scale to the paper's target regime. A full
   reimplementation is a substantial engineering task (weeks, not
   hours) and was out of scope.
2. **The $1/15^d$ decay is only visually consistent.** Ratios of
   $F_{\mathrm{XEB}}$ between adjacent depths in the $L{=}4$ control
   are $\sim 4\times$--$8\times$ per step at small $n$, not the clean
   $15\times$ the theorem predicts asymptotically. This is likely
   dominated by finite-$n$ corrections, block-size mismatch (fixed 4
   vs true light cone), and the fact that the theorem is a lower
   bound in expectation over circuits, not a tight rate. But we did
   not model any of this quantitatively.
3. **No error bars on the CP trajectory.** The collision-probability
   numbers in §4.2 are means over 20 circuits with no reported
   variance. The Porter-Thomas convergence is a smooth trend but we
   cannot say from this data alone whether the finite-$n$ correction
   matches the $2/(2^n+1)$ prediction to precision better than
   $\sim 10\%$.
4. **No 2D architecture.** Corollary 1.2 targets 2D grids;
   we tested only 1D brick-wall. The paper's Corollary 1.2 for 1D
   uses the same $1/15^d$ mechanism, so this is a legitimate
   substitution for testing the mechanism, but it is NOT a test of
   the Sycamore-style setting the paper is ultimately about.
5. **No noise.** All simulation is noiseless. The paper is
   noiseless-classical vs noiseless-quantum, so this matches the
   paper's setup, but it means we say nothing about the
   quantum-supremacy question in practice (which is entirely a
   noise-threshold argument).
6. **No cross-validation against tensor-network samplers.** Post-2020
   tensor-network methods (Pan-Zhang 2021 etc.) subsume and extend
   the paper's spoofing thesis in ways the paper could not
   anticipate. We did not compare.

## What would strengthen the replication (in priority order)

1. **Adaptive block sizing.** Set the light-cone block $L$ equal to
   the actual light cone at each depth (i.e., $L = 2d$ for 1D
   brick-wall), and re-plot $F_{\mathrm{XEB}}$ vs $d$. If the decay
   really is $\sim 15^{-d}$, this run should show it cleanly. Cheap;
   ~1 hour more CPU.
2. **Numerical fit of the $15^{-d}$ law.** With the adaptive-$L$ data,
   fit $\log F_{\mathrm{XEB}}$ vs $d$ and report the slope with a
   confidence interval. Publishable.
3. **2D lattice sanity check.** Repeat the $L{=}4$ block spoofer on a
   2D $3\times 3$ brick-wall at $n=9$, $d\in\{1,2,3\}$. Still CPU-feasible
   (statevector on $n\le 12$).
4. **HOG cross-benchmark.** Compute heavy-output-generation scores
   alongside $F_{\mathrm{XEB}}$ on the same runs; see whether the
   spoofer that trivially beats XEB also beats HOG. This directly
   probes the "is XEB uniquely fragile?" question.
5. **Tensor-network sampler comparison.** Add \texttt{quimb}-based MPS
   sampling as a stronger classical baseline. Would reveal how much of
   the paper's contribution is subsumed by post-2020 methods.

## What is definitively out of scope

- Reproducing Sycamore's $F=(2.24\pm 0.21)\cdot 10^{-3}$ on 53 qubits.
  Requires HPC-scale simulation or a physical quantum device. The
  paper itself does not do this.
- Implementing the full poly(n, 2^L) 2D construction of Corollary 1.2.
  Non-trivial engineering (tensor-network light-cone contraction), not
  a weekend project.

## Honest bottom line

The paper's headline mechanism -- "shallow-depth Linear XEB is
classically spoofable by a light-cone-restricted algorithm" -- is
reproduced end-to-end in the small-instance regime accessible to CPU
statevector simulation. The verdict **REPLICATED** is well-supported
for what was tested. It is *not* an end-to-end verification of the
$1/15^d$ scaling law, the 2D $\sqrt{\log n}$-depth construction, or
the Sycamore comparison -- and none of those were claimed.
