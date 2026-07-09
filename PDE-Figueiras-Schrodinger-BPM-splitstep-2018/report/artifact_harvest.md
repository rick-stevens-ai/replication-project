# Artifact Harvest

| Artifact | Source | Detail |
|---|---|---|
| Paper PDF | `https://iopscience.iop.org/article/10.1088/1361-6404/aac999/pdf` (OA, CC-BY 3.0) | 8 pp, 2,248,218 bytes, saved `work/figueiras.pdf`; text `work/figueiras.txt` (656 lines via `pdftotext -layout`) |
| OA status | Unpaywall `10.1088/1361-6404/aac999` | is_oa=true, publisher host, IOP |
| Crossref metadata | api.crossref.org | title/authors/venue confirmed |

**Not harvested:** the paper's own supplementary code library ("BPM library" + 20 example scripts, ref [4]) is hosted as IOP supplementary material and was **deliberately not downloaded/used** — this is an *independent* re-implementation. Our solver (`work/bpm.py`) was written from the equations in the paper (eq. 1, eq. 2 algorithm steps I–V) with no reference to the authors' code, precisely so the reproduction is independent.

**Checksums (sha256, local):**
```
$(shasum -a 256 work/figueiras.pdf)
```
(see attempt_log for exact value)
