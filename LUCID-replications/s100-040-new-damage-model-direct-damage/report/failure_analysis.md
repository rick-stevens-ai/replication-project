# Failure Analysis — LUCID Slot 040 (Park 2022)

Honest critique of both the paper and this replication.

## Queue verdict vs substance

Queue label: **REPLICATED**. Substantive verdict: **Partial —
Analytical Complete**. We preserve the queue label to keep the metadata
stable, but a reader who takes "REPLICATED" at face value will
overstate what this session actually established.

**What was actually reproduced.** Every analytically tractable quantity
in the paper: CG bead radii from group volumes, phosphate PO₃ total
binding energy to 0.4 meV, McMahon-Currell mass conservation to machine
epsilon, μ back-fit from OC(D) curves to <0.4%, Eq. (8) formula, and
Table 3 threshold-range inclusion.

**What was NOT reproduced.** The headline claim — 14.2% mean error
against gel-electrophoresis SSB/DSB yields across seven LET points —
requires a Geant4-DNA v10.7p01 Monte Carlo run over 5,400 plasmids in
a 3 μm sphere with the authors' unreleased application source. That is
roughly 40% of the paper's quantitative content and it was not
independently reproduced here. Calling this "REPLICATED" without a
footnote is misleading; the correct label is "analytical scope closed,
MC scope out of reach."

## Weaknesses of the paper (not the replication)

### 1. The direct/indirect split is not independently derived

The paper's central sales-pitch is replacing empirical threshold
energies with CG-potential threshold energies for the *direct* damage
channel. But the paper does not perform a first-principles calibration
of the *indirect* (radical-mediated) channel. The McMahon φ parameter
soaks up indirect damage and is fit to totals, not to independent
OH-radical yield or diffusion-kinetics data. Our back-fits confirmed
this weak constraint: OC(D) recovers μ to <0.4% but φ only to ±46% for
⁶⁰Co and ±42% for 1-MeV e⁻. The paper does not acknowledge this.

The honest framing: the direct channel is now first-principles, but the
overall damage model is still one adjustable parameter (φ) short of
identifiability from OC data alone.

### 2. No scavenger-modulation or OER validation

The standard test of a direct-damage model is to sweep radical
scavenger concentration (DMSO, glycerol, Tris, mannitol) and show that
the direct component is invariant. The paper does neither. All
validation is unmodulated ⁶⁰Co and 1-MeV e⁻ on dried pBR322 in air.
Dried plasmid suppresses but does not eliminate the bound-water shell,
and does not test scavenger-concentration dependence at all. Without
this test the central claim — that the model correctly partitions
direct vs indirect damage — is not experimentally validated; only
totals are validated.

Similarly, no OER prediction is made. OER-vs-LET is the single
strongest discriminator between damage models and the paper does not
attempt it.

### 3. Cross-code comparison is intra-family only

Fig. 5b compares to TOPAS-nBio, which shares Geant4-DNA physics
underneath. No comparison to TRAX (Krämer group), KURBUC (Nikjoo group),
or PARTRAC (Friedland group) — all of which have independent
track-structure implementations. A cross-family comparison would be a
genuine test; an intra-family one is a consistency check.

### 4. Deoxyribose 30.5 eV cannot be reconstructed from the paper

Table 2 itemises only the phosphate PO₃ bead. The deoxyribose 30.5 eV
threshold appears as a final number and is never broken down in the
main text. Our closed-form estimate using the canonical furanose
skeleton (3 C-C + 3 C-O + 1 non-bonded O⋯O) gives 22.12 eV. Anyone
reimplementing from the article alone will land ~8 eV short, and the
discrepancy will propagate directly into predicted deoxyribose-lesion
yields. Supplementary Fig. S2 presumably itemises the missing pairs
but we did not retrieve it.

### 5. Data-availability statement is functionally closed

"Available from the corresponding author through a reasonable written
request" means no public code, no CG geometry file, no clustering
algorithm, and no gel CSV. All five reproducibility blockers documented
in the source REPORT.md §6 flow from this. In the LUCID corpus this is
a mid-tier reproducibility posture; every subsequent reproduction
attempt will hit the same wall.

### 6. Paper Eq. (3) is misprinted

Documented in REPORT.md §Bug Discovery. The typeset Morse expression
yields U(r_e) = −2 D_e and inflates the phosphate total by 2.75×. Table
2 was clearly produced with the standard Morse form; only Eq. (3) is
wrong. Anyone reimplementing from the equations alone (not from the
tables) will be off by a factor of two until they spot this. Would be
a useful erratum.

## Weaknesses of this replication (not the paper)

### 1. Analytical scope only

We did not build Geant4-DNA, did not run any MC, did not attempt to
reproduce Figs 3-5 or the headline 14.2% number. This was a deliberate
scope choice (CPU-only host, out-of-policy build, ~10⁵-10⁶ CPU-hours to
converge) but it means the paper's *empirical validation claim*
remains unverified by us. That is the most consequential unreproduced
element.

### 2. Deoxyribose closed-form is incomplete

We estimated the deoxyribose CG total using the canonical furanose
covalent skeleton (3 C-C + 3 C-O + 1 O⋯O) and landed at 22.12 eV vs
the paper's 30.5 eV — an 8 eV shortfall. This is not a bug in the
paper (Supplementary Fig. S2 presumably itemises more pairs); it is a
gap in our access to the supplement. We flagged this as blocker #2 but
did not close it.

### 3. Supplementary Information not retrieved

Neither Fig. S1 (CG geometry) nor Fig. S2 (deoxyribose bond list) nor
the gel-band-intensity data were retrieved. Nature supplements have no
scriptable free API; a paid Springer route or a manual browser
download would close some of these gaps.

### 4. φ back-fit weakness noted but not deeply explored

The 40-50% φ recovery error is a known weak-constraint issue of OC
alone. A more thorough replication would demonstrate this by adding an
SC(D) point or an SC/OC ratio to break the degeneracy — we noted the
issue but did not perform that supplementary analysis.

### 5. No Nougat OCR

We used pdftotext -layout rather than Nougat because the source is
born-digital and pdftotext extracts equations and tables cleanly for a
Scientific Reports PDF. The `extraction/nougat.mmd` file is
intentionally a stub. This is defensible but breaks the LUCID
standard-artifact-set convention; a future re-run with Nougat would
give a proper .mmd file and would be a cheap addition.

## Cross-check on note-tag optimism

The note-tag / metadata around this slot uses "REPLICATED" as a
positive signal. The substantive picture is more nuanced:

- Analytical scope: **truly reproduced**, tight agreement (<1 meV on
  energies, <0.02 Å on geometry, machine ε on conservation laws).
- MC scope: **not reproduced**, blocked by five specific missing
  artefacts (source code, geometry, clustering, gel CSV, physics
  cards). None available from any free endpoint.
- Bug caught: paper Eq. (3) misprint, worth an erratum.

A more honest tag would be "REPLICATED-ANALYTICAL, MC-BLOCKED" but we
preserve the queue label per protocol.

## Bottom line

The paper is a solid piece of theoretical work with a clean CG-potential
derivation that reproduces to <1 meV. Its empirical validation is
methodologically thin (no scavenger sweep, no OER, no cross-family
code comparison) and its data-availability posture is functionally
closed. The model is worth building on — but not without the five
follow-up experiments listed in open_questions.json.
