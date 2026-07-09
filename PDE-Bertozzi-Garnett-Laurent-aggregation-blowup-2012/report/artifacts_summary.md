# Artifacts summary — Bertozzi, Garnett & Laurent (2012) replication

Paper: arXiv:1204.1095v1 · SIAM J. Math. Anal. 2012 · DOI 10.1137/11081986X.
Directory: `~/Dropbox/REPLICATE-PROJECT/PDE-Bertozzi-Garnett-Laurent-aggregation-blowup-2012/`

## Reports (`report/`)
- **REPORT.md** — canonical human-readable replication report (source of truth for all other files here). Sections: paper summary, claims table (C1–C6), method (7 numbered steps), results vs paper, judge verdicts, scope/limitations, verdict.
- **REPORT.tex** — LaTeX version of the above, with an added dedicated **Genuine Critique** section (§5) that records scope limitations, shared assumptions across the "three independent" methods, tautological aspects of the 10^(−16) rel-err rows, and honest interpretation of the multi-judge concordance.
- **open_questions.json** — 5 genuinely open questions grounded in the paper's aggregation-equation blow-up dynamics (non-Newtonian regime, non-monotone data stress-tests, sharp regularity threshold for the shock-time formula, universality of ρ_t = ρ² beyond uniform-ball, existence of other reducible exponents).
- **workflow.md** — step-by-step methodology.
- **artifacts_summary.md** — this file.
- **failure_analysis.md** — the one substantive numerical slip (np.gradient on non-uniform z-grid) plus categorised known limitations.

## Code (`code/` — from-scratch numpy, no library PDE solver)
- **aggregation_newtonian.py** — main solver module.
  - `run_uniform_ball` → C4 simultaneous-collapse via closed-form shell ODE (Method A).
  - `run_particles` → C2/C4 via N=1500 particle RK4 Lagrangian sim (Method B).
  - `run_burgers_uniform` → C1 Burgers characteristics on uniform z-grid (Method C).
  - `run_density_blowup` → C5 measurement of (dρ/dt)/ρ².
- **check_ordering.py**, **check_ordering_fine.py** — particle-shell ordering diagnostics for C2 across Δt = 4×10^(−4) → 5×10^(−5).
- **c3_shock_time.py** — clean uniform-z-grid characteristics solve; formula t_shock = 1/(d · sup_z m'_init(z)) vs observed first blow-up for Gaussian and parabolic-cap initial data, d = 2, 3.
- **judge.py** — three-model Argo assessor (gpt-5.2, gemini-2.5-pro, gpt-4.1); free endpoints only.

## Evidence (`evidence/`)
- **aggregation_results.json** — C4 table: t*_theory vs shell-time mean vs 20-shell spread for d = 2, 3, 4 (spread at machine ε ~ 10^(−16)–10^(−17)). Also particle-sim mean collapse times.
- **c3_shock_time.json** — C3 table: (data, d, t_shock formula, t_shock observed, rel err) for gaussian×{2,3} and parabola×{2,3}; rel errs 10^(−9)–10^(−16).
- **ordering_check.json** — C2 monotonicity: worst ordering disorder = 0 exactly for shells with r > 0.05 (d = 2); origin-boundary residual stable across Δt (confirms physical shock, not numerical artefact).
- **judge_verdicts.json** — three-judge REPLICATED verdicts with per-claim breakdown.

## External inputs
- **arXiv PDF** (1204.1095v1) + LaTeX source — canonical mathematical reference. Publisher HTML mirrors (SIAM/T&F/MDPI) Cloudflare-blocked but not needed for a math paper.
- **No authors' code** — none exists (analysis paper).
- **No proprietary data** — pure PDE / analytical replication.

## Compute footprint
- Host: CherryRd (local).
- Stack: numpy 2.4.3, scipy 1.18.0 (scipy present but not used for dynamics).
- Runtime: seconds per script (pure numpy on CPU, no GPU).
- Cost: **$0.00** (all judge calls via free Argo proxy; opus deliberately avoided).

## Traceability
Every number quoted in REPORT.md / REPORT.tex is regenerable from a single script in `code/` writing a single JSON in `evidence/`. The C4 → C1 → C3 → C5 → C2 chain corresponds one-to-one with the seven-step method list in `workflow.md`.
