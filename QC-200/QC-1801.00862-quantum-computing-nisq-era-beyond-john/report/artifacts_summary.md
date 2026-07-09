# Artifacts inventory — QC-1801.00862 (Preskill NISQ)

Root: `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-1801.00862-quantum-computing-nisq-era-beyond-john/`

## Top-level files (required by 8-artifact bar)

| # | Path | Purpose |
|---|------|---------|
| 1 | `paper.pdf` | Original arXiv v3 PDF (SHA-256 `cf64a00c…`; see failure_analysis.md for hash-mismatch note) |
| 2 | `extraction/marker.md` | Marker-style markdown (pdftotext-flow fallback; headered) |
| 3 | `extraction/nougat.mmd` | Nougat-style .mmd (pdftotext-flow fallback; headered) |
| 4 | `report/REPORT.tex` | Full LaTeX report (companion to REPORT.md) |
|   | `report/REPORT.md` | Human-readable Markdown report (primary) |
| 5 | `report/open_questions.json` | 5 heavy-duty open questions, {q, basis, next_steps} |
| 6 | `report/workflow.md` | Chronology + tool inventory + reproduce recipe |
| 7 | `report/artifacts_summary.md` | This file |
| 8 | `report/failure_analysis.md` | Honest gaps and friction |

## Evidence directory (`report/evidence/`)

| File | Type | Description |
|------|------|-------------|
| `qaoa_nisq_demo.py` | Python 3.13 script | Main experiment: n=10, 3-regular, QAOA p=1,2, ideal + noisy |
| `qaoa_nisq_results.json` | JSON | Optimized params, ideal/noisy expectations, ratios, depth, CX counts |
| `qaoa_nisq_run.log` | Text log | stdout of the main run |
| `qaoa_noise_sweep.py` | Python 3.13 script | Sweep p2 ∈ [0, 1e-1], fixed optimum |
| `qaoa_noise_sweep.json` | JSON | Ratio vs p2 for p=1,2 |
| `qaoa_noise_sweep.log` | Text log | stdout of the sweep |
| `llm_judge.py` | Python 3.13 script | Argo GPT-5.2 verdict prompt |
| `llm_judge_verdict.json` | JSON | Final verdict + reasoning + confidence |
| `llm_judge.log` | Text log | stdout of the LLM-judge call |

## Work directory (`work/`)

| File | Description |
|------|-------------|
| `paper_v1.pdf`, `paper_v2.pdf`, `paper_v3.pdf` | Fetched arXiv PDFs (v3 promoted to `paper.pdf` at root) |
| `paper_v3.txt` | pdftotext -layout output |
| `paper_v3_flow.txt` | pdftotext (flow) output — used as marker/nougat fallback |

## Key numerical results (see report/REPORT.md §4 for full table)

- Classical MAX-CUT (n=10, 3-reg, seed=0): `C_max = 13`.
- QAOA p=1: ideal r=0.765, noisy r=0.761 at p2=1e-3.
- QAOA p=2: ideal r=0.836, noisy r=0.831 at p2=1e-3.
- Noise sweep shows p=2 → p=1 crossover at p2 ≈ 3e-2.
- LLM-judge (Argo gpt-5.2): **PARTIAL**, `supports_nisq_thesis=true`, confidence=medium.

## Traces / logs

- Argo call log: `report/evidence/llm_judge.log` (verdict JSON echoed to stdout)
- Sim wallclock: 27.0 s (main) + ~10 s (sweep). Machine: CherryRd.
