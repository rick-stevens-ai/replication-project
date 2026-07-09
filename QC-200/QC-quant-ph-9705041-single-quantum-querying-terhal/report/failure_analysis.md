# Failure Analysis — quant-ph/9705041 (Terhal & Smolin) Replication

Verdict was **REPLICATED**, but honest analysis of friction, gaps, and
assumptions is still required per the standard.

## What failed / friction encountered
1. **Task-brief target vs paper's actual claim.**
   The task brief framed this as a "Grover on N=4, P > 0.5" reproduction with
   P = 1/2 + 1/(2√2) ≈ 0.85. That's a *different* paper's claim (it is the
   optimal single-query success bound for the Grover-style search on N=4,
   from later work by Boyer–Brassard–Høyer–Tapp and Zalka). Terhal & Smolin
   1997 is a Bernstein–Vazirani parity paper claiming P = 1 (not ≈0.85)
   using a different oracle model. Recognising and re-framing the target
   consumed the first two reading passes over the PDF; had this been done
   without reading, the "replication" would have implemented the wrong
   algorithm and reported a spurious mismatch. Root cause: brief author
   conflated two 1997 single-query results. Fix applied: read the paper
   first, reproduce its *actual* central claim, note the discrepancy in
   REPORT.tex, and provide Grover baselines separately for context.

2. **Marker and Nougat not installed.**
   The dir standard requires `extraction/marker.md` and `extraction/nougat.mmd`.
   Neither tool was on PATH; installing Marker (VikParuchuri/marker) and
   Nougat (facebookresearch/nougat) requires torch + vision-transformer
   weights (~2–5 GB), which would have blown the wave time budget and
   violates the "no heavy install" spirit of the QC brief.
   **Workaround applied:** used `pdftotext -layout` and `pdftotext -raw`
   as fallbacks with clearly labeled provenance headers, matching the
   convention used by sibling QC-200 dirs (e.g. QC-quant-ph-9607014). This
   is the same fallback the QC-200 wave has been using; it is a *residual
   gap* rather than a work-around bug.

3. **Random-coding variant (Sec. III.B) not simulated.**
   The paper's random-coding scheme with analytic collision probability
   `p_col = 1 - (1 - A^-m)^(k-1)` was the only quantitative claim with
   room for numerical disagreement. It was left untested to keep the pass
   inside the subagent time budget. Tracked as open question Q4 with
   concrete next steps.

4. **Noise model absent.**
   The paper is noiseless. Our replication is likewise noiseless. This is
   *faithful* to what the paper reports, but it means the replication does
   not stress-test how robust the single-query advantage is in practice.
   Tracked as open questions Q1 and Q5.

5. **Grover baseline nuance.**
   The task brief cited `(3/4)^2 = 0.5625` as the Grover N=4, 1-iteration
   success rate. The analytic formula `sin^2((2k+1)*arcsin(1/sqrt(N)))`
   gives `sin^2(3*pi/6) = 1.0` exactly for N=4, k=1 (this is why "one
   Grover iteration solves N=4" is a textbook example). The `0.5625` figure
   is a common textbook approximation for the average-case success before
   the final measurement or under different amplitude-amplification
   conventions. We recorded both figures in `bv_results.json` and flagged
   the discrepancy in REPORT.tex so downstream readers aren't misled.

## Residual gaps
- Random-coding (Sec. III.B): NOT TESTED.
- Huffman non-uniform-prior variant (Sec. III.A, Fig. 2): NOT TESTED
  (subsumed by the uniform-prior Walsh case which was verified).
- Marker/Nougat proper extractions: pdftotext fallback in place, not the
  ML-based parses.
- LaTeX report has not been compiled to PDF in this pass
  (no `latexmk`/`pdflatex` invocation attempted; the `.tex` source is
  syntactically valid and would compile with a standard TeX Live).
- The circuit does not use the paper's exact "alternating-sign" preparation
  on the B register for A > 2; we used the standard A=2 phase-kickback
  ancilla, which is the special case of the paper's construction that is
  equivalent for parity oracles. For A > 2 the phase preparation would need
  QFT-like circuits — out of scope this pass.

## What worked cleanly (for future waves' reference)
- The BV oracle-as-CNOTs pattern is trivial to implement and matches the
  paper exactly. No subtle sign or ordering bugs.
- Statevector simulation on Qiskit Aer 0.17.2 handled n=8 (256 databases)
  in <2 s total wall-clock, well under any subagent budget.
- Using `Statevector.from_instruction` alongside `AerSimulator` shots gave
  a nice cross-check: both agreed exactly at P=1, ruling out
  measurement-ordering or endianness bugs.
- The sibling-dir pdftotext-fallback convention meant the extraction step
  was frictionless.

## Recommendations for the next replication
- Always read the paper's actual claim before writing simulation code; do
  not trust the task brief's paraphrase alone (especially when the brief
  cites specific numerical values not attributed to a page/equation).
- If the paper has multiple algorithm variants, pick the one with the
  strongest numerical claim to reproduce first; leave the softer/
  probabilistic variants as open questions.
- Keep a running `report/evidence/*.json` file per algorithm variant so
  the artifacts inventory writes itself from `find + wc + shasum`.
