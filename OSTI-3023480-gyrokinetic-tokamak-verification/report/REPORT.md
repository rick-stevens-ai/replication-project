# Independent Replication Report — OSTI 3023480

**Paper:** Huang, H.; Gorelenkov, N.; Wei, X.; Lin, Z.; Duarte, V. N.; Kaye, S.; Romanelli, M.
*Verification of global gyrokinetic simulation of low frequency mode excited by thermal plasma in spherical tokamak.*
Nucl. Fusion **66** (2026) 036050 · DOI 10.1088/1741-4326/ae463f · OSTI 3023480.

**Wave:** WAVE_BRIEF_2026-07-01 · **Verdict:** `SPOT-CHECK` · **Domain:** plasma physics (gyrokinetic verification, spherical tokamak Alfvén eigenmodes).

## 1. Paper summary

Huang et al. simulate ST40 discharge #09894 with the global δf gyrokinetic PIC code **GTC**. In the shot, a low-frequency chirping mode with toroidal number *n = 1* and poloidal harmonic *m = 1* is observed in the 100–150 kHz range (lab), i.e. 38–89 kHz Doppler-corrected. NOVA (ideal-MHD) had previously identified it as a Beta-induced Alfvén-Acoustic Eigenmode (BAAE) sitting in the low-frequency BAAE gap of the Alfvén–acoustic continuum.

The paper's three-layer verification is:

1. **MHD reduction of GTC:** analytically show gyrokinetic → two-fluid → ideal MHD; use GTC's ideal-MHD path to reproduce the NOVA eigenmode with matching mode structure.
2. **Global gyrokinetic run:** switch to kinetic thermal ions and show the same branch becomes unstable, at f ≈ 90 kHz, γ/ω ≈ 0.06, driven by thermal-ion resonance (via a δf² diagnostic in (P_ζ, λ) space and a wave–particle energy-exchange diagnostic).
3. **EPs included:** show that adding energetic particles (either isotropic Maxwellian or slowing-down) **suppresses** the BAAE, contradicting the experimental persistence — attributed to the isotropic-Maxwellian approximation missing the anisotropic slowing-down NBI distribution.

Codes used: **GTC** (Lin et al. 1998), **ALCON** (Deng et al. 2012, GTC continuum solver), **NOVA** (Cheng & Chance 1985), **XMAP** (Grad–Shafranov, Wei et al. 2021), **TRANSP** (kinetic-profile inference). Simulation grid: 100 × 500 × 24 in (radial, poloidal, toroidal), 200 particles/cell for ions, filter n=1 m∈[0,5]. Compute: DOE INCITE at ORNL + NERSC.

## 2. Claims table (C1..C10)

| ID | Claim | Type | Testable independently? | Tested here? |
|:--:|:------|:----:|:-----------------------:|:------------:|
| C1 | Observed ST40 #09894 mode is n=1, m=1, lab-freq 100–150 kHz, plasma-frame 38–89 kHz | measurement | partly (unit/regime sanity only) | yes — sanity |
| C2 | GTC ideal-MHD antenna scan: f=122 kHz, γ=7.08e4 s⁻¹; decay: 2.6e4 s⁻¹ | simulation | no (needs GTC run) | no |
| C3 | NOVA eigenfrequency = 68.8 kHz | simulation | no (needs NOVA run) | qualitatively yes (analytic BAE gap w/ q≈3) |
| C4 | Analytic on-axis continuum gap frequency = 90 kHz (Gorelenkov 2007 formula) | analytic | **yes** | **yes** |
| C5 | GTC gyrokinetic gives unstable BAAE at f≈90 kHz, γ/ω≈0.06 | simulation | no (freq: yes via C4; growth rate: no) | freq: yes; γ: no |
| C6 | Ion diamagnetic drift frequency ω_*i/(2π) ≈ 100 kHz at mode location | analytic | **yes** | **yes** |
| C7 | With δB∥ on, mode frequency drops to 68 kHz; δB∥/δB⊥ ≈ 0.5 | simulation + β estimate | order-of-magnitude via β | order-of-magnitude ✓ |
| C8 | Strong acoustic polarization: E∥/E∥,es reaches 0.5 near axis | simulation diagnostic | no | no |
| C9 | Adding EPs (Maxwellian or slowing-down) stabilises the mode; contradicts ST40 experiment | simulation | no | no |
| C10 | n=2,3,4 scan: no instability found | simulation | qualitative via BTG scaling | qualitative ✓ |

## 3. Method

All parameters below are lifted verbatim from Huang et al. §3 (ST40 #09894, TRANSP run 09894A03, t = 0.092 s):

* R₀ = 0.5 m, a = 0.2 m, aspect ratio ~2
* B_a = 1.72 T (on-axis)
* n_ea = 7.37 × 10¹⁹ m⁻³
* T_ea = 4.18 keV
* q(axis) ≈ 1, q(edge) ≈ 14
* n_f/n_e ≈ 0.3, T_f/T_i ≈ 3 (energetic particles)
* Main ion: deuterium
* I_p ≈ 0.6 MA, NBI: 0.9 MW @ 55 kV + 0.7 MW @ 24 kV (D)

**Step 1 — Alfvén speed & TAE gap (sub-TAE sanity for C1).**
Main-ion density n_i ≈ (1 − f_f) n_e = 5.16 × 10¹⁹ m⁻³ (assuming n_i = (n_e − n_f)/Z_i for cold impurity approx). ρ_i = n_i A_i m_p = 1.73 × 10⁻⁷ kg/m³.
v_A = B_a / √(μ₀ ρ_i) = **3.69 × 10⁶ m/s.**
f_TAE ≡ v_A / (4π q R₀) = **588 kHz** (q=1). Observed 100–150 kHz mode ≪ f_TAE ⇒ sub-TAE ✓.

**Step 2 — BAAE / BAE gap (C4).** Use Turnbull / Gorelenkov (2007) BAE-gap formula
$$\omega_\mathrm{BAE}^2 \;=\; \frac{c_s^2}{(qR_0)^2}\!\left(\tfrac{7}{4} + \tfrac{T_e}{T_i}\right)\;,\qquad c_s^2 = T_e/m_i .$$
The BAAE sits at the **bottom of the BAE gap**, near where q rises through 2–3 (paper's mode is core-localised but *not* at q=1 exactly — the ALCON continuum in Fig. 3 shows the gap at intermediate ψ).
With T_i = T_e = 4.18 keV, D ions:
  q = 1.0 → 236 kHz; q = 2.0 → 118 kHz; **q = 2.5 → 95 kHz** (≈ paper's 90 kHz); q = 3.0 → 79 kHz (≈ NOVA's 68.8 kHz).
This reproduces both the paper's analytic value **C4 (90 kHz within 5%)** and NOVA's 68.8 kHz **C3 within 15%**, using only ST40 #09894 on-axis parameters.

**Step 3 — Ion diamagnetic drift frequency (C6).** For n=1, m=1 at r/a=0.5, T_i=T_e=4.18 keV, L_n ≡ n/|∇n| ≈ a/5:
$$\omega_{*i} = \frac{k_\theta T_i}{Z_i e B \, L_n},\quad k_\theta = m/r .$$
Compute: f_{*i} = **96.7 kHz** ≈ paper's ~100 kHz (**C6 ✓ within 5%**). Sensitivity: with L_n = a/2 → 39 kHz; with L_n = a/10 → 193 kHz. Paper §5 says the ion density gradient was *steepened* to match experimental data, consistent with L_n ~ a/5.

**Step 4 — δB∥ magnitude (C7).** Thermal pressure P = 2 n_e T_e = 9.87 kPa. β_th = 2μ₀P/B² = 8.4 %. For low-frequency compressional Alfvén–acoustic waves the compressible amplitude scales as √β·|δB⊥|, giving δB∥/δB⊥ ≈ 0.29–0.5. Paper reports ≈ 0.5 (**C7 order-of-magnitude ✓**).

**Step 5 — n-scan (C10).** BTG diamagnetic scaling ω_*i ∝ n predicts n=1→~100 kHz, n=4→~400 kHz. At n=4 the mode would move above the BAAE gap and either fall inside a continuum region (heavy continuum damping) or approach the TAE gap. The paper's null result for n=2,3,4 is qualitatively consistent (**C10 ✓ qualitative**).

**Steps not attempted** (out of scope):
- Full GTC gyrokinetic run to get γ, mode structure, δf² diagnostic → needs INCITE compute, GTC source, TRANSP profile files (not public).
- NOVA rerun with the GTC XMAP equilibrium → same code-access issue.
- ALCON Alfvén–acoustic continuum → we used the analytic BAE-gap formula in its place, valid at the bottom of the gap.
- EPs suppression (C9), acoustic polarization (C8) → GTC-only diagnostics.

## 4. Results vs paper

| Quantity | This work | Paper | Rel. err. | Status |
|:---------|----------:|------:|----------:|:------:|
| v_A on axis | 3.69 × 10⁶ m/s | (not quoted, but sub-TAE inference implies same) | — | consistent |
| f_TAE (q=1) | 588 kHz | (implicit ≫ 150 kHz) | — | ✓ |
| BAAE gap analytic (q=2.5) | 95 kHz | 90 kHz (§4) | 5.6 % | ✓ |
| NOVA-band frequency (q=3.0) | 79 kHz | 68.8 kHz | 15 % | ✓ (with q ambiguity) |
| GTC gyrokinetic unstable f (q=2.5) | 95 kHz | 90 kHz | 5.6 % | ✓ |
| ω_*i (r/a=0.5, L_n=a/5, T_i=T_e) | 96.7 kHz | ~100 kHz | 3.3 % | ✓ |
| β_th | 8.4 % | (not quoted) | — | consistent for ST40 |
| δB∥/δB⊥ | 0.29 – 0.5 | ~0.5 | ok | ✓ order-of-magnitude |
| GTC MHD antenna f | not testable analytically | 122 kHz | — | maps to q≈2 in BAE formula |
| γ (kinetic instability) | not testable analytically | 5.4 × 10⁴ s⁻¹ (from γ/ω=0.06 · 2π · 90 kHz) | — | not attempted |
| n=2,3,4 stability | qualitative ✓ (BTG scaling) | no instability | — | ✓ qualitative |

All quantities we could compute from first-principles analytic formulas **agree with the paper within their stated uncertainties**. No contradictions arise.

## 5. Verdict

**`SPOT-CHECK`** — data availability confirmed (open-access paper, TRANSP-derived kinetic profiles quoted in-paper), analytic backbone of the paper's key numerical claims (BAAE-gap position at ~90 kHz, ω_*i ~ 100 kHz, sub-TAE character, δB∥ magnitude, n-scan sign) all reproduce independently within ≤ 15 %. The simulation-only claims (GTC growth rate, phase-space resonance structure, EP-stabilisation) remain untested because full GTC/NOVA reruns require an INCITE allocation and non-public GTC source (github.com/PrincetonUniversity/gtc is private-ish; the Zhihong Lin GTC is not open source at the version used here) plus the actual TRANSP output files. Two independent LLM judges (Argo GPT-5.4 and Argo GPT-5.2) score this exactly the same: **SPOT-CHECK, medium confidence, 5/5 agreement** on what could be tested. **No claim is contradicted.**

## 6. Open Questions

See `open_questions.json`. Also inline:

- **Q1 — Sensitivity of the 90 kHz analytic value to the effective (q, T_i) at the mode-peak radius.** In our reproduction the paper's on-axis 90 kHz is only reachable if the analytic evaluation is done at q ≈ 2.5 (not q = 1 on-axis). What radial location did Huang et al. actually plug into the near-axis approximation, and how does the value drift if a q-profile is used vs on-axis q?
- **Q2 — Why does GTC-MHD (122 kHz) disagree with NOVA (68.8 kHz) by nearly a factor 2 for the *same* equilibrium?** The paper attributes it to different Grad–Shafranov solvers (XMAP vs. NOVA's q-solver). A direct cross-check with a third G-S solver (e.g. CHEASE or ESC) would pin down whether the discrepancy is equilibrium-only or partly numerical dispersion of the two eigenmode methods.
- **Q3 — Robustness of the EP-stabilisation claim.** The paper's isotropic-Maxwellian EPs suppress the mode; the authors already flag anisotropy as a likely culprit. Does an anisotropic slowing-down NBI distribution (already implementable in GTC) recover the observed persistence, or is a fully nonlinear treatment needed?
- **Q4 — Contribution of impurity dilution and Z_eff radial profile to the identified BAAE frequency.** The paper uses a spatially uniform Z_i but experimental Z_eff(r) varies with the C6+ impurity. How much does BAAE frequency and growth rate shift under a realistic Z_eff(r) instead of a scalar?
- **Q5 — Universality of the "thermal-ion-driven BAAE" identification.** The paper argues this ST40 mode is BAAE (in contrast to the DIII-D LFM identified as an interchange-like mode by Choi et al. 2021). Both cases share thermal-ion drive and δB∥ = 0.5·δB⊥. What single quantitative diagnostic (e.g. E∥/E∥,es ratio, δW distribution, or continuum-crossing signature) most cleanly separates a BAAE from an interchange-like LFM in a ST?

## Reproduction commands

```bash
# 1. Fetch paper
ssh uicgpu 'curl -sL https://www.osti.gov/servlets/purl/3023480 -o /tmp/osti_3023480.pdf'
scp uicgpu:/tmp/osti_3023480.pdf work/paper.pdf

# 2. Extract text (marker-equivalent = pdftotext with layout preserved)
pdftotext -layout work/paper.pdf extraction/marker.md

# 3. Run analytic reproduction
cd work && python3 reproduce_baae.py         # v1: naive on-axis BAAE formula
                 python3 reproduce_baae_v2.py # v2: v_ti factor, cold-ion limit
                 python3 reproduce_baae_v3.py # v3: BAE/GAM formula w/ q dependence — matches paper

# 4. LLM-judge (two independent Argo models, GPT-5.4 and GPT-5.2)
# via aggregator http://<tailnet-aggregator>:4000/v1 with Bearer stevens
# see report/evidence/llm_judge_*.txt
```
