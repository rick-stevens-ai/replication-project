# LUCID100 slot 66 (rank 97, Wave 7) — Belov et al. 2015: Quantitative model of major DSB repair pathways

**Paper:** Belov O.V., Krasavin E.A., Lyashko M.S., Batmunkh M., Sweilam N.H. (2015). *A quantitative model of the major pathways for radiation-induced DNA double-strand break repair.* **Journal of Theoretical Biology** **366**, 115–130.
**DOI:** [10.1016/j.jtbi.2014.09.024](https://doi.org/10.1016/j.jtbi.2014.09.024)
**PMID:** 25261728  (Europe PMC `isOpenAccess: N`, no PMC ID)
**Preprint (open):** JINR Communication E19-2014-39, Dubna 2014 — `publications.jinr.ru/record/152491` and `inis.iaea.org/.../45110611.pdf`.
**LUCID100 master:** rank 97, Wave 7, B-tier, priority 12, `candidate_curated`, `simulation/model replication`.
**This pass:** Wave 7 backfill slot 66, first-pass artifact harvest + minimal smoke replication.

## What the paper does

Develops a deterministic ODE-based biochemical-kinetics model of the three "major" mammalian DSB repair pathways with a shared induction term and a γ-H2AX foci read-out:

- **NHEJ** (Eqs A.1, 9 ODEs): Ku → DNA-PKcs/Artemis → bridge → LigIV/XRCC4/XLF (+PNKP, Pol X) → re-ligated dsDNA.
- **HR** (Eqs B.1, 8 ODEs): MRN/CtIP/ExoI/Dna2 end-resection → RPA-ssDNA → Rad51/BRCA2 filament → D-loop → dHJ → resolution.
- **SSA** (Eqs C.1, 5 ODEs): Rad52 annealing of resected ends → ERCC1/XPF flap cutting → LigIII sealing.
- **Shared induction** (Eq 1): `dn0/dt = α(L)·dD/dt·N_ir − V_NHEJ − V_HR − V_SSA`, with `α(L) = a·exp(−b·L)`, `a=27.5`, `b=2.43e-3`, `L` in keV/µm; `N_ir` is the LET- and repair-status-dependent irreparable fraction (Table A.2, 16 rows).
- **γ-H2AX foci** (Eq A.1 last line, Eqs 22–24): saturable Michaelis-Menten production `K9·[Sum]·[H2AX]/(K10+[Sum])`, minus `K11·[dsDNA] + K12·[γ-H2AX]`; `K10 = 1.93e-7 / N_ir M`.

**No alt-EJ / MMEJ branch** is included (acknowledged limitation in the discussion).

The paper is *not* a damage-Monte-Carlo paper — it is a closed-form mean-field kinetic system whose parameters are fitted to literature time-courses (Ku binding, DNA-PKcs recruitment, Rad51 foci, γ-H2AX foci) across LET = 0.2–236 keV/µm and three γ-H2AX repair-deficient cell lines (DNA-PKcs⁻, BRCA2⁻, ERCC1/XPF⁻).

## What this folder is

A first-pass artifact harvest plus a faithful local reimplementation of the **complete coupled 22-ODE system** as written in Appendices A–C. Parameters and initial conditions are taken **verbatim** from Tables A.1 and A.2 of the JINR preprint (= published Appendix). The smoke run reproduces the qualitative behaviour reported in Figs 5–7:

- Fast NHEJ component (half-time ≈ tens of minutes).
- Slow HR/SSA tail.
- γ-H2AX rise within minutes, peak around 30–60 min, slow decay over 24 h with a residual proportional to `N_ir`.

We do **not** re-fit any rate constants — the goal is a *smoke* replication that the equations as published do what the paper says they do.

## Layout

```
.
├── README.md                          # this file
├── PROGRESS.md                        # task log
├── FIRST_PASS_REPORT.md               # verdict + smoke results
├── MANIFEST.json                      # artifact list + provenance
├── artifacts/
│   ├── belov2015_inis_iaea.pdf        # JINR preprint E19-2014-39 (open access via IAEA INIS)
│   ├── belov2015_inis_iaea.txt        # pdftotext extraction
│   └── epmc_meta.json                 # Europe PMC metadata for the JTB version
├── refs/
│   └── (empty — no separate refs harvested in first pass)
├── scripts/
│   └── smoke_belov2015.py             # full 22-ODE NHEJ+HR+SSA+γ-H2AX integrator
└── results/
    ├── smoke_results.json             # parameters used + summary statistics
    └── smoke_traces.png               # n0, NHEJ/HR/SSA contributions, γ-H2AX vs time
```

## How to run

```bash
cd scripts
python3 smoke_belov2015.py            # writes ../results/smoke_results.json and ../results/smoke_traces.png
```

Requires: `python3`, `numpy`, `scipy`, `matplotlib`. CPU-only, runs in well under a minute on CherryRd; **no heavy compute needed**.

## Licence / availability

- **JTB paper itself:** Elsevier, not OA (Europe PMC `isOpenAccess: N`).
- **JINR preprint E19-2014-39:** open access via INIS/IAEA mirror and `publications.jinr.ru`; same equations and parameter tables as the JTB appendices.
- **Author code:** not deposited — paper states "computations done at JINR LIT facilities" but no GitHub/Zenodo. No data/code DOI.
- **Experimental data used for fitting:** all literature, cited; no new experimental data in this paper.

## QA recommendation

**Retag → `replicated_smoke` / `KEEP: relevant and replication-plausible`.** The full model is reproducible from the JINR preprint alone with no author contact required.
