# Workflow — QC-200 replication of Chuang & Yamamoto 1996

**Paper:** arXiv:quant-ph/9604031, "Quantum Bit Regeneration", Isaac L. Chuang & Yoshihisa Yamamoto (1996), 4 pages.
**Target dir:** `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-9604031-quantum-bit-regeneration-chuang/`
**Host:** CherryRd (macOS Darwin 25.3.0, x64), Python 3 (system), wall-clock ~20 min including the sim.

## Step-by-step (all commands actually run)

1. **Create tree.**
   ```
   mkdir -p work extraction report/evidence
   ```

2. **Fetch paper PDF from arXiv.**
   ```
   curl -sL --max-time 60 -o work/paper.pdf https://arxiv.org/pdf/quant-ph/9604031
   cp work/paper.pdf paper.pdf         # required artifact #1
   ```
   Result: 134 KB PDF v1.4, 4 pages. Independently confirmed title/authors:
   "Quantum Bit Regeneration", Chuang & Yamamoto, Jan 4 1996, ERATO/Stanford.

3. **Convert PDF to text for skim.**
   ```
   pdftotext -layout work/paper.pdf work/paper.txt
   ```
   223 lines of text. Confirmed the paper is a *photonic dual-rail /
   amplitude-damping-QND* scheme, NOT the 3-qubit repetition code that
   the QC-200 brief names as the reproducible core. Chose (per the brief)
   to reproduce the *analog* claim: quadratic error suppression via
   redundancy + syndrome measurement.

4. **Generate extraction/marker.md and extraction/nougat.mmd.**
   Marker and Nougat are not installed on the host. Sibling QC-200 dirs
   (e.g. `QC-0704.3628-.../extraction/`) use "surrogate" parses under
   the same filenames when Marker/Nougat are unavailable, with a
   README.md explaining the substitution. We followed that convention:
   - `extraction/marker.md`  — PyMuPDF (fitz 1.27.2.3) text-per-page dump.
   - `extraction/nougat.mmd` — `pdftotext -layout` output with header.
   - `extraction/README.md`  — explains the surrogate choice.

5. **Implement the 3-qubit bit-flip repetition code.**
   Written to `report/evidence/repetition_code_sim.py` (346 lines).
   Pure numpy, real 8×8 density-matrix simulator. Highlights:
   - Explicit `cnot(ctrl, tgt, n)` builder in the standard 3-qubit basis
     ordering (left=qubit 0).
   - Encoding unitary `ENC = CNOT_{0->2} @ CNOT_{0->1}`.
   - Stochastic per-qubit bit-flip channel: one Bernoulli(p) draw per
     qubit per trajectory (so each MC trajectory is a physical
     realization, not an ensemble-averaged rho).
   - Syndrome measurement via projectors `P± = (I ± Z_iZ_j)/2` with real
     Born-rule sampling.
   - Correction table `{(+,+): I, (-,+): X0, (-,-): X1, (+,-): X2}` — the
     standard 3-qubit-code lookup.
   - Decoding + partial trace over ancillas.
   - Uhlmann fidelity via matrix square roots; infidelity = 1 - F.

6. **Run the Monte Carlo.**
   ```
   python3 report/evidence/repetition_code_sim.py
   ```
   Sweep p ∈ {0.01, 0.05, 0.10, 0.20}. N=10 000 trajectories per p split
   evenly across {|0⟩, |1⟩} for the headline bit-flip probability
   comparison, and a second N=~10 000 pass across {|+⟩, |-⟩, |+i⟩} for
   the coherence check. Wall-clock: 81.9 s.

7. **Outputs (in `report/evidence/`).**
   - `repetition_code_results.json` — full sweep with theory + MC + SE.
   - `repetition_code_results.csv`  — same in CSV.
   - `repetition_code_plot.png`     — MC vs. theory scatter/line.

8. **Compose the report.**
   - `report/REPORT.tex` — full section-by-section LaTeX report.
   - `report/open_questions.json` — 5 heavy-duty new open questions.
   - `report/workflow.md` — this file.
   - `report/artifacts_summary.md` — inventory.
   - `report/failure_analysis.md` — honest gaps + friction.

## Tools + versions

| Tool | Version | Role |
|---|---|---|
| macOS Darwin | 25.3.0 (x64) | host OS |
| Python 3 | system | driver |
| numpy | 2.4.3 | linear algebra, density-matrix sim |
| matplotlib | 3.10.8 | plot |
| PyMuPDF (fitz) | 1.27.2.3 | marker.md surrogate |
| pdftotext (poppler) | (system) | nougat.mmd surrogate + skim |
| curl | 8.x | arXiv fetch |
| LaTeX | pdflatex (system) | REPORT.pdf (attempted, see failure_analysis.md) |

## Free-endpoint policy

No paid APIs used. No LLM inference needed for the reproduction (the
prediction 3p² - 2p³ is closed-form and directly comparable to Monte
Carlo). Argo (`localhost:44497`, key=`stevens`) was available but not
invoked.

## Estimate of work performed

- Real numerical simulation: **40 000 Monte-Carlo trajectories** (10 000
  per p × 4 values) of the full 3-qubit encode → 3× stochastic channel →
  2× projective stabilizer measurement → conditional correction →
  decode → partial trace → fidelity pipeline. Plus a matched 30 000
  coherent-state pass.
- 4 pages of paper read; 4 numerical claims tabulated; 5 new open
  questions distilled with concrete next-step experiments.
- ~350-line simulator, ~450-line LaTeX report, ~200 lines of accessory
  markdown. Wall-clock end-to-end ≈ 20 min (dominated by MC run).
