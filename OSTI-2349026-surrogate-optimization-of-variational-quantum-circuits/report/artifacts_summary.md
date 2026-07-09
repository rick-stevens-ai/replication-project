# Artifacts Summary — OSTI-2349026 Replication

**Paper:** Gustafson et al., "Surrogate optimization of variational quantum circuits," *PNAS* **122**(36), e2408530122 (2 Sep 2025). DOI 10.1073/pnas.2408530122. OSTI-2349026.

**Verdict:** PARTIAL.

## 1. Inputs (fetched, unmodified)

| Artifact | Path | Source | Size | MD5 |
|---|---|---|---:|---|
| Paper PDF | `work/paper.pdf` | https://www.osti.gov/servlets/purl/2349026 | 5,025,832 B | `df95983131d50dbedc1c5bca5900ad7a` |
| Paper text | `work/paper.txt` | `pdftotext -layout work/paper.pdf` | 659 lines | — |
| STALK code tarball | `work/code/stalk-v0.1.tar.gz` | https://codeload.github.com/QMCPACK/stalk/tar.gz/refs/tags/v0.1 | 181,488 B | `b7e6e413603b24dfd34082c5b97d9b10` |
| STALK code extracted | `work/code/stalk-0.1/` | tar xz | — | — |

All inputs are free/open and no API keys were used.

## 2. Environment

| Component | Version |
|---|---|
| Python | 3.12.13 |
| venv | `work/venv/` |
| numpy | 2.5.0 |
| scipy | 1.18.0 |
| qiskit | 2.5.0 |
| qiskit-aer | 0.17.2 |

## 3. Replication code (produced)

| Script | Purpose |
|---|---|
| `work/replicate_vqe_ising.py` | v1 single-seed run at sigma=1e-3, Ns=4, 6 optimizers |
| `work/replicate_vqe_ising_v2.py` | v2 5-seed threshold benchmark at sigma=5e-4, Ns=4 |

Both scripts implement:
- TFIM Hamiltonian (paper Eq. 2) at Ns=4, J1=1.0, J2=0.9, ht=0.4, PBC.
- 4-parameter hardware-efficient ansatz (paper Eq. 5-6): alternating even/odd XY+ZY entanglers.
- Exact statevector cost, additive Gaussian noise for the "high-level" channel.
- SurrogateLS: FD Hessian on smooth surrogate, eigendecomposition, per-direction 7-point parabolic fit line search on noisy cost.
- Baselines via `scipy.optimize.minimize`: Powell, BFGS, COBYLA, CG, SLSQP.

## 4. Reports (produced)

| File | Description |
|---|---|
| `report/REPORT.md` | Canonical narrative report (Markdown) |
| `report/REPORT.tex` | LaTeX report with dedicated Genuine Critique section |
| `report/workflow.md` | End-to-end reproduction steps |
| `report/artifacts_summary.md` | This file — inventory |
| `report/failure_analysis.md` | What did not work and why |
| `report/open_questions.json` | 5 truly open follow-up questions |

## 5. Evidence (produced)

| File | Description |
|---|---|
| `report/evidence/vqe_ising_run.log` | v1 single-seed run log |
| `report/evidence/vqe_ising_results.json` | v1 machine-readable results |
| `report/evidence/vqe_ising_v2_run.log` | v2 5-seed multi-optimizer log |
| `report/evidence/vqe_ising_results_v2.json` | v2 machine-readable results |

## 6. Key numeric results (headline)

- **v1 single seed, sigma=1e-3, Ns=4:**
  - Ansatz variational minimum (noise-free): -0.686093 (true GS: -3.945095).
  - SurrogateLS reaches final gap +0.227 in 84 noisy calls (Powell: +0.003 in 429; COBYLA: +0.012 in 38; BFGS/CG/SLSQP: failed).

- **v2 5-seed median, sigma=5e-4, Ns=4:**
  - Median calls to gap<0.1: Powell 40, COBYLA 11, SurrogateLS 16, BFGS N/A.
  - Speedup vs Powell at gap<0.1: SurrogateLS 2.50×, COBYLA 3.64×.
  - Paper's headline claim: SurrogateLS 2–4× faster than Powell → **direction and magnitude match** on this scaled-down benchmark.

## 7. What is NOT here (deliberate)

- No SWS-based chemistry results — SWS is not part of public STALK v0.1 and no independent URL is given in the paper.
- No IBM `ibm_brisbane` 40-qubit QPU results — paid/gated resource.
- No ExcitationSolve baseline — outside scipy; would require pulling paper ref 95's implementation.
- No MPS-bond-4 surrogate — engineering scope beyond one session; the exact statevector is used as the surrogate instead (biases in favor of SurrogateLS, noted as a limitation).

## 8. Reproducibility

Anyone with Python 3.12, `pip install numpy scipy qiskit qiskit-aer`, and internet access to OSTI + GitHub can rerun the entire pipeline from scratch — no secrets required. Expected numeric reproduction is within the 5-seed uncertainty band reported in Section 4.2 of REPORT.md.

## 9. Storage footprint

| Category | Approx size |
|---|---:|
| Inputs (PDF + STALK tarball + extracted) | ~6 MB |
| venv | ~700 MB (numpy/scipy/qiskit/qiskit-aer + deps) |
| Evidence logs + JSON | <100 KB |
| Reports (all formats) | ~50 KB |
