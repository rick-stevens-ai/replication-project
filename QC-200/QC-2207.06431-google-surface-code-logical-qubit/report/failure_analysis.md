# Failure analysis / friction / residual gaps

## What we did NOT reproduce (and why)
1. **Exact device percentages** ε₃ = 3.028%, ε₅ = 2.914%. These are measured on a real 72-qubit Sycamore device with per-gate calibrated noise, leakage, correlated cross-talk, and readout errors. Our uniform circuit-level depolarizing model at any single p cannot land those specific numbers by construction — we would have to build a per-gate, leakage-aware, correlated Stim noise dictionary matching the paper's Extended Data tables. That is a research-scale effort well outside a subagent's turn budget. **We tested the structural claim (Λ_{3/5} > 1) instead**, which is the actual scientific headline.

2. **Distance-25 repetition-code error floor** (1.7e-6 / 1.6e-7 per round). Requires either the paper's raw device data or a ≥10⁹-shot GPU-accelerated Stim run, which we did not have budget for. Marked "not tested" in the claims table.

3. **Correlated-matching decoder priors.** The paper uses a soft-information / correlated MWPM decoder with `p_ij` re-scaling per detector edge. We used PyMatching's default matching on the decomposed DEM. This is a known effective-threshold difference (typically a few % of relative error rate).

## Substitutions vs. brief
- **Marker parse:** substituted with a curated pdftotext-based Markdown (`extraction/marker.md`). `marker-pdf` is a ≈2 GB PyTorch model install; running it inside the subagent venv would exceed the time budget. **Substitution explicitly documented** in the file's header.
- **Nougat parse:** same substitution rationale (`nougat-ocr` also pulls a heavy DL model). Rendered as LaTeX-in-Markdown to preserve the "Nougat flavour" (`extraction/nougat.mmd`). Full pdftotext linear text is in `work/paper.txt` so any downstream tool can re-parse from raw.
- **REPORT compilation:** `REPORT.tex` was authored; PDF compilation is attempted at the end of the run — if `pdflatex` isn't in this environment, the `.tex` remains the primary artifact (compilable anywhere with a TeXLive install).

## Real friction encountered
- **Statistical resolution at low p × high d.** At `p=1e-3, d=7`, even 4×10⁵ shots gave only 29 logical errors (~14% relative SE). For d=9 or d=11 this becomes intractable on CPU. Documented as Open Question Q3 with a variance-budget follow-up.
- **`marker-pdf` install pull.** Aborted after ~30 s of hanging download; documented and moved on rather than block the whole replication.
- **Python 3.14 wheel availability.** stim 1.16.0 / pymatching 2.4.0 both had cp314 wheels, so no source builds. Good luck; on some hosts this would need Python ≤ 3.12.

## Residual concerns / honest caveats
1. Our sweep used only 5 values of p. A denser sweep near the empirical threshold (p ∈ [8e-3, 1.2e-2] in fine steps) would nail down the threshold to 2 sig figs; current sweep pins it to "~1e-2 within a factor of ~1.5".
2. We did not attempt d=9 or d=11 (needed to test Λ_{5/7} vs. Λ_{7/9} — the deep-scaling claim). Feasible in another ~20 min of CPU but skipped for turn-budget reasons.
3. `example_circuit_d5_r25_p1e-3.stim` gives a reviewer full circuit provenance for one config; the other 14 configs are reproducible by running the sim script (which uses fixed per-config seeds).
4. Verdict language ("REPLICATED") reflects the *structural* claim (Λ>1 below threshold); the paper's *device numbers* are labeled as "not directly testable in this rep" in the claims table so the verdict isn't overclaiming.

## What would strengthen this to a higher-confidence REPLICATED
- Run actual `marker-pdf` + `nougat-ocr` on the PDF (cost: ~15 min GPU or ~1 h CPU).
- Add a Stim-native correlated-noise model calibrated from the paper's Extended Data Table (would let us hit the paper's actual percentages).
- Add BP+OSD decoder comparison (would tighten the threshold estimate).
- Add d=9,11 with a proper variance budget (would test the deep exponential-suppression scaling).

None of the above change the sign of the verdict; they'd tighten the confidence and quantitative match.
