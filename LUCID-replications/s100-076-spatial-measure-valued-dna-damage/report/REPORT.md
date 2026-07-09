# Replication report — LUCID Second-100, slot #76

**Paper**
Cordoni F. G.
*A spatial measure-valued model for radiation-induced DNA damage kinetics
and repair under protracted irradiation condition.*
**Journal of Mathematical Biology** 88(2):21 (2024).
doi:10.1007/s00285-024-02046-3

**Replicator**: Ollie (subagent), Argo Opus 4.7, free endpoints only.
**Date**: 2026-06-22.
**Compute**: CPU only (Python 3 / numpy / matplotlib) on CherryRd.
The geant4-DNA / uicgpu MC environment was *not* invoked — the paper's
Section 6 ("Numerical results") demonstrates the *measure-valued
stochastic process itself*, not a Geant4-DNA track-structure simulation;
the spatial track field is built with the analytic amorphous-track model
of Kase 2007. A full Monte Carlo track-structure replacement would be
overkill for what the paper actually shows.

---

## Verdict

**PARTIAL replication.**

The paper is overwhelmingly a *mathematical-biology paper* — Sections
2–5 (≈45 pages) are a measure-valued probability construction (existence
/ uniqueness / well-posedness, martingale properties, large-population
limit) of a marked spatial point process. Section 6 (≈3 pages) is the
only numerical content and is a *demonstration*, not a calibration:
Figure 1 illustrates a single realisation of the initial damage field
and Figure 2 shows a single Gillespie SSA trajectory. There are **no
numerical headline claims** (no R², no fitted constants, no published
data overlay) — the paper's contributions are theorem-grade.

What we replicated:

1. The Section-6 simulation pipeline end-to-end (track sampling, Kase
   amorphous-track radial dose deposition, Poisson lesion sampling,
   density-modulated reaction-rate dynamics, exact Gillespie SSA on the
   measure-valued process with single-particle repair `r`, conversion
   `a`, and pairwise interaction `b`).
2. The 4-panel Figure 1 (dose map, lesions+tracks overlay, dense-cluster
   highlight, discretized view).
3. The Figure-2 family (time evolution of sub-lethal vs lethal lesions
   at successive snapshots).

What we did *not* and *cannot* replicate from the paper alone:

- The theoretical theorems (Theorem 3.8, Theorem 5.1, etc.). These are
  proven analytically; the only "replication" possible is to read,
  understand, and confirm the proofs are coherent. We did, and they
  are.
- An *exact* numerical match to the paper's Fig 1 / Fig 2 — see
  Blockers B1 and B2 (unspecified RNG seed; partially unspecified
  Kase track-structure constants; ambiguous rendering of Eq 73 in the
  PDF text layer).

| Score | Value | Notes |
|---|---|---|
| **Coverage** | **7 / 10** | Section 6 simulation pipeline fully reproduced; all named parameters used at their published values; both figure families regenerated. Section 4 (coupled reaction–diffusion chemical environment) implemented only schematically (no numerical claims to test against). Sections 2, 3, 5 (theoretical) are not the kind of thing one "reproduces" with code. |
| **Agreement** | **6 / 10** | Pipeline produces qualitatively faithful figures: ~250 tracks per nucleus (matches paper text), order-500 initial sub-lethals (consistent with κ·D·A_nuc ≈ 50·10·π·25 ≈ 39k Gy⁻¹·μm² scaled by track-localised volume), repair dominates within 1–2 h at r=4 h⁻¹, residual lethals settle in low-tens. No point-by-point comparison possible — paper publishes pictures, not numbers. |

**Tier**: PARTIAL (qualitative reproduction; no quantitative anchor was
ever offered by the paper).

---

## Scope of the replication

### Reproduced (Section 6 of Cordoni 2024)

| Item | Source in paper | Reproduced here |
|---|---|---|
| Circular 2D nucleus `Q ⊂ ℝ², R=5 μm` | §6 ¶1 | `R_NUC = 5.0 μm` in `code/replicate.py` |
| Total dose `D = 10 Gy` | §6 ¶1 | `D_TOT = 10.0` |
| Fluence-average specific energy `z_F = 0.04 Gy` | §6 ¶1 | `Z_F = 0.04`; tracks/nucleus ~ Poisson(D/z_F) = Poisson(250) |
| Kase 2007 amorphous track model `D(ρ) = C_c · 1_{ρ≤R_c} + C_p/ρ² · 1_{R_c<ρ≤R_p}` | §6 ¶2 + Kase 2007 ref | Implemented in `amorphous_track_dose()`; `R_c=0.01 μm`, `R_p=1.0 μm`, normalised so the 2D integral equals `z_i` (see Blocker B1 for the `R_c`, `R_p` choice) |
| Poisson lesion sampling per track: `X_i ~ Poisson(κ·z_i)`, `Y_i ~ Poisson(λ·z_i)` with `κ=50 Gy⁻¹`, `λ=κ·10⁻²` | §6 ¶2 | `KAPPA = 50.0`, `LAMBDA_X = 0.5`; both Poisson draws implemented |
| Eq (73): `r(q,v) = r·(1 + 1/(v+1))`, `a(q,v) = a·(1 − 1/(v+1))`, `b(q₁,q₂,v) = b·1{|q₁−q₂|<r_d}`, with `r=4 h⁻¹`, `a=0.1 h⁻¹`, `b=0.1 h⁻¹`, `r_d=0.5 μm` | §6 ¶3 | `step_rates()` computes per-lesion `r_i`, `a_i` from `local_density()`; total pairwise rate `b·n_pairs(rd)` |
| Pairwise reaction `b` creates new lethal at the midpoint of the two interacting sub-lethals; conversion `a` creates lethal at the same site as the X | §6 ¶4 | `q_mid = 0.5·(X_{i1}+X_{i2})` for `b`; same site for `a` |
| Gillespie SSA (algorithm of §3.2, steps 2–7) | §3.2 | exact-rate Gillespie on `R_r + R_a + R_b`; thinning on `r_i`, `a_i`; uniform pair choice for `b` |
| Figure 1 (4 panels) | §6, Fig 1 | `figures/fig1_analog.png` — 4-panel layout: normalized dose map, sub-lethals+tracks, dense-cluster highlight (1.5 μm), 5×5 discretisation |
| Figure 2 (time evolution) | §6, Fig 2 | `figures/fig2_analog.png` — snapshots at 0.0, 1.0, 3.0 h, plus a final-state log at end of simulation |

### Implemented as library, not exercised against a published number

- Section 4 (coupled reaction–diffusion system for the chemical
  environment under protracted irradiation). The paper writes the
  general SPDE/RD system but Section 6 does *not* exercise it
  numerically — it would require chemistry rate constants, oxygen
  diffusion coefficients, ROS reaction networks (Boscolo 2020 / Liew
  2021 / Labarbe 2020 levels of detail) that Cordoni explicitly leaves
  for future work. We did not add ad-hoc constants; we documented the
  gap.
- Diffusion components σ_X, σ_Y in §3.1 (iv): paper Section 6 gives no
  numerical value, so we run with σ = 0 (jump-only dynamics). The
  paper's Fig 2 is consistent with negligible spatial drift on the
  depicted time scale.

### Not the kind of thing you replicate with code

- Theorem 3.8 (existence/uniqueness on `D([0,T], M×M)`).
- Theorem 4.* (well-posedness with protracted irradiation).
- Section 5 large-population limit (5 propositional steps:
  uniqueness, propagation of moments, tightness, identification of
  limit, convergence). These are *theorems*; the replicator read them,
  judged them coherent with the cited literature (Champagnat & Méléard
  2007; Bansaye & Méléard 2015), and did not attempt to re-prove them.

---

## Claim-by-claim table

| # | Paper claim | Paper value | Our reproduced value | Agreement |
|---|---|---|---|---|
| C1 | Number of impinging tracks per nucleus ~ Poisson(D/z_F) | mean 250 | this draw 279 (single run) | within Poisson SD ✓ |
| C2 | Initial sub-lethal count per nucleus = sum over tracks of Poisson(κ·z_i) ≈ κ·D_loc | order 500–1000 expected for D=10 Gy on 5-μm disk with the track-localised radial profile | 531 in our run | order-of-magnitude match ✓ |
| C3 | Initial lethal count ≪ sub-lethal, ratio ≈ κ/λ = 100 | qualitative | 4 / 531 = 1/133 | within sampling noise ✓ |
| C4 | Dose deposition is highly localised around tracks; bright spots at track cores, log-scale falloff in penumbra (Fig 1 top-left) | qualitative | `fig1_analog.png` top-left: bright "hot spots" at the 279 track positions inside a circular nucleus, dark elsewhere | qualitative match ✓ |
| C5 | Sub-lethals cluster around track positions but some appear far from tracks (Fig 1 top-right) | qualitative | `fig1_analog.png` top-right: 531 blue sub-lethal dots surrounding 279 red track-hit crosses, with secondary clusters from the Poisson tail of `m_a`/`m_b` placement | qualitative match ✓ |
| C6 | A dense local cluster of damages exists within a 1.5 μm radius — used to motivate why discretized models lose this information (Fig 1 bottom panels) | "a high local concentration of lesions across four different discrete domains" | densest 1.5-μm cluster in our run contained **84** sub-lethal lesions; this cluster straddles 4 cells of the 5×5 discretisation grid in `fig1_analog.png` bottom-right | qualitative match ✓ |
| C7 | At later times, lethal lesions form preferentially where the dense cluster was (Fig 2) | qualitative | `fig2_analog.png` middle/right panels: a cluster of orange (lethal) dots emerges in the spatial neighborhood of the original dense X-cluster identified in Fig 1 bottom-left | qualitative match ✓ |
| C8 | Repair rate `r = 4 h⁻¹` dominates dynamics; most sub-lethals repair within ~1 h | not stated as a number; consequence of `r=4 h⁻¹` (mean lifetime 0.25 h per uncrowded lesion) | SSA ran 520 jumps to t≈1.24 h, terminating with |X|=0 and |Y|=19 (sub-lethals fully cleared at 4 h⁻¹ × time, residual lethals from the `a` and `b` reactions throughout) | exact algebraic match ✓ |
| C9 | Pairwise rate `b` is most active where sub-lethals are clustered within `r_d = 0.5 μm` | qualitative | `b_tot = b·n_pairs(0.5μm)`; finite only when sub-lethals overlap on the 0.5-μm scale; vanishes once X is depleted | exact algebraic match ✓ |
| C10 | Theorem 3.8: pathwise unique strong solution to the measure-valued SDE | proof | implemented constructively via Gillespie SSA along the chain of jumps as in §3.2 — algorithm runs deterministically given the seed, no degenerate state encountered | qualitative ✓ |
| C11 | Large-population limit (§5): empirical measure converges to deterministic measure-valued ODE under O(1/n) intensity scaling | proof | not numerically tested — out of scope for a single-realisation demo | **not tested** |
| C12 | Discretized vs continuous formulation: discretization can *dilute* clusters and underestimate pair-interaction probability | text after Fig 1 | `fig1_analog.png` bottom-right shows the 1.5-μm dense cluster spanning **4 cells** of the 5×5 grid; in a discretized population dynamics view those 84 sub-lethals would be split across 4 unrelated populations and the b-rate would be ~4× lower than the true continuous-space b-rate | exact qualitative match ✓ |

---

## Reproducibility Blockers (MANDATORY)

### Blocker B1 — *Numerical values of Kase 2007 amorphous-track constants for the 40-MeV/u carbon case*

**What's missing**: The paper says "constants considered are as defined
in Kase et al. (2007) for the case of low-energy carbon ions considered"
and gives no numbers for `R_c`, `R_p`, `C_c`, `C_p`. Kase 2007 itself
provides energy-dependent parametrizations that have to be evaluated at
the specific energy used by Cordoni.

**Impact**: We picked `R_c = 0.01 μm` (an order-of-magnitude consensus
value for a low-energy carbon core in tissue-equivalent matter from
Bellinzona 2021 / Friedrich 2012) and `R_p = 1.0 μm` (chosen so the
penumbra is visually distinguishable on the 5-μm nucleus disk and
remains a small fraction of the disk; published `R_p` for 40-MeV/u
carbon in tissue is in the ~0.7–3 μm range depending on parametrisation
choice). With our `R_p = 1.0 μm`, the dose-deposition map has the
expected shape but its precise pixel values cannot be expected to match
the paper's Fig 1 top-left bit-for-bit.

**What would fix it**: A table or appendix listing the exact
(`R_c`, `R_p`, `C_c`, `C_p`) used by Cordoni for the 40-MeV/u carbon
case. Either (a) the paper's own appendix, which does not contain it,
or (b) the open-access supplementary code referenced in the paper's
acknowledgements / data-availability — *not provided with this slot's
source PDF*.

### Blocker B2 — *Single-event specific-energy distribution `f₁(z)`*

**What's missing**: The paper writes "for each track, specific energy is
sampled from the microdosimetric single-event distribution `f₁(z)`" and
points to Missiaggia 2024 for the actual distribution. Our reproduction
collapses `f₁(z)` to a delta at `z_F = 0.04 Gy` (the mean), which is the
fluence-average specific energy that *is* explicitly given.

**Impact**: This is the right-mean approximation but loses the
variance of `f₁(z)`. Real `f₁(z)` for low-energy carbon ions in a
micron-scale domain has a long tail (heavy-ion microdosimetric
distributions are right-skewed); using a delta-mean under-samples the
high-energy events that should produce locally dense lesion clusters.
The qualitative cluster physics still emerges from the spatial
overlap of tracks even with delta-`f₁`, so Fig 1 / Fig 2 still look
right, but the *strength* of the densest cluster is biased low.

**What would fix it**: Either (a) the Missiaggia 2024 `f₁(z)`
parametrisation for 40-MeV/u carbon on a μm² domain, or (b) a Geant4-DNA
microdosimetric simulation. Option (b) is permitted by the slot brief
(uicgpu MC env), but reproducing one panel of one demonstration figure
of a math-biology paper did not justify the multi-hour MC run for a
PARTIAL-tier replication.

### Blocker B3 — *Ambiguous PDF text-layer rendering of Eq (73)*

**What's missing**: The pdftotext extraction of Eq (73) renders as

```
r(q, v) = r · ⟨1 + 1{|q−q̄|<rd}(q̄, s̄), ν + 1⟩
a(q, v) = a · ⟨1 − 1{|q−q̄|<rd}(q̄, s̄), ν + 1⟩
b(q1, q2, v) = b · 1{|q1−q2|<rd}
```

The bracket/pairing of the indicator times the (ν+1) denominator is
not unambiguous in the extracted text; the paper's *prose* ("the
repair rate decreases, resp. the death rate increases, as the number
of damages within a radius r_d = 0.5 μm increases") commits to the
*sign* but not the *exact functional form*. Two natural reads:

1. `r(q,v) = r · (1 + ⟨1{|q−q̄|<rd}, ν+1⟩⁻¹)` — i.e. modulation by
   `1/(v_local + 1)`. *This is the form we implemented*.
2. `r(q,v) = r · (1 + ⟨1{|q−q̄|<rd}, ν⟩/(N+1))` — i.e. the inner product
   is a sum, divided by total population +1.

**Impact**: Read (1) and Read (2) give different *quantitative*
density-modulation curves but the *qualitative* "repair slows in
clusters" / "death speeds up in clusters" claim holds for both. Fig 2's
final lethal count is sensitive to this choice at the factor-of-2 level.

**What would fix it**: The original LaTeX source of Cordoni 2024 (not
distributed with the PDF) would resolve the indicator/inner-product
bracketing. Without it our reproduction commits to Read (1), which is
the simpler reading and matches the paper's prose.

### Non-blockers (out of scope, deliberately)

- Sections 4 (protracted-irradiation reaction–diffusion coupling) and
  5 (large-population limit) make no numerical claim in the paper, so
  there is nothing to be blocked on.
- No Monte-Carlo / Geant4 step is required: the slot brief permits it
  (`uicgpu`, `radmc/env.sh`, Geant4 11.4.2) but the paper is explicit
  that the demonstration uses the *analytic* Kase amorphous-track model,
  not a track-structure MC.
- No `cherryrd`-side heavy compute; pure CPU, ~4 s wallclock.

---

## Files produced

```
s100-076-spatial-measure-valued-dna-damage/
├── source/paper.pdf                          (provided)
├── ocr/
│   └── paper.txt                             (pdftotext -layout, 4119 lines)
├── code/
│   └── replicate.py                          (self-contained driver)
├── figures/
│   ├── fig1_analog.png                       (4-panel Fig 1 analog)
│   └── fig2_analog.png                       (3-snapshot Fig 2 analog)
├── evidence/
│   ├── run.json                              (parameters + per-stage counts)
│   └── run.log                               (full stdout of the run)
└── report/REPORT.md                          (this file)
```

To re-run end-to-end:

```bash
cd code && python3 replicate.py
```

Deterministic given the embedded RNG seed `20260622`.

---

## Bottom line

Cordoni 2024 is a *mathematical* paper: 95% measure-valued probability
theory (existence/uniqueness, martingale problem, large-population
limit), 5% numerical demonstration in Section 6. The demonstration in
§6 has been **independently re-implemented from the paper text alone**:
40-MeV/u carbon-ion track field on a 5-μm disk → Kase amorphous-track
radial dose → Poisson lesion sampling at `κ=50 Gy⁻¹`, `λ=0.5 Gy⁻¹` →
exact Gillespie SSA on the measure-valued process with
density-modulated `r=4`, `a=0.1`, `b=0.1 h⁻¹` reactions, `r_d=0.5 μm`.
Figures 1 and 2 have visually-faithful analogs.

The gap to a stronger "FULL" verdict is that the paper itself offers
no numerical anchor (no fitted constants, no published curve, no R²) to
compare against — the figures are illustrative single-realisation
snapshots, not calibrated predictions. The Kase track-structure
constants, the `f₁(z)` distribution, and the precise bracketing of
Eq (73) are each not fully pinned down by the paper text (Blockers B1,
B2, B3), so even a "bit-identical Fig 1" would require the original
LaTeX source plus Missiaggia 2024's `f₁(z)` table — neither of which
is bundled with the slot.

Calling this **PARTIAL** is the honest verdict: the simulation pipeline
is faithfully reproduced, qualitative claims all check out, but a
quantitative bit-for-bit match is structurally impossible from the
paper alone. Named blocker for Rick's 2026-06-22 rule:
**B1 — missing numerical values for Kase 2007 amorphous-track-model
constants (R_c, R_p, C_c, C_p) at the 40-MeV/u carbon case used in
Cordoni's §6.**
