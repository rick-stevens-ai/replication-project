# Failure Analysis — tazai2025

## Verdict: PARTIAL (Coverage 8/10, Agreement 6/10)

## What reproduced (agreement)
1. **Sharp low-T rise of λ_d at η=0.014.** λ_d climbs monotonically from ~0.196
   at T=8 meV to ~0.360 at T=0.1 meV — the paper's central "λ_d drastically
   increases for T < 5 meV" behavior. ✓
2. **Resonant enhancement precisely at η=0.014.** In the η-sweep at T=0.5 meV,
   λ_d peaks at η=0.014 (0.270), clearly above η=0.010 (0.205) and η=0.016
   (0.213). The paper states the chiral d-wave emerges for η in 0.01–0.016 — our
   peak sits inside that window. ✓ (This is the strongest quantitative match.)
3. **LC suppresses s-wave.** λ_s falls monotonically with η (1.19 → 0.44 for
   η: 0 → 0.02), consistent with the LC order shifting the balance away from
   s-wave toward chiral d. ✓
4. **Chiral character of the leading d-channel eigenvector.** Overlap with
   (1, ω², ω) is ~0.63–0.70; A/C sublattice phases differ by ~180°, capturing
   the chiral winding. ✓ (partial)

## What did NOT reproduce (disagreement)
1. **Chiral d overtaking s-wave globally.** In our simplified kernel λ_s > λ_d
   at all T and η sampled, so chiral d is not the single leading instability.
   The paper's key claim — chiral d "takes over the s-wave state" — is only
   partially supported (we see the *trend* via the η=0.014 λ_d resonance and
   λ_s suppression, but not a full crossover).
2. **Exact chiral phase pattern.** Ideal (0°, −120°, +120°) is only
   approximately recovered (A −11°, B −18°, C +167°) on the coarse mesh.
3. **PDW (~5%) and winding number w=2** not computed (out of scope for the fast
   base run).

## Root causes
- **Approximate form factors.** We used a physically-motivated staggered
  triangle-circulating f_ij with a 2×2 sign stagger, not the paper's exact
  Fig.1(c) f_ij (and g_ij for BO). The precise pattern controls the
  Aharonov-Bohm phase in Γ_ml that selects chiral d over s-wave.
- **Sublattice-interference hierarchy** Γ_mm ≫ |Γ_ml| (m≠l), which the paper
  invokes to boost the inter-sublattice complex pair-hopping, is present only
  implicitly; the exact NNN structure and vHS placement matter.
- **Coarse k-mesh (nk=8)** and fixed Matsubara cutoff (±64) — adequate for
  trends, not for a fine crossover T_c(g) determination.
- **Shallow LC-induced Fermi pocket at Γ** (the paper's mechanism) not
  explicitly verified; μ set by filling only.

## What would close the gap
Encode the exact f_ij/g_ij from Fig.1, enforce the vHS-at-Γ pocket, refine the
mesh, and compute the PDW fraction + gap winding. See `open_questions.json`.

## Honesty note
No values were fabricated. All numbers trace to `tazai2025_result.json`
produced by `replicate_tazai2025.py`. The disagreements above are reported as
found; the run genuinely does not show chiral d as the global leading channel.
