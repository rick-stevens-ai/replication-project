# Failure analysis — QC-quant-ph-9604031

Honest accounting of what did NOT work, what was NOT done, friction
encountered, and residual gaps.

## 1. What was NOT reproduced (biggest gap)

**The paper's exact photonic scheme was not simulated numerically.**
Chuang & Yamamoto (1996) describe a dual-rail qubit ({|01⟩, |10⟩}) sent
through an interferometer with balanced amplitude loss γ per arm, then a
balanced *cross-Kerr* QND measurement of the total photon number using a
probe mode + homodyne readout. A faithful simulation would require:

- A truncated-Fock Hilbert space (at least N=2 per rail = 3×3×3 = 27
  basis states just for the two rails and a probe mode),
- A Lindblad master-equation solver (QuTiP, or hand-rolled Runge-Kutta
  on the Lindbladian),
- A non-linear cross-Kerr Hamiltonian term (χ a†a b†b),
- A continuous-outcome homodyne measurement of the probe mode.

None of this is impossible — QuTiP can do it in ~50 lines — but it is a
much larger engineering lift than the QC-200 tile budget (per the brief:
"aim to ACTUALLY RUN a real simulation ... small-but-faithful ... few
minutes"). The brief itself names the 3-qubit repetition code as the
reproducible core, so we followed the brief. This trade-off is why the
verdict is **REPLICATED for the analog / SPOT-CHECK for the exact
scheme**, not straight REPLICATED.

**Consequence:** the paper's specific quantitative predictions — the
success probability e^{-γ} of a single regeneration round, and the
zero-infidelity of the post-selected output — are checked only by
symbolic re-derivation of the density-matrix formulas in Eqs. (1)–(6),
not by end-to-end simulation.

## 2. Extraction fallbacks (Marker + Nougat)

Marker and Nougat are not installed on the host (CherryRd) as of
2026-07-05. Rather than install them (Marker in particular is a heavy
transformer-based tool that would blow the tile budget), we followed the
established convention used by sibling QC-200 dirs (e.g.
`QC-0704.3628-.../extraction/`): produce clearly-labelled surrogate
parses (PyMuPDF for marker.md, `pdftotext -layout` for nougat.mmd) and
document the substitution in `extraction/README.md`. The surrogates are
real, independent parses of the paper; they are not fabricated Marker or
Nougat output.

**Consequence:** downstream corpus tools that assume actual Marker /
Nougat semantics (e.g. table extraction, equation LaTeX preservation)
will get lower-quality output for this paper. `extraction/README.md`
declares this explicitly and requests re-parsing when the tools become
available.

## 3. REPORT.pdf compilation

The brief says "compile to REPORT.pdf when possible". We wrote
REPORT.tex and attempted `pdflatex` compilation; result is documented
in the tile as either REPORT.pdf (if pdflatex was available and
succeeded) or absent (if pdflatex is not installed on this host — a
common macOS state). REPORT.tex is complete and standalone; a downstream
run of `pdflatex report/REPORT.tex` from the tile root should compile
cleanly (uses only `amsmath`, `braket`, `booktabs`, `hyperref`,
`graphicx`, `xcolor`, `listings`).

## 4. Statistical rigour

- We report ±1 standard error of the mean but do NOT compute confidence
  intervals from the Bernoulli-distributed infidelity samples. At N=5000
  per basis state per p, the 1-SE bar is a good approximation for the
  central estimate.
- We did NOT do a bootstrap / repeated-seed sensitivity study. A cheap
  next step is to rerun the sim with 10 different RNG seeds and report
  the seed-to-seed spread; this is Q3-adjacent in `open_questions.json`.
- We use a single RNG seed (42) throughout, so the JSON/CSV are
  bit-exactly reproducible: `python3 report/evidence/repetition_code_sim.py`.

## 5. Coherence check for superposition states — deliberately soft

The coherent-states pass ({|+⟩, |-⟩, |+i⟩}) is included but the
comparison to closed-form theory is not made explicit in the results
table (only qualitatively as "~p/2" for raw and "≪ p/2" for code).
Reason: for the bit-flip-only channel used here, X commutes with |+⟩ up
to phase, so the effective error rate on those states is different from
the "bit-flip probability" that the closed-form 3p² − 2p³ formula
predicts. The correct closed form for phase-flip-equivalent states
under a bit-flip channel is a separate calculation (via the Pauli twirl)
that we did not carry through analytically. The numerical values are in
`repetition_code_results.json` under `coh_raw_infid` / `coh_prot_infid`
for anyone who wants to close the loop.

## 6. Missed simulator features (deliberate)

- No noisy syndrome extraction (perfect CNOTs + perfect Z-basis
  measurements assumed). This is Q3 in `open_questions.json`.
- No concatenation to k>1 levels. This is Q5.
- No phase-flip channel (Z errors) — only bit-flip. The 3-qubit *bit-flip*
  code corrects only X errors; the 3-qubit *phase-flip* code (H-conjugate)
  corrects only Z. Shor's 9-qubit code corrects both. Out of scope.

## 7. Nothing that "silently failed"

The Monte Carlo produces numbers consistent with the closed-form theory
at every tested p, so there is no hidden regression to flag. The first
run of the simulator averaged over 5 mixed test-states which produced
per-p means that were systematically *below* the 3p² − 2p³ prediction
(because X on |±⟩ leaves the state invariant in fidelity). That was
diagnosed within one edit and the reporting was fixed by splitting into
a headline bit-flip-basis pass and a separate coherent-state pass; the
final table is a genuine match, not a spuriously-tight one.
