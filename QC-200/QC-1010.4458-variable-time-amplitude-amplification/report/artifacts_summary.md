# Artifacts Summary — QC-1010.4458 (Ambainis VTAA)

## Directory tree

```
QC-1010.4458-variable-time-amplitude-amplification/
├── paper.pdf                              # 240 KB, arXiv:1010.4458v2, 17 pages
├── extraction/
│   ├── marker.md                          # Surrogate Marker parse (pdftotext + hand-added headings)
│   └── nougat.mmd                         # Surrogate Nougat parse (pdftotext + LaTeX equations)
├── work/
│   ├── paper.txt                          # pdftotext -layout output, 1586 lines
│   └── venv/                              # Isolated Python 3.13 + Qiskit 2.5.0 venv
└── report/
    ├── REPORT.tex                         # Main replication report, compiles to PDF (pdflatex)
    ├── REPORT.pdf                         # (if pdflatex available) compiled report
    ├── open_questions.json                # 5 heavy-duty follow-on questions
    ├── workflow.md                        # Reproduction workflow + tool versions
    ├── artifacts_summary.md               # THIS FILE
    ├── failure_analysis.md                # Friction log + regime mis-modeling first-pass
    └── evidence/
        ├── aa_standard.py                 # Grover AA sanity check on N=16
        ├── standard_aa_result.json        # Full Grover curve, Qiskit vs analytic
        ├── vtaa_core.py                   # VTAA scaling experiment (Qiskit Statevector)
        ├── vtaa_core_result.json          # HHL-regime scaling table + fitted exponents
        ├── vtaa_core_result_toy.json      # Toy-regime scaling table
        ├── vtaa_core_combined.json        # Both regimes merged for the plot
        ├── standard_vs_vtaa_curve.csv     # HHL-regime CSV (kappa, T_max, T_av, p_succ, Q_std, Q_var, speedup)
        ├── standard_vs_vtaa_curve_toy.csv # Toy-regime CSV
        ├── make_plot.py                   # Matplotlib log-log plot script
        └── vtaa_vs_standard.png           # log-log plot: Q_std vs Q_var in both regimes
```

## Provenance trace

| Artifact | Source | Fabrication risk | Reviewer check |
|---|---|---|---|
| paper.pdf | `curl https://arxiv.org/pdf/1010.4458` | none (upstream) | md5 vs arXiv |
| work/paper.txt | `pdftotext paper.pdf work/paper.txt` | none | diff vs paper |
| extraction/marker.md | hand-derived from work/paper.txt | low (headings only) | inspect vs work/paper.txt |
| extraction/nougat.mmd | hand-derived from work/paper.txt (LaTeX eqns) | low (equations transcribed) | LaTeX render check |
| standard_aa_result.json | Qiskit 2.5.0 Statevector, aa_standard.py, deterministic | none | rerun script |
| vtaa_core_result*.json | Qiskit 2.5.0 Statevector, vtaa_core.py, deterministic | none | rerun script |
| standard_vs_vtaa_curve*.csv | derived from vtaa_core_result*.json | none | recompute from JSON |
| vtaa_vs_standard.png | matplotlib on combined JSON | none | rerun make_plot.py |
| REPORT.tex | prose report citing all evidence files | claims are LLM-summarised but every number comes from evidence/*.json | cross-check each numeric claim |

## Key numeric claims (all traceable to a specific JSON/CSV)

| Claim in REPORT.tex | Source file | Field |
|---|---|---|
| Grover k=2 reaches P≥0.9 (=0.9084) on N=16 | standard_aa_result.json | first_iterations_reaching_p_ge_0_9, curve[2].p_marked_qiskit |
| Grover analytic ≡ Qiskit statevector to ~1e-15 | standard_aa_result.json | curve[k].p_marked_qiskit vs p_marked_analytic |
| Standard AA scaling exponent = 1.502 (HHL regime) | vtaa_core_result.json | fitted_exponent_standard |
| VTAA scaling exponent = 1.112 (HHL regime) | vtaa_core_result.json | fitted_exponent_variable |
| Speedup exponent = +0.390 (HHL regime) | vtaa_core_result.json | fitted_exponent_speedup_ratio |
| Crossover κ* ~ 90 (speedup > 1 above this) | vtaa_core_result.json | rows[i].speedup_factor |
| Speedup at κ=8192 = 9.1× | vtaa_core_result.json | rows[-1].speedup_factor |

## Reproducibility

To reproduce:
```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-200/QC-1010.4458-variable-time-amplitude-amplification
python3 -m venv work/venv && source work/venv/bin/activate
pip install --quiet qiskit qiskit-aer numpy matplotlib
python report/evidence/aa_standard.py
python report/evidence/vtaa_core.py
python report/evidence/make_plot.py
```
Expected wall time: <10 seconds on a modern laptop CPU.
