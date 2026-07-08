# Workflow — QC-2009.04417 Mitiq replication

Full end-to-end procedure used to produce this replication. All steps ran on CherryRd (macOS, Apple Silicon, Python 3.12). All endpoints used are free.

## 0. Paper acquisition

- `curl -L -o work/paper.pdf https://arxiv.org/pdf/2009.04417v4`
- `pdftotext work/paper.pdf work/paper.txt` (for grep on claim statements)
- Cross-check: journal DOI 10.22331/q-2022-08-11-774 (Quantum, CC-BY 4.0).

## 1. Claim extraction

- Manual read of §3 (ZNE), §5 (PEC), §6 (CDR), and Figs. 3, 4.
- Enumerated 8 testable claims (C1–C8) in REPORT.md §2, marking each as software / API / numerical.
- Selected **C3 (ZNE Fig. 3 capability)** and **C5 (CDR §6 capability)** as headline numerical claims to exercise; C7/C8 marked out of scope for the CPU-fast pass.

## 2. Environment build

```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2009.04417-mitiq-error-mitigation
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install mitiq qiskit qiskit-aer ply     # ply needed for cirq.contrib.qasm_import
python -c "import mitiq, qiskit, qiskit_aer, cirq; print(mitiq.__version__, qiskit.__version__, qiskit_aer.__version__, cirq.__version__)"
# Expected: 1.0.0 2.5.0 0.17.2 1.7.0
```

## 3. ZNE replication (code/zne_replicate.py)

For 10 random seeds:
1. Build a depth-8 2-qubit RB-like circuit: 8 layers of (Rz(θ)·Rx(φ)·Rz(ψ) on each qubit, then CX(0,1)), then append the exact inverse. Analytical truth: `⟨00|ρ|00⟩ = 1`.
2. Build a Qiskit-Aer `NoiseModel` with `depolarizing_error(0.01, 1)` on all 1q gates and `depolarizing_error(0.04, 2)` on CX.
3. Executor: `executor_noisy(qc) -> float`, appends `measure_all`, `transpile(optimization_level=0)`, runs `shots=20000` on `AerSimulator(noise_model=nm)`, returns `counts.get('00', 0) / total`.
4. Truth executor: same, but on a noise-free `AerSimulator()`.
5. For each of three factories — `RichardsonFactory([1,2,3])`, `PolyFactory([1,2,3], order=2)`, `LinearFactory([1,2,3])` — call `zne.execute_with_zne(qc, executor_noisy, factory=f, scale_noise=fold_gates_at_random)`.
6. Record `{seed, truth, raw, richardson, poly, linear}` to `report/evidence/zne_results.json`.

Runtime: ~20 s on CherryRd.

## 4. CDR replication (code/cdr_replicate.py)

1. Build a fixed 2-qubit Cirq circuit: `[H(q0), CNOT(q0,q1), Rz(0.5)(q0), Rz(1.2)(q1), CNOT(q0,q1), Rz(0.7)(q0), H(q0)]`. Observable: `Z⊗I` (Z on q0).
2. Executors:
   - `noisy_exec(c)`: apply `cirq.depolarize(p=0.02)` per moment via `c.with_noise(...)`, simulate with `cirq.DensityMatrixSimulator`, take `Tr(ρ · Z⊗I)`.
   - `noiseless_exec(c)`: identical but no noise application.
3. Truth: `noiseless_exec(circuit)`.
4. Mitigated: `mitiq.cdr.execute_with_cdr(circuit, executor=noisy_exec, simulator=noiseless_exec, observable=Z⊗I, num_training_circuits=10, fraction_non_clifford=0.2)`.
5. Record `{truth, raw, cdr}` to `report/evidence/cdr_results.json`.

Runtime: ~30 s.

## 5. Verdict decision

Applied Rick's headline-exercised rule:
- Both C3 (ZNE Fig. 3 capability) and C5 (CDR §6 capability) are the paper's operational headlines.
- Both were exercised on independently-constructed circuits + independent simulators (Qiskit-Aer for ZNE, Cirq DensityMatrixSimulator for CDR).
- All three ZNE variants and CDR beat raw noisy on absolute error.
- ⇒ **REPLICATED.** Not "REPLICATED (strong)" because the exact hardware numbers from Fig. 3/4 were not re-produced (different noise channel, no real QPU access).

## 6. Backfill (2026-07-06)

Added report/REPORT.tex, report/open_questions.json (5 truly-open questions with concrete free-endpoint next_steps), report/open_questions_section.tex, report/workflow.md, report/artifacts_summary.md, report/failure_analysis.md, extraction/nougat.mmd stub. No re-runs of simulations. All original files preserved.

## Free-endpoint compliance

- No paid model calls made during the replication or backfill.
- Only local Python simulators used (no QPU / no cloud runtime).
- Paper obtained from arXiv (free); code obtained from GitHub (free).
