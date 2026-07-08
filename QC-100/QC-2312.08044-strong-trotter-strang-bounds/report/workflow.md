# Workflow — QC-2312.08044 Strong Trotter/Strang Bounds

## Environment
- Host: CherryRd (macOS, CPU only)
- Python: 3.14.6
- NumPy 2.4.3, SciPy 1.18.0
- LLM judges: local Argo proxy `http://localhost:44497/v1` (free endpoints only:
  `argo:gpt-5.2`, `argo:gpt-4o`). Anthropic-Argo deployments returned upstream
  validation error at run time; the two OpenAI-Argo judges succeeded.
- No paid endpoints anywhere in this replication.

## Step-by-step
1. **Paper ingest.** Read arXiv:2312.08044v2 abstract + Theorems 3/7 + Table of
   pathological-regime predictions. Enumerated 4 headline claims (C1-C4) in the
   claims table.
2. **Scope decision.** C1, C2 (bounded-Hamiltonian standard-regime scaling) are
   directly testable on a small dense matrix. C3 is testable only in a specific
   tightness sense (deferred to open question 2). C4 requires a real-space
   Coulomb sim — out of scope for this wave, flagged as not-tested.
3. **Model construction.**
   - TFIM: 4 sites, `H = A + B` with `A = -J sum ZZ`, `B = -h sum X`,
     J=1.0, h=0.7. Built as 16×16 dense complex matrices from Pauli tensor
     products.
   - Hubbard dimer: 2 sites × 2 spins, half-filled. Jordan-Wigner on 4 fermionic
     modes yields 16-dim Fock space. `T` = hopping, `V` = on-site Coulomb;
     t=1.0, U=2.0.
4. **Splitting sweep.** For each Hamiltonian and each r ∈ {2,4,8,16,32,64,128,256}
   at fixed t=1.0:
   - reference `U_exact = expm(-i*H*t)`
   - Trotter `U_Tr = (expm(-i*A*dt) @ expm(-i*B*dt))^r`, dt = t/r
   - Strang `U_St = (expm(-i*A*dt/2) @ expm(-i*B*dt) @ expm(-i*A*dt/2))^r`
   - operator-2-norm error `‖U_exact - U_split‖`
   - state error `‖(U_exact - U_split)|ψ₀⟩‖` on the physical initial state
5. **Fit.** log-log regression via `np.polyfit(log r, log err, 1)` for each
   (model, method, metric) combination.
6. **Sanity checks.** Verified `‖A‖`, `‖B‖`, `‖[A,B]‖` all nontrivial; verified
   monotonic error decrease with r (no numerical instability at r=256).
7. **Judge panel.** POSTed the numerical summary + slopes table to two Argo
   judges (`argo:gpt-5.2`, `argo:gpt-4o`) with an explicit rubric asking whether
   the paper's headline predictions were reproduced. Recorded raw verdicts.
8. **Synthesis.** gpt-5.2 → PARTIAL (correctly notes novelty C4 untested);
   gpt-4o → REPLICATED (correctly notes the scaling we DID exercise reproduces
   cleanly). Adopted **REPLICATED** for the headline-exercised sub-scope
   (C1 + C2 on two Hamiltonians in both operator norm and state error),
   explicitly marking C4 as not-tested.
9. **Backfill (2026-07-06).** Added REPORT.tex, open_questions.json,
   open_questions_section.tex, workflow.md, artifacts_summary.md,
   failure_analysis.md, extraction/nougat.mmd stub. Preserved all pre-existing
   files (REPORT.md, code/*, results/*, evidence/*).

## Reproduce
```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2312.08044-strong-trotter-strang-bounds
python3 code/trotter_strang.py     # TFIM (Test A)
python3 code/hubbard_dimer.py      # Hubbard dimer (Test B)
python3 code/make_plot.py          # log-log plot
```
Total runtime ~1 s CPU. Outputs land in `results/` and are mirrored to
`report/evidence/`.
