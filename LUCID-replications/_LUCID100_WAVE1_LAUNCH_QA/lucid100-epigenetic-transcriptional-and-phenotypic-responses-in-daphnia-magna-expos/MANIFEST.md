# Artifact Manifest — LUCID100 Wave 1 Slot 5

Paper: Thaulow et al. 2020, *Environ. Res.* 190, 109930. DOI 10.1016/j.envres.2020.109930.

## Files in this folder

```
README.md                              # Replication brief, claims, acceptance criteria
PROGRESS.md                            # Running progress log
FIRST_PASS_REPORT.md                   # Verdict + evidence
MANIFEST.md                            # This file
artifacts/
  thaulow2020_envres.pdf               # Publisher preprint, 13 pp, 7.94 MB
                                       # Source: Utrecht University repository, hdl 1874/408631
                                       # Downloaded 2026-06-09 via curl from dspace.library.uu.nl
  thaulow2020_envres.txt               # pdftotext -layout extraction, 796 lines
repro/
  digitized_dose_response_template.csv # Empty skeleton for hand-digitised dose-response values
  pca_variance_smoke.py                # PCA smoke test (PC1+PC2 ≈ 85.41 %)
```

Mirror under workspace (identical PDF + txt):

```
/Users/stevens/.openclaw/workspace/lucid-replications/slot5-daphnia/artifacts/
```

## File provenance

| Path                                          | Source                                                            | Notes                                |
| --------------------------------------------- | ----------------------------------------------------------------- | ------------------------------------ |
| `artifacts/thaulow2020_envres.pdf`            | `https://dspace.library.uu.nl/bitstream/handle/1874/408631/1_s2.0_S0013935120308252_main.pdf?sequence=1` | OA publisher preprint, retrieved with `curl -sL` |
| `artifacts/thaulow2020_envres.txt`            | `pdftotext -layout artifacts/thaulow2020_envres.pdf`              | macOS / Homebrew poppler             |

## What is *not* in this folder (and why)

- **No GEO/SRA/ENA accession dump.** The paper deposits nothing. Confirmed by full-text search.
- **No Elsevier MMC supplementary files.** Probed `ars.els-cdn.com/.../mmc{1..4}.{pdf,docx,xlsx}` → all 404. Confirmed by PDF inspection that no "Appendix A. Supplementary data" section exists.
- **No primer / probe sequence table.** Primers are cited to three secondary papers (Gomes 2018, Lindeman 2019b, Song 2020); those would need their own harvest if a future replication needed them.
- **No code.** The authors used GraphPad Prism v8.0.2 and XLSTAT v2019.3.2 (proprietary GUI tools). There is no code to mirror.

## Environment for the optional smoke test

```
python >= 3.9
numpy
scikit-learn   # for sklearn.decomposition.PCA
pandas         # for CSV ingest
```

Install ad-hoc (uv-managed env optional):
```
pip install --quiet numpy pandas scikit-learn
```

The smoke test currently runs on a synthetic dose-response matrix and prints a PASS/FAIL line against the 85.41 % PC1+PC2 acceptance metric. It is intended to be re-run once `repro/digitized_dose_response_template.csv` is populated by hand from Figs. 1, 2, 3, 6.

## SHA-256

```
$ shasum -a 256 artifacts/thaulow2020_envres.pdf
$ shasum -a 256 artifacts/thaulow2020_envres.txt
```

(See live hashes printed in `repro/sha256.txt` if regenerated.)
