# Workflow — QC-1304.5773 replication (Gaitan & Clark 2013/2014)

## Objective
Independently reproduce the headline claim of arXiv:1304.5773 — that an
adiabatic quantum algorithm recovers a valid vertex permutation for small
isomorphic graph pairs (and produces a strictly positive energy for
non-isomorphic pairs) — on real numpy Hamiltonian dynamics.

## Tools + versions
| Tool | Version | Role |
| --- | --- | --- |
| Python | 3.13 (system) | driver |
| numpy | 2.5.1 | dense linalg |
| scipy | 1.18.0 | (imported; not needed for final path) |
| networkx | 3.6.1 | graph objects + edge-set arithmetic |
| matplotlib | latest | spectrum + gap figures |
| PyMuPDF (`fitz`) | 1.27.2.3 | `extraction/marker.md` (surrogate — Marker not installed) |
| poppler `pdftotext -layout` | system | `extraction/nougat.mmd` (surrogate — Nougat not installed) |
| curl / arXiv | — | paper fetch |
| No paid API calls | — | brief compliance |

Argo localhost:44497 was available for LLM-judge scoring but was not needed:
the verdict is decidable from the numerical results directly (fidelity > 0.997
on both iso instances; energy = classical HP_min on the non-iso control).

## Steps
1. **Fetch paper.** `curl -L https://arxiv.org/pdf/1304.5773 -o paper.pdf` →
   22-page v2 PDF, verified authors "Frank Gaitan and Lane Clark" (task brief
   had a typo "Clemente"), title matches.
2. **Skim + extract most-checkable claims.** `pdftotext paper.pdf` → recorded
   in REPORT.tex §2. Headline: adiabatic AQA recovers isomorphism for small N
   with non-negligible min gap on the interior of the schedule.
3. **Install env.** `python3 -m venv work/venv; pip install numpy scipy networkx
   matplotlib`.
4. **Implement simulator** (`report/evidence/gi_adiabatic.py`):
   - Enumerate S_N.
   - Build diagonal H_P from edge-mismatch cost.
   - Build H_D = (N-1)·I − Cayley-adjacency of adjacent transpositions.
   - Evolve |uniform⟩ under (1−s)H_D + s·H_P via Trotter with per-step
     dense Hermitian eigendecomposition (exact matrix exponential).
   - Compute fidelity on the isomorphism ground-space, spectrum along the
     schedule, and dominant final-state permutations.
5. **Run three instances.** N=4 iso, N=5 iso, N=5 noniso (path vs star).
   Final call: `--T 200 --steps 2000`. First run at T=50 gave 0.766 fidelity
   at N=5, second run at T=200 gave 0.997 — expected adiabatic-time behavior.
6. **Plot** (`report/evidence/plot_spectra.py`): low-4 spectrum + gap curves.
7. **Extraction artifacts.** Marker/Nougat not installed → produced clearly
   labelled surrogates (PyMuPDF, pdftotext-layout); see `extraction/README.md`.
   This follows the convention already used in sibling QC-200 dirs
   (e.g. `QC-0704.3628-*/extraction/`).
8. **Report.** `report/REPORT.tex` (this dir); attempted LaTeX compilation
   below.
9. **Companion artifacts.** open_questions.json, artifacts_summary.md,
   failure_analysis.md.

## Work-effort estimate
- Env setup + venv: ~1 min.
- Paper read + method extraction: ~5 min.
- Simulator + debugging + longer-T rerun: ~10 min (two runs).
- Extraction surrogates: ~2 min.
- Report writing: ~15 min.
- Total wall clock: ~35 min for this subagent.

## Reproduction command (single shot)
```
cd $(dirname $0)/..
work/venv/bin/python report/evidence/gi_adiabatic.py --T 200 --steps 2000 \
  --out report/evidence/results.json
work/venv/bin/python report/evidence/plot_spectra.py
```

## Determinism
The simulator is fully deterministic given `--T` and `--steps`: no random
sampling anywhere except the (unused) `rng` handle in `make_instances`. All
three graph pairs and both permutations pi_a, pi_b are hard-coded.
