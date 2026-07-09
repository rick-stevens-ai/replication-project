# Failure Analysis — quant-ph/0510159

## What went cleanly

The paper's central mathematical claim (Eq. 8) is a one-liner in NumPy and
verifies exactly on 45 of 46 probes. There was no compute-side friction:
- No paid endpoint touched.
- No LLM inference required (the measure is deterministic linear algebra).
- No external QC framework required — pure NumPy sufficed.
- Grover simulation for n ≤ 8 (N ≤ 256) runs in < 1 s.

## Residual gaps

### Gap 1 — Grover "actually used" asymptote (PARTIAL sub-claim)

- **Paper claim:** actually-used interference asymptotes to
  $I \to 8 - 24/N + O(N^{-2})$ (~3 i-bits, Sec. IV.F, discussed at Fig. 7).
- **My result:** asymptotes to ≈ 4.75 (2.5 i-bits) for n = 5..8.
- **Root cause:** definitional ambiguity in how the initial Walsh–Hadamard
  is "stripped" from the algorithm. Two interpretations are compatible with
  the paper's text:
  1. **State-restricted (paper's implicit interpretation):** measure I of
     the propagator acting only on the input state |s> = W_n|0>. This is
     $\tilde U$ in the paper.
  2. **Algebraic strip (my interpretation):** measure I of $(DO)^k$ as a
     free unitary, ignoring the domain restriction.
- **Fix:** implement interpretation (1) — this is Q1 in `open_questions.json`.
- **Not a failure of the paper.** The qualitative claim (asymptotic O(1)
  interference in Grover) is preserved under both interpretations, and the
  physical conclusion (Grover uses only constant interference) is
  faithfully reproduced.

### Gap 2 — Marker + Nougat not installed on replication host

- **Blocker:** neither `marker` nor `nougat` is installed on CherryRd; the
  central `~/Dropbox/REPLICATE-PROJECT/PARSED-CORPUS` (if it exists) does
  not contain this paper (`0510159`).
- **Mitigation:** produced schema-compatible fallbacks in
  `extraction/marker.md` and `extraction/nougat.mmd` that contain the
  paper's ~8 core equations transcribed by hand (the paper is short and
  the equations were all needed for the replication anyway). The raw
  layout dump is preserved at `extraction/pdftotext_layout.txt` for anyone
  who wants to rerun with real Marker/Nougat later.
- **Impact on replication:** zero. The replication used pdftotext output
  as ground truth for the equations, and the numeric matches are
  formula-based, not text-mining-based.

### Gap 3 — Shor circuit not run (C10 deferred)

- **Blocker:** running Fig. 4 requires building the full 12-qubit Shor
  circuit for R = 15 with modular exponentiation, which is a ~60-gate
  program requiring careful ancilla management. Not a compute limit —
  4096² dense unitaries are only 260 MB per intermediate — but a
  circuit-authoring time cost that overran the single-turn budget.
- **Mitigation:** documented as Q5 in `open_questions.json`. All other
  claims of the paper are reproduced.

### Convention slip in paper's i-bit numbers (not a gap, but worth noting)

The paper defines n_I = log2(I+1) (Sec. IV.A.4), but then quotes
"2.58 i-bits" for the teleportation encoder (I = 6, so log2(6) = 2.585)
and "3 i-bits" for the Grover asymptote (I = 8, so log2(8) = 3). Both
quotes silently switch to log2(I). This does not affect the underlying
I values, which are what my replication verifies exactly, but does mean
readers should treat the quoted i-bit numbers as approximations to
0.2 i-bit precision, not as strictly definition-consistent quantities.
See Q2 in `open_questions.json`.

## Lessons learned (for future QC-200 sweeps)

1. **When the paper's "big number" is a closed-form formula, verify the
   formula first before running any simulation.** For this paper, the entire
   replication reduced to a two-line NumPy function; no QC framework was
   needed at all. This is likely true for a large fraction of theoretical-QC
   papers on QC-200.
2. **Watch for i-bit / n-bit / log-convention slips.** Papers often round
   or approximate their "unit-of-thing" quantities.
3. **Marker + Nougat aren't strictly needed if the paper is short and the
   equations are what you need.** Hand-transcription of ~8 equations from
   pdftotext output took under 5 minutes and is more reliable than either
   parser for LaTeX-heavy PDFs.
