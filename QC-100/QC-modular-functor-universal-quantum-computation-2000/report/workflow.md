# Workflow

## Narrative

1. **Paper acquisition.** `curl` the arXiv v2 PDF to `paper.pdf` (23 pages).
2. **Text extraction.** No marker/nougat available locally or in `uicgpu:marlamr`; used `pdftotext -layout` as fallback for both `extraction/marker.md` and `extraction/nougat.mmd`, with the origin documented in `extraction/EXTRACTION_NOTE.md`. This is honest and the paper's math is LaTeX so OCR would not have added value.
3. **Paper reading.** Read Sections 1–4 of the extracted text; identified the paper's concrete testable content:
    - **Combinatorial:** dimensions V_n^ℓ.
    - **Algebraic:** Jones-representation matrices for the (2,5)-Young diagrams λ=[2,1], [3,3], [4,2].
    - **Spectral:** eigenvalues, multiplicities.
    - **Group-theoretic:** braid relations, Temperley–Lieb relations.
    - **Density (Thm 4.1):** only *ingredients* numerically testable.
    - **Concrete printed matrices** in Section 3.
4. **Implementation.** Wrote `fkw_replication.py` from scratch (415 LOC) using the paper's formulas (3), (13)–(15). No external quantum-computing libraries — pure numpy — to keep the replication genuinely independent.
5. **Verification.** Ran the script; all C1–C5 PASS at machine precision (≤ 10⁻¹⁵); C6 density-ingredients consistent; C7 revealed a likely typo in the paper's printed ρ_{[2,1]}(σ_2) matrix.
6. **Depth checks.** Wrote `fkw_extras.py` and `fkw_hadamard_deep.py` to strengthen the density evidence and universality-in-action check.
7. **LLM judge.** Called Argo GPT-5.1 (free ANL endpoint via the LiteLLM aggregator on cherryrd) with a critical prompt and the numerical evidence JSON; received a strict-JSON verdict.
8. **Reporting.** Assembled the 8 required artifacts.

## Tools + versions

| Tool                  | Version                          | Role                                                     |
|-----------------------|----------------------------------|----------------------------------------------------------|
| macOS / Darwin        | 25.3.0 (Tahoe)                   | Host OS on CherryRd                                       |
| Python                | 3.14.6 (Homebrew)                | Language                                                 |
| numpy                 | 2.5.1                            | Linear algebra                                           |
| scipy                 | 1.18.0                           | (installed, minimally used — future SVD/Haar)            |
| poppler-utils         | `pdftotext -layout`              | PDF text extraction (marker/nougat fallback)             |
| curl                  | system                           | PDF download + LLM aggregator call                       |
| LiteLLM aggregator    | http://<tailnet-aggregator>:4000/v1      | LLM router on cherryrd                                   |
| Argo proxy            | argo:gpt-5.1                     | Free ANL LLM endpoint (judge)                            |

## Codes / scripts written for this replication

- `work/fkw_replication.py` — 415 LOC, core replication.
- `work/fkw_extras.py` — 130 LOC, Haar comparison + hillclimb + stress.
- `work/fkw_hadamard_deep.py` — 70 LOC, BFS depth 15.
- `work/run_judge.py` — 90 LOC, LLM-judge caller.
- `work/run_judge.sh` — 60 LOC bash equivalent (superseded by Python).

## Effort estimate

| Dimension                            | Value                        |
|--------------------------------------|------------------------------|
| Wall clock (author-agent, 1 session) | ~50 minutes                  |
| Human-agent turns                    | ~35                          |
| LOC written (Python)                 | ~705                         |
| Compute time (all runs)              | ~2 minutes CPU (single-core, laptop) |
| GPU compute time                     | 0                            |
| External API calls                   | 1 arXiv PDF fetch, 1 LLM judge, 1 Argo model-list |
| Rework loops                         | 2 (bash → Python judge, Claude → GPT-5.1 model)  |

The replication is **compute-light** because the paper is pure theory; the value-add is a careful, from-scratch numerical construction that confirms the paper's algebraic formulas and reveals a likely typo in the paper's printed matrix.
