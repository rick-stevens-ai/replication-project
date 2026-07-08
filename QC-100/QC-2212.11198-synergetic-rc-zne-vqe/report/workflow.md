# Workflow — QC-2212.11198 (Synergetic RC + ZNE for VQE)

## 1. Paper acquisition
- Fetched `arXiv:2212.11198` PDF into `work/2212.11198.pdf`.
- Ran `pdftotext -layout` → `work/2212.11198.txt` for grep-friendly reading.
- Identified the headline claim: RC+ZNE gives super-additive error suppression
  vs. RC-only, ZNE-only, or raw noisy VQE on H₂/LiH with coherent 2q-gate noise.

## 2. Reproduction plan
- **Chose the smallest instance that exercises the headline:** H₂/STO-3G
  parity-tapered to 2 qubits (O'Malley 2016 coefficients), deep hardware-efficient
  ansatz (6 CX / 13 params) — enough CX depth for coherent noise to accumulate.
- **Decided on 4-way sweep** (raw / RC-only / ZNE-only / RC+ZNE) at 4 noise
  strengths (ε = 0.02, 0.05, 0.08, 0.10 rad) to test C1 + C2 + C3 + C4
  simultaneously in one pass.
- Deferred: LiH (C5), optimizer robustness (C6), finite-shot regime (C7).

## 3. Environment setup
```
python3.12 -m venv .venv
source .venv/bin/activate
pip install qiskit qiskit-aer 'mitiq>=0.30' numpy scipy ply
# Locked: qiskit==2.5.0, qiskit_aer==0.17.2, mitiq==1.0.0, python==3.12.13
```

## 4. Implementation (`code/vqe_rc_zne.py`)
1. Build H₂ Hamiltonian (5-term Pauli sum) + exact diag → E_FCI = -1.857275 Ha.
2. Build deep HEA ansatz builder `build_ansatz(θ, reps=6)`.
3. Multistart Nelder-Mead (20 restarts) on **noiseless** energy → θ\*
   converges to FCI ≤ 1e-8 Ha.
4. Build noise executor: per-CX inject RX(ε)⊗RX(ε) + RZZ(ε/2) coherent
   over-rotation + 2q depolarizing p=0.002 via AerSimulator density-matrix.
5. Build RC twirl: sample (Pc, Pt) ∈ {I,X,Y,Z}² pre-CX, propagate through CX
   to get (P'c, P't) post-CX + post-noise-block. N_rand = 30 per evaluation.
6. Wire Mitiq `execute_with_zne(clean_ansatz, executor, LinearFactory([1,2,3]),
   scale_noise=fold_global)`.
7. Loop over ε, evaluate all four methods, write JSON + CSV.

## 5. Execution
```
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2212.11198-synergetic-rc-zne-vqe
source .venv/bin/activate
python code/vqe_rc_zne.py     # < 10 s laptop CPU; writes report/evidence/*
python code/llm_judge.py       # Argo multi-judge → report/evidence/llm_judge.txt
```

## 6. LLM-judge verdict
- Submitted the results table + method summary to three Argo judges (free).
- `argo:gpt-4.1` → REPLICATED / high confidence.
- `argo:gemini-2.5-pro` → REPLICATED / high confidence.
- `argo:claude-opus-4.7` → 502 upstream; NOT retried (two-judge consensus
  already sufficient).

## 7. Verdict
**REPLICATED** — see `REPORT.md` §6 for full justification and `REPORT.tex`
§4–5 for critique of what was and was NOT independently verified.

## 8. Backfill (2026-07-06)
- Read existing `report/REPORT.md`.
- Wrote 7 additional artifacts (this backfill wave): `REPORT.tex`,
  `open_questions.json` (5 items), `open_questions_section.tex`, `workflow.md`,
  `artifacts_summary.md`, `failure_analysis.md`, `extraction/nougat.mmd` stub.
- No re-simulation. All existing files preserved.
- Free endpoints only (no paid API calls).
