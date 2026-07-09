# Attempt Log

Chronological.

1. Read WAVE_BRIEF_2026-07-01.md and PDE_NEXT50 priority list; listed existing PDE-replications/ for structure and dedup.
2. Candidate selection: skipped the 9 already-done tonight. Considered top OA repro-ok items. First tried Mohamed unsteady-Burgers (T&F, rank 47) and Savović FD-vs-PINN (MDPI, rank 26): BOTH publishers Cloudflare/403-blocked to curl AND to uicgpu-proxied curl AND web_fetch. Pivoted to an arXiv-hosted paper for clean OA access.
3. Chose Bertozzi–Garnett–Laurent (rank 48, arXiv:1204.1095, "Characterization of radially symmetric finite time blowup in multidimensional aggregation equations"). Dedup: no existing *Bertozzi*/*aggregation*/*blowup* dir. Created target dir PDE-Bertozzi-Garnett-Laurent-aggregation-blowup-2012/.
4. Fetched arXiv PDF (436 KB) + LaTeX source (BGL-revised.tex, 2519 lines). pdftotext -layout → bgl.txt.
5. Read the paper. It is primarily an analysis paper; identified Section 4 (Newtonian kernel α=2−d) as the concrete/testable core with computable reference numbers.
6. Derived the reduction myself: radial field v(r)=−m(r)/r^{d-1}, m(r)=∫₀^r s^{d-1}ρ ds (eq 4.2); mass eq m_t+v m_r=0 (4.3) → Newtonian → m_t − m m_r/r^{d-1}=0; z=r^d → inviscid Burgers m_t − m m_z = 0 (eq 4.4). Worked out that uniform ball ⇒ shell collapse time r0^d/(d m0) is r0-INDEPENDENT ⇒ simultaneous collapse.
7. Wrote aggregation_newtonian.py (numpy only): (A) exact Lagrangian shell ODE r^d=r0^d−d m0 t; (B) direct N-particle radial sim (no shell-conservation assumed); (C) Burgers-by-characteristics; plus density-blowup and gaussian shock-time tests. First write hit a path-resolution bug (workspace `..` resolved to nonexistent ~/.openclaw/Dropbox); rewrote to absolute Dropbox path.
8. Ran it: C4 shell-collapse spread ~1e-16 (simultaneous, machine zero) for d=2,3,4, t*=R0^d/d exact; C1 Burgers t_shock matches shell ODE exactly; C5 (dρ/dt)/ρ² median = 1.00000 (stable) ⇒ ρ_t=ρ²; C2 particle sim ordering flagged False.
9. Investigated C2 "ordering False": check_ordering.py + check_ordering2.py showed far-field (r>0.05) disorder = 0.00 EXACTLY (d=2); residual is confined to the simultaneous-collapse pileup at the origin and does NOT vanish with dt ⇒ it is the physical shock-at-origin, exactly the paper's claim, not a scheme error.
10. Multi-judge (judge.py) via free Argo: gpt-5.2, gemini-2.5-pro, gpt-4.1. All three → REPLICATED. gpt-5.2 flagged C3 as only a formula spot-check (no direct observed-vs-predicted comparison on non-uniform data).
11. Tightened C3 (c3_shock_time.py): independent z-Burgers characteristics solve for monotone gaussian + parabolic cap. Predicted t_shock=1/(d sup m'_init) vs OBSERVED first-blowup/origin-reach time: rel_err 1e-9 to 1e-16 (d=2,3). Confirmed first interior char-cross time == origin-reach time ⇒ shock forms exactly at origin for monotone data. (This also corrected a spurious d=3 gaussian mismatch in step 8 caused by np.gradient on a non-uniform z-grid.)
12. Wrote report artifacts.
