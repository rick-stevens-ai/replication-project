# Artifacts summary — QC-200 / 1612.09512

Root: `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-1612.09512-efficient-lindblad-simulation-cleve-wang/`

## Required 8 artifacts (per QC_WAVE_BRIEF_2026-07-03.md)

| # | Path | Kind | Status | Notes |
|---|------|------|--------|-------|
| 1 | `paper.pdf` | source PDF | ✔ present (776,841 B) | Fetched from `https://arxiv.org/pdf/1612.09512`. |
| 2 | `extraction/marker.md` | Marker-slot | ✔ present (fallback) | Marker not installed on host; hand-authored structured Markdown mirroring `pdftotext -layout` + explicit fallback banner. |
| 3 | `extraction/nougat.mmd` | Nougat-slot | ✔ present (fallback) | Nougat not installed on host; hand-typed TeX-equation transcription of Theorem 1, Cor. 2, Cor. 3, master equation, LCU expansion + explicit fallback banner. |
| 4 | `report/REPORT.tex` | main report (LaTeX) | ✔ present, 6.8 kB, PDF compile optional | Section-by-section reproduction narrative, claims table (6 claims), method, results, verdict, open questions. |
| 5 | `report/open_questions.json` | 5 open Qs | ✔ present, 5 entries with `q` / `basis` / `next_steps` | Grounded in what the replication actually observed. |
| 6 | `report/workflow.md` | workflow + tools + effort | ✔ present | Full command list, versions, ~50 min wall-clock estimate. |
| 7 | `report/artifacts_summary.md` | this file | ✔ present | ← you are here. |
| 8 | `report/failure_analysis.md` | honest failure analysis | ✔ present | Missing parsers (impact: cosmetic), gate-count untested (structural), circuit-level LCU untested (scoped out). |

## Evidence + code

| Path | Bytes | Kind |
|------|-------|------|
| `report/evidence/lindblad_lcu.py` | ~10.5 kB | Self-contained reproduction script |
| `report/evidence/results.json` | ~7 kB | Full numeric results: per-(t,K) Frobenius errors, K-scaling sweep 1..30 for each t, trajectory-trace, summary + verdict |

## Working intermediates

| Path | Bytes | Kind |
|------|-------|------|
| `work/paper.txt` | ~120 kB | `pdftotext -layout` full-body extraction, used for skim/grep |

## Provenance

- Executed 2026-07-05 evening CDT on host `CherryRd` under subagent
  `agent:main:subagent:22f4b497-e98e-4b45-9f14-435b2644670a` (spawned by
  main gateway session `agent:main:telegram:direct:8542341053`).
- No external LLM calls (numerical replication only).
- No external data required beyond the arXiv PDF.
- Deterministic: no RNG in `lindblad_lcu.py`.

## How to verify

```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-200/QC-1612.09512-efficient-lindblad-simulation-cleve-wang
python3 report/evidence/lindblad_lcu.py            # rewrites results.json, prints summary
python3 -c "import json; d=json.load(open('report/evidence/results.json')); print(d['summary']['verdict'])"
# expected: REPLICATED
```

Verified summary at time of writing:
```
{
  "per_t_min_frobenius_error": {"0.5": 2.05e-16, "1.0": 1.02e-14, "2.0": 1.26e-09},
  "slopes_log10eps_per_K": [-1.124, -0.917, -0.709],
  "convergent_slopes_count_of_3": 3,
  "trajectory_trace_max_dev_from_1": 4.62e-16,
  "num_t_reaching_1e-6": 3,
  "verdict": "REPLICATED"
}
```
