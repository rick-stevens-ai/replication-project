# Failure Analysis — Honest Critique

This is not a whitewash. The paper is competent and the replication verdict is
REPLICATED, but there are real gaps in both the paper and this replication. Naming
them honestly:

## What DID work
- Algebraic inversion of Tables 1–3 recovered absolute foci-per-cell counts with
  strong internal consistency (5 independent I_0 estimates for γH2AX-acute agree
  to stdev 0.10 around mean 2.19).
- Linear regressions reproduced to ≥ 3 decimal places for all three explicit fits.
- Hockey-stick SSE comparison qualitatively supports the paper's non-rejection of
  low-dose thresholds in the chronic-mode data.

## What DID NOT work / is missing

### (1) Lutz–Lutz bootstrap p-values NOT reproduced
The paper's headline threshold-model claims (p=0.72 for γH2AX-chronic, p=0.95 for
pATM-chronic) rely on a 10,000-iteration Lutz & Lutz (2009, Mutat. Res. 678:118)
stochastic procedure that requires per-cell raw counts (~300–400 cells per data
point × 4 technical replicates × 3 experiments = ~3600–4800 cells per data point).
We have only the derived means and SEMs. Our SSE-based check agrees in qualitative
direction, but the exact p-values are not independently verified. **This means the
paper's most rhetorically weighty statistical claim is only partially replicated.**

### (2) Figure 3 (co-localization) intermediate points are interpolated
The paper's narrative gives only endpoints (43% acute, 67% acute-late; basal chronic,
~60% chronic-late). Intermediate dose points in Fig 3 would require pixel-level
digitization of the published bar chart or access to the underlying CSV. We linearly
interpolated between endpoints and flagged this on the figure. A user consuming
`figures/fig3_colocalization.png` as canonical data would be misled about the shape
of the intermediate response.

### (3) Single-exponential kinetics is a stand-in, not derived
The paper reports half-lives (γH2AX: 2.35 h acute / 2.44 h chronic; pATM: 1.64 h /
2.14 h) without stating the functional form used. We assumed single-exponential decay
to a plateau at I_0. Our fit slightly over-predicts repair speed at 6 h (8% remaining
vs paper's 14% for pATM-acute), which is consistent with the true decay being
multi-exponential or having a plateau ABOVE I_0. We cannot distinguish these
alternatives from published data.

### (4) MSC radioresistance claim not internally tested by the paper
The paper positions MSCs as radioresistant but does not include a same-day lymphocyte
control on the same source. The reported γH2AX slope (0.021 foci/mGy acute) is
broadly comparable to published lymphocyte slopes in the same dose window. The
"MSCs are special" framing is inherited from prior literature, not shown internally.
This is a paper-design limitation we flag but cannot fix without wet-lab work.

### (5) Passage / donor confound is undisclosed
Methods report "primary human bone-marrow MSCs (Biolot, Russia)" without donor count
or characterization. Passage 5–6 is mid-passage. The chronic-mode fit has R² = 0.888
(vs 0.988 acute), suggesting substantial residual variance that could be donor,
passage, or biological noise — the paper cannot distinguish. No passage-controlled
sub-arm.

### (6) Co-localization asymmetry not decomposed
The paper reports co-localization as a single percentage per condition, not
decomposed into "fraction of γH2AX+ foci also pATM+" vs "fraction of pATM+ foci also
γH2AX+". At low chronic dose these fractions likely diverge (ROS-driven pATM without
DSB). This asymmetry is invisible in Table 4 and unrecoverable by us.

### (7) ATM-kinase dependence at low chronic dose not tested
At 30 mGy chronic, pATM K-value (0.0075) approaches γH2AX K-value (0.0080) while
co-localization is basal — suggesting a large fraction of low-chronic-dose pATM foci
may be ROS- or replication-stress-driven rather than DSB-driven. The paper does not
apply KU-55933 or an ROS scavenger to test this.

### (8) Nougat parse skipped
We did not run a GPU-hosted Nougat parse of the PDF because pdftotext extraction of
Tables 1–3 was clean and sufficient for the numerical inversion. A stub
`extraction/nougat.mmd` with the PDF SHA-256 is provided so a future re-run can
detect drift. Friction: **low** — no analysis depends on the missing parse.

## Residual uncertainty

- **Quantitative uncertainty:** low. Linear fits match paper to ≥ 3 decimal places.
  The one 5% discrepancy (pATM-acute intercept 1.039 vs 0.993) is fully explained by
  SEM-driven rounding in Tables 2–3.
- **Interpretive uncertainty:** moderate. The paper's mechanistic story (concurrent
  repair during chronic exposure driving the 2.6× slope reduction) is plausible but
  not tested against the alternative saturation hypothesis. Our replication inherits
  this ambiguity.
- **Statistical uncertainty:** moderate. Non-rejection of a threshold model at n=5
  dose points with the reported SEMs is not the same as evidence FOR a threshold.
  Our qualitative SSE check does not resolve this.
- **Biological uncertainty:** high. Findings on one MSC source at passage 5–6
  cannot be assumed to generalize across donors, passages, or MSC subtypes
  (iPSC-MSC, adipose-MSC, umbilical-MSC).

## What would flip the verdict
- If a lymphocyte control arm at matched dose rate showed comparable or lower
  slopes than the MSCs, the "radioresistance" framing would need revision.
- If per-cell raw counts became available and a proper Lutz–Lutz bootstrap yielded
  p < 0.10 for the threshold-vs-linear tests, the low-dose-threshold claim would be
  rejected.
- If intermediate-dose-rate (0.5–8 mGy/min) experiments showed a sigmoidal
  foci-vs-rate curve, the concurrent-repair interpretation would be falsified in
  favor of signaling saturation.
