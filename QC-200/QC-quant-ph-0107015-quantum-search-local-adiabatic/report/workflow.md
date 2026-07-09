# Workflow — Roland & Cerf (2001) replication

Target dir: `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-0107015-quantum-search-local-adiabatic/`
Run date: 2026-07-05 (US/Central).
Agent: automated subagent, model `argo/argo:claude-opus-4.7` via Argo proxy (free endpoint), no LLM API calls issued during the run — the replication is pure numerical simulation.

## Step-by-step

1. **Read the wave brief.** `~/Dropbox/REPLICATE-PROJECT/scripts/QC_WAVE_BRIEF_2026-07-03.md` (Rick 2026-07-03) plus the newer 8-artifact `REPLICATION_DIR_STANDARD_2026-07-05.md`.
2. **Create the target dir.** `mkdir -p .../{code,extraction,report/evidence,logs}`.
3. **Fetch the paper.** `curl -sL -o paper.pdf https://arxiv.org/pdf/quant-ph/0107015` → 107 kB, 4-page PDF v1.4.
4. **Extract text.** `pdftotext paper.pdf paper.txt` → 573 lines. Skimmed the whole thing; verified authors from PDF (Roland + Cerf), abstract, and the two headline formulas Eq. 15 ($T \geq N/\varepsilon$) and Eq. 19 ($T = (\pi/2\varepsilon)\sqrt N$).
5. **Design the simulation.**
   - Recognized that H₀ and Hₘ both preserve the 2-D invariant subspace span(|m⟩, |m⊥⟩), where |m⊥⟩ is the normalized projection of |ψ₀⟩ onto |m⟩⊥. Reduced dynamics to a 2×2 real-symmetric H̃(s).
   - Implemented both schedules:
     - **Linear:** s(t) = t/T.
     - **Local-adiabatic:** invert Eq. (18) — given (N, T), solve for ε such that s(T)=1 exactly, then $s(t) = 1/2 + \tan[(2\varepsilon\sqrt{N{-}1}\,t/N) - \arctan(\sqrt{N{-}1})] / (2\sqrt{N{-}1})$.
6. **Sanity check.** For N ∈ {4, 8, 16} and both schedules, compared the 2-D reduced integration against a full N-dim dense statevector integration. All differences ≤ 2e-15 ⇒ the 2-D reduction is exact to machine precision.
7. **T\* bisection.** For each (N ∈ {8,16,32,64,128,256,512,1024,2048}, schedule ∈ {linear, local}), bisected T until the smallest T achieving p_succ ≥ 0.5 was found (tolerance 0.01 relative). Starting brackets anchored on the paper's own predictions (T~N linear, T~(π/2)√N local), with automatic expansion/contraction if the bracket didn't straddle the threshold.
8. **Log-log fit.** `np.polyfit(log N, log T*, 1)` gave slopes 0.9992 (linear) and 0.4756 (local), R² > 0.9995 in both cases.
9. **Plots.** `code/plots.py` produced `evidence/scaling.pdf` (log-log T* vs N with reference lines) and `evidence/p_vs_T_N64.png` (success curve at N=64).
10. **Written up in LaTeX.** `report/REPORT.tex` compiled with `pdflatex` (TeX Live 2026-03-01) → `report/REPORT.pdf` (6 pages, 322 kB).
11. **Extraction files.** Marker/Nougat weren't installed in the sandbox; produced `extraction/marker.md` and `extraction/nougat.mmd` from `pdftotext` output plus hand structuring, explicitly noting the fallback method in each file.
12. **Open questions.** 5 non-trivial follow-on questions written to `report/open_questions.json`, each with `basis` (what in this replication motivates it) and `next_steps` (a concrete experiment). Also embedded in REPORT.tex.
13. **Failure/friction notes** captured in `report/failure_analysis.md`.

## Tools & versions

| Tool | Version | Role |
|---|---|---|
| Python | 3.14.6 (/usr/local/bin/python3) | driver |
| NumPy | 2.4.3 | linear algebra |
| SciPy | 1.18.0 | `scipy.integrate.solve_ivp` (DOP853) |
| Matplotlib | 3.10.8 | plotting |
| Poppler `pdftotext` | (Homebrew) | paper extraction |
| TeX Live | 2026-03-01 (Homebrew) | `pdflatex` for REPORT.pdf |
| Marker | *not installed* | extraction fallback used |
| Nougat | *not installed* | extraction fallback used |

## Estimated work

- Paper fetch + skim: 3 min
- Simulation coding: ~15 min
- Sanity check + full sweep: ~90 s wall-clock across N ∈ {8..2048} × 2 schedules
- Plotting + LaTeX compile: 2 min
- Extraction files: 5 min
- Report + open questions + failure analysis: 20 min

Total elapsed: on the order of 30-40 minutes agent wall-clock.

## Reproduction command

```
cd ~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-0107015-quantum-search-local-adiabatic
python3 code/adiabatic_search.py report/evidence
python3 code/plots.py
cd report && pdflatex -interaction=nonstopmode REPORT.tex
```

Deterministic (no RNG); results.json will be bitwise reproducible up to `solve_ivp` step-adaptation minutiae, which are stable at the specified rtol/atol.
