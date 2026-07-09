# Workflow — quant-ph/0211124 replication

## Executive summary
- **Target**: independently replicate Theorem 2 (per-trial `Omega(1)` success of paper's basis) and the GSVV-style random-basis indistinguishability contrast, for the affine group `A_p` HSP over hidden conjugates `H^b`.
- **Total wall time**: ~30 minutes end-to-end (paper fetch → env → 3 experiments → LaTeX compile).
- **Verdict**: REPLICATED. All four testable claims (C1, C2, C4, C5) confirmed within tolerance.

## Step-by-step

### 1. Paper acquisition and reading (~3 min)
- `curl -sL https://arxiv.org/pdf/quant-ph/0211124 -o paper.pdf` (239 KB, 16 pages).
- `pdftotext paper.pdf work/paper.txt` (1043 lines).
- Identified the reproducible core: Section 2 ("Conjugates of the Largest Non-Normal Subgroup") gives an explicit closed-form per-trial success bound `>= (2/pi)^2` for the paper's basis choice, and Section 4 argues Abelian methods (and by GSVV citation, random-basis strong methods) give distributions independent of the hidden conjugate label b.

### 2. Environment (~2 min)
- Created isolated venv at `work/venv/`.
- Installed `qiskit==2.5.0` + `numpy==2.5.1` + scipy (transitive).
- Real Qiskit statevector class used for Haar-random unitary draws (`qiskit.quantum_info.random_unitary`, CUE-distributed).

### 3. Implementation (~10 min)
Three self-contained scripts in `report/evidence/`:
1. `replicate_affine_hsp.py` — main experiment: builds `A_p`, hidden subgroups `H^b`, coset states `|psi_b>`, Fourier component at rho, runs paper's basis vs single-fixed-U random basis with MAP decoder trained on same-U pilot. Also runs multi-shot majority vote (k=1..10).
2. `random_basis_average.py` — averaged over 30 draws of Haar-random U, computes MAP accuracy per U.
3. `gsvv_fresh_basis_test.py` — **definitive test**: fresh U per trial, decoder unaware of U. Confirms outcome distribution collapses to the prior (accuracy = 1/p exactly to within noise).

### 4. Runs (~5 min compute)
- `replicate_affine_hsp.py`: 4000 trials/b for p=5, 2000/b for p=7. Multi-shot: 500 trials/b/k.
- `random_basis_average.py`: 30 unitaries × 150 trials/b × 2 primes.
- `gsvv_fresh_basis_test.py`: 4000 pilot + 1500 score trials per basis mode per prime.
- All outputs saved as JSON + `.log` file per script.

### 5. Report (~5 min)
- `REPORT.tex` written and compiled to `REPORT.pdf` (5 pages, 277 KB) via `pdflatex`.
- `open_questions.json` with 5 substantive follow-up questions grounded in observed behavior.
- `artifacts_summary.md` + `failure_analysis.md` written.
- `extraction/marker.md` + `extraction/nougat.mmd` created as best-effort substitutes (Marker and Nougat not installed in the environment; central corpus has no entry for this arxiv id).

## Tools + versions
| Tool | Version | Purpose |
|---|---|---|
| macOS | 25.3.0 | host OS |
| Python | 3.13 | scripting |
| numpy | 2.5.1 | array math, complex arithmetic |
| qiskit | 2.5.0 | Haar-random unitary generation (`qiskit.quantum_info.random_unitary` = CUE distribution) |
| scipy | (transitive) | pulled in with qiskit |
| pdftotext | XPDF/poppler (macOS built-in) | paper text extraction |
| pdflatex | TeXLive 20260301 | REPORT.pdf compilation |
| Marker | NOT INSTALLED | substitute markdown produced from `pdftotext` |
| Nougat | NOT INSTALLED | substitute MMD produced from `pdftotext` |

## Effort estimate
- Paper reading + understanding: 8 minutes (small paper, mathematically precise).
- Simulator design: 5 minutes (three-block structure: group setup, rho matrix, protocol A/B/B-fresh).
- Debugging: minimal (~2 minutes: one indexing issue where `k` was 0-indexed vs 1-indexed as elements of `Z_p^*`).
- Analysis + report: 12 minutes.
- **Total: ~30 minutes wall clock.**

## Reproducibility
Every result in `REPORT.tex` § 4 is reproducible by:
```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-0211124-hidden-subgroup-affine-groups
source work/venv/bin/activate
python report/evidence/replicate_affine_hsp.py
python report/evidence/random_basis_average.py
python report/evidence/gsvv_fresh_basis_test.py
```
All RNGs are seeded explicitly (seed=42 primary, offsets for pilot vs scoring). Results should match to `< 0.01` in accuracy.
