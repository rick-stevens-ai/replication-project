# Workflow — arXiv:2304.07917 replication

## Environment

- macOS host `m1` (via Openclaw subagent), CPU-only
- Python 3.14.6 in an isolated `--system-site-packages` venv at `work/venv/`
- qiskit 2.5.0, qiskit-aer 0.17.2, numpy 2.4.3, scipy 1.18.0, matplotlib 3.10.8
- Free endpoints only (no paid inference used); no HPC needed for these
  4-qubit (TIM) and 4-qubit (Hubbard) simulations
- Argo Opus 4.7 driving the replication via the OpenClaw / subagent harness

## Steps

1. **Fetch paper.** `curl https://arxiv.org/pdf/2304.07917 -o work/paper.pdf`
   then `pdftotext paper.pdf paper.txt` for grep-friendly access to the
   parameter values.
2. **Set up venv and install qiskit stack** (see Environment above).
3. **Enumerate claims.** Read Section IV of the paper carefully; extract
   claims C1--C6 (see `REPORT.md` §2). Mark C6 out of scope for CPU budget.
4. **Build the 4-site TIM Hamiltonian** in explicit `2^n x 2^n` matrix form:
   `H = J sum_i X_i X_{i+1} + h sum_i Z_i` with periodic BCs at $n = 4$
   (`work/ite_tim.py::build_tim_hamiltonian`). Exact-diagonalise via
   `numpy.linalg.eigh` to get $E_0 = -2.0202968496$.
5. **Implement Trotterised PITE at the statevector-with-post-selection
   level.** For each Pauli-string term `c_k * sigma_k`, apply
   `exp(-c_k dtau sigma_k) = cosh(c_k dtau) I - sinh(c_k dtau) sigma_k`
   (exact since `sigma^2 = I`), renormalise, and log the per-gadget success
   probability as `||unnormalised||^2 / alpha^2` with
   `alpha^2 = exp(2 |c_k| dtau)` (paper Eq. 26).
6. **Cross-check** the Trotter propagator against `scipy.linalg.expm(-beta H)`
   applied to the same initial state (`work/cross_check_expm.py`); assert
   state overlap > 0.999 across the swept range of $\beta$ before proceeding.
7. **Run the 4-site TIM experiment**: `J=0.5, h=0.1, dtau=0.1`, 45 Trotter
   steps, initial `|+>^{tensor 4}`. Emit
   `ite_tim_result.json`, `ite_tim_history.csv`, `ite_tim_summary.json`.
8. **Build the 2-site Hubbard model.** Use explicit JW annihilation/creation
   matrices on 4 qubits; decompose into Pauli strings by inner product with
   the full 4-qubit Pauli basis. Half-filled `(n_up, n_down) = (1, 1)` sector,
   singlet initial state `(|0110> - |1001>) / sqrt(2)`. Use **open boundary
   conditions** (inferred from paper's reported $E_0 \approx -0.156$; PBC on
   two sites doubles hopping and gives $-0.353$, ruled out).
9. **Run the 2-site Hubbard experiment**: `t=-0.1, U=0.1, dtau=0.1`, 60
   Trotter steps. Emit `ite_hubbard_result.json`.
10. **Attempt full ancilla-circuit reconstruction** in Qiskit
    (`work/qiskit_gadget_verify.py`, `work/qiskit_full_ite.py`): CNOT ladder
    + `Rx(phi)` + measurement + reset per Pauli term. Post-select on ancilla
    `|0>` outcomes; check system-state fidelity against the target
    non-unitary operator. Achieved fidelity $\gtrsim 0.999$; success-probability
    convention has a residual factor-of-two ambiguity we did not fully unwind
    (documented in §5.3 of `REPORT.md`).
11. **Generate plots.** `work/make_plots.py` produces `fig7_tim.png` and
    `fig8_hubbard.png`, mirroring the three-panel layout of the paper.
12. **Copy artefacts** into `report/evidence/`.

## Reproducibility

To rerun the numeric results from a fresh clone:

```
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2304.07917-non-unitary-trotter-ite/work
python3 -m venv --system-site-packages venv
./venv/bin/pip install --quiet qiskit qiskit-aer matplotlib
./venv/bin/python ite_tim.py           # 4-site TIM (Fig 7)
./venv/bin/python ite_hubbard.py       # 2-site Hubbard (Fig 8)
./venv/bin/python cross_check_expm.py  # sanity check vs scipy.expm
./venv/bin/python make_plots.py        # regenerate plots
```

All scripts are deterministic (no RNG usage in the statevector code path).

## What was **not** done

- No noise-model simulation.
- No paper-reported 100 000-shot ancilla-outcome resampling loop
  (we compute exact expectation values instead).
- No baseline comparison against measurement-based QITE (McArdle et al.)
  or against VQE.
- No two-qubit-gate-count / depth accounting.
- Larger-system (3-site, 4-site) Hubbard claim (C6) untested (out of CPU
  budget).
- Only the specific Hamiltonians and parameters from Figs 7 & 8 tested;
  no parameter sweep in $J/h$, $t/U$, or $\Delta\tau$.
