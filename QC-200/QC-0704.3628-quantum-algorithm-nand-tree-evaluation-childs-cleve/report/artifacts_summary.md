# Artifacts summary — arXiv:0704.3628 replication

Directory root: `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-0704.3628-quantum-algorithm-nand-tree-evaluation-childs-cleve/`

## The 8 required artifacts

| # | Artifact | Path | Status | Notes |
|---|----------|------|--------|-------|
| 1 | Original PDF | `paper.pdf` | ✓ | 281,555 bytes, 21 pages, fetched from https://arxiv.org/pdf/0704.3628 |
| 2 | Marker extraction | `extraction/marker.md` | ✓ (surrogate) | PyMuPDF 1.27.2.3 with page markers; Marker not installed on host, see `extraction/README.md` |
| 3 | Nougat extraction | `extraction/nougat.mmd` | ✓ (surrogate) | `pdftotext -layout` reflow; Nougat not installed on host, see `extraction/README.md` |
| 4 | LaTeX report | `report/REPORT.tex` | ✓ | Section-by-section, per-claim what-worked/didn't, verdict + justification; 13.6 KB |
| 5 | Open questions | `report/open_questions.json` + `## Open Questions` in REPORT.tex | ✓ | 5 non-superficial questions, each with basis + next_steps; 4.5 KB JSON |
| 6 | Workflow | `report/workflow.md` | ✓ | Narrative + tools/versions table + LOC + wall-clock + runs count |
| 7 | Artifacts summary | `report/artifacts_summary.md` | ✓ | This file |
| 8 | Failure analysis | `report/failure_analysis.md` | ✓ | 6 friction points documented with root cause + workaround + residual gap |

## Evidence + code (`report/evidence/`)

| File | Bytes | Purpose |
|------|-------|---------|
| `nand_tree_walk.py` | ~16 KB | Full replication: tree/tail construction, U₁/U₂/ψ_start, phase estimation, scaling harness |
| `classical_baseline.py` | ~2.8 KB | Snir/Saks-Wigderson randomised classical query lower bound baseline |
| `scaling_results.json` | ~2 KB | 60-trial per N sweep results (n=2,4,6,8; N=4,16,64,256); seed 20260705 |
| `classical_vs_quantum.json` | ~1 KB | Baseline comparison table (quantum queries vs Snir LB per N) |

## Intermediates + downloaded data (`work/`)

| File | Bytes | Purpose |
|------|-------|---------|
| `paper.txt` | ~46 KB | `pdftotext -layout` of paper.pdf; used for skimming the algorithm construction |

## External data sources

| Source | URL | Retrieved | Purpose |
|--------|-----|-----------|---------|
| arXiv | https://arxiv.org/pdf/0704.3628 | 2026-07-05 | Paper PDF |

## Key numerical results (headline)

Reproduced by re-running `python3 report/evidence/nand_tree_walk.py --seed 20260705`:

| n | N | queries/input | success ≥ 2/3? | success rate |
|---|---|---------------|-----------------|--------------|
| 2 | 4 | 35 | ✓ | 0.950 |
| 4 | 16 | 75 | ✓ | 0.950 |
| 6 | 64 | 155 | ✓ | 0.950 |
| 8 | 256 | 315 | ✓ | 0.917 |

Empirical scaling exponent: **log(queries) = 0.528 · log(N) + 2.838** (or 0.518 excluding n=2). Paper predicts **0.5**.

**Verdict: REPLICATED.**

## Reproducibility

Any host with Python 3 + numpy + scipy can reproduce end-to-end:
```
git clone <this dir>
cd QC-0704.3628-quantum-algorithm-nand-tree-evaluation-childs-cleve
python3 report/evidence/nand_tree_walk.py --seed 20260705 --out report/evidence/scaling_results.json
python3 report/evidence/classical_baseline.py
```
Wall-clock: ~95 s on a laptop CPU. No GPU, HPC, quantum hardware, or paid API required.

## Directory listing (final)
```
paper.pdf                            281 KB
extraction/README.md                 1 KB
extraction/marker.md                 49 KB   [Marker surrogate: PyMuPDF]
extraction/nougat.mmd                45 KB   [Nougat surrogate: pdftotext]
report/REPORT.tex                    14 KB   [detailed LaTeX report]
report/open_questions.json           5 KB    [5 open Qs with basis + next_steps]
report/workflow.md                   5 KB
report/artifacts_summary.md          <this file>
report/failure_analysis.md           7 KB
report/evidence/nand_tree_walk.py    17 KB   [core replication code]
report/evidence/classical_baseline.py 3 KB
report/evidence/scaling_results.json 2 KB
report/evidence/classical_vs_quantum.json 1 KB
work/paper.txt                       46 KB
```
