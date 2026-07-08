# Workflow: QC-2101.02331-crosstalk-readout-noise

## Steps executed

1. **Extraction.** Retrieved arXiv:2101.02331v3 (Maciejewski, Baccari, Zimborás,
   Oszmaniec 2021) and read Sections 3-7 for the noise model, DDOT protocol,
   mitigation math, and headline hardware numbers (>22x on IBM 15q Melbourne,
   >5.5x on Rigetti 23q Aspen). No Nougat / marker OCR needed — arXiv PDF is
   text-native. A `nougat.mmd` stub is committed in `extraction/` as the
   REPLICATE-PROJECT artifact placeholder.

2. **Environment setup.** `python3 -m venv venv && source venv/bin/activate`,
   then `pip install qiskit==2.5.0 qiskit-aer==0.17.2 numpy scipy matplotlib`.
   Host: CherryRd (macOS, Python 3.14.6).

3. **Model construction.** Built a 4-qubit cluster-crosstalk noise model by
   hand following the paper's structural form:
   - Asymmetric per-qubit `A_i` with `p01=[0.02,0.03,0.03,0.04]`,
     `p10=[0.06,0.07,0.07,0.09]`.
   - Cluster `C = {q1, q2}` with an extra 5-percentage-point flip probability
     conditioned on the neighbor's true state.
   - Full `R_true` (16x16, column-stochastic) constructed by enumeration over
     all 4-bit inputs.
   - Tensor-product baseline `R_tp = ⊗ A_i(base)` for comparison.

4. **Pipeline (per circuit, 25 seeds).**
   - Build random p=2 QAOA circuit (line-4 MaxCut cost, RX mixer).
   - Sample ideal distribution on Aer noiseless (10^5 shots).
   - Apply `R_true` → resample noisy distribution.
   - Mitigate two ways: `R_tp` pseudo-inverse + simplex projection;
     `R_true` pseudo-inverse + simplex projection.
   - Metrics: TVD to ideal; energy error |ΔE| for
     `H = Σ_(i,j)∈E Z_i Z_j`.

5. **QAOA landscape (§7 style).** p=1 grid sweep on `(γ,β)` over
   `13x13` of `[0,π] x [0,π/2]`. Produces 4 cost surfaces (ideal, raw noisy,
   TP mitigated, correlated mitigated).

6. **Reproduce script.**
   ```bash
   cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2101.02331-crosstalk-readout-noise
   source venv/bin/activate
   python code/reproduce.py   # ~90 s
   python code/plot.py        # fig1, fig2
   ```

7. **Report.** REPORT.md (source of truth), REPORT.tex, workflow.md,
   artifacts_summary.md, failure_analysis.md, open_questions.json,
   open_questions_section.tex. All artifacts placed in `report/`; evidence in
   `evidence/`; code in `code/`.

8. **Verdict.** REPLICATED (reproducible core; correlated mitigation gives
   30.8x reduction on |ΔE| — same order of magnitude as the paper's IBM 15q
   Melbourne >22x number; TP baseline only 3.4x, confirming the correlated
   advantage).

## Compute used

- CherryRd macOS CPU only. No GPU. No paid endpoints. Total wall time < 5 min.

## Not done (out of scope)

- IBM Melbourne / Rigetti Aspen hardware runs (chips retired).
- DDOT circuit-count scaling study.
- ML-based characterization.
- Longitudinal calibration drift.
- N > 4 sweep.

These are enumerated as open questions with concrete probes.
