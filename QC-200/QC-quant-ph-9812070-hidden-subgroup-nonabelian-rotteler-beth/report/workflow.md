# Workflow — QC-200 replication of arXiv:quant-ph/9812070

## Environment
- Host: CherryRd (macOS Darwin 25.3, x64)
- Python: `/usr/local/bin/python3` (system python3)
- NumPy: 2.4.3
- Poppler `pdftotext` (for text extraction)
- No LLM calls made — analytic paper, math + numpy sufficient.
- No paid endpoints touched. Free tier only.

## Tools NOT used (and why)
- **Qiskit / Cirq / PennyLane**: not needed. The paper's DFT_{W_n} is
  a small (32x32 at n=2, 128x128 at n=3) real orthogonal matrix; numpy
  does everything at machine precision. A gate-level Qiskit simulation
  would reproduce the same input/output behavior but adds no scientific
  content beyond what the numpy simulation already establishes.
- **Marker / Nougat**: not installed on this host; paper is text-native
  LaTeX with no OCR concerns, so `pdftotext -layout` gave a faithful
  extraction that captured every algorithm step, definition, and
  equation used downstream. See `failure_analysis.md`.
- **Argo LLM (`localhost:44497`)**: available but unused. No LLM judge
  needed: verdict follows deterministically from the empirical success
  probability table.

## Steps executed
1. **Fetch paper** (`work/paper.txt`)
   - `curl -sL -o paper.pdf https://arxiv.org/pdf/quant-ph/9812070`
   - `pdftotext -layout paper.pdf work/paper.txt`
   - Verified: authors "Martin Rötteler, Thomas Beth", title
     "Polynomial-Time Solution to the Hidden Subgroup Problem for a
     Class of non-Abelian Groups", 16 pages, arxiv id
     `quant-ph/9812070v1` (24 Dec 1998). Matches task metadata.

2. **Read the paper** end-to-end. Extracted:
   - Group definition W_n = Z_2^n wr Z_2, order 2^{2n+1}
   - Multiplication rule (paper p.4, top)
   - Pairing mu (Def. 4.3, three cases on a, a')
   - Fourier matrix DFT_{W_n} with entries (-1)^{mu(g,h)} / sqrt(|G|)
   - Algorithm 7.1 (steps 1-9)
   - Lemma 6.3 failure bound 2^{-i/4}
   - Sec. 4.1 abelian HSP subroutine for U ∩ N

3. **Implement + verify** (`report/evidence/hsp_wreath.py`, ~350 lines)
   - Enumerate group and index elements
   - Multiplication (assert closure under inverse, exponent divides 4)
   - Subgroup closure BFS
   - Pairing mu
   - Build DFT; assert F @ F^T = I to 1.1e-16
   - Coset sampler
   - phi bijection W_n → F_2^{2n+1}
   - Nullspace-based classical postprocessing
   - Abelian-HSP subroutine on N
   - Full Algorithm 7.1

4. **Main experiment** — 6 random subgroups at n=2 (3× |U|=2, 3× |U|=4),
   32 samples/rep, 10 reps each. All 6 hit p_success = 1.00.
   - Output: `report/evidence/results.json`, `run.log`

5. **Stress + non-abelian focus + scaling**
   (`report/evidence/scaling_and_stress.py`, ~150 lines)
   - Sample-count sweep {2..32} at n=2, 5 subgroups × 20 reps each
   - 5 non-abelian-focused subgroups (transversal generators) × 20 reps
   - Scaling test at n=3 (|G|=128) × 6 subgroups × 10 reps × 12 samples
   - Total wall-clock: 2.75 seconds
   - Output: `report/evidence/stress_results.json`, `stress_run.log`

6. **Write reports**
   - `report/REPORT.tex` — full LaTeX report with claims, method,
     results, verdict, open questions
   - `report/open_questions.json` — 5 Q + basis + next_steps
   - `report/workflow.md` — this file
   - `report/artifacts_summary.md` — inventory
   - `report/failure_analysis.md` — honest gaps

## Effort estimate
- ~20 minutes reading the paper + notes
- ~30 minutes implementing hsp_wreath.py (algorithm + sanity checks)
- ~10 minutes stress/scaling script
- ~2 minutes total compute (both scripts combined)
- ~30 minutes writing the LaTeX report + auxiliary docs
- **Total wall-clock: ~1.5 hours end-to-end**

## Reproducibility
- All seeds are hardcoded in the scripts (main: `random.Random(2026-7-5)` = 2014;
  stress: 1234, 9999, 31415).
- Rerun end-to-end with:
```
python3 report/evidence/hsp_wreath.py
python3 report/evidence/scaling_and_stress.py
```
- Expected wall-clock ~5 seconds total on any modern laptop.
