# Artifact Harvest — Radia et al. 2021

Every public artifact pulled during this replication.

## Paper

| URL | Description | Size | SHA-256 (head 16) |
|-----|-------------|------|-------------------|
| https://arxiv.org/abs/2112.10567 | arXiv abstract page (v3, 20 Jun 2022) | 45 KB | – |
| https://arxiv.org/pdf/2112.10567 | Preprint PDF (v3) — Radia et al., "Lessons for adaptive mesh refinement in numerical relativity", Class. Quantum Grav. 39 135006 | 2251117 B (2.25 MB) | (computed at run time; see below) |

DOI (journal-of-record): 10.1088/1361-6382/ac6fa9 (IOP, Classical and Quantum Gravity 39, 135006).

## Code repos referenced (not built)

| URL | Description |
|-----|-------------|
| https://github.com/GRTLCollaboration/GRChombo | Open-source GRChombo repo used by the paper. Not built in this replication (Chombo+MPI+HDF5 stack, out of scope for a single wave slot). |
| https://www.grchombo.org/ | Project website. |
| https://arxiv.org/abs/2201.03458 | Companion paper: Andrade et al., "GRChombo: An adaptable numerical relativity code..." |

## What we did NOT pull

- No initial-data files (paper uses `TwoPunctures` spectral solver output; specific parameter files not published as artifacts alongside this paper).
- No pre-run waveform data / kick numbers (Fig. 6, Fig. 7). Paper Sec. 4.2 reports discretization errors ΔhA22/hA22 ≲ 1%, kick 3400–3700 km/s, but no numerical tables were extracted as reproducible artifacts.
- No code from the paper's supplementary material (paper does not appear to ship one; the AMR machinery lives in the GRChombo repo itself).

## Locally produced artifacts

| Path (relative to target dir) | Description |
|-------------------------------|-------------|
| `work/paper.pdf` | The arXiv preprint. |
| `work/paper.txt` | pdftotext of the above (2463 lines). |
| `work/abs.html` | arXiv abs page. |
| `work/amr_wave.py` | 1D scalar-wave AMR reference implementation (~500 lines). |
| `work/llm_judge.py` | LLM judge script that calls the Argo proxy. |
| `work/run.log`, `work/run2.log` | Two runs of amr_wave.py (initial + retuned truncation threshold). |
| `work/judge.log` | LLM judge output. |
| `report/evidence/amr_wave_results.json` | All numerical results as machine-readable JSON. |
| `report/evidence/llm_judge_verdict.json` | LLM judge JSON verdict with per-claim analysis. |

## Checksums

Computed at report-write time:
```
file, sha256, size
work/paper.pdf, 714738b8819e00b648f27cac8bfd5b68437b612aaa2fb036542fa162b991cc17,  2251117
work/paper.txt, a09b6a90b9d92441929ae9d78efc19fec290295a09d6d447f35dffa2fee8bee8,   158643
work/amr_wave.py, 7458a38087b55b1a73e00035ea8f2d81cd25b1feb7ed9b94ae95414089657f9c,    23416
work/llm_judge.py, 191103651c54528c594a9e91fd98e78afc0290c3ccececfee6f47b38b1ae7f35,     7016
report/evidence/amr_wave_results.json, 2b4c21cf48ce546c820140cfcbee59e2859b6350abc06db1f0aed0d0e9442795,     2576
report/evidence/llm_judge_verdict.json, e67586e7fdb2529d144c21929c9497ad231c2c226529fc6a344967cd53f51919,     3352
```
