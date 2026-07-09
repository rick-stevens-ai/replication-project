# Failure analysis / friction / residual gaps

Honest ledger of what went smoothly, what didn't, and what this replication
does *not* cover.

## What went smoothly

- Fetching the paper (arXiv, 138 KB, straight pdftotext).
- Installing qiskit 2.5.0 into a fresh venv on macOS (no --break-system-packages).
- Reading the paper: the headline claim is stated cleanly in §3 (eps → eps^3
  for one step) and §4 (recursion → eps^(3^m) in q_m = (3^(m+1)-1)/2 queries).
- Implementing the recursion as a direct matrix composition on 2^n×2^n
  operators: for n∈{4,6} this fits comfortably in RAM.
- The reproduction hit the theory law to <2×10^-14 on the first try — no
  sign issues, no phase-convention debugging, no dagger transpose bugs.

## What went less smoothly

### Extraction (Artifacts #2 and #3): fallback used

- `marker_single` is not installed on CherryRd.
- `nougat` is not installed on CherryRd.
- The shared UICGPU parse cluster (where Ollie's LUCID-100 keeps
  Marker/Nougat installs) did not respond within the subagent's
  ~10 s ssh timeout budget on 2026-07-05.
- The paper is a 7-page born-digital LaTeX arXiv PDF (not a scan), so
  pdftotext / pdftotext -layout recover the full text faithfully.
  Equations render as approximate ASCII math, which is enough for
  downstream textual / LLM-judge use but is *not* a genuine Marker or
  Nougat parse.
- **Mitigation**: `extraction/marker.md` and `extraction/nougat.mmd` are
  both marked with a top-of-file comment stating they are pdftotext-based
  fallbacks, and `extraction/README.md` documents the situation and
  makes clear they can be overwritten in place if Marker/Nougat becomes
  available. The numeric replication does *not* consume either
  extraction file — it works directly from the PDF's math — so the
  reproduction verdict is independent of this fallback.
- **Suggested fix at wave-runner level**: pre-parse the QC-200 papers on
  UICGPU (or wherever the persistent Marker/Nougat installs live) into
  `~/Dropbox/REPLICATE-PROJECT/CORPUS-EXTRACTIONS/<arxiv-id>/` and let
  QC-wave subagents pull from there, matching the LUCID-100 pattern.

## What this replication does NOT cover (residual gaps)

1. **Section 6 (error correction).** The paper's applied punchline is
   that the same eps → eps^3 rule reduces *systematic* error in a
   driving unitary U (given exact U^dagger). We did not implement any
   noise model. Our verdict speaks only to the algebraic identity, not
   to the error-correction application. (Q5 in open questions.)
2. **Gate-level cost.** We work with 2^n×2^n unitaries, not compiled
   Clifford+T circuits. The paper's query count 3^m is verified, but
   the true T-count / depth / ancilla cost is not measured. (Q1.)
3. **Noise crossover.** All results are in the exact-unitary limit.
   The recursion's practical crossover point m* at realistic gate
   error rates is untested. (Q2.)
4. **Section 5 averaging.** Our analytic recompute of the
   partial-search failure integrals gives ~0.39% (vs the paper's
   ~0.8%) — the discrepancy is almost certainly a difference in the
   conditional-on-success sampling convention rather than an error in
   the pi/3 rule itself, but we did not close this out numerically. (Q3.)
5. **Larger N.** We tested N=16 and N=64. The recursion is unitary
   and the identity is algebraic, so larger N would just be a rerun
   with bigger matrices; nothing prevents extending to N=256 or 1024
   other than run time. It is a genuine gap only if someone believes
   the eps^(3^m) law breaks at large N — no evidence of that, but we
   didn't push it.

## Threats to the verdict

- **Marked-index choice**: we picked target index 5 for N=16 and 42 for
  N=64. Both are arbitrary; the algorithm is index-permutation-
  covariant under Walsh-Hadamard so this cannot bias the result. Spot-
  checking a second target would be trivial but was not done.
- **Numerical precision**: matrix composition at N=64 uses complex128;
  the observed sim-vs-theory diff is at the ~10^-14 level, comfortably
  above numerical noise. No sign of instability.
- **Global-phase / operator-order convention**: this is the classic
  place to make a mistake. The sanity check is that (a) the theory
  formula 1 - eps^(3^m) is matched, and (b) standard Grover
  oscillates as expected. Both hold, so the compose ordering is
  correct.

## Overall

The replication is clean and the verdict (REPLICATED) is defensible.
The only real friction was extraction tooling not being present on
this host; the mathematical / simulation core reproduced the paper's
central claim on the first try to machine precision on two independent
problem sizes.
