# Workflow — Quantum Autoencoder Replication

**Paper:** Romero, Olson, Aspuru-Guzik, *Quantum Sci. Technol.* **2**, 045001 (2017). arXiv:1612.02806.
**Replicator:** Ollie (CherryRd), 2026-06-26.
**Set:** QC-100 / W2-quantum-autoencoder.

## Stages

1. **Read + summarize.** Ingest the arXiv PDF; identify the two testable claims:
   (a) training on trash-qubit-$\ket{0}$ fidelity is a valid proxy for
   reconstruction fidelity via the decoder $U^\dagger$; (b) reconstruction
   fidelity is high when latent size $k$ is adequate and degrades under
   over-compression.

2. **Substitution decision.** The paper's headline demo is $H_2$
   ground-state compression at multiple bond lengths, but those input state
   vectors are not deposited. Substituted a controlled 6-state ensemble drawn
   from a fixed 2-D subspace of the 4-qubit Hilbert space; effective rank is
   known exactly so the degradation threshold is predictable.

3. **Encoder implementation.** 4 qubits; hardware-efficient ansatz
   ($R_y+R_z$ per qubit + linear CNOT chain, 3 layers, 24 params). Pure numpy
   + scipy — no qiskit, no cirq, no external state files.

4. **Training.** COBYLA optimizer, 4 random restarts, cost =
   $1 - \langle \text{trash-}\ket{0}\text{ fidelity}\rangle$. Runs are cheap
   (sub-minute per configuration on CherryRd CPU).

5. **Compression sweep.** Trash size swept over $\{1, 2, 3\}$ (latent
   $k \in \{3, 2, 1\}$). For each configuration record training trash-F and
   reconstruction fidelity $F = |\braket{\psi_\text{in}}{\psi_\text{rec}}|^2$
   averaged over the ensemble.

6. **Verification.** Confirm (i) trash-F tracks recon-F (paper's proxy claim)
   and (ii) monotone degradation with more aggressive compression (paper's
   trade-off claim).

7. **Reporting.** Table results, mark substitutions honestly, document the
   $k=1$ optimization-gap deficiency, list truly-open questions.

## Artifacts produced

- `replicate.py` — clean-room encoder + training + sweep.
- `results.json` — recorded fidelities per compression level.
- `REPORT.md` (top-level) — original narrative report.
- `report/REPORT.tex` — LaTeX report with honest critique + `\input` of open questions.
- `report/open_questions.json` — 5 open questions, machine-readable.
- `report/open_questions_section.tex` — LaTeX section, `\input`-ed by REPORT.tex.
- `report/workflow.md` — this file.
- `report/artifacts_summary.md` — inventory.
- `report/failure_analysis.md` — honest deficiency analysis.
- `extraction/nougat.mmd` — stub (paper text not re-OCR'd; arXiv source is authoritative).

## Constraints honored

- Free / local compute only (numpy + scipy on CherryRd CPU).
- No paid endpoints; no re-runs of the simulator during this backfill pass.
- All prior files preserved; top-level `REPORT.md` untouched.
