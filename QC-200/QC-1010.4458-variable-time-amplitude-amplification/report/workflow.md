# Replication Workflow — arXiv:1010.4458 (Ambainis 2010, VTAA)

## Overview

Task: independent replication of the *core mechanism* of variable-time
amplitude amplification (VTAA), the tool introduced by Ambainis to improve
HHL linear-systems complexity from O(κ² log N) to O(κ log³ κ log N).

Verdict target: **PARTIAL** — the full VTAA-improved HHL is a research-scale
engineering effort. We reproduce the *scaling claim at the heart of the paper*:
that standard amplitude amplification costs O(T_max / √p_succ) while VTAA
costs O(T_max log T_max + T_av · log^{1.5} T_max / √p_succ), and that this
gap grows unboundedly in κ when the stopping-time distribution is
geometrically-concentrated (the paper's HHL regime).

## Time budget

- Read + pdftotext + brief skim: 4 min.
- Design toy Statevector encoding of Ambainis's model: 15 min.
- First run: T_av too large (regime mis-modeled) → iterate: 10 min.
- Correct regime, re-run, verify exponents: 5 min.
- Extraction (surrogate marker.md + nougat.mmd): 8 min.
- Plotting + write-up + REPORT.tex: 25 min.
- Total wall time: ~65 min.

## Tools and versions

| Tool | Version | How used |
|---|---|---|
| Python | 3.13.0 (system) | driver |
| Qiskit | 2.5.0 (fresh venv install via pip) | Statevector, QuantumCircuit, initialize |
| qiskit-aer | latest at 2026-07-05 (installed alongside) | not directly used (Statevector path) |
| numpy | via pip | probability vectors, exponent fits |
| matplotlib | via pip | log-log scaling plot |
| pdftotext (poppler) | system | PDF → work/paper.txt |
| curl | system | arXiv PDF fetch |
| LLM (Argo Opus 4.7) | Argo localhost:44497 key=stevens | model reasoning through the paper (free endpoint) |

## Reproduction steps (exact commands used)

```bash
# 1. Set up target dir
mkdir -p ~/Dropbox/REPLICATE-PROJECT/QC-200/QC-1010.4458-variable-time-amplitude-amplification/{work,extraction,report/evidence}
cd ~/Dropbox/REPLICATE-PROJECT/QC-200/QC-1010.4458-variable-time-amplitude-amplification

# 2. Fetch paper
curl -sL -o paper.pdf https://arxiv.org/pdf/1010.4458
pdftotext paper.pdf work/paper.txt

# 3. Install Qiskit into an isolated venv (Rick's free-tools policy)
python3 -m venv work/venv
source work/venv/bin/activate
pip install --quiet qiskit qiskit-aer numpy scipy matplotlib

# 4. Standard AA sanity check (Grover on N=16, one marked item)
python report/evidence/aa_standard.py
# --> report/evidence/standard_aa_result.json

# 5. VTAA core scaling experiment (kappa in {4,8,...,8192}, two regimes)
python report/evidence/vtaa_core.py
# --> report/evidence/vtaa_core_result.json (HHL regime),
#     report/evidence/vtaa_core_result_toy.json (toy regime),
#     report/evidence/vtaa_core_combined.json,
#     report/evidence/standard_vs_vtaa_curve.csv,
#     report/evidence/standard_vs_vtaa_curve_toy.csv

# 6. Plot the scaling curves
python report/evidence/make_plot.py
# --> report/evidence/vtaa_vs_standard.png

# 7. Write extractions (surrogate marker.md + nougat.mmd — no marker/nougat installed)
#    (produced by hand from work/paper.txt with LaTeX equation rendering)

# 8. Write REPORT.tex, open_questions.json, artifacts_summary.md, failure_analysis.md
```

## Numerical results summary

**Standard amplitude amplification (Grover, N=16, single marked item):**
- Qiskit statevector amplitude on the marked item at k iterations matches
  the analytic formula sin²((2k+1)θ), θ = arcsin(√(1/16)), to ~1e-15
  agreement over k=0..14.
- First iteration count reaching P(marked)≥0.9: **k=2** (P=0.9084).
- Optimal iteration: k=3 (P=0.9613). Theory: (π/4)√N = π ≈ 3.14.
- Oracle-query count for near-certain success ~ O(√N) = 4, consistent with
  Ambainis's O(T_max/√p_succ) with T_max=1, p_succ=1/16.

**VTAA core scaling (Qiskit statevector; doubling schedule t_i = 2^(i+1), i=0..m-1; m = ⌈log₂ κ⌉):**

*Toy regime (p_succ ~ O(1))*: standard AA scales as κ^{1.00}, VTAA as
κ^{1.15}. VTAA is *worse* here because the log T_max prefactor of Theorem 1
is > 1 when the sqrt(p_succ) advantage is absent. This is Ambainis-consistent:
Theorem 1 explicitly notes the improvement requires small p_succ.

*HHL regime (p_succ ~ 1/κ, mimicking HHL step-3 amplitude)*:
- standard AA scales as **κ^{1.502}** (Ambainis expects κ · √κ = κ^{1.5} ✓)
- VTAA scales as **κ^{1.112}** (Ambainis expects κ · polylog κ ✓)
- Speedup Q_std / Q_var grows as κ^{0.39}. At κ=8192 the observed speedup is
  9.1× and still rising with κ (crossover at κ*≈128 in the toy).

**These exponents match Ambainis's Theorem 1 and Theorem 3 claims within
~1% (standard) and consistent-up-to-logs (VTAA).**

## What was NOT reproduced

- The full HHL-with-VTAA quantum algorithm running actual eigenvalue
  estimation with the doubling schedule against a real Hamiltonian.
- The exact log³ κ vs log^{1.5}(T_max) log(κ) constants — we test only the
  leading polynomial factor.
- The Aaronson–Ambainis Lemma 1 tighter-Grover analysis (used as a black
  box; our simulation counts abstract "query proxy" units, not Lemma-1
  amplified rotations).

Justification: verdict is **PARTIAL** (per brief), scoped to the core VTAA
scaling law that underlies the O(κ²)→O(κ log³ κ) HHL improvement.

## Estimated effort

- Wall time: ~65 minutes (1 attempt required regime re-tuning).
- Compute: single CPU core, <1 second total for all Qiskit simulations.
- Storage: ~350 KB (paper.pdf 240 KB, evidence 100 KB, extractions 20 KB).
- Free endpoints only (Argo Opus 4.7 for reasoning, all data pulled from arXiv).
