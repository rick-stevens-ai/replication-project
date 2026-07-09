# Artifacts summary

Target dir: `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-0406180-complexity-local-hamiltonian-kempe-kitaev-regev/`

## Required 8-artifact bar (per REPLICATION_DIR_STANDARD_2026-07-05)
| # | Path                          | Status | Notes |
|---|-------------------------------|--------|-------|
| 1 | `paper.pdf`                   | ✓      | Copy of `work/paper.pdf` (arxiv v2, 30 pp, 321 KB). |
| 2 | `extraction/marker.md`        | ✓ (surrogate) | PyMuPDF (fitz) v1.27.2.3 parse; Marker not installed on host. Header labels tool. |
| 3 | `extraction/nougat.mmd`       | ✓ (surrogate) | `pdftotext -layout` parse; Nougat not installed on host. Header labels tool. |
| 4 | `report/REPORT.tex`           | ✓      | 6-page detailed LaTeX report with claims table, method, results, scaling fit, verdict, open-questions section. Compiles to `report/REPORT.pdf`. |
| 5 | `report/open_questions.json`  | ✓      | 5 heavy-duty open questions, each `{q,basis,next_steps}`; also `## Open Questions` in REPORT.tex. |
| 6 | `report/workflow.md`          | ✓      | Comprehensive workflow, tools + versions, work-time estimate. |
| 7 | `report/artifacts_summary.md` | ✓      | This file. |
| 8 | `report/failure_analysis.md`  | ✓      | Honest failure/friction/gaps. |

## Directory tree
```
QC-quant-ph-0406180-.../
├── paper.pdf                       [required art. 1]
├── extraction/
│   ├── README.md                   Explains surrogate parses.
│   ├── marker.md                   [required art. 2]
│   └── nougat.mmd                  [required art. 3]
├── report/
│   ├── REPORT.tex                  [required art. 4] LaTeX source
│   ├── REPORT.pdf                                    compiled 6 pp
│   ├── open_questions.json         [required art. 5]
│   ├── workflow.md                 [required art. 6]
│   ├── artifacts_summary.md        [required art. 7] this file
│   ├── failure_analysis.md         [required art. 8]
│   └── evidence/
│       ├── reproduce_gadget.py     dense-diagonalisation reproducer (Section 6.2 gadget)
│       ├── results.json            full machine-readable eigenvalues + errors + log-log fit
│       ├── scaling.csv             Δ, δ, err_gs, err_gap
│       └── scaling.png             log-log err vs Δ plot with paper's O(δ) reference line
└── work/
    ├── paper.pdf                   original download
    └── paper.txt                   `pdftotext paper.pdf` output for skimming
```

## Traces / provenance
- Paper source: `curl -sL -o work/paper.pdf https://arxiv.org/pdf/quant-ph/0406180` on 2026-07-05.
- Gadget definition transcribed from **Section 6.2, Eqs. (13)-(14)** of the v2 PDF.
- Reproducer's seed for the random 2-local `Y` operator: **numpy default_rng seed = 0**, exactly reproducible.
- Sector projection: eigenstates classified by their weight on the mediator subspace `span{|000⟩,|111⟩}` and further by the |+⟩_eff / |−⟩_eff sub-projections.
- Log-log fit: `numpy.polyfit(log(Δ), log(err), 1)` over `200 ≤ Δ ≤ 100000` (asymptotic window; excludes the small-Δ non-perturbative regime and the very-large-Δ conditioning floor).

## Results at a glance
- **Verdict: REPLICATED.**
- Ground-state error at Δ=1000: **1.1 × 10⁻¹** (δ = 0.10; paper predicts O(δ)).
- Ground-state error at Δ=5000: **4.9 × 10⁻²** (δ = 0.058; paper predicts O(δ)).
- Log-log slope err vs Δ (asymptotic window): **−0.41** (paper worst case: −1/3).
- Promise-gap error at Δ=1000: **9.7 × 10⁻²** (gap = 5.53 target, 5.43 gadget; <2% error).
- Promise-gap error at Δ=5000: **5.4 × 10⁻²** (<1% error).

## Executive one-liner
Section 6.2 three-qubit perturbation gadget of Kempe-Kitaev-Regev is
empirically verified: dense exact diagonalisation on 6-qubit systems
confirms the gadget's low-energy sector reproduces the target 3-local
Hamiltonian's spectrum with `O(δ) = O(Δ⁻¹/³)` error and preserves the
promise gap to within 1% by Δ = 5000, in units of the perturbation
scale V = 1.
