# Artifacts summary — arXiv:2311.09290

| Artifact | Path | Description |
|---|---|---|
| Paper (source) | `paper.pdf` | arXiv:2311.09290v2, 38 MB |
| Extracted text | `paper.txt` | `pdftotext -layout`, 6483 lines |
| Extraction marker | `extraction/marker.md` | method + central claims + scope classification |
| Verification code | `code/verify_jiang2023.py` | reuses shared kagome kernel; C1–C5 |
| Results | `work/results.json` | all numeric checks (machine-precision) |
| DOS data/plot | `work/dos_kagome.npz`, `work/dos_kagome.png` | flat-band peak + vHS at M |
| Band plot | `work/bands_kagome.png` | Γ-K-M-Γ, flat @ +2t, Dirac @ K |
| Report | `report/REPORT.tex` (+ `REPORT.pdf`) | full writeup |
| Open questions | `report/open_questions.json` | exactly 5 |
| Workflow | `report/workflow.md` | reproduction steps + debug log |
| Failure analysis | `report/failure_analysis.md` | scope + limitations |

## Result headline
All 9 numerical sub-checks (across 5 claims) reproduce.

| Claim | Result | Status |
|---|---|---|
| C1 flat band @ +2t | width 7e-15, E=2.000 | PASS |
| C1 Dirac @ K | gap 1e-15 | PASS |
| C2 Case#1 (Nd−Np=6−2) | 4 flat bands | PASS |
| C2 Case#4 (Nd2−Np=3−2) | 1 flat band | PASS |
| C3 BCL theorem | 4 zero-modes = N_L+N_L̃−2r | PASS |
| C4 NN-only flat | width 2.6e-15 eV | PASS |
| C4 quasi-flat (t'=0.03) | width 0.205 eV | PASS |
| C4 dispersive (t'=0.30) | width 1.95 eV | PASS |
| C5 vHS at M | −2.004 vs −2.000 | PASS |

## Kernel reuse / provenance
`code/verify_jiang2023.py` imports
`~/Dropbox/XFER/TEXTURES-100/shared-kernels/loop_current_kagome_kernel.py`
directly (`KagomeModel`, `.bands`, `.dos`, `.all_eigvals`). The kagome geometry,
conventions, and FHS machinery are unchanged; only the flux=0 substrate is
exercised (this paper has no loop-current content). BCL flat-band counting is
new paper-specific code added on top.

## Verdict
Reproduced (within scope). **Coverage 6/10** (DFT/cRPA half inherently
out-of-scope), **Agreement 10/10**.
