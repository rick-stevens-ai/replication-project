# Failure Analysis — lucid-mcmahon-2016-medras-original

**Verdict this critiques:** REPLICATED (COVERAGE=9/10, AGREEMENT=10/10)

The paper reproduces cleanly — but "clean" is not "complete", and a
REPLICATED verdict earned by re-running the authors' own code against
the authors' own data is a **weaker** form of replication than an
independent re-derivation. This document is the honest critique of what
this audit did **not** do, where it took the paper's word, and what
residual uncertainty remains. It is written to be readable by a hostile
reviewer looking for the weakest joint.

---

## 1. What the audit actually proved

- The **authors' shipped code**, ported to Python 3 with three textual
  edits, produces **bit-stable** parameter values that fall within the
  paper's Table 1 ±1σ intervals (11/11) and regenerates 6 of 8 figures
  as TSV curves.

- That's it.

The audit did **not** independently implement the model from the SI
equations, did **not** re-collect the input data, did **not** re-derive
the geometry constants A and B from an independent Monte Carlo, and did
**not** stratify residuals by cell line or dose.

## 2. Genuine weaknesses (ranked by how much they weaken the verdict)

### 2.1 Fig. 7 — the paper's headline validation number is unaudited

Fig. 7 is the paper's main **out-of-sample** sanity check: observed vs.
predicted mean-inactivation-dose (MID) across all cell lines with R² =
0.91 (G1) and 0.96 (G2). This is the number the abstract and Discussion
lean on when arguing the model generalises beyond the fit.

**This audit did not recompute those R² values.** The regenerated
survival TSV contains everything needed (per-cell-line predictions on
the observed doses), but the observed-vs-predicted scatter and its
regression were not assembled. The R² = 0.91 / 0.96 headline is
therefore **structurally bracketed**, not verified. This is open
question #1 and it is the single biggest gap.

**If this failed on re-audit**, it would materially change the verdict:
a "we reproduce Table 1 but not Fig. 7" outcome is a different story
from a clean REPLICATED. Right now we cannot rule it out.

### 2.2 The A, B geometry constants are inherited on faith

Every fitted Table-1 parameter was obtained with A = 0.757 and B = 5.39
held fixed at the values the paper pins from an independent 2016 Monte
Carlo run (SI Fig. S2). **That MC code is not in the supplementary
archive.** If the 2016 MC had a bug, or fit the ω(R,σ) functional form
to the wrong dataset, every downstream parameter is silently shifted.

This audit did nothing to test A or B. The verdict is genuinely
conditional on trusting the authors' unpublished 2016 MC. See open
question #2.

### 2.3 Fit uncertainties are known-underestimates and we relied on them anyway

SI §S5 explicitly says the covariance-matrix ±1σ intervals may
underestimate true uncertainty **"by a factor of a few"** due to an
ad-hoc 5% data-extraction inflation.

**Our "within ±1σ" verdict for all 11 parameters lives inside this
optimistic envelope.** If the true ±1σ were 2–3× wider, the verdict
would still be within-error, but the specific claim "matches the
published Table 1 uncertainty" becomes trivially true (any answer would
match a wider envelope). A profile-likelihood or MCMC re-analysis would
give honest intervals; this audit did not do that.

### 2.4 The high survival χ²/N = 16.3 is un-interrogated

We accepted the paper's framing ("clonogenic survival has large
inter-experimental variance"). But χ²/N = 16.3 vs. DNA χ²/N = 1.34 is a
12× ratio. If the misfit is uniform noise, the paper is right; if it is
concentrated in a subset of cell lines, that concentration would
identify a specific missing mechanism (e.g. cell-line-specific HR
competence, apoptosis threshold, or DSB-yield scaling).

**We did not stratify.** See open question #3.

### 2.5 Non-identifiability of the 11-parameter fit not tested

With 11 parameters against heterogeneous data, some pairs are likely to
be strongly correlated — candidates include p_c ↔ p_fail (both control
the fraction of breaks going to slow/fallback branches), λ_S ↔ λ_M (both
are slow-branch rates), and σ ↔ (A, B) (all three set misrepair
geometry). If any pair trades off along a ridge, the point-estimate
table hides a lower true dimensionality and the mechanistic
interpretation of each parameter is weaker than it looks.

**We did not compute the covariance matrix off-diagonals, run profile
likelihood, or run MCMC.** See open question #4.

### 2.6 Per-cell-line coverage is aggregate, not stratified

All 11 cell lines in SI Table S1 enter the global fit and appear in the
regenerated TSV. But we never computed per-line goodness-of-fit, so we
cannot tell whether the fit is genuinely joint across lines or whether
one or two dominate. Related: the paper's "G2 rescue" causal claim (2.4×
resistance in G2 over G1 for NHEJ-defective cells) was verified from the
**model's own predictions**, not from the raw per-line data (open
question #5). Confirming the model reproduces its own prediction is
weaker than confirming the underlying biological claim.

## 3. Reproducibility friction (documented, not fixed upstream)

None of these change the verdict, but they made the audit harder than
it should have been and would trip up a naïve re-doer:

- **Python 2.7-only source in 2026.** Three-line port is trivial once
  you know it, but a fresh reader has to notice and fix `xrange`,
  `print`, and one `map()` before anything runs.

- **No internal manifest in the supplementary ZIP.** No
  `SHA256SUMS`, no `MANIFEST`, no `requirements.txt`. `unzip` on macOS
  silently truncated the file list on our first attempt; we caught it
  only because we ran `unzip -l` first as a ground-truth check.
  A future auditor without that habit would miss files silently.

- **Cell-line index → citation map is implicit.** SI Table S1 lists the
  11 cell lines with their primary references, but
  `Full Survival Data Sets.csv` uses a numeric cell-line index column
  without inline citations. Fine for numeric reproduction, blocking for
  any downstream re-curation.

- **No dependency pinning.** We confirmed the fit is stable across
  numpy 2.4.x and scipy 1.17–1.18, but a pinned `requirements.txt`
  would make bit-exact reproduction future-proof.

## 4. What this audit does **not** claim

- Does **not** claim the model equations in the SI are correct — we
  ran the code, not the equations.
- Does **not** claim the input datasets (`Full DNA Data Sets.csv`,
  `Full Survival Data Sets.csv`) are correctly extracted from the
  primary literature — we accepted them as given.
- Does **not** claim the geometry constants A, B are correct — see 2.2.
- Does **not** claim the parameter uncertainties are honest — see 2.3.
- Does **not** claim the model's Fig. 7 R² = 0.91/0.96 holds — see 2.1.

## 5. What would change the verdict

The current verdict is REPLICATED at 9/10 coverage. To push to 10/10 or
to demote below REPLICATED, in order of probable impact:

| Change | Likely direction | Owner-effort |
|---|---|---|
| Fig. 7 R² recomputation fails materially | ⬇ (would demote) | ~1 day: parse observed MIDs, regress against predicted |
| A/B re-derivation from Medras-MC 2021 shifts fitted parameters outside ±1σ | ⬇ (would demote) | ~3 days: run MC, re-fit, compare |
| MCMC widens intervals but all 11 still within | neutral | ~2 days |
| MCMC finds strongly bimodal/ridged posterior | ⬇ (weakens mechanistic story) | ~2 days |
| Per-line residual stratification finds one dominating line | neutral–⬇ (adds a caveat) | ~4 hours |
| Fig. 7 R² recomputation succeeds | ⬆ (would promote to 10/10) | ~1 day |

## 6. Bottom line

REPLICATED is the correct verdict on the evidence gathered. But the
verdict rests substantially on the authors' generosity (shipping code +
data + a detailed SI), not on the depth of this audit. Five concrete
audits (open questions #1–#5) would materially strengthen or weaken the
verdict; none has been done.

This document is meant to be read alongside `open_questions.json` and
`report/REPORT.tex`'s `\ref{sec:critique}` section — same limitations,
different audiences.
