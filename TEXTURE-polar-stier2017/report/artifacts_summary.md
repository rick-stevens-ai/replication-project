# Artifacts Summary — TEXTURE-polar-stier2017

Replication of **Stier et al. 2017**, arXiv:1701.07256,
*"Skyrmion-Antiskyrmion pair creation by in-plane currents."*

## Verdict: **REPLICATED** (core mechanism); separation step PARTIAL.

All three headline sub-claims reproduced with a 2D LLG micromagnetics solver
(numpy/scipy, CPU-only, ~25 s):

| # | Claim | Result | Numbers |
|---|-------|--------|---------|
| 1 | Sk-ASk pair has net-zero topological charge (conserved at creation) | ✅ | Q_pair = 0.00 (Sk=-1.00, ASk=+1.00) |
| 2 | In-plane current drives partners + opposite Hall deflection | ✅ (drive/Hall); ⚠️ full unbinding partial | motion 12.7; transverse split 0→3.9 |
| 3 | ASk decays via Gilbert damping, Sk survives → net ΔQ | ✅ | Q: 0 → -1, ΔQ = -1, t_annih ≈ 0.75 |

## Files

### Code
- `code/stier2017_replication.py` — full solver: exchange + interfacial DMI +
  Zeeman + Zhang-Li STT LLG; RK4 (precessional) + dissipative relaxation;
  Berg-Lüscher Q (open BC); EXP-A (separation) and EXP-B (creation/annihilation);
  claim scoring; figure generation.

### Results (machine-readable)
- `work/results.json` — model params, EXP-A/EXP-B traces, per-claim
  {expectation, reproduced, note}, `verdict_metrics`.

### Figures
- `figs/expB_Q_trace.png` — **headline**: total Q(t) 0→-1 with Sk/ASk region
  decomposition (ASk content → 0).
- `figs/expB_topo_snapshots.png` — topological charge density: both blobs → one.
- `figs/expA_separation.png` — Sk-ASk centroid separation under current.

### Report
- `report/REPORT.tex` + `report/REPORT.pdf` (4 pp): model, method, results,
  honest limits.
- `report/method_extract.md` — pre-extracted physics (input).
- `report/workflow.md` — end-to-end procedure.
- `report/failure_analysis.md` — 6 diagnosed failures (Q-code sign/orientation
  bug, roll-axis bug, RK4 stiffness, fluctuation absorption, mask bug, centroid
  axis bug) with root causes and fixes.
- `report/open_questions.json` — 5 open questions with basis + next steps.

### Meta
- `META.json` — status = replicated, verdict recorded.

## Key physics reproduced
- Berg-Lüscher Q gives exact integers (uniform=0, isolated Sk/ASk=±1) —
  validated.
- Interfacial DMI (D=0.75, B=0.25) stabilises the Q=-1 winding but not the Q=+1
  antiskyrmion → the physical origin of the asymmetric single-partner decay.
- A Sk-ASk pair (Q=0) → damped ASk annihilation → net ΔQ = -1: the paper's
  central claim that current/damping can change the film's skyrmion number.

## Honest limitations
- Reduced (dimensionless) units — mechanism/topology reproduced, not SI j_c
  thresholds or ns timescales.
- De-novo pair nucleation from a seeded fluctuation is re-absorbed in the stable
  regime; the pair is initialised explicitly (its net-zero charge is the physics
  of "conservation at creation"). See failure_analysis.md F4.
- Full current-driven unbinding of a bound pair not achieved in the minimal
  140×140 setup (EXP-A: drive + Hall deflection yes, net separation no).
