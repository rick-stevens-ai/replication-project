# Workflow — s100-041 replication

**Paper:** Abolfath, Grosshans, Mohan (2020) *Oxygen depletion in FLASH ultra-high-dose-rate radiotherapy: a molecular dynamics simulation.* Med. Phys. 47(12). arXiv:2010.00744v1. DOI 10.1002/mp.14548.

## Steps executed
1. **Ingest.** Copied `source/paper.pdf` (2.2 MB, 11 pp, pdfTeX 1.40.21 / LaTeX). Extracted plain text with `pdftotext -layout` → `ocr/paper.txt` (729 lines, clean; no OCR needed because PDF has embedded text).
2. **Manuscript audit.** Read all 11 pp. Identified two disjoint methodological halves:
   - §II.A + Figs 1–5: multiscale MD pipeline (Geant4-DNA → CPMD → LAMMPS-ReaxFF + GROMACS). Snapshot-rendering only, no quantitative observables.
   - §II.B + Figs 6–7: coarse-grained rate-equation model (Eqs 1–9). Quantitatively reproducible from the printed equations.
3. **Reproducibility triage.** Chose to focus reproduction on §II.B because (a) it is the only part of the paper with numerical claims, and (b) rerunning the MD pipeline requires Geant4-DNA + LAMMPS-ReaxFF + GROMACS + a DFT code, all on HPC, and is out of scope for a laptop-scale replication of a claim that is not itself made from MD.
4. **Numerical reproduction.** Implemented `code/repro_eq12.py`:
   - `scipy.integrate.solve_ivp` with method=`Radau` (stiff-tolerant).
   - Two runs: FLASH pulse (G=100 for 0.01 s, then G=0 out to 100 s) and CDR pulse (G=0.01 for 100 s).
   - $D_f = 1$ in the paper's natural units (paper never supplies a numeric value).
   - IC: $N_1(0) = N_2(0) = 0$.
5. **Scaling verification.** Implemented `code/verify_scaling.py`:
   - Constant-G integration at G = 1 and G = 100.
   - Log-log slope fits over four decades to verify Eqs 7 ($N_1 \propto G t$, slope 1), 8 ($N_2 \propto G^2 D_f t^3$, slope 3), and 9 ($N_2 \propto (G^2/D_f)^{1/3} t^{1/3}$, slope 1/3).
6. **Comparison.** Extracted (i) $N_2(\text{FLASH})/N_2(\text{CDR})$ at long times (paper caption Fig 7: ≈ 2×), (ii) fitted slopes vs analytic, (iii) shape of $N_1(t)$ vs Fig 6.
7. **Reporting.** Wrote `report/REPORT.md` (markdown source of truth). Later generated:
   - `report/REPORT.tex` (LaTeX version with honest critique + verdict downgrade).
   - `report/open_questions.json` (5 questions, machine-readable).
   - `report/open_questions_section.tex` (\input'd by REPORT.tex).
   - `report/workflow.md` (this file).
   - `report/artifacts_summary.md`.
   - `report/failure_analysis.md` (why queue said REPLICATED but substance is SPOT-CHECK).
   - `extraction/nougat.mmd` (stub; not run — PDF text extracted losslessly via `pdftotext`).

## What was NOT done (and why)
- **MD pipeline (Stages 1–3):** not rerun. Required software: Geant4-DNA 11.x, LAMMPS with `pair_style reax/c`, GROMACS 2020+, CPMD 4.x. Estimated wall-time on uicgpu A100: 24–72 h per O2-condition. No code/data released by authors, so any rerun would require independent reconstruction of the input decks — that is a re-implementation, not a replication.
- **Oxygen sweep (§III claim of physoxic-optimum):** not attempted. The claim in the paper is text-only, no supporting curve; verifying it would require the μ_1 source function, which is symbolic-only in the manuscript.
- **New MD runs on a substitute force field:** out of scope for laptop replication; captured as Q5 in open questions.

## Compute + provenance
- All numerics run on M1 MacBook laptop; total wall time < 5 s.
- No paid endpoints, no external LLM calls. Free tooling only (Python, scipy, numpy, matplotlib).
- Runs are deterministic; scripts self-contained.
