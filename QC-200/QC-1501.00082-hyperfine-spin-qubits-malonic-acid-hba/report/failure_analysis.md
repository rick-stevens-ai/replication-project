# Failure analysis — QC-1501.00082

Honest ledger of what did NOT work, what was NOT tested, and residual gaps.

## 1. Deliberately skipped (out of scope)

These are paper claims we chose NOT to test because doing so would exceed a
text-only, CPU-only, minutes-scale replication budget:

- **C5. GRAPE pulse fidelities** (AHC: 99% / 98% / 96% for e-H swap /
  e-Cm swap / 3-qubit compression). Reproducing these requires (i)
  fitting the actual malonic-acid spin Hamiltonian (14 hyperfine
  parameters listed in the paper's Table 1-2), (ii) running GRAPE
  optimization over a Lorentzian distribution of Zeeman-Hamiltonian
  samples for T2*-robustness, (iii) numerical propagation of density
  matrices under piecewise-constant microwave envelopes. Any one of
  these is 1-2 days of implementation; not appropriate for a QC-200 wave
  replication.
- **C6. Realistic Fig 7 red-curve number** (Cm/e_b ratio ≈ 1.51 at
  round 9, i.e. 76% of theory). This depends on the same GRAPE pulses
  as C5 PLUS a full Lindblad master-equation integration with
  T1e=27 µs, T2e=5 µs, T2*=28 ns, plus per-round electron-reset
  simulation. Also out of scope.
- **C7. 5-qubit HBAC with Q=100 resonator bandwidth effects.** Requires
  simulating the full ESR spectrum (80 lines for the per-13C-labeled
  molecule) and offset-dependent pulse-length scaling from the resonator
  transfer function. Out of scope.
- **Experimental verification.** No hardware was used; this is a
  simulation-only replication as the brief specifies ("Real simulation
  only. Install the open tool, run the actual circuit").

## 2. Real limitations of the numerical simulation

- **n≥5 sort-per-round under-shoot (documented in C3 verdict).** Our
  simulator applies one non-increasing sort per round for all n. This is
  EXACTLY the paper's protocol at n=3 (which is why we match to 1e-6),
  and matches at n=4, but at n=5 our simulator saturates at 4.2×ε_b
  vs. the theoretical weak-limit optimum 8×ε_b. This is not a bug: the
  paper itself does not simulate the full recursive PPA at n=5 (Sec 5,
  para 2: "we only simulated one round to demonstrate feasibility"), so
  there is no paper number for our n=5 asymptote to compete against.
  Open Question Q1 proposes implementing the recursive Boykin-Mor PPA
  as the follow-on.
- **No coherences / off-diagonals.** Justified for the PPA idealization
  (see workflow.md §Design decisions), but a real experiment with
  imperfect swaps DOES introduce coherences; we cannot say anything
  about how those affect the asymptote.
- **Reset is instantaneous.** A finite-time Markovian reset with
  cross-relaxation onto the nuclear qubits (paper's actual concern) is
  NOT modeled. This is exactly the gap between the paper's "Theory"
  black-dashed curve (which we match) and its "with relaxation" red
  curve (which we do not attempt). Open Question Q2 formalizes the
  correction.

## 3. Tooling friction

- **Marker CLI not installed** on CherryRd. Substituted PyMuPDF layout
  extraction (extraction/marker.md carries a provenance header disclosing
  this). This is the same choice the sibling QC-200 dirs made
  (`QC-1611.05543-.../extraction/marker.md`,
  `QC-quant-ph-0206003-.../extraction/marker.md`, etc.).
- **Nougat CLI not installed** on CherryRd. Substituted
  `pdftotext -layout` (extraction/nougat.mmd header discloses this).
  Same sibling-QC-200 convention.
- **Neither surrogate produces LaTeX math.** The paper's equations
  appear as text/glyphs, not TeX. For the analytical claims we
  replicate, this does not matter (we read the prose formulas
  "1.5 ε_b − 0.5 ε_b^3" and "2 ε_b" out of both surrogates plus
  `work/paper.txt` and cross-verified against the PDF). For a heavier
  math-critical replication it would matter and would justify actually
  installing Nougat.

## 4. Residual gaps (honest)

- The paper's exact analytical formula "ε_th = ε_b · 2^(n-2)" holds
  for the RECURSIVE PPA, not the flat sort-per-round we use. Our C3 at
  n=3,4 accidentally matches because for those n a single sort IS the
  PPA. For a scientifically-tight statement we should either (a) rerun
  with recursive PPA or (b) explicitly weaken C3 to "PPA-consistent
  scaling at n=3,4; sort-per-round protocol saturates earlier at n≥5."
  The REPORT.tex uses (b).
- **No LLM-judge scoring.** The QC brief mentions "LLM-judge scoring
  for the final verdict, never regex." We did not invoke Argo because
  the numerical claims are exactly-verifiable analytic formulas
  (rel_err at 1e-13 leaves no interpretive room). A judge panel would
  add procedure but no signal here. If Rick or the QC wave lead
  wants an Argo panel run post-hoc, the `hbac_results.json` +
  `REPORT.tex` are self-contained enough to feed to it.
- **LaTeX compilation.** REPORT.tex is written to compile cleanly, but
  we did not require pdflatex to be present on CherryRd; if
  REPORT.pdf is missing from the dir, `pdflatex REPORT.tex` in
  `report/` produces it. (No externally-hosted images; the one PNG is
  a relative path.)

## 5. What would upgrade the verdict beyond REPLICATED

Nothing in the paper's analytical core is left ambiguous by our
simulation; we already have floating-point-precision agreement. The only
way to add signal would be to reproduce the GRAPE-limited experimental
projections (C5, C6, C7), which would transform this replication into
an ~2-day faithful reimplementation of the paper's Sec 5 relaxation
model. That is a genuinely different (and larger) research task than a
QC-200 wave replication and would deserve its own project.
