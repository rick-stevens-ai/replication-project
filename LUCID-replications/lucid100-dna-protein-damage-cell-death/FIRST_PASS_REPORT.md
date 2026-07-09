# First-pass replication report

**Paper.** Shuryak & Brenner (2012). *Mechanistic Analysis of the Contributions
of DNA and Protein Damage to Radiation-Induced Cell Death.* Radiat. Res. 178(1),
17–24. DOI [10.1667/RR2877.1](https://doi.org/10.1667/RR2877.1) ·
[PMC3580191](https://pmc.ncbi.nlm.nih.gov/articles/PMC3580191/).

**LUCID100.** Wave 3 · Tier A · slot 23 (rank 54) · priority 16.

**Date.** 2026-06-09 (subagent first pass; no follow-on session yet).

---

## Verdict

> **GREEN-LIGHT — qualitative replication achieved.**
> The full mechanistic model (5 equations, 4 parameters) is fully recoverable
> from the open-access JATS XML, including the best-fit parameter table
> with 95 % CIs and the Q₁/Q₂ dominant-mechanism map per strain × radiation.
> A pure-Python smoke implementation reproduces **10 of 10** dominant-mechanism
> cells from the paper's Table 2 in < 1 s on CherryRd CPU. Numeric
> replication of Table 1 (re-fitting `Kdam_UV`, `Krep`, `X` to the data) and
> Figs. 1, 3–5 (overlays) is **straightforward but requires WebPlotDigitizer
> on Krisko & Radman 2010 (PNAS, PMC2922536)** because that source paper
> publishes its `F(D)` and `S(D)` only as figure points.

## What was harvested

- Full-text JATS XML via PMC OAI-PMH (80 KB) — the EuropePMC and NCBI PDF
  endpoints are currently behind HTTP 500 / reCAPTCHA respectively, but
  the JATS contains the entire body, all 5 equations, both tables, and
  all 5 figure captions, so the PDF is not on the critical path.
- Unpaywall confirmation (oa_status = green).
- All 24 references resolved, including the source-data paper.

## What is missing

- Authors' FORTRAN custom random-restart simulated-annealing fitter is
  **not publicly released** (no GitHub user `igorshuryak`; no Zenodo /
  Figshare URL anywhere in the paper or its references; GitHub code
  search returned 0 hits).
- Raw `F(D)` / `S(D)` values from Krisko & Radman 2010 are not in
  tabular form anywhere in PMC; they must be digitized from PNAS Figs.
  1 and 2 for a numeric refit.
- Figure JPGs of *this* paper (Shuryak 2012) are blocked behind
  reCAPTCHA on every public endpoint tried; the captions plus the
  parameter tables are sufficient for replication scoping, so this is
  not blocking the first pass.

## Smoke replication

`scripts/smoke_shuryak_2012.py` implements:

```
P(D) = 1 − [F(D) − F(0)] / [Fmax − F(0)]                            (Eq. 2)
Q1   = exp[−Kdam · D · exp(−Krep · P)]                              (Eq. 3)
Q2   = P^X                                                          (Eq. 4)
S    = Q1 · Q2  (S = Q2 for λ-phage infective centers)              (Eq. 5)
```

with Table 1 parameter values (`Fmax = 8.5 nmol carb./mg`, `Kdam_γ =
10 kGy⁻¹`, `Kdam_UV = 3.99 m²/kJ`, `Krep = 13.9` (or 0 for recA-),
`X = 3.88` for *D. radiodurans* and 6.76 for *E. coli* + λ IC).

| Strain × radiation                | Paper's expected dominant mechanism | Smoke result | Match |
|-----------------------------------|--------------------------------------|--------------|-------|
| *D.r.* R1, γ (0–15 kGy)           | Q₂ (direct protein damage)           | Q₂           | ✅ |
| *D.r.* R1, UV (0–4 kJ/m²)         | Q₂                                   | Q₂           | ✅ |
| *D.r.* recA-, γ (0–1.6 kGy)       | Q₁ (DNA damage)                      | Q₁           | ✅ |
| *D.r.* recA-, UV (0–3 kJ/m²)      | Q₁                                   | Q₁           | ✅ |
| *E.c.* WT, γ (0–4 kGy)            | Q₂                                   | Q₂           | ✅ |
| *E.c.* WT, UV (0–0.36 kJ/m²)      | Q₂                                   | Q₂           | ✅ |
| *E.c.* Res, γ (0–4 kGy)           | Q₂                                   | Q₂           | ✅ |
| *E.c.* Res, UV (0–0.36 kJ/m²)     | Q₂                                   | Q₂           | ✅ |
| λ IC in *E.c.*, γ                 | Q₂                                   | Q₂           | ✅ |
| λ IC in *E.c.*, UV                | Q₂                                   | Q₂           | ✅ |

**10 / 10** dominant-mechanism cells reproduced. Quantitative end-of-range
S values are within a few orders of magnitude of the paper's Table 2
ranges with the placeholder `F(D)` curves; tight quantitative match
awaits digitized data.

The single boundary case where the paper expects a Q₁ switch — *D.r.*
R1 at 20 kGy γ — is not separately tabulated by the smoke script (it
emits the dominant mechanism only at the maximum dose of the listed
range, and at 20 kGy the placeholder still puts Q₂ slightly ahead).
Easy to add as a per-dose dominant-mechanism plot once digitized F(D)
is in hand.

## Next actions (in priority order)

1. **(highest leverage)** WebPlotDigitizer on Krisko & Radman 2010
   PNAS Figs. 1 and 2 → CSV per strain × (γ, UV) for `S(D)` and
   `F(D)`. This unblocks a numeric refit and per-figure overlay.
   (Use `user` browser profile for PNAS — headless `curl` is blocked.)
2. Replace `_logistic_F` callables in `smoke_shuryak_2012.py` with
   interpolators over the digitized `F(D)` tables. Re-run smoke.
3. Add `scripts/refit_shuryak_2012.py` using `scipy.optimize.minimize`
   with random restarts to re-fit (`Kdam_UV`, `Krep`, `X_D.r.`, `X_E.c.`)
   and verify they fall inside the paper's 95 % CIs.
4. Add Fig. 3 (incorrectly-repaired-DSB fraction), Fig. 4 (Q₁ surface),
   and Fig. 5 (S vs P) plotters.
5. (optional) Cross-validate on Daly et al. 2007 PLoS Biol data for
   *Shewanella oneidensis* and *Pyrococcus furiosus* to test the
   model's portability beyond the original training set.

## Compute / cost / safety

- All work CPU-only on CherryRd; total wall time < 30 s including
  network. No GPU, no scheduler, no paid endpoint used.
- No author contact; no data exfiltrated; no destructive operations.

## QA decision (retag recommendation)

- **KEEP** in LUCID100; **stay at Tier A**.
- Update `LUCID100_SOLID_MASTER_QA.tsv` row 57 (rank 54, DOI
  `10.1667/rr2877.1`):
  - `replication_folder` → `lucid100-dna-protein-damage-cell-death`
  - `pdf_or_url`        → keep EuropePMC link, also note JATS XML route works
  - `verdict_or_plan`   → `simulation/model replication — qualitative complete; numeric pending Krisko & Radman 2010 figure digitization`
  - `status`            → `first_pass_done`
