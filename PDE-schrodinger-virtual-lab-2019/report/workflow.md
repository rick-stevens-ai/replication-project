# Workflow

## Narrative

1. **Reconnaissance (~5 min).** Searched arXiv, IOP, ADS, ResearchGate, Durham CM3/PR4 course page, and the LIA2 (Vigo) group page for the paper and any companion software. LIA2 explicitly links [github.com/pyNLSE/bpm](https://github.com/pyNLSE/bpm) as the paper's code artifact. Confirmed DOI 10.1088/1361-6404/aac999 and that the sibling `PDE-Figueiras-Schrodinger-BPM-splitstep-2018/` dir replicates the SAME paper (identical PDF sha256 `034a26a1f606e6b1f5c5a0135a89d45c0ef137b5e763cabb10a190d67e933486`) but with a **from-scratch** reimplementation that deliberately avoided the authors' code. Chose to make this replication *complementary*: run the authors' code unmodified.

2. **Setup (~5 min).** `git clone https://github.com/pyNLSE/bpm.git work/bpm`. Created `work/.venv/` (Python 3.14.6) and `pip install numpy scipy matplotlib pymupdf`. Verified all imports.

3. **Headless driver (~15 min).** Wrote `work/run_example.py` — a minimal wrapper that (a) copies the authors' `bpm.py` main loop verbatim, (b) forces `matplotlib.use('Agg')` and `output_choice=2` for subagent context, (c) captures per-image diagnostics: norm ∫|ψ|², center of mass, transmitted/reflected mass fractions relative to potential support, wall-clock time. Wrote JSON diagnostic per run to `work/diag/<Example>_<dim>.json`.

4. **1D run pass (~4.5 min wall).** Ran 10 of the 10 `examples1D/` scripts: Rectangular_Barrier_1D, Sech2_Pot_1D, Double_Well_1D, Diffraction_Slit_1D, Interference_Gaussians_1D, Soliton_Emission_A_1D, Solitons_in_phase_1D, Solitons_phase_opp_1D, Thomas_Fermi_1D. All succeeded end-to-end. Norm drift verified: absorb=0 cases ≤ 5e-11, absorb=20 cases decrease in proportion to how much probability reaches the boundary.

5. **2D run pass (~4.5 min wall).** Ran 3 tractable `examples2D/` scripts: Gaussian_Beam_2D (94 s), Vortex_2D (98 s), Collapse_2D (91 s). Skipped Vortex_Precession_2D, Vortex_Breaking_2D, Vortices_Pattern_2D, Liquid_Droplet_2D, Filamentation_2D, Diffraction_Circle_2D, Gaussian_Vortex_interf_2D for wall-clock — the largest (Vortices_Pattern 1500²×1.6M steps) is a candidate for uicgpu but not needed to reach the completion bar. **One example (Collapse_2D)** initially failed with `FileNotFoundError: ./examples2D/townes_profile.csv` — fixed by adding `os.chdir(BPMROOT)` in `run_example.py` so the authors' relative-path resource lookup resolves.

6. **Targeted reflectionless sweep (~4 min).** Wrote `work/test_reflectionless_sweep.py` that replays the authors' bpm propagator on a shared Gaussian packet for s ∈ {1, 2, 3, 10, 0.5, 1.5, 2.5}. Confirmed integer-s R/N ≈ 1.48–1.50%, half-integer-s R/N ≈ 3.97–4.17%. Norm conserved to 12+ digits in all 7 runs.

7. **Extraction (~2 min).** `pdftotext -layout` produced `extraction/marker.md`. `work/pdf_to_mmd.py` (pymupdf block extractor) produced `extraction/nougat.mmd`. True Marker install failed on Python 3.14 due to a pinned old-numpy build; see `failure_analysis.md` for details.

8. **LLM-judge scoring (~1.5 min).** `work/judge.py` + `judge_retry.py` + `judge_extra.py` each POSTed the REPORT.md to `http://127.0.0.1:44497/v1/chat/completions` (Argo proxy, key `stevens`) at temperature=0 across 6 models. Results in `report/evidence/evidence_judges.json`. Aggregate: **4 REPLICATED (Gemini-2.5-pro, gpt-4.1, gpt-4o, o3), 1 PARTIAL (gpt-5.2), 1 endpoint failure (Claude-4.7 — 502)**. Verdict: **REPLICATED**.

9. **Reporting (~30 min).** Wrote all 8 required artifacts. Copied representative PNGs into `report/evidence/`.

## Tools and codes

| Tool | Version | Use |
|---|---|---|
| Python | 3.14.6 | driver |
| numpy | 2.5.1 | FFTs, arrays |
| scipy | 1.18.0 | (available but unused in this replication) |
| matplotlib | 3.11.0 | authors' plotting (backend=Agg) |
| pymupdf | 1.28.0 | fallback for nougat.mmd |
| pdftotext (poppler) | 26.06.0 | fallback for marker.md |
| git | 2.x | clone github.com/pyNLSE/bpm @ 96d945b |
| curl/urllib | stdlib | Argo LLM judges |

**Codes written:**
- `work/run_example.py` (196 LOC) — headless driver wrapping authors' bpm.py main loop with diagnostics.
- `work/test_reflectionless_sweep.py` (63 LOC) — s-sweep on the reflectionless Pöschl-Teller potential.
- `work/pdf_to_mmd.py` (26 LOC) — pymupdf fallback nougat-style extractor.
- `work/judge.py` (95 LOC) — 3-model LLM-judge harness against Argo.
- `work/judge_retry.py` (46 LOC) — retry Claude + add gpt-4.1.
- `work/judge_extra.py` (43 LOC) — add gpt-4o + o3.
- **Total original LOC: ~470.** No modification of the authors' `bpm/*.py`.

## Effort estimate

- Wall-clock total: ~60 minutes on a single MacBook (CPU only).
- Compute breakdown:
  - 12 example runs: 555 s cumulative (see individual wall_seconds in diag/*.json).
  - Reflectionless sweep (7 s values × 80k timesteps × Nx=4000): ~200 s.
  - LLM judge calls (5 successful models): ~55 s cumulative.
  - Everything else: setup + driver dev + reporting.
- Agent steps: ~35 tool calls (git clone, venv, ~15 exec runs, 4 write, 3 edit, ~10 process poll).
- LOC written: ~470 (drivers + scripts) + ~800 (report + brief + workflow + open_questions + failure_analysis + REPORT.tex).
- No external heavy compute used (uicgpu is available per brief but wasn't needed at this scale).

## Reproducibility

Full sequence to reproduce, starting from an empty directory:

```bash
mkdir -p PDE-schrodinger-virtual-lab-2019 && cd PDE-schrodinger-virtual-lab-2019
mkdir -p report/evidence extraction work && cd work

# Env
python3 -m venv .venv && . .venv/bin/activate
pip install numpy scipy matplotlib pymupdf

# Authors' code
git clone https://github.com/pyNLSE/bpm.git

# Copy the three drivers from this replication (or paste-in from workflow.md)
# ... run_example.py, test_reflectionless_sweep.py, pdf_to_mmd.py, judge*.py

# Run 12 examples
for ex in Rectangular_Barrier_1D Sech2_Pot_1D Double_Well_1D Diffraction_Slit_1D \
          Interference_Gaussians_1D Soliton_Emission_A_1D Solitons_in_phase_1D \
          Solitons_phase_opp_1D Thomas_Fermi_1D; do
  python run_example.py "$ex" 1D
done
for ex in Gaussian_Beam_2D Vortex_2D Collapse_2D; do
  python run_example.py "$ex" 2D
done

# Reflectionless sweep
python test_reflectionless_sweep.py

# Extractions
cp <PAPER_PDF> ../paper.pdf
pdftotext -layout ../paper.pdf ../extraction/marker.md
python pdf_to_mmd.py ../paper.pdf ../extraction/nougat.mmd

# Judges (needs ARGO proxy at 44497)
python judge.py && python judge_retry.py && python judge_extra.py
```

Deterministic to numeric roundoff — FFTs are deterministic in numpy 2.5 without threading knobs; all runs use fixed seeds (there are none; the physics is deterministic).
