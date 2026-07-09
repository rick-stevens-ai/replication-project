# Artifacts summary — arXiv:1701.08669 replication

Directory root: `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-1701.08669-graphical-quantum-algorithm-hidden-subgroup/`

## The 8 required artifacts

| # | Artifact | Path | Status | Notes |
|---|----------|------|--------|-------|
| 1 | Original PDF | `paper.pdf` | ✓ | 546,220 bytes, 21 pages, fetched from https://arxiv.org/pdf/1701.08669 (2026-07-05) |
| 2 | Marker extraction | `extraction/marker.md` | ✓ (surrogate) | PyMuPDF 1.27.2.3 with page markers; Marker not installed on host, see `extraction/README.md` |
| 3 | Nougat extraction | `extraction/nougat.mmd` | ✓ (surrogate) | `pdftotext -layout` reflow; Nougat not installed on host, see `extraction/README.md` |
| 4 | LaTeX report | `report/REPORT.tex` | ✓ | Section-by-section, per-claim what-worked/didn't, verdict + justification |
| 5 | Open questions | `report/open_questions.json` + `## Open Questions` in REPORT.tex | ✓ | 5 non-superficial questions, each with basis + next_steps |
| 6 | Workflow | `report/workflow.md` | ✓ | Narrative + tools/versions table + LOC + wall-clock + runs count |
| 7 | Artifacts summary | `report/artifacts_summary.md` | ✓ | This file |
| 8 | Failure analysis | `report/failure_analysis.md` | ✓ | Friction points, workarounds, residual gaps |

## Evidence + code (`report/evidence/`)

| File | Purpose |
|------|---------|
| `hsp_abelian.py`   | Full replication: cyclic-group / subgroup / coset utilities, hiding-function builder, statevector HSP pipeline, ZX-rewrite consistency check (V3), CLI, JSON output. |
| `hsp_results.json` | Full result dump: character distributions per test group, per-coset conditionals, V3 trials (5 random hiding functions each), overall_ok flag. |
| `hsp_output.log`   | Stdout of the successful run showing V1/V2/V3 all pass. |

## Intermediates + downloaded data (`work/`)

| File | Purpose |
|------|---------|
| `paper.txt` | `pdftotext -layout` of paper.pdf; used for skimming the algorithm construction. |

## External data sources

| Source | URL | Retrieved | Purpose |
|--------|-----|-----------|---------|
| arXiv | https://arxiv.org/pdf/1701.08669 | 2026-07-05 | Paper PDF |

## Key numerical results (headline)

Reproduced by re-running `python3 report/evidence/hsp_abelian.py --seed 20260705`:

| Case | Group | H | Analytic H^⊥ | P(y ∈ H^⊥) | \|\|P - uniform(H^⊥)\|\|₂ | V3 max\|P_A - P_B\| |
|------|-------|---|--------------|-----------|---------------------------|---------------------|
| (a) | Z_8  | ⟨2⟩ = {0,2,4,6}  | {0,4}          | 1.000000000000000  | 3.14e-16 | 1.11e-16 |
| (b) | Z_15 | ⟨5⟩ = {0,5,10}   | {0,3,6,9,12}   | 0.999999999999995  | 2.69e-15 | 2.78e-17 |

Per-coset conditionals identical in both cases (Diagram 5.3 independence-of-b confirmed).
V3 was verified on 5 random hiding functions per test group; every trial's max
absolute deviation between Pipeline-A (full protocol) and Pipeline-B (post-rewrite via
partial trace) was < 3e-16.

**Verdict: REPLICATED.**

## Reproducibility

Any host with Python 3 + numpy can reproduce end-to-end:
```
git clone <this dir>
cd QC-1701.08669-graphical-quantum-algorithm-hidden-subgroup
python3 report/evidence/hsp_abelian.py --seed 20260705 --outdir report/evidence
```
Wall-clock: <1 s on a laptop CPU. No GPU, HPC, quantum hardware, or paid API required.

## Directory listing (final)
```
paper.pdf                            533 KB
extraction/README.md                 1 KB
extraction/marker.md                 ~57 KB  [Marker surrogate: PyMuPDF]
extraction/nougat.mmd                ~56 KB  [Nougat surrogate: pdftotext]
report/REPORT.tex                    17 KB   [detailed LaTeX report]
report/open_questions.json           6 KB    [5 open Qs with basis + next_steps]
report/workflow.md                   5 KB
report/artifacts_summary.md          <this file>
report/failure_analysis.md           see file
report/evidence/hsp_abelian.py       18 KB   [core replication code]
report/evidence/hsp_results.json     ~15 KB
report/evidence/hsp_output.log       ~6 KB
work/paper.txt                       55 KB
```
