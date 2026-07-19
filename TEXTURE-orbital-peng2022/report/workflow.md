# Workflow — peng2022 SOAM single-particle replication

**Paper:** Peng & Jiang, *Spin-orbital-angular-momentum-coupled quantum gases*, arXiv:2209.07051 (review/perspective).
**Texture class:** orbital (atomic OAM ↔ spin). **Method class:** theory (analytic + model-Hamiltonian; single-particle diagonalization).
**Host:** CherryRd (macOS, CPU-only). No GPU, no external data, no paid APIs.

## Steps performed

1. **Read existing extraction.** `extraction/marker.md` (2912 lines, clean pdftotext of the full review) and `report/method_extract.md`. Confirmed the paper is a review; the replicable core is the **single-particle SOAM Hamiltonian** (Eqs. 15–17) and its **dispersion / degeneracy claims** (Sec. III.A, Figs. 2–3). Interacting GPE (C2 of the review) and experiments (C4) are out of scope for a <5 min CPU replication; single-particle physics (chosen replication target) is fully tractable.

2. **Identified 3 computationally reproducible headline claims:**
   - **C1** — At Ω_R = 0 the spectrum is a spinor 2D harmonic oscillator; ground state has QAM l_z = ±1, doubly degenerate; excitation interval ℏω.
   - **C2** — At δ = 0, the ground state is doubly degenerate at l_z = ±1 for weak coupling and jumps to a single l_z = 0 state at strong coupling (first-order, contrasted with continuous SLM case).
   - **C3** — Time-reversal symmetry at δ = 0 makes the spectrum symmetric about l_z = 0, E(l_z)=E(−l_z); detuning δ≠0 breaks T and lifts the ±1 degeneracy.

3. **Built a self-contained solver** `code/peng2022_replication.py` (numpy + scipy only):
   - Works in the QAM frame [Eq. 17]. For each integer QAM l_z, the two spin components feel spin-dependent centrifugal barriers with effective angular momenta (l_z − n) and (l_z + n), coupled by the radial Rabi term Ω(r) = Ω_R (r/w)^p e^{−2r²/w²}.
   - Radial coordinate discretized on a cell-centered finite-difference grid (NR = 600, R_max = 8 a_ho) with a **symmetrized Hermitian** FD form of (1/r) d/dr(r d/dr) to avoid the r = 0 singularity.
   - Assembles the 2·NR × 2·NR real-symmetric Hamiltonian per l_z; diagonalized with `scipy.linalg.eigh` (lowest 3 eigenvalues via `subset_by_index`).
   - Parameters: l_+ = −2, l_− = 0 ⇒ n = −1; δ = 0 for C1/C2; harmonic units ℏ = m = ω = 1.

4. **Ran the code** (`python3 code/peng2022_replication.py`, ~30 s wall on CherryRd). Results written to `work/results.json`. Two figures written to `figs/` (`fig2_dispersion.png` = Fig. 2 replica; `fig3b_lowest_band.png` = Fig. 3(b) replica).

5. **Validated against analytic HO limit** (Ω_R = 0): lowest energies match (|l_eff|+1)·ℏω to < 1e-4; degenerate l_z = ±1 ground state at E = 1 ℏω confirmed.

6. **Honest normalization audit.** Scanned waist w and coupling Ω_R (scratch scripts in /tmp). Found the ±1→0 transition at Ω_R ≈ 8.5 in our HO units vs the paper's window (between 100 and 250). The peak of the Rabi profile is w-independent, so the mismatch is an **unpublished-normalization gap** (paper does not give w or the E_recoil/ℏω ratio), not a physics error. Documented in `normalization_note` in results.json and in `failure_analysis.md`.

7. **Wrote all 8 artifacts** (see `artifacts_summary.md`), including the report (`REPORT.tex` → attempted `pdflatex`), 5 open questions, this workflow, and the failure analysis; updated `META.json`.

## Tools / codes used
- Python 3 (numpy 2.4.3, scipy, matplotlib/Agg) — the entire replication.
- `scipy.linalg.eigh` — dense symmetric eigensolver.
- pdflatex (TeX Live) if available — report compilation.
- No external datasets, no network, no GPU, no paid model APIs.

## Effort estimate
- Reading + claim identification: ~15 min.
- Solver design + implementation (correct Hermitian radial FD, spin-dependent centrifugal terms): ~40 min including a units/normalization debugging pass.
- Runs + figure generation: ~2 min compute.
- Artifact authoring (report, questions, analyses): ~30 min.
- **Total: ~1.5 h agent time; <1 min pure CPU compute per run.**
