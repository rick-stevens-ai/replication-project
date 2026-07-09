# LUCID replication — Patra et al. 2022 (PolβΔ / PA1 radiosensitivity)

**Target:** Patra A, Nag A, Chakraborty A, Bhattacharyya N. *PA1 cells containing a truncated DNA polymerase β protein are more sensitive to gamma radiation.* Radiat Oncol J 2022;40(1):66-78. **DOI [10.3857/roj.2021.00689](https://doi.org/10.3857/roj.2021.00689)**.

**Verdict: PARTIAL** — coverage 5/10, agreement 7/10 on the reproducible computational pieces, paper-internal consistency 4/10. See [`REPORT.md`](REPORT.md) for the full write-up.

## What was attempted

| Component | Status |
|---|---|
| Sequence translation + WT/Δ alignment from Suppl Table S1 | **DONE** — major issue found (cDNA does not encode the claimed 97-aa in-frame deletion) |
| Linear-quadratic refit of Fig. 2 colony-forming data | **DONE** — DMF ≈ 1.80 at 10 Gy reproduced |
| Internal-consistency audit of all paper numbers | **DONE** — several flagged anomalies |
| HDOCK protein-DNA docking (4 runs) | **NOT rerun** — server queue cost; inputs/units spot-checked |
| ClusPro protein-protein docking (9 partners) | **NOT rerun** — same; numbers tabulated and unit error flagged |
| Wet-lab experiments (Figs 1, 3-7) | **Out of scope** — values tabulated for audit |

## Headline findings

1. **Sequence inconsistency.** The ΔPolβ cDNA the authors deposited in Supplementary Table S1 is **not** an in-frame deletion of residues 208–304. It is a 413-nt deletion (frame-shifted, NOT a multiple of 3) between WT codons 121 and 257, producing 198 aa of which the last ~80 are scrambled / contain ≥6 premature stop codons. The "ΔPolβ structural model" used for docking cannot have been built from this cDNA.
2. **Deletion range is given in three different ways** in the paper text (208–301, 208–304, 211–339).
3. **HDOCK and ClusPro scores are mislabelled as kcal/mol** — both tools output dimensionless template/cluster scores.
4. **LQ refit confirms the radiobiological claim.** D10: WT 17.8 Gy → mutant 8.85 Gy. DMF ≈ 1.80 at the paper's "optimal" 10 Gy dose.
5. **ROS at 10 Gy is *lower* than at 5 Gy** in the mutant, and *lower* than in WT — both undiscussed; both opposite to the BER-failure hypothesis.

## Reproducing this work

```bash
# Inside this directory:
python3 code/01_sequence_check.py        # 1 s
python3 code/02_lq_fit.py                # 1 s
python3 code/03_quantitative_audit.py    # < 1 s
```

Requires Python 3.10+, `biopython`, `numpy`, `scipy`, `matplotlib`.

All inputs are public (paper PDF + 4 supplements at e-roj.org). No author contact, no paid endpoints used.

## Directory layout

```
.
├── REPORT.md              # full replication report
├── PROGRESS.md            # session log
├── README.md              # this file
├── code/
│   ├── 01_sequence_check.py
│   ├── 02_lq_fit.py
│   └── 03_quantitative_audit.py
├── data/
│   ├── paper.pdf  +  paper.txt
│   ├── suppl{1,2,3,4}.pdf + .txt
├── results/
│   ├── sequence_check.json
│   ├── alignment.txt
│   ├── {wt,del}_{protein,nt}.fasta
│   ├── lq_fit.json
│   └── quant_audit.{json,txt}
└── figures/
    ├── page{4,5,6}-{0X}.png   # source pages
    └── fig2_replication.png   # our LQ refit
```

## License of replication code

CC0 / public domain. Paper PDF and supplements are CC BY-NC 4.0 (Korean Society for Radiation Oncology).
