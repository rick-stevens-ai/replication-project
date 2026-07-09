# Workflow: Replicating quant-ph/0012055 (Wang, Sørensen, Mølmer)

## Effort estimate

- **Wall-clock:** ~90 minutes (including debugging convention issues and typo hypothesis).
- **Compute:** local CPU only (`CherryRd`, Darwin 25.3.0 x64, Python 3.14). No GPU needed. No `ssh uicgpu`. Peak memory <500 MB.
- **Manual labor:** ~5 min PDF text extraction + hand-derivation of the algebraic identity that reveals the Eq. (5) mismatch.
- **Model calls:** none beyond the LLM-judge verdict pass (see `evidence/llm_judge.txt`); no expensive API usage.

## Steps in order

1. `curl -sL -o paper.pdf https://arxiv.org/pdf/quant-ph/0012055` — pulled the arXiv v2 PDF (4 pages, 113,185 bytes).
2. `pdftotext -layout paper.pdf extraction/paper_text.txt` — extracted plain text of the paper (~315 lines).
3. Copied the pre-existing sibling directory's `extraction/{marker.md, nougat.mmd}` (of the same paper) into my `extraction/` (per brief: legitimate corpus reuse; sibling dir untouched).
4. Wrote `work/toffoli_eq5.py`: encode Eq. (5) in QuTiP with truncated Fock space, evolve, project onto oscillator state, reduce to qubit block, fidelity vs Toffoli target.
5. Ran sweeps over K, N_ph, oscillator state. Saw a **constant** F=0.966 that is _K- and N_ph- and oscillator-state-independent_ → not truncation, not oscillator entanglement — a systematic gate mismatch.
6. Wrote `work/toffoli_eq5_v2.py`: scan x-prefactor and tau-scale to see if a scaling can hit F=1. Best F was still 0.966 at the paper's literal parameters.
7. Realized the algebra: `(σz1+σz2+1)² = 2(σz1+1)(σz2+1) - 1`. So Eq. (5) literally gives Toffoli × exp(-iπσx3/16).
8. Wrote `work/toffoli_eq5_v3.py`: compare against three candidate targets. Confirmed F_literal = 1.0000, F_Toffoli = 0.9662, F_Toffoli+rot = 1.0000.
9. Wrote `work/toffoli_eq5_v4.py`: test typo hypothesis — replace +1/(32K) with -σx3/(32K). Result: F vs Toffoli = 1.0000 exactly, confirming the typo hypothesis is self-consistent.
10. Wrote `work/eq6_and_grover.py`: verified Eq. (6) Fourier identity (Frobenius diff < 10⁻¹⁵ for nc=1..5); verified Eq. (10) UG = ±((2/N)M − I) for n=1..5; ran full Grover for n=2..5, all inputs, all HIT after fixing the σz-convention issue (paper: |0⟩ = σz=−1 eigenstate; QuTiP default: |0⟩ = σz=+1).
11. Wrote `work/grover_trajectory.py`: sweep k=0..7 for n=3..6, x0=all-ones. All P(x₀) match theory to machine precision.
12. Wrote `work/cnot_multibit.py` + `work/cnot_action_fid.py`: build Cnc-NOT two ways (direct exponential + Eq. 6 product form) for nc=1..6; verify permutation fidelity F_perm = 1.0000; check full 3-qubit Toffoli truth table (all 8 rows correct).
13. Wrote `work/ghz_states.py`: verify GHZ generation via Jy² for N=2..7; confirmed even-N gets F=1.0, odd-N gets low fidelity (known feature of Jy² dynamics, not a paper claim).
14. Wrote all report artifacts (REPORT.md, REPORT.tex, workflow.md, artifacts_summary.md, failure_analysis.md, open_questions.json, brief.md, attempt_log.md, artifact_harvest.md).
15. Ran LLM-judge verdict pass via Argo Opus 4.7 (`localhost:44497`, key=stevens); logged prompt+response into `evidence/llm_judge.txt`.

## Tools and versions

| Tool | Version | Role |
|------|---------|------|
| Python | 3.14 | Runtime |
| QuTiP | 5.3.0 | Statevector evolution (`sesolve`), tensor products, Fock basis |
| NumPy | 2.5.1 | Linear algebra |
| SciPy | 1.18.0 | Matrix exponentials |
| pdftotext (poppler) | system | PDF → text extraction |
| Argo proxy | localhost:44497 | LLM-judge verdict (Opus 4.7, free) |
| curl | system | arXiv PDF download |

## Files produced

Under `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph0012055-multibit-gates-wang-sorensen-molmer/`:

- `paper.pdf` (113,185 bytes) — arXiv source
- `extraction/paper_text.txt` (~32 kB) — pdftotext output
- `extraction/marker.md` (from central corpus)
- `extraction/nougat.mmd` (from central corpus)
- `work/toffoli_eq5.py`, `toffoli_eq5_v2.py`, `toffoli_eq5_v3.py`, `toffoli_eq5_v4.py` — Eq. (5) tests
- `work/eq6_and_grover.py` — Fourier identity + Grover
- `work/grover_trajectory.py` — full Grover trajectory n=3..6
- `work/grover_debug.py` — debug of Uf convention (retained)
- `work/cnot_multibit.py`, `cnot_action_fid.py` — Cⁿ-NOT
- `work/ghz_states.py` — GHZ via Jy²
- `report/evidence/*.json` — machine-readable results (7 files)
- `report/evidence/llm_judge.txt` — LLM-judge verdict record
- `report/REPORT.md`, `report/REPORT.tex`, `report/brief.md`, `report/attempt_log.md`, `report/artifact_harvest.md`, `report/workflow.md`, `report/artifacts_summary.md`, `report/failure_analysis.md`, `report/open_questions.json`
