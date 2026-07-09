# Artifact Harvest

All artifacts pulled 2026-07-04 UTC via arXiv OA. No paywalls encountered.

| # | Artifact | URL | Local path | Size |
|---|---|---|---|---|
| 1 | ABC 2022 paper (arXiv v1) | https://arxiv.org/pdf/2112.03116 | `work/paper.pdf` | 426,725 B |
| 2 | ABC 2022 paper (extracted text) | (pdftotext of #1) | `work/paper.txt` | 79,203 B |
| 3 | Vishik 2018 part I (arXiv:1805.09426) | https://arxiv.org/pdf/1805.09426 | `work/vishik1.pdf` | 805,352 B |
| 4 | Vishik 2018 part II (arXiv:1805.09440) | https://arxiv.org/pdf/1805.09440 | `work/vishik2.pdf` | 759,762 B |
| 5 | ABC + De Lellis, Giri, Janisch, Kwon exposition of Vishik (arXiv:2112.06949, ref [1] of ABC) | https://arxiv.org/pdf/2112.06949 | `work/vishik_exposition.pdf` | 1,480,073 B |
| 6 | Independent numerical eigenvalue solver (code) | — | `work/vishik_eigenvalue.py` | 8,454 B |
| 7 | Grid refinement driver | — | `work/vishik_refinement.py` | 1,124 B |
| 8 | Eigenvalue results (all profiles × modes) | — | `work/vishik_eig_results.json` → mirrored to `report/evidence/vishik_eig_results.json` | 18,571 B |
| 9 | Grid-refinement results | — | `work/vishik_refinement.json` → mirrored to `report/evidence/vishik_refinement.json` | 2,614 B |

**Data flow provenance:** Paper text → identify Vishik dependency → pull Vishik + exposition → implement linearized 2D Euler operator per Sec.2.2 of paper → discretize + solve for eigenvalues on uicgpu (8×A100, but the problem is small: 5s CPU run) → grid-refinement → LLM-judge via Argo proxy (free endpoint).

**No fabrication:** every number in the report is an actual numpy output from the runs recorded in `evidence/`.

## Compute lineage
- Numerical work: `uicgpu` (uicgpu01, 8×A100). Actual runs used CPU only — problem is N≤1200 dense complex `np.linalg.eig`, trivial. Total wall ≈5s + refinement ≈50s.
- LLM-judge: Argo proxy `http://localhost:44497/v1` (free), key `stevens`. Five judges polled: gpt-5.2, gpt-5.1, gpt-5, o3, gemini-2.5-pro. (claude-opus-4.7/4.8 upstream 502 in Argo proxy on this day — logged.)
