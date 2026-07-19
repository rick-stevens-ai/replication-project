# Workflow --- Urazhdin 2024 (arXiv:2408.08683v3) replication

## Paper
S. Urazhdin, *Atomic and inter-atomic orbital magnetization induced in SrTiO$_3$ by
chiral phonons*, arXiv:2408.08683v3 [cond-mat.mtrl-sci], 5 Jun 2025.
Method class: **model-Hamiltonian / molecular-orbital tight-binding + time-dependent
perturbation theory** (analytic, no public code, no numerical tables).

## Pipeline (acquire -> parse -> extract -> build -> run -> compare -> report)
1. **Acquire** --- PDF already in corpus dir (`textures-orbital-urazhdin2024.pdf`).
2. **Parse** --- `pdftotext` (poppler) for text; `marker`/`nougat` not installed,
   so artifacts 2--3 are honest pdftotext interims (layout mode -> `marker.md` prose;
   reading order + hand-transcribed LaTeX equations -> `nougat.mmd` math).
3. **Extract recipe** --- `replication_recipe.json`: minimal 6-state MO tight-binding,
   params $t_{TiO}=-1.14$, $t_{OO}=-0.8$~eV, $r_{TiO}=0.2$~nm, $a=0.39$~nm,
   $\Delta=3.2$~eV, $\hbar\omega=12.4$~meV.
4. **Build** --- from-scratch Python kernel `work/urazhdin2024_repl.py` (numpy only):
   (A) 6x6 complex-Hermitian MO Hamiltonian + `eigh`; (B) Koster--Slater chain;
   (C) numeric first-order TDPT (400k-point trapezoid) + closed-form cross-check;
   (D) inter-atomic scale $\mu_1$ in SI -> $\mu_B$.
5. **Run** --- `/home/stevens/comfyui-env/bin/python work/urazhdin2024_repl.py`
   -> `work/urazhdin2024_result.json`. Runtime < 2 s (6x6 matrices, trivial).
6. **Compare** --- per-claim checks against the paper's equations/numbers
   (see `report/REPORT.tex` table).
7. **Report** --- 8-artifact package (this dir).

## Tools / versions
- Python: `/home/stevens/comfyui-env/bin/python`, numpy 2.3.5, scipy 1.17.0 (numpy only used).
- `pdftotext` (poppler) for text extraction. `marker`/`nougat`/`pdflatex` NOT installed
  (interim fallbacks + .tex source shipped; see failure_analysis.md).
- Host: spark (ARM64 Linux).

## Verification performed
- **Live re-run on 2026-07-19** of the kernel reproduced the saved `*_result.json`
  to all quoted digits (spectrum, gap=3.2000, $a_t=5.70$, $a_l=19.95$, $\mu_1=1.597$,
  TDPT ratio 0.99996) --- the package is built on verified, not stale, evidence.
- Numeric diagonalization vs analytic Eqs.(1)-(3): machine precision ($\sim10^{-16}$).
- Numeric TDPT vs closed-form Eq.(8): ratio 0.99996.
- Every `.json` artifact parse-checked with `json.load`.

## Effort estimate
- Physics (build + run + compare): ~1.5 h (done in a prior session).
- Packaging (this pass): ~1 h (extraction interims, REPORT.tex with equation
  transcription, open_questions, workflow, artifacts_summary, failure_analysis,
  evidence copy, audit).

## Verdict
**REPLICATED** --- Coverage ~6/10, Agreement ~9/10. MO level structure and bandgap
(3.2 eV) reproduce exactly; Koster--Slater estimates and $\mu_1$ within ~2%. Honest
gaps: no transport observable / full k-space band structure (paper reports none),
absolute experimental magnitude not targeted (out of scope by paper's own conclusion).
