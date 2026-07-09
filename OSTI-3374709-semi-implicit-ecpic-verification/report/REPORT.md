# Independent Replication Report — OSTI 3374709

**Paper:** R. M. Hedlof, D. C. Barnes, R. E. Groenewald, *et al.*,
*"Verification of an energy-conserving semi-implicit electrostatic particle-in-cell
scheme for modeling high-density plasma at scale"*, **Phys. Plasmas 33, 053902 (2026)**.
DOI: 10.1063/5.0315721 · OSTI: 3374709 · LBNL (eScholarship item 8xt682g7) · CC-BY 4.0.

**Set:** OSTI-100 (rank 4, accelerator_plasma) · **Domain:** semi-implicit PIC / plasma
kinetics · **Replicated by:** independent from-scratch 1D ES-PIC re-implementation.

---

## 1. Paper summary

Momentum-conserving explicit electrostatic PIC (ECPIC) must resolve the electron plasma
period (`ωpe·Δt ≲ 2`) for stability, which is prohibitively expensive for high-density
plasmas. The authors present a **semi-implicit** ES-PIC (SIPIC) in which the particle mass
is replaced by an SPD operator that suppresses only the Langmuir (plasma-wave) response.
In the implemented form (their Eqs. 9–10, barycentric shape functions) this is exactly
equivalent to solving Poisson's equation with a **density-dependent effective dielectric**

  `eps_eff = eps0 · (1 + C_SI · ωpe² · Δt² / 4)`

so that the electron plasma mode is **down-shifted** to (their Eq. 16)

  `ωpe_SI = ωpe / √(1 + C_SI · ωpe² · Δt² / 4)`,

making the scheme stable at `Δt` far larger than `1/ωpe` while remaining second-order
accurate for lower-frequency modes and (per §III.B) leaving cyclotron / hybrid physics
essentially unaffected. The `VERIFICATION` section (§III) demonstrates this against
analytic dispersion (§III.A Bohm–Gross), upper/lower hybrid modes (§III.B), Landau
damping (§III.C), and energy conservation, using WarpX and Aleph code-to-code comparison.

---

## 2. Claims table

| ID | Claim | Type | Testable? | Tested here? |
|----|-------|------|-----------|--------------|
| **C1** | SIPIC introduces effective dielectric `eps0·(1+C_SI·ωpe²Δt²/4)` and down-shifts the plasma mode by `1/√(1+C_SI·ωpe²Δt²/4)` (Eqs. 12/16) | analytic + numerical | **Yes** | **YES — core target** |
| C2 | Modified Bohm–Gross `ω²=(ωpe_SI)²+1.5 vth²k²` (Eq. 18) matches simulated dispersion | analytic + numerical | Yes | Partial (cold limit of C1; thermal term small by design) |
| C3 | Scheme is stable for arbitrarily large Δt provided `C_SI ≥ 1` (`ωΔt < 2/√C_SI`, Eq. 14) | analytic/stability | Yes | Yes (implicitly — all runs to `ωpe·Δt=16` stayed bounded) |
| C4 | Upper/lower hybrid frequencies unaffected except via `ωpe_SI` (Eqs. 19-20) | numerical | Yes (needs B-field 2D) | No (out of scope for 1D core) |
| C5 | Total energy change < 2.5% over full run; SIPIC≈ECPIC energy behavior | numerical | Yes | No (Fig. 2, requires full WarpX/Aleph runs) |
| C6 | Landau damping rates preserved (§III.C) | numerical | Yes | No (out of scope) |

**Focus of this replication: C1 (the central verification claim), with C3 as a byproduct.**

---

## 3. Method

**Independent re-implementation** (no paper code; ~180-line NumPy PIC in
`work/sipic_dispersion.py`):

1. **1D electrostatic PIC**, periodic box, normalized units (`ωpe = 1`, `eps0 = 1`,
   `q = -1`, `m = 1`). Leapfrog particle push; Cloud-In-Cell (linear) charge deposition
   and field gather; **spectral (FFT) Poisson solve**.
2. **SIPIC modification** implemented exactly as the paper's field operator (Eqs. 9–10):
   the negative-Laplacian is multiplied by `F = (1 + C_SI·ωpe²·Δt²/4)`, i.e.
   `eps_eff = eps0·F`. (The paper's Eq.12 writes `κ = 1/F`, `eps_SI = eps0·κ`,
   `ω² = ωp²/κ`; that κ-bookkeeping is internally inverted relative to the *stated*
   Eq.16 down-shift, so we implement the physical operator from Eqs. 9-10 directly. The
   resulting down-shift factor `1/√F` is identical to Eq.16.)
3. **Test problem:** cold Langmuir oscillation — uniform plasma with a small mode-1
   position perturbation (`amp = 0.02`); `vth = 0` (cold, so the Bohm–Gross thermal
   term vanishes and C1 is isolated); N = 80,000 particles, 32 cells, long box (small k).
4. **Sweep:** numerical factor `a ∈ {0.5,1,2,4,8}` giving `ωpe·Δt ∈ {1,2,4,8,16}`
   (a 16× range spanning both `Δt` conventions in the paper), with **C_SI = 4** (Table I).
5. **Diagnostic:** record the signed real part of the complex mode-1 Fourier coefficient
   of E each step; FFT the time series (Hann window, parabolic sub-bin interpolation,
   physical search band) to extract the oscillation frequency `ω`.
6. **Validation control:** run classical PIC (`C_SI = 0`) at well-resolved `Δt` — a
   correct code must recover `ω ≈ ωpe`.
7. **Judge:** free Argo `argo:gpt-5.2` (localhost:44497), temperature 0, given the
   measured-vs-analytic table (no regex scoring).

**Tools/versions:** Python 3 + NumPy + Matplotlib (local, CherryRd). OA PDF fetch +
`pdftotext` via `ssh uicgpu` (osti.gov proxy). Free endpoints only.

**Commands:**
```
python3 work/sipic_dispersion.py report/evidence/sipic_dispersion_results.json
python3 work/plot.py
python3 work/judge.py | tee report/evidence/llm_judge_verdict.txt
```

---

## 4. Results vs paper

### Validation (classical PIC, C_SI = 0) — sanity check
| ωpe·Δt | measured ω/ωpe | target |
|--------|----------------|--------|
| 0.10 | 1.033 | 1.0 |
| 0.20 | 1.011 | 1.0 |
| 0.50 | 1.017 | 1.0 |

→ The from-scratch PIC recovers the physical plasma frequency to ~1–3%. Diagnostic sound.

### C1 — SIPIC down-shift (C_SI = 4): measured vs analytic Eq. 16
| ωpe·Δt | measured ω/ωpe | **Eq. 16 prediction** | classical (unmodified) | error vs Eq. 16 |
|--------|----------------|------------------------|------------------------|-----------------|
| 1  | 0.731 | 0.707 | 1.000 | **3.3 %** |
| 2  | 0.451 | 0.447 | 1.000 | **0.9 %** |
| 4  | 0.252 | 0.243 | 1.000 | **3.9 %** |
| 8  | 0.126 | 0.124 | 1.000 | **1.9 %** |
| 16 | 0.069 | 0.062 | 1.000 | **10.2 %** |

**The measured plasma-oscillation frequency tracks the analytic SIPIC down-shift
(Eq. 16) across a 16× range of `ωpe·Δt` — to ~1–4% for `ωpe·Δt ≤ 8` and ~10% at the most
extreme step (`ωpe·Δt = 16`, only ~6 samples per down-shifted oscillation) — and is
decisively inconsistent with the classical, unmodified `ω/ωpe = 1`.** This is exactly the
paper's stated verification result ("As Δt is increased, the contours follow the modified
dispersion relation … the modified dispersion curves traverse downward", §III.A).
Plot: `evidence/sipic_downshift.png`. Raw numbers: `evidence/sipic_dispersion_results.json`.

### Stability (C3)
All runs, including `ωpe·Δt = 16` (16× beyond the explicit-PIC limit), remained bounded
with the mode amplitude oscillating cleanly — consistent with the paper's stability bound
`ωΔt < 2/√C_SI` for `C_SI ≥ 1` (Eq. 14).

### Discrepancies / caveats
- **Paper-internal inconsistency:** Table I gives `Δt = 2a/ωpe` (ωpe·Δt = 2a) while §III.A
  prose gives `Δt·ωpe = a/2`. Because Eq. 16 depends only on the product `ωpe·Δt`, the
  replication sweeps the full range and the conclusion is independent of this ambiguity.
- **Paper κ-notation inversion:** Eq. 12/13 (`κ=1/F`, `ω²=ωp²/κ`) written literally gives an
  *up*-shift, contradicting the Eq. 16 text ("reduced frequency") and Fig. 1 (downward
  contours). The physically correct + self-consistent reading (implemented here) is the
  down-shift; this is a typographic/bookkeeping subtlety, not a physics error.
- Not tested: hybrid modes (C4), full energy-conservation curves (C5, needs WarpX/Aleph),
  Landau damping (C6). C2's thermal Bohm–Gross term was intentionally suppressed (cold run)
  to isolate C1.

---

## 5. LLM-judge verdict (free Argo gpt-5.2, verbatim)

> "The measured ω/ωpe agrees with Eq. 16 within ~1–4% for ωpe·Δt ≤ 8 and shows the correct
> down-shift trend at 16 (but with ~10% error) … the core claim — an effective dielectric
> producing a stable, down-shifted plasma frequency scaling like Eq. 16 for large ωpe·Δt —
> is reproduced. **VERDICT: REPLICATED.**"

Full text: `evidence/llm_judge_verdict.txt`.

---

## Verdict
**Verdict:** REPLICATED

The paper's central verification claim — that the SIPIC effective-dielectric modification
down-shifts the electron plasma frequency by `1/√(1 + C_SI·ωpe²·Δt²/4)` (Eqs. 12/16),
enabling stable operation far beyond the explicit `ωpe·Δt` limit — was independently
reproduced from the paper's equations with a from-scratch 1D ES-PIC. Measured frequencies
track the analytic prediction to ~1–4% over `ωpe·Δt ≤ 8` (10% at 16) and are decisively
distinct from the unmodified classical `ωpe`; a classical-PIC control recovers `ω ≈ ωpe`.

---

WAVE_RESULT set=OSTI-100 paper=3374709 verdict=REPLICATED dir=~/Dropbox/REPLICATE-PROJECT/OSTI-3374709-semi-implicit-ecpic-verification one_line=Independent 1D ES-PIC reproduces the SIPIC plasma-frequency down-shift ωpe/√(1+C_SI·ωpe²Δt²/4) (Eqs.12/16) to ~1-4% over ωpe·Δt≤8 (10% at 16), decisively unlike classical ωpe.
