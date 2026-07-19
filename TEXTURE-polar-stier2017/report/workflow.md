# Workflow — Replication of Stier et al. 2017 (arXiv:1701.07256)

**Paper:** "Skyrmion-Antiskyrmion pair creation by in-plane currents."
**Class:** 2D LLG micromagnetics + analytic EOM (theory, tractable in-process).
**Goal:** reproduce (1) Sk-ASk pair with conserved topological charge at
creation, (2) current-driven separation, (3) antiskyrmion decay via Gilbert
damping producing a net change in total topological charge Q.

## 1. Method extraction
- Read `report/method_extract.md` (physics pre-extracted): extended LLG with
  interfacial DMI + Zeeman + Zhang-Li STT; B_eff = -dH/dn; v_s ∝ j_c;
  Berg-Lüscher topological charge; Sk (Q=-1), ASk (Q=+1).

## 2. Solver construction (`code/stier2017_replication.py`)
- Fields: unit magnetization n (3×N×N), N=140.
- Effective field: exchange 2A∇²n + Rohart-Thiaville interfacial DMI +
  Zeeman B ẑ.
- Two integrators:
  - **Precessional RK4** for full LLG+STT (dt=1.5e-3, stiff → small dt).
  - **Dissipative gradient descent** dn = -n×(n×B_eff) dt (unconditionally
    stable) for state preparation and damped annihilation.
- Topological charge: Berg-Lüscher lattice solid angle, **open boundaries**,
  two identically-wound triangles per plaquette.

## 3. Validation (before any physics)
- Uniform state → Q = 0 (exact).
- Isolated skyrmion / antiskyrmion → Q = ±1 (exact integer, no distributed
  noise) after fixing the Q-code (see failure_analysis.md).
- Relaxed skyrmion in the film is smooth (nearest-neighbour gradient ~0.003)
  and DMI-stable at D=0.75, B=0.25.

## 4. Experiments
- **EXP-A (separation):** clean Sk+ASk pair (Q=0), in-plane current →
  measure partner motion and transverse (skyrmion-Hall) deflection.
- **EXP-B (creation-conservation + annihilation → ΔQ):** Sk (Q=-1) + small
  ASk (Q=+1), total Q=0; damped evolution → ASk annihilates, Sk survives →
  Q: 0 → -1 (net ΔQ = -1).

## 5. Scoring & artifacts
- Incremental `work/results.json` (claims: expectation/reproduced/note,
  verdict_metrics, full Q(t)/region traces).
- Figures: `figs/expB_Q_trace.png`, `figs/expB_topo_snapshots.png`,
  `figs/expA_separation.png`.
- Report: `report/REPORT.tex` → `REPORT.pdf`.
- Meta: `META.json` (status + verdict).

## Runtime
- Single CPU process, numpy/scipy only. Full run ≈ 25 s. No paid APIs, no GPU.

## Reproduce
```bash
cd TEXTURE-polar-stier2017
python3 code/stier2017_replication.py        # writes work/results.json + figs/
cd report && pdflatex REPORT.tex && pdflatex REPORT.tex
```
