# Workflow — lucid-bnct-radioresistant-hcc

## Provenance
- **Paper:** Huang et al. 2022, *J. Hepatocell. Carcinoma*, DOI [10.2147/JHC.S383959](https://doi.org/10.2147/JHC.S383959)
- **Source PDF SHA-cited filename:** `2c94a15708907c2998f2f6db1ac1b1e9186b39cd.pdf`
- **License:** CC BY-NC 3.0 (Dove Medical Press) — open access, redistribution allowed with attribution
- **Set:** LUCID
- **Replication run:** 2026-05-30 (LaTeX backfill: 2026-07-06)

## Pipeline (as executed)

1. **Ingest.**
   - Locate PDF by SHA-cited filename in the LUCID PDF corpus.
   - Read title/abstract/methods to confirm identity: BNCT vs γ-ray on HepG2 (parental) and HepG2-R (acquired-radioresistant) hepatocellular carcinoma cell lines.

2. **Extract text-quoted quantities.**
   - Table 1 (dose × dose-rate × irradiation time for γ-ray).
   - Table 4 (D10 for γ-ray, D10 for BNCT, RBE per cell line).
   - Fig 1C text-quoted mean survival fractions at 1, 2, 5 Gy for each of HepG2 and HepG2-R γ-ray series.
   - Fig 3B: no text-quoted per-dose SF — must be digitized from figure.

3. **Digitize Fig 3B (BNCT clonogenic).**
   - Manual point extraction from published figure (BNCT panel).
   - Mark as digitization-limited in downstream provenance.

4. **Recompute RBE arithmetic** (`code/replicate.py`).
   - RBE = D10(γ) / D10(BNCT).
   - Compare vs paper Table 4.
   - Output: `results/rbe_table.csv`.

5. **LQ fits.**
   - Fit S(D) = exp(-αD − βD²) via scipy.optimize.curve_fit to:
     - γ-ray: three text-quoted mean SFs per line.
     - BNCT: digitized SFs from Fig 3B.
   - Solve D10 numerically from fitted (α, β).
   - Output: `results/fit_parameters.csv`.

6. **Table 1 internal-consistency check.**
   - Compute expected t = 60·D / dose_rate for each row.
   - Compare vs listed t.
   - Output: `results/table1_check.csv`.

7. **Plot.**
   - `figures/clonogenic_gamma.png`: paper points + LQ fit overlay for γ-ray.
   - `figures/clonogenic_bnct.png`: digitized BNCT points + LQ fit overlay.

8. **Mechanism panels (Figs 4–8, Table 5).**
   - Attempt: read text for fold-changes and directional claims.
   - Result: only summary fold-changes; no raw data; no supplementary tables.
   - Verdict: directional corroboration only — cannot independently verify magnitudes.
   - Do NOT fabricate quantitative agreement.

9. **Cross-check verdict against LUCID rubric.**
   - Fraction of quantitative claims that are cleanly reproducible: ~5/10.
   - Agreement on the reproducible subset: ~8/10 (γ-ray D10 within 3.5%; RBE arithmetic exact; BNCT D10 digitization-limited).
   - Verdict: **PARTIAL**.

## What was NOT executed (honest gaps)

- **Neutron beam Monte Carlo.** The paper cites the THOR reactor thermal-neutron column (Suppl. Fig 1 is the geometry schematic) but does not publish the MCNP/PHITS deck. We did not re-simulate the beam or the ¹⁰B(n,α) micro-dosimetry; we accepted the paper's absorbed doses at face value. For a BNCT paper this is the largest honest omission.
- **Raw ICP-AES ¹⁰B uptake traces (Table 2).** No per-well concentration data available; the 58–59 ppm plateau is a single summary value with no error bars.
- **Wet-lab mechanism panels (Figs 4–8).** No γH2AX foci counts, no Western densitometry, no `.fcs` flow files — cannot verify beyond direction.

## Reproducibility

The full replication is deterministic on the text-quoted γ-ray data:
```
python code/replicate.py
```
Produces `results/*.csv` and `figures/*.png` byte-identical modulo matplotlib
minor-version rendering.

The BNCT-side digitization is manual and not perfectly reproducible;
different digitizer coordinates within figure resolution shift D10 by a
few percent, which is smaller than the 18–40% offset vs paper D10.
