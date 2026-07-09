# Workflow — QC-200 replication of arXiv:0712.1008 (Somma, Boixo, Barnum, 2007)

## One-line
Numerical replication of the Szegedy-walk quadratic-speedup core of "Quantum
Simulated Annealing" on random ±J Ising Metropolis chains at n=4,5,6 spins,
β ∈ {0.5, 1.0, 2.0}. Real numpy linear algebra on a 2^{2n}-dim edge Hilbert
space. Verdict: REPLICATED.

## Timeline (approximate, wall-clock)
| Step | What | Wall-clock |
|------|------|-----------|
| 1 | Read wave brief + create target dir + fetch arXiv PDF (`curl`) | ~30 s |
| 2 | `pdftotext` + grep to locate Szegedy walk section, confirm Eqs. 5–14 | ~2 min |
| 3 | Verify author list vs task brief (found discrepancy; task said Knill/Ortiz, PDF says Barnum) | ~1 min |
| 4 | Design + implement `qsa_szegedy.py` (Ising energy, Metropolis, Szegedy W, checks) | ~15 min |
| 5 | Run `python3 qsa_szegedy.py` — 5 instances × 3 β × (build M, diag M, build W ∈ C^{4096×4096}, diag W) | 4 s (real) |
| 6 | Produce `extraction/marker.md` + `extraction/nougat.mmd` fallbacks (marker/nougat not installed; noted in header) | ~1 min |
| 7 | Write `open_questions.json`, LaTeX `REPORT.tex`, `pdflatex REPORT.tex` | ~15 min |
| 8 | Write `workflow.md`, `artifacts_summary.md`, `failure_analysis.md` | ~10 min |
| **Total human/agent time** | | **~45 min** |
| **Total compute time** | (single-threaded numpy on Apple Silicon Rosetta / macOS 25.3) | **~4 s** |

## Tools + versions
| Tool / library | Version | Role |
|----------------|---------|------|
| macOS | 25.3.0 x64 (CherryRd) | Host |
| Python | /usr/bin/python3 (system, 3.13+ era) | Runtime |
| numpy | 2.4.3 | All linear algebra (`eigvals`, `eig`, matrix products) |
| poppler `pdftotext` | 24.x (Homebrew) | Paper text extraction |
| curl | 8.x | PDF fetch |
| TeX Live | 20260301 (Homebrew Cellar) | `pdflatex` compilation of REPORT.tex |
| bash / zsh | zsh (default) | Shell |
| Marker | **not installed** on CherryRd — see failure_analysis.md; `extraction/marker.md` is a `pdftotext` fallback with an explicit provenance header |
| Nougat | **not installed** on CherryRd — same story; `extraction/nougat.mmd` is a `pdftotext -layout` fallback with an explicit provenance header |

## Codes / scripts written
| File | LOC | Purpose |
|------|-----|---------|
| `report/evidence/qsa_szegedy.py` | 405 | Full replication: Ising instance generator, Metropolis transition matrix (verified column-stochastic + detailed-balanced), classical spectral gap, Szegedy walk W = R_B R_A on d²-dim edge space (isometries X, Y explicit), quantum phase gap, coherent Gibbs state check, aggregate PASS/FAIL verdict. |
| `report/REPORT.tex` | ~200 | Section-by-section LaTeX replication report. |
| `report/open_questions.json` | 5 entries | Post-replication open questions with next-steps. |

## What ran, in order
```
mkdir -p ~/Dropbox/REPLICATE-PROJECT/QC-200/QC-0712.1008-quantum-simulated-annealing-somma-boixo-knill-ortiz/{work,extraction,report/evidence}
curl -sSL https://arxiv.org/pdf/0712.1008 -o work/paper.pdf
cp work/paper.pdf paper.pdf
pdftotext -layout work/paper.pdf work/paper.txt
pdftotext           work/paper.pdf work/paper_flow.txt

# extraction/ fallbacks (real Marker/Nougat unavailable)
{ echo '<provenance header>'; pdftotext           work/paper.pdf -; } > extraction/marker.md
{ echo '<provenance header>'; pdftotext -layout   work/paper.pdf -; } > extraction/nougat.mmd

# numerical replication
python3 report/evidence/qsa_szegedy.py 2>&1 | tee report/evidence/run.log
# -> report/evidence/qsa_results.json + verdict REPLICATED

# report
pdflatex -interaction=nonstopmode -halt-on-error report/REPORT.tex   # -> REPORT.pdf, 5 pages, 289 KB
```

## Key numerical calls (per (n, β) instance)
- Build `M ∈ R^{d×d}` with d = 2^n (Metropolis, n ∈ {4,5,6} → d ∈ {16,32,64})
- `numpy.linalg.eigvals(M)` — classical spectrum
- Build isometries X, Y ∈ R^{d²×d}; reflections R_A, R_B ∈ R^{d²×d²}, walk W = R_B R_A ∈ R^{d²×d²}
- `numpy.linalg.eigvals(W)` — quantum spectrum, largest instance is W ∈ C^{4096×4096}, still trivial on CPU
- `numpy.linalg.norm(W ψ_G − ψ_G)` — coherent Gibbs residual check

## Effort estimate
- **Human/agent LOC written:** ~605 total (405 python + ~200 LaTeX + 5 JSON questions + this workflow + failure + artifacts summary).
- **Compute wall-clock:** ~4 s for the entire numerical experiment (all 15 rows), including diagonalization of five 4096×4096 quantum walk matrices.
- **Runs executed:** 1 successful replication run (no false starts on the numerical side).
- **API calls:** 0 LLM calls; entirely offline + numerical.
- **Human/agent turns:** 1 subagent turn (this one), single-shot.
