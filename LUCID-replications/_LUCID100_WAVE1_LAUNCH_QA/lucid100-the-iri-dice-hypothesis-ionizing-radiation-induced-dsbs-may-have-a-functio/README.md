# The IRI-DICE hypothesis: ionizing radiation-induced DSBs may have a functional role for non-deterministic responses at low doses

## LUCID100 curated Wave 1 replication brief

- **Rank:** 39
- **Tier/score:** A / 20
- **DOI:** 10.1007/s00411-020-00854-x
- **Year / venue:** 2020 / Radiation and Environmental Biophysics (Controversial Issue)
- **Themes:** DNA repair / DDR; dose-rate / low-dose response; radiation quality / RBE; omics / biomarkers / signatures
- **Worktype (master TSV):** "omics/signature replication" — **mis-categorised; this is a hypothesis paper with no data.** See `FIRST_PASS_REPORT.md`.
- **Source:** semantic_scholar
- **PDF / URL:** https://link.springer.com/content/pdf/10.1007/s00411-020-00854-x.pdf
- **Status:** first-pass complete, partial replication via toy scaffold; see `FIRST_PASS_REPORT.md` for verdict.

## What this paper is

A conceptual *hypothesis* paper. The authors propose that DNA double-strand
breaks at low dose cause stochastic, persistent cis-acting changes in
transcription of nearby genes, where the *sign* of the change depends on
whether the DSB hit a promoter, gene core, enhancer, or negative regulatory
element. They argue this explains the observed diversity and
non-determinism of low-dose IR responses. The paper has:

- 1 figure (a non-quantitative cartoon),
- 0 tables,
- 0 equations,
- 0 supplementary files,
- 0 code,
- 0 new datasets.

The authors themselves state that direct experimental testing is currently
impossible and propose a future computational programme as the only
feasible test.

## Directory layout

```
.
├── README.md                          # this file
├── PROGRESS.md                        # status updates
├── FIRST_PASS_REPORT.md               # verdict, scope decision, smoke results
├── artifacts/
│   ├── paper.pdf                      # CC-BY 4.0 OA from Springer
│   ├── paper.txt                      # pdftotext -layout extract
│   ├── MANIFEST.md                    # provenance + hashes
│   └── figs/
│       ├── fig_doseresponse_diversity.png
│       ├── fig_suppression_dominance.png
│       ├── fig_repair_threshold.png
│       └── summary.json
├── code/
│   └── iri_dice_toy_mc.py             # minimal Monte Carlo smoke test
└── logs/                              # (empty; smoke run is sub-second)
```

## Reproducing the smoke run

```bash
cd code/
python3 iri_dice_toy_mc.py --ncells 3000 --seed 0
# writes ../artifacts/figs/{fig_*.png, summary.json}
```

Dependencies: Python 3, `numpy`, `matplotlib`. Runs in <2 s on a laptop.
No network, no GPU, no heavy compute.

## Replication scope

See `FIRST_PASS_REPORT.md` § "Replication scope decision". Short version:
the only meaningful replication target for a hypothesis paper without data
is the **conceptual mechanism itself**, implemented as a toy Monte Carlo
that the authors explicitly outline in their "Approaches to test IRI-DICE"
section. The smoke run qualitatively reproduces claims 2 (diversity),
3 (suppression dominance), and 4 (repair-threshold non-monotonicity).

A full quantitative replication is *not defined by the paper* and is
out of scope.

## Initial abstract

Low-dose ionizing radiation (IR) responses remain an unresolved issue in
radiation biology and risk assessment. … Cellular responses to low-dose IR
appear diverse and stochastic in nature and to date no model has been
proposed to explain the underlying mechanisms. Here, we propose a hypothesis
on IR-induced double-strand break (DSB)-induced cis effects (IRI-DICE) and
introduce DNA sequence functionality as a submicron-scale target site with
functional outcome on gene expression … (see `artifacts/paper.txt` for full).
