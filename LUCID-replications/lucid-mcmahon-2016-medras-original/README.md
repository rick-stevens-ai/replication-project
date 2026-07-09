# LUCID100 Slot 62 / Wave 7 — McMahon 2016 (srep33290)

**Paper:** McMahon SJ, Schuemann J, Paganetti H, Prise KM (2016). *Mechanistic
Modelling of DNA Repair and Cellular Survival Following Radiation-Induced DNA
Damage.* **Scientific Reports 6:33290.** DOI: [10.1038/srep33290](https://doi.org/10.1038/srep33290).

LUCID master row: rank 93, tier B, priority 12, worktype `simulation/model
replication`. Themes: DNA repair / DDR; computational model / simulation.

This paper is the **original analytic MEDRAS model** (Mechanistic DNA Repair
And Survival) — the foundation for the Medras-MC Monte-Carlo implementation
replicated separately in `../lucid-medras-mc/`. Same author, same code base,
same 11 mechanistic parameters.

## TL;DR — verdict

**FULL REPLICATION ACHIEVED (smoke + full fit).** All 11 fitting parameters
recovered to within paper-quoted uncertainty by re-running the paper's own
Python source (Supplementary Code, ZIP linked from Nature), after a minimal
Python 2 → Python 3 port (≈4 lines changed across 6 modules). All six model
"figure" output TSVs regenerated, Fig. 5 survival panels visually reproduced.

**QA retag recommendation:** `done_replicated` (full replication, no caveats).

## Layout

```
lucid-mcmahon-2016-medras-original/
├── README.md                    # this file
├── PROGRESS.md                  # phase tracker
├── FIRST_PASS_REPORT.md         # full claim-by-claim replication report
├── MANIFEST.md                  # artifact manifest with SHA-256
├── artifacts/
│   ├── srep33290.pdf            # main paper (CC BY 4.0)
│   ├── srep33290.txt            # pdftotext extract for grepping
│   ├── supplementary_methods.pdf
│   ├── supplementary_code.zip   # author-released Python source + data
│   └── supplementary_code/      # unzipped working copy
├── code_py3/                    # author code, Py3-ported, runnable
│   ├── CharacteriseCell.py
│   ├── CellDNAModel.py
│   ├── SurvivalModel.py
│   ├── DNAModelFit.py
│   ├── SurvivalFit.py
│   ├── CellModelOutputs.py
│   ├── Full DNA Data Sets.csv
│   ├── Full Survival Data Sets.csv
│   └── README_UPSTREAM.txt
├── scripts/
│   └── plot_survival.py         # local: Fig. 5 reproduction plot
├── results/
│   ├── Model Data - Survival.tsv            # Fig. 5 curves
│   ├── Model Data - Foci Yields.tsv         # Fig. 1 curves
│   ├── Model Data - Misrepaired Breaks.tsv  # Fig. 2 curve
│   ├── Model Data - Aberration Yield.tsv    # Fig. 3a curves
│   ├── Model Data - Aberration Kinetics.tsv # Fig. 3b curves
│   └── Model Data - Mutation Yield.tsv      # Fig. 4 curve
├── figures/
│   └── fig5_reproduction_survival.png       # local reproduction plot
└── logs/
    ├── dna_fit.log
    ├── survival_fit.log
    └── cell_model_outputs.log
```

## Reproduce

```bash
cd code_py3
python3 DNAModelFit.py       # prints Table-1 DNA params (~5 s)
python3 SurvivalFit.py       # prints Table-1 ψ, φ (~10 s)
python3 CellModelOutputs.py  # writes the six "Model Data - *.tsv" files (~15 s)
mv *.tsv ../results/
python3 ../scripts/plot_survival.py  # produces figures/fig5_reproduction_survival.png
```

Requires Python 3 + `numpy` + `scipy` (any modern version; tested with
numpy 2.4.3, scipy 1.17.1, Python 3.14.4 on Darwin/x86_64). No GPU, no
heavy compute. Single-machine CPU fit, < 30 s total.

## License & ethics

- Main paper and supplementary information: Creative Commons Attribution 4.0
  International (CC BY 4.0). Reuse with citation permitted.
- Supplementary Code: published as part of the CC BY 4.0 supplementary
  material; not separately licensed. Author email present in README.txt.
- No author contact, no paid endpoints, no PII, all assets fetched from the
  publisher's own static-content host.

## Relationship to other LUCID slots

- **`../lucid-medras-mc/`** — replicates the 2021 Frontiers in Oncology paper
  (the **Monte-Carlo** Medras-MC variant, also by McMahon). The MEDRAS-MC
  GitHub repo (`sjmcmahon/Medras-MC`) cites *this* 2016 paper as its
  analytical foundation. Slot 62 (this folder) covers the original analytical
  model and its specific 11-parameter fit; the two replications are
  complementary, not redundant.
