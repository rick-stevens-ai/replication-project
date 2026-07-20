# Workflow — Replication of Bhowal & Spaldin (arXiv:2212.03756 / 2205.09500)

**Paper:** *Magnetic octupoles as the order parameter for unconventional
antiferromagnetism*, S. Bhowal & N. A. Spaldin, arXiv:2212.03756v1 (7 Dec 2022);
earlier arXiv version 2205.09500; published Phys. Rev. X **14**, 011019 (2024).
**System:** rutile MnF2 — prototype centrosymmetric, non-relativistic-spin-split
(NRSS / altermagnetic) antiferromagnet.

> Note on arXiv ID: the task specified 2205.09500. The `paper.pdf` on disk is the
> same work under its later arXiv identifier 2212.03756v1 (identical title/authors/
> content). We proceeded with the on-disk PDF and flag the ID mapping here.

## Steps executed

1. **Locate target dir.** Requested name `TEXTURE-multipolar-chen2022` did not
   exist; the multipolar/2205.09500 paper in `REPLICATE-PROJECT/` is
   `TEXTURE-multipolar-bhowal2022` (author = Bhowal). Confirmed by reading the PDF
   title page.

2. **Extract paper text.** `pdf` model tool was unavailable (API credit / model
   errors), so text was extracted deterministically with `pypdf` into
   `extraction/marker.md` (13 pages, ~66k chars). Read abstract, Sec. II–V, and
   Appendices A–C (computational details, Table I TB parameters, band structure).

3. **Identify machine-checkable claims.** Selected the tractable model-tier
   claims (spin-splitting formula, d-wave symmetry, hopping dependence, octupole
   form factor, piezomagnetic tensor symmetry). Flagged DFT-only results
   (multipole magnitudes, Compton profiles, strain-induced moments) as out of
   scope.

4. **Implement minimal model** (NOT DFT):
   - `code/tb_mnf2.py` — canonical 4-band/8-band TB model, Eqs. (2)–(6),
     Table I parameters (eV, realistic lattice constants).
   - `code/model.py` + `code/run_checks.py` — independent second implementation
     in reduced units, as a cross-check.

5. **Run verification** under `work/`:
   - `code/verify_claims.py` → `work/verify_results.json` (10 claims, 10/10 PASS).
   - `code/run_checks.py` → `work/results.json` (5 claims, all PASS; corroborates).
   - `code/make_figs.py` → `work/fig_spin_splitting.png`;
     `run_checks.py` also writes `work/fig_dwave_map.png`, `fig_spin_splitting_GM.png`.

6. **Quantitative comparison** to paper Fig. 3(d), Fig. 2, Eq. (6): documented in
   `report/REPORT.tex`.

7. **Compile report** to PDF (see artifacts_summary.md for status).

## Environment
- Python venv at `work/.venv` (numpy, scipy, matplotlib, pypdf).
- Host: CherryRd (macOS). No external/paid endpoints used; DFT not run.

## Reproduce
```bash
cd TEXTURE-multipolar-bhowal2022
python3 -m venv work/.venv && source work/.venv/bin/activate
pip install numpy scipy matplotlib pypdf
cd code
python tb_mnf2.py         # self-test table (eq6_exact == full8 == approx within ~2%)
python make_figs.py       # -> ../work/fig_spin_splitting.png
python verify_claims.py   # -> ../work/verify_results.json  (10/10 PASS)
python run_checks.py      # -> ../work/results.json  (independent cross-check)
```
