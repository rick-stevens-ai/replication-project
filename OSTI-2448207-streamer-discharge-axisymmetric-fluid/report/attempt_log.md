# Attempt Log — OSTI 2448207

Chronological, times CDT 2026‑07‑02.

- **03:45** Read WAVE_BRIEF_2026‑07‑01.md and OSTI100_TOPUP50 priority list. Enumerated already‑done ids + existing OSTI‑* dirs.
- **03:46** Selected rank‑7 candidate **osti 2448207** (applied_math; "Massively parallel axisymmetric fluid model for streamer discharges"): STILL‑UNDONE, OA PDF, strong analytic/convergence validation targets (explicit CFL numbers, element counts, first‑order convergence claim, scheme‑sensitivity claim). Confirmed no colliding dir.
- **03:48** Fetched OA PDF via `ssh uicgpu` proxy → `https://www.osti.gov/servlets/purl/2448207` (1.99 MB, PDF v1.5). CherryRd‑direct avoided per brief. `scp` to work/. `pdftotext -layout` → 830 lines clean text (one harmless "Invalid number of shared object groups" syntax warning).
- **03:49** Read methodology (eqs 1‑52): drift‑diffusion continuity (eq 1‑3), finite‑volume face fluxes (eq 6‑21, 1st‑order upwind), central diffusion (eq 22‑26), forward‑Euler update (eq 27), Poisson central‑difference (eq 30‑37), local‑field source Q=ᾱμ|E|n (eq 51), semi‑implicit time loop (eq 48‑49), RE definitions (eq 50, 52). Extracted quantitative claims.
- **03:47** `analytic_checks.py`: verified Courant‑linear‑in‑dt, benchmark Courant≈0.1, all element‑count products, domain reconstruction. **All pass.** → evidence/analytic_checks.json.
- **03:48** `streamer1d_convergence.py`: first attempt at coupled 1D DD+Poisson streamer with aggressive local‑field fits → **blew up** (inf/NaN in Poisson RHS; positive ionization feedback). Root cause: explicit scheme + unbounded α·μ·|E| source at fine dh needs adaptive CFL + real transport tables. Not used as evidence.
- **03:49** Pivoted to rigorous **MMS order test** (`mms_order.py`): reimplemented the paper's EXACT face treatment (upwind advection + central diffusion, periodic to isolate scheme order), manufactured n(z)=exp(sin), dh sweep 64→4096. Fixed two trivial bugs (numpy‑bool JSON; slope sign). **Result: observed order → 1.000, fitted p=0.995 (Linf)/0.997 (L2).** Confirms paper's linear‑convergence claim. → evidence/mms_order_result.json.
- **03:50‑03:52** `streamer1d_stable.py`: bounded‑transport nonlinear toy solver + Koren‑vs‑upwind velocity comparison. Still unstable at fine dh (peak‑E spike to 9e8 at 5µm) and front tracker returned 0 velocity with the chosen anode‑side seed/params. **Reported as an unsuccessful secondary attempt, not evidence** (honest; the stable run is the paper's HPC computation).
- **03:53** LLM‑judge via free Argo `argo:gpt-5.2` (`judge.py`) → **PARTIAL, coverage 60%, moderate agreement.** → evidence/llm_judge.json.
- **03:54** Wrote report/ (REPORT.md, brief.md, this log, artifact_harvest.md).
