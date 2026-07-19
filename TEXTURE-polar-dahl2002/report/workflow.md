# Workflow — TEXTURE-polar-dahl2002 replication

## 0. Provenance
- **Target:** I. Dahl, *"Ferroelectricity, SSFLC, bistability and all that"*, arXiv:cond-mat/0211693 (2002).
- **Texture class:** polar (SSFLC / chiral smectic-C* ferroelectric liquid crystals).
- **Scaffold state at start:** paper.pdf, extraction/marker.md (pdftotext, 1318 lines), report/method_extract.md. No code/work/report.

## 1. Read & classify (inputs)
- `extraction/marker.md` — full extracted text (read via `grep`/`sed`; PDF tool blocked by Dropbox path policy, so worked from the marker text).
- `report/method_extract.md` — prior extract flagged the paper **REVIEW/OPINION → non-replicable as posed**. Confirmed independently.
- Searched marker.md for equations, director-field, free-energy, switching, polarization, tilt, bistability, anchoring.

## 2. Decision
The paper presents **no solvable model / dataset / figure**. Instead of fabricating, reduced the *domain physics the paper argues about* (Clark–Lagerwall SSFLC picture + Dahl's "alternative view") to a minimal azimuthal (φ) smectic-cone model and extracted **5 machine-checkable claims** (C1–C5), including Dahl's two original proposals (helix-unwinding invariance C3, static-friction bistability C5).

## 3. Implement (`code/`)
- `code/ssflc_model.py` — minimal 1D SSFLC free-energy + overdamped dynamics; one `check_Cx()` per claim; `__main__` dumps JSON.
- `code/verify_C2_prefactor.py` — analytic vs numeric 10–90% switch time to explain the C2 prefactor.

## 4. Run (`work/`)
```
python3 code/ssflc_model.py > work/results.json 2> work/run.log
python3 code/verify_C2_prefactor.py | tee work/C2_prefactor.log
```
Environment: Python 3, numpy 2.4.3, scipy 1.18.0 (local, no network). No external/paid endpoints used.

## 5. Compare (quantitative)
- C1: measured 45.00° vs expected 2θ = 45.0° (err 7e-15°) — **exact**.
- C2: τ ∝ 1/E, R²=0.9999; slope 3.5× γ/Ps = definitional 10–90% integration constant (analytic ∫sec dφ), numeric↔analytic agree <3%.
- C3: unwound/wound criterion invariant under K-scaling (fixed W_s/(K q0)); reduced gap collapses to −11.16.
- C4: 2 degenerate minima at φ=±90°, barrier 2e-4 J/m²; 0 minima without anchoring.
- C5: memory at E=0, pinned below E_th=4 MV/m, switches above — static-friction bistability self-consistent.

## 6. Artifacts (`report/`)
REPORT.tex, open_questions.json (5 new), workflow.md, artifacts_summary.md, failure_analysis.md.

## 7. Reproduce from scratch
```
cd ~/Dropbox/REPLICATE-PROJECT/TEXTURE-polar-dahl2002
python3 code/ssflc_model.py
python3 code/verify_C2_prefactor.py
```
Deterministic (no RNG); results.json is byte-stable across runs.
