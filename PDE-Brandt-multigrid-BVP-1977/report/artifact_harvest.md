# Artifact Harvest

## Paper

| Item | URL | Size | SHA-256 |
|---|---|---|---|
| Brandt (1977) PDF (open access, AMS) | https://www.ams.org/journals/mcom/1977-31-138/S0025-5718-1977-0431719-X/S0025-5718-1977-0431719-X.pdf | 6,106,566 bytes (10 pages of scan) | `d4f187bd5bcdb5262214598ab33a98d83affe390800e3b246964746d35089e5b` |
| Extracted plain text (pdftotext -layout) | local | 2937 lines | `work/brandt1977.txt` |

Note on PDF size: the AMS scan spans the full 58-page article (paginated 333–390 in the journal) rendered as 10 image-pages of the scanned reprint; text is fully extractable with `pdftotext -layout`.

## Ground-truth reference numbers pulled from the paper

- **Brandt Table 1** (§6.2): standard 5-point Laplace, SOR (Gauss–Seidel, ω=1), mesh ratio 1:2, 2D
  - smoothing factor `p` (interior) = 0.500
  - MG convergence factor (theoretical) `μ = p / (1 − p^d) = 0.500 / (1 − 0.25) = 0.667` — reported as **0.595** in Brandt's Table 1 with a more careful analysis
- **Brandt Appendix B experiment**: 33² fine grid, Cycle C (injection restrict, linear interp)
  - Measured factor `μ ≈ (0.009051)^(1/12.92) = 0.686` (paper text, lines 1116–1120 of extracted text)
  - "Each cycle costs 4.3 WU" (Appendix B annotation)
- **Complexity claim** (§Abstract, §6.3): system of `n` unknowns solved to accuracy in `O(n)` operations
  - "40 n additions and shifts for Poisson problems" (Abstract)

## Software

| Item | Version |
|---|---|
| Python | 3.14.6 (system) |
| NumPy | (whatever ships with system Python 3.14 — used only for basic array ops, no exotic API) |
| matplotlib | 3.x (Agg backend) |
| pdftotext | Poppler (used for text extraction only) |

## Compute

- Local CPU, host `CherryRd` (macOS). No HPC needed — the largest problem (513² ≈ 2.6·10⁵ unknowns) runs in ~0.24 s per V-cycle in pure NumPy.

## LLM scoring endpoint

- Argo proxy `http://127.0.0.1:44497` (free ANL), model `argo:claude-sonnet-4.6`, temperature 0.0.
  Judge prompt + JSON response saved in `report/evidence/llm_judgment.json` and `llm_judge_raw.txt`.
