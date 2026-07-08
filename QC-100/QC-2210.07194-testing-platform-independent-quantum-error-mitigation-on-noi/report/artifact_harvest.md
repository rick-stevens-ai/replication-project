# Artifact Harvest — QC-2210.07194

Every public artifact pulled during this replication.

## Primary sources

| Artifact | URL | Size | Notes |
|---|---|---|---|
| arXiv abstract page | https://arxiv.org/abs/2210.07194 | 42,399 B | Metadata (title, authors, abstract, date) |
| arXiv PDF (v2, Dec 2022) | https://arxiv.org/pdf/2210.07194 | 1,057,810 B | Full paper, 38 pages |
| Extracted plaintext | (local) `work/paper.txt` | 96 KB | Extracted with `pdftotext -layout` |

## Referenced code (paper repo)

| Artifact | URL | Used? | Notes |
|---|---|---|---|
| Mitiq (paper cites v0.18.0) | https://github.com/unitaryfund/mitiq | YES — we installed current v1.0.0 | Actual mitigation library |
| Paper repo (data + notebooks per §II.B.4 / Listing 1) | https://github.com/unitaryfund/mitiq (as software), plus referenced supplementary at Unitary Fund | Not directly cloned | We built ZNE + PEC calls from scratch using the same mitiq API |

## Python packages installed in `work/venv/`

- mitiq 1.0.0
- qiskit 2.5.0
- qiskit-aer 0.17.2
- cirq (transitively; used by mitiq for interop)
- numpy, matplotlib
- ply (transitive dep of cirq contrib qasm parser)

## Our own artifacts (this replication)

Under `work/`:
- `paper.pdf` — original arXiv PDF (copy for local reference)
- `paper.txt` — pdftotext extraction of the paper
- `arxiv_abs.html` — arXiv abstract page HTML
- `replicate_zne.py` — v1 ZNE replication (Richardson + Linear, 5 depths, |C|=4, single-trial)
- `replicate_zne_v2.py` — v2 with N_TRIALS=4 and both 0.5% and 1.0% depol noise levels
- `replicate_pec.py` — PEC replication (kPEC=100, 1% depol)
- `plot_results.py` — matplotlib plots

Under `report/evidence/`:
- `zne_results.json` — v1 raw numbers
- `zne_results_v2.json` — v2 raw numbers with both noise levels and per-depth summaries
- `pec_results.json` — PEC raw numbers
- `zne_run.log`, `zne_v2_run.log`, `pec_run.log` — stdout of each run
- `improvement_factor_vs_depth.png` — Fig. 2-style plot of μ vs d
- `expectation_vs_depth.png` — Fig. 2 (bottom) style plot of ⟨A⟩ vs d
- `llm_judge_verdict.md` — LLM-judge verdict (see below)

## Compute

- All experiments ran locally on CherryRd (host: Mac, macOS Darwin 25.3.0). No GPU/HPC needed for n=3 qubit simulator work.
- ZNE v1: 32.6 s wall.
- ZNE v2: 251.2 s wall.
- PEC: 188.0 s wall.
- Total compute budget consumed: < 8 min wall on a single laptop core.

## LLM usage

- Paper text extraction: `pdftotext` (poppler), zero LLM.
- Analysis + verdict framing: local reasoning only; final verdict is authored here.
- No paid LLM endpoints hit for this replication. (The Argo/Sophia/CELS free routes remained available but were not needed — the paper's core claim is a numerical experiment we could run directly.)
