# Artifact Harvest

| Artifact | URL / Source | Size / Version | Notes |
|---|---|---|---|
| NodePy package | PyPI `nodepy` | v1.0.1 | Installed into `work/.venv` via pip |
| NodePy source | https://github.com/ketch/nodepy | (via pip) | Reference implementation by paper author |
| JOSS paper | DOI 10.21105/joss.02515 | OA, JOSS | Metadata + methods narrative |
| Dahlquist test problem | y'=−y, y(0)=1, exact e^(−t) | Analytical | No download needed |
| Butcher tableaux | Loaded via `nodepy.runge_kutta_method.loadRKM(name)` | Built-in | 10 methods: RK44, DP5, Heun33, SSP22, SSP33, SSP53, SSP104, Merson43, Fehlberg45, CK5, BuRK65 |

## Evidence files
- `evidence/evidence_orders.txt` — order + SSP-coef table (10 methods)
- `evidence/evidence_convergence.txt` — empirical convergence log
- `evidence/convergence.csv` — machine-readable errors vs N
- `evidence/stability_RK44.png` — stability region plot
- `evidence/stability_DP5.png` — stability region plot
- `evidence/stability_SSP104.png` — stability region plot

## LLM endpoint used (judge)
- Argo proxy `http://localhost:44497/v1` (FREE, per hard rule)
- Model `argo:claude-opus-4.7`
