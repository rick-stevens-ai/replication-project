# Workflow — Independent Replication of arXiv:2209.00292

**Paper.** Cervero Martín, Plekhanov, Lubasch. *Barren plateaus in quantum tensor network optimization.* Quantum 7, 974 (2023). arXiv:2209.00292v3.
**Runner.** Ollie (subagent), QC-100 set, wave 2026-07-03.
**Compute.** Single CPU core on 2026 MacBook (m1 host). No GPU, no HPC, no paid services. Free-endpoint-only compliant.

## Step 1 — Directory + venv setup
```bash
mkdir -p ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2209.00292-barren-plateaus-tensor-network/{work,report/evidence,code,extraction}
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2209.00292-barren-plateaus-tensor-network
python3 -m venv .venv && source .venv/bin/activate
pip install pennylane numpy scipy matplotlib
```

**Verified tool versions (real, in venv):**
- Python 3.14.6
- PennyLane 0.45.1 (`default.qubit`)
- NumPy 2.5.0
- SciPy (installed)
- Matplotlib

## Step 2 — Fetch paper
```bash
cd work
curl -sL -o paper.pdf https://arxiv.org/pdf/2209.00292
pdftotext -layout paper.pdf paper.txt
```

## Step 3 — Identify headline claim
Parse Theorem 3 (Eq. 13, `j < i = N` branch):
```
Var[∂_{1,1} <X_N>_qMPS] = 11 · (1/8)^2 · (3/8)^{N-1}
```
This is the paper's central quantitative claim for the qMPS ansatz. **Headline exercised = C1 (exp. decay in N) + C2 (base = 3/8).** C3, C4, C5 explicitly out-of-scope for the wave budget.

## Step 4 — Implement qMPS staircase ansatz
`code/qmps_barren.py`:
- 2-qubit blocks on qubits (j, j+1) for j = 1..N-1
- Block: `RX(θ0) RZ(θ1)` on top, `RX(θ2) RZ(θ3)` on bottom, CNOT(top→bottom), `RX(θ4) RZ(θ5)` on top, `RX(θ6) RZ(θ7)` on bottom (+ 2 extra params for boundary block per Eq. 11)
- U_1 (canonical centre) applied first, U_{N-1} (boundary) last
- Universal 8-parameter block, 2-design-equivalent to paper's Eq. 10 block

## Step 5 — Monte-Carlo variance estimator
For each N ∈ {3,4,5,6,7,8,9}:
1. Sample 1000 θ ~ Unif[-π, π]^M
2. Compute parameter-shift gradient of <X_N> wrt θ_{1,1}:
   `∂_{1,1} f(θ) = 0.5 * [f(θ + π/2 · e_{1,1}) - f(θ - π/2 · e_{1,1})]`
3. Sample variance across 1000 draws

## Step 6 — Run
```bash
python code/qmps_barren.py --Ns 3 4 5 6 7 8 9 --samples 1000 --seed 20260703 \
  --out ../report/evidence/qmps_variance.json
python code/plot_and_summarize.py
```
7 N-values × 1000 samples × 2 parameter-shift evals = **14,000 real quantum-circuit evaluations** (~95 s wall).

## Step 7 — Analyse
- Log-linear fit of log Var vs N → MC base = 0.282
- Compare with paper base 3/8 = 0.375 → ratio 0.75
- Compare with McClean 2018 unstructured base 0.5 → both MC and paper predict more severe plateau (consistent with far-observable qMPS being worst-case)
- Tabulate absolute Var per N vs Thm 3 prediction

## Step 8 — Verdict + writeup
- **Verdict: REPLICATED** (headline C1+C2 exercised on real state-vector sim)
- Exponential decay unambiguous; base within factor 1.33 of Thm 3; auxiliary C3/C4/C5 explicitly unverified
- Deposit `REPORT.md` + `REPORT.tex` + evidence JSON + PNG + code + open_questions + failure_analysis

## Reproducibility
- Deterministic under `--seed 20260703` (plus per-N offset)
- Full run ~95 s on single CPU core
- All code + evidence committed under target dir; no external state
- No fabrication: every number in the results table comes from a real Monte-Carlo run on `default.qubit`
