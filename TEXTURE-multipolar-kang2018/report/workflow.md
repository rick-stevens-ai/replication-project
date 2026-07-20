# Workflow — Replication of Kang, Shiozaki, Cho (PRB 100, 245134)

## Environment
- Host: CherryRd (macOS 26.5.2), Python 3 with numpy + matplotlib.
- No DFT, no GPU, no paid API. Free/local tools only.
- PDF text extracted with `pdftotext -layout` (the `pdf` vision tool was
  unavailable — no API credits / document-extract plugin disabled).

## Steps
1. **Fetch & identify.** Confirmed arXiv:1812.06999 = "Many-Body Order
   Parameters for Multipoles in Solids". Target dir did not pre-exist; created
   `~/Dropbox/REPLICATE-PROJECT/TEXTURE-multipolar-kang2018/` and downloaded
   `paper.pdf` (v4, 2.6 MB) from `arxiv.org/pdf/1812.06999`.
2. **Extract.** `pdftotext -layout paper.pdf` -> transcribed the key equations
   (Eqs. 1-3 order parameters; Eq. 8/D5 BBH model with exact Gamma-matrix
   convention; symmetry operators D6-D11; Thouless-pump Eqs. 9-10) into
   `extraction/marker.md`.
3. **Pick claims.** Selected 5 machine-checkable claims (C1-C5) — see
   `artifacts_summary.md`.
4. **Implement** (`code/bbh_multipole.py`):
   - Gamma matrices exactly per the paper (Γ0=τ3⊗τ0, Γi=−τ2⊗τi, Γ4=τ1⊗τ0).
   - Bloch Hamiltonian h(k), Eq. 8.
   - Real-space occupied subspace P by inverse-FT of Bloch eigenvectors on an
     Lx×Ly torus at half filling (2 of 4 bands).
   - Many-body order parameter via the Slater determinant identity
     `<exp(i Σ φ n)> = det(P† diag(e^{iφ}) P)`; Q_xy = Im ln / 2π.
   - Atomic-trivial reference (λ→0) fixes the coordinate origin so trivial→0,
     topological→1/2 (paper convention).
5. **Run** (`code/run_all.py work`): sweeps L∈{6,8,10,12}, the γ_y transition
   cut, dipole check, and the isotropic Thouless pump. Writes
   `work/results.json`.
6. **Figures** (`code/make_figures.py work`): `work/replication_figures.png`
   (transition + pump; mirrors Fig 1c / Fig 2a).
7. **Report.** `report/REPORT.tex` (+ compiled PDF), `open_questions.json`
   (5), `artifacts_summary.md`, `failure_analysis.md`, this file.

## Reproduce
```bash
cd TEXTURE-multipolar-kang2018
python3 code/bbh_multipole.py            # self-test
python3 code/run_all.py work             # all claims -> work/results.json
python3 code/make_figures.py work        # -> work/replication_figures.png
cd report && pdflatex REPORT.tex         # -> REPORT.pdf (if pdflatex present)
```

## Key decisions / deviations
- **Analytic/TB, not DFT** (as instructed). The paper's numerical proof is
  itself a tight-binding calculation, so this is a faithful (not reduced-order)
  reproduction of the free-fermion part.
- **Atomic reference** for the origin: the raw Q_xy phase is convention
  (coordinate-origin) dependent; only the phase *difference* is gauge-invariant.
  Referencing to the atomic-trivial limit yields the paper's 0 / (1/2) reading
  and is consistent with the paper's proven invariance under adding trivial
  atomic bands.
- **Out of scope (marked):** interacting/bosonic cases, the anomalous
  quadrupole insulator (Fig 1d, supplement-only params), and the generalized
  partial-region operators V(l) (Fig 3). Captured as open questions.
