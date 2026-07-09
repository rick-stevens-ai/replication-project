# LUCID p53 / DNA-damage-repair replication

Independent re-implementation of the p53 regulatory module from:

> Hu A. et al. (2022). **Modeling of DNA Damage Repair and Cell Response in
> Relation to p53 System Exposed to Ionizing Radiation.**
> *Int. J. Mol. Sci.* 23, 11323. DOI: [10.3390/ijms231911323](https://doi.org/10.3390/ijms231911323)

The LUCID paper's p53 module is built explicitly on the open-access PLOS
Computational Biology model of:

> Hat B., Kochańczyk M., Bogdał M.N., Lipniacki T. (2016). **Feedbacks,
> Bifurcations, and Cell Fate Decision-Making in the p53 System.**
> *PLOS Comput. Biol.* 12(2): e1004787 (CC-BY)

The LUCID supplement (with the bare reaction list) was initially blocked at
`www.mdpi.com/article/.../s1` (HTTP 403, bot-gated). We therefore used the
fully-open Hat 2016 `S1 Text` (Tables A/B/C — every reaction, rate law, and
rate constant) as the verbatim source of equations. The two papers' p53 cores
are equation-by-equation identical; LUCID adds one downstream pathway
(p21 → GADD45 → p38 → TGFβ) and a Hill-function ATM activator that we
implement directly.

**Cleanup 2026-05-28:** the LUCID supplement *was* reachable all along via
the static MDPI CDN (`mdpi-res.com`). It is now cached locally in
`artifacts/mdpi-supplement/` and Tables S1–S3 / Fig S1 have been verified to
match the Hat 2016 reactions and rate constants used here. The
`paywall-supplement` friction tag is **resolved**.

## What's here

```
lucid-p53-repair/
├── README.md                ← this file
├── PROGRESS.md              ← running log + friction tags
├── REPORT.md                ← claim-by-claim agreement table & limitations
├── source-LUCID-paper.pdf   ← target paper
├── source-LUCID-paper.txt   ← extracted text
├── source-Hat2016-S1.pdf    ← upstream model supplement (reactions + rates)
├── source-Hat2016-S1.txt    ← extracted text
├── code/
│   ├── p53_model.py         ← deterministic ODE (SciPy LSODA)
│   └── run_experiments.py   ← drivers + figure generation
├── figures/                 ← PNG reproductions of LUCID Fig 4/5/6
├── logs/                    ← stdout from runs
└── results/
    └── summary.json         ← peak values per species × dose × ATM threshold
```

## Reproduce

```bash
python3 code/run_experiments.py
```

Takes ~6 s on a single CPU core. Produces four figures and a JSON summary.

## Friction tags

`paywall-supplement`, `no-code`, `monte-carlo-substitution`, `model-substitution`, `stochastic-omitted` — see `REPORT.md` §5 for details.

## Coverage

Approximately **6 / 8** of the qualitative LUCID claims are reproduced
(3 fully + 3 partially + 0 contradicted). See `REPORT.md` §4 for the
claim-by-claim table.

## License

The two source papers are CC-BY. This replication code is released as MIT.
