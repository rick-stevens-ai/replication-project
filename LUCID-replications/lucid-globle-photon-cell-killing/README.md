# GLOBLE Kinetic Photon Cell-Killing Model — Replication

Replication of:

> Herr L, Friedrich T, Durante M, Scholz M. (2014) **A Model of Photon Cell Killing Based on the Spatio-Temporal Clustering of DNA Damage in Higher Order Chromatin Structures.** *PLoS ONE* **9**(1): e83923. doi:10.1371/journal.pone.0083923

## What this reproduces

The paper's "kinetically extended GLOBLE" (Giant LOop Binary LEsion) model — a five-level ODE
system describing the dynamics of isolated and clustered DNA double-strand breaks (DSBs) inside
1–2 Mbp chromatin "giant loops" during and after photon irradiation. Cell survival follows from
the asymptotic occupation of the two "lethal" levels via Eq. (18).

We reproduce:

- **Fig. 2** — dose-rate survival families for the RT112 and MT cell lines.
- **Fig. 3** — MT split-dose survival vs separation time, for 5+5 Gy and 6+6 Gy.
- **Fig. 4** — GLOBLE vs LQ + Lea-Catcheside equivalence in the Lea-Catcheside factor G.
- **Fig. 5** — isoeffective dose vs dose rate for pneumonitis and bone-marrow syndrome.
- **Fig. 6** — LL split-dose 5+5 Gy: split-dose fit vs. prediction from the dose-rate fit.

We also produce a `results/all_cell_lines_survival.json` table covering all 17 cell lines in
Table 2.

## Layout

```
.
├── README.md          this file
├── REPORT.md          claim-by-claim audit, friction tags, verdict
├── PROGRESS.md        chronological work log
├── paper.md           source paper (markdown extraction)
├── code/
│   ├── globle.py      core ODE + closed-form helpers
│   ├── cell_lines.py  cell-line parameter table (Table 2 of the paper)
│   └── make_figures.py reproduces Figs. 2, 3, 4, 5, 6
├── figures/           generated PNGs
└── results/           generated JSON
```

## How to rerun

Requires Python ≥3.10 with `numpy`, `scipy`, `matplotlib`.

```bash
cd ~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid-globle-photon-cell-killing
python3 code/make_figures.py
```

Expected runtime: about **20 s** on a modern laptop (the slowest piece is the bisection-based
isoeffective-dose search in Fig. 5; the ODE integration is cheap).

To exercise just the model and run consistency checks (high-rate limit → static GLOBLE; low-rate
limit → Eq. 38 closed form):

```bash
python3 - <<'PY'
import sys; sys.path.insert(0,'code')
from globle import GlobleParams, survival_static, survival_single_dose, survival_low_dose_rate_closed_form
p = GlobleParams(eps_i=0.00529, eps_c=0.195, hlt_i=0.485)   # RT112 from Table 2
for D in [1, 2, 4, 6, 8, 10]:
    s_static = survival_static(p, D)
    s_high   = survival_single_dose(p, D, 1e6)
    s_low    = survival_low_dose_rate_closed_form(p, D, 0.05)
    s_ode_lo = survival_single_dose(p, D, 0.05)
    print(f'D={D:>4.1f}  static={s_static:.4g}  ODE_hi={s_high:.4g}  Eq38_lo={s_low:.4g}  ODE_lo={s_ode_lo:.4g}')
PY
```

## Implementation notes

- ODEs integrated with `scipy.integrate.solve_ivp(method="LSODA", rtol=1e-9, atol=1e-12)`.
- `t = ∞` is approximated by relaxing 50 h beyond the beam-off time, then cross-checked against
  the closed form l_x(∞) = l_x(T) + ε_x · f_x(T) (Eqs. 20–21).
- All paper-fixed constants live in `globle.py`: α_DSB = 30 DSB/Gy/cell, N_L = 3000 domains,
  HLT_c = 5 h.

## Verification

- **High-dose-rate limit** of the ODE solver collapses to the static GLOBLE survival (Eqs. 6–7)
  to better than 0.3 % over D ∈ [1, 10] Gy.
- **Low-dose-rate limit** matches the closed form Eq. 38 to within a few percent over the same
  dose range (the small residual is the clustered-DSB contribution that Eq. 38 drops by
  construction).
- **LQ–GLOBLE equivalence** (Fig. 4) reproduces the paper's "lines lie on top of each other"
  claim across protraction times from 1 ms to >300 h, for both α/β = 1 Gy and α/β = 5.26 Gy
  hypothetical cell lines.

## Friction summary

1. **No supplement (File S1) available.** The paper's closed-form approximation is referenced
   but not present in the markdown extract; we implement the full ODE numerically and recover
   the same behaviour Fig. 4 documents.
2. **No raw experimental data points.** The original authors digitised plots with
   "GetData Graph Digitalizer"; the underlying numbers are not in the source. We reproduce
   model curves under the published Table 2 parameters and confirm qualitative and
   parameter-consistent claims rather than overlaying measured markers.
3. **Caption typo (Fig. 4).** The paper's Figure 4 caption gives ε_i = 0.002 for the
   α/β = 5.26 Gy hypothetical cell line, but Eq. (8) with α = 0.15/Gy and α_DSB = 30/Gy/cell
   demands ε_i = 0.005. We use the internally consistent value (ε_i = 0.005, ε_c = 0.20) so the
   GLOBLE↔LQ equivalence holds as the paper claims. This is a probable typo in the original
   manuscript; see REPORT.md.

See REPORT.md for the full claim-by-claim ledger.
