# workflow.md — replication workflow

## 1. Extraction
```
pdftotext -layout paper.pdf paper.txt      # 1739 lines, full text read
```
Recorded central claims + method in `extraction/marker.md`.

## 2. Kernel triage
Read `~/Dropbox/XFER/TEXTURES-100/shared-kernels/loop_current_kagome_kernel.py`.
Confirmed the paper IS a spinless kagome loop-current paper — a direct match
for the kernel's flux-phase / Chern machinery. Decision: reuse geometry +
Peierls-flux + FHS Chern + bond-current + 3Q classification; add a folded 2×2
model for the paper-specific 1nn+2nn imaginary bond order.

## 3. Claim selection (5 machine-checkable)
- A: bare kagome spectrum (flat band, Dirac at K, p-type VHS at E=0).
- B: LCO imaginary bond order opens a full gap (Fig 3d).
- C: gapped LCO state is a Chern insulator, total C=1 (Fig 3d).
- D: Landau quartic Eq.(2), Z1−Z2>0, selects equal-weight 3Q.
- E: TRS broken only for imaginary bond order (LCO), not real (CBO); 3Q is FM.

## 4. Implementation
`code/replicate_zhan2025.py` imports the shared kernel by path (provenance
preserved) and adds `FoldedKagomeLCO`. Run:
```
cd work && python3 ../code/replicate_zhan2025.py   # writes work/results.json
```

## 5. Comparison
Each claim's numeric output compared against the paper's stated values/qualitative
statements. See `artifacts_summary.md` and REPORT for the table.

## 6. Artifacts
report/: REPORT.tex (+PDF), open_questions.json, workflow.md,
artifacts_summary.md, failure_analysis.md, PROVENANCE.md.
extraction/: marker.md. work/: results.json, run.log.

## Reproduce from scratch
```
cd ~/Dropbox/REPLICATE-PROJECT/TEXTURE-loop-current-zhan2025
pdftotext -layout paper.pdf paper.txt
cd work && python3 ../code/replicate_zhan2025.py
cd ../report && latexmk -pdf REPORT.tex   # optional
```
