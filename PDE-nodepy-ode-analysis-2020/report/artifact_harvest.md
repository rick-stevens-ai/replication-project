# Artifact Harvest — NodePy replication

## Public artifacts pulled

| # | Source | URL | Size | Notes |
|---|---|---|---|---|
| 1 | JOSS PDF | https://www.theoj.org/joss-papers/joss.02515/10.21105.joss.02515.pdf | 145,449 bytes | Saved as `paper.pdf`. Version 1.5 PDF, 4 pages, CC BY 4.0. |
| 2 | NodePy on PyPI | https://pypi.org/project/nodepy/1.0.1/ | (via pip) | Installed into `work/.venv/`. `pip show nodepy` → version 1.0.1. |
| 3 | NodePy on GitHub | https://github.com/ketch/nodepy | (not cloned; PyPI wheel used) | Referenced by paper. |
| 4 | NodePy docs | https://nodepy.readthedocs.io/en/latest/ | (web) | Referenced by paper. |

## Dependencies pulled transitively

`pip install nodepy numpy sympy matplotlib scipy` also installed (in `work/.venv/`): numpy 2.5.1, sympy 1.14.0, mpmath 1.3.0, matplotlib 3.10.7, scipy 1.16.3, plus their transitive tree (pillow, contourpy, cycler, fonttools, kiwisolver, pyparsing, packaging, python-dateutil, six).

## Data downloaded

None beyond the PDF and PyPI wheel. NodePy is a pure analysis tool; no external data corpora are required to test its capability claims — the "data" is the coefficients of the RK methods themselves, which ship with the package.

## Checksums

```
paper.pdf: 145,449 bytes  MD5 = 3124ea2c410741d26dfc0f75285eea64
```
