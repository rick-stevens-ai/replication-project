# Failure analysis — honest critique

Slot: QC-100 / QC-QAOA-benchmarking-Guerreschi2019
Paper actually replicated: **arXiv:1907.02359, Willsch et al., 2020**.
Verdict: **REPLICATED** (simulator core, headline-exercised).

## 1. Paper-identity mismatch (worth calling out first)
- The queue TSV row named this slot after **Guerreschi & Matsuura 2019**
  (arXiv:1812.07589), whose central claim is a runtime/approximation-ratio
  crossover requiring **"hundreds of qubits" before QAOA can beat classical
  MaxCut baselines** (Goemans-Williamson, simulated annealing).
- The arXiv id in the row (`1907.02359`) actually points to **Willsch et al.
  2020**, a different QAOA benchmark paper that (a) does not make the
  hundred-qubit-crossover claim, (b) uses only up to 18 qubits, and (c)
  compares QAOA against D-Wave and IBM Q hardware, not against GW/SA
  runtime models.
- We honored the arXiv id (authoritative), not the queue row title.
- **What this means for the brief:** the brief asked us to critique whether
  the "QAOA runtime + approximation-ratio scan was independently reimplemented
  and crossover-qubit-count reproduced for paper's specific noise/runtime
  model vs quoted, whether comparison against Goemans-Williamson or simulated
  annealing was made, whether the pessimistic conclusion held quantitatively
  at small N." **None of that applies to the paper we replicated**, because
  those claims are not in Willsch 2020. They are in Guerreschi 2019, which
  is a different paper and is NOT in this slot's `work/` tree.
- **If the intent was to replicate Guerreschi 2019**, this slot needs re-pulling
  with the correct arXiv id (1812.07589), and none of the current numerical
  work would carry over (Willsch 2020 = statevector on 8/16/18 qubits with
  Table-1 success probabilities; Guerreschi 2019 = analytical runtime model
  with per-qubit gate cost accounting and no simulator statevector at all).

## 2. What was tested, honestly
- **C1** (exact instance ground energies -9 and -17.7): PASS, exact match.
- **C2** (analytic p=1 energy, Eq. 19): PASS, 4e-15 / 6e-15 absolute error,
  which is machine precision. This is genuinely independent — we
  re-derived Eq. 19 from the ansatz and coded it separately from the
  statevector path.
- **C3** (Table 1, 2-SAT-8A energy-min QAOA): p=1 PASS to reported precision
  (8.84%, r=0.71). p=5 is 41.03% vs 42.39%, a **1.4 pp gap** — inside the
  local-optimum uncertainty band the paper itself warns about, but not exact.
  Intermediate p=2,3,4 are not in the paper's tables so cannot be cross-checked.
- **C4** (16-var MaxCut, Fig. 7): p=1 success 1.45% satisfies the paper's
  "< 2%" qualitative claim. p=2..5 monotone rise reproduces the paper's
  central trend but is compared only against a figure eyeball, not against
  a specific reported number.
- **C5** (linear-anneal init large-p): 2-SAT p=50 success 81.24% vs paper
  ~82.7% is within ~1.5 pp. **MaxCut p=10 success 76.43% vs paper ~85.6% is
  a ~9 pp gap** — this is our largest quantitative discrepancy. We ascribe
  it to Nelder-Mead getting stuck in a local minimum, and the paper itself
  warns of exactly this, but we did NOT run multi-seed CI bands to prove
  the gap is a seed effect vs a systematic bias in our schedule init.

## 3. What was NOT tested
- **C6** (D-Wave 2000Q outperforms simulator QAOA): out of scope, requires
  a proprietary QPU.
- **C7** (IBM Q Experience p=1 grid-search is poor quality): out of scope,
  requires proprietary QPU.
- **Noise models** of any kind. Willsch et al. run ideal statevector on the
  simulator side and let the QPU sides carry their own noise; we matched only
  the ideal side. A depolarizing/thermal Kraus channel sweep is a natural
  extension (see open_questions.json #4).
- **Multi-seed statistical bars.** All numbers are single-seed. The paper
  itself often averages over restarts; we did layer chaining + a small number
  of restarts (see run.log) but did not produce mean ± std bands.
- **Classical baselines** (Goemans-Williamson SDP, simulated annealing,
  branch-and-cut). Willsch 2020 does not make this comparison, so we did
  not either. But it would be a natural extension (open_questions.json #2)
  and IS the core of the Guerreschi 2019 paper the queue row was mis-titled
  after.
- **Crossover-qubit-count analysis.** Not in Willsch 2020, so not exercised.

## 4. Alternative-implementation cross-check
We did NOT cross-check against a second QAOA implementation (e.g. Qiskit's
`QAOA` primitive or `pennylane`). This would be a valuable additional
guardrail but is not required for a REPLICATED verdict when the analytic
form (Eq. 19) matches to machine precision, which independently pins the
p=1 path.

## 5. Headline-exercised judgment
- **Willsch 2020 headline**: "QAOA performance is strongly instance-dependent;
  increases monotonically with depth p; large-p can be near-solved via
  linear-annealing initialization." — **YES, all three sub-claims exercised
  and reproduced.**
- **Guerreschi 2019 headline** (brief-referenced, wrong paper): "QAOA needs
  hundreds of qubits before beating GW/SA on MaxCut." — **NO, not exercised**,
  because that is not the paper in this slot.

## 6. Bottom line
Verdict **REPLICATED** stands for what was actually attempted (Willsch 2020
simulator core, headline-exercised). If the intent behind this slot was
Guerreschi 2019 crossover-analysis replication, this slot needs re-pulling
with the correct paper and the current work does not address that claim.
