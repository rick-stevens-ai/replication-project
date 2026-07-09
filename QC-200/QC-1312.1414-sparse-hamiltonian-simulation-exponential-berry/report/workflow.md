# Workflow — arXiv:1312.1414 (Berry, Childs, Cleve, Kothari, Somma) replication

Date: 2026-07-05
Wave: QC-200 (paper QC-1312.1414-sparse-hamiltonian-simulation-exponential-berry)
Executor: automated subagent under Rick Stevens' `REPLICATE-PROJECT` framework.

## Steps executed (in order)

1. **Directory setup**
   - `mkdir -p work extraction report/evidence` under target dir.

2. **Paper acquisition + identity verification**
   - `curl -sL -o work/paper.pdf https://arxiv.org/pdf/1312.1414`
   - `file paper.pdf` → PDF v1.4, 28 pages.
   - `pdftotext paper.pdf paper.txt` → 2,026 lines.
   - Verified from first page: title = *Exponential improvement in precision for simulating sparse Hamiltonians*, authors = Berry, Childs, Cleve, Kothari, Somma, arxiv v2 = 7 Oct 2014. Matches task brief.

3. **Claim harvesting**
   - `grep -n -i "Taylor|LCU|linear combin|K =|truncat|segment|amplitude amplif"` on `paper.txt` → confirmed the paper explicitly uses:
     - Taylor-series truncation of $e^{-iHt}$,
     - LCU (linear combinations of unitary operations),
     - segmented fractional-query gadget,
     - oblivious amplitude amplification.
   - Extracted headline complexity O(τ · log(τ/ε) / log log(τ/ε)) from the abstract.

4. **Extraction artifacts (Marker + Nougat)**
   - `marker` and `nougat` not installed on this host, and no central corpus at `~/Dropbox/REPLICATE-PROJECT/central-corpus/` exists as of 2026-07-05.
   - Fallback per 8-artifact bar: produced `extraction/marker.md` and `extraction/nougat.mmd` from `pdftotext` output with an explicit provenance banner at the top of each so downstream consumers know they are text-only proxies, not true Marker/Nougat parses.
   - Fixing this properly would require installing Marker+Nougat and re-parsing (see `failure_analysis.md`).

5. **Numerical replication**
   - Wrote `report/evidence/lcu_taylor_sim.py`.
   - Constructed a random d=2-sparse 8×8 Hermitian H with seed 20260705 (deterministic).
   - Gold: `scipy.linalg.expm(-1j*H*t)` for t ∈ {0.5, 1.0}.
   - LCU/Taylor: U_K = Σ_{k=0}^K (-it)^k H^k / k! for K ∈ {1,2,4,6,8,10,12,14,16,20}.
   - Trotter 1st-order baseline: split H = D (diagonal) + X (off-diagonal), then (exp(-iD t/r)·exp(-iX t/r))^r with r = K.
   - Metrics: Frobenius, spectral, and state-vector error vs. the exact evolution; analytic Taylor bound (||H||₂t)^(K+1)/(K+1)!.
   - Structural check: LCU prepare amplitudes √(c_k)/√s with c_k = t^k/k!, verified Σ |amp|² = 1 and s → e^t.
   - Wrote `results.json` (all numbers) and `eps_vs_K.png` (semilog plot).

6. **Empirical scaling**
   - Fit slope of log(eps_LCU) vs. log((K+1)!) and log(eps_trot) vs. log(K).
   - Trotter slope came out −1.001 (t=0.5) and −1.006 (t=1.0) — perfect match to product-formula theory.
   - LCU slope came out −0.876 (t=0.5) and −0.806 (t=1.0) — close to −1 but slightly shallow (limited by double-precision floor at K≥16; see Q2 in open questions).

7. **Report assembly**
   - `report/REPORT.tex` — full section-by-section report with claim table, exact commands, results-vs-paper table, verdict, and 5 open questions.
   - `report/open_questions.json` — 5 grounded open questions with `{q, basis, next_steps}`.
   - `report/artifacts_summary.md` — this workflow's sibling.
   - `report/failure_analysis.md` — honest gaps.

## Tools + versions

| Tool | Version | Purpose |
|---|---|---|
| Python 3 (system) | 3.13 | Runtime |
| numpy | 2.4.3 | Linear algebra, matrix powers, RNG |
| scipy | 1.18.0 | `scipy.linalg.expm` gold-standard evolution |
| matplotlib | (Agg backend) | eps-vs-K semilog plot |
| poppler `pdftotext` | system | PDF → text extraction |
| `curl` | system | arXiv PDF fetch |
| Marker | NOT INSTALLED | (fallback used) |
| Nougat | NOT INSTALLED | (fallback used) |
| Qiskit / Cirq | NOT NEEDED for the ideal-LCU test; would be needed to compile SELECT + oblivious AA (Q3, Q5) |
| Argo LLM proxy | NOT INVOKED (deterministic numerical replication; no LLM-judge needed for a match-the-analytic-bound test) |

## Work estimate

| Phase | Wall time |
|---|---|
| PDF fetch + text + skim + claim extraction | ~3 min |
| Environment probe + design of LCU sim | ~4 min |
| Code writing (`lcu_taylor_sim.py`, 240 lines) | ~5 min |
| Run + verify + plot | <1 min (all 20 K-values on 8×8) |
| Extraction fallbacks + reports (REPORT.tex, workflow.md, artifacts_summary.md, failure_analysis.md, open_questions.json) | ~10 min |
| **Total wall time** | **~25 min** |

## Reproducibility

`python3 report/evidence/lcu_taylor_sim.py` will regenerate `results.json` and `eps_vs_K.png` bit-identically thanks to the fixed seed (20260705).
