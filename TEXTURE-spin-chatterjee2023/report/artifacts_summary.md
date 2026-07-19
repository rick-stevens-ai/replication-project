# Artifacts Summary — chatterjee2023 (arXiv:2308.12703)

## Produced
| Artifact | Path | Notes |
|---|---|---|
| Original PDF | paper.pdf | sha256 `634c572037a635979c92bad5941e6eb3c06f65eda0b629cf6e59f0e49974ec5d` |
| Marker text | extraction/marker.md | pdftotext fallback (~1620 lines) |
| Nougat stub | extraction/nougat.mmd | GPU-only; sha256+DOI recorded for later corpus sweep |
| Replication code | code/chatterjee2023_replication.py | ~270 LOC, exact real-space BdG, CPU-only |
| Figure code | code/make_fig.py | ~60 LOC |
| Results JSON | work/results.json | per-claim match flags C1/C2/C3 (all True) |
| Figure 1 | figs/fig1_mcm_quadrupole.png | LDOS of 4 MCMs + |E| spectrum + g-transition |
| LaTeX report | report/REPORT.tex | section-by-section, claims table, critique |
| Open questions | report/open_questions.json | 5 heavy-duty, paper-grounded |
| Workflow | report/workflow.md | narrative + tools + effort |
| Failure analysis | report/failure_analysis.md | this set |
| LLM-judge verdict | report/evidence/llm_judge.json | REPLICATED, cov 7, agr 9 (sonnet-4.6, free) |
| Evidence: run log | report/evidence/run_log.txt | full stdout trace of the replication run |
| Evidence: results copy | report/evidence/results.json | mirror of work/results.json |

## Traces / key numbers
- C1: exactly **4** near-zero modes (|E|~1.3e-4), corner localization **92.5%** in corner boxes.
- C2: **Qxy = 0.5000** (topological, g=0.2) vs **0.0000** (trivial, g=1.4) — exact quantization.
- C3: g-sweep — 4 zero modes for g ∈ {0.0,0.1,0.2,0.4,0.7}; **0** zero modes by g=1.0, 1.4 ⇒ topological→trivial transition near g≈0.85.
- gap to 5th (bulk) mode at g=0.2: 0.176 (clean sub-gap isolation of the MCMs).

## Provenance
- arXiv: https://arxiv.org/abs/2308.12703 ; DOI 10.48550/arXiv.2308.12703
- Published in Phys. Rev. B (v2, 29 Jan 2024).
