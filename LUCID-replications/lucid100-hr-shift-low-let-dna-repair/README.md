# lucid100-hr-shift-low-let-dna-repair

**LUCID100 Wave 2, slot 19** — first-pass replication scoping for:

> Belov O., Chigasova A., Pustovalova M., Osipov A., Eremin P., Vorobyeva N., Osipov A.N. (2023).
> *Dose-Dependent Shift in Relative Contribution of Homologous Recombination to DNA Repair after
> Low-LET Ionizing Radiation Exposure: Empirical Evidence and Numerical Simulation.*
> **Current Issues in Molecular Biology** 45(9): 7352–7373. DOI **10.3390/cimb45090465**.
> PMID 37754249 · PMCID PMC10528584 · MDPI CC BY 4.0.

## What this replication attempts

The paper has two halves:

1. **Empirical** — γH2AX and Rad51 foci kinetics in human skin fibroblasts (Cell Applications
   106K-05a) at 0.25, 1, 2, 4, 6, 24 h after X-ray doses of 20, 40, 80, 160, 250, 500, 1000 mGy
   (40 mGy/min, RUB RUST-M1 200 kVp). Plus CENPF S/G2 fraction at 24 h.
2. **Simulation** — a 5-pathway mass-action ODE model (NHEJ + HR + SSA + micro-SSA + Alt-EJ,
   ~30 ODEs, ~50 rate constants) inherited from Belov et al. 2015 (JTB 366:115–130). Used to
   derive a continuous dose dependence of the HR contribution `P_HR(D)`.

This folder is a **first-pass scoping**, not a full replication. The full simulation replication is
feasible from the paper text alone but requires multi-day model implementation + parameter
verification work. See `REPORT.md` for the scoping verdict and `PROGRESS.md` for status.

## Quick start

```bash
cd ~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-hr-shift-low-let-dna-repair
python3 scripts/smoke_dsb_yield.py
# -> results/smoke_dsb_yield.csv, results/smoke_dsb_yield_grid.csv,
#    figures/smoke_dsb_yield.png, logs/smoke_dsb_yield.log
```

Runtime: <1 s. Deps: `numpy`, `matplotlib`. No GPU, no network at runtime.

The smoke script verifies two closed-form quantities directly readable from Appendix C of the
paper without solving any ODE:

* **Initial DSB yield** N0 = α(L)·D with α(L) = 27.5 · exp(−2.43·10⁻³ · L). At L≈0.3 keV/μm
  (low-LET X-rays), N0 ranges from 0.55 DSBs/cell at 20 mGy to 27.5 DSBs/cell at 1 Gy — consistent
  with the standard ~35 DSB/Gy/cell estimate (cf. MEDRAS-MC, Cucinotta 2008).
* **Irreparable-DSB fraction** Nirrep(D) piecewise function. Non-monotonic with a peak ≈0.087
  near 250 mGy and a floor of 0.01 at ≥1 Gy. This directly encodes the paper's central
  qualitative claim: residual γH2AX foci at 24 h are disproportionately high after low-to-
  moderate doses.

## Layout

```
README.md                       this file
PROGRESS.md                     execution status + decisions log
REPORT.md                       FIRST-PASS REPORT + replication verdict
ARTIFACT_MANIFEST.md            paper, code, data inventory
paper/
  paper_pmc.pdf                 Europe PMC render PDF (10 pp)
  fulltext.xml                  Europe PMC JATS XML
  fulltext.md                   stripped markdown of the XML
  europepmc.json                Europe PMC search hit (authors, IDs)
  supp_list.json                supplementary-files probe (EPMC returned 500; empty regardless)
artifacts/
  equations_A4_A7.txt           verbatim ODE systems extracted from disp-formula blocks
  table_A1_parameters.csv       Appendix C parameter table, cleaned
scripts/
  smoke_dsb_yield.py            closed-form smoke script (no ODE solve)
results/
  smoke_dsb_yield.csv           7 paper dose points
  smoke_dsb_yield_grid.csv      1001-point dose grid
figures/
  smoke_dsb_yield.png           2-panel smoke figure
logs/
  smoke_dsb_yield.log           stdout from the smoke run
```

## Code & data availability (verbatim, from the paper)

> **Data Availability Statement.** Not applicable.

No GitHub, no Zenodo, no supplementary CSVs/code. The single repo cited (`varnivey/darfi`,
accessed 19 Sep 2016) is the manual foci-counting GUI, not the simulation. The simulation
model is presented as authors' own code, built on Belov et al. 2015 JTB (paywalled, no public
repo located).

## Compute footprint

* Smoke run: <1 s, CPU, 3 MB RAM.
* Full ODE-system replication (not done here): would be a single Python process with a stiff-ODE
  solver (`scipy.integrate.solve_ivp` LSODA) — minutes per dose, ~hour for a full 0–1 Gy sweep at
  0.1 mGy resolution as in the paper. Well within CherryRd's safe envelope; no HPC needed.

## Citations

Use the BibTeX entry below.

```bibtex
@article{Belov2023HRshift,
  title   = {Dose-Dependent Shift in Relative Contribution of Homologous Recombination to DNA
             Repair after Low-LET Ionizing Radiation Exposure: Empirical Evidence and Numerical
             Simulation},
  author  = {Belov, Oleg and Chigasova, Anna and Pustovalova, Margarita and Osipov, Andrey and
             Eremin, Petr and Vorobyeva, Nataliya and Osipov, Andreyan N.},
  journal = {Current Issues in Molecular Biology},
  volume  = {45},
  number  = {9},
  pages   = {7352--7373},
  year    = {2023},
  doi     = {10.3390/cimb45090465},
  pmcid   = {PMC10528584}
}
```
