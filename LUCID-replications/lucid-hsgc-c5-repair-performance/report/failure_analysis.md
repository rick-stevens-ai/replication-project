# Failure Analysis — Sakata et al. 2021 (HSGc-C5 TLK repair-performance)

## Verdict: PARTIAL (preserved)

The queue verdict PARTIAL is preserved. Substance justifies it:

- The TLK ODE curve-fit half of the paper is fully replicated.
- The Geant4-DNA Monte Carlo half is **not re-executed** — a genuine gap.
- The paper's Appendix A NB1RGB Table A1 is **not reproducible** from the paper's
  own supplement — a genuine reproducibility red flag (paper-side).
- One arithmetic self-inconsistency in the paper (43% vs true 40.5%) — minor.

No upgrade to REPLICATED is warranted. Rick's 2026-07-05 rule: preserve queue
verdict unless report substantiates upgrade. It does not.

## What the paper's headline actually claims

Sakata et al. present a **Monte-Carlo-plus-TLK repair-performance benchmark**:

1. Simulate initial DNA damage from 70 MeV protons using Geant4-DNA
   (~56,400 + 11,400 events, fractal chromatin nucleus geometry, Nikjoo 10-bp
   DSB clustering).
2. Feed simulated DSB yields (Σ₁ simple, Σ₂ complex) into a TLK two-lesion
   kinetics ODE model.
3. Fit TLK repair parameters (λ₁, λ₂, η, β₂, γ) to measured HSGc-C5 SF and FAR
   using Ceres-Solver nonlinear least squares.
4. Report SF R², FAR R², half-lives, and lethality percentages as the
   "repair-performance" metric.
5. Repeat for NB1RGB human fibroblasts in Appendix A.

The headline **repair-performance metric** is therefore the joint fit quality
(SF R² and FAR R²) achieved when the Geant4-DNA-simulated DSB yields are fed
into the TLK model with cell-line-specific repair constants.

## What was done vs the headline

### Done (headline components successfully exercised)
- ✅ Ingestion of paper's open MDPI supplement (SF, FAR, DepthDose CSVs).
- ✅ TLK ODE reimplementation (Eqs 3-6) with Stewart-2001 exponential form.
- ✅ Random-breakage FAR (Eq 7) reimplementation.
- ✅ Forward run using paper's Table 1 verbatim → SF R²=0.91, FAR R²=0.72.
- ✅ Joint NLS refit (Ceres-Solver analogue) → SF R²=0.96, FAR R²=0.96.
- ✅ Figure 5 qualitative reproduction (SF vs dose, FAR vs time).
- ✅ Half-life arithmetic (M1): 12.378 min fast, 70.015 h slow.
- ✅ Bragg-peak location from supplement (M2): exact match at 33 mm.
- ✅ Lethality-percentage arithmetic (M7, M7b, M11): all within 1 pp of paper.
- ✅ NB1RGB refit (M9): SF R²=0.96, FAR R²=0.96 with *new* parameters.

### NOT done (headline components skipped)
- ❌ **Geant4-DNA Monte Carlo half NOT re-executed.** The paper's entire
  "physics" branch (Sec 2.2.2) — simulating 56,400 + 11,400 proton events through
  a fractal chromatin nucleus geometry with DSB clustering — was skipped. We
  consumed the paper's reported per-Gy/Gbp yields directly. This is the primary
  gap and the primary reason the verdict is PARTIAL.
- ❌ **Ground-truth SF/FAR dataset NOT re-generated.** The paper's clonogenic
  assay and neutral-elution/electrophoresis measurements (Sec 2.2.1) are the
  ground truth against which the pipeline is scored. Not re-run (wet-lab). We
  scored against the paper's own published supplement CSVs.
- ❌ **PMMA I-value tuning NOT re-done.** Paper fitted I-value = 65 eV via
  Geant4 depth-dose matching. We consumed this as given. Would require Geant4
  condensed-history runs at multiple I-values.
- ❌ **Per-cell incident-proton energy spectra (Fig 3) NOT re-derived.**
  Requires Geant4 run.
- ❌ **Reference pipeline (paper's Ceres-Solver optimization) NOT re-run in
  Ceres.** Substituted SciPy TRF with log-SF residuals. Well-known TLK
  parameter degeneracy means this is not equivalent — our converged parameters
  differ from paper by factors 0.3-5.5x even though final R² is better.

## Critique summary

### C1: Half of the paper's headline is unvalidated
The Monte Carlo half is the physical-modeling contribution; without
re-execution, we cannot say whether the paper's Σ₁/Σ₂ yields are correct.
Any downstream TLK fit inherits this uncertainty. Genuine gap.

### C2: The "reference" ground-truth benchmark is not our ground truth
We score against the paper's own published SF/FAR supplement. This means our
"replication" of the fit quality is really a re-fit against the same data the
paper fit against. Genuine third-party validation would require independent
HSGc-C5 measurements — which do not exist in open literature that we found.

### C3: Appendix A NB1RGB Table A1 is non-reproducible
The paper publishes Table A1 as the NB1RGB TLK fit; forward-running Table A1
against the paper's own NB1 SF supplement gives R² = -3.20. Either Table A1 is
mistyped (λ₁ = 33062.9 h⁻¹ is physically implausible → 75 ms half-life) or the
paper's optimization landed on a degenerate local minimum where SF prediction
is decoupled from λ₁. Either way, Appendix A cannot be certified.

### C4: TLK parameter degeneracy
Our refit achieves R² = 0.96 but with parameters differing from paper by
factors of 0.3-5.5x. Only products γη and β₂λ₂ are identifiable from SF+FAR
alone. Our "better" fit is not necessarily correct; the parameter space is
under-determined.

### C5: Paper arithmetic self-inconsistency (minor)
Paper claims 43% complex-DSB increase from 0 mm to 32 mm PMMA. Correct
arithmetic on paper's own numbers: (1.04−0.74)/0.74 = 40.5%. Off by 2.5 pp.
Real but minor.

### C6: No external validation of TLK against orthogonal DSB readouts
We did not cross-validate TLK-predicted L_unrej(t) against γ-H2AX foci counts
or PFGE fragment distributions. Absence leaves TLK vulnerable to being read as
a phenomenological two-exponential curve-fit rather than a mechanistic model.

## Why PARTIAL not REPLICATED

- **Half the paper is out of scope** (Geant4-DNA Monte Carlo).
- **Appendix A does not reproduce** with the paper's own published parameters.
- **Parameter degeneracy** means our better R² does not certify the paper's
  parameter set.
- **No orthogonal validation** and **no re-generation of ground truth**.

PARTIAL is the honest verdict.

## What would flip to REPLICATED

- Re-run Geant4-DNA half with the molecularDNA example, get Σ₁/Σ₂ within
  Poisson stats of paper.
- Reproduce Table A1 verbatim (with a physically-plausible λ₁) via Ceres-Solver
  with the exact paper priors — OR obtain corrected Table A1 from authors.
- Cross-validate TLK-predicted L_unrej(t) against an orthogonal DSB readout
  (γ-H2AX or PFGE) on HSGc-C5 at matched dose and time points.

None of these are free-compute-only; all require either Geant4 CPU-days,
author correspondence, or wet-lab data acquisition. Hence PARTIAL persists.

## What would push to NO-GO

Nothing observed. The TLK core works, the arithmetic is close, the
Appendix A gap is honestly attributable to the paper. Verdict floor is PARTIAL.
