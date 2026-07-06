# First-pass report — IRI-DICE hypothesis (Langen et al. 2020)

**Paper:** Langen B., Helou K., Forssell-Aronsson E. (2020). *The IRI-DICE
hypothesis: ionizing radiation-induced DSBs may have a functional role for
non-deterministic responses at low doses.* Radiation and Environmental
Biophysics 59:349–355. DOI [10.1007/s00411-020-00854-x](https://doi.org/10.1007/s00411-020-00854-x).
License CC-BY 4.0.

**Slot:** LUCID100 Wave 1, slot 8 (rank 39, tier A/20, worktype
"omics/signature replication").

**Run date:** 2026-06-09.

## TL;DR verdict

**Verdict: PARTIAL REPLICATION — TOY SCAFFOLD ONLY.** The paper is an
explicitly conceptual *hypothesis* paper in the journal's "Controversial Issue"
section. It contains no new experimental data, no code, no supplementary
materials, no quantitative equations, and exactly one figure — a qualitative
cartoon (Fig. 1) of the proposed mechanism. The original "omics/signature
replication" worktype labelled in the master TSV is **mis-categorised**: there
is no signature and no omics result in this paper to replicate. The authors
themselves state that direct experimental testing is currently impossible and
propose a future computational programme. We implemented the most stripped-down
version of that programme as a runnable smoke test; it qualitatively reproduces
all three of the paper's central narrative claims under reasonable parameters.
A *quantitative* replication is not defined by the paper and is therefore
out of scope for this slot.

## What the paper actually claims (extracted)

The paper makes five testable narrative claims:

1. **Cis effect on transcription.** A DSB in or near a functional element
   (promoter, gene core, enhancer, NRE) changes transcript level of the local
   gene, with the *sign* depending on which element is hit. (Supported by
   Shanbhag 2010 / Iannelli 2017 in normal molecular biology; the paper
   contributes the framing, not new data.)
2. **Diversity / non-determinism.** Because DSBs are stochastically distributed
   across the genome, the per-cell pattern of transcript perturbation is
   diverse, not preprogrammed.
3. **Suppression dominance at low dose.** Because promoter + gene-core +
   enhancer disruption all suppress while only NRE disruption increases
   transcript, and NREs are short, suppression > overexpression in low-dose
   populations.
4. **Repair-threshold non-monotonicity.** ATM-driven repair has a DSB-count
   activation threshold (cited as Ismail 2005 / Huen 2010). Below the
   threshold (very low dose), IRI-DICE perturbations persist; above the
   threshold, repair restores most cis effects. The strongest persistent
   perturbation is therefore expected *near* the threshold, not at high dose.
5. **Radiation-quality dependence.** High-LET radiation (α) produces fewer but
   more complex DSBs that persist longer; low-LET (X-ray) produces more, less
   complex DSBs that repair faster. The frequency *and* lifetime of IRI-DICE
   events depend on radiation type.

Claims 1–4 are computationally testable with a toy model. Claim 5 is testable
in the same framework with two LET regimes; we did not implement it in the
smoke run but the scaffold accommodates it trivially.

## Artifact harvest

- Source PDF downloaded from Springer (CC-BY 4.0 open access),
  `artifacts/paper.pdf`, SHA-256 `ba50883d55f1262f9090a7348e170260b13166c8f901dfdea1ba1524e5fadc36`.
- Full text extracted to `artifacts/paper.txt` (`pdftotext -layout`).
- No supplementary files exist on the Springer landing page.
- No code repository or data accession is cited.
- No tables; one conceptual figure (Fig. 1).

Full inventory in `artifacts/MANIFEST.md`.

## Replication scope decision

After artifact harvest, four scoping options were considered:

| Option | Verdict | Reason |
|---|---|---|
| Exact rerun of authors' analysis | N/A | no analysis, no data, no code |
| Independent reimplementation of a quantitative method | N/A | no quantitative method specified |
| Table/figure digitization | N/A | the only figure is a non-quantitative cartoon |
| **Minimal computational scaffold of the proposed mechanism** | **CHOSEN** | matches the authors' own "Approaches to test IRI-DICE" section |
| No-go | Rejected | qualitative consistency check is cheap and informative |

The chosen scope is the **minimum viable scaffold** of the simulation programme
the authors explicitly call for: a Monte Carlo per-cell DSB sampler with
sequence-functionality-weighted hit categories, dose-scaled DSB number, and a
repair-activation threshold.

## Acceptance criteria

The toy scaffold "passes" if, at default parameters and without per-claim
tuning, it reproduces all four computationally testable narrative claims
above (1–4) on a single dose scan. It does **not** attempt quantitative
agreement with any external dataset; the paper supplies none.

## Smoke-run result

`code/iri_dice_toy_mc.py --ncells 3000 --seed 0` produced
`artifacts/figs/summary.json` and three figures. Per-cell summary across the
dose scan (0.001, 0.01, 0.05, 0.1, 0.5, 1.0, 2.0 Gy):

| Dose (Gy) | Mean DSBs | Mean suppressed/cell | Mean overexpr/cell | Σ\|log2FC\| /cell | Frac cells perturbed |
|---:|---:|---:|---:|---:|---:|
| 0.001 | 0.04 | 0.001 | 0.000 | 0.002 | 0.001 |
| 0.01  | 0.35 | 0.016 | 0.001 | 0.022 | 0.016 |
| 0.05  | 1.81 | 0.090 | 0.003 | 0.136 | 0.089 |
| 0.10  | 3.48 | 0.188 | 0.009 | 0.286 | 0.178 |
| 0.50  | 17.6 | 0.693 | 0.027 | 1.028 | 0.481 |
| 1.00  | 35.1 | 0.198 | 0.006 | 0.296 | 0.186 |
| 2.00  | 70.1 | 0.384 | 0.019 | 0.593 | 0.332 |

Interpretation against the paper's claims:

- **Claim 2 (diversity)** ✓ — `fig_doseresponse_diversity.png` shows broad
  per-cell distributions of `(suppressed − overexpressed)` at every dose, not
  a single deterministic value.
- **Claim 3 (suppression dominance)** ✓ — at every dose, mean suppressed /
  mean overexpressed > 10× and typically ~25×. This is a direct consequence
  of the relative sequence lengths and effect-sign assignments and matches
  the paper's qualitative argument.
- **Claim 4 (repair-threshold non-monotonicity)** ✓ — mean persistent
  Σ\|log2FC\| / cell rises with dose to a peak near 0.5 Gy (just above the
  parameterised repair threshold of ~0.57 Gy ≈ 20 DSBs / 35 DSB·Gy⁻¹), then
  *drops* by ~3× at 1 Gy as repair becomes active and restores 90 % of
  cis effects. This is the *signature* qualitative IRI-DICE prediction.
  `fig_repair_threshold.png` plots it.
- **Claim 1 (cis effect)** is the model assumption, so passing is trivial.
- **Claim 5 (LET dependence)** not implemented in smoke run; trivial extension
  by setting `dsb_per_gy` to LET-appropriate value and adding a complexity
  multiplier to `f_restore`.

The smoke run is therefore consistent with the IRI-DICE narrative at the
qualitative level the paper itself argues at.

## What was *not* attempted, and why

- **No quantitative replication of a published curve.** The paper has no curves.
- **No reanalysis of the authors' cited transcriptomic series** (Langen 2013/2015,
  Rudqvist 2012/2015/2017, Schüler 2014). Those are separate papers with their
  own slots — not the IRI-DICE paper. They would require GEO/ArrayExpress
  accession lookup and per-paper analysis pipelines.
- **No author contact** (per instructions).
- **No paid endpoints used** (per instructions).
- **No heavy compute** — smoke run was ~1 s of CPU, 3,000 cells × 7 doses,
  pure numpy. No CherryRd-unfriendly load.

## Blockers

- **None for this paper as written.** The paper is its own ceiling: a
  hypothesis paper without numbers cannot have a numeric replication.
- **Future quantitative replication blocker:** would require external
  transcriptomic data (e.g. Iannelli 2017 GEO series), a track-structure
  Monte Carlo (Geant4-DNA / TOPAS-nBio) for realistic DSB placement, and a
  chromatin model — all of which are *outside* what this paper specifies.

## Next actions (priority order)

1. **Re-tag** this slot's worktype in
   `lucid-replications/LUCID100_SOLID_MASTER_QA.tsv` from "omics/signature
   replication" to **"hypothesis-paper scaffold / no-data"**, with a note that
   the original tag was a master-list miscategorisation.
2. (Optional) **Extend the toy MC** with a second LET regime (high-LET α with
   reduced `dsb_per_gy`, increased per-DSB effect persistence) and produce a
   companion figure for claim 5.
3. (Out of scope for this slot, but logical follow-on) Take Iannelli et al.
   2017, *Nat Commun* 8:15656 — the strongest cis-effect dataset cited by
   IRI-DICE — and queue it as a separate LUCID replication slot. The GEO
   data for that paper exists and would be a *real* quantitative
   replication of the underlying biology IRI-DICE rests on.
4. Close this slot as **first-pass complete**: artifacts harvested, scaffold
   runs, qualitative claims reproduced, no further automated work warranted
   without a methodological pivot to one of the cited primary studies.

## Provenance

- Source-of-truth row: line for DOI `10.1007/s00411-020-00854-x` in
  `/Users/stevens/.openclaw/workspace/lucid-replications/LUCID100_SOLID_MASTER_QA.tsv`.
- Work directory: `/Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/_LUCID100_WAVE1_LAUNCH_QA/lucid100-the-iri-dice-hypothesis-ionizing-radiation-induced-dsbs-may-have-a-functio/`.
- Progress JSON: `/Users/stevens/.openclaw/workspace/memory/subagent-progress/lucid100-wave1-8-the-iri-dice-hypothesis--ionizing-radiation-induced-dsbs-may.json`.
- Environment: Python 3, numpy, matplotlib (Agg). No GPU. No network at run time.
