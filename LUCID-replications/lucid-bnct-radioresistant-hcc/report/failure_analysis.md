# Failure Analysis — lucid-bnct-radioresistant-hcc

Honest critique of this replication. Written to be adversarial to the
replication's own claims, not to the paper. Verdict is **PARTIAL** and this
document explains why it is not REPLICATED, and where the replication itself
is thin.

## 1. What the paper's headline actually is

The paper's headline is a two-part claim:

1. **HepG2-R (acquired γ-radioresistance) has a substantially higher D10 to
   Co-60 γ-rays than parental HepG2** (5.749 vs 3.496 Gy).
2. **BNCT closes that gap**: RBE(HepG2-R) = 5.972 vs RBE(HepG2) = 3.675, i.e.
   BNCT is *more* effective on the resistant line than on the parental line.
3. Mechanistically, BNCT drives more γH2AX foci, delayed DSB repair via HR/NHEJ
   suppression, sustained G2/M arrest, and apoptosis re-sensitization.

## 2. What the replication actually exercised

- **Arithmetic-level** exercise of the RBE claim (recomputed RBE from
  paper-quoted D10s → exact match to 4 s.f.).
- **LQ-refit-level** exercise of the γ-ray D10 claim (refit LQ to text-quoted
  SFs → within ~3.5%).
- **Digitization-level** exercise of the BNCT D10 claim (digitized Fig 3B →
  D10 off by 18–40%, direction preserved).
- **Text-consistency** exercise of Table 1.
- **Direction-only** cross-check of every mechanism panel.

So the headline is exercised in the sense that its arithmetic core is
independently reproduced. It is NOT exercised in the sense that:

- The BNCT dose (in Gy) is taken from the paper; the underlying neutron
  transport + ¹⁰B(n,α) micro-dosimetry was not re-simulated.
- No mechanism panel was quantitatively re-derived — we can only agree with
  the *sign* of every fold-change.

## 3. Where the replication is genuinely weak

### 3.1 No independent neutron-beam Monte Carlo
This is the single biggest gap. For a BNCT paper, the fluence-to-dose
conversion is where most of the physics lives, and the paper cites the THOR
reactor thermal column but does not publish the MCNP/PHITS deck. We accepted
the paper's absorbed doses at face value. A more complete replication would:

- Rebuild the THOR + irradiation-tube geometry in Geant4 or open-MCNP,
- Score thermal-neutron fluence at the sample position,
- Convert to absorbed dose via a ¹⁰B(n,α) micro-dosimetric kernel at the
  reported 25 µg/mL BA loading,
- Compare the derived Gy-per-second dose rate against the paper's stated dose
  rate.

That entire physics leg is missing here. Compute budget is the excuse; it is
still an honest omission.

### 3.2 BNCT-side clonogenic is digitizer-limited
The 18–40% D10 offset on Fig 3B is not a model failure; it is because the
paper does not publish per-dose SFs and figure digitization has finite
accuracy. This is a paper-side reproducibility gap that our replication
inherits rather than solves. It could be closed by writing to the authors
for raw SFs, which we did not attempt.

### 3.3 Mechanism panels are direction-only
Every claim about γH2AX foci, KU70/KU80/RAD51, cell-cycle fractions,
CHK2/CDK1 phosphorylation, caspase-3/BCL2/PUMA/BAX is only corroborated
directionally. Because the paper reports these as summary fold-changes
without raw data, we cannot say whether the magnitudes are correct — only
that the reported *sign* of the effect is plausible. A malicious over-claim
of 2× vs 1.2× fold-change would be undetectable from our replication.

### 3.4 Single cell-pair, single-source study
Even if everything above were closed, the paper is a single-cell-pair,
single-source study (HepG2 vs HepG2-R, Co-60 vs one BNCT geometry). The
generalization to "BNCT is a good idea for radioresistant HCC in the clinic"
is not licensed by n=1 pair.

### 3.5 No effort on ¹⁰B-uptake heterogeneity
Table 2 reports a mean 58–59 ppm plateau. Because BNCT dose scales linearly
with local ¹⁰B and the α range is ~10 µm, uptake heterogeneity can bias the
population-averaged RBE significantly. We did not attempt any stochastic
sensitivity analysis — see open question 4.

## 4. Where the replication is genuinely strong

- The RBE arithmetic recomputation to 4 s.f. rules out a
  simple-typo-in-Table-4 failure mode.
- The γ-ray LQ refit within 3.5% rules out a "the reported D10s are
  numerical artifacts of a bad fit" failure mode.
- The Table 1 consistency check rules out a
  "the dose-rate/time table is inconsistent" failure mode.
- Together these are enough to say the paper's *arithmetic and reporting* on
  the radiobiology side is clean. That's a real result.

## 5. Verdict justification

**PARTIAL** is the right call:
- **Not REPLICATED**, because the neutron beam physics + the mechanism
  quantitation + the BNCT SFs are all unverified beyond direction.
- **Not SPOT-CHECK**, because more than a spot check was done: full LQ refit
  on γ-ray, exact RBE recompute, table consistency, plus figure regeneration.
- **Not NO-GO**, because nothing here contradicts the paper.

Coverage of paper's claims 5/10; agreement on the replicable subset 8/10.
Headline is exercised on the arithmetic + γ-ray-fit level; not exercised at
the beam-physics or wet-lab-magnitude level.
