# Artifact harvest — QC-1801.04042

## Public artifacts pulled

| Artifact | URL / source | Size | Notes |
|---|---|---|---|
| Paper PDF | https://arxiv.org/pdf/1801.04042 | 146,890 B | 6 pages, arXiv:1801.04042v1 [quant-ph] 12 Jan 2018 |
| arXiv abstract HTML | https://arxiv.org/abs/1801.04042 | 41,303 B | metadata |
| Paper text (pdftotext) | `work/paper.txt` | 797 lines | extracted equations + block formulas |

## Third-party code / data

- **Stim** (Craig Gidney, Google Quantum AI): pip-installed v1.16.0. Used for uniform Clifford sampling (`stim.Tableau.random`), circuit → tableau conversion (`Tableau.to_circuit(method='elimination')`), and fast Clifford+Pauli-noise sampling (`stim.Circuit.compile_sampler`). Reference: https://github.com/quantumlib/Stim
- **NumPy** 2.5.0, **SciPy** 1.18.0 (curve_fit for exponential fitting), **matplotlib** for figures.

## No paper-supplied code
The paper is **theoretical** — it provides no reference simulation code, no supplementary numerical data, and no experimental values to compare against. It derives closed-form block-eigenvalue formulas for the twirled channel under each subgroup. This replication *implements* those formulas as theory predictions and *tests* them against Stim-simulated RB experiments with a known injected Pauli-noise channel.

## Nothing paywalled or gated
All materials pulled were open-access arXiv preprint + open-source software.
