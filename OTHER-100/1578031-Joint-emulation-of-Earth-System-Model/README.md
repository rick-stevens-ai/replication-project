# Joint emulation of Earth System Model temperature-precipitation realizations with internal variability and space-time and cross-variable correlation: fldgen v2.0 software description

- **OSTI ID:** 1578031
- **Rank:** #12
- **Replication Score:** 10/10
- **Open-Source Tools:** Yes
- **Code Repository:** Yes — https://github.com/jgcri/fldgen
- **Tools:** R (original), Python (this replication)

## Why This Paper
Open-source R package with public/synthetic data, fully specified methodology, code and test data available, and clear quantitative validation. End-to-end reproducible by AI.

## Replication Status
- [x] Paper reviewed
- [x] Code/tools identified
- [x] Algorithm reimplemented in Python
- [x] Results produced (10 realizations from synthetic ESM data)
- [x] Results validated against training data statistics
- [ ] Compared against original R package output (not done — see REPORT.md)

## Quick Start

```bash
cd replication/code
python3 run_replication.py
```

Produces figures in `replication/figures/` and data in `replication/data/`.

## Deliverables

| Path | Description |
|------|-------------|
| `REPORT.md` | Full replication report with validation metrics |
| `replication/code/fldgen.py` | Python implementation of fldgen v2.0 algorithm |
| `replication/code/synthetic_esm.py` | Synthetic ESM data generator |
| `replication/code/run_replication.py` | Main replication + validation script |
| `replication/data/` | Training data + 10 generated realizations + metrics |
| `replication/figures/` | 4 validation figures |

## Key Results

| Metric | Value | Interpretation |
|--------|-------|----------------|
| Spatial rank correlation RMSE | 0.056 | Excellent preservation |
| Marginal distribution (KS test) | 100% pass | Perfect |
| Cross-variable correlation r | 0.93 | Strong preservation |
| T variance ratio | 0.98 | Near-perfect |
| P variance ratio | 0.97 | Near-perfect |
| ACF mean absolute error | 0.067 | Good preservation |

## Dependencies
- Python 3.8+
- NumPy, SciPy, Matplotlib
