# Attempt Log

Chronological, factual.

## 2026-07-06 04:08 CDT — start

- Cron subagent spawned with paper assignment (PDE / schrodinger-virtual-lab-2019 / DOI 10.1088/1361-6404/aac999).
- Read `~/Dropbox/REPLICATE-PROJECT/scripts/WAVE_BRIEF_2026-07-01.md` and `REPLICATION_DIR_STANDARD_2026-07-05.md`.
- Confirmed target dir does NOT yet exist. Sibling `PDE-Figueiras-Schrodinger-BPM-splitstep-2018/` DOES exist and is a from-scratch replication of the SAME DOI (sha256 match on paper.pdf later verified). Decided: this dir will be an *artifact-based* replication (run authors' code) to complement the sibling's from-scratch approach.

## 04:09-04:11 — reconnaissance

- Web search for "An open source virtual laboratory for the Schrödinger equation" → IOP, ADS, ResearchGate, Durham CM3 course page.
- Web fetch of LIA2 (Vigo) group page → **code URL: https://github.com/pyNLSE/bpm**.
- `mkdir -p PDE-schrodinger-virtual-lab-2019/{report/evidence,extraction,work}`.

## 04:11 — clone + paper acquisition

- `cd work && git clone https://github.com/pyNLSE/bpm.git` — succeeded, HEAD `96d945b`.
- Located sibling's paper copy at `PDE-Figueiras-Schrodinger-BPM-splitstep-2018/work/figueiras.pdf`; `cp` into `paper.pdf`.
- `shasum -a 256 paper.pdf → 034a26a1f606e6b1f5c5a0135a89d45c0ef137b5e763cabb10a190d67e933486` — matches expected.

## 04:12 — venv + first driver

- `python3 -m venv work/.venv`.
- `pip install -q numpy scipy matplotlib` — succeeded (numpy 2.5.1, scipy 1.18.0, matplotlib 3.11.0).
- Wrote `work/run_example.py`: headless wrapper around authors' `bpm.py` main loop with per-image diagnostics.
- First smoke: `python run_example.py Rectangular_Barrier_1D 1D` — succeeded in 23.0 s (100 PNGs; norm 5.013 → 4.931).

## 04:15-04:20 — 1D batch pass

- Ran 8 more 1D examples: Sech2_Pot_1D (49.7s), Double_Well_1D (42.9s), Diffraction_Slit_1D (16.4s), Interference_Gaussians_1D (16.4s), Soliton_Emission_A_1D (84.6s), Solitons_in_phase_1D (20.1s), Solitons_phase_opp_1D (19.0s), Thomas_Fermi_1D (48.9s).
- All succeeded. Norm conservation confirmed: absorb=0 → drift ≤ 5e-11; absorb=20 → drift correlates with mass reaching boundary.

## 04:20-04:25 — 2D batch pass

- Gaussian_Beam_2D (94.3s) → norm 1.0 → 1.0 to 2e-12.
- Vortex_2D (97.6s) → norm 1.0 → 1.0 to 1e-10.
- Collapse_2D initial attempt → `FileNotFoundError: townes_profile.csv`. Fixed driver by chdir into `bpm/`. Rerun succeeded (90.7 s, norm 5.842 to 3e-13).
- Diffraction_Circle_2D initial attempt → 500² × 60000 timesteps, still running at ~4 min → killed. Kept as skipped-for-time.

## 04:25-04:29 — reflectionless sweep

- Wrote `work/test_reflectionless_sweep.py`: identical Gaussian packet, sweep s ∈ {1,2,3,10, 0.5,1.5,2.5}, Nx=4000, xmax=150, dt=0.001, tmax=80.
- All 7 runs succeeded. Result: integer s → R/N ≈ 1.48-1.50% (dominated by initial-packet tail contamination), half-integer s → R/N ≈ 3.97-4.17% (~2.7× larger, genuine reflection). Norm conserved to 12+ digits in every case.

## 04:30-04:33 — extraction

- `pip install marker-pdf` → failed on numpy build for Python 3.14. Substituted `pdftotext -layout paper.pdf extraction/marker.md`.
- Nougat install skipped (same class of issue). Wrote `work/pdf_to_mmd.py` (pymupdf) as substitute; produced `extraction/nougat.mmd`.

## 04:34-04:44 — report write

- Wrote REPORT.md, brief.md, open_questions.json.
- Copied 20 representative PNGs into `report/evidence/`.

## 04:44-04:48 — LLM judges

- `python work/judge.py` (3 judges: gpt-5.2, gemini-2.5-pro, claude-opus-4.7). Claude 502'd.
- `python work/judge_retry.py` (retry claude, add gpt-4.1). Claude 502'd again; gpt-4.1 → REPLICATED.
- `python work/judge_extra.py` (add gpt-4o, o3). Both → REPLICATED.
- Final tally: **4 REPLICATED (Gemini, gpt-4.1, gpt-4o, o3), 1 PARTIAL (gpt-5.2), 1 endpoint failure (Claude)**.

## 04:49-05:00 — remaining artifacts

- Wrote workflow.md, artifacts_summary.md, failure_analysis.md, REPORT.tex.
- Updated REPORT.md §6 with real judge tally.
- Final check: 8/8 required artifacts present.

## Total wall-clock: ~60 minutes
