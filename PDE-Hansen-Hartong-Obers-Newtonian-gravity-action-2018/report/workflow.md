# Workflow — Hansen, Hartong & Obers 2018 replication

Paper: arXiv:1807.04765, PRL 122, 061106 (2019). Fully analytical / no numerical work.
Compute host: **uicgpu** (single-thread SymPy 1.13.3, free ANL compute).
LLM endpoints: **Argo proxy** `http://127.0.0.1:44497` (free: `argo:gpt-5`, `argo:claude-opus-4.6`).
Total elapsed: ~10 minutes end-to-end.

---

## Stage 0 — Acquisition
1. Fetch paper on uicgpu:
   ```bash
   mkdir -p ~/replicate/hansen-newtonian-2018 && cd $_
   curl -sSL -o paper.pdf https://arxiv.org/pdf/1807.04765v2
   md5sum paper.pdf   # 15ce60ac1e1db7a0889275cb6b9a5220
   pdftotext -layout paper.pdf paper.txt   # 46265 B, 422 lines
   ```
2. Confirm key equations legible in `paper.txt` — the algebra table (eq. 11),
   the connection (eq. 2), the Newtonian limit (eq. 6/7), the action (eq. 12).

## Stage 1 — Claim enumeration
Read paper end-to-end and enumerate 14 discrete claims into a claims table
(see REPORT.md §2). Classify each as `algebraic identity`, `commutator value`,
`metric compatibility`, `direct component computation`, or `heavy derivation`.
Flag which are testable within a single-wave-slot budget.

## Stage 2 — Symbolic verification

### 2a. Algebra & Jacobi (`work/verify_algebra.py`)
- Build structure constants for the type-II algebra from paper eq. (11) using an
  auto-antisymmetrising `add()` helper (register each bracket once).
- Exhaustive Jacobi scan over every C(N,3) triple.
- Runs at d=2 (12 gens, 220 triples), d=3 (20 gens, 1140), d=4 (30 gens, 4060).
- Additional checks: `[N, G_a] = T_a` non-zero; `[G_a, G_b] = -S_{ab}` non-zero;
  ideal ⟨T,B,S⟩ closes; quotient reproduces Bargmann.
- Full stdout → `report/evidence/algebra_output.txt`.

### 2b. Metric compatibility (`work/verify_metric_compat.py`)
- Generic TTNC background: lapse `A(x^μ)` arbitrary function of all coords, `m_μ(x^μ)`
  generic, `h^{ij} = δ^{ij}`. **No** closed-τ assumption.
- Compute Γ̄ from eq. (2) symbolically, then evaluate:
  - `∇̄_μ τ_ν = ∂_μ τ_ν − Γ̄^λ_{μν} τ_λ`
  - `∇̄_μ h^{νρ} = ∂_μ h^{νρ} + Γ̄^ν_{μλ} h^{λρ} + Γ̄^ρ_{μλ} h^{νλ}`
  - Torsion `Γ̄^λ_{[μν]}` vs. paper's `−v̂^λ ∂_{[μ} τ_{ν]}`.
- d=2: 0/9, 0/27, 0/9 failures. d=3: 0/16, 0/64, 0/24 failures.
- Full stdout → `report/evidence/metric_compat_output.txt`.

### 2c. Newtonian-limit reduction (`work/verify_poisson_reduction.py`)
- Flat NC background: `τ_μ = δ_μ^0`, `h^{μν} = diag(0, I_d)`, `m_μ = Φ(t,x⃗) δ_μ^0`
  with Φ arbitrary SymPy function.
- Compute Γ̄, then Ricci.
- Verify: only non-zero Γ̄ is `Γ̄^{x_i}_{tt} = ∂_i Φ`; only non-zero Ricci is
  `Ricci_{tt} = ∇²Φ`.
- Substitute into paper's eq. (6) projected on (t,t) → paper's eq. (7):
  `∇²Φ = 8πG (d-2)/(d-1) ρ`.
- Verified at d=2, 3, 4.
- Full stdout → `report/evidence/poisson_output.txt`.

## Stage 3 — LLM judging
- Compose neutral prompt with all script outputs summarised without cherry-picking
  → `report/evidence/judge_prompt.txt`.
- Query both judges via Argo proxy (free):
  - `argo:gpt-5`     → REPLICATED, 70% coverage, very-high confidence.
  - `argo:claude-opus-4.6` → REPLICATED, 62% coverage, very-high confidence.
- JSON replies → `report/evidence/judge_response_gpt5.json`,
  `report/evidence/judge_response_argo_claude-opus-46.json`.
- Both estimates flag the SAME untested items independently flagged by the
  human replicator (C4, C5, C6): confirms honest reporting.

## Stage 4 — Reporting
- Author REPORT.md (~14 KB): summary, claims table, method, results vs. paper,
  caveats, compute audit, verdict.
- Author REPORT.tex with additional "Genuine critique" section.
- Compute totals: ~5,600 symbolic assertions, 0 failures.

## Stage 5 — Backfill artifacts (this task)
Files added post-hoc without re-running any analysis:
- `REPORT.tex` — LaTeX version of REPORT.md + dedicated Genuine Critique section.
- `open_questions.json` — 5 truly open research questions grounded in the paper.
- `workflow.md` — this file.
- `artifacts_summary.md` — inventory of produced artefacts.
- `failure_analysis.md` — what went wrong in the middle, and how it was resolved.

---

## Endpoint / compute audit rules obeyed
- All heavy compute on **uicgpu** (free ANL compute).
- All LLM calls via **Argo proxy** (free `argo:gpt-5`, `argo:claude-opus-4.6`).
- Zero paid direct-API calls (`pdf` tool routed to Anthropic direct and returned
  "credit balance too low" — verified no chargeable call landed).
- Zero fabricated numbers: every result is raw stdout of a SymPy script.
