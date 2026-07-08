# Workflow — Grover on SIMON replication

## Paper
- arXiv 2004.10686 (Anand, Maitra, Mukhopadhyay, 2020)
- Target: reduced-SIMON (n=3, k=6, T=4) Grover key-search demo (paper Section 3.3, Figures 11 + 14).

## Stages

1. **Read + parse.** Read v2 PDF from arXiv; extract Section 3.3 spec (round function, key schedule, round constants), Fig. 11 classical test vector, Fig. 14a/b Grover histograms.
2. **Environment.** Create `.venv` (Python 3.14.6), install `qiskit==2.5.0`, `qiskit-aer==0.17.2`, `numpy`. Local CPU only (CherryRd). Free tools only.
3. **Classical baseline (C1, C2).**
   - `code/simon_classical.py`: bit-level SIMON round + key-expansion, verify `(L0,R0,k0,k1)=([011],[101],[001],[110]) → (L4,R4)=([011],[111])`.
   - Sanity: encrypt `M=[011101]` under `K=[001110]` → `C=[011111]`.
4. **Classical oracle enumeration (C3, C4).**
   - `code/classical_brute.py`: brute-force all 64 keys; for each `(M,C)` pair record the matching set. Confirm pair 1 → {K, K'}; pair 2 → {K, K''}; intersection = {K}.
5. **Grover oracle construction.**
   - `code/grover_simon.py`: build 20-qubit reversible circuit:
     - `encrypt_inplace(L, R, k0, k1, k2, k3)` = 4 rounds SIMON in place; `k2, k3` derived via reversible key-expansion.
     - Comparator: XOR target `C` into `(L,R)`; MCX onto flag qubit iff all-zero; uncompute XOR.
     - Uncompute encryption; uncompute plaintext load.
     - Multi-controlled X from flag(s) onto `|->` phase kickback qubit.
     - Re-run flag-setting to clear flags.
     - Diffuser: `H⊗6 X⊗6 MCZ X⊗6 H⊗6` on `K`.
6. **Grover runs (C5, C6).**
   - Single-pair: 4 iterations, 20 000 shots → expect two peaks at `K` and `K'`.
   - Two-pair: 6 iterations, 10 000 shots → expect unique peak at `K`.
7. **Scaling scan (C7).**
   - `code/grover_scaling.py`: iterate k = 0..7 on single-pair oracle; compare empirical vs analytic `sin²((2k+1)θ)`.
8. **Report.** Write `report/REPORT.md` + `report/REPORT.tex` + evidence JSONs.

## Ordering constraints
- (1) → (2) → (3, 4 parallel) → (5) → (6, 7 parallel) → (8).

## Compute budget
- Total wall: ~2 min for all simulator runs (each Grover call ≤ 6 s on CPU).
- Zero paid API calls. Zero GPU. Free endpoints only.

## Provenance
- Independent clean-room reimplementation from paper spec.
- Author code NOT consulted.
- Host: CherryRd, macOS 25.3.0, Python 3.14.6, Qiskit 2.5.0.
