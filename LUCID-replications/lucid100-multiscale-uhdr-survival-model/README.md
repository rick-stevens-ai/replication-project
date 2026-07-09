# LUCID100 slot 65 — MS-GSM² multiscale UHDR cell-survival model

**Paper.** Battestini M., Missiaggia M., Bolzoni S., Cordoni F. G., Scifoni E.,
*A multiscale radiation biophysical stochastic model describing the cell
survival response at ultra-high dose rate*, **arXiv:2412.16322 [physics.bio-ph]**,
v1 posted 2024-12-20. No journal DOI yet.

**LUCID100 master row.** Slot 65, Wave 4, status `candidate_curated`,
type `simulation/model replication`.

**This folder.** `~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-multiscale-uhdr-survival-model/`.

## Bibliographic identity (verified)

- **Title:** A multiscale radiation biophysical stochastic model describing the cell survival response at ultra-high dose rate
- **Authors:** M. Battestini¹², M. Missiaggia²³, S. Bolzoni¹², F. G. Cordoni²⁴*, E. Scifoni²*
  (¹ Department of Physics, Univ. of Trento; ² TIFPA-INFN, Trento;
   ³ Univ. of Miami Miller School of Medicine; ⁴ DICAM, Univ. of Trento; * equal contribution)
- **Preprint:** arXiv:2412.16322v1 (2024-12-20), `physics.bio-ph`
- **Semantic Scholar:** paperId `e5c1ab5e67dbdb35bc6c0aea222926d1f6de0653`, CorpusId 274982107
- **Journal DOI:** **none yet** — preprint only as of 2026-06-09. Likely venue (per Battestini's 2023 predecessor) is Frontiers in Physics.
- **Predecessor (companion / preliminary version):** Battestini et al. 2023, *Across the stages: a multiscale extension of the generalized stochastic microdosimetric model (MS-GSM²) to include the ultra-high dose rate*, Frontiers in Physics 11.

## Model summary (what we are replicating)

MS-GSM² is a **multi-stage extension of GSM²** (Cordoni, Missiaggia et al. 2021)
that couples three physical/chemical/biological scales:

1. **Physical stage** — track-structure energy deposition events from a beam
   with prescribed mean dose D and mean dose rate Ḋ. Events arrive as
   exponentially-distributed inter-arrival times; per-event specific energy z
   is sampled from a microdosimetric spectrum. Nd=52 sub-domains per cell
   nucleus.
2. **Chemical stage** — 9-reaction radiolysis network in 5 ODEs over species
   `[O₂, H₂O₂, OH•, R•, ROO•]`, with literature rate constants k₁..k₉
   (paper Table TAB:chempar) and TRAX-CHEM-derived G-values. Substrate
   pools `[RH], [Fe²⁺], [XSH=GSH], [catalase]` held fixed.
3. **Biological / bio-chemical stage** — GSM² stochastic Markov chain on
   (X = sub-lethal lesions, Y = lethal lesions):
   - `X → ∅` rate `r` (repair)
   - `X → Y` rate `a` (sub-lethal → lethal)
   - `2X → Y` rate `b` (pairwise clustering → lethal)
   Lesion induction is split into direct + indirect, where indirect yield is
   modulated by `ϱ ∫₀ᵗ [ROO•](s) ds` (paper Eq. 7), normalised to 1 at
   conventional dose-rate + 21% O₂ (paper "Computational information" section).

Cell survival: `SF = Pr( lim_{t→∞} Y^(d)(t) = 0 for all d=1..Nd )` (paper Eq. 8).

Three biological-rate fits given (paper Table TAB:biorates):
| Experiment | Reference | a [1/h] | b [1/h] | r [1/h] |
|------------|-----------|---------|---------|---------|
| DU145, e⁻ | Adrian 2020 | 7.82e-3 | 1.83e-2 | 3.23 |
| A549, ⁴He | Tessonnier 2021 | 4.70e-3 | 1.34e-2 | 4.51 |
| CHO-K1, ¹²C | Tinganelli 2022a | 4.21e-3 | 2.43e-2 | 3.68 |

## Code & data availability (in the paper)

> *"All the simulations, the data fitting, and analyses reported in this work
> were performed using Julia"* — but **no public repository is cited**.
> *"The raw data supporting the conclusions of this article will be made
> available by the authors without undue reservation."*

GitHub search for `fcordoni`, `Battestini`, `2MaBa`, `MS-GSM2`, `GSM2 microdosimetric`
returns zero MS-GSM²/GSM² source repositories as of 2026-06-09. The Julia
implementation is **closed**.

**What we DO have** (sufficient for first-pass smoke):
- Full chemical ODE (Eq. 2) with all 9 rate constants and initial concentrations (Table TAB:chempar)
- Full biological Markov chain (Eq. 6)
- All three biological-rate fits (Table TAB:biorates)
- Complete SSA pseudocode (Algorithm "MS-GSM²" in arxiv source)
- Reference list (Research_mathematics.bbl)
- All paper figures as PDFs in the arXiv source tarball

## Replication scope (this first pass)

**Verdict — see `reports/FIRST_PASS_REPORT.md`:** *GO — smoke-only, mechanism reproduced; full bit-exact replication blocked by closed Julia code and unreleased raw experimental data.*

### What was implemented
- `code/smoke_ms_gsm2.py` — Python/SciPy port of:
  - The 5-ODE chemical network with BDF (stiff) integrator
  - The GSM² biological-stage Gillespie SSA (Eq. 6 reactions)
  - A coupling layer that normalises the per-Gy ROO• exposure to 1 at the
    paper's reference (conventional, 21% O₂) and uses it to scale indirect
    lesion induction.
  - 52-domain split with independent-domain product approximation for SF.

### What was NOT implemented (deferred / out-of-scope for smoke)
- Track-structure-derived microdosimetric specific-energy spectra (paper uses
  amorphous track models + TRAX-CHEM); we substituted average-yield Eq. (3)
  with literature `DSB_per_Gy` and an analytic OER.
- Cross-entropy optimisation of (a, b, r) on raw experimental clonogenic data
  (raw data not released; authors retain).
- Per-domain SSA with full chemical environment per domain (we run chemistry
  once per (D, dose-rate, [O₂]) cell-average; this is the headline simplification).
- TRAX-CHEM G-values; we use standard literature G(OH)=2.5, G(H₂O₂)=0.7,
  G(R•)=2.6 #/100eV.

### Smoke result (qualitative replication)

Grid: D ∈ {1, 2, 5, 8, 10, 15, 20} Gy ; Ḋ ∈ {0.1, 100} Gy/s ; [O₂] ∈ {21, 1}%.

The peroxyl-radical integral ∫[ROO•] dt is **systematically lower** under UHDR
than CONV at every (D, [O₂]) tested, and **drastically lower** at 1% O₂ than at
21% O₂ — both of which are the qualitative signatures the paper claims drive
the FLASH sparing effect.

The cell survival fraction declines monotonically with dose (e.g. SF drops from
≈1 at 1 Gy to ≈0.39 at 20 Gy / 1% O₂), and the FLASH-sparing ratio
`SF_UHDR / SF_CONV > 1` appears in the expected regime (highest at 15 Gy /
1% O₂, ratio ≈ 1.17, ≈17% sparing).

Full results: `results/smoke_results.csv`, `results/smoke_results.png`,
`results/smoke_chem_trace.csv`.

## How to reproduce

```bash
cd ~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-multiscale-uhdr-survival-model
python3 code/smoke_ms_gsm2.py
# outputs to results/
```

Requires: Python ≥3.10, numpy, scipy, matplotlib. No GPU. Wall time ≈ 30 s on
CherryRd; no heavy compute.

## Folder layout

```
.
├── README.md                      <- this file
├── PROGRESS.md                    <- task progress log
├── artifacts/MANIFEST.md          <- hashes/sizes of all artifacts
├── code/smoke_ms_gsm2.py          <- Python smoke replication
├── data/                          <- empty (no released raw data)
├── refs/
│   ├── arxiv-2412.16322.pdf
│   ├── arxiv-2412.16322.txt       <- pdftotext extract
│   ├── arxiv-2412.16322-src.tar.gz
│   └── arxiv-src/                 <- extracted LaTeX + figures
├── reports/
│   ├── FIRST_PASS_REPORT.md       <- main verdict + numbers
│   └── REPORT.md                  <- same content, canonical name
└── results/
    ├── smoke_results.csv
    ├── smoke_results.png
    └── smoke_chem_trace.csv
```

## Relation to other LUCID100 slots

- **Slot 27** (Cordoni 2023, Entropy, `lucid-stochastic-poisson-dna-damage/`) —
  REPLICATED earlier; that paper is the system-size expansion of GSM². The
  *biological* core (X, Y, a, b, r) is identical to MS-GSM², so this slot
  re-uses the SSA logic conceptually.
- **Slot 27 / Wave 3** (Liew 2021, IJROBP, `lucid-flash-time-dependent-dna-damage/`
  if present) — SMOKE-ONLY with dynamic-UNIVERSE; same FLASH-sparing
  qualitative target. MS-GSM² is a *more mechanistic* model targeting the same
  phenomenon from a different angle (chemistry-driven indirect damage rather
  than oxygen-depletion + repair-time dynamics).

## QA / bibliographic correction

- TSV row needs **DOI populated**: currently empty (`""`); preprint is
  arXiv:2412.16322. Recommend setting DOI cell to `arXiv:2412.16322` or
  leaving empty + adding URL `https://arxiv.org/abs/2412.16322`.
- TSV row needs **venue populated**: currently empty; should be
  `arXiv:2412.16322 [physics.bio-ph] (preprint)`.
- Outcome retag suggestion: **`smoke_only_go`** (chem+bio mechanism
  reproduced from open paper parameters; bit-exact comparison blocked by
  closed Julia code + unreleased raw data). Comparable to slot 27 (Liew 2021).
