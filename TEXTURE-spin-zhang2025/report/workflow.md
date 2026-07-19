# Workflow — zhang2025 (arXiv:2503.17916)

## Narrative
1. Fetched PDF; pdftotext (~9.8k words, marker.md); Nougat stub (GPU, sha256 logged).
2. Read abstract + Sec III + Table I: identified the reproducible-on-CPU content = the paper's own moment/splitting correlation (Table I) + the mechanism (strain-induced Stoner altermagnetism, SOC-free splitting). Flagged DFT+Wannier+Kubo theta_AS as out of scope.
3. Transcribed Table I (Ets 0-6%: moment muB, |Splitting|max meV).
4. C1: computed Pearson (all AM pts + rising branch) and Spearman rho on Table I -> positive but sub-linear/dome (honest).
5. C2: minimal strain-driven Stoner mean-field dome; matched onset (~2.5%) and peak (~4.3%) to Table I.
6. C3: SOC-free d-wave TB, t_AM ∝ moment; confirmed nonzero splitting linear in m without SOC (nonrelativistic).
7. Adjusted C1 to report the honest positive-but-nonlinear correlation (dome collapse lowers single Pearson).
8. LLM-judge (free Argo sonnet-4.6): PARTIAL, coverage 7, agreement 6.

## Tools & codes
Python 3.13, NumPy, SciPy (spearmanr), Matplotlib; pdftotext. code/zhang2025_replication.py (~180 LOC). LLM-judge -> argo:claude-sonnet-4.6 (free).

## Effort estimate
CPU-only, ~2s runtime. Wall clock ~15 min incl. Table I transcription + honest C1 recalibration. ~180 LOC, 2 iterations.
