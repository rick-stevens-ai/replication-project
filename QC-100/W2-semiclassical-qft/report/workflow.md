# Workflow — Semiclassical Fourier Transform Replication

**Paper:** Griffiths & Niu, *Phys. Rev. Lett.* **76**, 3228 (1996).
**Set:** QC-100. **Dir:** `W2-semiclassical-qft/`.
**Replicator:** Ollie (CherryRd), 2026-06-26. Backfill by Kukla, 2026-07-06.

## Environment
- Host: CherryRd (macOS, x86_64).
- Language: Python 3 with numpy only. No quantum-framework dependency
  (deliberately clean-room to prove the claim on first principles).
- Total runtime: sub-second (all experiments are exact-distribution enumerations).
- No paid API calls; no hardware queue; no data downloads.

## Steps

1. **Read the paper.** Griffiths–Niu is a short PRL that states an equivalence
   theorem: the iQFT step in phase estimation can be replaced by measure-and-
   feed-forward on single qubits, producing an identical output distribution.
2. **Choose a test setup.** Single-qubit unitary $U$ with eigenvalue
   $e^{2\pi i \varphi}$ on $|1\rangle$; $k$ counting qubits; controlled-$U^{2^j}$
   ladder produces the standard pre-iQFT product state.
3. **Implement Method A (coherent).** Build the $k$-qubit inverse-QFT unitary
   explicitly ($2^k \times 2^k$ matrix), apply to the pre-iQFT state, take
   $|amplitudes|^2$ as the output distribution.
4. **Implement Method B (semiclassical).** Iteratively enumerate every classical
   measurement branch, tracking the branch probability and the feed-forward
   phase correction to remaining qubits. Yields the exact per-outcome
   probability (no Monte-Carlo sampling).
5. **Compare.** Compute total-variation distance between the two full
   distributions for each $(\varphi, k)$ configuration.
6. **Sweep configurations.** 8 experiments spanning exactly-representable
   phases ($\varphi = 0.375, 0.0625, 0.5, 0.8125, 0.46875$) and
   non-representable phases ($0.1, 0.7, 1/3$) at $k \in \{3, 4, 5\}$.
7. **Debug convention bugs.** First attempts reported TV $\approx 1.0$; root
   cause was inconsistent bit-order / endianness between the two methods.
   Diagnosed using $\varphi = 0.375 = 0.011_2$ ($k=3$, must return $y=3$).
   Fixed both methods to use the identical index mapping; the buggy version
   is preserved as `replicate_subagent_buggy.py` for provenance.
8. **Write results.** `results.json` records all 8 experiments; `REPORT.md`
   (top-level) is the primary human-readable summary.
9. **Backfill (2026-07-06).** Kukla added `report/*.tex`, `open_questions.json`,
   `workflow.md`, `artifacts_summary.md`, `failure_analysis.md`, and
   `extraction/nougat.mmd` stub. No simulations re-run; existing files preserved.

## What could go wrong (and did)
- **Endian / bit-order between iQFT matrix and iterative measurement loop.**
  This was the actual bug that caused the initial disagreement. Any
  independent replication should double-check this convention on
  $\varphi = 0.375, k=3$ before believing large TV distances.
- **Non-representable phases produce non-trivial distributions.** Both methods
  must agree on the same nearest-grid MAP estimate AND the same full
  distribution, not just the MAP. That is what we verified.

## What was NOT done
- No gate-count / circuit-depth inventory comparing the two methods.
- No noisy-simulator run (measurement noise, readout error, gate error).
- No hardware-runtime measurement.
- No forward-QFT variant.
- No integration test with modern QPE front-ends (Kitaev iterative,
  rejection-sampling, robust phase estimation).

These are captured as open questions in `open_questions.json`.
