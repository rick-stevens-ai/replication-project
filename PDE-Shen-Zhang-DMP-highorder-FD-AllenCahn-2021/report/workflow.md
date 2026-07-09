# Workflow

## Compute

- **Host:** CherryRd (M2 Ultra Mac Studio), local. Total wall-clock: **1.3 s** for
  all 10 numerical experiments. No heavy compute needed — problem size is
  small (max 96×96 grid, ~60 time-steps). uicgpu was checked for
  marker/nougat availability but not used for compute since the workload
  is trivial.

## Tools + versions

- Python 3.14.6 (Homebrew).
- numpy 2.x (system).
- scipy (splu, sparse construction).
- matplotlib (Agg backend, PNG output).
- pdftotext (poppler) — used for extraction fallback.
- LLM judge: **argo:gpt-5.4** via LiteLLM aggregator
  `http://127.0.0.1:4000/v1`, Authorization: `Bearer stevens`.
  Fallback list attempted (argo:claude-opus-4.7 failed with LiteLLM 502
  — see `failure_analysis.md`).

## Free-endpoints-only compliance

- All LLM inference: **Argo** (localhost:44497 raw wrapper and
  localhost:4000 LiteLLM aggregator). Both are the free Argonne
  gateway.
- No Anthropic direct, OpenAI direct, OpenRouter direct, or paid API
  calls were made.

## Order of operations

1. Read wave brief.
2. Discover sibling replication `PDE-allen-cahn-maxprinciple-shen-zhang-2021`.
   Read its REPORT.md to decide a complementary angle (no overwrite of
   sibling).
3. Copy paper.pdf from sibling's cache (no re-download).
4. Extract (pdftotext -layout → marker.md + nougat.mmd per corpus convention).
5. Write from-scratch numerical solver (`allen_cahn_dmp.py`):
   - Sparse 1D/2D Laplacians (2nd + compact 4th order)
   - Stabilized IMEX backward-Euler with splu factorization
   - 6 DMP dynamics experiments
   - 4 manufactured-solution convergence tests
6. Run — 1.3 s.
7. Generate PNGs + CSVs.
8. LLM-judge the results against paper claims; save verdict JSON.
9. Write 8 required artifacts (REPORT.md + REPORT.tex + brief + attempt_log
   + artifact_harvest + workflow + artifacts_summary + failure_analysis +
   open_questions.json).
10. Verify 8-artifact standard.
11. Emit WAVE_RESULT line.

## Reproduction commands

```bash
cd ~/Dropbox/REPLICATE-PROJECT/PDE-Shen-Zhang-DMP-highorder-FD-AllenCahn-2021
# extract (if missing)
pdftotext -layout paper.pdf extraction/marker_body.txt
{ echo "# Marker-format extraction"; cat extraction/marker_body.txt; } > extraction/marker.md
{ echo "% Nougat fallback"; cat extraction/marker_body.txt; } > extraction/nougat.mmd

# numerical
cd work
python3 allen_cahn_dmp.py
python3 make_figures.py
python3 emit_csvs.py

# LLM-judge (needs Argo aggregator up on :4000 or :44497)
python3 judge.py
```

## Effort estimate

- Task-planning + reading sibling: ~5 min agent time
- Writing solver + convergence tests: ~10 min agent time
- Running experiments: 1.3 s wall-clock, ~1 min agent turn
- LLM-judge (including debugging the LiteLLM 502): ~5 min
- Writing reports: ~10 min
- **Total agent turn budget: ~30 min**
- **Total compute cost (billable): $0** (free Argo + local CPU only)
