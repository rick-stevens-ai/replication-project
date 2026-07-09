# Failure analysis — lucid100-fast-neutron-lymphocyte-dsbs-doserate

## Verdict framing
Verdict is **REPLICATED**, but that is a table-level verdict on a paper that
exposes almost none of its underlying primary data. The verdict should not be
read as "this paper is reproducible in a strong sense" — it means "everything
the paper made replicable was replicated, and 7/8 headline claims cleanly pass."

## Hard critique (Rick's 2026-07-05 rule: not a whitewash)

### 1. C7 method-text vs numbers inconsistency (real reproducibility defect)
The paper's Methods (§2.2, p.7) explicitly states the repair half-life was
obtained by subtracting the 24 h residual, dropping the 24 h point, and fitting
a single-exponential to t ∈ {2, 4, 8, 12}. Executing that procedure literally
on the paper's own Table 3 yields **t½ ≈ 2.89 h (HDR) / 3.27 h (LDR)**,
with bootstrap 95 % CI [0.84, 7.50] / [0.83, 6.73] — the paper-reported
8.6 / 12.0 h sit **outside** this interval. The reported numbers are only
recovered by a raw single-exponential fit from t ≥ 2 h (no subtraction),
yielding 9.92 / 13.08 h. This is a structural method-vs-number mismatch,
not a digitization error (table entries verified to ≤ 0.01 foci/cell).

This class of defect is important because it is silent-to-eyes: the paper's
qualitative story (LDR > HDR half-life, both ~10 h scale) is preserved under
both fits, so a casual reader would not notice. It only surfaces under
literal-Methods replication.

### 2. Fast-neutron RBE claim is implicit, not reproduced from data
The paper positions itself in the high-LET literature but does not include a
matched low-LET control arm at iThemba. Any RBE inference is cross-study.
Our replication cannot reproduce an RBE value because none is stated — and
the reader is left to synthesize one from external low-LET baselines that
differ in donor pool, scoring method, and fixation time. This is a common
weakness of single-facility neutron radiobiology papers.

### 3. Dose-rate effect (DRE) direction is not the classical high-LET expectation
Classical radiobiology holds that DREs shrink toward zero as LET rises,
because at high LET a single track deposits enough energy to make DSB
formation dose-rate-independent. The paper reports a ~40 % HDR-over-LDR
DSB-yield effect, which is direction-preserved (HDR > LDR) but not compared
against a low-LET DRE magnitude in the same lab. The result is that we cannot
say from this paper alone whether the DRE at fast-neutron LET is *reduced*
relative to low-LET (as expected) or *comparable* (as reported here).

### 4. Under-powered model selection
Only 5 dose points (0, 0.125, 0.25, 0.5, 1.0 Gy) were measured. The choice
of a 2nd-order polynomial over LQ (αD + βD²) or linear cannot be
statistically discriminated at this n. AICc gives poly2 an edge of ~5–6
units over linear but LQ is indistinguishable from poly2. The paper does not
discuss this ambiguity.

### 5. Donor variability is pooled, not modelled
n = 4 donors, cross-donor mean ± SD only. No per-donor tables, no ICC
estimate, no random-effect analysis. Since inter-donor variance in DSB
induction is known to be substantial (Vral 2011, Rothkamm 2003), all
paper-reported SDs are almost certainly conservative under-estimates of the
true prediction interval for a new donor.

### 6. Neutron spectrum specified only as "fast"
The p(66)/Be(40) reference points to prior dosimetry work [42] but the
actual energy spectrum, LET distribution at the irradiation point, and mean
neutron energy are not in the paper. This is the operative blocker for
mechanistic Monte Carlo (PARTRAC / MCDS / TRAX) replication, and it prevents
cross-facility comparison to 14 MeV or 62 MeV neutron beams.

## Reproducibility-blocker inventory
| Missing artifact | Blocks | Recoverable without author contact? |
|---|---|---|
| Per-cell γ-H2AX foci CSV (~32 k rows) | ANOVA, per-donor stats, weighted regression, C7 resolution | No |
| Metafer/MetaCyte classifier config | Wet-lab pipeline re-execution | No |
| GraphPad Prism v5 project (.pzfx) | C7 method-vs-number resolution | No |
| iThemba p(66)/Be(40) spectrum + LET | Mechanistic MC (PARTRAC/MCDS) | Partially — from dosimetry refs |
| Raw immunofluorescence micrographs | Image-analysis replication | No |
| IRB approval number / consent chain | Ethics-chain re-derivation | No |

## What went well
- Digitization was clean (max abs err 0.005 on per-dose ratio).
- 7/8 headline claims cleanly reproduced.
- Method-vs-number anomaly (C7) surfaced and documented, not hidden.
- No paid endpoints, no author contact, no heavy compute.

## What went badly
- Cannot resolve C7 without upstream Prism project or per-cell CSV.
- Cannot compute an RBE from data alone.
- Cannot mechanistically model DSB induction without the neutron spectrum.
- Verdict masks a paper that is table-replicable but not data-reproducible.

## Standing recommendation
Retag this paper in the LUCID-100 master TSV from `simulation/model replication`
to `wet-lab assay / radiobiology table replication`. The paper does not
provide a mechanistic model; the original tag was inaccurate.
