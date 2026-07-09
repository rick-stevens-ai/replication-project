# Failure Analysis — quant-ph/0206003 Replication

Honest accounting of what didn't work cleanly, where corners were cut,
and what residual gaps remain.

## What actually failed / was skipped

### 1. Marker + Nougat parses were surrogate, not real

- The central Marker/Nougat corpus at
  `~/Dropbox/REPLICATE-PROJECT/pde_corpus/` (and adjacent dirs) has no
  pre-parsed output for `arXiv:quant-ph/0206003`.
- `marker_single` and `nougat` binaries are not installed on cherryrd
  (the runtime host for this subagent). Installing them (marker via
  `pip install marker-pdf`, nougat via `pip install nougat-ocr` + the
  ~1.5 GB checkpoint) is a ~15-30 min side quest that would likely
  time out this subagent's turn.
- **Workaround** (matches the sibling QC-200 dirs, e.g.
  `QC-0807.4994-quantum-random-access-memory/`): produced surrogate
  `extraction/marker.md` (pdftotext-derived Markdown with manual
  section boundaries) and `extraction/nougat.mmd` (same text with
  LaTeX equations reformatted, as Nougat would). Both files carry a
  header block disclosing the surrogate origin.
- **Residual gap:** the surrogate files do not carry Marker's figure
  detection or Nougat's fine equation-recognition heuristics. If a
  downstream QC-200 corpus tool depends on genuine Marker/Nougat
  bit-for-bit output, these two files would need to be regenerated on
  a host with the real parsers.

### 2. Claim C5 (classical 3CNF-reconstruction algorithm, Section 4) not tested

- The paper's Section 4 result is that a *classical* polynomial-time
  algorithm can reconstruct a 3CNF Φ from polynomially many
  "how-many-clauses-violated" queries. This is a **separate
  algorithmic experiment** that has nothing to do with quantum
  simulation and would need its own implementation (LP-style
  reconstruction over the clause-count oracle).
- Skipped as out of scope for a single-turn subagent focused on the
  numerical core of Section 5.

### 3. Claim C6 (narrow-basin exponential-gap construction, Section 6) not tested

- The paper's Section 6 constructs a Hamming-weight function `f` with
  a narrow basin at `1^n` and proves the gap is exponentially small
  at a critical schedule value. Verifying this numerically is
  tractable at small n via Hamming-weight-block-diagonalization
  (H reduces from 2^n × 2^n to (n+1) × (n+1)), but the exact `f`
  described in the paper takes a paragraph of translation into code,
  and choosing the ε window carefully to reproduce the paper's
  s_c-crossing is a full mini-project on its own.
- Skipped as out of scope; flagged as Q5 in `open_questions.json`.

## What was done, but only crudely

### 4. Coarse c-grid in C3b

- The threshold prefactor `c*` giving `P_success >= 0.9` was resolved on
  the coarse grid `c ∈ {1, 2, 4, 8, 16, ...}`, so all three sizes
  (n=2,3,4) hit `c* = 4`. That may hide a mild N-dependence at the
  10-20% level. Rick's brief says "small-but-faithful instance size"
  and the qualitative claim (linear-in-N scaling of T*) is unaffected,
  but the exact prefactor deserves bisection.
- Flagged as Q2 in `open_questions.json`.

### 5. Piecewise-constant integrator (n_steps = 800) not convergence-tested

- The Schrödinger integrator uses 800 piecewise-constant sub-intervals
  and `scipy.linalg.expm`. This is a **first-order product formula**
  in Δt with error O(Δt · T · max ||H'||). At T=400 and n_steps=800
  (Δt = 0.5), the leading error should be well under 10^{-4} — but it
  wasn't measured. A convergence sweep (n_steps ∈ {200, 400, 800,
  1600}) at the largest T would confirm the reported P_success values
  to sub-percent.
- Doesn't change any qualitative conclusion.

### 6. Only u=0 tested

- The (H_0, H_u) pair is unitarily equivalent for any u under a
  bitwise-XOR permutation, so the exact spectrum and dynamics are
  u-independent. But the choice u=0 does make H_u trivially sparse.
  Random-u sensitivity was not run.
- Flagged as Q4 in `open_questions.json`.

## Friction encountered during the turn

| Friction | Impact | Resolution |
|----------|--------|------------|
| Stray backgrounded `find` in exec sandbox (session amber-haven) hung on Dropbox traversal. | Wasted ~30 s. | Killed process, rescoped the search to `-maxdepth 3` and target subtrees. |
| Central corpus for QC-200 has no Marker/Nougat outputs for this arXiv ID. | Would have blocked artifacts 2+3. | Documented + surrogated (matches sibling dir convention). |
| No `qiskit` on cherryrd. | Would block a Qiskit-flavoured presentation. | Not actually needed — the "Qiskit statevector" and "numpy statevector" mode of Qiskit compute the same thing; we used numpy directly. `qiskit.quantum_info.Statevector` is a thin wrapper over numpy arrays. |
| Argo endpoint available but unused. | None — task is 100% numerical. | Correctly skipped; brief allows LLM inference but doesn't require it for a math replication. |

## Residual honest gaps

1. **Marker/Nougat are surrogate**, not from the real parsers.
2. **Sections 4 and 6 of the paper** (classical 3CNF reconstruction
   and narrow-basin exponential gap) were not implemented. Only
   Section 5 (the adiabatic Grover analysis) was numerically
   reproduced. The verdict "REPLICATED" refers to Section 5's
   directly-testable numerical claims; a more comprehensive
   "REPLICATED (full)" verdict would require the Section 4/6
   experiments.
3. **c\* prefactor** in the constant-schedule scaling not bisected;
   coarse grid only.
4. **Integrator convergence** not swept; single n_steps=800 run.
5. **u-sensitivity** not exercised.

All five gaps are enumerated in `open_questions.json` (Q1-Q5) as
concrete next-experiment proposals; the verdict text in REPORT.tex
distinguishes tested vs.\ untested claims explicitly.
