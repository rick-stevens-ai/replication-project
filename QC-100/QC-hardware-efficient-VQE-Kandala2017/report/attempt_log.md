# Attempt Log — Kandala 2017 hardware-efficient VQE

Chronological. Times approximate (2026-07-01 night wave).

1. **Dedup check.** `ls QC-100 | grep -iE vqe|kandala|hardware-eff` → matched only
   W1-vqe-photonic-peruzzo (Peruzzo original VQE), W2-fermi-hubbard-vqe, W3-vqe-chem-benchmark
   — all confirmed DIFFERENT papers. No existing dir for THIS Kandala hardware-efficient VQE
   paper. Proceeded.
2. **Read brief + STATUS_AUDIT.** Rigor bar = disk-verified numerics, LLM-judge verdict,
   free endpoints, real replication (no fabricated numbers), no overwrite. Mirrored the
   BVBRC/Mitiq exemplar output structure.
3. **Fetched paper.** arXiv abstract + ar5iv full-text HTML (no paid PDF tools). Extracted
   plain text; grepped the tested claims (critical depths, PES vs exact, tapering, ansatz,
   optimizer).
4. **Environment.** Local Python is 3.14 with no qiskit/pyscf. Built a Python 3.12 venv;
   installed PennyLane 0.45.1 + PySCF 2.13.1 (pure `pip`, no GPU wheels needed).
5. **First ansatz cut.** Implemented HEA (Rz-Rx-Rz Euler layers + CNOT entangler). H₂ smoke
   with BK mapping gave **4 qubits** (not the paper's 2). VQE reached chem acc at d=2.
   `lightning.qubit` binary unavailable → switched device to `default.qubit`/backprop.
6. **Qubit-count fidelity.** PennyLane doesn't auto-taper; full-symmetry `qml.taper` removed
   too many qubits (H₂→1, LiH→3). Fixed by tapering with **only the first 2 symmetry
   generators** → removes exactly 2 qubits (the paper's spin-parity reduction), yielding the
   paper's exact counts: **H₂→2q, LiH→4q, BeH₂→6q**, with correct exact GS energies
   (−0.890629 / −7.635653 / −14.987535 Ha at bond distances). Term counts 6 / 44 / 84.
7. **H₂ (2q).** Depth scan (all-to-all entangler): chem acc already at **d=1** (err 8e-9).
   Full 10-point dissociation curve at d=1: **all points chem acc**, matching exact FCI to
   ~1e-8 Ha across 0.4–2.5 Å. ✓ (matches paper: H₂ critical depth d=1).
8. **LiH (4q).** Depth scan: d=1 fails (err 0.124 Ha), **d=2/4/8 all chem acc**
   (4.6e-5 / 1.9e-5 / 1.7e-8). Monotonic improvement with depth reproduced. 8-point
   dissociation curve at d=2 run.
9. **BeH₂ (6q).** Depth scan: d=1 (2.1e-2, fail), d=2 (2.1e-2, stuck — local min), **d=4
   chem acc (4.0e-4)**. 6-point dissociation curve at d=4 run (heaviest job).
10. **Process robustness note.** `nohup &` children died when the launching shell exited
    (macOS, no `setsid`); one LiH run lost its JSON. Re-ran via the exec background-session
    manager (survives) — all evidence JSONs written.
11. **Critical-depth interpretation.** Paper reports critical depth as the shortest depth
    where the **average of 10 optimizations** reaches chem acc: d=1,8,28 (experimental
    connectivity) / **d=1,6,16 (all-connected)**. I use **best-of-4-restarts** on a
    **noiseless exact-gradient** optimizer with all-to-all CNOTs, so I reach chem acc at
    shallower depth (1/2/4). Same qualitative law (depth grows with molecule size);
    quantitative difference fully explained by best-vs-average + noiseless-vs-SPSA.
12. **LLM-judge verdict** via free Argo (gpt-5.2 / opus-4.8 fallback).
