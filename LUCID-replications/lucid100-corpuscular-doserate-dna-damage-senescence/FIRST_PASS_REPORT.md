# FIRST PASS REPORT — LUCID100 slot 58

**Paper:** Soroko et al. 2024, *Curr. Issues Mol. Biol.* 46(12):13860-13880
**DOI:** [10.3390/cimb46120828](https://doi.org/10.3390/cimb46120828)
**PMC:** PMC11726848 (CC BY 4.0)
**Worker:** Ollie sub-agent on CherryRd · **Date:** 2026-06-09

---

## Verdict

**GO_LIGHT / KEEP-DONE-LIGHT — analytical smoke replication complete.**
**Worktype RETAG recommended** (master TSV → wet-lab radiobiology, not
simulation).

## What was harvested

| Artifact | Path | Provenance |
| --- | --- | --- |
| Paper PDF | `artifacts/paper.pdf` (4.03 MB, 10 p.) | EuropePMC `ptpmcrender.fcgi` |
| Paper full text | `artifacts/paper.txt` | `pdftotext -layout` |
| Paper JATS XML | `artifacts/paper.xml` | `eutils efetch` |
| 7 figure JPEGs (Figs 1–7) | `figures/cimb-46-00828-g00{1..7}.jpg` | NCBI OA tarball |
| Supplement PDF + ZIP | `artifacts/cimb-3305746-supplementary.pdf`, `artifacts/supplement.zip` | NCBI OA tarball |
| Supplement text | `artifacts/supplement.txt` | `pdftotext` |
| NCBI OA tarball | `artifacts/pmc_package.tar.gz` (4.45 MB) | `ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/deprecated/oa_package/6c/f3/PMC11726848.tar.gz` |
| Per-file manifest with sha256 | `artifacts/artifact_manifest.json` | this run |
| In-text numerical extraction | `data/digitized_values.json` | this run |

No author code or numerical data tables exist publicly — the Data
Availability Statement is *"included in the article"* only.

## Worktype audit

| Field | Master TSV | Recommended |
| --- | --- | --- |
| `worktype` | `simulation/model replication` | **`wet-lab radiobiology assay (dose-rate effect study)`** |

The paper is unambiguously experimental: A431 carcinoma cells, irradiation
on a Novalis Tx LINAC (6 MeV e⁻) and ⁹⁰Sr+⁹⁰Y sealed beta sources, with
seven wet-lab readouts (MTT, fluorescent counting, clonogenic, comet,
PI/AnnV flow, SA-β-gal, DCFH₂DA ROS, giant-cell morphology). Themes
"computational model / simulation" should be dropped; keep "dose-rate /
low-dose response", "radiation quality / RBE", "senescence".

## Light analytical replication — what we tried, what worked

The only public numerical handles are the in-text **anchor points**:

```
HDR (600 Gy/h, 6 MeV e⁻):  LD50 = 3.4 Gy,   D37 ≈ 8 Gy
LDR (0.25–3 Gy/h, β, 24 h): LD50 = 10.8 Gy, D37 ≈ 20 Gy
comet tail %, 4 Gy:        HDR 5 vs LDR 3   (LDR/HDR = 0.60)
comet tail %, 8 Gy:        HDR 8 vs LDR 4   (LDR/HDR = 0.50)
```

### Model 1 — Linear-Quadratic + Lea–Catcheside (the textbook biophysics)

Survival `SF(D) = exp(-α D - G β D²)`, with the Lea–Catcheside protraction
factor `G(t, μ) = 2 / (μ t)² · (μ t − 1 + e^{−μ t})` for a uniform 24-h
LDR exposure and single-exponential sublethal-damage repair rate `μ`.

Solving for `(α, β)` exactly through the two HDR anchors:

```
α_HDR = 0.262 /Gy
β_HDR = −0.0171 /Gy²     ← negative; LQ shoulder is upward, not downward
α/β   = −15.3 Gy (uninterpretable)
```

The negative β is the smoking gun: a drop from `SF=0.5` at 3.4 Gy to
`SF=0.368` at 8 Gy is a **1.36× decrease across a 2.35× dose increase**,
which is *much shallower* than even a pure exponential `exp(−α D)`, let
alone a curve with a downward LQ shoulder. This is consistent with the
authors' own caveat that **MTT readouts at 72 h conflate cell number,
metabolic activity per surviving cell, and cell-cycle arrest**, and so do
not behave like clonogenic survival.

If we ignore that and try to find the single `t½` that under shared
intrinsic LQ would predict the LDR LD₅₀ and D₃₇, the optimizer rails into
the boundary at `t½ = 0.1 h` (`G ≈ 0.012`) and still under-predicts the
LDR LD₅₀ (2.6 Gy vs observed 10.8 Gy). **The single-LQ + protraction
picture is biophysically falsified by this dataset.**

### Model 2 — Hill / log-logistic descriptive fit (what actually fits)

`V(D) = 1 / (1 + (D / LD50)ⁿ)` with two anchors fixes both `LD50` and `n`:

| Regime | LD₅₀ (Gy) | Hill `n` |
| --- | --- | --- |
| HDR | 3.4 | 3.59 |
| LDR | 10.8 | 5.18 |

This reproduces *both* anchors per regime exactly, and the **dose-modifying
factor at 50 % viability is the clean empirical ratio
`DMF₅₀ = 10.8 / 3.4 = 3.18`**, matching the paper's headline "≈3× sparing".

### Model 3 — Independent comet-tail consistency check

If the LDR/HDR comet ratio of ~0.55 at equal physical dose is dominated by
break rejoining *during* the 24-h LDR exposure, the end-of-exposure
residual-break fraction `f_res = (1 − e^{−μ t}) / (μ t)` would have to
have

```
f_res = 0.55  ⇒  t½ ≈ 12 h
```

This is **slow-component** kinetics (typical fast DSB rejoining is 0.3–1.5 h;
slow component 4–8 h). The survival fit prefers `t½ → 0`. The two
endpoints are pointing at different physical regimes, so it's wrong to
fold them into a single repair half-time.

## Smoke outputs

- `outputs/fig_lq_survival.png` — LQ fit on log-survival axes, both
  anchor pairs annotated; visually shows the LQ shoulder is *upward* under
  the two-point fit.
- `outputs/fig_drmf_vs_repair.png` — predicted LDR/HDR isoeffective-dose
  ratio vs `t½`, overlaid with the observed values; demonstrates that no
  single `t½` matches both LD₅₀ and D₃₇ DRMFs under a shared LQ.
- `outputs/fig_comet_ratio.png` — residual-break fraction vs `t½`; the
  observed 0.55 sits at `t½ ≈ 12 h`.
- `outputs/fig_hill_mtt.png` — Hill fit cleanly reproduces both regimes.
- `outputs/smoke_summary.json` — full numbers, sweep, ratios, machine-readable.

## What you can defensibly claim from this replication

1. **Empirical 3× sparing factor confirmed as a trivial ratio.** This is
   robust and does not depend on any model.
2. **The MTT survival data alone do not admit a sensible LQ fit.** Future
   replications wanting a biophysical model need the authors' clonogenic
   numbers, not the MTT numbers.
3. **The comet-tail ratio is independently consistent with break
   rejoining on a ~12-h timescale**, in the slow-DSB-repair range.
4. **The qualitative HDR-only signatures** (G2/M arrest, giant cells,
   higher ROS at lower dose) **are not reproducible from text alone** —
   they need access to flow-cytometry raw data and microscopy.

## What you cannot get without the wet lab or the authors

- Cell-cycle distribution time-courses (Fig 4B,C numerics)
- Annexin V / PI population fractions (Fig 5B,C numerics)
- ROS DCF fluorescence intensities (Fig 6 numerics)
- Giant-cell counts (Fig 7 numerics)
- SA-β-gal staining intensities (Fig 5E numerics)

These are not in the supplement; they exist only as bar charts inside the
PDF figures.

## Cost / compute footprint

| Resource | Used |
| --- | --- |
| Network egress | ~9 MB (PDF + tarball + supplement) |
| Local CPU | < 1 s for the smoke; pdftotext + tar dominate |
| GPU / HPC | none |
| Disk | ~ 10 MB total in the workdir |

CherryRd safe. No heavy compute needed for any future expansion of this
replication unless full Monte-Carlo track-structure simulation is pursued
(out of scope and unnecessary for the headline claim).

## Recommendation to LUCID100 QA

1. **Apply worktype retag** on master TSV row 89:
   `simulation/model replication` → `wet-lab radiobiology assay (dose-rate
   effect study)`.
2. **Mark verdict** `KEEP-DONE-LIGHT` (do not promote to a full replication
   without wet-lab access or author data).
3. Optionally cross-link this slot with the Wave-6 / Wave-7 dose-rate /
   DSB-repair model cluster (slots 57, 59, 62, 63) since the Lea–Catcheside
   smoke could be reused there.
