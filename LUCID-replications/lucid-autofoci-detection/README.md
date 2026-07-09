# AutoFoci replication (LUCID)

**Paper:** Lengert et al., *Scientific Reports* 8:17282 (2018). DOI 10.1038/s41598-018-35660-5.

**Status:** REPLICATED. Coverage 8/10, agreement 9/10. See `REPORT.md`.

## TL;DR

The AutoFoci paper claims that a hand-crafted "Object Evaluation
Parameter" (OEP), built from top-hat-filtered intensity × LoG-filtered
intensity × object compactness, divided by nucleus mean intensity, and
combined across two DNA-damage marker channels (53BP1 + γH2AX) by a
weighted geometric mean, achieves **Spearman ρ ≈ 0.90** against
manually-rated foci on 473 ground-truth objects.

We reimplemented equations 1–4 from the paper in ~350 lines of Python
(no use of the authors' Java binary) and ran them against the same
public ground-truth dataset.

**Result:** Spearman ρ = **0.890** vs. averaged manual rating
(paper: 0.90), AUC = **0.980** when using OEP to classify "foci"
(rating ≥ 5) vs. "background" (rating < 5). Bimodal histogram of
log(OEP) clearly separates the two populations, matching paper Fig. 3.

## Quickstart

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install tifffile numpy scipy scikit-image scikit-learn matplotlib pandas openpyxl

git clone https://github.com/nleng/AutoFoci.git repo
7z x repo/AutoFoci/manual_object_rating.7z -o./repo/manual_data/
7z x repo/AutoFoci/Test_Images_AutoFoci.7z -o./repo/test_images/

python code/autofoci_reimpl.py \
    --ratings repo/manual_data/manual_object_rating/Manual_object_rating_results.xlsx \
    --images  repo/test_images/Test_images_AutoFoci \
    --out     results/features.csv

python code/evaluate.py results/features.csv results
```

## What's in here

- `code/autofoci_reimpl.py` — Python reimplementation of equations 1–4.
- `code/evaluate.py` — correlations vs. paper, ROC, histograms, figures.
- `results/features.csv` — per-object features (53BP1 + γH2AX OEP, etc.).
- `figures/` — replicated versions of paper Fig. 2d/3, plus ROC.
- `REPORT.md` — full write-up with paper-vs-ours comparison table and
  honest accounting of what was and was not replicated.
- `PROGRESS.md` — chronology.

## Honest caveats

- Equation 3 (weighting factor `w`) is under-specified in the paper.
  The per-cell pixel-SD ratio we compute is far from the paper's
  reported range of 0.9–1.2, suggesting their ISTD is computed on a
  per-experiment scale not made explicit. Using `w=1` (the geometric
  mean limit, which is what eq. 4 reduces to when w≈1) reproduces the
  headline ρ; see REPORT.md.
- We did not replicate the wet-lab DSB-repair kinetics (Fig. 4) — those
  raw images are not in the public dataset, and that result is itself a
  re-replication of refs. 18, 20.

## License / provenance

- Original AutoFoci code (Java) by Nicor Lengert et al., GPL-licensed at
  https://github.com/nleng/AutoFoci.
- Manual rating data and test images by the same authors, distributed
  under the same repo.
- This replication is independent and unaffiliated with the authors;
  no contact was made.
