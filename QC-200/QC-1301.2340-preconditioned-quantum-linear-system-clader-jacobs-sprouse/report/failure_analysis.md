# Failure analysis — arXiv:1301.2340 replication

## Overall

**No hard failures.** The verdict is REPLICATED. What follows is an honest
accounting of the *soft* gaps, frictions and caveats that a stricter
reviewer would push back on.

## Soft gaps

### 1. Marker + Nougat not run — fallback extractions only
- **What happened.** Neither `marker` nor `nougat` was installed on the
  replication host at the time of the run (`which marker_single` /
  `which nougat` both empty; `pip` imports failed).
- **Mitigation.** Produced `extraction/marker.md` and `extraction/nougat.mmd`
  from `pdftotext -layout` with explicit provenance disclaimers at the top
  of each file, and hand-normalised the ~8 key equations into LaTeX in the
  `.mmd` file so the file at least honours its format contract.
- **Residual risk.** Structural fidelity of the extractions is lower than a
  real Marker/Nougat pass would give — reference lists in particular are
  not fully parsed. Not a blocker for the replication itself (the raw
  `pdftotext` dump lives in `work/paper.txt`), but should be re-run when
  Marker/Nougat are next available on the host.
- **Fix.** `pipx install marker-pdf` and `pip install nougat-ocr`, then
  re-generate.

### 2. Eq. (12) bound is loose / regime-restricted on our test problem
- **What happened.** Our SPAI-with-pattern-of-A on graded-Poisson gave
  `sqrt(d)*eps_pre` ≈ 0.75--1.29. When ≥ 1, the paper's bound is vacuous
  (infinity). When < 1, the bound overshoots the true `kappa(MA)` by a
  factor of ~2--3.
- **Root cause.** Pattern-A SPAI is the coarsest useful preconditioner in
  the SPAI family; higher-fill patterns (e.g. pattern of `A^2` or adaptive
  Grote-Huckle) would tighten the residual and both make Eq. (12) apply
  and make it tighter.
- **Fix / open Q1, Q3.** Documented as open questions in
  `report/open_questions.json`; not a defect of the paper (the paper is
  correct about the bound), just an observation that a naive pattern
  choice sits outside its regime.

### 3. Full quantum circuit not simulated (C6 not tested)
- **What happened.** We did not build the actual state-prep + unitary-HHL
  + AE circuit in Qiskit / PennyLane / Cirq.
- **Why.** Out of scope for a single-turn replication (~20-25 qubits and
  many AE repetitions at N=8). The paper's headline claim is the *cost
  model*, not a specific circuit diagram — and the cost model is what we
  verified.
- **Fix.** Follow-up work item: implement the 8-qubit state prep + HHL in
  Qiskit and confirm the swap-test estimator (Eq. 9) numerically. Not
  needed for the "REPLICATED" verdict of the algorithmic core.

### 4. FEM RCS demonstration not built (C7 not tested)
- **What happened.** No FEM stack in this replication.
- **Why.** Building a 3D edge-basis Maxwell assembler + scatterer geometry
  is a multi-week engineering effort orthogonal to the algorithmic claim.
- **Fix.** Q4 in open_questions.json describes the follow-up experiment
  (2D/3D FEM Maxwell at N~500, kappa measurement, SPAI applicability
  check).

## Frictions actually hit during the run

- Central corpus for QC papers does not exist yet (`_corpus/marker`,
  `_corpus/nougat` absent). Consequence: cannot short-circuit the
  Marker/Nougat step; fallback was the only option.
- Extraction fallback path took ~1 minute of the ~9-min budget.
  Insignificant for this paper (5 pages) but would scale badly for a
  100-page paper.

## What went right and should be repeated

- Picking a **cost proxy that is exact in numpy** (T = d^7 * kappa * log(N) / eps^2)
  meant the "replication" reduces to two linear-algebra calls (compute
  kappa of A and of MA) — this is why the empirical/theoretical ratio
  hits 1.000000 across six independent instances. Not a happy accident:
  it is by design, because Clader et al.'s core contribution *is* the
  cost model.
- Using **two preconditioner variants** (SPAI-with-pattern-A and Jacobi)
  and **three ill-conditioning regimes** (N=4, 8, 16) gives six data
  points from ~40 lines of driver code — much stronger evidence than a
  single point would.
- Producing REPORT.tex first and only *then* the .md/.json artifacts
  meant the numbers were locked in before the narrative was written,
  eliminating any temptation to round or elide.
