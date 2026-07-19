# Workflow — TEXTURE-orbital-gmitra2013

Replication of Gmitra, Matos-Abiague, Draxl & Fabian, PRL 111, 036603 (2013),
arXiv:1303.2510 — "Magnetic control of spin-orbit fields: a first-principles
study of Fe/GaAs junctions." Texture class: **orbital**.

## 1. Ingestion
- Read `paper.pdf` via `extraction/marker.md` (pdftotext dump; the `pdf` and
  `image` media tools are sandboxed away from Dropbox, so text extraction was
  used directly).
- Read `report/method_extract.md` and `META.json` for the pre-classified
  method/texture and the "DFT-heavy (needs cluster)" scope flag.

## 2. Physics identification
Extracted the paper's analytic backbone from the marker text:
- C2v symmetry-allowed SOC Hamiltonian (Eqs. 1-3).
- Bychkov-Rashba alpha_n / Dresselhaus beta_n decomposition.
- Symmetry extraction formulas Eqs. (4-9): w_x, w_y and alpha, beta from
  finite differences / velocities of the ab-initio bands.
- Table I: band-resolved cos(2 theta) expansion coefficients (Eqs. 10-11),
  the numerical ground truth used here.

## 3. Scope decision
Full relativistic FLAPW DFT (FLEUR) on Fe/GaAs slabs is **out of scope**
(in-process, no cluster dispatch). Replicated instead: the *symmetry model*
that is the paper's genuine methodological contribution, using the paper's own
extracted Table I as ab-initio ground truth. This is explicitly flagged in the
report and is not fabrication — no DFT numbers are invented.

## 4. Implementation (`code/`)
- `sof_model.py`: Hamiltonian, alpha_beta(theta), sof_linear, magnitude,
  toy band `model_energy`, and the extraction routines `extract_wxy` /
  `extract_alpha_beta` (direct transcriptions of Eqs. 4-9).
- `run_analysis.py`: six machine-checkable claims C1-C5, JSON metrics, and
  three figures (Fig.2 butterflies, Fig.2 polar |w|/k, Fig.3 alpha/beta vs theta).

## 5. Execution (`work/`)
Copied `code/*.py` into `work/`, ran `python3 run_analysis.py`.
Environment: numpy 2.4.3, matplotlib 3.10.8, Python 3 (CherryRd, macOS).
No network, no external endpoints. Deterministic (fixed seed).

## 6. Verification
`results/metrics.json` — 6/6 claims PASS. Cross-checked the key discriminators
(band-1 product flip vs band-2 non-flip; band-1 >> band-2 angular sensitivity)
directly against the paper's textual statements.

## 7. Reporting
Wrote the 8-artifact bar: REPORT.tex, open_questions.json (5 NEW questions),
workflow.md, artifacts_summary.md, failure_analysis.md, plus metrics + figures.

## Reproduce
```bash
cd work && cp ../code/*.py . && python3 run_analysis.py
cat ../results/metrics.json
```
