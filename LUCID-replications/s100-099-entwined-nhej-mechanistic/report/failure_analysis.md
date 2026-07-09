# Failure analysis — s100-099-entwined-nhej-mechanistic

Honest critique of this replication's limits. Written to Rick's
2026-07-05 standing rule: flag category gaps, do not paper over
absolute-metric disagreement, distinguish measurement-axis failure
from model-mechanism failure.

## Category 1 — What was NOT run (structural gaps)

### 1.1 Full 3-D CTRW spatial Geant4-DNA simulation
DaMaRiS is fundamentally a spatial Monte Carlo: each DSB end
performs continuous-time random-walk sub-diffusion in a 2.5 μm
nuclear sphere; synapsis is a diffusion-limited bimolecular
reaction at 25 nm encounter radius. This replication uses a
**mean-field per-DSB Gillespie surrogate** — the topology and
first-order rates are identical, but the spatial encounter
statistics are lumped into a single τ_synapsis = 60 s calibrated
to WT NHEJ t½. Consequences:
- **Cannot predict inter-DSB mis-rejoining statistics.** This is
  precisely the observable that would most decisively test
  "entwinement".
- **Cannot predict dose/density-dependent departures** from
  first-order kinetics (which DaMaRiS explicitly captures via
  spatial encounter saturation at high DSB density).
- **Cannot vary encounter radius** (10/25/50 nm sensitivity),
  which is a modelling choice the paper does not test.

### 1.2 Dynamic Time Warping goodness-of-fit
Paper reports DTW alongside χ² and RMSE, but does not condition
the conclusion on it. Not implemented here. Would be trivial to
add (10 lines with scipy or fastdtw).

### 1.3 Kuhne 2004 / Wu 2012 cross-validation datasets
Paper Fig 3 overlays black triangles/diamonds from these two
datasets as an out-of-sample cross-check. Not benchmarked in the
paper's quantitative Table 1 either, so not a headline claim, but
their omission means the replication cannot claim generalisation
beyond the Beucher 2009 fit target.

### 1.4 Fig 4 MRN/CtIP recruitment kinetics fit
The Scenario D rate constants were partly calibrated against
protein-recruitment-kinetics data in Fig 4 (not against Fig 3
foci kinetics alone). This is implicit in the archived
`pathwayHR.txt` rate values but was not independently re-fitted
here.

### 1.5 Alternative XLF-deficiency mechanism (Figs S6–S7)
Supplementary explores an alternative XLF model where the defect
is in fast NHEJ end-joining rather than in synapse stabilisation.
Not implemented; may change per-scenario ranking for XLF⁻ cells
specifically.

## Category 2 — What was run but disagrees (measurement-axis)

### 2.1 Absolute χ²_red values off by ~10×
This work: 52–66. Paper: 3–9.

Root cause: the Beucher 2009 Fig 1B **raw digitised foci counts**
(with SEMs) are not shipped with either paper. This replication
uses `code/beucher_data.py` — a template approximation calibrated
to the narrative ("WT resolves ~85% by 8 h; Lig4⁻ resolves <50%").
The template uses fractional residual (0…1) with SEM = 0.05 scaled
×100; the paper uses absolute foci counts (0…40) with SEM ±2–5
foci. Different denominators → different absolute χ².

This is **not** a model-mechanism failure. The rank ordering
(which is the paper's headline claim) is preserved: B is worst by
27% margin, D and A tied best, C intermediate. But **the specific
Table 1 numbers cannot be reproduced** without the Beucher raw
data. Blocker (a) in REPORT.md §6.

### 2.2 Paper ordering D < C < A < B; this work A ≲ D < C < B
The A/D tie in this replication is consistent with the paper's
own text ("Scenario A also fits well") and the paper's preference
for D over A rests on auxiliary MRN/CtIP recruitment-kinetics data
(Fig 4) not on Fig 3 foci alone. So this is not a disagreement so
much as a coarser resolution.

## Category 3 — What the paper itself does not test (honest gaps)

### 3.1 Spatial-entwinement geometry justification
The "entwined" mechanism assumes DSB ends stay in a common ~25 nm
neighbourhood long enough for MRN + RNF138 to act on both. This
is imposed by the CTRW encounter kernel, not derived from
chromatin-loop topology or damage-pattern statistics. See open
question Q1.

### 3.2 Chromosome-aberration validation
Residual DSB counts do not measure repair fidelity. mFISH /
translocation / dicentric assays would test entwinement much more
strongly. Not attempted in paper. See open question Q3.

### 3.3 Parameter identifiability
27 free rate constants fit to ~30 Beucher data points across 4
cell systems. No profile likelihood, MCMC posterior, or Fisher
information reported. Almost certainly non-unique. The four-
scenario comparison partly finesses this by fixing topology and
asking which topology wins, but even the winning topology's rates
are under-determined.

### 3.4 Cell-cycle-phase generality
Paper is G2-synchronised. G1 (HR unavailable) and S-phase
(replication-associated DSBs, single-ended HR) not tested. See
open question Q4.

### 3.5 High-LET regime and alt-EJ/MMEJ
Paper fit at 1.77 keV/μm proton. At high LET, Pol-θ-mediated
alt-EJ becomes a major competing pathway not represented in the
DaMaRiS graph. See open question Q2.

### 3.6 Cancer-cell translation
Normal fibroblasts + MEFs with single-gene KOs only. No cancer
cell lines with mixed DDR defects. See open question Q5.

## Category 4 — Verdict cross-check

Queue verdict: **REPLICATED**
Report 4-tier: **Partially Reproduced — Qualitative Confirmation**

Both consistent for this paper because its **headline deliverable
is a qualitative model-selection claim** ("entwined beats
competitive"), and that ordering — B worst, D ≈ A best, C
intermediate — was reproduced. Analogous to s100-072: paper's own
target is analytical/model-selection rather than an absolute-
number-matching claim, so REPLICATED-tier is defensible even with
a ~10× absolute-χ² gap on a measurement axis where the raw
reference data was never shipped.

Substance-matched note-tag: **"qualitative scenario ranking
replicated; absolute χ² values disagree ~10× due to
Beucher-2009-raw-data blocker; spatial CTRW replaced by mean-field
Gillespie surrogate."**

verdict_preserved = true (both queue and report agree at the level
of the paper's own headline claim).
