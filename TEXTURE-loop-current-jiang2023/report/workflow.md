# Workflow — arXiv:2311.09290 replication

## 1. Ingest
- `pdftotext -layout paper.pdf paper.txt` (poppler; 6483 lines). Text layer clean,
  no OCR / vision needed. PDF = 38 MB (figure-heavy DFT paper).
- Read main text §I–§VIII + Appendices II, D. Identified the paper as a
  **d-orbital TB + S-matrix flat-band** paper, NOT loop-current (scope note).

## 2. Kernel reuse (provenance)
- Read `~/Dropbox/XFER/TEXTURES-100/shared-kernels/loop_current_kagome_kernel.py`
  in full FIRST (per task rule).
- Determined the reusable overlap = the NN kagome TB substrate (flux=0 limit of
  `KagomeModel`) + its `dos()` + `bands()`. The kernel's flux/Chern/loop-current
  machinery is out of scope for this paper (no TRS-breaking currents here).
- `code/verify_jiang2023.py` imports the kernel directly (`sys.path.insert`) so
  every spectral number is provably produced by the shared kernel.

## 3. Claim selection (5 machine-checkable)
- C1 NN kagome spectrum (flat @ +2t, Dirac @ K, vHS @ M) — Eq. S2.25 / Fig. 4.
- C2 BCL case-counting (Case#1 → 4 flat, Case#4 → 1 flat) — §II A.
- C3 general chiral BCL theorem N_L+N_L̃−2·rank(S) — App. D, Eq. D2.
- C4 quasi-flat mechanism (small hoppings → narrow bandwidth) — §II A + Fig. S2.4.
- C5 DOS structure (flat-band peak + log vHS at M) — Figs. 2/4.

## 4. Implementation
- Reused kernel for C1, C5 (band structure + DOS on 240–400² BZ meshes).
- Added BCL machinery `bcl_flat_count(NL, NLt, S)`:
  builds H = [[0,S],[S†,0]], counts numerical zero eigenvalues over BZ, compares
  to N_L+N_L̃−2·rank(S).
- Reconstructed the paper's own `S_{ptxy,d1}(k)` (Eq. S2.18) for C2/C3.
- C4: single kagome d-band model H_d = μ + 2t·H_K^NN + 2t'·H_K^NNN; selected the
  flat band as the minimum-bandwidth band; swept t' from 0 → 0.03 → 0.30 eV.

## 5. Debug log
- First run: `bcl_flat_count` shape mismatch (NL/NLt swapped vs S orientation).
  Fixed by putting the LARGER sublattice as NL (rows) matching S = block.T.
- First C4 run: picked the top band, which is dispersive in the +2t convention;
  the flat band is the LOWEST band. Fixed by selecting min-bandwidth band.

## 6. Outputs (work/)
- `results.json` — all numeric checks.
- `dos_kagome.{npz,png}`, `bands_kagome.png` — figures.

## 7. Report (report/)
- REPORT.tex (+ compiled PDF), open_questions.json (5), workflow.md,
  artifacts_summary.md, failure_analysis.md. extraction/marker.md.

## Reproduce
```
cd work && python3 ../code/verify_jiang2023.py
cd ../report && pdflatex -interaction=nonstopmode REPORT.tex
```
Runtime < 30 s, CPU only, no network.
