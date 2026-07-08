# Workflow — arXiv:1904.02260 (contextuality test for VQE)

Procedural log of the QC-100 replication for Kirby & Love, PRL 123, 200501 (2019).

## 0. Setup

- **Wave:** QC-100 (small-instance quantum-computing CPU sweep)
- **Host:** CherryRd (macOS 25.3.0, Python 3.13)
- **Compute budget:** small CPU only; no paid API, no GPU, no HPC
- **Date:** 2026-07-03 (backfilled 2026-07-06)
- **Replicator:** Ollie (Claude Opus 4.7 subagent)

## 1. Paper acquisition + reading

1. Downloaded PDF: `work/paper.pdf` (arXiv 1904.02260v2, published PRL 123, 200501)
2. Text extraction: `work/paper.txt` (plain-text; extraction stub also at `extraction/nougat.mmd`)
3. Identified the headline claim structure:
   - **Theoretical:** Theorem 3 gives a polynomial classifier for Pauli-set contextuality via non-transitivity of commutation on the reduced set T
   - **Empirical:** Table I applies the classifier to seven published VQE experiments (H2 x3, HeH+, LiH, BeH, H2O, Schwinger, deuteron)
   - **Interpretive:** non-contextual VQE = classically simulable via a noncontextual hidden-variable model = not genuine quantum advantage

## 2. Scope decision

- **In scope:** re-implement Theorem 3 and re-run on 6 of the Table I molecules (all H2 variants, HeH+, LiH, H2O)
- **In scope:** VQE sanity check on 2q H2 to confirm the Hamiltonian we test is chemically real
- **Out of scope:** the CD_0 heuristic quantitative values (Appendix C); BeH, Schwinger, deuteron; the underlying classical-simulability construction (Kirby-Love 2020, separate paper); comparison to alternative advantage witnesses

## 3. Environment build

```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-1904.02260-contextuality-test-vqe
python3 -m venv venv
source venv/bin/activate
pip install --quiet qiskit qiskit-nature qiskit-algorithms pyscf openfermion openfermionpyscf
```

Resolved stack: qiskit 2.5.0 · qiskit-nature 0.8.0 · openfermion 1.7.1 · openfermionpyscf · pyscf 2.13.1 · numpy · scipy.

## 4. Implementation

Wrote `code/contextuality_test.py` (self-contained). Three modules:

1. **Molecular Hamiltonian builder** (via PySCF integrals + OpenFermion transforms)
   - H2/STO-3G bond 0.735 Å → JW 4q, BK 4q, BK-tapered 2q (`symmetry_conserving_bravyi_kitaev`, O'Malley/Kandala form)
   - HeH+/STO-3G bond 0.9295 Å → JW 4q
   - LiH/STO-3G bond 1.5 Å, occupied=[0], active=[1,2,5] → BK 6q
   - H2O/STO-3G bond 0.9584 Å, angle 104.45°, occupied=[0,1], active=[2..5] → JW 8q

2. **Contextuality classifier (Theorem 3, direct):**
   - Build S = { unique non-identity Pauli strings }
   - Compute T = { P in S : ∃ Q in S with {P,Q}=0 }
   - Search for triple (A, B, C) ⊂ T with [A,B]=[A,C]=0 and {B,C}=0
   - If found: `CONTEXTUAL`, return witness; else `NON-CONTEXTUAL`
   - Commutation via per-qubit non-identity mismatch parity

3. **VQE sanity (2q H2 only):**
   - Dense 4×4 Hamiltonian from Σ coeff·⊗Pauli
   - `numpy.linalg.eigh` for exact diag (compare to PySCF FCI)
   - Ry-Ry-CNOT-Ry-Ry ansatz (4 params); SciPy COBYLA; 5 random seeds × 500 iters; keep best

## 5. Execution

```bash
python3 code/contextuality_test.py
```

Total wall time: ~90 s on CPU. No errors. Wrote:
- `report/evidence/contextuality_results.json` (machine-readable results: |S|, |T|, witness triples, HF/FCI/VQE energies)

## 6. Scoring

For each of the 6 test molecules: read the paper's Table I verdict (contextual / non-contextual), compare to our classifier's output, log agreement, and record the witness triple (for contextual cases).

- 6/6 verdicts match (H2 variants x3 non-contextual; HeH+, LiH, H2O contextual)
- VQE − FCI = 1.6e-10 Ha (chemical accuracy is 1.6e-3, so we're 7 orders below)

## 7. Verdict

**REPLICATED.** Paper's headline algorithmic classifier is correctly implemented and reproduces all six Table I verdicts on real molecular Hamiltonians. See `REPORT.md` §5, `REPORT.tex` §Verdict, and `failure_analysis.md` for the honest caveats (|S| differs from paper's reduced form; CD_0 quantitative values not tested; classical-simulability construction not built).

## 8. Backfill (2026-07-06)

Under the QC-100 8-artifact standard, the following files were added post-hoc without re-running any sims:
- `report/REPORT.tex` — LaTeX version of REPORT.md with honest Critique section + `\input{open_questions_section.tex}`
- `report/open_questions.json` — 5 truly-open questions with basis + concrete next-step probes
- `report/open_questions_section.tex` — LaTeX rendering of the 5 questions
- `report/workflow.md` — this file
- `report/artifacts_summary.md` — artifact index
- `report/failure_analysis.md` — expanded honest critique
- `extraction/nougat.mmd` — extraction stub

The scientific content and verdict are unchanged; only the artifact packaging was upgraded.
