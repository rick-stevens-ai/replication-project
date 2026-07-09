# Failure Analysis — LUCID slot 63

Honest critique of what this replication actually delivered versus what the
paper's headline claims are. Written to justify a PARTIAL verdict and
resist the temptation to over-claim REPLICATED.

## The paper's actual headline

Friedrich, Durante, Scholz (RR2964, 2012) is the **founding static
formulation of the GLOBLE / Giant-Loop DNA Damage Model (GLDM) family**.
Its four most-cited contributions are:

1. A **closed-form survival curve** derived from Poisson placement of DSBs
   into $N_L$ megabase-pair chromatin loops, with isolated vs clustered
   lesion classes carrying weights $\varepsilon_i \ll \varepsilon_c$.
2. Mechanistic explanation of the empirical **LQ-to-linear crossover** in
   photon survival curves at clinical dose (5–20 Gy).
3. Analytic **map from microscopic parameters to LQ coefficients**
   $\alpha_{LQ}, \beta_{LQ}$.
4. **Empirical cross-cell-line $\beta$-vs-$\alpha$ anti-correlation** claim
   (Fig. 5), predicted mechanistically by the model, anchored on the 150+
   line dataset that becomes the PIDE database.

Downstream (not scored here): the same static machinery is the entry point
for the ion/high-LET extended GLOBLE line (Friedrich 2013, IJRB) and the
kinetic-GLOBLE branch (Herr 2014, PLoS ONE).

## What we did

- Contribution 1: **YES**, closed-form survival implemented exactly.
- Contribution 2: **YES**, LQ-to-linear crossover visually and numerically
  reproduced on RT112.
- Contribution 3: **YES**, LQ map exposed as `alpha_lq` / `beta_lq`
  properties, RT112 numbers in literature ballpark.
- Contribution 4: **NO on our subset.** 17 cell lines, Pearson $r=+0.655$,
  wrong sign. Recorded as INCONCLUSIVE.

That is 3 of 4 headline claims exercised and reproduced, and 1 headline
claim tested on a coverage-limited subset with an opposite-sign result.
**That is PARTIAL, not REPLICATED.** Calling it REPLICATED would ignore
that the paper's most-cited empirical claim (the anti-correlation) came
out wrong on our data.

## What we did NOT do (structural gaps)

### Gap 1: No track-structure Monte Carlo re-run
The paper's DSB yield $\alpha_{DSB} = 30$ DSB/Gy/cell is a paper-fixed
constant here, transcribed from Herr 2014 Table 1. We did NOT re-derive it
from PARTRAC, TOPAS-nBio, Geant4-DNA, or any other nanoscale
track-structure code. For photons this is defensible (the yield is
well-established and roughly LET-independent in the photon regime), but
it means the "upstream" half of the GLDM narrative — track structure
producing a DSB spectrum — is **input, not output**, in this
replication.

**Why we didn't:** track-structure MC is expensive (hours to days on a
CPU cluster) and out of scope for a first-pass smoke replication with
free endpoints only. Would push the slot to a proper full replication.

### Gap 2: No DSB-clustering algorithm reimplemented on real chromatin geometry
The paper's analytic core is Poisson placement of DSBs into $N_L$
**identical** loops. Real chromatin has a heavy-tailed, cell-type-specific
loop-length distribution (visible in modern Hi-C data). We did NOT:
- Build an explicit chromatin geometry model.
- Implement a DSB-cluster-detection algorithm (e.g., DBSCAN on 3D
  break positions with a genomic-distance threshold).
- Rerun the survival prediction on a length-distribution-weighted
  ensemble of loops.

**Why we didn't:** the paper itself uses the analytic Poisson-on-identical-loops
approximation, so our reimplementation matches the paper's abstraction.
A Hi-C-anchored rerun is a genuine extension (see open question Q2), not
a replication.

### Gap 3: No PDF text
Paper is closed-access. We worked from PubMed abstract + Herr 2014
sibling paper. **Risk:** minor symbol or sign-convention drift not
detectable without direct PDF verification. **Mitigation:** Herr 2014
explicitly re-cites Eqs. 1–7 and its numerical static limit reproduces our
numbers to plotted precision.

### Gap 4: 17 vs 150+ cell lines for the anti-correlation
The most consequential coverage gap. Recorded honestly as INCONCLUSIVE
rather than either REPLICATED or REFUTED, because:
- Our subset is small enough to have a legitimate positive $\varepsilon_i$–$\varepsilon_c$
  correlation that would mask the paper's predicted anti-correlation
  purely as a sampling artifact.
- The paper's own claim is explicitly anchored on the 150+ line PIDE
  meta-analysis; refuting on a 17-line subset would be an unfair standard.

### Gap 5: No radiation-quality / LET dependence
RR2964 is photon-only, but it is the entry point to the ion-extended
GLOBLE line. We stayed in scope (photon-only), so this is a scope decision
rather than a gap per se, but any reader wanting the "GLOBLE for ions"
story needs to look at the Friedrich 2013 IJRB follow-up.

## Why the verdict is PARTIAL, not REPLICATED

Three independent grounds:

1. **Empirical:** the paper's most-cited claim (Fig. 5 $\beta$-vs-$\alpha$
   anti-correlation) came out with the wrong sign on our 17-line subset.
2. **Structural:** neither the track-structure MC nor the chromatin-geometry
   DSB-clustering algorithm was rerun — both major mechanistic ingredients
   of the GLDM name were inherited whole from the paper as fitted or
   fixed constants.
3. **Access:** no PDF text; formula transcription cross-checked via
   sibling paper only.

Two independent grounds against saying it is SPOT-CHECK or worse:

1. The analytic core was cleanly reimplemented from scratch, and 3 of 4
   headline claims were genuinely reproduced with numerical output.
2. The 3-judge external audit majority-voted PARTIAL (2 of 3 judges);
   only one judge went to SPOT-CHECK.

PARTIAL is the honest label.

## Why this is a LUCID-typical result

The LUCID corpus is dominated by radiation-biology and radiation-oncology
papers that mix (a) tractable analytic cores that can be reimplemented on
a laptop, with (b) large empirical claims anchored on curated multi-decade
compilations (PIDE, ICRP, NUREG) that are not easily accessed in
machine-readable form. That combination reliably produces PARTIAL: the
analytic core replicates, the compilation-anchored empirical claim does
not, and no amount of local re-coding will close the gap without pulling
the compilation.
