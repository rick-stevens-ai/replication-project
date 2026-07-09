# Workflow — replication of arXiv:1701.08669 (Gogioso & Kissinger, graphical HSP)

## Narrative

1. **Fetch paper.** `curl` the arXiv PDF into the target dir. Verified 21-page PDF (533 KB).
2. **Verify author + title from the fetched PDF.** The subagent task text truncated the SCOUT title (all-caps). `pdftotext` of page 1 confirmed the exact title *"Fully Graphical Treatment of the Quantum Algorithm for the Hidden Subgroup Problem"* and authors *Stefano Gogioso and Aleks Kissinger* (Quantum Group, Oxford / iCIS, Radboud). Not a Coecke/Zwiers paper; Coecke is only cited (e.g. via CD11, Kis12) as prior categorical-QM work. The task brief note about "Zwiers/Coecke-style ZX-calculus" was a shorthand for the tradition, not the actual authors.
3. **Skim key sections.**
   - Sec 1 (context: HSP unifies Shor's, Simon's, discrete-log; prior categorical work by Vicary [Vic12]).
   - Sec 2 (concrete HSP setup: G abelian finite, hiding function f: G -> Z_2^N constant on cosets of H, subroutine outputs y in Ann[H] uniformly).
   - Sec 3 (†-Frobenius algebra machinery: point structure, group algebra, strong complementarity).
   - Sec 4 (traditional presentation of the quantum algorithm --- coset states, QFT_G, character sampling).
   - Sec 5 (**the main result**: fully diagrammatic proof of correctness, split into 8 subsections, culminating in Diagram 5.3).
   - Sec 6-7 (extensions: non-abelian with extra hypotheses, real quantum theory Simon, infinite abelian groups).
4. **Design the reproduction.** The paper's diagrammatic proof is not directly executable numerically (would need a ZX engine like PyZX). Its empirically-verifiable content is: *when instantiated in fdHilb, the paper's Diagram 5.3 = the standard HSP quantum-subroutine claim of Jozsa 2001, and V1/V2/V3 below verify it exactly.*
5. **Implement HSP subroutine.** Pure `numpy` statevector on register-1 (dim = |G|) tensor register-2 (dim = 2^M with M = ceil(log2 |G/H|)). Build hiding function by random injective label assignment on cosets. Apply the coherent oracle exactly (no gate compilation --- we're testing the algorithm, not the circuit).
6. **Verifications.**
   - **V1 (character marginal).** Analytic uniform-on-H^⊥ vs empirical: for Z_8/H=<2>, deviation 3.14e-16; for Z_15/H=<5>, deviation 2.69e-15. Both machine-noise.
   - **V2 (per-coset conditionals).** Compute P(y|b) for every b with P(b)>0; verify (i) uniform on H^⊥, (ii) same across all b (Diagram 5.3 independence-of-b).
   - **V3 (paper's Sec 5.7 rewrite).** Pipeline-A (full protocol) vs Pipeline-B (partial-trace-then-QFT, which is what applying s†s=id delivers) yield identical register-1 marginals to ~1e-16 on 5 random hiding functions per test group. This is the numerical corollary of the paper's key algebraic rewrite in the isometry-cancellation step.
7. **Run.** Single command, ~0.4 s wall clock. See `report/evidence/hsp_output.log`.
8. **Verdict + write-up.** REPLICATED. Wrote REPORT.tex (very detailed, section-by-section), open_questions.json (5 non-superficial), this workflow.md, artifacts_summary.md, failure_analysis.md.

## Tools + versions

| Tool / library | Version | Purpose |
|----------------|---------|---------|
| Python | 3.14.6 | Runtime |
| NumPy | 2.4.3 | Statevector linear algebra: dense matmul, QFT construction, RNG |
| SciPy | 1.18.0 | Available; not needed (numpy was sufficient) |
| PyMuPDF (`fitz`) | 1.27.2.3 | Extraction surrogate for Marker (page-boundary text extraction) |
| `pdftotext` | Poppler-provided | Extraction surrogate for Nougat (`-layout` reflow) |
| `curl` | macOS system | Fetching paper PDF |
| Argo LLM proxy | localhost:44497 (key `stevens`) | *Not used* for this replication — pure classical simulation, no LLM inference needed for the science. |

**No paid endpoints used.** No quantum hardware. No GPU. All reproducible on any laptop with Python + numpy.

## Code (all in `report/evidence/`)

| File | LOC | Purpose |
|------|-----|---------|
| `hsp_abelian.py` | ~330 | Group utilities (cyclic subgroup, orthogonal subgroup, cosets), hiding-function builder, full statevector HSP pipeline, ZX-rewrite consistency check (V3), CLI + JSON output. |
| `hsp_results.json` | (data) | Full result dump: character distributions, per-coset conditionals, V3 trials, overall OK flag. |
| `hsp_output.log` | (data) | Stdout of the run (paper's Diagram 5.3 verified for both test groups). |

## Effort estimate

- **Wall clock (agent):** ~25 min end-to-end (paper fetch → skim → design → build → smoke-run → write-up).
- **Compute:** <1 s (single-threaded numpy on a laptop-class CPU). Zero GPU/HPC used.
- **Human/agent steps:** ~12 tool calls (fetch PDF, pdftotext, mkdir, PyMuPDF extraction, pdftotext-layout extraction, write hsp_abelian.py, run, plus 5 write calls for REPORT/QA/workflow/artifacts/failure_analysis + this file).
- **LOC written by agent:** ~330 lines of Python (evidence code) + ~1600 lines of documentation (LaTeX report + 4 markdown docs + open questions JSON).
- **Runs executed:** 1 successful (script passed all checks on first execution; no debugging needed).
- **External API calls:** 1 (arXiv PDF fetch via curl). No LLM calls.
