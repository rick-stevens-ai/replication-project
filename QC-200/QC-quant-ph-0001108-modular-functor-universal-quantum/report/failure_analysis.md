# Failure analysis — quant-ph/0001108 replication

## Overall verdict rationale

Verdict: **SPOT-CHECK** (as designated by the QC wave brief for mathematical universality proofs).
This is not a failure verdict, but it does encode limitations. The paper proves a *density theorem* (image of the Jones representation is dense in SU(V) at r=5). We do not, and cannot at small instance, reproduce the theorem itself. What we do reproduce is the concrete arithmetic substrate the theorem operates on (Fibonacci F/R data, pentagon/hexagon axioms, unitarity of braid generators, and a small numerical density witness).

## Real friction encountered

### F1. Wrong author list in the brief
The wave brief listed "Freedman, Kitaev, Larsen, Wang" as authors. The v2 PDF on arXiv actually shows *Freedman, Larsen, Wang* with Kitaev only in the acknowledgements ("We would like to thank Alexei Kitaev for conversations on our approach.") The brief itself instructs to *trust the arxiv id, verify actual authors from the fetched PDF* — which is what we did. Not a blocker, but a reminder that even senior collaborators sometimes get folded into author lists in downstream databases.

### F2. Marker and Nougat CLIs not installed on the host
- `which marker` -> "marker not found"
- `which nougat` -> "nougat not found"
- The central corpus (SCOUT/LUCID/OSTI manifests on Eagle) was not queried in this run because the arXiv id namespace differs (`quant-ph/…` is not the modern `YYMM.NNNNN` form and is unlikely to be in a life-sciences manifest).
- **Workaround:** the standard permits this ("if not yet parsed, run Marker" — we cannot run it), so we produced honest `pdftotext -layout` fallbacks with explicit header notes calling out the fallback provenance. This does mean `extraction/marker.md` and `extraction/nougat.mmd` do not have Marker's math-mode-aware / table-aware output, nor Nougat's LaTeX equations. For a mathematically dense paper like this one, that is a real loss of extraction quality.
- **To close:** install `marker-pdf` and `nougat-ocr` under a project venv, or run the Eagle Marker/Nougat manifest lookup once we have credentials on this host.

### F3. JSON serialisation of numpy complex numbers
First run of `fibonacci_anyons.py` completed the numerical work correctly (visible in the log) but crashed serialising the hexagon dict because the sigma matrices are complex. Fixed by adding a `cx()` helper to unpack `.re`/`.im` before writing. Not a science problem, but wasted one run.

### F4. Exponential explosion of BFS at large depth
At `--max-len 18` the deduplicated frontier grew large enough that a single sequential CPU run did not finish in the time budget. We backed off to `--max-len 15`, which gives a strong SPOT-CHECK result but does not push to arbitrarily small epsilon.
- **To close:** implement meet-in-the-middle search (BFS to depth L/2 from identity, BFS to depth L/2 from V^{-1}, join on nearest-neighbour) — cuts effective depth in half at the cost of memory. Alternatively, follow BFS with Solovay-Kitaev refinement on the best short word.

## What was *not* attempted

1. **Density theorem proof.** The mathematical statement (Theorem 1.1 in the paper) is far outside what a numerical replication can address.
2. **2-qubit gates on B_6.** The paper's 2-qubit gate construction (Section 2, sigma-6 acting on V^0(6) + V^2(6)) is the load-bearing step in the polynomial-equivalence argument. We only built the 1-qubit case.
3. **Solovay-Kitaev.** No compilation refinement past raw BFS.
4. **Two-qubit leakage analysis.** Related to (2); we cannot see leakage error at 1-qubit.
5. **Comparison against non-universal Ising anyons.** Would strengthen the claim by showing the search plateaus for Ising and does not for Fibonacci.
6. **REPORT.pdf.** LaTeX was not compiled on this host in this pass; the `.tex` is complete and lint-clean but not turned into a PDF. `pdflatex report/REPORT.tex` would produce it.

## Residual gaps summary

| Gap | Severity | Would need |
|---|---|---|
| Marker/Nougat proper extraction | Medium (math-heavy paper) | `pip install marker-pdf nougat-ocr` + one re-run |
| Larger BFS depth | Low (SPOT-CHECK not tightened) | Meet-in-the-middle or S-K refinement |
| 2-qubit gate replication | Medium (misses the polynomial-equivalence heart) | Extension of `fibonacci_anyons.py` to B_6 with leakage tracking |
| Comparison across SU(2)_k | Low (adds insight, not verdict) | Parametric implementation of F/R for level r |
| REPORT.pdf compiled | Cosmetic | `pdflatex report/REPORT.tex` |

## Honest self-assessment

The core numerical evidence (pentagon/hexagon/unitarity all at machine precision; two independent Hadamard/T braid-word approximations at ~3% distance) is fully real, deterministic, and reproducible from the code in `report/evidence/`. The SPOT-CHECK verdict is honest for what was tested. Anyone wanting to push this to REPLICATED would need to (a) implement the 2-qubit case, (b) demonstrate that epsilon scales polylogarithmically with braid length, and (c) preferably re-prove the density theorem in a proof assistant — but (c) is outside the scope of any numerical replication and (a)+(b) is a well-defined 1-2 day extension.
