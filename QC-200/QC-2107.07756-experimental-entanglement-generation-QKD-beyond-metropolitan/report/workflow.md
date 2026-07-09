# Workflow — Independent replication of arXiv:2107.07756

## What this is
Independent, first-principles reproduction of the paper's own analytic
model of secure key rate (Eqs. 1–4 in Methods, Neumann et al.), driven
by the paper's own measured constants. No hardware, no proprietary
data, no paid APIs.

## Environment
- Host: CherryRd, macOS Darwin 25.3.0, Python 3.14.6
- Tools used (all preinstalled / free):
  - NumPy 2.4.3 (`np.trapezoid`, `np.linspace`, `np.exp`)
  - SciPy 1.18.0 (`scipy.special.erf` for Λ(λ) Gaussian fit)
  - Matplotlib 3.x (headless Agg backend for PNG output)
  - Poppler `pdftotext -layout` for PDF → text extraction
  - `curl` for arXiv PDF download
  - `pdflatex` (TeXLive) for compiling REPORT.tex → REPORT.pdf
- LLM tools used: **none required** — this replication is
  analytic/numeric and does not need model inference.
- Marker / Nougat: not installed centrally; `extraction/marker.md`
  and `extraction/nougat.mmd` fall back to pdftotext with a clearly
  labeled header stating why. Content is faithful to the source PDF.

## Steps executed
1. **Paper retrieval** (~2 s)
   - `curl -sL -o paper.pdf https://arxiv.org/pdf/2107.07756v4`
   - Verified 3 pp v4 (title + Quantum journal ref match arXiv abstract)
2. **PDF → text** (~1 s)
   - `pdftotext -layout paper.pdf work/paper.txt`
   - 794 lines including references
3. **Manual claims extraction** (~5 min)
   - Identified 8 testable claims (C1–C8; see REPORT.tex §2)
   - Extracted verbatim constants: B_ref = 4.10e6 cps/mW/nm,
     λ₀ = 1550.12 nm, t_Δ = 38 ps, η_det = 80%, ε_pol = 0.004,
     det_max = 200 MHz, deadtime_loss = 2%, spectral fill = 0.75,
     visibility = 99.4% (best) / 99.2% (min on 100 GHz)
   - Located Eqs. (1)–(4) and Eq. (3) integral for η
4. **Λ(λ) digitization** (~3 min)
   - Constrained a Gaussian to three paper-quoted averages
   - Bisection fit yields σ = 21.33 nm; all three constraints hit
     to <0.1% (see `outputs/summary.json` `Lambda_sanity` block)
5. **Model implementation** (~30 min)
   - `report/evidence/bbm92_key_rate.py`: 400 lines, self-contained.
   - Implements Eqs. (1), (2), (3), (4) verbatim.
   - Adds SNSPD nonparalyzable deadtime (τ = 100 ps from 2%/200 MHz).
   - Per-channel-pair coincidence-window optimization (grid + golden).
   - Sums over n symmetric WDM channel pairs about λ₀,
     truncated to |Δλ| ≤ 53 nm (paper's usable band).
6. **Sweep runs** (~1 min wall)
   - Pump power P ∈ {50, 100, 200, 400, 660, 800, 900, 1000} mW
   - WDM spacings: 200, 100, 50, 25, 12.5 GHz
   - Fiber distances: 0, 10, 20, 50, 100 km at α = 0.2 dB/km
7. **Plotting** (~5 s)
   - `report/evidence/plot_results.py` → two PNGs in outputs/
8. **Verdict scoring** (~5 min)
   - Cross-checked each of C1–C8 against the CSV; wrote REPORT.tex.
9. **PDF compile** (~5 s)
   - `pdflatex REPORT.tex` (2 passes for cross-refs)
10. **Open-questions** authored (~10 min)
    - Five specific, non-trivial questions grounded in observed gaps
      (not generic ones) — see `report/open_questions.json`.

## Debug log (chronological)
1. Initial numpy 2.4 `np.trapz` → `np.trapezoid` (fixed).
2. First run: used `sqrt(η_A η_B)` in Eq. (1) → 4.4× overshoot.
   Traced the sqrt to the Klyshko *measurement* identity
   (η = CC/√(S_A S_B)) which is the inverse relation used to
   *extract* B from data. Corrected to `η_A × η_B` per Eq. (1)
   as printed → factor of ~10 drop.
3. Second run: `η_A × η_B` gave 0.42× ratio — under-predicting.
   Reviewed: was using n=33 channel pairs but paper uses n=66 (100 GHz).
   Corrected pair counts per paper's own Fig. 6 legend.
4. Third run: 0.46–0.56× ratio, consistent across all scenarios ✓.
5. Distance rolloff computed at fixed 400 mW; paper's "63% at 10 km"
   uses a naive multiplication that ignores pump reoptimization —
   flagged as Q4 in open questions.

## Estimated work
- Total wall time: ~90 min end-to-end (interactive)
- Total CPU time: <2 min (all Python + LaTeX)
- Total lines of code written: ~450 (Python) + ~250 (LaTeX)
- Total lines of paper text read carefully: ~200 (Methods + Fig 6 caption)

## Reproducing
```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-200/QC-2107.07756-experimental-entanglement-generation-QKD-beyond-metropolitan
python3 report/evidence/bbm92_key_rate.py   # ~60 s
python3 report/evidence/plot_results.py     # ~5 s
cd report && pdflatex REPORT.tex && pdflatex REPORT.tex
```
