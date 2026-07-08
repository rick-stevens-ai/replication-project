# Artifacts Summary & Traces — Replication of arXiv:2606.30402

Inventory of every artifact produced/pulled for this replication and the traces of the run.

## Directory layout
```
QC-2606.30402-quantum-fusion-blanket-flibe-tritium/
  paper.pdf                         # (1) source paper, arXiv:2606.30402v1, 7 pp, 5.2 MB
  extraction/marker.md              # (2) layout-preserving text extraction (pdftotext; Marker pending)
  extraction/nougat.mmd             # (3) math-text extraction (same source; Nougat pending)
  report/REPORT.tex                 # (4) detailed LaTeX report (+ results_tables.tex, verdict.tex)
  report/open_questions.json        # (5) 5 heavy-duty open questions + next steps
  report/workflow.md                # (6) workflow, tools/versions, effort estimate
  report/artifacts_summary.md       # (7) this file
  report/failure_analysis.md        # (8) honest failure/gap analysis
  report/evidence/code/             # all replication code (build/ladder/ewf/analyze/launch)
  report/evidence/                  # results JSON + analysis (injected on completion)
  work/clusters/                    # generated cluster geometries (XYZ), 3 systems x (base+9)
```

## (1) Source paper
- `paper.pdf` — *Quantum Computations on Fusion Blanket Molten Salts*, Das, Pinheiro Dos
  Santos, Bhowmik, Bazayeva, Li, Shajan, Kaliakin, Liang, Bryantsev, Geist, McClain Gomez,
  Pellegrini, Walkup, Seelam, Motta, Merz Jr., Beck. arXiv:2606.30402v1, 2026-06-29. 7 pages
  main + Supporting Information. DOI 10.48550/arXiv.2606.30402.

## (2)/(3) Text extractions
- `extraction/marker.md`, `extraction/nougat.mmd` — full-paper layout-preserving text
  (poppler `pdftotext -layout`, 110 KB). Marker/Nougat native parses pending an install
  (see failure_analysis.md §C). Contain the complete main text + SI (systems, EWF method,
  ext-SQD, AIMD/MLFF protocol, solver dispatch, all claim numbers).

## (4) Report
- `report/REPORT.tex` — section-by-section: paper summary, systems, 9-row claims table
  (C1–C9), method-as-executed, results (injected), per-claim what-worked/didn't, verdict,
  open questions, reproducibility statement.
- `report/results_tables.tex`, `report/verdict.tex` — injected from `results/analysis.json`.

## (5)–(8) 
- `open_questions.json` — 5 grounded questions (eta-convergence of embedding error;
  difference-consistent embedding for E_bind; noiseless-vs-hardware SQD offset; multireference
  ensemble fraction; tritium isotope/nuclear-quantum effect), each with concrete next steps.
- `workflow.md`, `artifacts_summary.md`, `failure_analysis.md` — as described.

## Code (report/evidence/code/)
| File | Role |
|---|---|
| `build_clusters.py` | ASE construction of Li6Be3F12 / [Li6Be3F13]- / Li6Be3F13T clusters + 9 conformers each |
| `run_ladder.py` | full-molecule RHF/MP2/CCSD(+T1)/DFT(PBE-D3,B3LYP,PBE0) per conformer |
| `run_one.py` | single-conformer wrapper for parallel launch |
| `run_ewf_frag.py` | Vayesta EWF (IAO+MP2-BNO bath, eta=1e-5) + per-fragment FCI/CCSD/simulated-SQD |
| `analyze.py` | assembles T1, conformational dE, E_bind, SQD-vs-FCI MAD/max, embedding offset |
| `launch_all.sh` | parallel campaign driver (uicgpu) |

## Cluster geometries (work/clusters/)
- `FLiBe/`, `FLiBeF/`, `FLiBeTF/` — each with `*_base.xyz` + `*_c1..c9.xyz`. `meta.json`
  records formula/charge/spin/rattle-sigma. Verified stoichiometry: Be3F12Li6 (q0),
  Be3F13Li6 (q-1), HBe3F13Li6 (q0).

## Run traces (report/evidence/, injected on completion)
- `results/ladder_{FLiBe,FLiBeF,FLiBeTF}.json` — per-conformer full-molecule energies + T1.
- `results/frag_{FLiBe,FLiBeF,FLiBeTF}.json` — per-fragment CCSD/FCI/SQD-sim energies + M/nelec.
- `results/analysis.json` — the comparison tables vs the paper's reported bands.
- Compute host: uicgpu (8× A100 80 GB), env `~/flibe-repl/.venv` (Python 3.11); logs under
  `~/flibe-repl/logs/`.

## Verification traces already recorded
- RHF/6-31+G* on Li6Be3F12 = **378 AOs, 138 electrons** — matches paper's 378 AOs exactly.
- RHF total (cluster 1, our geometry) = −1273.3023 Ha; MP2 = −1275.6902 Ha; PBE-D3/B3LYP/PBE0
  converged. EWF-CCSD runs end-to-end; Vayesta reports per-fragment active spaces (Li ~8–12,
  F ~27–36 orbitals) consistent with the paper's 8–33 range (ours slightly larger due to
  hand-built, more diffuse clusters).
