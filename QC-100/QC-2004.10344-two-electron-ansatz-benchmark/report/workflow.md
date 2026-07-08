# Workflow — arXiv:2004.10344 replication

**Paper:** Smart & Mazziotti, *Efficient Two-Electron Ansatz for Benchmarking Quantum Chemistry on a Quantum Computer*, arXiv:2004.10344 (Phys Rev A 103, 012420, 2021).

**Wave:** QC-100. **Verdict:** REPLICATED. **Headline exercised:** yes (H2/STO-3G noise-free curve, 18 points; two independent code paths; parameter/CNOT baseline vs UCCSD).

## Environment

- Host: CherryRd (macOS, Darwin 25.3.0).
- Python 3.13, fresh venv.
- Deps: `pyscf==2.13.1`, `openfermion==1.7.1`, `openfermionpyscf==0.5`, `qiskit==2.5.0`, `numpy`, `scipy`, `matplotlib`.
- No GPU, no cloud, no hardware access. All statevector on CPU.
- Free-endpoint policy: obeyed (no paid API, no IBM Quantum runtime charges).

## Steps in order

1. **Ingest paper.** `wget https://arxiv.org/pdf/2004.10344` → `work/paper.pdf`; `pdftotext -layout` → `work/paper.txt`. Read for identifiable claims → six-item claims table in REPORT.md §2.

2. **Isolate testable core.** C1 (ansatz spans FCI, noise-free), C3 (CNOT count),
   C6 (parameter count) — all three are classical / statevector reproducible.
   C4 (hardware curve) and C5 (symmetry verification) require retired IBM
   devices — declared out of scope up front.

3. **Build Hamiltonian pipeline.** For each R ∈ 18 bond lengths (0.30 → 3.00 Å):
   - `openfermion.MolecularData` + `run_pyscf(run_scf=True, run_fci=True)` →
     MO Hamiltonian + FCI reference.
   - `get_fermion_operator → jordan_wigner → get_sparse_operator(n_qubits=4)`
     → 16×16 sparse H.

4. **Build compact ansatz.**
   `T = a†₂a†₃a₁a₀ - a†₀a†₁a₃a₂` (antihermitian double-excitation, JW-mapped).
   `|ψ(θ)⟩ = expm_multiply(θ·T_sparse, |HF⟩)` with `|HF⟩ = |0011⟩`.

5. **VQE optimisation.** BFGS from 9 starts in `[-π, π]` (defensive multi-start
   for a single-parameter landscape — global minimum always found).
   Objective: `⟨ψ(θ)|H|ψ(θ)⟩`.

6. **Cross-check via Qiskit.** Build 4-qubit `QuantumCircuit` with HF X-gates +
   `exp(-iθ/2 · Y₀X₁X₂X₃)` CNOT staircase. Evaluate via `Statevector`. Rerun VQE
   at R=0.735 Å; compare to path (4). Agreement to ~10⁻¹² Ha.

7. **UCCSD baseline.** JW-mapped UCCSD/H2/STO-3G: 2 spin-preserving Givens
   singles (2 CNOTs each) + 1 double (same 6-CNOT block) = 3 params, 14 CNOTs.

8. **Gate-count analysis.** `transpile(circuit, basis_gates={cx,u,rz,rx,ry,h,x},
   optimization_level=0)` → count CNOTs and depth for compact vs UCCSD.

9. **Plot.** Matplotlib reproduction of paper's Fig. 1 (HF, FCI, VQE-compact
   overlaid across dissociation). → `results/h2_dissociation_curve.png`.

10. **Verify + assemble report.** REPORT.md written 2026-07-03. Backfill of
    LaTeX version + open questions + workflow + summary + honest failure
    analysis + nougat OCR stub done 2026-07-05.

## Reproduction (single command sequence)

```bash
cd QC-100/QC-2004.10344-two-electron-ansatz-benchmark/
python3 -m venv .venv && source .venv/bin/activate
pip install pyscf==2.13.1 openfermion==1.7.1 openfermionpyscf==0.5 \
            qiskit==2.5.0 numpy scipy matplotlib
python code/vqe_h2_compact.py         # → results/h2_curve.{json,csv}
python code/circuit_gate_counts.py    # → results/gate_counts.json + circuit dumps
python code/plot_curve.py             # → results/h2_dissociation_curve.png
```

Expected walltime: <5 minutes on a modern laptop CPU.

## What was NOT done (deliberate scope cuts)

- **Hardware runs on ibm-5 / ibm-14** — both devices retired; no free-endpoint
  replacement gives the *same* device fidelity profile.
- **H3+ 6-qubit curve** (paper's second headline system) — out of scope,
  compact-ansatz principle already demonstrated on H2.
- **Symmetry verification effect on N-representability metric V** (paper's
  Table I) — requires hardware run to be meaningful.
- **Larger bases (6-31G, cc-pVDZ)** — the paper's minimal-basis STO-3G
  demonstration is what we set out to reproduce.

These are logged in `open_questions.json` / `open_questions_section.tex` as
concrete future probes with next-step designs.

## Provenance

- Replicator: OpenClaw QC-100 wave, backfilled 2026-07-05 by the replication-project system.
- Underlying REPORT.md written 2026-07-03.
- All code, results, and logs preserved in-tree; nothing overwritten.
