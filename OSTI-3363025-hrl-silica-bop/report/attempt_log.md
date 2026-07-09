# Attempt log — OSTI 3363025 replication

All times CDT 2026-07-05.

- **18:07** — Task received. Read `WAVE_BRIEF_2026-07-01.md` (free-endpoints-only rule, real-data rule, LLM-judge rule, 8-artifact bar).
- **18:10** — Fetched paper PDF via `ssh uicgpu` (proxy required — direct osti.gov unreachable from uicgpu without `source ~/env.sh`). 771 KB.
- **18:11** — Cloned `https://github.com/miscquanta/HMRRL-tersoff-silica.git` on uicgpu. Four files: `ML-Tersoff.tersoff`, `Q-Tersoff.tersoff`, `in.relax`, `quartz.data`. Verified initial density from quartz.data = 2.648 g/cm³ (matches experimental α-quartz).
- **18:13** — Extracted paper text with `pdftotext -layout`. Attempted `pdf` tool but Anthropic PDF endpoint out-of-credits; fallback to text extraction was fine.
- **18:13-14** — Read paper end-to-end. Identified reproducible core = α-quartz block (only structure shipped), Fig 4 heatmap α-quartz row = the direct target metric.
- **18:14** — Found LAMMPS on uicgpu at `/data/stevens/envs/lammps-cuda/bin/lmp` (29 Aug 2024 release).
- **18:15** — Ran ML-Tersoff verbatim `in.relax` (5×5×5, iso box/relax → NVE 10 ps). Density stuck at **1.591 g/cm³** (39.9% below exp). Temperature drifted from 298→1083 K under NVE.
- **18:17** — Ran Q-Tersoff verbatim `in.relax`. Density = **1.735 g/cm³** (34.5% below exp). Big red flag: paper claims Q-Tersoff density error is ~0%.
- **18:20** — Hypothesis: `iso` box/relax is inappropriate for hexagonal α-quartz. Tried `tri` (full triclinic freedom) at 0 K. ML-Tersoff → 1.949 g/cm³, Q-Tersoff → 2.100 g/cm³. Improved but still 20-27% below exp.
- **18:22** — Tried `aniso` (each axis independent, no shear). Same results to 4 decimals as `tri` — the potential's true minimum is definitely NOT α-quartz for either model.
- **18:23** — Wrote angle-analysis Python (`evidence/angles.py`). Applies triclinic min-image, uses Si–O cutoff 2.2 Å, computes O–Si–O over Si with ≥2 O and Si–O–Si over O with 2 Si. Also coordination-number histograms.
- **18:24** — Angle analysis on relaxed structures:
  - ML-Tersoff (0 K aniso min): Si-O-Si = **174.99° ± 0.00°** — essentially linear! Cell is not quartz anymore.
  - Q-Tersoff (0 K aniso min): Si-O-Si = **168.78° ± 2.71°** — 25° above exp.
  - Both potentials preserve SiO4 tetrahedra at 0 K min (100% 4-fold Si, 100% 2-fold O).
- **18:27** — Ran NPT 298 K for 20 ps as the closest match to the paper's "properties at 300 K" phrasing. Results:
  - Q-Tersoff: ρ = 2.029 g/cm³ (23.4% err), Si-O-Si = 147.55° (+3.85° err — order of magnitude consistent with paper's 1.7° claim), O-Si-O = 108.22° (−1.25° err), coord: 97.6% 4-fold Si.
  - ML-Tersoff: ρ = 1.856 g/cm³ (29.9% err), Si-O-Si = 128.68° (**−15° err, wrong sign** vs paper's +7°), O-Si-O = 105.95° (−3.5° err), coord: only **77% 4-fold Si**.
- **18:30** — First LLM judge: `argo:gpt-5.1` via CherryRd `:4000` aggregator → **CONTRADICTED** with 6 specific numerical citations.
- **18:31** — Second LLM judge: `argo:gemini-2.5-pro` (via same aggregator) → also **CONTRADICTED**, citing the same numerical mismatches. Two independent judges agree.
- **18:33** — Copied all 26 evidence files to `report/evidence/`. Wrote `brief.md`, `REPORT.md`, `open_questions.json`.
- **18:35** — Building remaining 8-artifact bar items (workflow.md, artifacts_summary.md, failure_analysis.md, REPORT.tex, extraction/marker.md, extraction/nougat.mmd).

## Key lessons

1. Free-endpoint LLM judge on Argo `:4000` aggregator works reliably; use `argo:gpt-5.1` not `argo:claude-opus-4.7` (the latter hit a `Failed to parse upstream response` error at the LiteLLM shim). Both `gpt-5.1` and `gemini-2.5-pro` responded cleanly with the same verdict.
2. `pdf` tool is down (Anthropic depleted); use `pdftotext -layout` fallback.
3. UICGPU always needs `source ~/env.sh` for outbound HTTPS (proxy) — direct curl to osti.gov fails.
4. For hexagonal crystals, `iso` box/relax is inappropriate — always use `tri` or `aniso`. This is a real UX issue with the paper's released `in.relax` script.
5. Even with correct box/relax mode, if the potential doesn't have your target crystal at its global minimum, no MD protocol will save you.
