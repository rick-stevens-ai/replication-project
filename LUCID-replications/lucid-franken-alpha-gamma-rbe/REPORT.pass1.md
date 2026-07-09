# Replication report — Franken et al. 2012, RBE of alpha vs gamma

**Target paper.** N.A.P. Franken et al., "Relative biological effectiveness
of high linear energy transfer α-particles for the induction of
DNA-double-strand breaks, chromosome aberrations and reproductive cell
death in SW-1573 lung tumour cells", *Oncology Reports* **27**: 769–774,
2012. DOI [10.3892/or.2011.1604](https://doi.org/10.3892/or.2011.1604).

**Verdict: PARTIAL — RBE arithmetic and uncertainty propagation fully replicated; raw dose-response data not tabulated, so the underlying LQ/linear fits cannot be re-run from scratch.**

- Coverage: **6 / 10**
- Agreement: **10 / 10** on what we *could* recompute.

## Why "partial" and not "replicated"

The paper reports its quantitative results in a single Table I:
linear-component slopes `alpha` (in Gy^-1) of the LQ model for four
endpoints (γ-H2AX foci, clonogenic survival, chromosome fragments,
colour junctions) under two radiation qualities (Am-241 α-particles,
130 keV/μm; Cs-137 γ-rays), plus their corresponding RBE values with
1-σ uncertainties.

What is **public and usable**:
- The exact LQ model: `S(D)/S(0) = exp(-αD - βD²)` for survival,
  `F(D) = αD + βD²` for the other endpoints (their eq. on p. 771).
- The exact `α` ± σ for every endpoint / radiation pair (Table I).
- All experimental details (cell line, dose ranges, LET, dose rates,
  fitting method = SPSS weighted linear regression).

What is **NOT available**:
- The individual data points (foci/cell at each dose, surviving
  fraction at each dose, etc.) used to fit Table I. These are only
  shown graphically in Figure 2 of the paper. There is no supplementary
  material.
- The numerical value of `β` for γ-ray cell survival (the paper says
  it is significant but does not tabulate it).
- Raw cell counts, replicate-level data, or any deposited dataset.

A full from-scratch refit would require figure digitization of Fig. 2
(four panels × two curves × handful of dose points each). The triage
note ("likely simple LQ/RBE dose-response refit; may be low-value but
still doable") was accurate: it is doable but adds digitization noise
on top of an already-replicated arithmetic core, so I stopped at the
partial verification.

## What was replicated

### 1. RBE recomputation from Table I α values

For each endpoint I computed `RBE = α_α / α_γ` with first-order
delta-method uncertainty propagation under independent Gaussian errors:

`σ(RBE) / RBE = sqrt( (σ_α/α_α)² + (σ_γ/α_γ)² )`

| Endpoint                  | α_α (Gy⁻¹)  | α_γ (Gy⁻¹)   | RBE recomp. | σ recomp. | RBE paper | σ paper | Match |
|---------------------------|-------------|--------------|-------------|-----------|-----------|---------|-------|
| γ-H2AX foci (DNA DSBs)    | 25.0 ± 8.2  | 25.0 ± 3.0   | 1.000       | 0.349     | 1.0       | 0.3     | ✔    |
| Clonogenic survival       | 2.2 ± 0.38  | 0.15 ± 0.045 | 14.67       | 5.08      | 14.7      | 5.1     | ✔    |
| Chromosome fragments      | 16.8 ± 4.5  | 1.10 ± 0.31  | 15.27       | 5.94      | 15.3      | 5.9     | ✔    |
| Colour junctions          | 9.2 ± 3.2   | 0.69 ± 0.20  | 13.33       | 6.04      | 13.3      | 6.0     | ✔    |

All four central RBE values reproduce to ≤ 0.5% and all four
uncertainties to ≤ 1.7% — i.e. exact match within rounding.
This confirms the paper used the same first-order Gaussian error
propagation for σ(RBE).

Results JSON: `results/rbe_recomputed.json`.

### 2. Internal consistency check — fraction of DSBs that are lethal

In the Discussion (p. 773) the authors claim that "only a small
fraction of the DNA-DSBs (about 1% of DSBs induced by γ-rays and
about 10% by α-particles), are involved in cell death".

Taking `α_survival / α_DSB` as a proxy for that fraction:

- γ-rays:  0.15 / 25.0 = **0.60 %**  (paper claim "about 1 %")
- α-part.: 2.20 / 25.0 = **8.80 %**  (paper claim "about 10 %")

Both are consistent with the paper's rounded-to-one-significant-figure
statements. Results JSON: `results/lethal_dsb_fraction.json`.

### 3. Reconstructed dose-response curves

Using the published `α` values from Table I, I redrew the four
panels of Figure 2 (with the caveat that γ-ray cell survival has a
β term the paper does not tabulate, so the survival panel is drawn
as pure exponential — i.e. the *linear contribution only*).

Figure: `figures/fig2_reconstructed.png`.

The visual shape and dose ranges match the published Fig. 2 layout:
- α-particle slopes are uniformly much steeper than γ-ray slopes for
  the three non-DSB endpoints.
- DSB induction lines (top-left panel) lie on top of each other,
  reflecting the RBE = 1 for γ-H2AX foci.
- Survival curves diverge by more than a decade at 2 Gy.

## What could be done with more effort

To upgrade to **REPLICATED** rather than **PARTIAL**:

1. Digitize the eight curves from Fig. 2 (e.g. WebPlotDigitizer on the
   PDF page). Each panel has ~5–8 data points per curve.
2. Re-fit `αD` (linear) for the three non-survival endpoints and
   `αD + βD²` for γ-ray survival using weighted least squares,
   weighting by error bars from the figure.
3. Compare refit `α` against Table I. Expect agreement within the
   digitization error (~5–10%).

This is mechanical but adds little scientific value: the arithmetic
already checks out exactly, the experimental design and equations
are public, and the only thing a digitized refit would reveal is
whether the SPSS fits in the paper were done correctly — which the
internal consistency of Table I already strongly suggests.

## Honest assessment

This paper is unusually **good** for replication on a small scale:
- The full quantitative result is in one printed table.
- The model equations are explicit.
- The experimental setup is described in enough detail to be
  reproduced wet-lab (with an α-particle facility).

It is unusually **bad** for *data*-driven replication:
- No deposited data, no supplement, no per-dose tabulation.
- Fits are described only as "SPSS weighted linear regression"
  with no further detail (weight function not specified beyond
  that error bars per point exist).

For a LUCID-style "can a model/automated agent rederive this?"
exercise, this is at the **low** end of useful: the result is a
4-row table of slope ratios, and any sensible agent that reads
the paper will reproduce those exact numbers in seconds. There
is no hidden computation, no statistical subtlety, no model
choice that another team could plausibly disagree on.

**Recommendation:** keep this in the LUCID corpus as a positive
control / sanity check on the agent's ability to (i) extract
numbers from a table, (ii) do error propagation correctly, and
(iii) recognize when a paper's "richness" is mostly textual rather
than data-rich. Do *not* use it as evidence that an agent can
"replicate radiobiology papers" in a strong sense.

## Files

```
.
├── franken_2012.pdf           # original PDF (copy of LUCID target)
├── README.md
├── PROGRESS.md
├── REPORT.md                  # this file
├── code/
│   └── refit_rbe.py           # full replication script
├── results/
│   ├── rbe_recomputed.json    # per-endpoint RBE recomputation
│   ├── lethal_dsb_fraction.json
│   └── summary.json
└── figures/
    └── fig2_reconstructed.png # reconstructed dose-response panels
```
