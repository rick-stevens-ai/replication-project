# Replication Workflow — OSTI 2448207

**Paper:** Fierro, Alibalazadeh, Stephens, Moore. "Massively parallel axisymmetric fluid model for streamer discharges." *Comput. Phys. Commun.* 2024. DOI 10.1016/j.cpc.2024.109345. SAND2024-12794J.
**Wave:** OSTI-100 top-up (efficient budget, <25 min wall, free endpoints only, no proprietary data / no paid tools).
**Host:** CherryRd (Python 3.14, numpy 2.4.3, scipy 1.18.0).

---

## Pipeline

```
[OSTI PDF fetch (via uicgpu proxy)]
        │
        ▼
[pdftotext -layout → 830-line text]
        │
        ├──► [analytic_checks.py]        → evidence/analytic_checks.json     (C1–C4)
        │
        ├──► [mms_order.py]              → evidence/mms_order_result.json    (C5)
        │       (reimplement paper's exact face fluxes; sweep nz=64..4096)
        │
        ├──► [streamer1d_convergence.py] → (unstable, recorded honestly)     (C6/C8 attempt)
        │    [streamer1d_stable.py]
        │
        └──► [judge.py]                  → evidence/llm_judge.json           (Argo gpt-5.2)
                                                        │
                                                        ▼
                                                  [REPORT.md]
```

## Steps

### 1. Environment prep
- Host: CherryRd. Python 3.14 stdlib + numpy 2.4.3 + scipy 1.18.0.
- No paid endpoints, no proprietary data.
- Verify CherryRd → osti.gov is blocked (it is); route PDF fetch via `ssh uicgpu`.

### 2. Artifact acquisition
- On uicgpu: `curl -sL https://www.osti.gov/servlets/purl/2448207 -o /tmp/2448207.pdf`.
- Size: 1.99 MB. MD5: `41204e9adef92fa85c980f66c0d8d39f`.
- `scp` back to CherryRd; `pdftotext -layout /tmp/2448207.pdf -` → 830 lines of extracted text.

### 3. Claims extraction
- Human read + grep of extracted text; enumerate the paper's testable claims.
- Populate a 9-row claims ledger (C1–C9); tag each with type (arithmetic / analytic / CFL / MMS / full-sim / HPC scaling) and testability under the efficient/free-only budget.
- Verdict-relevant conclusion: C1–C5 tractable within budget; C6–C9 need the full HPC run and proprietary CWI reference.

### 4. Analytic self-consistency (C1–C4)
- Script: `work/analytic_checks.py`.
- Verify domain reconstructions, Courant linearity in Δt, benchmark CFL magnitude, and six element-count products against paper-stated scalars.
- Output: `evidence/analytic_checks.json`.

### 5. Method-of-manufactured-solutions order test (C5)
- Script: `work/mms_order.py`.
- Reimplement paper's exact face treatment:
  - 1st-order upwind advective face flux (eq. 18–21).
  - 2nd-order central diffusive face flux (eq. 23–26).
- Assemble as discrete flux-divergence operator `L[n] = d/dz(v·n − D·dn/dz)`.
- Manufactured solution: `n(z) = exp(sin(2πz/L))`; periodic BCs to isolate scheme order.
- Sweep nz ∈ {64, 128, 256, 512, 1024, 2048, 4096}; measure L∞ and L2 error vs. analytic `L[n]`.
- Fit observed order `p = slope(log err, log Δh)`.
- Output: `evidence/mms_order_result.json` → **p = 0.995 (L∞), 0.997 (L2)**.

### 6. Coupled nonlinear 1-D toy attempt (C6/C8)
- Scripts: `work/streamer1d_convergence.py`, `work/streamer1d_stable.py`.
- 1-D axial drift-diffusion + tridiagonal Poisson + local-field ionization; upwind vs Koren.
- **Result: unstable at fine Δh (explicit-source blow-up).** Recorded honestly as failed secondary check; no numbers used as evidence, no fabrication.

### 7. LLM-judge synthesis
- Script: `work/judge.py`.
- Free Argo `argo:gpt-5.2` at `localhost:44497`.
- Feed the evidence artifacts + claims ledger; ask for claim coverage %, agreement level, and overall verdict.
- Output: `evidence/llm_judge.json` → coverage 60%, moderate agreement, verdict PARTIAL.

### 8. Verdict + report
- Human synthesis of analytic checks + MMS + LLM-judge → `report/REPORT.md`.
- Verdict: **PARTIAL** (core method + all analytic claims reproduced; full-simulation outputs out of reach).
- Backfilled artifacts (this file, REPORT.tex, open_questions.json, artifacts_summary.md, failure_analysis.md).

## Ground rules honored
- No fabricated numbers; failed surrogate is not evidence.
- Free endpoints only (Argo gpt-5.2 for judge, no paid models).
- No proprietary data (CWI reference curves not acquired → C6–C7 explicitly unreproduced).
- Efficient budget respected (no cluster runs → C9 unreproduced).
- CherryRd network limitations respected (osti.gov via uicgpu proxy).
