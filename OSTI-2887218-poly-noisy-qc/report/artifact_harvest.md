# Artifact harvest — OSTI 2887218

## Paper
- `https://www.osti.gov/servlets/purl/2887218`  →  `paper.pdf` (1,202,652 bytes, PDF v1.4, 31 pages, sha256 to be computed)
- Journal version: *Phys. Rev. X* **15**, 041018 (2025), DOI [10.1103/xct1-7kf2](https://doi.org/10.1103/xct1-7kf2). Featured in *Physics*. CC BY 4.0.

## Text extraction
- `extraction/marker.md` — actually `pdftotext -layout` fallback (marker not attempted because Anthropic PDF backend was credit-blocked at extraction time; nougat variant produced separately). 2,227 lines, 100 % readable ASCII math.
- `extraction/nougat.mmd` — nougat 0.1.x run in conda env `/gpustor/stevens/anaconda3/envs/nougat` on uicgpu (`facebook/nougat-small` checkpoint), 31 pages, `--no-skipping`.

## Code / data availability from the paper
- **NONE.** No GitHub URL, no Zenodo DOI, no supplementary code/data statement. The paper is entirely theoretical; the three figures are schematics with no underlying numerical data.

## Ancillary sources used
- No external code was reused.  `numpy 1.23.5` + `scipy 1.10.1` on uicgpu Python 3.10.  Haar-random 2-qubit gates via `qr(randn+1j·randn)` with phase-fix.
- No LLM API calls were required for this replication (the paper's claims are testable numerically with a self-contained 4-qubit simulator).

## Compute used
- **uicgpu** (8×A100, 255 cores, 2 TB RAM). Only CPU numpy was used — the full experiment (V1 + V3 + RMS) completes in < 90 s of wall time on a single core.
- 2 orphaned python processes from an early buggy run had to be manually killed via `ssh uicgpu 'kill -9 <pid>'` after `process kill` only reaped the local SSH driver.

## Files placed in this replication dir
| Path | Purpose |
|---|---|
| `paper.pdf` | fetched from OSTI |
| `extraction/marker.md` | `pdftotext -layout` text (marker fallback) |
| `extraction/nougat.mmd` | nougat MathPix-markdown extraction |
| `work/replication.py` | Algorithm 1 implementation + V1/V3 driver |
| `work/rms_experiment.py` | V2 (RMS-over-ensemble) driver |
| `work/dev_verify.py` | development-time small-system sanity check |
| `work/dev_schrod_pauli.py` | Schrödinger-in-Pauli-basis alternative simulator used to isolate bug B2 |
| `report/evidence/results.json` | V1 & V3 results (JSON) |
| `report/evidence/rms.json` | V2 RMS results (JSON) |
| `report/evidence/run.log` | full stdout of main run |
| `report/evidence/rms.log` | full stdout of RMS run |
| `report/REPORT.md`, `report/REPORT.tex` | full report (markdown + LaTeX) |
| `report/brief.md` | 1-paragraph brief |
| `report/attempt_log.md` | chronological log |
| `report/open_questions.json` | 5 new open questions |
| `report/workflow.md` | workflow + tools + effort |
| `report/artifacts_summary.md` | quick artifact summary |
| `report/failure_analysis.md` | root-cause debugging notes |
