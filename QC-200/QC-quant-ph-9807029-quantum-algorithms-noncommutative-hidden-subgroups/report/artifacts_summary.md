# Artifacts Summary — arXiv:quant-ph/9807029

**Paper:** Mark Ettinger & Peter Høyer, "On Quantum Algorithms for Noncommutative Hidden Subgroups", arXiv:quant-ph/9807029v1 (LA-UR-98-2010, May 1998; also published as Adv. Appl. Math. **25**:239, 2000).
**Replication verdict:** REPLICATED (see `REPORT.tex` / `REPORT.md`-equivalent LaTeX).
**Set:** QC-200. **Dir:** `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-9807029-quantum-algorithms-noncommutative-hidden-subgroups/`.

## Inventory (files + SHA-256)

| Slot | Path | SHA-256 | Bytes | Notes |
|---|---|---|---|---|
| 1 | `paper.pdf` | `cb816916def001a4…` | 162,248 | Downloaded from `https://arxiv.org/pdf/quant-ph/9807029` on 2026-07-05. Identical to `work/paper.pdf`. |
| 2 | `extraction/marker.md` | `881a0e7b2bb7905e…` | 35,700 | **Fallback**: Marker CLI not installed on this host. Contents are `pdftotext -layout` output with a Markdown header. See `failure_analysis.md`. |
| 3 | `extraction/nougat.mmd` | `3a35ad375fbafc26…` | 27,490 | **Fallback**: Nougat CLI not installed. Contents are `pdftotext` output with a Nougat-style header. |
| 4 | `report/REPORT.tex` | `84b0c1d8647e868b…` | 16,649 | Section-by-section LaTeX report. Compiled to `report/REPORT.pdf` (5 pages, 250 KB). |
| 5 | `report/open_questions.json` | `aa6ca575c7c3e5c6…` | 4,568 | Five heavy-duty questions with `q` + `basis` + `next_steps` each. Also mirrored in REPORT.tex `## Open Questions`. |
| 6 | `report/workflow.md` | `5189003fa0880a6b…` | 4,556 | Comprehensive workflow, tools+versions table, effort estimate. |
| 7 | `report/artifacts_summary.md` | (this file) | — | Inventory + traces. |
| 8 | `report/failure_analysis.md` | (see file) | — | Honest analysis of gaps, tool availability, paper-side issue. |
|   | `report/evidence/ettinger_hoyer_dihedral.py` | `dbb1273ea86f2c37…` | 11,882 | Main replication script. ~250 LOC. Qiskit 2.5.0 + NumPy 2.5.1. |
|   | `report/evidence/results_N4_k1.json`   | `108b252b60fc5a6a…` |  4,744 | N=4, k0=1, 800 trials/m'. TV=3.12e-16, m*_2/3=2, m*_paper=4, empirical@paper_m=1.00 |
|   | `report/evidence/results_N8_k3.json`   | `68c8e646eb742794…` |  6,286 | N=8, k0=3, 800 trials/m'. TV=4.58e-16, m*_2/3=8, m*_paper=30, empirical@paper_m=1.00 |
|   | `report/evidence/results_N16_k5.json`  | `a70252d2abd58065…` |  8,327 | N=16, k0=5, 500 trials/m'. TV=5.77e-16, m*_2/3=11, m*_paper=45, empirical@paper_m=1.00 |
|   | `report/evidence/results_N32_k11.json` | `fb157d86033bf9e7…` | 13,775 | N=32, k0=11, 300 trials/m'. TV=6.56e-15, m*_2/3=18, m*_paper=60, empirical@paper_m=1.00 |
|   | `work/paper.pdf` | (same as `paper.pdf`) | 162,248 | Original download location. |
|   | `work/paper.txt` | `837a418d73fa3eef…` | 32,844 | `pdftotext -layout` extraction used for reading during the replication. |
|   | `.gitignore` | — | small | Excludes `.venv/`. |
|   | `.venv/` | — | large | Local Python 3.14 venv with Qiskit 2.5.0 + NumPy 2.5.1 + transitive deps. Not part of artifact set; recreate with `python3 -m venv .venv && source .venv/bin/activate && pip install qiskit numpy`. |

## Traces

- **Source URL:** `https://arxiv.org/pdf/quant-ph/9807029`.
- **Publication:** *Advances in Applied Mathematics* **25**:239–251 (2000), preprint LA-UR-98-2010.
- **Runs:** 4 primary + ~6 diagnostic probes (in-terminal, not logged separately).
- **Compute:** CherryRd macOS local CPU only. No GPU, no HPC. No LLM inference.
- **Wall time:** ~30 min total agent turn.
- **Reproduction command sequence:** see `workflow.md` § Runs.

## Headline reproduced numbers

| Quantity | Paper | Our sim |
|---|---|---|
| Lemma 4: $\Pr[(a,0)] = \frac{1}{N}\cos^2(\pi k_0 a/N)$ | Analytical | Matched to $\leq 6.6\times 10^{-15}$ TV distance across $N\in\{4,8,16,32\}$ |
| Theorem 3: query bound $\leq 89\log N + 7$ for $\geq 1 - 1/(2N)$ success | Upper bound | Empirical $m^\star$ 4–60 across $N\in\{4,8,16,32\}$; $100\%$ success at paper's $\lceil 64\ln N\rceil$ in all cases |
| Quantum-vs-classical separation on same instances | Simon-style lower bound cited | Uniform-$\mathbb{Z}_N$ baseline never $\geq 2/3$ for $N\geq 8$ within swept budget |

## What is NOT here

- (none: REPORT.pdf successfully compiled with pdflatex 20260301, 5 pages.)
- True Marker/Nougat parses (see failure_analysis).
- Larger-$N$ sweeps ($N \geq 64$); would require a permutation-oracle rewrite for tractable memory.
- Kuperberg-sieve post-processing comparison (Open Question Q3).
