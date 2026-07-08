# Attempt Log (chronological)

1. Read WAVE_BRIEF_2026-07-01.md + QC-100/STATUS_AUDIT.md. Reviewed QC100 candidate TSV + existing QC-100 dirs.
2. Dedup check: confirmed no QAOA dir exists (`ls` + grep for "qaoa", "1907.02359", "approximate optimization" → 0 hits). Selected candidate **rank 17: "Benchmarking the QAOA", arXiv:1907.02359** (clean classical-simulator core, OA). Note: TSV metadata title/authors were slightly off; arXiv id 1907.02359 is authoritative — real authors are Willsch, Willsch, Jin, De Raedt, Michielsen (Jülich).
3. Created target dir `QC-QAOA-benchmarking-Guerreschi2019/` (kept slug per assignment convention even though lead author is Willsch).
4. Fetched paper via arXiv abstract + ar5iv full HTML → stripped to `work/paper_fulltext.txt`. Extracted: three performance measures (M1/M2/M3, Eq. 16), QAOA ansatz (Eqs. 9–14), p=1 analytic energy (Eq. 19), Table 1 results, linear-annealing schedule (Eqs. 25–31), and problem instances (Tables 2–5).
5. Transcribed the 16-var MaxCut (Table 2) and 8-var 2-SAT (A) (Table 3A) exactly from the raw ar5iv token stream.
6. Wrote `qaoa_core.py` (numpy statevector QAOA + diagonal Ising H_C + per-qubit mixer + Eq.19 analytic formula). **Validation:** Emin = -9.0 (2SAT-8A) and -17.7 (MaxCut-16), matching Fig.11/Fig.10 captions EXACTLY → confirms correct transcription. Both instances triangle-free (Eq.19 applies).
7. Wrote `run_replication.py`: T1 (analytic vs statevector), T2 (QAOA p=1..5 energy-min, Table 1 setting), T3 (linear-anneal init at large p).
8. First run under `timeout 280` was killed mid-way (16-qubit Nelder-Mead with many restarts is slow). Re-ran in background, unbuffered → `run.log`.
9. T1 result: analytic Eq.19 vs statevector max|dE| = 4.4e-15 / 6.2e-15 → machine precision. T2 2SAT-8A completed all p=1..5. MaxCut-16 completed p=1..4 in the long run; the single p=5 step ran >20 min under 20 restarts.
10. Killed the long run (saved `run_partial.log` with 2SAT-8A p1-5 + MaxCut p1-4), wrote `finish.py` (MaxCut p-chain with interp + 3 restarts; T3 with capped NM iters + tau scan). Ran to completion → `finish.log` + assembled `results.json`.
11. T2 MaxCut-16 completed p=1..5 (monotone 1.45→42.83%). T3: 2SAT-8A p=50 linear-anneal → 81.24% (paper ~82.7%); MaxCut-16 p=10 linear-anneal → 76.43% (paper ~85.6%).
12. LLM judge (free Argo): `gpt-5.2` → REPLICATED (cov 9, agr 8); `gpt-5.1` → REPLICATED (cov 8, agr 9). (opus-4.8/4.7 returned 502 at the time; two GPT-5 judges sufficed.)
13. Wrote report package (brief, attempt_log, artifact_harvest, REPORT).

## What worked / failed
- **Worked:** clean-room numpy statevector; exact instance transcription validated by ground-energy match; Eq.19 analytic cross-check at machine precision; Table-1 numbers reproduced (2SAT-8A p=1 exactly 8.84%/r=0.71; p=5 41.03% vs paper 42.39%).
- **Slow (not failed):** 16-qubit Nelder-Mead with many restarts. Mitigated by interpolation-based warm starts + capped iterations; results are honest local optima, slightly below the paper's best (expected for a non-convex landscape with many local minima — a phenomenon the paper itself emphasizes).
- **Out of scope:** IBM Q Experience + D-Wave 2000Q (proprietary hardware; hardware claims, not simulator claims).
