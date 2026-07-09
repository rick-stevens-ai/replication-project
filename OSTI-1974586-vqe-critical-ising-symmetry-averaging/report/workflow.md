# Workflow — OSTI 1974586 (Sewell/Bao/Jordan, VQE critical Ising + symmetry averaging)

Deterministic replication pipeline. All steps rerunnable from a clean checkout.

## Environment
- Host: CherryRd (macOS 25.3.0) for orchestration; uicgpu (8×A100) as proxy for the OSTI download only.
- Python 3 / NumPy 2.x / SciPy (CPU; the exactly-solvable core is tiny — no GPU needed).
- pdftotext (poppler) — used on uicgpu because the PDF was fetched there.
- Argo LLM-judge: `argo:gpt-5.2` at `localhost:44497` (free endpoint).

## Stage 0 — provenance
1. Locate OA PDF: `https://www.osti.gov/servlets/purl/1974586`.
2. `curl` from CherryRd → timeout. Fallback: `ssh uicgpu` + `source ~/env.sh` proxy → `curl` succeeds.
3. Record `md5 = 131ff7c062bfb6993df7c222f7aaae49`, filename `1974586.pdf`.
4. `pdftotext -layout 1974586.pdf 1974586.txt` (born-digital → no OCR needed; targeted-OCR fallback never triggered).
5. Extract into `extraction/` (text, figures, tables) and into `work/inputs/` (only the numeric target `-4/pi` and Eq. (3) form — no paper data reused).

## Stage 1 — extract testable claims
Enumerate paper claims into a 7-row table (C1…C7). For each, decide:
- Type: scalar reference / equivalence / convergence / qualitative + threshold / mechanism / full-circuit performance / magnitude.
- Independently testable? (Yes / Partially / No)
- In-scope this run? (Yes for C1–C5; No for C6/C7 — they require the paper's DMERA appendix parameters and matchgate optimization pipeline, out of scope for reference-physics replication.)

## Stage 2 — reference physics (C1, C2, C3)
Script: `work/replicate_tfim.py`.
1. Build single-particle dispersion `eps(k) = 4|sin(k/2)|` for J=h=1.
2. Even-parity ground state → anti-periodic fermion BC → momenta `k = (2m+1)π/L`.
3. Compute `E0 = -0.5 * sum_k eps(k)`; sweep `L in {4, 8, 12, 64, 256, 1024, 2e6}`.
4. Cross-check: for `L in {4, 8, 12}` build the L-qubit spin Hamiltonian (Eq. 3, PBC) via Pauli tensor products and diagonalize with `numpy.linalg.eigvalsh`.
5. Persist to `report/evidence/results.json`: per-L `{E, E/L, err_vs_-4/pi, ff_minus_dense}`.
6. Sanity gates:
   - `abs(E0(2e6)/L + 4/pi) < 1e-12` → pass.
   - `ff_minus_dense < 1e-13` for all L ≤ 12 → pass.
   - `err_vs_-4/pi ~ 1/L^2` (halving L-spacing quadruples reduction) → pass.

## Stage 3 — shallow QAOA scan (C4)
Script: `work/replicate_tfim.py` (same file, second entry point).
1. Build the L=8 (PBC) H_C = -sum XX and H_B = -sum Z as dense 2^L matrices; eigendecompose once.
2. QAOA ansatz `prod_{l=1..p} exp(-i beta_l H_B) exp(-i gamma_l H_C) |0…0>`; energy = `<psi|H|psi>` where `H = H_C + H_B`.
3. Nelder-Mead, 10 random restarts per p, p in {1,2,3,4}. Report min energy.
4. Compare against exact `E_exact = min eigvalsh(H)`.
5. Sanity gates:
   - `rel_err(p=1) ~ 5-6%`, `rel_err(p=2) ~ 2-3%`, `rel_err(p=3) ~ 1-2%` → pass.
   - `rel_err(p=4) < 1e-10` (exact at p = L/2) → pass, matches paper's exact-preparation threshold.

## Stage 4 — symmetry-averaging mechanism (C5)
Script: `work/symmetry_averaging.py`.
1. Model two KW-related error signals `e_A(t) = eps*exp(-t/tau)*cos(t)` and `e_B(t) = eps*exp(-t/tau)*cos(t+π-φ)`.
2. Compute averaged error `e_avg = 0.5*(e_A + e_B)` and its max over t.
3. Verify analytic identity: `max|e_avg| ≈ eps*exp(-t*/tau)*|sin(φ/2)|`.
4. Sweep `φ ∈ {1°, 2°, 5°}`; report orders-of-magnitude suppression = `log10(max|e_A| / max|e_avg|)`.
5. Persist to `report/evidence/symmetry_averaging_results.json`.
6. Sanity gate: `orders_reduced(φ=1°) ~ 2.0-2.2` → pass, matches paper's ~2-orders claim.

## Stage 5 — scoring / judge
1. Assemble judge prompt from REPORT.md + evidence JSONs.
2. POST to `http://localhost:44497/v1/chat/completions` (Argo, model `argo:gpt-5.2`, free).
3. Extract verdict token; persist to `report/evidence/judge_verdict.txt`.
4. Cross-check judge verdict against author's self-assessment (PARTIAL). Concurrence → proceed.

## Stage 6 — report emission
1. Write `report/REPORT.md` (canonical Markdown, this is the source of truth).
2. Emit `report/REPORT.tex` (detailed LaTeX with GENUINE CRITIQUE section).
3. Emit `report/open_questions.json` (5 truly-open follow-ups).
4. Emit `report/workflow.md` (this file).
5. Emit `report/artifacts_summary.md`.
6. Emit `report/failure_analysis.md`.
7. Print `WAVE_RESULT set=... paper=... verdict=PARTIAL dir=... one_line=...`.

## Rerunnability
- No RNG seeds required for C1/C2/C3 (deterministic linear algebra).
- QAOA Nelder-Mead uses seeded restarts (seed set at top of `work/replicate_tfim.py`); rerunning yields identical minima to ≲ 1e-8.
- Symmetry-averaging trig identity is analytic; no seed.
- Judge scoring is non-deterministic (LLM temperature > 0); persist raw verdict + do not re-poll.

## Boundary — what this workflow deliberately does NOT do
- Does not build the DMERA matchgate circuit (C6).
- Does not rerun the paper's optimization pipeline.
- Does not attempt hardware execution.
- Does not cross-check against arXiv PDF MD5 (single-source provenance risk logged in failure_analysis.md).
