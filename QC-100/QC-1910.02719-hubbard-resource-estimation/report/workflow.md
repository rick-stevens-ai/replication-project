# Workflow — QC-1910.02719 Cai Hubbard HVA Resource Estimation

## Environment

- Host: `m1` (CherryRd), macOS
- Python: 3.12 in local venv
- Key packages: `openfermion 1.7.1`, `cirq 1.7.0`, `numpy 2.3.4`, `scipy 1.16.4`
- LLM judge: local Argo proxy (`http://127.0.0.1:44497`, key `stevens`, model `argo:gpt-5.1`) — **free endpoint only**

## Setup

```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-1910.02719-hubbard-resource-estimation
python3.12 -m venv venv
source venv/bin/activate
pip install openfermion cirq numpy scipy
```

## Fetch paper

```bash
mkdir -p work && cd work
curl -sL -o 1910.02719.pdf https://arxiv.org/pdf/1910.02719
pdftotext -raw 1910.02719.pdf 1910.02719.raw.txt
pdftotext -layout 1910.02719.pdf 1910.02719.txt
```

## Step 1 — Closed-form gate-count + runtime formulas (C1, C2)

```bash
python code/formula_check.py
# → report/evidence/formula_check.json
```

Evaluates `N_1q(V) = 4·V^{3/2} + 7V − 4√V` and `N_2q(V) = 8·V^{3/2} + V − 4√V`
at `V ∈ {4, 6, 9, 12, 16, 20, 25, 30, 36, 49}`. Cross-checks headline `V=25` against
paper: `N_1q ≈ 650`, `N_2q ≈ 1000`, `T ≈ 45 τ_1q + 80 τ_2q`.

## Step 2 — OpenFermion Hubbard construction + qubit count + exact diag (C3)

```bash
python code/hubbard_vqe_small.py
# → report/evidence/hubbard_small_runs.json
```

For each `(L_x, L_y) ∈ {(2,2), (2,3)}`:
1. `openfermion.hamiltonians.fermi_hubbard(x_dim, y_dim, tunneling=1.0, coulomb=4.0, spinless=False)`
2. `openfermion.transforms.jordan_wigner`
3. `openfermion.count_qubits` — measures `N` directly (verifies `N = 2V`)
4. `openfermion.linalg.get_ground_state` — exact-diag `E_0`

## Step 3 — End-to-end small HVA VQE (C5)

```bash
python code/hubbard_vqe_run.py
# → report/evidence/hubbard_vqe_runs.json
```

For `V ∈ {4, 6}`, block depths `p ∈ {1, 2, 3}`:
- Initial state = Slater determinant of the `U=0` Hubbard.
- Ansatz = `p` blocks of `exp(-iθ_v H_v) · exp(-iθ_h H_h) · exp(-iθ_U H_U)`
  (first-order Trotter HVA).
- Optimise with `scipy.optimize.minimize` (L-BFGS-B, 200 iters).
- Report `E_VQE`, `E_0`, relative error.

## Step 4 — Boundary-check counter (kept for transparency, undercounts)

```bash
python code/count_hva_gates.py
# → report/evidence/hva_gate_counts.json
```

Combinatorial primitive counter. Undercounts vs. closed form by an amount
`≈ 4√V · L` due to a boundary `Z`-rotation cancellation the paper treats in
a footnote. Left in the repo as an honest artefact; authoritative check is
against the closed form (Step 1).

## Step 5 — LLM-judge scoring (free endpoint only)

```bash
python code/judge_argo.py
# → report/evidence/judge_argo.json
```

Passes all evidence JSON to `argo:gpt-5.1` (`temperature=0.1`) as a scientific
replication reviewer. Returns `{C1_verified, C2_verified, C3_verified,
vqe_run_end_to_end, verdict, one_line}`.

## Reproduction time

- Fresh venv install: ~2 min
- All scripts sequential (formula_check → hubbard_vqe_small → hubbard_vqe_run → count_hva_gates → judge): **~30 seconds** total (dominated by the two 2×3 exact-diag calls at ~0.3 s and the VQE optimisations at ~5 s).
- LLM judge: ~10 s.

## Endpoint policy

All computation local (no cloud). Only LLM call is against the local Argo proxy
(`argo:gpt-5.1` — free). No paid endpoints touched.
