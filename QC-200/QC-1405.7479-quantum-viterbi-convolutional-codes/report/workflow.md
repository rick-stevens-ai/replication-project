# Workflow

Independent replication of Grice & Meyer, arXiv:1405.7479, executed as a
QC-200 wave subagent on 2026-07-05.

## Timeline (rough)

| Step | Action | Duration |
|------|--------|---------|
| 1 | Read wave brief `QC_WAVE_BRIEF_2026-07-03.md` | ~1 min |
| 2 | Created target dir; downloaded paper.pdf from arXiv (`curl https://arxiv.org/pdf/1405.7479`) | ~30 s |
| 3 | `pdftotext paper.pdf work/paper.txt`; skimmed for headline claim | ~2 min |
| 4 | Verified authors + title from PDF page 1 (found brief had "Daniel A. Meyer" typo — actual is "David A. Meyer") | ~1 min |
| 5 | Grepped for O(sqrt), Grover, amplitude amplification, iteration to lock the L = F^N framing | ~1 min |
| 6 | Wrote `report/evidence/qva_replication.py`: encoder, BSC, classical Viterbi, trellis path enumeration, BBHT Grover, Dürr–Høyer min | ~10 min |
| 7 | First run: JSON written successfully; hit a scope bug in the summary print (MSG_LEN was inside function scope). Patched | ~1 min |
| 8 | Second run: full success — 30/30 trials matching classical argmin at L=256 | ~5 s wall |
| 9 | Wrote `report/evidence/scaling_sweep.py`: 7-point L in {16..1024} sweep, log-log fit | ~3 min |
| 10 | Sweep run: 100% success at all L; α=0.124 empirical fit | ~30 s wall |
| 11 | Wrote 8 mandatory artifacts (REPORT.tex, open_questions.json, workflow.md, artifacts_summary.md, failure_analysis.md, extraction/ stubs) | ~15 min |

Total human-perceived wall time: ~35 min. All numerical work runs in <1 min CPU.

## Tools and versions

| Tool | Version | Purpose |
|------|---------|---------|
| Python | CPython 3.13 (system, macOS 25.3) | driver |
| numpy | 2.x | real statevector, RNG, linear algebra |
| poppler / pdftotext | 25.x (macOS Homebrew) | PDF text extraction (in lieu of Marker/Nougat) |
| curl | system | fetch arXiv PDF |
| grep | system | claim mining in paper.txt |

**Explicitly NOT used:** Qiskit, Cirq, Stim, PennyLane, OpenFermion, PyMatching, cloud LLMs, paid APIs. Compliant with the free-endpoint hard rule.

## Reproducibility

Everything is deterministic under fixed seeds:
- Message RNG: `np.random.default_rng(20260705)`
- BSC noise RNG: same generator, drawn sequentially after message
- Trial RNGs: `np.random.default_rng(20260705 + trial)` for main; `np.random.default_rng(1000 + N*100 + t)` for sweep

To reproduce end-to-end:

```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-200/QC-1405.7479-quantum-viterbi-convolutional-codes
python3 report/evidence/qva_replication.py     # main experiment -> results.json
python3 report/evidence/scaling_sweep.py       # L-sweep     -> scaling.json
```

## Code lineage

All code is **fresh-written for this replication**. No blob-copy from any
prior repo. `qva_replication.py` and `scaling_sweep.py` are single-author
subagent output, ~500 lines total, no dependencies beyond numpy.

## Estimated work performed

- ~500 lines of Python (encoder + Viterbi + trellis enumeration + BBHT + Dürr–Høyer)
- ~350 lines of LaTeX / Markdown (report + artifacts)
- 1 arXiv PDF fetched (178 KB)
- 2 numerical experiments: 30-trial correctness demo + 7-size, 20-trial-per-size scaling sweep = 170 quantum-min-finding runs total, each a real statevector simulation
- 2 result JSONs; 2 stdout logs
- 8 required artifacts + 1 extraction README
