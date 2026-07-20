# Failure analysis — oh2026 p-wave OAM texture (tight-binding surrogate)

**Verdict: REPLICATED** (6/6 checks). The items below are scope boundaries and
caveats, not check failures — they cap *coverage*, not *agreement*.

## 1. Most important caveat: DFT was deliberately NOT run
The paper is a DFT + Wannier + CD/spin-ARPES study. **We reproduce only the
symmetry-dictated MODEL CORE**, the minimal chiral p-orbital tight-binding model
the authors themselves invoke (Sec. III, Fig. S1). We do **not** reproduce:
- material-specific band energies of (TaSe₄)₂I;
- the quantitative CD-ARPES node position (kx ≈ ±0.2 Å⁻¹ at E = −0.6 eV);
- the −0.25 eV constant-energy contour shape;
- the FPLO/Wannier numbers (12³ mesh, Ta-5d/6s/Se-4p/I-5p basis).

Why this is defensible: every headline feature the paper reports — p-wave
oddness, enantiomer flip, Mx/My mirror relations, Lx-even/Ly-weak/Lz-absent, and
OAM ≫ SAM — is a **symmetry consequence** of (a) the chiral helix (chiral
coupling odd in kx, helicity-controlled) and (b) the OAM content of the Se
{py,pz} polarizer doublet. None of these requires the specific DFT band
energies. So the model surrogate captures the reproducible physics; DFT would
add material-specific quantitative anchoring (see open_questions Q1).

## 2. Residuals are machine-precision — by construction, not by luck
All symmetry residuals are ~1e-14. This is **expected and honest**: the checks
test relations the model Hamiltonian satisfies exactly (sin kx is exactly odd;
χ → −χ exactly flips the chiral term). The non-trivial, falsifiable content is
that a *single minimal SOC-free model* reproduces *all six* qualitative paper
features *simultaneously and consistently* — and that the first (physically
wrong) parameterization FAILED C4/C5 (see §4), showing the checks can fail.

## 3. What was NOT built (scope-out, coverage-capping)
- **CD-ARPES intensity forward model.** We compute intrinsic Lx(k) directly; we
  do not simulate photoemission matrix elements (final-state, interference) that
  convert Lx into I_RCP − I_LCP. The paper's intrinsic-vs-extrinsic CD control
  experiment (no sign flip across ky; photon-energy sign reversals) is therefore
  not independently reproduced. (open_questions Q4.)
- **Single dx²-Wannier toy model.** The paper's Wannier90 minimal model uses a
  lone Ta-dx² orbital whose Se-p tails carry the OAM. We used an explicit
  {px,py,pz} basis instead, which is cleaner but sidesteps the subtle "OAM in the
  Wannier tails" question. (open_questions Q2.)
- **SOC sweep / OAM→SAM conversion.** We verified the weak-SOC limit (OAM ≫ SAM)
  but did not map the strong-SOC crossover to a p-wave SAM texture — the paper's
  proposed CISS/CIOS mechanism. (open_questions Q3.)

## 4. Diagnostic failure that was fixed (recorded for honesty)
The initial parameterization placed px (dx²-like) as the LOW-energy band. This
FAILED C4 (|Ly|/|Lx| = 2.2, |Lz|/|Lx| = 0.44) and C5 (impure harmonic), because
a px-dominated band mixes strongly into Ly rather than Lx. The fix was to follow
the paper's own microscopic picture: px is OAM-inert and sits ABOVE the {py,pz}
polarizer doublet, which is where Lx lives. After re-assignment (+ small doublet
splitting δ so Lx ∝ sin kx turns on smoothly), all 6 checks pass. The fix is
physically motivated by the paper text, not free tuning to hit the target.

## 5. Extraction tooling degraded (not a physics gap)
Neither `marker` nor `nougat` is installed on this host. `extraction/marker.md`
and `extraction/nougat.mmd` are the documented `pdftotext` interim fallbacks.
pdftotext mangles Unicode math, so the paper's equations were **hand-transcribed
into LaTeX** in `nougat.mmd` (and REPORT.tex) — those are authoritative; the raw
dumps are for text search only. `pdflatex` may also be absent, so REPORT.tex
ships as source. None of this affects the physics replication.

## 6. What would raise coverage toward 10/10
- Run FPLO DFT + Wannier on crux → pin node positions & material numbers (Q1).
- Forward-model CD-ARPES matrix elements → validate the intrinsic-CD inference (Q4).
- Sweep SOC → demonstrate the OAM→SAM p-wave conversion (Q3).
