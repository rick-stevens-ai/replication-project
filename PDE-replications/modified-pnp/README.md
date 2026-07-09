# Modified Poisson–Nernst–Planck (mPNP) — Independent Replication

**Target paper.** Manman Ma, Zhenli Xu, Liwei Zhang (2021),
*Modified Poisson–Nernst–Planck Model with Coulomb and Hard-sphere
Correlations*, SIAM Journal on Applied Mathematics 81(4), 1645–1667,
DOI [`10.1137/19m1310098`](https://doi.org/10.1137/19m1310098).
Open preprint: **arXiv:[2002.07489v3](https://arxiv.org/abs/2002.07489)**
(22 pages, 7 figures). PDF cached locally as `paper.pdf` / `paper.txt`.

**Status.** Independent open-source replication. No code release was located
from the authors. Implementation is pure NumPy/SciPy, runs on a CPU.

## What is implemented

Equilibrium (steady-state) modified Poisson–Boltzmann form of the paper's
two-plate 1D problem in dimensionless form (Sec. 3 of the paper):

```
-2 eps^2 phi''(x) = sum_i z_i c_i(x),      |x| < 1 - a
c_i(x) = exp(-z_i*phi - mu^co_i - mu^hs_i)  (Boltzmann form, normalized to bulk c=1)
phi(+/-(1-a)) +/- (a/eta_s) phi'(+/-(1-a)) = V_+/-   (Robin BC)
```

Four model variants:

| variant | description | mu^hs | mu^co |
|---------|---|---|---|
| **MF**  | classical mean-field PNP / PB | 0 | 0 |
| **SC**  | short-range correlation only (hard-sphere) | MFMT | 0 |
| **LC**  | long-range Coulomb correlation only | 0 | WKB-GDH |
| **LS**  | both (LC + SC; the new model proposed in the paper) | MFMT | WKB-GDH |

* **MFMT** = modified Fundamental Measure Theory (Yu & Wu / Roth) reduced
  to 1D weighted densities (Eqs. 3.3–3.5 of paper).
* **WKB-GDH** = Wentzel–Kramers–Brillouin approximation of the generalized
  Debye–Hückel Green's function (Eq. 3.22) with local screening
  `kappa(x) = sqrt(I(x))/eps` and dielectric-mismatch parameter
  `gamma = (1 - eta_b)/(1 + eta_b)`.

Numerical scheme: damped Picard (fixed-point) iteration in *log-space* on
the densities, with separate damping for the potential, voltage continuation
for hard parameter regimes, and conservative per-step density-growth caps
to avoid runaway in the LS variant.

## Repository layout

```
modified-pnp/
├── README.md                 -- this file
├── REPORT.md                 -- replication report (claims, results, limits)
├── PROGRESS.md               -- working log
├── paper.pdf                 -- arXiv 2002.07489v3
├── paper.txt                 -- pdftotext extraction
├── code/
│   ├── mpnp.py                          -- solver core
│   ├── run_fig41_hs_convergence.py      -- MFMT convergence (paper Fig 4.1)
│   ├── run_fig43a_no_dielectric.py      -- gamma=0 weak-correlation case
│   ├── run_fig45_four_models.py         -- gamma=1 four-model comparison
│   └── run_convergence_study.py         -- mesh convergence of Q
├── figures/                              -- PNG figures (one per experiment)
├── results/                              -- JSON summaries + .npz numerical results
└── logs/                                 -- run logs (one per script)
```

## How to run

```bash
cd modified-pnp
python3 code/run_fig41_hs_convergence.py    # ~10 s
python3 code/run_fig43a_no_dielectric.py    # ~30 s
python3 code/run_fig45_four_models.py       # ~6 min (LC and LS are slow)
python3 code/run_convergence_study.py       # ~10 min
```

Requirements: Python 3.10+, NumPy 2.x, SciPy 1.x, Matplotlib 3.x. No GPU.

## Results at a glance

* **MFMT bulk consistency:** at uniform `c=1`, mu^hs(0) converges to the
  analytic Carnahan–Starling value 0.2388 with apparent 2nd-order
  accuracy in `h` (see `figures/fig41_hs_convergence.png`).
* **Weak-correlation regime (Fig 4.3a-like, gamma=0, V=0.5):** all four
  models agree on the diffuse charge `Q` within ~1.5% (paper claim ✓).
* **Strong-correlation regime (Fig 4.5-like, gamma=1, V=1):**
  ordering is `SC > MF > LS > LC` for `Q`, matching the paper's claim
  that hard-sphere correlations enhance `Q` while Coulomb correlations
  suppress it.
* **Mesh convergence:** `Q(N)` is monotone-decreasing with N, consistent
  with the paper's reported 2nd-order Slotboom-FDM accuracy.

See `REPORT.md` for the full claim-by-claim table, agreement scores, and
limitations.

## License

MIT for the original code in this directory. The arXiv preprint `paper.pdf`
is © its authors and included only for offline reference.
