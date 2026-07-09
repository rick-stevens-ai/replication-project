# Failure analysis — honest critique

This is the un-whitewashed accounting. Written 2026-07-06 as part of the LUCID backfill.

## Verdict cross-check (Rick's 2026-07-05 rule)

- **Queue verdict:** `REPLICATED`
- **Actual verdict** (from REPORT.md §8, verbatim):
  > `VERDICT=PARTIAL COVERAGE=5/10 AGREEMENT=4/10`
- **Cross-check outcome:** **MISMATCH.** This dir is one of the ~4-of-18 LUCID dirs Rick
  flagged where the queue-side label overstated the actual replication depth.
- **Verdict preserved for this backfill:** `PARTIAL`. Do not upgrade to REPLICATED. The
  REPORT.md author (2026-06-22 pass) already correctly graded this as PARTIAL and explained
  why in §7. The queue label appears to have been set optimistically based on the
  "10/10 dominance match" without weighting the 2-60 orders of magnitude quantitative miss
  or the missing refit / CIs / figures 3-5.

## What did not work

### 1. The quantitative survival numbers are wrong by 2-60 orders of magnitude
Absolutely not defensible as a "replicated" quantitative curve. The 10-row `results/summary.csv`
puts *E. coli* WT at $S(\gamma=4\,\text{kGy}) = 1.4\times10^{-61}$ where the paper reports
$\sim 10^{-5}$. That is a 56-order-of-magnitude miss, driven entirely by using
$F(D) = $ logistic placeholder instead of the digitized Krisko & Radman 2010 curves. The
exponent $X = 6.76$ amplifies small $P$ errors catastrophically. **This is a real failure**,
not a rounding issue. It happens to leave the *ratio* $\log Q_1/\log S$ roughly right,
which is why the qualitative mechanism map still matches — but "the ratio is right and the
absolute numbers are 60 orders off" is a red flag, not a success.

### 2. The fitter was not independently run
Table 1 parameters were used as inputs, not outputs. The paper's 95% CIs are therefore
completely unverified by this replication. A replication that does not re-fit is
categorically weaker than one that does. The paper's central methodological artifact is the
FORTRAN random-restart simulated-annealing fitter, which is not publicly released — so any
CI verification would necessarily be an independent SciPy reimplementation, not a fitter
replication.

### 3. Figures 3, 4, 5 were not re-rendered
Only the two log-survival plots were produced. The paper's Fig. 4 (Q$_1$ contour in
$(D, K_\text{rep} P)$ space) and Fig. 5 (S-vs-P scatter) are exactly the plots that would
have visually validated the mechanism decomposition. Skipping them means the "5/10 coverage"
line is honest but the visual mechanism claim rests only on Table 2 (numerical) and not on
Figs. 4-5 (structural).

### 4. Data-availability blocker was not resolved
The path to a full quantitative replication is known and short (WebPlotDigitizer on Krisko
& Radman 2010 Fig. 2, ~4 hours in an interactive browser). But every headless attempt to
fetch the figure binaries hit reCAPTCHA on PMC/EuropePMC and 403 on PNAS. This is a policy /
scraping-defence gap, not a scientific one. **It has been left unresolved across at least
two replication passes and is still the single unblocked lever.**

## Gaps in the model / paper itself (identified during backfill re-read)

These are things the paper does not do that a rigorous critique should demand:

### 5. Protein-damage arm identifiability was not tested
Both $K_\text{rep}$ and $X$ act on the same monotone $P(D)$ transform. Without a profile
likelihood or Fisher-information analysis, the fit may be near-degenerate along a
$(K_\text{rep}, X)$ ridge. The paper does not report profile likelihoods or the FIM
condition number, so there is no evidence the fitted values are unique. See open question Q1.

### 6. Cell-death-mode specificity is absent
$S(D)$ is a scalar viability endpoint. Apoptosis vs mitotic catastrophe vs necrosis (and in
bacteria, RecA-mediated prophage lysis vs canonical repair failure) are conflated. The
$\lambda$ IC row's structural assumption that $Q_1 \equiv 1$ (so death is *by definition*
"pure Q$_2$") is a definitional choice, not an empirical decomposition — because $\lambda$
induction is itself an SOS response downstream of DNA damage. So the paper cannot claim to
have "measured" Q$_2$-only kill; it has *assumed* Q$_2$-only kill for one row and then read
off the resulting Table 2 dominance. See open question Q2.

### 7. Low-dose behaviour is unphysical
$D \to 0$ gives $Q_2 \to 1$ and $Q_1 \to \exp(-K_\text{dam} D)$ (pure exponential, no shoulder).
Real bacterial survival curves have visible shoulders, especially in *D. radiodurans*, and
eukaryotic normal-tissue survival curves have pronounced shoulders below ~1 Gy. The model
is fit on 0-20 kGy, so this low-dose failure is *outside* its fitting range — but any
LUCID-100-style extrapolation to normal-tissue late-effect prediction (which lives entirely
in the 0.01-1 Gy range) needs to face this. See open question Q3.

### 8. No bystander term
Single-cell / single-hit multiplicative model. Cannot accommodate bystander effects, which
dominate mammalian low-dose responses. See open question Q4.

### 9. No eukaryotic scaling evidence
Interpreting $X$ as a "count of essential vulnerable protein targets" is a heuristic reading
of $P^X$. There is no cross-taxon test that would validate this — and naive scaling would
predict eukaryotic $X$ should be *larger* (bigger proteome, more targets), yet no
eukaryotic fit exists. See open question Q5.

## What did work
- The 5-equation model was transcribed cleanly from JATS XML; forward simulation is
  deterministic and passes internal consistency checks ($S = Q_1 Q_2$, monotonicity, $Q_1 = 1$
  for $\lambda$ IC).
- The dominant-mechanism map (Table 2) matches 10/10. That is a real qualitative
  replication of a real claim in the paper, even though it is somewhat inevitable given the
  paper's parameters were used as inputs.
- The blocker analysis is precise: exact missing data files are named
  (`krisko_radman_2010_F_of_D.csv`, `krisko_radman_2010_S_of_D.csv`).
- Compute + endpoint story is clean: no paid endpoints, no GPU, no PIs pinged, no data
  redistributed.

## Residual uncertainty
- I did not re-verify the JATS XML transcription line-by-line against the paper PDF in this
  backfill (the original 2026-06-09 pass did). If there is a transcription bug in
  `smoke_shuryak_2012.py`, none of these ratios can be trusted.
- I did not attempt to acquire the Krisko & Radman 2010 figure data in this backfill
  (backfill-only pass; no new science requested).
- The claim that "the ratio $\log Q_i / \log S$ is more robust than the absolute values"
  is a reasonable structural intuition but was not formally proven; it relies on the model
  being right in *form* even where $F$ is wrong in *magnitude*.

## One-line summary
Model structure is honestly replicated at the qualitative level; the quantitative claim is
not, the fitter was not re-run, three figures were not re-rendered, one bounded data-access
task remains open across multiple passes, and the queue verdict overstated the depth. Real
grade: **PARTIAL**, exactly as REPORT.md §8 already said.
