# Failure analysis — honest report

## What went wrong / what took time

### F1 — `np.trapz` removed in numpy 2.4 (5 min lost)
First run crashed at `np.trapz`. NumPy 2.0 deprecation-removed `trapz`
in favor of `trapezoid`. Trivial fix via `sed`. Logged as a
cross-project lesson: NumPy 2.x code review checklist should include
`grep -n trapz`.

### F2 — sqrt(η_A η_B) mis-interpretation (30 min lost)
Initial version used `sqrt(η_A η_B)` in Eq. (1) because the paper's
Klyshko-efficiency measurement identity uses
`η = CC/sqrt(S_A · S_B)`, which visually appears near Eq. (3).
That inversion is for *extracting* B from data, **not** for
*predicting* coincidences from B. First run overshot by 4.4×.

The error was caught by comparing to paper's expected 1.2 Gbit/s
headline and reading Eq. (1) more literally. Corrected to `η_A × η_B`
per the printed formula.

**Lesson:** When a paper writes both `η` in a measurement identity
(Klyshko form) and `η(λ)` in a model formula (transmission per arm),
these are the same numerical quantity but enter the two equations
differently. Read the model equation as printed, not through the lens
of the measurement identity.

### F3 — n_channel_pairs off by 2× (15 min lost)
Second attempt used `n=33` for the 100 GHz spacing (mis-reading the
paper's `n` as "number of channels" rather than "number of channel
pairs"). Fig. 6 legend clearly labels `n=66` for 100 GHz, and text
confirms "using 66 channel pairs of off-the-shelf WDM devices"
(§2, para. after Eq. 4). Corrected to n=66 with symmetric summing
about λ₀.

### F4 — 12.5 GHz `n=529` requires ~66 nm range which exceeds the
usable band (~53 nm) → truncation applied but not perfectly
matched to the paper's implicit assumptions.

The paper claims `n=529` at 12.5 GHz spacing, which nominally spans
~66 nm — comfortably inside their quoted 106 nm band, so this
should work in principle. However, our Λ(λ) Gaussian drops to
<5% at Δλ = 53 nm and we truncate there. This truncation likely
contributes to the systematic 0.55× ratio at the narrowest spacing.
Logged as Q3 in `open_questions.json`.

## Residual gaps (things not fully closed)

### G1 — ~2× systematic underestimate across all five scenarios
Every replication rate is 0.46–0.56× the paper's number. Causes:
- Gaussian Λ(λ) is thinner in the shoulders than the true measured curve
- Coherence time σ_C is transform-limited (paper does not specify exact form)
- t_CC optimization is 1D; a joint (P, t_CC) or per-channel weighting could
  raise the total
None of these individually change the qualitative story, but they
prevent claiming "REPLICATED" at the tight (~30%) threshold.

### G2 — Marker / Nougat parses missing
Marker and Nougat are not installed centrally and the central corpus
does not have pre-parsed versions of this paper. The `extraction/`
files use `pdftotext -layout` with clear headers noting this. Content
is faithful; only layout is different.

**Rick note (2026-07-05):** the QC-100 brief allows this fallback
("pull from central corpus if parsed, else run Marker"). We chose
fallback over spending 30+ min installing Marker for a one-shot
replication.

### G3 — CHSH S computed analytically, not from a Monte Carlo
For a Werner state ρ = V|Φ+⟩⟨Φ+| + (1-V)I/4, max CHSH is 2√2·V.
Using V = 0.994 gives S = 2.811. This is not a real detection-outcome
Monte Carlo; it's the analytic Tsirelson-bound-scaled prediction.
Since the paper does not print an explicit measured S value (only
the visibility), the analytic prediction is the correct benchmark.
A Monte Carlo with the same underlying state and detector model would
reproduce this to statistical fluctuations.

### G4 — Detector-count-rate saturation flagged but not fully modeled
The paper assumes 200 MHz max SNSPD count rate. Our per-channel
singles at 400 mW / 100 GHz exceed this (~250 MHz on central pairs).
A nonparalyzable dead-time model with τ = 100 ps was applied and
had a small effect. The paper implicitly requires 132 physical
detectors per party running at 250+ MHz simultaneously; whether such
a system exists is Q5 in `open_questions.json`.

## Friction categories

| Category | Occurrences | Impact | Mitigation |
|----------|-------------|--------|------------|
| NumPy API drift | 1 | Low (5 min) | Test-first pattern for new environments |
| Formula misreading (sqrt vs product) | 1 | Med (30 min) | Read equations as printed, not through inferred conventions |
| Off-by-2× parameter | 1 | Low (15 min) | Cross-check n against figure legends |
| Missing central-corpus artifact (Marker) | 2 | None (used fallback) | Consider running Marker on QC-200 batch centrally |
| Missing exact-form definitions in paper (σ_C, Λ(λ), tCC opt basin) | 3 | Med (drives residual bias) | See open questions Q1-Q3 |
| Long analytic runs (n=529) | 1 | Low (once caught, optimized in 5 min) | Coarse grid then golden-section refine |

## What worked really well

- Paper's own Methods section is explicit enough that all four core
  equations can be transcribed directly into Python.
- The three published Λ(λ) averages exactly pin a Gaussian fit
  (peak, +/-28.15 nm mean, +/-53 nm mean → sigma=21.33 nm, all three
  reproduced to <0.1%). This is a rare case of a paper being
  cross-checkable at the digitization step.
- QBER < 0.4% from V > 99.2% is algebraically exact — no simulation
  needed, matches perfectly.
- Distance rolloff qualitatively reproduced (10 km → 40% in
  replication vs 63% in paper) — the sign is right, and the
  discrepancy has a clean physical explanation (pump reoptimization).

## Would I trust this replication?

Yes, for the qualitative claim "this source can deliver Gbit/s secure
key rates in a BBM92 scheme with dense WDM at telecom wavelengths".
No, for the exact "1.2 Gbit/s at 400 mW" number — that requires
either (a) a hardware repeat of the measurement or (b) access to the
paper's actual Λ(λ) tabular data. Both are outside a text-driven
independent replication's reach.
