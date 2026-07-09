# Workflow — Sato et al. 2021 VQA-Poisson Replication

Chronological, exact steps taken to independently replicate the paper's central
quantitative claims (Fig. 3(b) and Fig. 4).

## 0. Scope & policy

- Target: Sato, Kondo, Koide, Takamatsu, Imoto, *Variational quantum algorithm
  based on the minimum potential energy for solving the Poisson equation*,
  Phys. Rev. A **104**, 052409 (2021); arXiv:2106.09333; DOI
  10.1103/PhysRevA.104.052409.
- Set: PDE (rank 14 in the replication project queue).
- Endpoints: free only (Argo Opus 4.7 for LLM judge).
- Compute: CherryRd, single-thread numpy statevector; no GPU / uicgpu / HPC needed.

## 1. Paper acquisition

```
curl -o work/sato_2021.pdf https://arxiv.org/pdf/2106.09333
pdftotext -layout work/sato_2021.pdf work/sato_2021.txt
```

Recorded size: 785,930 bytes. Extraction used as a searchable reference for
equation numbers and figure captions.

## 2. Reference-code survey (not depended on)

```
git clone https://github.com/ToyotaCRDL/VQAPoisson work/VQAPoisson
```

- License: Apache-2.0.
- Interface confirms Ry+CNOT-ladder ansatz, Hadamard-test cost, BFGS optimizer.
- Dependency wall: pins Qiskit 0.23 and the retired `qiskit-aqua` package —
  not viable on a modern environment.
- **Decision:** do NOT run the reference harness. Reimplement from scratch in
  NumPy so that (a) we have a working execution, and (b) the replication is a
  genuine independent implementation of the paper's math rather than a rerun of
  the authors' bundled harness.

## 3. Independent implementation

File: `work/vqa_poisson_replicate.py`. Pure NumPy statevector.

- Ansatz `U(theta) = ((Ry^n)(CNOT ladder))^L (Ry^n)`, `L = 5`, so
  `nparams = (L+1)*n`.
- Poisson matrix `A`:
  - Dirichlet: `tridiag([-1, 2, -1])`.
  - Periodic: same tridiagonal with corner wrap terms; ε-regularized on the
    zero-eigenvalue nullspace.
  - Neumann: not implemented in this pass.
- Right-hand side `|f>` built explicitly as the +1/√N / −1/√N step function
  per paper Eq. (45), equivalent to `H^n · (X ⊗ I^{n-1})`.
- Cost `E_h(theta) = -0.5 * <f|psi>^2 / <psi|A|psi>` per Eq. (14).
  For real ansatz + real |f> this is the Hadamard-test estimand exactly.
- Norm recovery `r = 1 / sqrt(<psi|A^2|psi>)` per Eq. (48).
- Metrics:
  - `eps_tr = sqrt(1 - |<psi|u_hat>|^2)` per Eq. (46).
  - Norm recovery per Eq. (48).
  - `rel_L2 = ||u_q - u_exact|| / ||u_exact||`.

## 4. Optimization protocol

```
scipy.optimize.minimize(
    fun=E_h, x0=theta0, method="L-BFGS-B",
    options={"gtol": 1e-7, "ftol": 1e-10, "maxiter": 2000}
)
```

- `theta0` sampled uniformly from `[0, 4π]` per paper Sec. IV.B.2.
- Seeds: `1000*n + k` for k = 0..9 (10 trials per n, deterministic).
- Reference solve: `numpy.linalg.solve(A, f)`.

## 5. Experiment matrix

| BC        | n values      | trials/n | ansatz L |
|-----------|---------------|----------|----------|
| Dirichlet | 2, 3, 4, 5    | 10       | 5        |
| Periodic  | 5             | 5        | 5        |
| Neumann   | — (skipped)   | —        | —        |

Total optimizations: 45.

## 6. Execution

```
cd work && . .venv/bin/activate && python vqa_poisson_replicate.py
```

- Wall time: ~90 s (single thread, CherryRd).
- All 40 Dirichlet trials converged (L-BFGS-B success flag).
- All 5 periodic trials converged.
- Per-trial iteration counts written to `report/evidence/results_*.json`.

## 7. Automated adjudication

- Judge model: `argo:claude-opus-4.7` (free endpoint per project policy).
- Prompt fed with: paper claims table (C1..C8), results table, protocol summary,
  and honest scope statement (C6, C7 partially/not tested).
- Judge output stored at `report/evidence/judge_response.json`.
- Verdict returned: **REPLICATED**, matching the human-adjudicated call.

## 8. Report writing

- `report/REPORT.md` written from the results tables + judge rationale.
- `report/REPORT.tex` produced from REPORT.md (this backfill pass) with a
  dedicated Genuine Critique section.
- Evidence files:
  - `report/evidence/results_dirichlet.json` — full 40 trials.
  - `report/evidence/results_periodic.json` — 5 trials.
  - `report/evidence/run_dirichlet.log` — driver stdout.
  - `report/evidence/judge_response.json` — LLM judge JSON output.
- Brief + attempt log + artifact harvest referenced in REPORT.md Sec. 6.

## 9. Not done (deliberate scope cuts, documented)

- Neumann BC (C7 partial).
- n = 6, 7, 8 scaling sweep needed for C6 fit.
- Shot-noise + gate-noise simulation (would test the paper's NISQ-friendliness
  claim).
- Real hardware run (IBM Quantum / Rigetti).
- Head-to-head against Liu 2020 in the same harness (would substantiate the
  measurement-cost advantage empirically).
- Head-to-head against VQLS or HHL for the same Poisson operator.

These are recorded as follow-up items in `open_questions.json`.

## 10. Reproduction from scratch

```
git clone https://github.com/ToyotaCRDL/VQAPoisson  # reference (not run)
python -m venv work/.venv && . work/.venv/bin/activate
pip install numpy scipy
python work/vqa_poisson_replicate.py > report/evidence/run_dirichlet.log 2>&1
```

Everything after that is table generation and the LLM-judge call.
