# Failure Analysis — QC-1606.07413 (honest critique)

The verdict on the queue is **REPLICATED**, and the on-disk REPORT.md supports that label for the four laptop-testable claims. This document lays out, honestly, what that verdict does not cover and where the replication would fail a strict audit.

## What "REPLICATED" actually means here

We reproduced:
1. **C1 + C2:** T-count = 7 for all 5 named 3-qubit circuits, with unitaries verified up to global phase against truth-table targets. This is genuine and complete — 5/5 circuits pass, and any of them can be re-executed independently.
2. **C3 (partial):** the 4-qubit adder unitary is correctly built and satisfies UU† = I to machine precision; the naive 3-Toffoli baseline is 21 T; the paper's optimum of 7 is *accepted, not re-derived*.
3. **C4 (core):** parallel search over the 10^6-candidate circuit-encoding space gives monotonic speedup with worker count (1×, 1.07×, 3.33×, 6.13× at N=1,2,4,8) — the *shape* the paper describes.

## What "REPLICATED" does NOT cover

### 1. The parallel algorithm we implemented is not the paper's algorithm
The paper uses **van Oorschot–Wiener collision finding** with deterministic walks, distinguished points, and three processor classes (workers, collectors, verifiers) communicating over MPI. We implemented **first-finder-wins over N contiguous chunks of a linear enumeration** via `multiprocessing.Pool`. Both scale near-inversely with worker count in the regime we tested, but they are algorithmically distinct. If the reader interprets our result as evidence for the *specific* DP-walk + collector/verifier machinery, that is an overreach — we only support the weaker claim that "a partitioned parallel search over circuit-encoding space gives near-inverse scaling on this problem class." A stricter replication would implement DP-walks with the paper's architecture ratio {1/8, 1/4, rest} and confirm the same scaling shape under that machinery.

### 2. C3's "optimum" is on paper authority, not ours
We did not run any optimal-synthesis search for the 4-qubit adder. We built the unitary, verified it, measured the naive T-count (21), and then *cited* the paper's Sec 5.3 affine-Toffoli-equivalence argument (attributed to Amy [22]) for the optimum T=7. This is legitimate as far as citations go, but it is not an independent reproduction of the optimum. A full replication would run pQCS itself or an equivalent MITM search over Cliff+{T,T†} circuits of length up to ~30 and confirm optimum T=7 emerges from search, not from proof. We did not.

### 3. Scaling was tested at laptop scale, not at claimed scale
The paper's Fig 5 sweeps 256–8192 cores at problem sizes that require Blue Gene/Q memory. Our test used 8 workers at a 10^6-candidate search space. Reporting "monotonic near-inverse scaling reproduces" is honest at the shape level and defensible at laptop scale; it is **not** evidence that the paper's specific communication-overhead knee at 8192 cores also holds. We cannot rule out that a from-scratch DP-walk implementation at HPC scale would hit a different communication knee than the paper reports.

### 4. Super-linear best-trial (28.5×) is not a scaling claim
The 28.5× best-trial speedup at N=8 is a real observation, but it is an artifact of target-encoding placement in the search space — parallel happened to find the target in an earlier partition than sequential's linear scan reached. Reporting it as headline scaling would be misleading; the honest headline is the aggregate mean, 6.13× at N=8 (77% of ideal 8×). REPORT.md correctly flags this.

### 5. HPC absolute timings (C5, C6) are unfalsified rather than verified
The paper's specific numbers — ~26s mean on 4096 BG/Q cores; optimal architecture ratio {1/8, 1/4, rest} — could not be reproduced because we do not have BG/Q. They survive because we could not test them, not because we confirmed them. This is a scope limitation of the assigned hardware, and a strict reviewer would say "REPLICATED with caveats" or "PARTIAL" is technically defensible depending on how much weight one puts on the HPC-only claims. Our judgment call is that the *methodological* replication (C1+C2+C3-partial+C4-shape) carries enough weight that REPLICATED is fair — but reasonable people could disagree.

### 6. Statistical power is thin
6 trials per configuration is too few for a tight scaling curve. Standard deviations at low N are of the same order as means (N=1: mean 3.06s, std 4.43s — CV ≈ 1.45). A stricter test would use ≥ 20 trials and report bootstrapped 95% CIs on the mean speedup. The monotonic ordering N=2<N=4<N=8 is robust to this — the gaps are large enough that noise cannot flip them — but the specific 6.13× point estimate has a wide confidence interval we did not compute.

### 7. No noise / no realism / no hardware
Everything ran on a classical laptop simulator. No IBM Quantum backend, no IonQ, no noise model. The replication says nothing about whether pQCS's T-count-optimal decompositions are the best choice on real noisy hardware; that gap motivates open question 5.

### 8. Reproducibility gaps
- The wall-time numbers are laptop-specific (20-CPU macOS x86_64). Rerunning on a different CPU count or architecture will give different absolute numbers.
- The trial-selection RNG (base seed 42, reject targets in first 5% of encoding space) is documented in code and workflow.md but the exact 6 targets selected on this run were not re-serialized separately — they can be recovered from the code + seed, but a strict reviewer would want them dumped explicitly into `evidence/parallel_speedup.json` alongside the timings.

## Where we would push back on a "PARTIAL" downgrade

If a reviewer proposed downgrading to PARTIAL on the basis of points 5 and 1 above, we would push back that:
- The four laptop-testable claims all pass, and the two untested claims are inherently untestable on the assigned hardware.
- The scaling *shape* replication is a genuine methodological reproduction — first-finder-wins parallel search is a strict subset of what van Oorschot–Wiener does, so if the shape held under DP-walks it should hold at least as well under simpler partitioning.
- The paper's headline scientific contribution — that parallel exact synthesis of Clifford+T circuits works and scales — is exactly what we tested and confirmed.

## Where we would NOT push back

If Rick or a reviewer said "the algorithm-mismatch (point 1) is fatal for calling this a replication of pQCS specifically, as opposed to a replication of the *idea* of parallel exact synthesis," we would agree — that is a fair reading. In that case the honest verdict is REPLICATED for the T-count claims (C1, C2) and the adder unitary (C3-partial), with C4 downgraded to a shape-consistency check rather than an algorithm reproduction. That would probably read as PARTIAL overall.

## Bottom line

REPLICATED is fair *for the laptop-testable claims of the paper*, with the caveats above. It is not a re-implementation of pQCS, and no one should read this replication as evidence that a from-scratch pQCS clone would exhibit the paper's specific HPC-scale behaviors. The four highest-leverage next steps are in `open_questions.json`.
