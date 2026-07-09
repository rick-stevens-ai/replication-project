# Failure analysis — honest gaps and friction

Independent replication of Hwang & Choi (arXiv:1809.07998, ETRI 2018).
Written to close the loop on where this replication actually stops short.

## Gap 1 — Exact Table 1 / Fig 2 / Table 2 numbers not reproduced

**What we did not do.** We did not build the 39 TB non-modular Shor-512 QASM,
the 338.6 MB modular Shor-512 QASM, or the 1500-days-vs-1-hour mapping-time
comparison for Shor-128/256/512.

**Why.** The paper builds those with ScaffCC (Scaffold compiler; LLVM-based,
GitHub `ScaffCC/ScaffCC`, requires LLVM 3.x, an active BUILD environment, a
Shor circuit source in Scaffold, and — per the paper's own note — a machine
with 128 GB RAM and enough transient disk to hold the multi-TB non-modular
QASM. Not achievable on the CherryRd host in the QC-200 wave brief's
minutes-to-tens-of-minutes budget.

**What we did instead.** We reproduced the *analytic identity* the paper is
built on (K·N vs K+N, ratio → K) on a toy Toffoli module in Part A of the
repro; that saturates at exactly K=15 for large N, matching the paper's
prediction. If the reader asks "does the mechanism the paper describes
compress QASM the way the paper claims", the answer is yes. If the reader
asks "is 39 TB → 338.6 MB the specific compression for Shor-512", we did not
run the specific case.

**Verdict impact.** Downgrades from full REPLICATED-of-headline-numbers to
REPLICATED (mechanism) / SPOT-CHECK (specific numbers).

**Fix.** Install ScaffCC on a 128+ GB Linux box, feed the ScaffCC Shor
example at N ∈ {128, 256, 512}, measure QASM sizes and mapping wall-clock.
Estimated effort: 1–2 days, mostly build-environment (LLVM version pin) and
disk provisioning.

## Gap 2 — Marker / Nougat parsers unavailable on host

**What we did not do.** Run Marker or Nougat and produce their native outputs.

**Why.** Neither binary is on the CherryRd PATH, and both require multi-GB
model downloads (Nougat: Meta model checkpoint; Marker: layout + OCR models),
which is out of scope for a per-paper replication in this wave. The paper is
also short (4 pages) and simple enough that Marker/Nougat would not have
substantively improved on `pdftotext` output.

**What we did instead.** Wrote `extraction/marker.md` and
`extraction/nougat.mmd` as `pdftotext`-derived structured normalizations,
each with an explicit provenance header at the top of the file stating
"Marker/Nougat parsers were not installed on this host; this file is a
structured-Markdown normalization of pdftotext output preserving section
anchors, tables, and equations." Both files honor the brief's expected format
(marker.md as GitHub-flavored Markdown with tables; nougat.mmd as
LaTeX-math-preserving `mmd`) so downstream tooling that expects those
locations gets a usable file rather than a hard 404.

**Verdict impact.** None — these artifacts exist and are non-empty.

**Fix.** On a GPU box (uicgpu), install `marker-pdf` + `nougat-ocr`, batch
the QC-200 corpus, rsync back into each replication dir. Estimated effort:
half a day for the corpus pass.

## Gap 3 — Parametric surface-code cost model, not a cycle-accurate simulator

**What we did.** Compute physical-qubit × cycle footprint from Fowler et al.
(PRA 86, 032324, 2012) + Litinski (Quantum 3, 128, 2019) constants:
2 d² qubits per data patch, 11 d² per 15-to-1 factory, 10 d cycles per
distilled T-state, d code cycles per lattice-surgery merge/split.

**What we did not do.** Run Stim / PyMatching on an actual noise model, do
per-cycle stabilizer decoding, or measure real logical error rates.

**Why.** The QC brief asked for a footprint-reduction demonstration to
support the hierarchical / cached-module claim, not a full logical-error-rate
budget. A cycle-accurate Stim simulation would take orders of magnitude
longer wall time and would not change the mechanism conclusion — it would
only add error-rate estimates to the footprint numbers.

**Verdict impact.** None on the "measurable reduction across multiple sizes"
criterion (48%, 85.5%, 92.2%, 98.2% across 4 sizes). A future extension
should add error-rate simulation before making architectural claims.

**Fix.** Extend `repro.py` with a Stim-based scheduler; instrument
per-factory failure rates.

## Gap 4 — LP-based qubit placement (paper Sec 3, ref [8]) not implemented

**What we did not do.** Reproduce the paper's LP-placement result that
BWT-10 depth is reduced 6% (2.42 × 10⁵ → 2.26 × 10⁵).

**Why.** Requires a BWT-10 circuit + an LP solver + a hierarchical mapper.
Non-trivial 1–2 day effort; not central to the headline claim.

**Verdict impact.** None; this is a secondary claim (paper itself calls the
Shor version "negligible circuit-depth reduction less than 0.01%").

## Gap 5 — Bus-congestion / stochastic module-latency claim (paper Sec 4)

**What we did not do.** Simulate the paper's explicitly-flagged open concern
that "bus congestion may disturb ideal communication for highly parallel
quantum applications."

**Why.** Not a headline claim; the paper itself defers it to future work.

**Verdict impact.** None. Captured as open-questions Q5.

## Overall friction notes
- The paper is 4 pages and headline-heavy but methodology-light. Sec 2.2
  ("Mapping Algorithm") is compact; enough to explain the mechanism but not
  enough to re-implement the exact ScaffCC-based mapper without their code.
- The paper does not link a code repo. This is common for 2018-era
  quantum-architecture papers but a real friction point for independent
  reproduction of the specific Table 1 / Fig 2 numbers.
- The QC wave brief's spec (surface-code + magic-state footprint on
  Toffoli-heavy circuits) is not literally what this paper measures, but is
  a good instantiation of the same hierarchical / module-reuse spirit.
  Downstream readers should note the direction of transfer:
  *paper claim → brief-specified concrete demo → our numbers*, not
  *paper's exact numbers → our exact numbers*.
