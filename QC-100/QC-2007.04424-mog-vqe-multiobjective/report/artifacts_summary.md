# Artifacts Summary — QC-2007.04424-mog-vqe-multiobjective

Set: **QC-100**. Verdict: **REPLICATED** (H₂ scope). Paper: arXiv:2007.04424.

## Standard-8 artifact inventory

| # | Artifact | Path | Status |
|---|----------|------|--------|
| 1 | Source paper | `work/paper.pdf`, `work/paper.txt` | present |
| 2 | Report (Markdown, original) | `report/REPORT.md` | present |
| 3 | Report (LaTeX, backfilled) | `report/REPORT.tex` | **added** |
| 4 | Open questions JSON | `report/open_questions.json` | **added** |
| 5 | Open questions section (LaTeX) | `report/open_questions_section.tex` | **added** |
| 6 | Workflow | `report/workflow.md` | **added** |
| 7 | Failure analysis | `report/failure_analysis.md` | **added** |
| 8 | Extraction (Nougat stub) | `extraction/nougat.mmd` | **added** |
| — | Code | `code/mog_vqe_h2.py`, `code/refine_min_cnots.py` | present |
| — | Evidence (JSON, CSV, logs) | `report/evidence/*.json`, `*.csv`, `*.log` | present |

## Key result files (evidence)

- `report/evidence/mog_vqe_h2_result.json` — main NSGA-II run (FCI, HF, UCCSD, HEA sweep, GA history, final Pareto front).
- `report/evidence/mog_vqe_h2_pareto.csv` — final Pareto front (CNOTs vs energy).
- `report/evidence/mog_vqe_h2_refined.json` — directed enumeration k=2,3,4 topology sweep.
- `report/evidence/run_h2.log` — stdout, main NSGA-II run.
- `report/evidence/run_refined.log` — stdout, enumeration run.

## Headline numbers

| Circuit | # CNOTs | Energy error (Ha) | Reaches chem-acc (1.6 mHa)? |
|---------|---------|-------------------|----------------------------|
| UCCSD (Trotter) | 18 | 9e-10 | ✓ |
| HEA L=2 (first feasible) | 6 | 3.4e-9 | ✓ |
| **MoG-VQE 3-block (Pareto elbow)** | **3** | **6.4e-14** | **✓** |
| MoG-VQE 2-block (0/60 topologies) | 2 | 9.6e-3 | ✗ (real lower bound) |

Reduction vs UCCSD: **6×**. Reduction vs HEA: **2×**. Paper's headline (10× on BeH₂/LiH) not
directly tested; sign and mechanism reproduced.

## Verdict cross-check
**verdict_preserved = REPLICATED** (matches the substance: paper's headline
qualitative claim was reimplemented and reproduced end-to-end via genuine circuit
simulation, with numerical Pareto front and CNOT-reduction factors documented).
