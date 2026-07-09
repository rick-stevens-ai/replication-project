# workflow.md — QC-1608.02005 replication workflow

## Timeline / effort estimate
- Total wall-clock: **~55 minutes** (subagent single session, 2026-07-05 14:20 CDT +)
- Human/agent labour equivalent: about 1 hour focused work — extraction of algorithm, brute-force DS enumeration, statevector implementation, convention diagnosis (Step-4 conjugate + peak-at-+s), and reporting.

## Tools + versions
| Tool | Version | Where |
|---|---|---|
| Python | 3.13 (system) | `/usr/bin/python3` |
| numpy | 2.5.1 | `venv/` |
| qiskit | 2.5.0 | `venv/` (used only for version stamping + convention cross-check) |
| pdftotext (poppler) | 25.x | system `pdftotext` |
| Marker | **NOT installed** — extraction fallback used | — |
| Nougat | **NOT installed** — extraction fallback used | — |
| curl | system | for arXiv fetch |
| LaTeX / pdflatex | (not run — REPORT.tex left as .tex; compile with `pdflatex report/REPORT.tex` if needed) | — |
| Argo LLM | not used (self-verdict; the quantitative claim is a numerical amplitude comparison against the paper's own closed form, so a judge panel would be redundant) | — |

## Step-by-step
1. Fetch paper:
   ```
   curl -sL https://arxiv.org/pdf/1608.02005 -o paper.pdf
   ```
2. Extract text:
   ```
   pdftotext -layout paper.pdf work/paper.txt
   ```
3. Identify the ONE most-checkable numerical claim: Algorithm 1 Step-5 measurement probability distribution, with peak probability p = 4(k-lambda)/|A| (plus exact closed form).
4. Choose small cyclic groups admitting known difference sets:
   - Z_7  (7,3,1)   — Singer / Fano projective plane PG(2,2)
   - Z_11 (11,5,2)  — Paley q=11
   - Z_13 (13,4,1)  — Singer PG(2,3)
   - Z_19 (19,9,4)  — Paley q=19
5. Brute-force enumerate size-k subsets of Z_v, count all pairwise differences, filter to constant-count subsets (real difference sets), deduplicate by translation class.
6. Implement Algorithm 1 as a v-dimensional statevector:
   - Step 1: uniform superposition (1/sqrt v) * ones(v).
   - Step 2: oracle sign-flip on positions in (s + D).
   - Step 3: apply v-dim unitary DFT F (F[j,k] = exp(2 pi i j k / v)/sqrt v).
   - Step 4: multiply by diagonal diag(1, conj(chi_j(D))/sqrt(k-lambda)) for j != 0. See REPORT.tex for why conjugate.
   - Step 5: apply F^dagger.
   - Read off probabilities as |psi|^2.
7. For every (DS, shift s) pair (50 combinations across the 4 DS's), run Algorithm 1 and record:
   - full probability vector over Z_v,
   - argmax outcome,
   - prob at s (our convention) and at -s (paper's convention),
   - paper's leading-order p = 4(k-lambda)/v,
   - paper's Step-5 closed-form (c_bulk + c_extra)^2,
   - Step-4 diagonal unit-modulus max-error (Turyn check).
8. Cross-check classical brute-force baseline for the same oracle (recover s in O(v*k)) — passes on all 50.
9. Save results to `report/evidence/algorithm1_run.json` and console log to `report/evidence/algorithm1_run.log`.
10. Draft `report/REPORT.tex` with claims table, method, results table, verdict, open questions.
11. Draft supporting docs: this workflow.md, `artifacts_summary.md`, `failure_analysis.md`, `open_questions.json`.
12. Write fallback extraction files `extraction/marker.md` and `extraction/nougat.mmd` with a prominent PROVENANCE note explaining Marker/Nougat are not installed and this is a pdftotext-derived structural transcription.

## Convention diagnosis (the tricky bit)
The paper writes the Step-4 diagonal as `diag(1, chi(D)/sqrt(k-lambda))` and the Step-5 measurement outcome as `|-s>`. For A = Z_v with complex characters this is inconsistent: plugging chi(D) literally gives chi(D)^2 in Step 4 (complex, not equal to k-lambda). The two natural fixes are:
- Use `conj(chi(D))/sqrt(k-lambda)` — reproduces the paper's own stated Step-4 output.
- Absorb a global g <-> -g relabelling into the QFT direction — reconciles the "peak at -s" statement.
We adopted the first fix and noted the second in comments. The empirically observed peak is at `+s` under our F convention; both `+s` and `-s` are one classical XOR away from each other so this is not a physical discrepancy.

## What is NOT tested (out of scope)
- Reduction of Algorithm 1 to the shifted-Legendre algorithm for Paley DS (would need van Dam-Hallgren-Ip separately).
- Reduction to shifted-bent-function for Hadamard DS.
- Efficient implementation of Step-4 diagonal for Singer / Mersenne dihedral HSP (would need the van Dam-Seroussi 2003 compiler as a separate module).
- Full dihedral HSP end-to-end.

## Files produced
See `artifacts_summary.md`.

## How to re-run
```
cd ~/Dropbox/REPLICATE-PROJECT/QC-200/QC-1608.02005-quantum-algorithms-abelian-difference-sets
source venv/bin/activate
python report/evidence/replicate_algorithm1.py
```
Expected runtime ~2 seconds on any modern CPU. Deterministic (no RNG in the algorithm; measurement is analytical, not sampled).
