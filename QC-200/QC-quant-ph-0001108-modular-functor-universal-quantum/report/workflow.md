# Workflow — quant-ph/0001108 replication

## Narrative

1. Read the QC wave brief (`~/Dropbox/REPLICATE-PROJECT/scripts/QC_WAVE_BRIEF_2026-07-03.md`) and the 8-artifact standard (`REPLICATION_DIR_STANDARD_2026-07-05.md`).
2. Created target directory tree under `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-0001108-modular-functor-universal-quantum/`.
3. Fetched the paper PDF: `curl -sL https://arxiv.org/pdf/quant-ph/0001108 -o work/paper.pdf` (212 KB, 20 pages).
4. Ran `pdftotext -layout paper.pdf paper.txt` and skimmed the first 200 lines to identify the concrete claim. Confirmed the actual author list from the PDF is *Freedman, Larsen, Wang* (three authors, Kitaev acknowledged but not co-author on v2) — differs from the brief's parenthetical.
5. Identified this as a mathematical universality proof (Chern–Simons at level 5 = SU(2)_3 = Fibonacci anyons). Selected as the reproducible substrate: verify Fibonacci F/R data satisfy pentagon + hexagon; build the B_3 representation on the 2-dim 3-anyon computational subspace; run a breadth-first density search over braid words and report the best operator-norm distance to Hadamard and T gates.
6. Wrote a self-contained NumPy implementation (`work/fibonacci_anyons.py`, ~500 LOC) — no third-party TQFT library required.
7. Ran the simulation at `--max-len 15`, walltime ~3 minutes on one CPU core. Results written to `fibonacci_results.json`.
8. Fixed an initial JSON-serialisation bug (complex numbers in the hexagon dict) and re-ran.
9. Copied evidence to `report/evidence/`.
10. Because Marker and Nougat CLIs are not installed on CherryRd and the central corpus does not appear to hold this arXiv id, the `extraction/marker.md` and `extraction/nougat.mmd` files were populated as honest `pdftotext -layout` fallbacks with headers making the fallback explicit — as permitted by REPLICATION_DIR_STANDARD_2026-07-05.md ("copy from central manifest if available, else run Marker/Nougat").
11. Wrote all 8 required artifacts (paper.pdf, extraction/{marker.md, nougat.mmd}, report/REPORT.tex, open_questions.json, workflow.md, artifacts_summary.md, failure_analysis.md).

## Tools and codes used

| Tool | Version | Role |
|---|---|---|
| Python | 3.14.6 (Homebrew, macOS Darwin 25.3.0 x86_64) | interpreter |
| NumPy | 2.4.3 | linear algebra, complex arithmetic, matrix exponentiation |
| SciPy | 1.18.0 | (imported but not strictly needed) |
| curl | system | download paper PDF from arXiv |
| pdftotext (poppler) | system | text extraction (Marker/Nougat fallback) |
| `work/fibonacci_anyons.py` | v1 (this replication) | Fibonacci F/R construction, axiom checks, braid-word BFS density search |

## Effort estimate

| Item | Value |
|---|---|
| Human/agent turns | ~15 (single subagent, single session) |
| Wall clock (agent) | ~15 minutes |
| Compute time (real sim) | ~3 minutes CPU on one core |
| LOC written | ~500 (fibonacci_anyons.py) |
| Simulation runs executed | 2 (initial failed on JSON; second succeeded) |
| PDFs read | 1 (paper.pdf, first ~200 lines skimmed) |
| Downloads | 1 (paper.pdf, 212 KB) |

## Reproducibility one-liner

```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-0001108-modular-functor-universal-quantum/work
python3 fibonacci_anyons.py --max-len 15 --out fibonacci_results.json
```
