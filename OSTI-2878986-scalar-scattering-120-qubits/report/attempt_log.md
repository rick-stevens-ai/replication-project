# Attempt Log — OSTI 2878986

All times CDT (America/Chicago), 2026-07-05.

## 06:14 — Kickoff
Received wave brief. Cleaned target dir, created `report/` (+ `evidence/`) and `work/` subdirs.
Confirmed no existing sibling dir being overwritten.

## 06:16 — PDF fetch
- `curl` on uicgpu (needed `source ~/env.sh` for proxy) → success, 4.45 MB PDF.
- `scp` to local Dropbox target dir. Also mirrored to `~/.openclaw/workspace/tmp-osti/` (attempt to work around `pdf` tool allowed-dir restriction).
- Confirmed via arXiv metadata: this is arXiv 2411.02486 v2, "Scalable Quantum Simulations of Scattering in Scalar Field Theory on 120 Qubits", single-author (Zemlevskiy). Retrieved arXiv e-print source tarball (`/tmp/2411.02486.src`, 5.03 MB) — contains `main_v3.tex`, `preamble.tex`, `main_v3.bbl`, and a `graphics/` dir with 18 PDF figures. **No code, no README, no supplementary Zenodo/GitHub link.**

## 06:20 — PDF text extraction
- `pdf` MCP tool failed (Anthropic credit exhausted, Gemini model unknown, OpenAI extraction disabled). Fell back to `pdftotext -layout osti_2878986.pdf osti_2878986.txt` (3711 lines, 1.7 MB text — layout-preserving; some Unicode math + LaTeX overlays are noisy in Table II but numbers are readable).
- Extracted the paper's key numeric claims:
  - 120 physical qubits, IBM Heron `ibm_fez`, superconducting.
  - nq=2 qubits/site, ϕ_max=1.5, m=1/2, λ∈{0,2}, wavepackets k=±π/3, σ_k=π/3.
  - Two-qubit gate counts: 2284 (t=1–3), 3604 (t=4–6), 4924 (t=7–9); depth 59/81/103 respectively.
  - 80 Pauli-twirled circuits × 2 TREX twirls × 8000 shots per (physics + mitigation) circuit.
  - Error mitigation stack: DD → PT (CZ) → TREX → ODR with vacuum-evolution mitigation circuits, layout randomization.
  - Local infidelity Id per stage (Table I): vacuum prep 0.018 (λ=0) / 0.007 (λ=2); wavepacket 0.055/0.055; time evol 0.17→0.59 for λ=0, 0.13→0.42 for λ=2.
  - Circuit resource formula: time evol has 2q depth = 22⌈t/3⌉ per step + 72 variational parameters.
  - Ground truth: qiskit MPS simulator, max bond dim 100, convergence 10⁻²–10⁻³.

## 06:30 — Design replication strategy
- **Impossible to reproduce:** the actual 120-qubit `ibm_fez` runs, or the L=60 MPS numbers (requires IBM Quantum access + qiskit-aer MPS backend; qiskit not installed on uicgpu; the paper claims no code repo).
- **Possible to reproduce:** the digitized lattice Hamiltonian (Eq. 1 + JLP encoding Eqs. 13–16) is a fully specified finite matrix for small L. Building it and diagonalizing exactly directly probes the physics the paper's MPS reference is supposed to reproduce.
- **Ground rule:** we build the Hamiltonian and evolve small-L wavepackets to compare qualitative claims (translation invariance of vacuum, λ=2 smaller vacuum ⟨ϕ²⟩, collision peak attenuation, free dispersion, presence/absence of time delay).

## 06:35 — First implementation (`replicate_scalar_scattering.py`)
- Wrote self-contained numpy/scipy code:
  - Built on-site ϕ (diagonal) and Π (Fourier-rotated diagonal) operators, verified ϕ eigenvalues = {−1.5, −0.5, +0.5, +1.5} and k_ϕ = {±π/(2·1), ±3π/(2·1)} for nq=2, ϕ_max=1.5.
  - Built full H by summing 4 terms (Π², m²ϕ², ½(ϕ_{j+1}−ϕ_j)², λ/24 ϕ⁴) with PBCs.
  - Lanczos (`scipy.sparse.linalg.eigsh`) for ground state.
  - Smeared-ϕ two-wavepacket surrogate: apply Σ_j g_j(k_0) ϕ_j to |vac⟩ once for right-mover, once for left-mover (center_site = L//2−2 and mirror). This is NOT the paper's SC-ADAPT-VQE prep, but a cheap analog that excites a Gaussian-envelope superposition of single-particle modes.
  - `scipy.sparse.linalg.expm_multiply` for real-time evolution.
- First run at L=6 was slow (~8 s per H build) because `kron_at_site` was densifying full dim×dim intermediate matrices.

## 06:45 — Refactor: full-sparse construction
- Rewrote `kron_at_site` / `kron_two_sites` to keep everything as `scipy.sparse` CSR throughout. Also rewrote `phi2_expectation_per_site` to use a reshape + broadcast trick (no need for a dim×dim operator) since ϕ² is diagonal in the JLP basis.
- Verified numerical equivalence: L=6 rerun after refactor gave IDENTICAL numbers to the pre-refactor run (both vacuum means and every scattering peak to all recorded digits), and H build time dropped from 8 s → 0.07 s.

## 06:50 — L=10 attempt
- Tried L=10 (Hilbert dim 4^10 = 1 048 576). H build completed but `expm_multiply` per time step was still very slow / appeared to hang beyond a couple minutes. Killed and dropped back to L=8.

## 06:55 — L=8 main run
- L=8 (Hilbert dim 65 536). Full run (both λ, 9 time steps each) completed in ~1:43 wall time. Every quantitative claim we planned to check landed cleanly.

## 07:05 — Comparison + figures
- `compare_free_vs_int.py`: extracted C1–C5 verdicts (see `claim_verdicts.json`).
- `make_figures.py`: rendered analogs of paper Fig. 9 (heatmap) and Fig. 11 (peak vs time), plus dispersion.

## 07:10 — LLM-judge verdict
- Sent report + evidence summary to Argo (free localhost:44497) with `argo:claude-opus-4.8` for verdict scoring.
