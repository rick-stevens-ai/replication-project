# Workflow — QC-0808.0369 Mosca "Quantum Algorithms" survey replication

## What this replication is
Michele Mosca 2008 is a review-mode survey with no unique novel empirical claim
of the author's own. The QC-200 wave brief for this dir therefore called for a
**spot-check reproduction**: pick two representative algorithms Mosca covers,
run each on a small-but-faithful instance in Qiskit statevector, and check
that the numbers match the closed-form predictions the paper cites. Verdict
vocab: SPOT-CHECK if both hit, else PARTIAL.

## Steps executed
1. **Fetch paper**
   - `curl https://arxiv.org/pdf/0808.0369 -o work/paper.pdf`
   - Copied to `paper.pdf` at the target-dir root (artifact 1).
   - `pdftotext paper.pdf paper.txt` for skim; `pdftotext -layout` and
     `-raw` variants for the extraction fallbacks (artifacts 2 and 3).
2. **Environment setup**
   - Fresh venv `.venv/` on CherryRd (macOS, Python 3.13).
   - `pip install qiskit qiskit-aer numpy` → Qiskit 2.5.0.
   - No LLM inference required for the reproduction; no external endpoint
     called.
3. **Pick spot-check targets**
   - Section 5 (amplitude amplification) → **Grover on N=8, M=1**.
     Non-trivial (needs 2 iterations), small enough for exact statevector,
     matches a closed-form success probability Mosca cites in general form.
   - Section 4 (Shor factoring / order-finding / Abelian HSP) → **Order-
     finding for a=7 mod N=15**, m=8 counting qubits.  Classical order
     r=4 divides 2^m=256 exactly, so the QFT gives four clean peaks each of
     probability 1/r, which is the exact assertion Mosca makes about peaks
     at multiples of 1/r.
4. **Implement + run**
   - `report/evidence/grover_N8.py` (139 LOC): oracle + diffuser +
     `Statevector.from_instruction` + theory-comparison + JSON dump.
   - `report/evidence/orderfinding_a7_N15.py` (140 LOC): H^m on counting
     qubits, |1⟩ init on 4 work qubits, controlled-`UnitaryGate(perm)^{2^j}`
     for j=0..7, inverse `QFT(...)`, statevector marginal, continued-
     fraction recovery, JSON dump.
   - Both scripts write `*_result.json` and stdout log `*_result.log`.
5. **Compare vs paper**
   - Grover: simulation 0.94531 vs theory sin^2(5θ)=0.94531 → **MATCH** at 1e-6.
   - Order-finding: 4 peaks at k∈{0,64,128,192} each with P=0.25000, sum=1.0,
     continued fractions recover r=4 → **MATCH**.
6. **Write reports and inventory**
   - `report/REPORT.tex` — detailed LaTeX, claims table, results-vs-paper,
     verdict, Open Questions.
   - `report/open_questions.json` — 5 new questions with {q, basis, next_steps}.
   - `report/artifacts_summary.md` — this + inventory.
   - `report/failure_analysis.md` — honest friction log.

## Tools + versions
| Tool | Version | Purpose |
|---|---|---|
| Python | 3.13.x | driver |
| Qiskit | 2.5.0 | statevector simulator + circuit construction |
| numpy | latest (whatever pip installed) | matrices, argsort, complex arithmetic |
| poppler pdftotext | (system) | PDF → text for skim + Marker/Nougat fallback |
| curl | (system) | fetch arXiv PDF |

## Estimate of work
- Wall clock: ~15 minutes end-to-end (including pip install, PDF skim,
  writing both scripts, running both, writing REPORT.tex, JSON, workflow,
  artifacts, failure_analysis).
- Compute: negligible — both simulations complete in <1s on CPU. No GPU
  needed; no noise model; statevector dim 8 for Grover and 2^12=4096 for
  order-finding. Neither circuit is transpiled to hardware, both are run
  directly through the reference `Statevector.from_instruction` path.
- LLM tokens: 0 for the replication itself (no Argo/Sophia calls for the
  reproduction; the report is a hand-written writeup, not an LLM summary).

## What we deliberately did NOT do
- We did NOT implement noisy simulations, shot-based sampling, or hardware
  transpilation. Mosca's exposition is fully idealised, so exact statevector
  is the appropriate comparison target.
- We did NOT implement Sections 6–11 (simulation, non-Abelian HSP, walks,
  adiabatic, topological, quantum tasks). A full survey replication would
  need one QC-100/QC-200 sub-project per topic, which is out of scope for a
  single-paper subagent.
- We did NOT install Marker or Nougat. Their absence is called out in the
  extraction stanzas, and pdftotext -layout / -raw were used instead per
  the sibling QC-200 convention.
