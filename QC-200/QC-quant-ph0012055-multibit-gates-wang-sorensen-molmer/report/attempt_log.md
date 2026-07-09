# Attempt Log

**All times in America/Chicago, 2026-07-06.**

- **12:10 CDT** — Received subagent task. Read `WAVE_BRIEF_2026-07-01.md`. Created target dir; downloaded `paper.pdf` from arXiv (`https://arxiv.org/pdf/quant-ph/0012055`, 113 kB, 4 pp).
- **12:11 CDT** — `pdftotext -layout paper.pdf extraction/paper_text.txt` → 315 lines of clean prose. Read the whole paper. Identified 8 concrete testable claims (C1–C8 in REPORT.md).
- **12:12 CDT** — Attempted `pdf` tool for equation extraction. Failed: (a) local path not under allowed dir; (b) all image models failed (Anthropic credit exhausted; Gemini model unknown; OpenAI PDF extraction disabled). Fell back to direct reading of `paper_text.txt` — sufficient because the paper is only 4 pages.
- **12:13 CDT** — Created `work/venv/` (Python 3.14), installed `qutip 5.3.0`, `scipy 1.18.0`, `numpy 2.5.1`. Verified imports.
- **12:14 CDT** — Wrote `work/toffoli_eq5.py`: literal Eq. (5) implementation, sweep over K ∈ {1,2,3}, N_ph ∈ {6,12,20}, oscillator state ∈ {ground, Fock-1, coherent(α=1,2)}.
- **12:15 CDT** — First run: F_avg vs Toffoli = **0.9662** for ALL (K, N_ph, osc) with N_ph≥12. Note: F_avg is CONSTANT across all sweeps → not a truncation issue, not an oscillator issue. Systematic gate mismatch.
- **12:16 CDT** — Wrote `work/toffoli_eq5_v2.py`: scan alternate prefactors and tau_scale to test whether a scaling constant is missing. Best fidelity remained 0.9662 at paper's literal parameters.
- **12:17 CDT** — Derived by hand: `(σz1+σz2+1)² = 2(σz1+1)(σz2+1) - 1`. So Eq. (5) generates `exp(-iπ(σz1+σz2+1)²σx3/16)` = Toffoli × `exp(-iπσx3/16)`.
- **12:18 CDT** — Wrote `work/toffoli_eq5_v3.py`: compare simulated propagator vs three targets: (a) literal `exp(-iπ(σz1+σz2+1)²σx3/16)`, (b) Toffoli, (c) Toffoli × correction. Result: (a) and (c) both give F=1.0000 across the whole sweep; (b) gives 0.9662. Confirmed.
- **12:19 CDT** — Wrote `work/toffoli_eq5_v4.py`: typo hypothesis test. Replaced `+Iq/(32K)` with `-sx3/(32K)` in Eq. (5). Result: F vs pure Toffoli = 1.0000 across K=1..3. Hypothesis self-consistent.
- **12:20 CDT** — Wrote `work/eq6_and_grover.py`: Fourier identity (nc=1..5, all errors < 10⁻¹⁵); UG (n=1..5, initially "failed" for n=1 due to global-sign issue → fixed by comparing to ±UG_target). Ran Grover for n=2..5, all inputs.
- **12:21 CDT** — Initial Grover runs all MISSED (amplifying complement). Wrote `work/grover_debug.py`; realized paper's σz convention is opposite of QuTiP default (paper: |0⟩=σz=−1; QuTiP: |0⟩=σz=+1). Fixed `Z2 = -sigmaz()`. Re-ran: all Grover targets HIT at optimal k.
- **12:22 CDT** — Wrote `work/grover_trajectory.py`: sweep k=0..8 for n=3..6, x0=all-ones. All P(x₀) values match analytical `sin²((2k+1)arcsin(1/√N))` to 10⁻⁶.
- **12:23 CDT** — Wrote `work/cnot_multibit.py` + `work/cnot_action_fid.py`: Cⁿ-NOT via direct exponential and via Eq. (6) product form for nc=1..6. Process fidelity < 1 (as paper says: "up to phase factors"), but permutation fidelity = 1.0000 in every case. Full 3-qubit Toffoli truth table exact.
- **12:24 CDT** — Wrote `work/ghz_states.py`: verify Jy² building block. GHZ fidelity 1.0000 for N=2,4,6 at χt=π/2; low for odd N (expected).
- **12:25 CDT** — Wrote report files: REPORT.md, REPORT.tex, workflow.md, artifacts_summary.md, failure_analysis.md, open_questions.json, brief.md, attempt_log.md, artifact_harvest.md. Copied `extraction/marker.md`, `extraction/nougat.mmd` from sibling directory (per brief's "pull from central corpus if parsed").
- **12:26 CDT** — Ran LLM-judge verdict pass via Argo Opus 4.7. See `evidence/llm_judge.txt`.
- **12:27 CDT** — Emitted final WAVE_RESULT line.

## What worked

- QuTiP `sesolve` handles the truncated-Fock + qubit tensor product cleanly at moderate sizes.
- The Sørensen-Mølmer decoupling machinery reproduces exactly as advertised.
- Grover via the paper's Uf + UG is textbook-perfect once conventions are fixed.
- Cⁿ-NOT via Eq. (6) product form scales cleanly up to 7 qubits.

## What did not work / took extra debug

- The `pdf` analysis tool was unavailable (all providers failed); had to fall back to raw text.
- σz convention mismatch cost about 3 minutes to diagnose.
- Eq. (5) constant term is either a typo or a documentation convention I don't share. Took ~5 minutes to isolate and confirm the correction.

## Compute footprint

- Local CPU only, single-threaded QuTiP.
- Peak memory well under 500 MB.
- Total elapsed simulation time: <30 seconds cumulative across all runs.
- No `ssh uicgpu` needed.
