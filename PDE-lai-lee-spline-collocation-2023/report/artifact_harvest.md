# Artifact Harvest

| Artifact | Source | Notes |
|---|---|---|
| paper.pdf | https://arxiv.org/pdf/2109.09698v4 | arXiv OA, 1,415,050 bytes, PDF v1.5. Fetched via curl (NOT paid pdf tool). |
| paper.txt | `pdftotext -layout paper.pdf` | 1628 lines; used to extract exact PDE, method, test functions, Table 4/5 values. |

**No author code was used.** The paper references an "Algorithm 1 in [15]" (a companion
MATLAB spline toolbox) but does not bundle runnable code with the manuscript. The entire
solver here was implemented from scratch in Python from the mathematical description in
Sections 3–6, so this is a genuine independent reimplementation, not a rerun of author code.

**Reference numbers extracted from the paper (Table 4, 2D Poisson, D=8, r=2):**
- us1 = e^{(x²+y²)/2}:      RMSE(u−us) 6.95e-11 / 1.23e-11 / 1.67e-12 / 1.63e-11 across 4 domains
- us3 = 1/(1+x²+y²):        RMSE 2.58e-11 / 6.96e-12 / 1.48e-12 / 8.03e-12
- us6 = arctan(x²−y²):      RMSE 1.75e-11 / 3.23e-12 / 2.97e-13 / 7.51e-12
- us7 = −cos x cos y e^{…}: RMSE 3.07e-12 / 1.15e-12 / 2.81e-13 / 1.10e-12
- us5 = sin 3πx sin 3πy:    RMSE 6.16e-08 … 3.02e-10 (hardest smooth case, larger errors)
- Domains: Moon, Flower-with-a-hole, Star-with-2-holes, Circle-with-3-holes.

**Compute:** convergence sweep run on uicgpu (8×A100 host, CPU numpy/scipy) — see
evidence/conv_study.log and evidence/conv_results.json. Light dev/tests run locally on CherryRd.
