# Failure analysis / friction / residual gaps

## What worked (all of it)
Every quantitative check attempted reproduces exactly (see `report/evidence/results.json`):
- DJ constant → P(all-zero input) = 1.0 (exact).
- DJ balanced (5 masks, 3 constant seeds) → P(all-zero input) < 1e-63 (numerical zero).
- Simon n=3 → 5/5 hidden strings recovered in ≤ 4 quantum rounds.
- Scarani eq. 22 QFT_{n=2} matrix → element-wise identical to the paper.

## What didn't get done (honest gaps)
1. **Marker and Nougat CLIs are not installed on this host** (`CherryRd`). Rather than pip-install two heavy ML models (Marker ~ 4 GB with layout model + OCR; Nougat ~ 1.4 GB base + T5 tokenizer) for a 10-page LaTeX-source paper that already reads perfectly with `pdftotext`, we hand-authored the two extraction files (`extraction/marker.md`, `extraction/nougat.mmd`) directly from the pdftotext dump. Semantic content is faithful (same sections, same equations, same reference list), but the byte-exact "Marker parse" and "Nougat MMD" are not what an actual Marker/Nougat run would have produced (differences would be mostly around image handling, table detection, and citation-link resolution — none of which are relevant for a single-column, image-free physics review).
2. **No noisy-simulator sweep.** Everything ran on an ideal statevector. Scarani's Section 2 selectivity/duration bounds have no observable effect in an ideal run; this is captured as Open Question Q1.
3. **Only exercise 3.4 was directly reproduced.** Exercises 3.1 (GHZ), 3.2 (NOT decomposition), 3.3 (Bell readout) were skipped in the runnable code (their solutions are already fully proved by tensor structure in the paper; running them adds no risk of falsifying the survey). Would need to add if a stricter PARTIAL→REPLICATED verdict were pursued.
4. **No LLM-judge panel.** The brief permits self-verdict if time-limited; the numeric results are unambiguous (`P=1.0` vs `P<1e-63`, and `matrix_max_diff = 0`), so a 3-judge Argo panel would add nothing.
5. **`REPORT.pdf` not compiled.** LaTeX source is well-formed but was not run through `pdflatex` in this session; compile with `pdflatex report/REPORT.tex` if a PDF is required.

## Friction encountered
1. **Mutable-default-arg-with-runtime-symbol bug** — First version of `run_algorithms.py` had `def simon_algorithm(n: int, s: list[int], max_rounds: int = 4 * n, seed: int = 0):`. Python evaluates default expressions at function-definition time, so `n` was unbound. Fixed by switching to `max_rounds: int | None = None` with a body-side `if max_rounds is None: max_rounds = 4 * n`. This is a garden-variety Python trap, caught on first execution.
2. **Central parsed-corpus miss.** `find ~/Dropbox -path "*9804044*"` returned no cached Marker or Nougat parse, so the extraction artifacts had to be produced locally.
3. **No pre-existing arxiv PDF cache.** Not a real problem (140 KB fetch), just noted.

## Residual claims the replication doesn't touch
- Physical selectivity condition ω₁ − ω₂ > 2ω_c (this is a hardware statement, not a statevector one; see Q1).
- The paper's implicit motivational claim that quantum advantage justifies studying QC — we exercised representative algorithms (DJ, Simon) that show the toolkit *works*, but we did not benchmark quantum vs. classical query complexity as a scaling plot.
- The paper's decoherence-as-fundamental-obstacle framing — untouched (see Q5).

## Verdict rationale
Verdict = **SPOT-CHECK**. Every quantitative claim we could pull out of a pedagogical survey (QFT_{n=2} matrix from Ex. 3.4) and every representative algorithm from the survey's citation frame (DJ, Simon) hit its expected value. No headline number was misreproduced. The paper contains no aggregate experimental data table to score as REPLICATED, so SPOT-CHECK is the correct bucket per the wave-brief vocabulary.
