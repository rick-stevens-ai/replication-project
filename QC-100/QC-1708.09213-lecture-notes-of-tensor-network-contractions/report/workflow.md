# Workflow — QC-1708.09213 (Ran et al., Lecture Notes of Tensor Network Contractions)

## Pipeline actually executed

```
arXiv:1708.09213v4 (PDF)
        │
        ▼
    read + summarize monograph structure
        │           │
        │           ▼
        │      pick 4 load-bearing claims (C1..C4)
        │           │
        ▼           ▼
  set up env    author 6 experiment scripts (work/exp*.py)
  (venv,        │
   quimb 1.14,  │
   numba, np)   │
        │      run scripts on laptop CPU
        │           │
        ▼           ▼
   cross-checks:  raw stdout logs (work/*.log or captured)
     ED (N<=12)       │
     Pfeuty FF        ▼
     analytic -4/π  numerical tables (energies, entropies, truncation errors)
        │           │
        └───────┬───┘
                ▼
        evidence JSON → LLM judge (Argo gpt-5, free)
                │
                ▼
         per-claim + overall verdict
                │
                ▼
         REPORT.md (top of dir)
                │
                ▼
      REPORT.tex + open_questions.* + artifacts_summary.md + failure_analysis.md
      + extraction/nougat.mmd stub  ← THIS BACKFILL
```

## Steps in order

1. Fetched arXiv:1708.09213v4 PDF; identified 4 replicable claims (DMRG energy, entanglement scaling → c=1/2, MPS canonicalization/optimal truncation, iTEBD ground-state convergence).
2. Set up `work/.venv` on macOS/CPU with `quimb 1.14.0`, `numba 0.62.1`, `numpy`, `scipy`.
3. Wrote a Pauli-convention Hamiltonian and an explicit Pfeuty-formula reference (`exp1_dmrg_tfim_energy.py`, `exp1b_check_ed_small.py`) — this pinned the spin convention against ED and FF simultaneously.
4. Ran DMRG for N=20, 40, 60, 80 at χ=32 → 1/N extrapolation of e0.
5. Ran DMRG for N=32, 64, 128 at χ=64 → measured block entropies at every bond → fit slope × log(chord) → c.
6. ED entropy (`exp2c`) for N=10..16 as a small cross-check on the fit method.
7. Verified MPS canonicalization + optimal truncation on random and DMRG states (`exp3`).
8. Ran second-order iTEBD (imaginary time) on N=64, χ=32 for T=8, dτ=0.05 → per-site energy vs FF (`exp4`).
9. Assembled evidence JSON; sent to Argo `argo:gpt-5` via `llm_judge.py` (free endpoint at `localhost:44497`); recorded structured verdict.
10. Wrote `REPORT.md` with numeric tables, judge JSON, and verdict.
11. **(This backfill, 2026-07-06)** Added: LaTeX rendering (`REPORT.tex`), machine-readable open questions (`open_questions.json` + `open_questions_section.tex`), workflow/artifact/failure narratives, and Nougat extraction stub — no simulations re-run, no numbers changed.

## Compute + endpoint hygiene

- All numerics on laptop CPU (Darwin 25.3.0 x86_64), single-node, single-thread-friendly.
- LLM judge on Argo (free, `argo:gpt-5`) — no paid endpoints touched.
- No paywalled data; every reference value is either analytic or computed here from a Pauli-convention Hamiltonian.
