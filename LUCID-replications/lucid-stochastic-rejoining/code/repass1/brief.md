# Brief — REPASS-1 for lucid-stochastic-rejoining

**Target paper:** Li Y, Qian H, Wang Y, Cucinotta FA (2012). *A Stochastic Model of DNA Fragments Rejoining.* PLoS ONE 7(9): e44293.

**Canonical parse used:** Marker (Datalab) hybrid pdftext+surya output at:
`~/Dropbox/REPLICATE-PROJECT/LUCID-replications/_LUCID100_ADMIN/marker_md_uicgpu_20260622/merged/10_1371_journal_pone_0044293/10_1371_journal_pone_0044293.md`
(9 pages, table_of_contents preserved, math equations preserved in LaTeX, figures captured as JPEG side-by-side).

**Prior pass:** First-pass replication 2026-05-28 reached Coverage = 6 of 8 actually-run claims (C1, C2, C4, C5, C6, plus structural C3/C8); see REPORT.md §3.

## Newly enumerated claims from canonical text (this repass)

Going through the Marker text in order, identifying *quantitative* claims that were missed or only structurally argued in pass 1:

- **C9 — Secondary jump at L\*/m.** Paper §"Impact Factors" page 4: *"Interestingly, another jump occurs at L̄ ≈ L\*/2... we may expect a jump occurring at the mean length given at L\*/m for any positive integer m."* Test: sweep mean length finely on [Lm, L\*] and look for a sub-threshold jump near L\*/2 = 22.5 bp.
- **C10 — Closed-form event count for L̄ > L\*.** Paper page 4: *"with initial M_T fragments, the entire rejoining process consists of 2M_T steps of protein recruitment (each fragment needs two proteins) and M_T − 1 steps of fragments rejoining"* ⇒ exactly **3M_T − 1** events total in long-only regime. Test: count event categories per trajectory for long-only init, verify the totals exactly.
- **C11 — 2D monotonicity of T_M(r1, r2).** Paper Fig 3(d): T_M is monotone increasing in *both* r1 (fraction in I2 = (L\*/2, L\*]) and r2 (fraction in I1 = (Lm, L\*/2]). Test: build a coarse 2D grid in (r1, r2) at fixed M_T=40, L_T=2000 bp, compute T_M, check monotonicity on each axis.
- **C12 — Variance/fluctuation discontinuity at L\*.** Paper Fig 2(b): error bars (max - min spread, std) are *much* larger for L̄ ≤ L\* than for L̄ > L\*. First pass only checked mean. Test: compute std and (max-min) of rejoining time per mean length and verify discontinuity at 45 bp.
- **C13 — k3 effect: dose-response and zero-effect-when-long.** Paper Fig 3(b): smaller k3 markedly increases rejoining time when L̄ ≤ L\*, but k3 has *no effect* when L̄ > L\*. First pass dispatched this as "structural" — now run explicitly with k3 ∈ {0.025, 0.05, 0.1, 0.2, 0.4} at L̄ = 30 (short) and L̄ = 80 (long).
- **C7-revisit — Biphasic two-exponential fit of Fig 4 kinetics.** Paper text page 5–6: *"Our kinetic model naturally leads to such a biphasic description where long DNA fragments (≥45 bp) are joined through fast kinetics and short DNA fragments (<45 bp) are joined through slow kinetics."* Test: fit the simulated remaining-fraction curve under high-LET (70/30) to a two-exponential and check that the two time constants differ by an order of magnitude (slow > fast).

## Plan

1. Add `code/repass1/` scripts:
   - `c9_secondary_jump.py` — fine sweep over L̄ ∈ [15, 50] (1-bp resolution), 60 runs each, plot to look for L\*/2 jump.
   - `c10_event_count_check.py` — count recruit/join/release events per trajectory; verify 3M_T-1 for long-only init.
   - `c11_2d_fraction_surface.py` — (r1, r2) coarse 6×6 grid, 60 runs/cell.
   - `c12_variance_check.py` — re-derive std and (max-min) from same Fig 3 length sweep we already ran, also rerun at finer resolution near L\*.
   - `c13_k3_sweep.py` — k3 ∈ {0.025..0.4} at two L̄ regimes.
   - `c7_revisit_biphasic_fit.py` — load existing Fig 4 npz, fit two-exponential to the mean remaining-fraction curve, report (A1,τ1,A2,τ2).
2. Each script: writes results to `results/repass1/`, log to `logs/repass1/`, figure to `figures/repass1/`.
3. Free compute only: CPU NumPy / SciPy on CherryRd.
4. Update `REPORT.md` in-place, preserving pass-1 verdict as a sibling note; add `PARSER_PROVENANCE` line.

## Compute budget

- CPU only. Expected total wallclock ≤ 5 min for all 6 scripts.
- No external data, no paid endpoints.

## Audit-shape adherence

- Brief (this file) → artifact harvest (existing Marker parse + previous npz results) → attempts (per-script runs, real numbers) → REPORT.md with new Coverage/Agreement + 4-tier verdict.
- Every number reported below comes from a runnable script in `code/repass1/`; nothing fabricated.
