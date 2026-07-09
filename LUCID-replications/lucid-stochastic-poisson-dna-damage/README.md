# lucid-stochastic-poisson-dna-damage

Replication of:

> Cordoni, F.G. *On the Emergence of the Deviation from a Poisson Law in
> Stochastic Mathematical Models for Radiation-Induced DNA Damage: A System
> Size Expansion.* **Entropy 2023, 25(9), 1322.**
> DOI: <https://doi.org/10.3390/e25091322>

The paper takes the master equation of the *Generalized Stochastic
Microdosimetric Model* (GSM²) for sub-lethal `X` and lethal `Y` DNA lesions
and performs a van-Kampen system-size expansion. At order √K it recovers
the deterministic MKM ODEs; at order 1 the fluctuations satisfy a 2-D
linear Fokker–Planck equation whose solution is Gaussian. The paper's
central claim is that the **lethal-lesion distribution is sub-Poissonian**
(variance strictly less than mean) because of the negative covariance
induced by the clustering reaction `2X → Y`.

The paper publishes no code or data ("No new data have been created").
This repo re-implements the model from the equations alone.

## Layout

```
.
├── code/
│   ├── gsm2_model.py        # Gillespie SSA, macro ODE, moment ODE, OU paths
│   └── run_replication.py   # driver: produces results/ and figures/
├── results/
│   ├── summary.json         # headline numerics + claim-by-claim status
│   ├── histogram_summary.json
│   └── moments_vs_time.csv  # x̄, ȳ, c_ξξ, c_ξv, c_vv (ODE) and SSA moments
├── figures/
│   ├── fig1_histograms.png      # SSA vs Gaussian (vs Poisson) at 3 times
│   ├── fig2_moments_vs_time.png # moment trajectories, LNA lines + SSA markers
│   ├── fig3_sample_paths.png    # 10 paths SSA vs OU
│   └── fig4_fano_factor.png     # Fano(Y) vs time — Poisson-deviation diagnostic
├── REPORT.md                # full audit, claim-by-claim, verdict
├── PROGRESS.md              # chronology + blockers
└── README.md                # this file
```

## How to rerun

### Requirements
- Python ≥ 3.10
- `numpy`, `scipy`, `matplotlib` (any version from the last ~5 years)

Tested with `numpy 2.4.3`, `scipy 1.17.1`, `matplotlib 3.10.8` on macOS / CherryRd.

### One command

```bash
cd code
python run_replication.py
```

This re-creates everything under `results/` and `figures/` in roughly
**~11 seconds** on a 2024 iMac (20 000 SSA realisations + 20 000 OU paths
on a 301-point time grid). Memory peak is well under 1 GB.

### Parameters

All knobs live in `code/gsm2_model.py` (`PAPER_PARAMS`) and
`code/run_replication.py`:

| symbol | value | meaning |
|---|---|---|
| `x0` | 100 | initial sub-lethal lesions |
| `y0` | 0 | initial lethal lesions |
| `r` | 4.0 | sub-lethal repair rate |
| `a` | 0.1 | direct sub-lethal → lethal rate |
| `b_tilde` | 0.01 | clustering rate `b/K` (Eq. 6 of the paper) |
| `t_max` | 1.5 (a.u.) | simulation horizon |
| `N_SSA` | 20 000 | number of Gillespie realisations |
| `N_OU`  | 20 000 | number of OU sample paths |

These match the values stated in Sec. 4 of the paper (`r = 4, a = 0.1,
b̃_K = 0.01`, `x₀ = 100`, `y₀ = 0`); the paper's figures are at
`t ∈ {0.5, 0.7, 0.9}` a.u.

## What's in `results/summary.json`

The driver writes the headline numerics plus a self-check of each of the
paper's three central qualitative claims:

- `claim_subpoissonian_lethal` → `subpoissonian: true` (Var(Y) ≪ E[Y]).
- `claim_negative_covariance` → `always_nonpositive_*: true` (Cov(X,Y) ≤ 0 for all t).
- `claim_mkm_macroscopic_limit` → absolute error between deterministic
  ODE means and SSA means (both `<0.1` at t=1.5).

See `REPORT.md` for the audit table and verdict.

## Friction tags

- **F1** — code unavailable from author (re-implemented from text + equations).

No data-availability friction — the paper is theoretical.
