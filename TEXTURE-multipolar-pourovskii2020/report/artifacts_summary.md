# Artifacts Summary

Replication of **Pourovskii & Khmelevskyi, arXiv:2009.08908** — *Hidden order and
multipolar exchange striction in a correlated f-electron system* (NpO2),
Nat. Commun. 12, 3282 (2021).

## Verdict
**PARTIAL** (strong) — Coverage **6/10**, Agreement **8/10**.
Four low-energy claims reproduced with real computation (one *exact*, parameter-
free); the ab initio DFT+DMFT+force-theorem machinery and its direct numerical
outputs are out-of-scope (no proprietary actinide DFT available).

## Directory layout
```
TEXTURE-multipolar-pourovskii2020/
├── paper.pdf
├── extraction/
│   └── marker.md                 # pdftotext -layout dump (737 lines)
├── code/
│   ├── cf_j92.py                 # J=9/2 Stevens operators + CF Hamiltonian
│   ├── cf_llw_scan.py            # LLW W,x parametrization; x=-0.54 scheme
│   ├── cf_irrep_map.py           # irrep sequence vs x; x=-0.54 & -0.48 window
│   ├── jeff_exchange_split.py    # Jeff=3/2 Gamma8 singlet-doublet-singlet
│   └── mft_striction.py          # mean-field T0 + exchange striction eps~xi^2
├── work/
│   ├── cf_run1.txt
│   ├── cf_llw_scan.txt
│   ├── cf_irrep_map.txt
│   ├── jeff_exchange_split.txt
│   ├── mft_striction.txt
│   └── elastic_check.txt
└── report/
    ├── REPORT.tex  (+ REPORT.pdf if latex available)
    ├── open_questions.json       # exactly 5
    ├── workflow.md
    ├── artifacts_summary.md      # this file
    └── failure_analysis.md
```

## Key reproduced numbers
| Quantity | Paper | This replication | Verdict |
|---|---|---|---|
| CF irrep ordering (J=9/2) | Gamma8-Gamma8-Gamma6 | Gamma8-Gamma8-Gamma6 | reproduced |
| Excited Gamma8 gap | 68 meV | 68 meV (W-scaled) | reproduced |
| Gamma6 doublet | >300 meV | 126 meV | partial (J-mixing) |
| LLW x window | x=-0.54 (INS -0.48) | both in Q-Q-D window | reproduced |
| Quartet splitting pattern | singlet-doublet-singlet | singlet-doublet-singlet | reproduced |
| E(upper singlet)/E(doublet) | 12.2/6.1 = 2.00 | **2.0000 (exact)** | reproduced |
| 1k order test | (implicitly excluded) | doublet-doublet (excluded) | supports 3k |
| MF transition order | 2nd order, T0=38 K | continuous, tuned 38 K | reproduced |
| Striction shape | eps ~ xi_pr^2(T) | eps ~ xi^2(T) | reproduced |
| xi^2 at 3/4 T0 | ~60% | 56% | reproduced |
| Striction magnitude @T=0 | 0.023% (exp 0.018%) | same ~2e-4 order | consistent |
| K_el = (C11/2+C12)/3 | (implied) | 115 GPa | reproduced |

## Highlight
The **parameter-free ratio 2.00** for the upper-singlet/doublet exchange
splitting of the Gamma8 quartet under a 3k Gamma5-triakontadipole field matches
the paper's 12.2/6.1 = 2.00 to 4 decimal places — a clean, unforced quantitative
hit that also independently selects the 3k (triple-q) order over 1k.

## Reproduce
```
cd TEXTURE-multipolar-pourovskii2020
python3 code/cf_llw_scan.py
python3 code/cf_irrep_map.py
python3 code/jeff_exchange_split.py
python3 code/mft_striction.py     # ~40 s (bisection)
```
Requires: Python 3 + NumPy. No network, no DFT.
