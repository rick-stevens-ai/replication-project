# LUCID XFER New-20 Replication Summary — 2026-05-30

Source folder: `~/Dropbox/XFER/LUCID-replication-targets/`

This summary covers the 20 PDFs added after the first 10-paper LUCID batch. The original 10 were already completed earlier and are not counted here.

## Headline

- **20/20 new PDFs accounted for**
- **0 active subagents remaining**
- **20/20 have deliverables** (`REPORT.md` or `NO-GO-REPORT.md` plus progress artifacts)

Verdict breakdown:

- **REPLICATED:** 6
- **PARTIAL / PARTIAL-REPLICATED / PARTIAL strong:** 10
- **SPOT-CHECK:** 1
- **NO-GO:** 3

## Per-paper table

| Hash | Slug | Verdict | Coverage | Agreement | Notes |
|---|---|---:|---:|---:|---|
| `00f21513` | `lucid-h2ax-phosphorylation-review-triage` | NO-GO | N/A | N/A | Narrative review; no model/table/meta-analysis. |
| `0d005b82` | `lucid-fukui-saga-lq-sldr-aldh` | PARTIAL | 7/10 | 8/10 | LQ+SLDR / IMK survival refit; headline `w_SLDR` reproduced. |
| `12b37ba3` | `lucid-grandt-fibroblast-rnaseq` | PARTIAL strong | 8/10 | 9/10 | DEG/pathway claims from supplementary tables replicate strongly; no raw FASTQ. |
| `2c94a157` | `lucid-bnct-radioresistant-hcc` | PARTIAL | 5/10 | 8/10 | RBE/D10 arithmetic and LQ gamma refit replicate; wet-lab mechanism panels not reproducible. |
| `367ea049` | `lucid-cu64-topas-nbio-lethal-damage` | PARTIAL | 5/10 | 10/10 | Eq. 1 → Table 2 reproduced; full TOPAS-nBio/Geant4-DNA blocked. |
| `45fb7c48` | `lucid-pariset-53bp1-mouse-strains` | PARTIAL | 6/10 | 8/10 | Key `r=-0.75` claim reproduced as `r=-0.758`; raw foci/survival data absent. |
| `53c00a02` | `lucid-spatiotemporal-early-dna-damage` | REPLICATED | 7/10 | 8/10 | Early DDR ODE network reproduced from supplement. |
| `555f0ea0` | `lucid-franken-alpha-gamma-rbe` | PARTIAL | 6/10 | 10/10 | RBE arithmetic and uncertainty propagation exactly reproduce; no raw dose-response data. |
| `58db87da` | `lucid-dsb-repair-history-review-triage` | NO-GO | N/A | N/A | Historical/narrative review; no original data/model. |
| `6faf169c` | `lucid-ulyanenko-gammah2ax-patm-msc` | REPLICATED | 8/10 | 9/10 | Published tables algebraically recover foci counts; regressions match to ≥3 decimals. |
| `775336cd` | `lucid-actinium-lutetium-dose-effect` | PARTIAL / SPOT-CHECK | 6/10 | 7.5/10 | Linear dose-effect/RBE refit good; Geant4/wet-lab/raw data not replicated. |
| `7dfb04b2` | `lucid-staaf-mixed-beam-gamma-h2ax` | PARTIAL / REPLICATED | 7/10 | 7/10 | RBE/additivity/large-foci delay recovered from digitized figures. |
| `836900da` | `lucid-nuclear-matrix-uv-repair-triage` | NO-GO | N/A | N/A | Pre-modern wet-lab autoradiography/Southern blot; no data/model. |
| `909f825a` | `lucid-skin-inflammation-nfkb-cox2` | SPOT-CHECK | 3/10 | 9/10 | Wet-lab paper; digitized/recomputed selected ANOVA/dose-response/PGE2 checks. |
| `aa68c63a` | `lucid-patra-polbeta-radiosensitivity` | PARTIAL | 5/10 | 7/10 | Survival claim survives; sequence/docking story has serious inconsistencies. |
| `c039ec1f` | `lucid-hsgc-c5-repair-performance` | REPLICATED (TLK portion) | 6/10 | 9/10 | Open MDPI supplement; TLK/foci/survival curve-fit reproduced. |
| `c716b571` | `lucid-mariotti-split-dose-gamma-h2ax` | REPLICATED | 7/10 | 9/10 | Analytical split-dose gamma-H2AX model + supplement parameter table reproduced. |
| `c71a2c0c` | `lucid-turner-gamma-h2ax-biodosimetry` | REPLICATED | 9/10 | 9/10 | Biodosimetry model and validation correlations reproduce strongly. |
| `cf734521` | `lucid-dna-repair-kinetics-doserate-rbe` | PARTIAL | 6/10 | 9/10 | Photon-side UNIVERSE repair/dose-rate submodel reproduces; FLUKA/HIT ion side closed. |
| `eecae73a` | `lucid-autofoci-detection` | REPLICATED | 8/10 | 9/10 | Public code/data; independent OEP implementation matches paper. |

## Notable findings

1. **Best clean replications:** Turner biodosimetry, AutoFoci, Ulyanenko foci regressions, HSGc-C5 TLK, Mariotti split-dose, Spatiotemporal early DDR ODE.
2. **Strong partials:** Grandt RNA-seq, Fukui/Saga LQ-SLDR, Liew UNIVERSE photon repair/dose-rate, Staaf mixed-beam, Cu64 lethal-damage analytic chain.
3. **Real red flag:** Patra Polβ paper — central radiosensitivity survives, but the cDNA/protein deletion story appears internally inconsistent and docking scores are mis-described as kcal/mol.
4. **Review/wet-lab NO-GOs are now explicitly documented:** H2AX phosphorylation review, DSB repair history review, nuclear-matrix UV repair legacy paper.

## Next action

Update the integrated `REPLICATION_EVALUATION_REPORT` with this new LUCID XFER New-20 wave and refresh aggregate counts/summary tables.
