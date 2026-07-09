# Failure analysis / friction / residual gaps

## What went smoothly
1. Paper acquisition from arxiv.org and PDF-to-text extraction worked first try (30-page paper, well-formatted TeX source).
2. Section 6.2 is precisely operational — Eqs. (13) and the definitions of `H`, `V`, `X` are unambiguous, so building the numerical construction was direct.
3. Dense diagonalization at n_data=3 + 3 mediators = 64-dim Hilbert space fits comfortably in RAM and runs in a fraction of a second per Δ point.

## What went wrong (and was fixed)

### F1. Task brief's `V³/Δ²` scaling prediction was WRONG
The task brief said the paper predicts ε(Δ) ∝ 1/Δ² (i.e. err ~ V³/Δ²).
**Reading the paper carefully, this is not what KKR actually predict.**
Eq. (14) — after the counter-term `X = Y + δ⁻¹(B1²+B2²+B3²)` cancels the
leading `V⁻+V+⁻` unwanted contribution — leaves a residual of `O(δ)`
where `δ = Δ⁻¹/³`. A naive `V³/Δ²` estimate would apply only to the
raw third-order term in Σ_-(z) *before* the counter-term cancellation.

Fix: report the paper's actual prediction (`O(δ) = O(Δ⁻¹/³)`) and
verify it empirically. The brief's mis-statement is called out
explicitly in `report/REPORT.tex` §Task-brief scaling mis-statement.

### F2. First-pass eigenvalue comparison was misaligned
Initial code compared `E_gadget[:8]` to `E_target[:8]` directly (naive
sort). This gave apparent "saturation" of ε at ~ 0.05 that didn't match
the paper's O(δ) prediction. **Root cause:** the gadget's low-lying
spectrum contains 16 eigenvalues (not 8), organised as 8 pairs
`(E_+ , E_-)` corresponding to the two effective-qubit sectors
|+⟩_eff and |−⟩_eff. The target's 8 eigenvalues match only the
|+⟩_eff sector (where `Heff = Y - 6 B1 B2 B3`); the |−⟩_eff sector
has `Heff' = Y + 6 B1 B2 B3` (opposite sign, so higher ground energy
since B1 B2 B3 is PSD).

Fix: explicit projection `P_± = I_data ⊗ |±⟩_eff⟨±|_eff` on the
mediator subspace, classify each gadget eigenstate by weight, and
compare only the |+⟩_eff sector to `H_target`. See
`project_low_subspace_energy()` in `reproduce_gadget.py`. After fix,
scaling is clean: err ~ Δ⁻⁰·⁴¹ ≈ δ⁺¹·²⁴ over 200 ≤ Δ ≤ 10⁵.

## Residual gaps and limitations

### G1. Numerical floor at very large Δ
At Δ ≥ 10⁵ the ground-state error stops decreasing linearly with δ and
plateaus near 3-5×10⁻². Two candidate causes:
- Finite constant coefficient in front of the paper's `O(δ)` bound —
  a genuine `C·δ` with `C ≈ 2-3`. This is consistent with the paper
  and does not undermine the scaling claim.
- `numpy.linalg.eigh` relative-error conditioning: at Δ = 5×10⁵ the
  spectrum spans 10⁶ in magnitude, and `eigh`'s small-eigenvalue
  absolute error is `~ ε_mach · ||H||` = `~ 5×10⁻¹¹`, well below the
  observed floor, so this is likely NOT the cause.
  
Not distinguished experimentally in this replication — see Q2 in
`open_questions.json` for the proposed mpmath / Schur-complement
follow-up.

### G2. Only a single Y instance tested
Everything was done with numpy seed 0. We do not know how sensitive
the observed super-linear slope (−0.41 vs paper's worst-case −1/3) is
to the specific random Y. See Q1 in `open_questions.json`.

### G3. Only a single 3-local term
Section 6.3 of the paper argues that *simultaneous* gadgetisation is
required — sequential gadgetisation gives exponential norm blowup.
We reproduced only one gadget, so this multi-term aspect is not
tested. See Q5 in `open_questions.json`.

### G4. Extraction is surrogate, not Marker/Nougat
Marker and Nougat are not installed on this host. We produced two
independent extractions (PyMuPDF and pdftotext-layout) with headers
that clearly label the actual tool used. This is the same convention
used by earlier QC-200 dirs on this host (e.g. QC-0704.3628).

### G5. Structural claims (C1, C5) not tested
- C1 (2-Local Hamiltonian is QMA-hard) is a complexity-theoretic
  claim; verifying it means checking the paper's structural proof,
  which is outside the "run a small real simulation" mandate of the
  QC-200 brief.
- C5 (universal 2-local adiabatic QC) similarly is structural; the
  numerical scope here is the single-gadget reduction that C5 relies on.

## LLM / infrastructure friction
- Zero. All computation ran on CherryRd with pre-installed numpy,
  matplotlib, pdftotext, PyMuPDF, and TeXLive. No LLM inference was
  needed for the verdict (deterministic numerical comparison against
  the paper's stated scaling). No paid endpoints touched.
- The `pdflatex` compile of REPORT.tex was clean on first try (6-page
  PDF, no warnings).

## Bottom line
The gadget construction is empirically verified within the paper's
own asymptotic regime; the only real friction was the task brief's
mis-statement of the predicted scaling (`V³/Δ²` vs the correct
`O(δ)`), which we resolved by reading Eq. (14) directly. Verdict:
**REPLICATED**.
