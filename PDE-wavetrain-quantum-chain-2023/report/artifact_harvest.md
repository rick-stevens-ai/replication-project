# Artifact Harvest — WaveTrain (Riedel et al., 2023)

Every public artifact pulled during this replication.

| Artifact | URL / accession | Size | Notes |
|---|---|---|---|
| Preprint PDF | https://arxiv.org/pdf/2302.03725v2 | 706 379 B | `paper.pdf` (arXiv 2302.03725v2, 2023-02-13) |
| WaveTrain source | https://github.com/PGelss/wave_train.git (HEAD, shallow) | ~5 MB | `work/wave_train/` |
| scikit_tt source | https://github.com/PGelss/scikit_tt.git (HEAD) | pip-installed | into venv site-packages |
| WaveTrain bundled example | `work/wave_train/test_scripts/Exciton/tise_1.py` | in-repo | reference config we replay |
| WaveTrain other examples | `Exciton_Krylov/`, `Phonon/`, `Exc_Pho_Coupling/`, `Bath_Map_1/` | in-repo | not tested this pass |

## Provenance metadata

- arXiv preprint discovery via `export.arxiv.org/api/query` (title match: "WaveTrain" AND "tensor trains") — single hit.
- No paywalled resource accessed. Journal DOI (10.1063/5.0147314) resolves to AIP; we
  used the open arXiv preprint (identical content per common practice for JCP submissions).
- No datasets downloaded (this paper's replication is a code + solver check, not a
  data-analysis paper).

## Local dependencies (versions actually resolved)
- Python 3.12.13 (venv)
- numpy 1.26.4 (pinned <2)
- scipy 1.17.1
- matplotlib (latest at install time; not exercised in the benchmark)
- wave_train HEAD (Riedel-era layout)
- scikit_tt HEAD (with our 4-line dtype patch on `solvers/evp.py`)

## Modifications to third-party code
- `venv/lib/python3.12/site-packages/scikit_tt/solvers/evp.py` lines 381–384:
  cast `micro_op` to `np.complex128` when the deflation addend
  `shift * tmp @ tmp.conj().T` is complex-valued. Backup at
  `evp.py.bak`. Patch is minimal and preserves real-arithmetic behavior when
  possible. Same class of fix as reported by the sibling replication
  (`PDE-Riedel-WaveTrain-tensor-trains-2023`); the fix was derived independently
  from the traceback here.

## Checksums (for later cross-audit)
```
$ shasum -a 256 paper.pdf
(see evidence/paper.pdf.sha256 for the recorded value)
```
