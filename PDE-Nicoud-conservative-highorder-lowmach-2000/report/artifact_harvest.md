# Artifact harvest

## External artifacts touched (no downloads used in analysis)

| Source | URL | What we got |
|---|---|---|
| Semantic Scholar | https://www.semanticscholar.org/paper/…/202e3dae9098e2fef51bf3a2df1e6c5b3bd66633 | Bibliographic + abstract confirmation (DOI 10.1006/jcph.1999.6408, vol 158 pp 71-97, three FD algorithms, 4th-order spatial, 2nd-order temporal). |
| HAL | https://dumas.ccsd.cnrs.fr/I3M_UMR5149/hal-00910303 | Metadata only; body blocked by Anubis anti-bot challenge. |
| ScienceDirect | https://www.sciencedirect.com/science/article/pii/S0021999199964082 | Blocked (403, publisher paywall). |
| arXiv 2405.11063 | https://arxiv.org/html/2405.11063 | Independent citation confirming the scheme family. |
| AIAA J. 2020 (10.2514/1.J058222) | https://arc.aiaa.org/doi/abs/10.2514/1.J058222 | Reference confirmation. |

Nicoud (2000) is not open access. The replication does not require the paper's source code (there is none public). We use published-abstract-level knowledge of the scheme plus the (well-documented, textbook) Morinishi/Nicoud family of staggered 4th-order operators, and re-derive the (27/24, −1/24) telescoping conservative divergence + (9/16, −1/16) staggered interpolation from first principles.

## Local artifacts produced (this replication)

| Path (rel to replication root) | Size | SHA-256 (short) | Purpose |
|---|---|---|---|
| `work/nicoud_scheme.py` | ~18 KB | — | Solver + T1/T2/T3 test battery |
| `work/llm_judge.py` | ~4 KB | — | Argo REST LLM-judge caller with model-fallback |
| `work/run.log` | ~2 KB | — | Solver stdout |
| `report/evidence/results.json` | ~7 KB | — | Structured numerical results consumed by judge |
| `report/evidence/judge_verdict.json` | ~2 KB | — | LLM judge raw + parsed verdict |

All local artifacts are the product of this replication, run on `cherryrd`, Python 3.14.6 + numpy + scipy, wall time ~2.5 s for the solver and ~9 s for the judge.

## No paid endpoint usage

* All LLM calls: Argo proxy `http://127.0.0.1:44497` (key `stevens`, free per standing rule).
* No calls to Anthropic-direct, OpenAI-direct, OpenRouter, Ollama-pro, or any billed provider.
* All compute local; uicgpu not needed (numpy problem, 2.5 s on CPU).
