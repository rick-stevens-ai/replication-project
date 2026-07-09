# Workflow — AutoFoci Replication

**Paper:** Lengert et al., *Sci. Rep.* **8**:17282 (2018). DOI 10.1038/s41598-018-35660-5.
**Original run:** 2026-05-30 17:21–17:34 CDT (~13 min wall).
**Backfill (items 4–8):** 2026-07-06.
**Host:** subagent workspace, macOS (CherryRd), CPU-only (no GPU).

## Narrative

1. **PDF acquisition & extraction (17:21–17:22, ~1 min).**
   Vision/Anthropic PDF backends were unavailable at replication time; fell back to `pdftotext`. Cleanly extracted section headings, equations 1–4, LoG 5×5 kernel, and all user-defined parameters. Did not audit supplementary methods.
   *Risk noted at backfill:* no canonical `paper.pdf` was archived at replication time. See `paper.pdf.MISSING.md` and the nougat stub for the future central-corpus sweep hook.

2. **Repo + data acquisition (17:23).**
   `git clone https://github.com/nleng/AutoFoci` into `repo/`. Decompressed `manual_object_rating.7z` (473 objects, three raters, XLSX) and `Test_Images_AutoFoci.7z` (804 single-cell TIFFs) with `7z x`.

3. **Go/no-go check (17:25).**
   Verified 344/344 rated images present in the test image set. Ground-truth is complete → GO.

4. **Channel convention check (17:26).**
   Plotted a random test image's three channels + DAPI mask (`figures/channel_check.png`). Confirmed R=53BP1, G=γH2AX, B=DAPI as assumed by the Java source. This detail is not stated explicitly in the paper — inferred from the Java code.

5. **Environment (17:28).**
   `python3 -m venv .venv` + `pip install tifffile numpy scipy scikit-image scikit-learn matplotlib pandas openpyxl`. Python 3.13. No CUDA, no jar dependency.

6. **Reimplementation (17:30).**
   `code/autofoci_reimpl.py` (~350 LOC, 15 677 bytes): implements eqs. 1–4 + all intermediate features (mean intensity, top-hat, LoG, compactness) per channel per object, plus nuclear DAPI mask, plus 3-brightest-pixel aggregation. Cross-checked LoG kernel byte-for-byte against `repo/AutoFoci/src/.../ObjectFinder.java` line 91.

7. **First feature run (17:30).**
   Feature extraction on 473 rated objects: ~75 s. Output `results/features.csv` (473 × 22).

8. **First evaluation (17:31).**
   `code/evaluate.py` (~190 LOC, 7 966 bytes). Panel-by-panel Spearman ρ, inter-experimenter agreement, ROC, bimodality analysis, figures.
   *Result:* 4 of 9 panels within 0.05 of paper, but combined OEP (panel ix) with per-cell w = 0.555 vs. paper 0.90. Delta −0.35, replication apparently failing.

9. **Diagnosis of eq. 3 discrepancy (17:32).**
   Inspected per-cell `w = I_STD,red / I_STD,green` distribution. Median 0.52, range 0.30–1.05. Paper says typical range 0.9–1.2. The per-cell pixel-SD interpretation of `I_STD` does not match paper. Substituted `w = 1` (plain geometric mean, which eq. 4 reduces to when w ≈ 1) → panel ix ρ = 0.890, matching paper to −0.01.
   *This is a partial replication of C3* (see `report/failure_analysis.md` and `report/REPORT.tex` §Critique).

10. **Bimodality + threshold (17:33).**
    Smoothed KDE on log10(OEP) histogram; two peaks at 2.925 and 4.093 with a valley at 3.738. Valley threshold: TP=113, FP=0, FN=88, TN=272, F1=0.720. F1-optimal threshold (3.181): F1=0.927. ROC AUC=0.980, AP=0.978.

11. **Write-up (17:34).**
    `REPORT.md`, `README.md`, `PROGRESS.md`, all figures.

12. **Backfill (2026-07-06).**
    Added `report/REPORT.tex` (detailed LaTeX report + critique + Open Questions Q1–Q5), `report/open_questions.json` (5 questions, each with basis + concrete next steps), `report/workflow.md` (this file), `report/artifacts_summary.md`, `report/failure_analysis.md`. Created `extraction/` with nougat stub + marker.md derived from existing REPORT.md content. Recorded `paper.pdf.MISSING.md` marker for the future central corpus sweep.

## Tools & versions

| Tool | Version | Role |
|---|---|---|
| Python | 3.13 | Reimplementation host |
| numpy | (venv-pinned) | Array math |
| scipy | (venv-pinned) | ndimage, stats |
| scikit-image | (venv-pinned) | morphology, filters |
| scikit-learn | (venv-pinned) | ROC / AUC |
| matplotlib | (venv-pinned) | Figures |
| pandas | (venv-pinned) | features.csv I/O |
| openpyxl | (venv-pinned) | XLSX reader for rating spreadsheet |
| tifffile | (venv-pinned) | TIFF reader for single-cell images |
| p7zip / `7z` | system | Decompress `.7z` archives from author repo |
| git | system | Clone `nleng/AutoFoci` |
| pdftotext (Poppler) | system | PDF → text (vision backends unavailable) |

## Codes written (this replication)

| File | LOC | Bytes | Purpose |
|---|---:|---:|---|
| `code/autofoci_reimpl.py` | ~350 | 15 677 | Python reimpl. of eqs. 1–4 + all intermediate features per object per channel |
| `code/evaluate.py` | ~190 | 7 966 | Panel-by-panel Spearman ρ, inter-rater agreement, ROC/AUC, bimodality/threshold, all figures |

## Codes reused (upstream)

| File | Role |
|---|---|
| `repo/AutoFoci/src/.../ObjectFinder.java` | Source-of-truth check for LoG 5×5 kernel and inertia disk radius (both used in our Python impl.) |
| `repo/AutoFoci/AutoFoci.jar` | Present but NOT executed — the whole point was an independent reimplementation |
| `repo/AutoFoci/manual_object_rating/Manual_object_rating_results.xlsx` | Ground truth: 473 objects × 3 raters × 1–9 quality score |
| `repo/AutoFoci/Test_Images_AutoFoci/*.tif` | 804 single-cell TIFFs; we used the 344 that carry rated objects |

## Compute + wall-clock estimate

| Phase | Wall time |
|---|---|
| PDF extraction + reading | ~1 min |
| Repo clone + 7z decompress | ~1 min |
| Ground-truth verification + channel check | ~2 min |
| Python venv + package install | ~2 min |
| Reimpl. coding | ~4 min (agent-drafted, mostly first-try) |
| Feature extraction (473 objects) | 75 s |
| Evaluation + figures | ~2 s |
| Diagnosis of eq. 3 + refit with w=1 | ~1 min |
| Bimodality + threshold analysis | ~1 min |
| Report write-up | ~2 min |
| **Original total wall** | **~13 min** |
| Backfill (items 4–8) | ~5 min |

## Agent steps (approximate)

- Original run: ~40 tool calls (subagent), one contiguous session (2026-05-30).
- Backfill run: ~10 tool calls (this subagent, 2026-07-06).

## Estimate of LOC produced

- Novel code (Python): ~540 LOC across `autofoci_reimpl.py` + `evaluate.py`.
- Documentation: this workflow + REPORT.md + REPORT.tex + failure_analysis.md + open_questions.json + artifacts_summary.md ≈ 2 000 LOC of markdown/LaTeX/JSON.

## Reproducibility recipe

```bash
cd lucid-autofoci-detection/
python3 -m venv .venv && source .venv/bin/activate
pip install tifffile numpy scipy scikit-image scikit-learn matplotlib pandas openpyxl

# (already present in repo/ from original run, skip if re-using)
git clone https://github.com/nleng/AutoFoci.git repo
7z x repo/AutoFoci/manual_object_rating.7z -o./repo/manual_data/
7z x repo/AutoFoci/Test_Images_AutoFoci.7z   -o./repo/test_images/

python code/autofoci_reimpl.py \
  --ratings repo/manual_data/manual_object_rating/Manual_object_rating_results.xlsx \
  --images  repo/test_images/Test_images_AutoFoci \
  --out     results/features.csv

python code/evaluate.py results/features.csv results
```

Expected runtime: ~75 s (feature extraction) + ~2 s (evaluation).
