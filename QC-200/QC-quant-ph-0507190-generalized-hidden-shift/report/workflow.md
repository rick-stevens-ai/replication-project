# Workflow — Childs & van Dam (2005) replication

## Objective
Reproduce numerically the two headline quantitative claims of arXiv:quant-ph/0507190:
1. **Closed-form PGM success probability, Eq. (15).**
2. **Lemma 2:** Pr(1 ≤ η_w^x ≤ 4) is bounded below by a constant when M = ⌊N^(1/k)⌋, k ≥ 3.

Both claims underpin the paper's main **Theorem 3**: efficient poly(log N) quantum algorithm for the generalized hidden shift problem whenever M ≥ N^ε.

## Timeline (2026-07-05, subagent session)

| Step | Action | Duration |
|---|---|---|
| 1 | Read wave brief `~/Dropbox/REPLICATE-PROJECT/scripts/QC_WAVE_BRIEF_2026-07-03.md` | 1 min |
| 2 | Create target dir `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-0507190-generalized-hidden-shift/` | <1 min |
| 3 | Fetch paper via `curl -sL https://arxiv.org/pdf/quant-ph/0507190 -o paper.pdf` (222 KB, 16 pp) | <1 min |
| 4 | `pdftotext paper.pdf work/paper.txt` and skim | 2 min |
| 5 | Identify Eq. (15) + Lemma 2 as the concrete testable claims | 1 min |
| 6 | Set up `.venv` with qiskit 2.5.0, qiskit-aer, numpy 2.5.1, matplotlib | 2 min |
| 7 | Draft `code/childs_vandam_pgm.py` (Test A + B + C) | ~15 min |
| 8 | **Bug fix 1:** initial nested-loop enumeration of η too slow (dying on k=4, N=32). Rewrote as FFT-based combinatorial convolution. Verified against brute-force enumeration on 3 cases. | ~5 min |
| 9 | **Bug fix 2:** Qiskit end-to-end initially used rank-1 factorization E_j = |f_j⟩⟨f_j|; incorrect because E_j is generically full-rank block-diagonal per x. Rewrote using Kraus construction K_j = sqrt(E_j) + Naimark dilation with QR completion in support subspace of Σ. | ~15 min |
| 10 | Full run: Test A sweep (24 rows), Test B (4 rows), Test C (3 Qiskit runs) | 8 min wall |
| 11 | Generate figures via `code/make_figures.py` (3 PNG) | <1 min |
| 12 | Write extraction fallbacks (marker.md, nougat.mmd) | 3 min |
| 13 | Write REPORT.tex, open_questions.json, this workflow, artifacts_summary, failure_analysis | ~10 min |

Total: ~1 hour of wall-clock time.

## Tools & versions

| Tool | Version | Role |
|---|---|---|
| macOS | Darwin 25.3.0 | host |
| Python | 3.14.6 | driver |
| Qiskit | 2.5.0 | quantum circuit builder + statevector simulator |
| qiskit-aer | (bundled with 2.5.0) | AerSimulator method="statevector" |
| numpy | 2.5.1 | density matrices, POVM construction, FFT convolution for η counting |
| scipy | latest | (transitively imported) |
| matplotlib | latest | figures |
| pdftotext | poppler | PDF → text extraction (fallback since marker/nougat not installed) |
| curl | system | fetching arXiv |
| Argo proxy | localhost:44497 | free LLM endpoint (not actually invoked in this replication — everything is deterministic sim) |

## Reproducibility

Everything lives inside the target dir:

```
QC-quant-ph-0507190-generalized-hidden-shift/
├── paper.pdf
├── work/                             # intermediates
│   └── paper.txt                     # pdftotext dump
├── extraction/
│   ├── marker.md                     # (pdftotext-derived fallback)
│   └── nougat.mmd                    # (pdftotext-derived fallback)
├── code/
│   ├── childs_vandam_pgm.py          # main simulation (Test A + B + C)
│   └── make_figures.py               # matplotlib plots
├── figures/
│   ├── fig1_pgm_success_vs_N.png
│   ├── fig2_lemma2_fraction.png
│   └── fig3_M_too_small_regime.png
├── report/
│   ├── REPORT.tex                    # replication report (this file's parent)
│   ├── open_questions.json           # 5 heavy-duty follow-ups
│   ├── workflow.md                   # THIS file
│   ├── artifacts_summary.md
│   ├── failure_analysis.md
│   └── evidence/
│       ├── results.json              # machine-readable numerical output
│       └── run_log.txt               # full stdout of the sim run
└── .venv/                            # (gitignored) virtualenv with qiskit 2.5.0
```

To re-run end-to-end:
```bash
cd QC-quant-ph-0507190-generalized-hidden-shift/
python3 -m venv .venv
source .venv/bin/activate
pip install qiskit qiskit-aer numpy scipy matplotlib
python code/childs_vandam_pgm.py     # ~8 min wall
python code/make_figures.py
```

## Estimate of work done

- **Fetching + reading the paper:** ~5 minutes.
- **Coding the numerical PGM + η enumeration:** ~25 minutes of active coding plus ~15 minutes of debugging the Naimark rank-1-vs-full-rank bug.
- **Running:** ~8 minutes of CPU (single core, ~1 GB RAM peak at k=4, N=24).
- **Report writing:** ~15 minutes.

The **cross-check that operational Tr(E_s σ_s) equals analytic Eq. (15) to 1e-16** is what makes this a real replication and not just a code-runs-something exercise: both quantities are computed independently (Eq. (15) via combinatorics on η_w^x; the operational trace via numpy eigendecomposition of Σ and matrix products on density matrices), and they agree to machine precision. That confirms my POVM implementation is correct, and the Qiskit end-to-end then verifies that the paper's Naimark dilation can be run as an actual quantum circuit.

## Note on the Lenstra IP subroutine (Section 4 of the paper)

The paper's efficiency claim in Theorem 3 depends on Lenstra's polynomial-time algorithm for k-dimensional integer programming as the classical subroutine implementing the quantum sampling `|w,x⟩ → |S_w^x, x⟩`. We do **not** re-implement Lenstra here; for our small-N enumeration we brute-force enumerate S_w^x directly (which is polynomial in the enumerated regime since |{0..M-1}^k| = M^k is tiny for our (M,k)). This is equivalent for correctness testing at small N, but means we cannot verify the *asymptotic* poly(log N) complexity claim — only the success-probability claim. This limitation is explicitly noted in REPORT.tex Section "Verdict".
