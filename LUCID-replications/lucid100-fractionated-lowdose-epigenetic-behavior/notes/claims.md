# Quantitative claims extracted — Koturbash et al. 2016 (dvw025)

Source: Europe PMC JATS XML (`artifacts/europepmc_fullText.xml`), Results section.

## Animal model
- Strain: C57BL/6 male mice, 60 days old at start.
- Groups: control n=8 (sham, half sacrificed Day 1, half Day 6); treated n=60.
- Fractionation: 0.1 Gy X-ray (90 kV, 5 mA, 5 cGy/s) per day, Days 1–5; cumulative 0.1, 0.2, 0.3, 0.4, 0.5 Gy.
- Sacrifice times: 6 h (acute) and 24 h (delayed) after each daily exposure.
- Tissues: frontal cortex, olfactory bulb, hippocampus, cerebellum.

## DNA strand breaks (ROPS, Fig 2)
| Tissue | Time | Cumulative dose | Effect | p |
|---|---|---|---|---|
| Frontal cortex | 6 h | 0.2 Gy | 1.85× control | 0.027 |
| Frontal cortex | 6 h | 0.3–0.5 Gy | up to 3.0× | <0.05 |
| Frontal cortex | 24 h | 0.2 Gy | 2.1× | 0.005 |
| Frontal cortex | 24 h | 0.3–0.5 Gy | up to 3.5× | <0.05 |
| Cerebellum | 6 h | 0.1 Gy | 1.5× | <0.005 |
| Cerebellum | 6 h | 0.2–0.4 Gy | 1.3–1.4× | <0.005 |
| Cerebellum | 6+24 h | 0.5 Gy | 1.3× both | <0.005 |
| Hippocampus | 6 h | 0.1 Gy | 1.5× | 0.013 |
| Hippocampus | other | — | ns | ns |
| Olfactory bulb | all | — | ns | ns |

## p38 (Fig 3)
- Cerebellum: dose-dependent up-regulation, 6 h only, P < 0.01.
- Olfactory bulb: dose-dependent up-regulation, 6 h only, P < 0.01.
- Frontal cortex: down-regulation at 6 h and 24 h.
- Hippocampus: down-regulation at 6 h only.

## Global DNA methylation (HpaII extension, Fig 4)
- Cerebellum, 6 h, 0.1 Gy: 1.35× hypomethylation, P < 0.05. Returns to baseline at 24 h.
- Hippocampus, 6 h, 0.1 Gy: 1.5× hypomethylation; persists at 24 h (1.6×).
- Frontal cortex, 6 h, 0.1 Gy: 1.2× (ns); 24 h, 0.1 Gy: 1.25×, P < 0.05; trend toward hypermethylation from Day 2.
- Olfactory bulb: no significant changes at any dose / time.

## DNMTs and MeCP2 (Fig 5)
- DNMT1 down-regulated in frontal lobe, cerebellum, olfactory bulb (from Day 3); up-regulated in hippocampus.
- DNMT3a up-regulated in frontal lobe, hippocampus, olfactory bulb. Cerebellum up at Day 1, then down Days 2–3.
- DNMT3b up-regulated in hippocampus and (trend) olfactory bulb; ns in frontal lobe and cerebellum.
- MeCP2 up-regulated in all four tissues: 1.2× cerebellum, ~1.5× frontal cortex / hippocampus / olfactory bulb.

## Behavior — ladder rung walking (Fig 6)
- Two test sessions per day (4 h and 24 h post-exposure).
- One-way ANOVA + Tukey HSD. Numeric values not in text.

## Behavior — open field (Fig 7)
- Rearing, fields entered, novel fields, % time centre vs outside.
- 0.4 and 0.5 Gy: reduced centre-field exploration (anxiety-like).
- One-way ANOVA + Tukey HSD. Numeric values not in text.

## Statistical methodology
- DNA damage + Western: Welch/Student t-test with Bonferroni α/m, m=5, α=0.05 → α_corr=0.01.
- Behavior: one-way ANOVA + Tukey HSD, α=0.05.
- Software: MS Excel 2007 (Bonferroni), SPSS 11.5 (ANOVA).

## Data availability
- No deposited raw data of any kind (no GEO, SRA, ENA, ArrayExpress, ProteomeXchange, MetaboLights, BioStudies, GitHub, Zenodo, figshare, Dryad).
- No supplementary materials (Europe PMC supplementaryFiles endpoint returns the standard "no supplements" landing HTML; JATS XML has zero `<supplementary-material>` and zero `<table-wrap>` elements).
- All quantitative information is encoded in bar-chart figures only.
