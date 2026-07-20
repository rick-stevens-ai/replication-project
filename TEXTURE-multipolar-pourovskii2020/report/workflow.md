# Workflow — Replication of arXiv:2009.08908 (NpO2 hidden order)

## 1. Ingestion
- `paper.pdf` (1.7 MB) pre-fetched into the target dir.
- Extracted layout text with `pdftotext -layout paper.pdf extraction/marker.md` (737 lines).
- Read abstract, RESULTS, and METHODS. The paper is a DFT+DMFT(Hubbard-I) +
  force-theorem ab initio study; the reproducible core is the effective
  low-energy model (crystal field + Jeff=3/2 pseudospin + mean field).

## 2. Claim triage
Picked 5 claim clusters (C1–C5), 4 machine-checkable + 1 out-of-scope:
- C1 cubic CF level scheme / irrep ordering (J=9/2, x=-0.54).
- C2 LLW x-parameter consistency (x=-0.54 vs INS x=-0.48).
- C3 singlet-doublet-singlet exchange splitting, ratio 12.2/6.1 = 2.00.
- C4 mean-field 2nd-order transition + exchange striction eps ~ xi^2(T).
- C5 full 15x15 ab initio SEI matrix / RPA INS / real-space texture (OOS).

## 3. Implementation (`code/`, pure Python + NumPy 2.4.3)
1. `cf_j92.py` — angular-momentum + Stevens operators; first attempt using
   Hutchings Stevens factors on the paper's A_k^q<r^k> (diagnostic; gave right
   Gamma8-ground symmetry but wrong ordering/x-sign due to factor conventions).
2. `cf_llw_scan.py` — switched to the canonical LLW W,x parametrization
   (F4=60, F6=13860 for J=9/2). At x=-0.54, W<0 -> Gamma8-Gamma8-Gamma6 with
   excited Gamma8 fixable to 68 meV. THIS is the clean, convention-independent test.
3. `cf_irrep_map.py` — mapped the full irrep sequence vs x; confirmed x=-0.54
   AND x=-0.48 both sit in the Q-Q-D window.
4. `jeff_exchange_split.py` — Jeff=3/2 Gamma8 quartet; three Gamma5 (t2g)
   rank-3 pseudo-operators; 3k uniform mean field -> singlet-doublet-singlet,
   ratio exactly 2.0000. 1k order -> doublet-doublet (rules out 1k).
5. `mft_striction.py` — self-consistent single-site MF; Jex tuned to T0=38 K;
   confirmed continuous (2nd-order) xi(T); eps* ~ xi^2 with 56% at 3/4 T0;
   K_el = (C11/2+C12)/3 = 115 GPa.

## 4. Execution (`work/`)
Ran each script, captured logs:
- `cf_run1.txt`, `cf_llw_scan.txt`, `cf_irrep_map.txt`,
  `jeff_exchange_split.txt`, `mft_striction.txt`, `elastic_check.txt`.
- `mft_striction.py` runs a bisection (each step scans 800 T points) → ~40 s;
  run under a 300 s timeout, completed cleanly (exit 0).

## 5. Comparison to paper
| Claim | Paper | This work | Status |
|---|---|---|---|
| CF ordering | G8-G8-G6 | G8-G8-G6 | reproduced |
| excited G8 | 68 meV | 68 meV (scaled) | reproduced |
| G6 doublet | >300 meV | 126 meV | partial (J-mixing) |
| LLW x | -0.54 (INS -0.48) | both in Q-Q-D window | reproduced |
| splitting pattern | S-D-S | S-D-S | reproduced |
| upper-singlet/doublet | 12.2/6.1=2.00 | 2.0000 (exact) | reproduced |
| MF transition | 2nd order, T0=38 K | continuous, tuned 38 K | reproduced |
| striction shape | eps ~ xi_pr^2, ~60% @ 3/4 T0 | eps ~ xi^2, 56% @ 3/4 T0 | reproduced |
| striction magnitude | 0.023% vs 0.018% exp | same 2e-4 order | consistent |
| 15x15 SEI / RPA INS | ab initio | not attempted | out-of-scope |

## 6. Reporting (`report/`)
REPORT.tex (+PDF), open_questions.json (5), workflow.md, artifacts_summary.md,
failure_analysis.md. Extraction in extraction/marker.md.
